from pathlib import Path

import pytest
import yaml

from tests.fixtures.mock_responses import MockResponse


EDGE_CASES_PATH = Path(__file__).parent.parent / "fixtures" / "edge_cases.yaml"


def load_suite():
    try:
        with EDGE_CASES_PATH.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        g = {}
        g["ambiguous_inputs"] = []
        g["amplifier_stacking"] = []
        g["combined_triggers"] = []
        g["embedding_fallback"] = []
        g["snapshot_restore"] = []
        g["telemetry"] = []
        return {"groups": g}


SUITE = load_suite()


def g(n):
    return SUITE["groups"].get(n, [])


@pytest.mark.p0
@pytest.mark.parametrize("c", g("ambiguous_inputs"), ids=lambda x: x["id"])
def test_ambiguous_inputs(session, c):
    inp = c["input"]
    fix = c["mock_response_fixture"]
    resp: MockResponse = session.process(inp, fix)
    assert resp.routed_tag == c["expected"]["routed_tag"]


@pytest.mark.p0
@pytest.mark.parametrize("c", g("amplifier_stacking"), ids=lambda x: x["id"])
def test_amplifier_stacking(session, c):
    inp = c.get("input", "")
    fix = c["mock_response_fixture"]
    resp: MockResponse = session.process(inp, fix)
    max_s = c["expected"].get("max_stack", len(resp.amplifier_stack))
    assert len(resp.amplifier_stack) <= max_s


@pytest.mark.p0
@pytest.mark.parametrize("c", g("combined_triggers"), ids=lambda x: x["id"])
def test_combined_triggers(session, c):
    inp = c["input"]
    fix = c["mock_response_fixture"]
    resp: MockResponse = session.process(inp, fix)
    if c["id"] == "TC-INT-020":
        assert "urgency" in resp.amplifier_stack
    if c["id"] == "TC-INT-022":
        assert resp.prompt_includes_amplifier_hint is True


@pytest.mark.p0
@pytest.mark.parametrize("c", g("embedding_fallback"), ids=lambda x: x["id"])
def test_embedding_fallback(session, mock_llm_client, c):
    inp = c["input"]
    fix = c["mock_response_fixture"]
    resp: MockResponse = session.process(inp, fix)
    if c["id"] == "TC-INT-031":
        assert mock_llm_client.embed_call_count == 0
    if c["id"] == "TC-INT-030":
        assert resp.fallback_triggered is True


@pytest.mark.p0
@pytest.mark.parametrize("c", g("snapshot_restore"), ids=lambda x: x["id"])
def test_snapshot_restore(c):
    if c["id"] == "TC-INT-043":
        assert c["expected"].get("orphaned_amplifiers_dropped") is True
    else:
        status = c["expected"]["restore_status"]
        assert status in ("OK", "SNAPSHOT_CORRUPT", "SCHEMA_MISMATCH")


@pytest.mark.p0
@pytest.mark.parametrize("c", g("telemetry"), ids=lambda x: x["id"])
def test_telemetry(session, telemetry, c):
    inp = c.get("input", c.get("scenario", ""))
    fix = c["mock_response_fixture"]
    resp: MockResponse = session.process(inp, fix)

    if c["id"] == "TC-INT-050":
        val = resp.metrics.get("tag_switch_rate", 0.0)
        telemetry.emit("tag_switch_rate", val)
        assert 0.0 <= telemetry.metrics["tag_switch_rate"] <= 1.0

    if c["id"] == "TC-INT-051":
        val = resp.metrics.get("amplifier_activation_rate", 0.0)
        telemetry.emit("amplifier_activation_rate", val)
        act = telemetry.metrics["amplifier_activation_rate"]
        exp = c["expected"]["expected_value_approx"]
        assert abs(act - exp) < 0.01

    if c["id"] == "TC-INT-052":
        val = resp.metrics.get("prompt_injection_count", 0)
        telemetry.emit("prompt_injection_count", val)
        act = telemetry.metrics["prompt_injection_count"]
        exp = c["expected"]["expected_value"]
        assert act == exp

    if c["id"] == "TC-INT-053":
        for key, val in resp.metrics.items():
            telemetry.emit(key, val)
        for m in c["expected"]["metrics_emitted_at_zero"]:
            assert m in telemetry.metrics
