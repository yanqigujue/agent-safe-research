from __future__ import annotations

import os
import time
from collections.abc import Mapping
from typing import Any

import httpx

from formaltrust_platform.state import FormalTrustState, ModelResponse


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


def openai_compatible_model_node(state: FormalTrustState, config: Mapping[str, Any]) -> dict[str, Any]:
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

