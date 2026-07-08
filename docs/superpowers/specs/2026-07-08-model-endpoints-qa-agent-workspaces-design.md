# Model Endpoints, QA Workspace, and Agent Flow Workspace Design

Date: 2026-07-08

## Goal

FormalTrust should present itself as two clear workspaces backed by one shared model-connection layer:

- **QA Workspace**: prompt/case/dataset -> model -> answer -> score and failure analysis.
- **Agent Flow Workspace**: task/case -> agent components, trace, tools, skills, memory, guardrails, evaluator -> final action or answer.

The platform must always show which model endpoint is currently being used, whether it is local Ollama, OpenAI-compatible API, or mock/offline. Historical results must preserve a model snapshot so a result can be audited later without guessing which model produced it.

This design is the target architecture. Implementation can be sequenced, but the data contracts and UI boundaries should point at this final shape from the beginning.

## Product Information Architecture

The desktop UI has three stable top-level concepts:

1. **Model Endpoints**
   Shared resource used by both workspaces.

2. **QA**
   Direct model answer testing.

3. **Agent Flow**
   Node graph, trace import, authority/guardrail analysis, and workflow evaluation.

Resource lists, run history, datasets, and logs stay available, but they are secondary navigation inside these workspaces. The main mental model is no longer "configure experiment first"; it is "choose QA or Agent Flow, then select model endpoint and data."

## Model Endpoint Contract

Add a platform-level model endpoint resource. It is not owned by any single node.

```json
{
  "endpoint_id": "ollama-qwen2-5-7b",
  "name": "Local Qwen 2.5 7B",
  "kind": "ollama",
  "provider": "Ollama",
  "base_url": "http://127.0.0.1:11434",
  "model": "qwen2.5:7b",
  "api_key_env": null,
  "capabilities": ["chat", "json_output"],
  "status": "available",
  "last_probe_at": "2026-07-08T10:47:00Z",
  "last_probe_error": null
}
```

Required endpoint kinds:

- `ollama`
- `openai_compatible`
- `mock`

Endpoint kinds should remain strings rather than closed enums in persisted files. New providers such as vLLM, LM Studio, Azure OpenAI, or custom lab endpoints can be added without a schema migration.

Secrets are never stored. `api_key_env` names an environment variable only.

## Model Snapshot Contract

Every QA or Agent run stores a snapshot of the endpoint actually used.

```json
{
  "endpoint_id": "ollama-qwen2-5-7b",
  "kind": "ollama",
  "provider": "Ollama",
  "base_url": "http://127.0.0.1:11434",
  "model": "qwen2.5:7b",
  "api_key_env": null,
  "resolved_at": "2026-07-08T10:49:12Z",
  "status_at_run_start": "available"
}
```

Agent flows can have multiple snapshots keyed by role:

```json
{
  "planner": {"endpoint_id": "ollama-qwen2-5-7b", "model": "qwen2.5:7b"},
  "actor": {"endpoint_id": "deepseek-chat-api", "model": "deepseek-chat"},
  "evaluator": {"endpoint_id": "mock-offline", "model": "mock-safe-model"}
}
```

The UI displays these snapshots in run details and reports.

## Backend API

Add shared endpoint APIs:

```text
GET  /api/model-endpoints
POST /api/model-endpoints
PUT  /api/model-endpoints/{endpoint_id}
DELETE /api/model-endpoints/{endpoint_id}
POST /api/model-endpoints/{endpoint_id}/probe
GET  /api/ollama/models?base_url=http://127.0.0.1:11434
```

Add QA APIs:

```text
POST /api/qa/run
GET  /api/qa/runs
GET  /api/qa/runs/{run_id}
```

Agent flow continues to use the existing experiment config and job runner, but config validation and run summaries gain endpoint awareness:

```text
POST /api/jobs/run
GET  /api/runs
GET  /api/runs/{run_id}
```

The existing `/api/catalog` remains the node interface catalog. `/api/agent-interfaces` remains the agent runtime object catalog. Model endpoints are a third catalog, not a replacement for either.

## Endpoint Execution Semantics

The backend owns provider-specific calling logic.

For `ollama`:

- List models with `GET {base_url}/api/tags`.
- Chat/generate through Ollama's local API.
- Preserve raw response in run artifacts or structured result metadata.

For `openai_compatible`:

- Use `{base_url}/chat/completions`.
- Read the secret from `api_key_env`.
- Store only the env var name in configs and snapshots.

For `mock`:

- Return deterministic output suitable for offline testing.

The frontend never constructs provider-specific request bodies beyond choosing an endpoint and task input.

## QA Workspace

The QA workspace supports:

- Single prompt input.
- Dataset/case selection.
- Model endpoint selector with visible status.
- Optional evaluation rule or evaluator endpoint.
- Run button.
- Answer panel.
- Score/failure panel.
- Run history filtered to `run_type = "qa"`.

