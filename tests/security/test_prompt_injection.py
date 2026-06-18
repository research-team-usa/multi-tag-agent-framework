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
        g["injection_detection"] = []
        g["prompt_leakage"] = []
        g["combined_sec"] = []
        return {"groups": g}


SUITE = load_suite()


def g(n):
    return SUITE["groups"].get(n, [])


@pytest.mark.p0
@pytest.mark.parametrize("c", g("injection_detection"), ids=lambda x: x["id"])
def test_injection_detection(session, c):
    fix = c["mock_response_fixture"]
    for v in c.get("variants", []):
        resp: MockResponse = session.process(v, fix)
        assert resp.injection_detected is True


@pytest.mark.p0
@pytest.mark.parametrize("c", g("prompt_leakage"), ids=lambda x: x["id"])
def test_prompt_leakage(session, c):
    scen = c.get("scenario", "")
    fix = c["mock_response_fixture"]
    resp: MockResponse = session.process(scen, fix)
    assert resp.system_prompt is None


@pytest.mark.p0
@pytest.mark.parametrize("c", g("combined_sec"), ids=lambda x: x["id"])
def test_combined_security(session, c):
    inp = c.get("input", c.get("scenario", ""))
    fix = c["mock_response_fixture"]
    resp: MockResponse = session.process(inp, fix)
    assert resp.injection_detected is True
