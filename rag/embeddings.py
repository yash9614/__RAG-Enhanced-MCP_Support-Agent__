"""Embedding helpers."""
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings


def get_embeddings():
    """Prefer OpenAI if key present, else local HuggingFace."""
    if os.getenv("OPENAI_API_KEY"):
        return OpenAIEmbeddings(model="text-embedding-3-small")
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
