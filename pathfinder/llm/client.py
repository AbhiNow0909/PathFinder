# llm/client.py
"""
Centralized LLM client — all LLM calls go through here.
Uses Groq API with llama-3.3-70b-versatile.
"""

from __future__ import annotations

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

_client: Groq | None = None


def _get_client() -> Groq:
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY not set. Add it to your .env file:\n"
                "  GROQ_API_KEY=gsk_..."
            )
        _client = Groq(api_key=api_key)
    return _client


def chat(
    messages: list[dict],
    model: str = "llama-3.3-70b-versatile",
    temperature: float = 0.3,
) -> str:
    """
    Send a chat completion request and return the response text.
    All agents call this instead of ollama directly.
    """
    client = _get_client()
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content.strip()
