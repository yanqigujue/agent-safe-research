from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from formaltrust_platform.state import FormalTrustState


def input_noop_guardrail_node(state: FormalTrustState, config: Mapping[str, Any]) -> dict[str, Any]:
    return {"metrics": {"input_guardrail_checked": True}}


def output_noop_guardrail_node(state: FormalTrustState, config: Mapping[str, Any]) -> dict[str, Any]:
    return {"metrics": {"output_guardrail_checked": True}}

