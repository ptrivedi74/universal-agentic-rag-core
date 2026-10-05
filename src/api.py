"""
REST API Web Service Endpoint
-----------------------------
FastAPI application exposing the Agentic RAG engine as an HTTP service.

Usage:
    uvicorn src.api:app --reload --port 8000
"""


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agents.retriever import AgenticRAGGraph

app = FastAPI(title="Custom Agentic RAG Service")
rag_graph = AgenticRAGGraph().build_graph()

class QueryRequest(BaseModel):
    query: str

@app.post("/api/v1/chat")
async def chat_endpoint(request: QueryRequest):
    try:
        initial_state = {"query": request.query}
        result = rag_graph.invoke(initial_state)
        return {
            "response": result.get("generation"),
            "metrics": result.get("metrics")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
