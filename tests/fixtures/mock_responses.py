from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class MockResponse:
    routed_tag: str
    amplifier_stack: List[str]
    fallback_triggered: bool = False
    injection_detected: bool = False
    system_prompt: Optional[str] = None
    prompt_includes_amplifier_hint: bool = False
    metrics: Dict[str, Any] = None


FIXTURE_REGISTRY: Dict[str, MockResponse] = {
    "ambiguous_billing_wins": MockResponse(
        routed_tag="billing",
        amplifier_stack=[],
        fallback_triggered=False,
        injection_detected=False,
    ),
    "ambiguous_equal_confidence_first_registered": MockResponse(
        routed_tag="payments",
        amplifier_stack=[],
    ),
    "three_amplifiers_no_overflow": MockResponse(
        routed_tag="incident",
        amplifier_stack=["urgency", "priority_high", "production"],
    ),
    "amplifier_overflow_guard": MockResponse(
        routed_tag="incident",
        amplifier_stack=["urgency", "priority_high", "production", "sla_breach", "escalation"],
    ),
    "tag_and_amp_same_message": MockResponse(
        routed_tag="billing",
        amplifier_stack=["urgency"],
        prompt_includes_amplifier_hint=True,
    ),
    "no_embedding_high_confidence": MockResponse(
        routed_tag="billing",
        amplifier_stack=[],
        fallback_triggered=False,
    ),
    "embedding_fallback_chargeback": MockResponse(
        routed_tag="payments",
        amplifier_stack=[],
        fallback_triggered=True,
    ),
    "telemetry_tag_switch_rate": MockResponse(
        routed_tag="billing",
        amplifier_stack=[],
        metrics={"tag_switch_rate": 0.5},
    ),
    "telemetry_amp_activation_rate": MockResponse(
        routed_tag="incident",
        amplifier_stack=["urgency"],
        metrics={"amplifier_activation_rate": 0.4},
    ),
    "telemetry_injection_count": MockResponse(
        routed_tag="default",
        amplifier_stack=[],
        injection_detected=True,
        metrics={"prompt_injection_count": 2},
    ),
    "ignore_previous_instructions": MockResponse(
        routed_tag="default",
        amplifier_stack=[],
        injection_detected=True,
    ),
    "role_override_attacks": MockResponse(
        routed_tag="default",
        amplifier_stack=[],
        injection_detected=True,
    ),
    "system_prompt_exfil": MockResponse(
        routed_tag="default",
        amplifier_stack=[],
        injection_detected=True,
        system_prompt=None,
    ),
    "base64_injection": MockResponse(
        routed_tag="default",
        amplifier_stack=[],
        injection_detected=True,
    ),
    "indirect_tool_injection": MockResponse(
        routed_tag="default",
        amplifier_stack=[],
        injection_detected=True,
    ),
    "unicode_homoglyph_injection": MockResponse(
        routed_tag="default",
        amplifier_stack=[],
        injection_detected=True,
    ),
    "no_system_prompt_leak": MockResponse(
        routed_tag="default",
        amplifier_stack=[],
        injection_detected=False,
        system_prompt=None,
    ),
    "combined_injection_exfil": MockResponse(
        routed_tag="default",
        amplifier_stack=[],
        injection_detected=True,
        system_prompt=None,
    ),
    "nested_base64_exfil": MockResponse(
        routed_tag="default",
        amplifier_stack=[],
        injection_detected=True,
    ),
    "json_wrapped_injection": MockResponse(
        routed_tag="default",
        amplifier_stack=[],
        injection_detected=True,
    ),
    "combined_sec_telemetry": MockResponse(
        routed_tag="default",
        amplifier_stack=[],
        injection_detected=True,
        metrics={"prompt_injection_count": 2},
    ),
}


class MockLLMClient:
    def __init__(self):
        self.call_count = 0
        self.embed_call_count = 0

    def complete(self, prompt: str, fixture: str) -> MockResponse:
        self.call_count += 1
        return FIXTURE_REGISTRY[fixture]

    def embed(self, text: str) -> List[float]:
        self.embed_call_count += 1
        # Return a dummy embedding vector
        return [0.0, 0.1, 0.2]
