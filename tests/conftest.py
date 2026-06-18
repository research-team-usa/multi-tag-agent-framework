import pytest

from tests.fixtures.mock_responses import MockLLMClient


@pytest.fixture(scope="session")
def mock_llm_client():
    return MockLLMClient()


@pytest.fixture
def session(mock_llm_client):
    # Replace with your real session/router construction
    class DummySession:
        def __init__(self, client):
            self.client = client

        def process(self, message: str, fixture: str):
            return self.client.complete(message, fixture)

        def reset(self):
            pass

    return DummySession(mock_llm_client)


@pytest.fixture
def amp_stack():
    return []


@pytest.fixture
def telemetry():
    class Telemetry:
        def __init__(self):
            self.metrics = {}

        def emit(self, name, value):
            self.metrics[name] = value

        def reset(self):
            self.metrics.clear()

    return Telemetry()


@pytest.fixture
def test_workflow_context():
    return {
        "workflow_id": "wf-test-001",
        "tags": ["audit", "security"],
        "timestamp": "2026-06-17T12:00:00Z",
    }


@pytest.fixture
def audit_log(tmp_path):
    log_file = tmp_path / "audit.log"
    log_file.touch()
    return log_file


@pytest.fixture(autouse=True)
def reset_state(session, amp_stack, telemetry):
    yield
    session.reset()
    amp_stack.clear()
    telemetry.reset()
