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
                "injection_detection": [],
                "prompt_leakage": [],
                "combined_sec": [],
            }
        }


SUITE = load_suite()


def get_cases(group_name):
    return SUITE["groups"].get(group_name, [])


@pytest.mark.p0
@pytest.mark.parametrize(
    "case",
    get_cases("injection_detection"),
    ids=lambda case: case["id"],
)
def test_injection_detection(session, case):
    fix = case["mock_response_fixture"]

    for variant in case.get("variants", []):
        response: MockResponse = session.process(variant, fix)

        assert response.injection_detected is True


@pytest.mark.p0
@pytest.mark.parametrize(
    "case",
    get_cases("prompt_leakage"),
    ids=lambda case: case["id"],
)
def test_prompt_leakage(session, case):
    scenario = case.get("scenario", "")
    fix = case["mock_response_fixture"]

    response: MockResponse = session.process(scenario, fix)

    assert response.system_prompt is None


@pytest.mark.p0
@pytest.mark.parametrize(
    "case",
    get_cases("combined_sec"),
    ids=lambda case: case["id"],
)
def test_combined_security(session, case):
    input_text = case.get("input", case.get("scenario", ""))
    fix = case["mock_response_fixture"]

    response: MockResponse = session.process(input_text, fix)

    assert response.injection_detected is True
