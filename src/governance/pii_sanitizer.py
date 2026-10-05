import re

class PIISanitizer:
    """Utility to scrub sensitive entities (PII) before LLM invocation."""
    
    PATTERNS = {
        "email": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        "phone": r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',
        "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
        "credit_card": r'\b(?:\d[ -]*?){13,16}\b'
    }

    def __init__(self, redact_types=None):
        self.redact_types = redact_types or ["email", "phone", "ssn", "credit_card"]

    def sanitize(self, text: str) -> str:
        sanitized_text = text
        for ptype in self.redact_types:
            if ptype in self.PATTERNS:
                pattern = self.PATTERNS[ptype]
                sanitized_text = re.sub(pattern, f"[REDACTED_{ptype.upper()}]", sanitized_text)
        return sanitized_text