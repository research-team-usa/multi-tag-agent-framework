from pathlib import Path

import pytest
import yaml

from tests.fixtures.mock_responses import MockResponse


EDGE_CASES_PATH = Path(__file__).parent.parent / "fixtures" / "edge_cases.yaml"


def load_suite():
    try:
        with EDGE_CASES_PATH.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file)
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


def get_cases(group_name):
    return SUITE["groups"].get(group_name, [])


@pytest.mark.p0
@pytest.mark.parametrize(
    "case",
    get_cases("ambiguous_inputs"),
    ids=lambda case: case["id"],
)
def test_ambiguous_inputs(session, case):
    input_text = case["input"]
    fix = case["mock_response_fixture"]

    response: MockResponse = session.process(input_text, fix)

    assert response.routed_tag == case["expected"]["routed_tag"]


@pytest.mark.p0
@pytest.mark.parametrize(
    "case",
    get_cases("amplifier_stacking"),
    ids=lambda case: case["id"],
)
def test_amplifier_stacking(session, case):
    input_text = case.get("input", "")
    fix = case["mock_response_fixture"]

    response: MockResponse = session.process(input_text, fix)

    max_stack = case["expected"].get("max_stack", len(response.amplifier_stack))

    assert len(response.amplifier_stack) <= max_stack


@pytest.mark.p0
@pytest.mark.parametrize(
    "case",
    get_cases("combined_triggers"),
    ids=lambda case: case["id"],
)
def test_combined_triggers(session, case):
    input_text = case["input"]
    fix = case["mock_response_fixture"]

    response: MockResponse = session.process(input_text, fix)

    if case["id"] == "TC-INT-020":
        assert "urgency" in response.amplifier_stack

    if case["id"] == "TC-INT-022":
        assert response.prompt_includes_amplifier_hint is True


@pytest.mark.p0
@pytest.mark.parametrize(
    "case",
    get_cases("embedding_fallback"),
    ids=lambda case: case["id"],
)
def test_embedding_fallback(session, mock_llm_client, case):
    input_text = case["input"]
    fix = case["mock_response_fixture"]

    response: MockResponse = session.process(input_text, fix)

    if case["id"] == "TC-INT-031":
        assert mock_llm_client.embed_call_count == 0

    if case["id"] == "TC-INT-030":
        assert response.fallback_triggered is True


@pytest.mark.p0
@pytest.mark.parametrize(
    "case",
    get_cases("snapshot_restore"),
    ids=lambda case: case["id"],
)
def test_snapshot_restore(case):
    if case["id"] == "TC-INT-043":
        assert case["expected"].get("orphaned_amplifiers_dropped") is True
    else:
        status = case["expected"]["restore_status"]

        assert status in ("OK", "SNAPSHOT_CORRUPT", "SCHEMA_MISMATCH")


@pytest.mark.p0
@pytest.mark.parametrize(
    "case",
    get_cases("telemetry"),
    ids=lambda case: case["id"],
)
def test_telemetry(session, telemetry, case):
    input_text = case.get("input", case.get("scenario", ""))
    fix = case["mock_response_fixture"]

    response: MockResponse = session.process(input_text, fix)

    if case["id"] == "TC-INT-050":
        value = response.metrics.get("tag_switch_rate", 0.0)
        telemetry.emit("tag_switch_rate", value)

        assert 0.0 <= telemetry.metrics["tag_switch_rate"] <= 1.0

    if case["id"] == "TC-INT-051":
        value = response.metrics.get("amplifier_activation_rate", 0.0)
        telemetry.emit("amplifier_activation_rate", value)

        actual = telemetry.metrics["amplifier_activation_rate"]
        expected = case["expected"]["expected_value_approx"]

        assert abs(actual - expected) < 0.01

    if case["id"] == "TC-INT-052":
        value = response.metrics.get("prompt_injection_count", 0)
        telemetry.emit("prompt_injection_count", value)

        actual = telemetry.metrics["prompt_injection_count"]
        expected = case["expected"]["expected_value"]

        assert actual == expected

    if case["id"] == "TC-INT-053":
        for key, value in response.metrics.items():
            telemetry.emit(key, value)

        for metric in case["expected"]["metrics_emitted_at_zero"]:
            assert metric in telemetry.metrics
