import pytest
from src.governance.pii_sanitizer import PIISanitizer
from src.governance.cost_tracker import CostTracker

def test_pii_sanitizer():
    sanitizer = PIISanitizer()
    raw_text = "Contact me at john.doe@example.com or 555-123-4567."
    cleaned = sanitizer.sanitize(raw_text)
    
    assert "john.doe@example.com" not in cleaned
    assert "555-123-4567" not in cleaned
    assert "[REDACTED_EMAIL]" in cleaned
    assert "[REDACTED_PHONE]" in cleaned

def test_cost_tracker():
    tracker = CostTracker(model_name="gpt-4o-mini")
    tokens = tracker.count_tokens("Hello world from unit test")
    assert tokens > 0
    
    cost_data = tracker.calculate_cost(100, 50)
    assert cost_data["total_tokens"] == 150
    assert cost_data["estimated_cost_usd"] > 0