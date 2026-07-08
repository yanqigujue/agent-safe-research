from __future__ import annotations

import os
import time
from collections.abc import Mapping
from typing import Any

import httpx

from formaltrust_platform.interfaces import ConfigField, node
from formaltrust_platform.model_endpoints import (
    DEFAULT_MODEL_ENDPOINTS_PATH,
    ModelEndpointStore,
    chat_with_endpoint,
)
from formaltrust_platform.state import FormalTrustState, ModelResponse


@node(
    "model.mock",
    category="model",
    summary="Deterministic offline model that renders a response template. Needs no API key.",
    config_fields=[
        ConfigField("model", default="mock-model", description="Model id reported in the response."),
        ConfigField(
            "response_template",
            default="SAFE_RESPONSE: {input}",
            description="Response template; supports {input}, {prompt}, and {case_id} placeholders.",
        ),
    ],
)
def mock_model_node(state: FormalTrustState, config: Mapping[str, Any]) -> dict[str, Any]:
    model = str(config.get("model", "mock-model"))
    template = str(config.get("response_template", "SAFE_RESPONSE: {input}"))
    prompt = state.prompt or state.case.input
    content = template.format(input=state.case.input, prompt=prompt, case_id=state.case.id)
    return {
        "model_response": ModelResponse(
            content=content,
            model=model,
            raw={"provider": "mock", "prompt": prompt},
            latency_ms=0.0,
        ),
        "metrics": {"model_called": True},
    }


@node(
    "model.openai_compatible",
    category="model",
    summary="Call any OpenAI-compatible /chat/completions endpoint (OpenAI, Azure, Ollama, vLLM, ...).",
    config_fields=[
        ConfigField(
            "model_endpoint_id",
            description="Shared model endpoint id. When set, base_url/model/api_key_env are resolved from the endpoint store.",
        ),
        ConfigField(
            "base_url",
            required=True,
            required_without_any=["model_endpoint_id"],
            description="Endpoint base URL, e.g. https://api.deepseek.com/v1 (no trailing /chat/completions).",
        ),
        ConfigField(
            "model",
            required=True,
            required_without_any=["model_endpoint_id"],
            description="Model id sent to the endpoint.",
        ),
        ConfigField(
            "api_key_env",
            required=True,
            required_without_any=["model_endpoint_id"],
            secret_env=True,
            description="Name of the environment variable holding the API key (the key itself is never stored in config).",
        ),
        ConfigField("temperature", type="float", default=0, description="Sampling temperature."),
        ConfigField("timeout_seconds", type="float", default=60, description="HTTP request timeout in seconds."),
    ],
)
def openai_compatible_model_node(state: FormalTrustState, config: Mapping[str, Any]) -> dict[str, Any]:
    if config.get("model_endpoint_id"):
        endpoint = ModelEndpointStore(DEFAULT_MODEL_ENDPOINTS_PATH).get(str(config["model_endpoint_id"]))
        result = chat_with_endpoint(
            endpoint,
            state.prompt or state.case.input,
            temperature=float(config.get("temperature", 0)),
        )
        return {
            "model_response": ModelResponse(
                content=result.answer,
                model=str(result.model_snapshot["model"]),
                raw=result.raw,
                latency_ms=result.latency_ms,
            ),
            "metrics": {"model_called": True, "model_snapshot": result.model_snapshot},
        }

    base_url = str(config["base_url"]).rstrip("/")
    model = str(config["model"])
    api_key_env = str(config["api_key_env"])
    api_key = os.getenv(api_key_env)
    if not api_key:
        raise RuntimeError(f"Environment variable '{api_key_env}' is required for model.openai_compatible")

    prompt = state.prompt or state.case.input
    started = time.perf_counter()
    response = httpx.post(
        f"{base_url}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": config.get("temperature", 0),
        },
        timeout=float(config.get("timeout_seconds", 60)),
    )
    response.raise_for_status()
    payload = response.json()
    content = payload["choices"][0]["message"]["content"]
    return {
        "model_response": ModelResponse(
            content=content,
            model=model,
            raw=payload,
            latency_ms=(time.perf_counter() - started) * 1000,
        ),
        "metrics": {"model_called": True},
    }
