from pathlib import Path

from formaltrust_platform.model_endpoints import (
    ModelEndpoint,
    ModelEndpointStore,
    chat_with_endpoint,
    snapshot_endpoint,
)


def test_endpoint_store_creates_defaults(tmp_path: Path) -> None:
    store = ModelEndpointStore(tmp_path / "model_endpoints.json")
    endpoints = store.list()

    assert {endpoint.kind for endpoint in endpoints} >= {"mock", "ollama"}
    assert any(endpoint.endpoint_id == "mock-offline" for endpoint in endpoints)


def test_snapshot_omits_secret_value() -> None:
    endpoint = ModelEndpoint(
        endpoint_id="api",
        name="API",
        kind="openai_compatible",
        provider="DeepSeek",
        base_url="https://api.example.com/v1",
        model="deepseek-chat",
        api_key_env="DEEPSEEK_API_KEY",
    )

    snapshot = snapshot_endpoint(endpoint)

    assert snapshot["api_key_env"] == "DEEPSEEK_API_KEY"
    assert "api_key" not in snapshot


def test_mock_chat_returns_deterministic_answer() -> None:
    endpoint = ModelEndpoint(
        endpoint_id="mock",
        name="Mock",
        kind="mock",
        provider="Mock",
        model="mock-safe-model",
    )

    result = chat_with_endpoint(endpoint, "hello")

    assert result.answer.startswith("MOCK_RESPONSE:")
    assert result.model_snapshot["endpoint_id"] == "mock"
    assert result.latency_ms >= 0
