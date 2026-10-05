from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class RouteQuery(BaseModel):
    """Route user query to appropriate handling node."""
    destination: str = Field(
        description="Choose 'vectorstore' for domain knowledge questions, or 'direct' for general prompts/greetings."
    )

class IntentRouter:
    """Evaluates query intent to route execution flow."""

    def __init__(self, model_name: str = "gpt-4o-mini"):
        llm = ChatOpenAI(model=model_name, temperature=0)
        self.structured_llm = llm.with_structured_output(RouteQuery)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert intent router. Classify if the query requires internal database lookup."),
            ("human", "{query}")
        ])
        self.chain = self.prompt | self.structured_llm

    def route(self, query: str) -> str:
        res = self.chain.invoke({"query": query})
        return res.destination