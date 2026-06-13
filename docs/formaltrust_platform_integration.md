# FormalTrust Platform Integration Guide

## Quick Start
Run the local mock demo without any API key:

```powershell
formaltrust run --config examples/mock_validation.yaml
```

The command creates `runs/<run_id>/` with `results.json`, per-case JSON files, and a debug-oriented `report.md`.

## Node Contract
Custom nodes are normal Python callables:

```python
def my_node(state: FormalTrustState, config: Mapping[str, Any]) -> dict[str, Any]:
    return {"metrics": {"seen": True}}
```

Rules:
- Read inputs from `FormalTrustState`.
- Return only fields defined on `FormalTrustState`.
- Return nested objects using the Pydantic models in `formaltrust_platform.state`.
- Register the callable with `NodeRegistry.register("my.node_id", my_node)`.

If a node returns an unknown field, the runner records a friendly per-case error and continues the batch.

## YAML Graph
YAML configs reference registered node ids and connect them with edges:

```yaml
graph:
  nodes:
    - name: model
      node_id: model.mock
  edges:
    - from: START
      to: model
    - from: model
      to: END
```

Supported conditional edge predicates are `has_errors`, `no_errors`, and `halted`.

## Model Keys
OpenAI-compatible model nodes read secrets only from environment variables:

```yaml
node_id: model.openai_compatible
config:
  base_url: https://api.deepseek.com/v1
  model: deepseek-chat
  api_key_env: DEEPSEEK_API_KEY
```

The mock demo does not require any key.
