from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.agents.router import IntentRouter
from src.agents.evaluator import ContextEvaluator
from src.vectorstore.store import VectorStoreManager
from src.governance.pii_sanitizer import PIISanitizer
from src.governance.cost_tracker import CostTracker

class AgentState(Dict[str, Any]):
    """LangGraph state object."""

class AgenticRAGGraph:
    """LangGraph Self-Corrective RAG Orchestrator."""

    def __init__(self):
        self.router = IntentRouter()
        self.evaluator = ContextEvaluator()
        self.vstore = VectorStoreManager()
        self.sanitizer = PIISanitizer()
        self.tracker = CostTracker()
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

    def route_node(self, state: AgentState) -> str:
        destination = self.router.route(state["query"])
        return "retrieve" if destination == "vectorstore" else "generate_direct"

    def retrieve_node(self, state: AgentState) -> AgentState:
        docs = self.vstore.similarity_search(state["query"], k=4)
        state["documents"] = docs
        return state

    def evaluate_node(self, state: AgentState) -> AgentState:
        query = state["query"]
        docs = state.get("documents", [])
        valid_docs = []
        
        for d in docs:
            if self.evaluator.evaluate(query, d.page_content):
                valid_docs.append(d)
        
        state["documents"] = valid_docs
        state["is_relevant"] = len(valid_docs) > 0
        return state

    def generate_node(self, state: AgentState) -> AgentState:
        query = self.sanitizer.sanitize(state["query"])
        docs = state.get("documents", [])
        context = "\n\n".join([d.page_content for d in docs]) if docs else "No relevant internal context found."

        prompt = ChatPromptTemplate.from_messages([
            ("system", "Answer the question using the provided context clearly and concisely."),
            ("human", "Context:\n{context}\n\nQuestion: {query}")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({"context": context, "query": query})
        
        # Track Usage
        prompt_tokens = self.tracker.count_tokens(context + query)
        completion_tokens = self.tracker.count_tokens(response.content)
        usage = self.tracker.calculate_cost(prompt_tokens, completion_tokens)

        state["generation"] = response.content
        state["metrics"] = usage
        return state

    def build_graph(self):
        workflow = StateGraph(AgentState)

        workflow.add_node("retrieve", self.retrieve_node)
        workflow.add_node("evaluate", self.evaluate_node)
        workflow.add_node("generate", self.generate_node)

        workflow.set_conditional_entry_point(
            self.route_node,
            {"retrieve": "retrieve", "generate_direct": "generate"}
        )

        workflow.add_edge("retrieve", "evaluate")
        workflow.add_edge("evaluate", "generate")
        workflow.add_edge("generate", END)

        return workflow.compile()