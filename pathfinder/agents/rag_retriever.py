# agents/rag_retriever.py
"""
Step 7 of the pipeline: RAG Retrieval (Curriculum Grounding).

For each topic in the ordered plan, retrieves the most relevant curriculum
passages from the ChromaDB vector store (populated by rag/ingest.py).

Retrieval strategy (two-stage):
  1. Metadata filter: WHERE concept == <topic_concept>
     Ensures we only search within relevant topic chunks.
  2. Semantic similarity: cosine similarity ranks filtered chunks;
     top-k are concatenated into a single context string.

Returns a list of CurriculumEntry objects — one per ordered topic —
preserving the same order for the Planning Agent downstream.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from schemas.models import CurriculumEntry, OrderedTopic

# ── ChromaDB setup ────────────────────────────────────────────────────────────

_RAG_DIR    = Path(__file__).resolve().parent.parent / "rag"
_CHROMA_DIR = _RAG_DIR / "chroma_db"
COLLECTION_NAME = "dsa_curriculum"
TOP_K = 3  # number of chunks to retrieve per topic

# Lazy-loaded singletons
_client: Optional[chromadb.PersistentClient] = None
_collection = None
_embed_fn: Optional[SentenceTransformerEmbeddingFunction] = None


def _get_collection():
    """Return (and lazily initialise) the ChromaDB collection."""
    global _client, _collection, _embed_fn

    if _collection is not None:
        return _collection

    if not _CHROMA_DIR.exists():
        raise RuntimeError(
            f"ChromaDB not found at {_CHROMA_DIR}.\n"
            "Run ingestion first:  python -m rag.ingest"
        )

    _embed_fn   = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    _client     = chromadb.PersistentClient(path=str(_CHROMA_DIR))
    _collection = _client.get_collection(
        name=COLLECTION_NAME,
        embedding_function=_embed_fn,
    )
    return _collection


# ── Core retrieval ────────────────────────────────────────────────────────────

def _retrieve_for_concept(concept: str, query: str) -> tuple[str, str]:
    """
    Retrieve top-k chunks for a concept.

    Returns (context_text, source_reference) where:
      - context_text: concatenated top-k passages
      - source_reference: e.g. "CLRS (dynamic_programming_intro.md)"
    """
    collection = _get_collection()

    try:
        # Two-stage: metadata filter + semantic similarity
        results = collection.query(
            query_texts=[query],
            n_results=TOP_K,
            where={"concept": concept},
            include=["documents", "metadatas", "distances"],
        )
    except Exception:
        # Fallback: no metadata filter (concept might be "general" or unmapped)
        results = collection.query(
            query_texts=[query],
            n_results=TOP_K,
            include=["documents", "metadatas", "distances"],
        )

    docs      = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    if not docs:
        return (
            f"No curriculum content found for '{concept}'.",
            "N/A",
        )

    context = "\n\n---\n\n".join(docs)

    # Build a clean source reference from the first result's metadata
    first_meta = metadatas[0] if metadatas else {}
    source   = first_meta.get("source", "Unknown")
    filename = first_meta.get("filename", "")
    reference = f"{source} ({filename})" if filename else source

    return context, reference


# ── Public interface ──────────────────────────────────────────────────────────

def retrieve_curriculum_context(
    ordered_topics: list[OrderedTopic],
) -> list[CurriculumEntry]:
    """
    Step 7: Retrieve curriculum context for each ordered topic.

    Args:
        ordered_topics: Output of run_ordering_loop() — ordered list of topics.

    Returns:
        List[CurriculumEntry], one per topic, in the same order.
    """
    entries: list[CurriculumEntry] = []

    for ot in ordered_topics:
        concept = ot.topic  # topic names ARE graph concept names after ordering loop

        # Query: concept name + skill context give semantic signal
        query = f"{concept} data structure algorithm explanation"

        context, reference = _retrieve_for_concept(concept, query)

        entries.append(CurriculumEntry(
            concept=concept,
            is_target=ot.is_target,
            estimated_hours=ot.estimated_hours,
            context=context,
            reference=reference,
        ))

    return entries
