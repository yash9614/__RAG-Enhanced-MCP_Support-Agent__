"""RAG retrieval helpers."""
from typing import List, Dict, Any

from rag.vectorstore import KnowledgeVectorStore
from rag.embeddings import get_embeddings


def search_knowledge(query: str, top_k: int = 4) -> List[Dict[str, Any]]:
    """Search the knowledge base and return chunks with metadata."""
    embeddings = get_embeddings()
    store = KnowledgeVectorStore(embeddings=embeddings)
    docs = store.similarity_search(query, k=top_k)

    results = []
    for doc in docs:
        results.append({
            "content": doc.page_content,
            "source": doc.metadata.get("source", "unknown"),
            "page": doc.metadata.get("page"),
        })
    return results
