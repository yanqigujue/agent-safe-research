"""Template for a custom MODEL node.

Contract (see ``formaltrust_platform.interfaces.ModelNode``):
  Reads:  ``state.prompt`` (falling back to ``state.case.input``).
  Writes: MUST return ``{"model_response": ModelResponse}``.
  Secrets: read from environment variables only — declare them with
           ``ConfigField(..., secret_env=True)``; never put keys in ``config``.

Register with: ``registry.register(custom_model_node)``  (the @node decorator
attaches the interface metadata, so the no-arg form works).
"""

from collections.abc import Mapping
from typing import Any

from formaltrust_platform.interfaces import ConfigField, node
from formaltrust_platform.state import FormalTrustState, ModelResponse


@node(
    "model.custom",
    category="model",
    summary="Example custom model node.",
    config_fields=[
        ConfigField("model", default="custom-model", description="Model id reported in the response."),
        ConfigField(
            "api_key_env",
            secret_env=True,
            description="Name of the env var holding the API key (omit for a keyless model).",
        ),
    ],
)
def custom_model_node(state: FormalTrustState, config: Mapping[str, Any]) -> dict[str, Any]:
    prompt = state.prompt or state.case.input
    # To call a real endpoint, read the key from the env var named by config["api_key_env"]
    # (os.getenv(...)) — never store the key in config.
    content = f"custom response for {state.case.id}: {prompt}"
    return {
        "model_response": ModelResponse(content=content, model=str(config.get("model", "custom-model"))),
        "metrics": {"custom_model_called": True},
    }
