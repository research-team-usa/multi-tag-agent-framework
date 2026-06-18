# isort: skip_file
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
        return {
            "groups": {
                "injection_detection": [],
                "prompt_leakage": [],
                "combined_sec": [],
            }
        }


SUITE = load_suite()


def iter_sec(group_name):
    return SUITE["groups"].get(group_name, [])


@pytest.mark.p0
@pytest.mark.parametrize(
    "case",
    iter_sec("injection_detection"),
    ids=lambda c: c["id"],
)
def test_injection_detection(session, case):
    variants = case.get("variants", [])
    for v in variants:
        resp: MockResponse = session.process(v, case["mock_response_fixture"])
        assert resp.injection_detected is True


@pytest.mark.p0
@pytest.mark.parametrize(
    "case",
    iter_sec("prompt_leakage"),
    ids=lambda c: c["id"],
)
def test_prompt_leakage(session, case):
    resp: MockResponse = session.process(
        case.get("scenario", ""),
        case["mock_response_fixture"],
    )
    assert resp.system_prompt is None


@pytest.mark.p0
@pytest.mark.parametrize(
    "case",
    iter_sec("combined_sec"),
    ids=lambda c: c["id"],
)
def test_combined_security(session, case):
    resp: MockResponse = session.process(
        case.get("input", case.get("scenario", "")),
        case["mock_response_fixture"],
    )
    assert resp.injection_detected is True
