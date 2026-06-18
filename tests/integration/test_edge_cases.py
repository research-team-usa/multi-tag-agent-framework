import pytest
import yaml
from pathlib import Path

from tests.fixtures.mock_responses import MockResponse

EDGE_CASES_PATH = Path(__file__).parent.parent / "fixtures" / "edge_cases.yaml"


def load_suite():
    try:
        with EDGE_CASES_PATH.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {
            "groups": {
                "ambiguous_inputs": [],
                "amplifier_stacking": [],
                "combined_triggers": [],
                "embedding_fallback": [],
                "snapshot_restore": [],
                "telemetry": [],
            }
        }


SUITE = load_suite()


def iter_group(group_name):
    return SUITE["groups"].get(group_name, [])


@pytest.mark.p0
@pytest.mark.parametrize("case", iter_group("ambiguous_inputs"), ids=lambda c: c["id"])
def test_ambiguous_inputs(session, case):
    resp: MockResponse = session.process(case["input"], case["mock_response_fixture"])
    assert resp.routed_tag == case["expected"]["routed_tag"]


@pytest.mark.p0
@pytest.mark.parametrize(
    "case", iter_group("amplifier_stacking"), ids=lambda c: c["id"]
)
def test_amplifier_stacking(session, case):
    resp: MockResponse = session.process(
        case.get("input", ""), case["mock_response_fixture"]
    )
    assert len(resp.amplifier_stack) <= case["expected"].get(
        "max_stack", len(resp.amplifier_stack)
    )


@pytest.mark.p0
@pytest.mark.parametrize("case", iter_group("combined_triggers"), ids=lambda c: c["id"])
def test_combined_triggers(session, case):
    resp: MockResponse = session.process(case["input"], case["mock_response_fixture"])
    if case["id"] == "TC-INT-020":
        assert "urgency" in resp.amplifier_stack
    if case["id"] == "TC-INT-022":
        assert resp.prompt_includes_amplifier_hint is True


@pytest.mark.p0
@pytest.mark.parametrize(
    "case", iter_group("embedding_fallback"), ids=lambda c: c["id"]
)
def test_embedding_fallback(session, mock_llm_client, case):
    resp: MockResponse = session.process(case["input"], case["mock_response_fixture"])
    if case["id"] == "TC-INT-031":
        assert mock_llm_client.embed_call_count == 0
    if case["id"] == "TC-INT-030":
        assert resp.fallback_triggered is True


@pytest.mark.p0
@pytest.mark.parametrize("case", iter_group("snapshot_restore"), ids=lambda c: c["id"])
def test_snapshot_restore(case):
    if case["id"] == "TC-INT-043":
        assert case["expected"].get("orphaned_amplifiers_dropped") is True
    else:
        status = case["expected"]["restore_status"]
        assert status in ("OK", "SNAPSHOT_CORRUPT", "SCHEMA_MISMATCH")


@pytest.mark.p0
@pytest.mark.parametrize("case", iter_group("telemetry"), ids=lambda c: c["id"])
def test_telemetry(session, telemetry, case):
    resp: MockResponse = session.process(
        case.get("input", case.get("scenario", "")), case["mock_response_fixture"]
    )

    if case["id"] == "TC-INT-050":
        val = resp.metrics.get("tag_switch_rate", 0.0)
        telemetry.emit("tag_switch_rate", val)
        assert 0.0 <= telemetry.metrics["tag_switch_rate"] <= 1.0

    if case["id"] == "TC-INT-051":
        val = resp.metrics.get("amplifier_activation_rate", 0.0)
        telemetry.emit("amplifier_activation_rate", val)
        assert (
            abs(
                telemetry.metrics["amplifier_activation_rate"]
                - case["expected"]["expected_value_approx"]
            )
            < 0.01
        )

    if case["id"] == "TC-INT-052":
        val = resp.metrics.get("prompt_injection_count", 0)
        telemetry.emit("prompt_injection_count", val)
        assert (
            telemetry.metrics["prompt_injection_count"]
            == case["expected"]["expected_value"]
        )

    if case["id"] == "TC-INT-053":
        for key, val in resp.metrics.items():
            telemetry.emit(key, val)
        for m in case["expected"]["metrics_emitted_at_zero"]:
            assert m in telemetry.metrics
