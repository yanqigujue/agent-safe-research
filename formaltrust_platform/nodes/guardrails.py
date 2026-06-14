from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from formaltrust_platform.interfaces import node
from formaltrust_platform.state import FormalTrustState


@node(
    "guardrail.input.noop",
    category="guardrail",
    summary="Pass-through input guardrail (records a metric; performs no filtering).",
)
def input_noop_guardrail_node(state: FormalTrustState, config: Mapping[str, Any]) -> dict[str, Any]:
    return {"metrics": {"input_guardrail_checked": True}}


@node(
    "guardrail.output.noop",
    category="guardrail",
    summary="Pass-through output guardrail (records a metric; performs no filtering).",
)
def output_noop_guardrail_node(state: FormalTrustState, config: Mapping[str, Any]) -> dict[str, Any]:
    return {"metrics": {"output_guardrail_checked": True}}

