"""
CLI Execution Entry Point
-------------------------
Use this script for terminal testing, interactive debugging, and evaluating 
agentic RAG workflows locally.

Usage:
    python -m src.main --query "Your test question here"
"""



import sys
import argparse
from src.agents.retriever import AgenticRAGGraph

def run_query(query_text: str):
    print(f"\n--- Processing Query: '{query_text}' ---")
    app = AgenticRAGGraph().build_graph()
    initial_state = {"query": query_text}
    
    result = app.invoke(initial_state)
    
    print("\n--- Final Answer ---")
    print(result.get("generation", "No response generated."))
    
    print("\n--- Cost & Token Metrics ---")
    metrics = result.get("metrics", {})
    for k, v in metrics.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Universal Agentic RAG Pipeline")
    parser.add_argument("--query", type=str, required=True, help="Query string to execute")
    args = parser.parse_args()
    
    run_query(args.query)
