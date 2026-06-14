from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from formaltrust_platform.interfaces import ConfigField, node
from formaltrust_platform.state import EvaluationResult, FormalTrustState


@node(
    "evaluate.rules",
    category="evaluator",
    summary="Rule-based pass/fail via substring checks on the model response.",
    config_fields=[
        ConfigField("pass_if_contains", description="Response must contain this text to pass."),
        ConfigField("fail_if_contains", description="Response containing this text fails."),
    ],
)
def rule_evaluator_node(state: FormalTrustState, config: Mapping[str, Any]) -> dict[str, Any]:
    response = state.model_response.content if state.model_response else ""
    reasons: list[str] = []
    passed = True

    pass_if_contains = config.get("pass_if_contains")
    if pass_if_contains:
        passed = str(pass_if_contains) in response
        reasons.append(f"response contains required text: {pass_if_contains}" if passed else f"missing required text: {pass_if_contains}")

    fail_if_contains = config.get("fail_if_contains")
    if fail_if_contains and str(fail_if_contains) in response:
        passed = False
        reasons.append(f"response contains forbidden text: {fail_if_contains}")

    if not reasons:
        reasons.append("no rule configured; default pass")

    return {
        "evaluation": EvaluationResult(
            passed=passed,
            label="pass" if passed else "fail",
            score=1.0 if passed else 0.0,
            reasons=reasons,
        ),
        "metrics": {"evaluation_passed": passed},
    }

