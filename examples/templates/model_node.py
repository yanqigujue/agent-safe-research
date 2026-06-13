"""Template for adding a custom model node."""

from collections.abc import Mapping
from typing import Any

from formaltrust_platform.state import FormalTrustState, ModelResponse


def custom_model_node(state: FormalTrustState, config: Mapping[str, Any]) -> dict[str, Any]:
    prompt = state.prompt or state.case.input
    content = f"custom response for {state.case.id}: {prompt}"
    return {
        "model_response": ModelResponse(content=content, model="custom-model"),
        "metrics": {"custom_model_called": True},
    }

