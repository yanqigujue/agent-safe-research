from __future__ import annotations

import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx
from pydantic import Field

from formaltrust_platform.state import StrictModel


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class ModelEndpoint(StrictModel):
    endpoint_id: str
    name: str
    kind: str
    provider: str = ""
    base_url: str | None = None
    model: str
    api_key_env: str | None = None
    capabilities: list[str] = Field(default_factory=list)
    status: str = "unchecked"
    last_probe_at: str | None = None
    last_probe_error: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ModelEndpointProbe(StrictModel):
    endpoint_id: str
    status: str
    checked_at: str = Field(default_factory=utc_now_iso)
    models: list[str] = Field(default_factory=list)
    error: str | None = None


class ModelChatResult(StrictModel):
    answer: str
    model_snapshot: dict[str, Any]
    latency_ms: float
    raw: dict[str, Any] = Field(default_factory=dict)


def default_model_endpoints() -> list[ModelEndpoint]:
    return [
        ModelEndpoint(
            endpoint_id="mock-offline",
            name="Mock offline model",
            kind="mock",
            provider="Mock",
            model="mock-safe-model",
            capabilities=["chat", "json_output"],
            status="available",
        ),
        ModelEndpoint(
            endpoint_id="ollama-local",
            name="Local Ollama",
            kind="ollama",
            provider="Ollama",
            base_url="http://127.0.0.1:11434",
            model="qwen2.5:7b",
            capabilities=["chat", "json_output"],
        ),
    ]


def sanitize_endpoint_id(value: str) -> str:
    sanitized = re.sub(r"[^a-zA-Z0-9_.-]+", "-", value.strip()).strip("-").lower()
    if not sanitized:
        raise ValueError("endpoint_id must contain at least one letter or number")
    return sanitized


def snapshot_endpoint(endpoint: ModelEndpoint) -> dict[str, Any]:
    return {
        "endpoint_id": endpoint.endpoint_id,
        "kind": endpoint.kind,
        "provider": endpoint.provider,
        "base_url": endpoint.base_url,
        "model": endpoint.model,
        "api_key_env": endpoint.api_key_env,
        "resolved_at": utc_now_iso(),
        "status_at_run_start": endpoint.status,
    }


class ModelEndpointStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def list(self) -> list[ModelEndpoint]:
        if not self.path.exists():
            self.save_all(default_model_endpoints())
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        return [ModelEndpoint.model_validate(item) for item in payload.get("endpoints", [])]

    def save_all(self, endpoints: list[ModelEndpoint]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"endpoints": [endpoint.model_dump(mode="json") for endpoint in endpoints]}
        self.path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    def get(self, endpoint_id: str) -> ModelEndpoint:
        for endpoint in self.list():
            if endpoint.endpoint_id == endpoint_id:
                return endpoint
        raise KeyError(f"Unknown model endpoint '{endpoint_id}'")

    def upsert(self, endpoint: ModelEndpoint) -> ModelEndpoint:
        endpoint = endpoint.model_copy(update={"endpoint_id": sanitize_endpoint_id(endpoint.endpoint_id)})
        endpoints = [item for item in self.list() if item.endpoint_id != endpoint.endpoint_id]
        endpoints.append(endpoint)
        self.save_all(sorted(endpoints, key=lambda item: item.endpoint_id))
        return endpoint

    def delete(self, endpoint_id: str) -> None:
        current = self.list()
        endpoints = [item for item in current if item.endpoint_id != endpoint_id]
        if len(endpoints) == len(current):
            raise KeyError(f"Unknown model endpoint '{endpoint_id}'")
        self.save_all(endpoints)


def list_ollama_models(base_url: str, *, timeout_seconds: float = 5.0) -> list[str]:
    response = httpx.get(f"{base_url.rstrip('/')}/api/tags", timeout=timeout_seconds)
    response.raise_for_status()
    payload = response.json()
    return [str(model.get("name")) for model in payload.get("models", []) if model.get("name")]


def probe_endpoint(endpoint: ModelEndpoint) -> ModelEndpointProbe:
    try:
        if endpoint.kind == "mock":
            return ModelEndpointProbe(endpoint_id=endpoint.endpoint_id, status="available", models=[endpoint.model])
        if endpoint.kind == "ollama":
            models = list_ollama_models(endpoint.base_url or "http://127.0.0.1:11434")
            status = "available" if endpoint.model in models or not endpoint.model else "unavailable"
            error = None if status == "available" else f"Model '{endpoint.model}' was not returned by Ollama"
            return ModelEndpointProbe(endpoint_id=endpoint.endpoint_id, status=status, models=models, error=error)
        if endpoint.kind == "openai_compatible":
            if endpoint.api_key_env and not os.getenv(endpoint.api_key_env):
                return ModelEndpointProbe(
                    endpoint_id=endpoint.endpoint_id,
                    status="error",
                    error=f"Environment variable '{endpoint.api_key_env}' is not set",
                )
            return ModelEndpointProbe(endpoint_id=endpoint.endpoint_id, status="available", models=[endpoint.model])
        return ModelEndpointProbe(endpoint_id=endpoint.endpoint_id, status="unchecked")
    except Exception as exc:  # noqa: BLE001 - probe should return a user-visible diagnostic.
        return ModelEndpointProbe(endpoint_id=endpoint.endpoint_id, status="error", error=str(exc))


def chat_with_endpoint(endpoint: ModelEndpoint, prompt: str, *, temperature: float = 0) -> ModelChatResult:
    started = time.perf_counter()
    if endpoint.kind == "mock":
        return ModelChatResult(
            answer=f"MOCK_RESPONSE: {prompt}",
            model_snapshot=snapshot_endpoint(endpoint),
            latency_ms=(time.perf_counter() - started) * 1000,
            raw={"provider": "mock", "prompt": prompt},
        )
    if endpoint.kind == "ollama":
        response = httpx.post(
            f"{(endpoint.base_url or 'http://127.0.0.1:11434').rstrip('/')}/api/chat",
            json={
                "model": endpoint.model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "options": {"temperature": temperature},
            },
            timeout=120,
        )
        response.raise_for_status()
        payload = response.json()
        return ModelChatResult(
            answer=str(payload.get("message", {}).get("content", "")),
            model_snapshot=snapshot_endpoint(endpoint),
            latency_ms=(time.perf_counter() - started) * 1000,
            raw=payload,
        )
    if endpoint.kind == "openai_compatible":
        api_key = os.getenv(endpoint.api_key_env or "")
        if endpoint.api_key_env and not api_key:
            raise RuntimeError(f"Environment variable '{endpoint.api_key_env}' is required")
        response = httpx.post(
            f"{(endpoint.base_url or '').rstrip('/')}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"} if api_key else {},
            json={
                "model": endpoint.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
            },
            timeout=120,
        )
        response.raise_for_status()
        payload = response.json()
        return ModelChatResult(
            answer=str(payload["choices"][0]["message"]["content"]),
            model_snapshot=snapshot_endpoint(endpoint),
            latency_ms=(time.perf_counter() - started) * 1000,
            raw=payload,
        )
    raise ValueError(f"Unsupported model endpoint kind '{endpoint.kind}'")
