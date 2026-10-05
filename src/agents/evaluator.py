from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class GradeDocument(BaseModel):
    """Binary score for document relevance check."""
    score: str = Field(description="Relevance score: 'yes' or 'no'")

class ContextEvaluator:
    """Grades whether retrieved context is relevant to the prompt."""

    def __init__(self, model_name: str = "gpt-4o-mini"):
        llm = ChatOpenAI(model=model_name, temperature=0)
        self.structured_llm = llm.with_structured_output(GradeDocument)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a quality evaluator. Grade if the document context is relevant to user query. Output 'yes' or 'no'."),
            ("human", "Context: {context}\n\nQuery: {query}")
        ])
        self.chain = self.prompt | self.structured_llm

    def evaluate(self, query: str, context: str) -> bool:
        res = self.chain.invoke({"query": query, "context": context})
        return res.score.lower() == "yes"