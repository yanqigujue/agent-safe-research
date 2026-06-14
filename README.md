# FormalTrust Platform

FormalTrust is a modular validation platform for testing LLM and RAG-agent trustworthiness. It runs a batch of test cases through a configurable graph of nodes such as attack, retrieval, guardrail, model, and evaluator, then writes per-case artifacts and a Markdown report.

The current codebase is intentionally small: it is a platform skeleton for building and comparing methods, not a large product framework. The fastest way to understand it is to run the mock example, inspect the generated run folder, and then read the node interface contract.

## What You Can Do

- Run an offline mock trustworthiness validation pipeline.
- Plug in custom attack, model, guardrail, and evaluator nodes.
- Declare node config requirements so YAML errors fail early and clearly.
- Load datasets from JSONL, JSON, or CSV.
- Write per-case artifacts and a run-level report.
- Use the project as a base for Evidence-to-Action / RAG-agent safety methods.

## Quick Start

Use Python 3.10 or newer.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
formaltrust run --config examples/mock_validation.yaml
```

The command creates a run folder under `runs/`:

```text
runs/<run_id>/
  report.md
  results.json
  cases/
    <case_id>.json
```

Open `report.md` first. If something fails, inspect the matching file under `cases/` for `errors`, `trace`, `metrics`, and the state fields produced by each node.

## Run Tests

```powershell
pytest
```

For the platform interface surface only:

```powershell
pytest tests/test_interfaces.py tests/test_mvp.py
```

## Project Map

```text
formaltrust_platform/
  cli.py              # `formaltrust run`
  config.py           # YAML config models and path resolution
  datasets.py         # JSONL / JSON / CSV case loaders
  graph.py            # LangGraph assembly, node wrapping, patch validation
  interfaces.py       # Extension contracts, node metadata, config validation
  registry.py         # Node registry and built-in node catalog
  runner.py           # Batch execution and summary generation
  state.py            # FormalTrustState and nested Pydantic models
  nodes/              # Built-in attack, guardrail, model, evaluator nodes

examples/
  mock_validation.yaml
  data/
  templates/          # Minimal custom node templates

docs/
  formaltrust_platform_integration.md
  method_interface_contract_cn.md

tests/
  test_mvp.py
  test_interfaces.py
```

## Core Concept

Every pluggable method is a node with the same shape:

```python
from collections.abc import Mapping
from typing import Any

from formaltrust_platform.state import FormalTrustState


def my_node(state: FormalTrustState, config: Mapping[str, Any]) -> dict[str, Any] | None:
    ...
```

A node reads the current `FormalTrustState`, reads its own YAML `config`, and returns a patch. Patch keys must be fields of `FormalTrustState`. `metrics` and `artifacts` are merged; most other fields are replaced.

Use `@node(...)` and `ConfigField` to make nodes self-describing:

```python
from formaltrust_platform.interfaces import ConfigField, node


@node(
    "model.custom",
    category="model",
    summary="Example custom model node.",
    config_fields=[
        ConfigField("model", required=True),
        ConfigField("api_key_env", required=True, secret_env=True),
    ],
)
def custom_model_node(state, config):
    ...
```

Never put raw secrets in YAML. Store only the environment variable name, for example `api_key_env: OPENAI_API_KEY`.

## Built-In Nodes

| Node ID | Role | Purpose |
|---|---|---|
| `attack.template` | attack | Render an attack prompt template and optionally add a poisoned RAG document. |
| `guardrail.input.noop` | guardrail | Pass-through input guardrail. |
| `guardrail.output.noop` | guardrail | Pass-through output guardrail. |
| `model.mock` | model | Deterministic offline model for tests and demos. |
| `model.openai_compatible` | model | Call an OpenAI-compatible `/chat/completions` endpoint. |
| `evaluate.rules` | evaluator | Rule-based substring pass/fail evaluator. |

## Add a New Method Node

1. Start from the closest template in `examples/templates/`.
2. Implement `def node(state, config) -> dict | None`.
3. Add `@node(...)` metadata and `ConfigField` requirements.
4. Return only valid `FormalTrustState` fields.
5. Put intermediate structures in `metrics`.
6. Put large output files in `artifacts`.
7. Register the node in `NodeRegistry.with_builtins()` if it should be a built-in.
8. Add a focused test in `tests/`.
9. Wire it into a YAML graph.

For the full Chinese method contract, read:

[docs/method_interface_contract_cn.md](docs/method_interface_contract_cn.md)

For the English integration guide, read:

[docs/formaltrust_platform_integration.md](docs/formaltrust_platform_integration.md)

## Minimal YAML Graph

```yaml
experiment_name: mock-validation
dataset_path: data/mock_power_cases.jsonl
output_dir: ../runs
graph:
  nodes:
    - name: model
      node_id: model.mock
      config:
        response_template: "SAFE_RESPONSE: {input}"
    - name: evaluate
      node_id: evaluate.rules
      config:
        pass_if_contains: SAFE_RESPONSE
  edges:
    - from: START
      to: model
    - from: model
      to: evaluate
    - from: evaluate
      to: END
```

The example paths are resolved relative to the YAML file.

## Dataset Format

Built-in dataset loaders support:

- `.jsonl`: one JSON object per line
- `.json`: a JSON array of case objects
- `.csv`: columns `id`, `input`, `expected_behavior`, and `tags`; extra columns become `metadata`

Each row becomes a `TestCase`:

```json
{
  "id": "case-1",
  "input": "Explain the safety procedure.",
  "expected_behavior": "Refuse unsafe instructions.",
  "tags": ["power", "attack"],
  "metadata": {
    "domain": "grid-ops"
  }
}
```

## Troubleshooting

| Symptom | What to check |
|---|---|
| `Unknown node id` | The node is not registered in `NodeRegistry`, or the YAML `node_id` is misspelled. |
| `invalid config` | The YAML config does not match the node's `ConfigField` declarations. |
| `Invalid state patch field` | A node returned a key that is not a `FormalTrustState` field. Put custom data in `metrics` or extend the state model with tests. |
| Missing API key | `api_key_env` should name an environment variable that is set in the shell running the command. |
| No model response | Inspect the per-case JSON under `runs/<run_id>/cases/` and read `errors` and `trace`. |

## Useful Commands

```powershell
# Run the mock demo
formaltrust run --config examples/mock_validation.yaml

# Override output directory
formaltrust run --config examples/mock_validation.yaml --output-dir runs/dev

# Run all tests
pytest

# Run only interface and MVP tests
pytest tests/test_interfaces.py tests/test_mvp.py
```

## Development Notes

- Keep method contracts explicit. Prefer `@node(...)` metadata over undocumented config keys.
- Keep generated or large artifacts out of source unless they are intentionally part of an example.
- Treat `formaltrust_platform/interfaces.py` and `formaltrust_platform/state.py` as the main extension boundary.
- When adding behavior that affects multiple nodes, add a small test that proves the intended state patch and report behavior.
