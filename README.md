# Universal Agentic RAG Core (`universal-agentic-rag-core`)

A modular, domain-agnostic Python reference architecture for building production-grade **Agentic Retrieval-Augmented Generation (RAG)** pipelines. 

Designed for enterprise deployment, this core engine combines **LangGraph orchestration**, **Corrective RAG (CRAG)** self-correction loops, **hybrid vector retrieval**, and **enterprise LLM guardrails** (PII redaction and token cost management).

---

## Key Architecture & Workflow

```text
    DOCUMENT INPUTS                     USER / API PROMPT
 (PDF, MD, CSV, JSON, TXT)            (Natural Language Query)
            │                                     │
            ▼                                     ▼
┌───────────────────────┐            ┌────────────────────────┐
│  Universal Document   │            │   Query Classifier &   │
│   Ingestion & Chunk   │            │   Intent Router Agent  │
└───────────┬───────────┘            └───────────┬────────────┘
            │                                    │
            ▼                                    ▼
┌───────────────────────┐            ┌────────────────────────┐
│ Hybrid Vector Store   │◄───────────┤ Adaptive RAG Retriever │
│ (ChromaDB / Qdrant)   │            │   (Dense + Sparse)     │
└───────────────────────┘            └───────────┬────────────┘
                                                 │
                                                 ▼
                                     ┌────────────────────────┐
                                     │ Self-Correction Agent  │
                                     │ (Re-rank & Relevance)  │
                                     └───────────┬────────────┘
                                                 │
                                                 ▼
                                     ┌────────────────────────┐
                                     │  Response Generator &  │
                                     │ Guardrails (PII/Audit) │
                                     └────────────────────────┘

## **Adapting This Engine for Your Own Projects**

This repository is built with a plug-and-play modular architecture. You can easily adapt it for your custom domain, custom LLM providers, or existing vector databases in three steps:

### 1. **Connecting Your Own Document Sources**
Replace the sample files in `data/sample_docs/` with your own project documentation (`.pdf`, `.md`, `.txt`, `.csv`, `.json`).

To trigger chunking and vector indexing programmatically within your own Python application:

```python
from src.ingestion.loader import UniversalDocumentLoader
from src.vectorstore.store import VectorStoreManager

# Load and split your custom documents
loader = UniversalDocumentLoader(chunk_size=1000, chunk_overlap=150)
chunks = loader.load_directory("./path/to/your/custom_docs")

# Index into ChromaDB
vstore = VectorStoreManager(persist_dir="./data/vector_db")
vstore.add_documents(chunks)
