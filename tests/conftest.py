"""Pytest fixtures for Multi-Tag Agent Framework tests."""

import pytest

from tests.fixtures.mock_responses import MockLLMClient


@pytest.fixture(scope="session")
def mock_llm_client():
    """Provide a session-wide mock LLM client."""
    return MockLLMClient()


@pytest.fixture
def session(mock_llm_client):
    """Provide a dummy session that routes to the mock client."""
    # pylint: disable=redefined-outer-name

    class DummySession:
        """Minimal session for testing routing."""

        def __init__(self, client):
            self.client = client

        def process(self, message: str, fixture: str):
            """Process a message using the mock client."""
            return self.client.complete(message, fixture)

        def reset(self):
            """Reset session state."""
            pass

    return DummySession(mock_llm_client)


@pytest.fixture
def amp_stack():
    """Provide an empty amplifier stack."""
    return []


@pytest.fixture
def telemetry():
    """Provide a simple telemetry collector."""

    class Telemetry:
        """Collect metrics in memory."""

        def __init__(self):
            self.metrics = {}

        def emit(self, name, value):
            """Store a metric."""
            self.metrics[name] = value

        def reset(self):
            """Clear metrics."""
            self.metrics.clear()

    return Telemetry()


@pytest.fixture
def test_workflow_context():
    """Provide a static workflow context."""
    return {
        "workflow_id": "wf-test-001",
        "tags": ["audit", "security"],
        "timestamp": "2026-06-17T12:00:00Z",
    }


@pytest.fixture
def audit_log(tmp_path):
    """Provide a temporary audit log file."""
    log_file = tmp_path / "audit.log"
    log_file.touch()
    return log_file


@pytest.fixture(autouse=True)
def reset_state(session, amp_stack, telemetry):
    """Reset shared fixtures after each test."""
    # pylint: disable=redefined-outer-name
    yield
    session.reset()
    amp_stack.clear()
    telemetry.reset()
