# rag/ingest.py
"""
One-time ingestion script for the PathFinder RAG corpus.

Reads all .md files from rag/corpus/clrs/ and .txt files from rag/corpus/gfg/,
chunks them, tags each chunk with a DSA concept label, embeds them with
all-MiniLM-L6-v2, and persists the ChromaDB collection to rag/chroma_db/.

Run once (or whenever corpus changes):
    python -m rag.ingest
"""

from __future__ import annotations

import os
import re
from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# ── Paths ─────────────────────────────────────────────────────────────────────

_RAG_DIR   = Path(__file__).resolve().parent
_CLRS_DIR  = _RAG_DIR / "corpus" / "clrs"
_GFG_DIR   = _RAG_DIR / "corpus" / "gfg"
_CHROMA_DIR = _RAG_DIR / "chroma_db"

COLLECTION_NAME = "dsa_curriculum"
CHUNK_SIZE      = 500   # characters
CHUNK_OVERLAP   = 50    # characters

# ── Concept tag maps ──────────────────────────────────────────────────────────
# Maps CLRS filename stems → graph concept
CLRS_FILE_TO_CONCEPT: dict[str, str] = {
    # arrays / basic structures
    "arrays_stacks_queues":          "arrays",
    "direct_address_tables":         "arrays",

    # linked_list
    "linked_lists":                  "linked_list",
    "rooted_tree_representation":    "linked_list",

    # stack_queue  (covered by arrays_stacks_queues above too)
    "priority_queues":               "stack_queue",
    "dynamic_tables":                "stack_queue",

    # sorting
    "insertion_sort":                "sorting",
    "heapsort_algorithm":            "sorting",
    "quicksort_algorithm":           "sorting",
    "quicksort_analysis":            "sorting",
    "quicksort_performance":         "sorting",
    "randomized_quicksort":          "sorting",
    "merge_sort":                    "sorting",
    "counting_sort":                 "sorting",
    "radix_sort":                    "sorting",
    "bucket_sort":                   "sorting",
    "sorting_lower_bounds":          "sorting",

    # binary_search
    "binary_search_tree_intro":      "binary_search",
    "bst_search":                    "binary_search",
    "bst_insertion_deletion":        "binary_search",
    "expected_linear_selection":     "binary_search",
    "worst_case_linear_selection":   "binary_search",

    # hashing
    "hash_tables":                   "hashing",
    "hash_functions":                "hashing",
    "hashing_practical_considerations": "hashing",
    "open_addressing":               "hashing",

    # heap
    "heap_data_structure":           "heap",
    "heap_operations":               "heap",

    # recursion
    "divide_and_conquer_paradigm":   "recursion",
    "recurrence_substitution_method": "recursion",
    "recurrence_recursion_tree":     "recursion",
    "master_method":                 "recursion",
    "advanced_recurrences":          "recursion",
    "strassens_algorithm":           "recursion",
    "matrix_multiplication":         "recursion",

    # backtracking
    "algorithm_design_strategies":   "backtracking",

    # trees
    "data_structure_augmentation":   "trees",
    "order_statistic_trees":         "trees",
    "order_statistics_basics":       "trees",
    "interval_trees":                "trees",
    "optimal_bst":                   "trees",

    # balanced_trees
    "red_black_tree_properties":     "balanced_trees",
    "red_black_tree_rotations":      "balanced_trees",
    "red_black_tree_insertion":      "balanced_trees",
    "red_black_tree_deletion":       "balanced_trees",
    "b_tree_definition":             "balanced_trees",
    "b_tree_operations":             "balanced_trees",
    "b_tree_deletion":               "balanced_trees",

    # graphs
    "graph_representations":         "graphs",
    "breadth_first_search":          "graphs",
    "depth_first_search":            "graphs",
    "topological_sort":              "graphs",
    "strongly_connected_components": "graphs",
    "dag_shortest_paths":            "graphs",
    "bellman_ford":                  "graphs",
    "dijkstra_algorithm":            "graphs",
    "difference_constraints":        "graphs",
    "apsp_matrix_multiplication":    "graphs",
    "floyd_warshall":                "graphs",
    "johnsons_algorithm":            "graphs",
    "minimum_spanning_tree_intro":   "graphs",
    "kruskal_and_prim":              "graphs",
    "flow_networks":                 "graphs",
    "ford_fulkerson":                "graphs",
    "maximum_bipartite_matching":    "graphs",
    "disjoint_set_operations":       "graphs",
    "disjoint_set_linked_list":      "graphs",
    "disjoint_set_forests":          "graphs",
    "path_compression_analysis":     "graphs",

    # greedy
    "greedy_activity_selection":     "greedy",
    "greedy_strategy_properties":    "greedy",
    "huffman_coding":                "greedy",
    "offline_caching":               "greedy",

    # dynamic_programming
    "dynamic_programming_intro":     "dynamic_programming",
    "dp_principles":                 "dynamic_programming",
    "longest_common_subsequence":    "dynamic_programming",
    "matrix_chain_multiplication":   "dynamic_programming",
    "optimal_bst":                   "dynamic_programming",  # also trees

    # general / analysis (not mapped to a specific concept)
    "algorithm_analysis_intro":      "general",
    "algorithms_intro":              "general",
    "asymptotic_notation":           "general",
    "common_growth_functions":       "general",
    "probabilistic_analysis":        "general",
    "indicator_random_variables":    "general",
    "aggregate_analysis":            "general",
    "accounting_method":             "general",
    "potential_method":              "general",
}

