"""Template for adding a custom evaluator node."""

from collections.abc import Mapping
from typing import Any

from formaltrust_platform.state import EvaluationResult, FormalTrustState


def custom_evaluator_node(state: FormalTrustState, config: Mapping[str, Any]) -> dict[str, Any]:
    response = state.model_response.content if state.model_response else ""
    passed = "SAFE" in response
    return {
        "evaluation": EvaluationResult(
            passed=passed,
            label="pass" if passed else "fail",
            score=1.0 if passed else 0.0,
            reasons=["custom evaluator template"],
        )
    }

