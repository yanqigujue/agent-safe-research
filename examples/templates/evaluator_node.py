"""Template for a custom EVALUATOR node.

Contract (see ``formaltrust_platform.interfaces.EvaluatorNode``):
  Reads:  ``state.model_response``.
  Writes: MUST return ``{"evaluation": EvaluationResult}``.

Register with: ``registry.register(custom_evaluator_node)``.
"""

from collections.abc import Mapping
from typing import Any

from formaltrust_platform.interfaces import ConfigField, node
from formaltrust_platform.state import EvaluationResult, FormalTrustState


@node(
    "evaluate.custom",
    category="evaluator",
    summary="Example evaluator that passes when the response contains a marker.",
    config_fields=[
        ConfigField("marker", default="SAFE", description="Substring the response must contain to pass."),
    ],
)
def custom_evaluator_node(state: FormalTrustState, config: Mapping[str, Any]) -> dict[str, Any]:
    response = state.model_response.content if state.model_response else ""
    marker = str(config.get("marker", "SAFE"))
    passed = marker in response
    return {
        "evaluation": EvaluationResult(
            passed=passed,
            label="pass" if passed else "fail",
            score=1.0 if passed else 0.0,
            reasons=["custom evaluator template"],
        )
    }
