# FormalTrust Platform Integration Guide

FormalTrust is a modular LLM-trustworthiness testing platform. A run flows through a
graph of nodes: **attack → guardrail → model → guardrail → evaluate**, carrying a
single `FormalTrustState` per test case. Every pluggable part — node roles, dataset
loaders, reporters — has a **clear, self-describing interface with declared
requirements**, defined in `formaltrust_platform/interfaces.py`.

## Quick Start

Run the local mock demo without any API key:

```powershell
formaltrust run --config examples/mock_validation.yaml
```

This creates `runs/<run_id>/` with `results.json`, per-case JSON files, and a
debug-oriented `report.md`.

---

## The node interface

Every node is a callable with the same signature:

```python
def my_node(state: FormalTrustState, config: Mapping[str, Any]) -> dict[str, Any] | None:
    ...
```

- **`state`** — the current `FormalTrustState` (read-only; never mutate in place).
- **`config`** — this node's `config` block from the YAML.
- **return** — a *patch* dict whose keys must be fields of `FormalTrustState`
  (or `None` for "no change"). `metrics` and `artifacts` are merged; other
  fields are replaced. Returning an unknown field is reported as a friendly
  per-case error and the batch continues.

### Role contracts

Each role has a `Protocol` in `formaltrust_platform.interfaces` documenting exactly
what it reads and what it must write:

| Role (`interfaces`) | Reads | Must return | Notes |
|---|---|---|---|
| `AttackNode` | `state.case.input` | `{"prompt": str}` | Should also set `attack: AttackResult`; may add `retrieval_context`. |
| `GuardrailNode` | input: `state.prompt`; output: `state.model_response` | (optional patch) | Raise — or call `state.add_error(...)` — to block a case. |
| `ModelNode` | `state.prompt` (→ `case.input`) | `{"model_response": ModelResponse}` | **Read secrets from env vars only**, never from `config`. |
| `EvaluatorNode` | `state.model_response` | `{"evaluation": EvaluationResult}` | |

Construct nested objects with the Pydantic models from `formaltrust_platform.state`
(`AttackResult`, `ModelResponse`, `EvaluationResult`, `RetrievedDocument`).

### Declaring an interface (config requirements)

Use the `@node(...)` decorator to bind interface metadata — category, a one-line
summary, and the node's **configuration requirements** — to the function. This is
what makes a node self-describing and lets the platform validate config before a run:

```python
from formaltrust_platform.interfaces import ConfigField, node
from formaltrust_platform.state import FormalTrustState, ModelResponse

@node(
    "model.custom",
    category="model",
    summary="Example custom model node.",
    config_fields=[
        ConfigField("base_url", required=True, description="Endpoint base URL."),
        ConfigField("api_key_env", required=True, secret_env=True,
                    description="Env var name holding the API key."),
        ConfigField("temperature", type="float", default=0, description="Sampling temperature."),
    ],
)
def custom_model_node(state, config):
    ...
```

`ConfigField` fields:

| Field | Meaning |
|---|---|
| `name` | Config key. |
| `type` | One of `str`, `int`, `float`, `bool`, `list`, `dict`. |
| `required` | If true, the run fails fast when the key is absent. |
| `default` | Documented default (the node still reads `config.get(...)`). |
| `description` | Human-readable explanation (shown in diagnostics). |
| `secret_env` | The value *names an environment variable* holding a secret. The platform only checks the variable exists; it never copies the secret. |

Decorated functions stay plain callables — they can still be called or registered
directly. Working examples live in `examples/templates/{attack,model,evaluator,guardrail}_node.py`.

### Registering and discovering nodes

```python
from formaltrust_platform.registry import NodeRegistry

registry = NodeRegistry.with_builtins()

registry.register(custom_model_node)            # @node-decorated → uses its declared id
registry.register("custom.plain", plain_fn)     # plain callable → recorded as a "custom" node

# Discover what exists and what each node requires:
for d in registry.catalog():
    print(d.node_id, d.category, [f.name for f in d.config_fields])
print(registry.describe("model.openai_compatible").config_fields)
```

Both registration styles are supported; the two-argument form keeps older code working.

### Config validation & friendly diagnostics

When a graph is assembled, each node's YAML `config` is checked against its declared
requirements with `validate_config(...)`. A problem fails the run **once, up front**,
with a clear message instead of a deep `KeyError`:

```
Node 'model' (model.openai_compatible) has invalid config: missing required config
'base_url' (Endpoint base URL, ...)
```

Validation catches missing required fields, wrong value types, and unknown fields.
Secret-env presence (`secret_env` → is the env var actually set?) is reported by
`validate_config(..., check_env=True)` but **not** enforced at assembly time, so a
graph can be validated offline; the model node reads the key at run time.

---

## Built-in nodes

| `node_id` | Category | Key config |
|---|---|---|
| `attack.template` | attack | `attack_type`, `template`, `poison_document` (all optional) |
| `guardrail.input.noop` / `guardrail.output.noop` | guardrail | — |
| `model.mock` | model | `model`, `response_template` (optional; no key needed) |
| `model.openai_compatible` | model | **required** `base_url`, `model`, `api_key_env`; optional `temperature`, `timeout_seconds` |
| `evaluate.rules` | evaluator | `pass_if_contains`, `fail_if_contains` (optional) |

`model.openai_compatible` targets any OpenAI-compatible `/chat/completions`
endpoint (OpenAI, Azure OpenAI, Ollama, vLLM, DeepSeek, …) and reads its key only
from the environment variable named by `api_key_env`:

```yaml
node_id: model.openai_compatible
config:
  base_url: https://api.deepseek.com/v1
  model: deepseek-chat
  api_key_env: DEEPSEEK_API_KEY
```

To add another provider (e.g. Anthropic Claude, Google Gemini), implement a node
against the `ModelNode` contract using that provider's SDK or REST API, declare its
config with `@node(...)`, and register it — see `examples/templates/model_node.py`.

---

## Dataset interface

A dataset loader satisfies `interfaces.DatasetLoader` — `(path) -> list[TestCase]`.
`datasets.load_cases(path)` dispatches by file extension across the built-in loaders:

| Extension | Loader | Format |
|---|---|---|
| `.jsonl` | `load_jsonl_cases` | one JSON object per line |
| `.json` | `load_json_cases` | a single JSON array of case objects |
| `.csv` | `load_csv_cases` | `id`/`input`/`expected_behavior` columns map directly; `tags` is split on `;`; other columns become `metadata` |

All three produce equivalent `TestCase` lists. See `examples/data/mock_power_cases.{jsonl,csv}`.

---

## YAML graph

```yaml
graph:
  nodes:
    - name: model
      node_id: model.mock
      config:
        response_template: "SAFE_RESPONSE: {input}"
  edges:
    - from: START
      to: model
    - from: model
      to: END
```

Conditional edge predicates: `has_errors`, `no_errors`, `halted`.
