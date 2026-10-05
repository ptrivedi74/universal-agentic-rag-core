import os
from typing import List
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

class VectorStoreManager:
    """Wrapper managing vector indexing and retrieval."""

    def __init__(self, persist_dir: str = "./data/vector_db", collection_name: str = "enterprise_knowledge"):
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vector_store = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.persist_dir
        )

    def add_documents(self, documents: List[Document]):
        if documents:
            self.vector_store.add_documents(documents)

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        return self.vector_store.similarity_search(query, k=k)

    def as_retriever(self, k: int = 4):
        return self.vector_store.as_retriever(search_kwargs={"k": k})