Header example:

```text
QA    Model: Ollama - qwen2.5:7b - Local - Available
```

QA result shape:

```json
{
  "run_id": "qa-20260708-104912",
  "run_type": "qa",
  "input": {"prompt": "...", "case_id": null},
  "answer": "...",
  "model_snapshot": {...},
  "latency_ms": 820,
  "evaluation": {"passed": true, "label": "pass", "score": 1.0, "reasons": []},
  "raw": {}
}
```

## Agent Flow Workspace

The Agent Flow workspace keeps the current node graph and configuration depth, but reorganizes it around agent-flow inspection:

- Workflow header with model role summary.
- Graph/config editor.
- Node contract panel.
- Trace/agent interface panel.
- Run controls.
- Step-by-step inputs and outputs.
- Guardrail decisions.
- Final action/answer.
- Run history filtered to `run_type = "agent"`.

Header example for one model:

```text
Agent Flow    Model: API - deepseek-chat - OPENAI_API_KEY - Available
```

Header example for role-bound endpoints:

```text
Agent Flow
planner: Ollama - qwen2.5:7b
actor: API - deepseek-chat
evaluator: Mock - offline
```

Agent flow configs can keep existing node `config` blocks, but model nodes should support `model_endpoint_id`. Explicit node config remains available for advanced cases, but the UI should prefer endpoint selection.

## Run Record Unification

Do not create two incompatible result systems. Store one normalized run envelope:

```json
{
  "run_id": "...",
  "run_type": "qa | agent",
  "started_at": "...",
  "finished_at": "...",
  "status": "succeeded | failed | running",
  "model_snapshots": [],
  "summary": {},
  "artifacts": {},
  "workspace_payload": {}
}
```

`workspace_payload` differs by run type:

- QA: prompt, answer, scoring, raw model response.
- Agent: config path, node trace, agent trace events, final action, guardrail/evaluator metrics.

The UI can show separate QA and Agent histories without duplicating storage logic.

## Dataset Organization

Datasets can already contain both QA and agent cases. The platform should classify cases by metadata:

- `scenario_kind = "qa"` or `task_type = "direct_qa"` -> QA.
- `scenario_kind = "agent"` or presence of `agent_trace_events` / `candidate_action` -> Agent Flow.

The UI should filter datasets by workspace while preserving the same `TestCase` loader.

## UI Layout Requirements

The app shell should become:

- Top native menu remains.
- Left rail: workspace switcher and resource groups.
- Main area: selected workspace.
- Right rail: current status, selected endpoint status, run log, recent results.

Each workspace header must show:

- workspace name;
- selected endpoint or endpoint roles;
- connection status;
- last probe time or error;
- run button state.

No user should need to open a node card to know whether the current run uses Ollama, API, or Mock.

## Compatibility With Existing FormalTrust Nodes

Existing nodes remain valid.

Compatibility path:

- `model.openai_compatible` can accept explicit `base_url/model/api_key_env` as today.
- New UI-generated configs prefer `model_endpoint_id`.
- During graph assembly or node execution, `model_endpoint_id` resolves to a model snapshot and provider config.
- Existing AFW/EAIR metrics such as `candidate_action`, `final_action`, `agent_trace_events`, `afw_source_events`, and `afw_consumptions` remain unchanged.

## Error Handling

Endpoint probe:

- `available` when the endpoint responds and the model is usable.
- `unavailable` when the endpoint is reachable but invalid or missing model.
- `error` when network, auth, or provider response fails.
- `unchecked` before probe.

QA run:

- If endpoint is unavailable, block run with a clear message.
- If model call fails, record failed run with endpoint snapshot and raw error.

Agent flow run:

- Config validation should surface missing endpoint IDs.
- Runtime failure should attach endpoint snapshot to the failed run for debugging.

## Tests

Backend tests:

- model endpoint CRUD and validation;
- Ollama model listing with mocked HTTP transport;
- endpoint probe for Ollama, OpenAI-compatible, and mock;
- QA run with mock endpoint;
- QA run records `model_snapshot`;
- Agent config using `model_endpoint_id` resolves snapshot;
- existing node catalog and agent interface catalog stay stable.

Frontend tests or checks:

- workspace switcher renders QA and Agent Flow;
- QA header shows endpoint kind/provider/model/status;
- Agent Flow header shows role-bound endpoint badges;
- endpoint errors are visible without opening advanced config;
- long model names and env var names do not overflow.

## Stability Rules

- Model endpoints are shared resources, not copied into each workspace.
- Persisted endpoint records store env var names, never secrets.
- Endpoint kinds, component kinds, and event types are strings with canonical recommendations, not closed schemas.
- Run history always stores snapshots, not references only.
- Agent runtime objects continue to use `agent-runtime-interface/v1`.
- UI can add richer views, but the underlying contract should remain endpoint + run snapshot + workspace payload.
