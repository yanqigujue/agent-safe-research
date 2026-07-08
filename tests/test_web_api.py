from fastapi.testclient import TestClient

from formaltrust_platform.web_api import app


def test_web_api_exposes_node_catalog() -> None:
    client = TestClient(app)

    response = client.get("/api/catalog")

    assert response.status_code == 200
    payload = response.json()
    node_ids = {node["node_id"] for node in payload["nodes"]}
    assert "model.openai_compatible" in node_ids
    assert "guardrail.afw_capguard" in node_ids
    assert payload["edge_conditions"] == ["has_errors", "no_errors", "halted"]

    catalog_by_id = {node["node_id"]: node for node in payload["nodes"]}
    trace_adapter = catalog_by_id["custom.afw_trace_adapter"]
    assert "metrics.afw_source_events" in trace_adapter["outputs"]
    assert "afw_trace_adapter_summary" in trace_adapter["metrics"]
    assert "schema_preset" in trace_adapter["advanced_fields"]

    openai_node = catalog_by_id["model.openai_compatible"]
    assert "environment variable api_key_env" in openai_node["inputs"]
    assert openai_node["examples"]


def test_web_api_exposes_agent_runtime_interface_catalog() -> None:
    client = TestClient(app)

    response = client.get("/api/agent-interfaces")

    assert response.status_code == 200
    payload = response.json()
    assert payload["schema_version"] == "agent-runtime-interface/v1"
    assert "skill" in payload["canonical_component_kinds"]
    assert "tool" in payload["canonical_component_kinds"]
    assert "memory" in payload["canonical_component_kinds"]
    assert "action.candidate" in payload["canonical_event_types"]
    assert "authority.consumed" in payload["canonical_event_types"]
    model_names = {model["name"] for model in payload["models"]}
    assert {"AgentRuntimeTrace", "AgentComponentDescriptor", "AgentTraceEvent"} <= model_names


def test_web_api_model_endpoints_and_mock_qa_run() -> None:
    client = TestClient(app)

    endpoints_response = client.get("/api/model-endpoints")
    assert endpoints_response.status_code == 200
    endpoints = endpoints_response.json()["endpoints"]
    assert any(endpoint["endpoint_id"] == "mock-offline" for endpoint in endpoints)

    qa_response = client.post(
        "/api/qa/run",
        json={"endpoint_id": "mock-offline", "prompt": "Summarize relay status."},
    )

    assert qa_response.status_code == 200
    payload = qa_response.json()
    assert payload["run_type"] == "qa"
    assert payload["answer"].startswith("MOCK_RESPONSE:")
    assert payload["model_snapshot"]["endpoint_id"] == "mock-offline"


def test_web_api_lists_formaltrust_configs() -> None:
    client = TestClient(app)

    response = client.get("/api/configs")

    assert response.status_code == 200
    payload = response.json()
    paths = {config["path"] for config in payload["configs"]}
    assert "examples/mock_validation.yaml" in paths
    assert all(config["node_count"] > 0 for config in payload["configs"])


def test_web_api_rejects_paths_outside_workspace() -> None:
    client = TestClient(app)

    response = client.get("/api/config", params={"path": "../outside.yaml"})

    assert response.status_code == 400
    assert "inside" in response.json()["detail"]
