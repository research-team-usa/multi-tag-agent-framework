"""Main orchestrator tying router, stack and LLM together."""

from typing import Any, Optional

from src.amplifier import AmplifierStack
from src.auron import TagRouter

class AgentOrchestrator:
    """Process input through routing and amplification."""

    def __init__(self, llm_client: Any, router: Optional[TagRouter] = None,
                 stack: Optional[AmplifierStack] = None) -> None:
        self.llm_client = llm_client
        self.router = router or TagRouter()
        self.stack = stack or AmplifierStack()

    def process(self, input_text: str, fixture: Optional[str] = None) -> Any:
        """Route, amplify and call LLM."""
        tag = self.router.route(input_text)
        self.stack.push({"input": input_text, "tag": tag})
        # fixture wird von deinen Tests genutzt
        return self.llm_client.complete(input_text, fixture or tag)