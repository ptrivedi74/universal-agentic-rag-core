import tiktoken

class CostTracker:
    """Tracks token consumption and estimates API invocation cost."""
    
    def __init__(self, model_name: str = "gpt-4o-mini", cost_in: float = 0.00015, cost_out: float = 0.00060):
        self.model_name = model_name
        self.cost_in = cost_in / 1000.0
        self.cost_out = cost_out / 1000.0
        try:
            self.encoder = tiktoken.encoding_for_model(model_name)
        except Exception:
            self.encoder = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> int:
        return len(self.encoder.encode(text))

    def calculate_cost(self, prompt_tokens: int, completion_tokens: int) -> dict:
        input_cost = prompt_tokens * self.cost_in
        output_cost = completion_tokens * self.cost_out
        total_cost = input_cost + output_cost
        return {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
            "estimated_cost_usd": round(total_cost, 6)
        }