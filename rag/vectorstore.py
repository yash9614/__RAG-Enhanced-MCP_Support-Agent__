"""Vector store wrapper around ChromaDB."""
from pathlib import Path
from typing import List, Optional

import chromadb
from chromadb.config import Settings
from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings


class KnowledgeVectorStore:
    def __init__(
        self,
        persist_directory: str = "chroma_db",
        collection_name: str = "telusko_knowledge",
        embeddings: Optional[Embeddings] = None,
    ):
        self.persist_directory = Path(persist_directory)
        self.collection_name = collection_name
        self.embeddings = embeddings
        self._client = None
        self._store = None

    @property
    def client(self):
        if self._client is None:
            self._client = chromadb.PersistentClient(
                path=str(self.persist_directory),
                settings=Settings(anonymized_telemetry=False),
            )
        return self._client

    def get_store(self) -> Chroma:
        if self._store is None:
            self._store = Chroma(
                client=self.client,
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=str(self.persist_directory),
            )
        return self._store

    def add_documents(self, documents: List, ids: Optional[List[str]] = None):
        store = self.get_store()
        store.add_documents(documents, ids=ids)

    def similarity_search(self, query: str, k: int = 4):
        store = self.get_store()
        return store.similarity_search(query, k=k)

    def as_retriever(self, k: int = 4):
        return self.get_store().as_retriever(search_kwargs={"k": k})
