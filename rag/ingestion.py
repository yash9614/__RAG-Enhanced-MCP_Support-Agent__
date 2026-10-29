"""Document ingestion pipeline."""
from pathlib import Path
from typing import List

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.vectorstore import KnowledgeVectorStore
from rag.embeddings import get_embeddings


def load_documents(path: Path) -> List:
    docs = []
    for file in path.rglob("*"):
        if file.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(file))
        elif file.suffix.lower() in {".md", ".markdown"}:
            loader = UnstructuredMarkdownLoader(str(file))
        elif file.suffix.lower() in {".txt", ".md"}:
            loader = TextLoader(str(file))
        else:
            continue
        docs.extend(loader.load())
    return docs


def ingest(path: str = "knowledge/docs", chunk_size: int = 1000, chunk_overlap: int = 200):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Knowledge path not found: {path}")

    raw_docs = load_documents(path)
    if not raw_docs:
        print("No documents found.")
        return

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunks = splitter.split_documents(raw_docs)

    embeddings = get_embeddings()
    store = KnowledgeVectorStore(embeddings=embeddings)
    store.add_documents(chunks)

    print(f"Ingested {len(chunks)} chunks from {len(raw_docs)} documents.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default="knowledge/docs")
    args = parser.parse_args()
    ingest(args.path)
