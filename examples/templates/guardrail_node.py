"""Template for a custom GUARDRAIL node.

Contract (see ``formaltrust_platform.interfaces.GuardrailNode``):
  Input guardrails read/rewrite ``state.prompt`` before the model call;
  output guardrails inspect ``state.model_response`` afterwards.
  Return ``None`` or a metrics-only patch to "allow"; raise to block the case
  (the runner records the failure and continues the batch).

Register with: ``registry.register(custom_output_guardrail_node)``.
"""

from collections.abc import Mapping
from typing import Any

from formaltrust_platform.interfaces import ConfigField, node
from formaltrust_platform.state import FormalTrustState


@node(
    "guardrail.output.blocklist",
    category="guardrail",
    summary="Example output guardrail that blocks responses containing a forbidden phrase.",
    config_fields=[
        ConfigField("blocked_phrase", description="If present in the response, the case is blocked."),
    ],
)
def custom_output_guardrail_node(state: FormalTrustState, config: Mapping[str, Any]) -> dict[str, Any]:
    response = state.model_response.content if state.model_response else ""
    blocked = str(config.get("blocked_phrase", ""))
    if blocked and blocked in response:
        raise ValueError(f"output guardrail blocked response containing '{blocked}'")
    return {"metrics": {"output_guardrail_checked": True}}