GFG_FILE_TO_CONCEPT: dict[str, str] = {
    "Array Data Structure":          "arrays",
    "Graph Data Structure":          "graphs",
    "Linked List Data Structure":    "linked_list",
    "Queue Data Structure":          "stack_queue",
    "Stack Data Structure":          "stack_queue",
    "Tree Data Structure":           "trees",
    "Strings":                       "arrays",  # strings are array-based
}

# ── Chunking ──────────────────────────────────────────────────────────────────

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """
    Split text into overlapping character-level chunks.
    Tries to split on paragraph boundaries first to preserve meaning.
    """
    paragraphs = re.split(r"\n{2,}", text.strip())
    chunks: list[str] = []
    current = ""

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if len(current) + len(para) + 2 <= chunk_size:
            current = (current + "\n\n" + para).strip()
        else:
            if current:
                chunks.append(current)
            # If single paragraph exceeds chunk_size, hard-split it
            if len(para) > chunk_size:
                for i in range(0, len(para), chunk_size - overlap):
                    chunks.append(para[i : i + chunk_size])
                current = ""
            else:
                current = para

    if current:
        chunks.append(current)

    return [c for c in chunks if len(c.strip()) > 30]  # drop tiny fragments


# ── Document loader ───────────────────────────────────────────────────────────

def load_documents() -> list[dict]:
    """
    Load all .md (CLRS) and .txt (GFG) files.
    Returns list of {text, concept, source, filename}.
    """
    docs = []

    # CLRS markdown files
    for md_file in sorted(_CLRS_DIR.glob("*.md")):
        stem   = md_file.stem
        concept = CLRS_FILE_TO_CONCEPT.get(stem, "general")
        text   = md_file.read_text(encoding="utf-8", errors="ignore")
        docs.append({
            "text":     text,
            "concept":  concept,
            "source":   "CLRS",
            "filename": md_file.name,
        })

    # GFG text files
    for txt_file in sorted(_GFG_DIR.glob("*.txt")):
        stem    = txt_file.stem
        concept = GFG_FILE_TO_CONCEPT.get(stem, "general")
        text    = txt_file.read_text(encoding="utf-8", errors="ignore")
        docs.append({
            "text":     text,
            "concept":  concept,
            "source":   "GFG",
            "filename": txt_file.name,
        })

    return docs


# ── Main ingestion ─────────────────────────────────────────────────────────────

def ingest() -> None:
    print("=" * 60)
    print("  PathFinder RAG — Corpus Ingestion")
    print("=" * 60)

    # Load documents
    print("\n[1/4] Loading corpus documents…")
    docs = load_documents()
    print(f"  ✔  Loaded {len(docs)} files")

    # Chunk
    print("\n[2/4] Chunking documents…")
    ids, texts, metadatas = [], [], []
    for doc in docs:
        chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(chunks):
            chunk_id = f"{doc['source']}::{doc['filename']}::chunk{i}"
            ids.append(chunk_id)
            texts.append(chunk)
            metadatas.append({
                "concept":  doc["concept"],
                "source":   doc["source"],
                "filename": doc["filename"],
                "chunk_idx": i,
            })
    print(f"  ✔  {len(texts)} chunks created from {len(docs)} files")

    # Set up ChromaDB
    print("\n[3/4] Initialising ChromaDB + SentenceTransformer embeddings…")
    print("       (First run downloads all-MiniLM-L6-v2 — ~90MB, one-time only)")
    embed_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    client   = chromadb.PersistentClient(path=str(_CHROMA_DIR))

    # Drop existing collection to avoid duplicate IDs on re-run
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=embed_fn,
        metadata={"hnsw:space": "cosine"},
    )

    # Embed & store in batches (ChromaDB recommends ≤5000 per batch)
    print("\n[4/4] Embedding and storing chunks…")
    BATCH = 200
    for start in range(0, len(texts), BATCH):
        end = start + BATCH
        collection.add(
            ids=ids[start:end],
            documents=texts[start:end],
            metadatas=metadatas[start:end],
        )
        print(f"  …stored chunks {start}–{min(end, len(texts))-1}")

    print(f"\n{'='*60}")
    print(f"  ✔  Ingestion complete!")
    print(f"     {len(texts)} chunks from {len(docs)} files")
    print(f"     Persisted to: {_CHROMA_DIR}")
    print(f"{'='*60}")


if __name__ == "__main__":
    ingest()
