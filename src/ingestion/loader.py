import os
import glob
from typing import List
from langchain_community.document_loaders import TextLoader, PyPDFLoader, CSVLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class UniversalDocumentLoader:
    """In-gestion pipeline to load multi-format files and produce chunks."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 150):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def load_file(self, file_path: str) -> List[Document]:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".txt":
            loader = TextLoader(file_path, encoding="utf-8")
        elif ext == ".pdf":
            loader = PyPDFLoader(file_path)
        elif ext == ".csv":
            loader = CSVLoader(file_path)
        elif ext in [".md", ".markdown"]:
            loader = UnstructuredMarkdownLoader(file_path)
        else:
            return []
        
        docs = loader.load()
        return self.splitter.split_documents(docs)

    def load_directory(self, dir_path: str) -> List[Document]:
        all_chunks = []
        supported_exts = ["*.txt", "*.pdf", "*.csv", "*.md"]
        for ext in supported_exts:
            for file_path in glob.glob(os.path.join(dir_path, "**", ext), recursive=True):
                chunks = self.load_file(file_path)
                all_chunks.extend(chunks)
        return all_chunks