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
