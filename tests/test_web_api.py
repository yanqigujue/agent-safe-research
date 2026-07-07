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
