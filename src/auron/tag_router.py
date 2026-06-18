"""Tag-based router for multi-agent framework."""

from typing import Dict, List

class TagRouter:
    """Route inputs to tags like billing, payments, incident."""

    def __init__(self) -> None:
        self.rules: Dict[str, List[str]] = {
            "billing": ["invoice", "bill", "charge", "payment due", "rechnung"],
            "payments": ["pay", "refund", "transaction", "credit card", "paypal"],
            "incident": ["error", "down", "outage", "bug", "fail", "crash"],
        }

    def route(self, text: str) -> List[str]:
        """Return matching tags for input text."""
        text_lower = text.lower()
        tags = [
            tag
            for tag, keywords in self.rules.items()
            if any(keyword in text_lower for keyword in keywords)
        ]
        return tags or ["general"]