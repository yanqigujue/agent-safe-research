# Model Endpoints QA Agent Workspaces Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the final shared model endpoint layer, QA workspace, and Agent Flow workspace model visibility described in `docs/superpowers/specs/2026-07-08-model-endpoints-qa-agent-workspaces-design.md`.

**Architecture:** Add a backend `model_endpoints` module that owns endpoint persistence, probing, snapshots, and chat execution. Expose endpoint and QA APIs from `web_api.py`; keep Agent Flow on the existing graph runner while allowing model nodes to resolve `model_endpoint_id`. Update the React desktop app to use workspace-level navigation: Model Endpoints, QA, and Agent Flow.

**Tech Stack:** Python, FastAPI, Pydantic, httpx, pytest, React, TypeScript, Vite, Electron.

---

### Task 1: Backend Model Endpoint Core

**Files:**
- Create: `formaltrust_platform/model_endpoints.py`
- Test: `tests/test_model_endpoints.py`

- [ ] **Step 1: Write failing tests for endpoint defaults, snapshots, and mock chat**

Add `tests/test_model_endpoints.py`:

```python
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
```

- [ ] **Step 2: Run tests to verify failure**

Run: `pytest tests/test_model_endpoints.py -q`

Expected: FAIL because `formaltrust_platform.model_endpoints` does not exist.

- [ ] **Step 3: Implement endpoint models, store, snapshot, and mock chat**

Create `formaltrust_platform/model_endpoints.py` with:

```python
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
        endpoints = [item for item in self.list() if item.endpoint_id != endpoint_id]
        if len(endpoints) == len(self.list()):
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
    except Exception as exc:  # noqa: BLE001 - probe should return a user-visible diagnostic
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
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_model_endpoints.py -q`

Expected: PASS.

- [ ] **Step 5: Commit**

```powershell
git add formaltrust_platform/model_endpoints.py tests/test_model_endpoints.py
git commit -m "Add model endpoint contracts"
```

### Task 2: Web API for Model Endpoints and QA Runs

**Files:**
- Modify: `formaltrust_platform/web_api.py`
- Test: `tests/test_web_api.py`

- [ ] **Step 1: Add failing API tests**

Append to `tests/test_web_api.py`:

```python
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
```

- [ ] **Step 2: Run test to verify failure**

Run: `pytest tests/test_web_api.py::test_web_api_model_endpoints_and_mock_qa_run -q`

Expected: FAIL with 404 for `/api/model-endpoints`.

- [ ] **Step 3: Add API models and endpoints**

In `formaltrust_platform/web_api.py`, import:

```python
from formaltrust_platform.model_endpoints import (
    ModelEndpoint,
    ModelEndpointStore,
    chat_with_endpoint,
    list_ollama_models,
    probe_endpoint,
)
```

Add globals:

```python
MODEL_ENDPOINTS_PATH = EXAMPLES_DIR / "model_endpoints.json"
_model_endpoints = ModelEndpointStore(MODEL_ENDPOINTS_PATH)
```

Add request models:

```python
class ModelEndpointRequest(BaseModel):
    endpoint: dict[str, Any]


class QaRunRequest(BaseModel):
    endpoint_id: str
    prompt: str
    temperature: float = 0
```

Add route functions:

```python
@app.get("/api/model-endpoints")
def list_model_endpoints() -> dict[str, Any]:
    return {"endpoints": [endpoint.model_dump(mode="json") for endpoint in _model_endpoints.list()]}


@app.post("/api/model-endpoints")
def save_model_endpoint(request: ModelEndpointRequest) -> dict[str, Any]:
    endpoint = _model_endpoints.upsert(ModelEndpoint.model_validate(request.endpoint))
    return {"endpoint": endpoint.model_dump(mode="json")}


@app.put("/api/model-endpoints/{endpoint_id}")
def update_model_endpoint(endpoint_id: str, request: ModelEndpointRequest) -> dict[str, Any]:
    endpoint = ModelEndpoint.model_validate({**request.endpoint, "endpoint_id": endpoint_id})
    endpoint = _model_endpoints.upsert(endpoint)
    return {"endpoint": endpoint.model_dump(mode="json")}


@app.delete("/api/model-endpoints/{endpoint_id}")
def delete_model_endpoint(endpoint_id: str) -> dict[str, str]:
    try:
        _model_endpoints.delete(endpoint_id)
        return {"status": "deleted"}
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/api/model-endpoints/{endpoint_id}/probe")
def probe_model_endpoint(endpoint_id: str) -> dict[str, Any]:
    try:
        endpoint = _model_endpoints.get(endpoint_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    probe = probe_endpoint(endpoint)
    updated = endpoint.model_copy(
        update={
            "status": probe.status,
            "last_probe_at": probe.checked_at,
            "last_probe_error": probe.error,
        }
    )
    _model_endpoints.upsert(updated)
    return {"probe": probe.model_dump(mode="json"), "endpoint": updated.model_dump(mode="json")}


@app.get("/api/ollama/models")
def ollama_models(base_url: str = Query("http://127.0.0.1:11434")) -> dict[str, Any]:
    return {"models": list_ollama_models(base_url)}


@app.post("/api/qa/run")
def run_qa(request: QaRunRequest) -> dict[str, Any]:
    try:
        endpoint = _model_endpoints.get(request.endpoint_id)
        result = chat_with_endpoint(endpoint, request.prompt, temperature=request.temperature)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    run_id = f"qa-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"
    payload = {
        "run_id": run_id,
        "run_type": "qa",
        "input": {"prompt": request.prompt},
        "answer": result.answer,
        "model_snapshot": result.model_snapshot,
        "latency_ms": result.latency_ms,
        "evaluation": {"passed": True, "label": "completed", "score": 1.0, "reasons": []},
        "raw": result.raw,
    }
    run_dir = RUNS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "qa_result.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload
```

- [ ] **Step 4: Run API tests**

Run: `pytest tests/test_web_api.py tests/test_model_endpoints.py -q`

Expected: PASS.

- [ ] **Step 5: Commit**

```powershell
git add formaltrust_platform/web_api.py tests/test_web_api.py
git commit -m "Expose model endpoints and QA run API"
```

### Task 3: Resolve Model Endpoint IDs in Model Nodes

**Files:**
- Modify: `formaltrust_platform/nodes/models.py`
- Modify: `formaltrust_platform/web_api.py`
- Test: `tests/test_interfaces.py`

- [ ] **Step 1: Add failing test for `model_endpoint_id` config**

Add to `tests/test_interfaces.py`:

```python
def test_model_node_accepts_model_endpoint_id_config() -> None:
    registry = NodeRegistry.with_builtins()
    descriptor = registry.describe("model.openai_compatible")
    field_names = {field.name for field in descriptor.config_fields}

    assert "model_endpoint_id" in field_names
```

- [ ] **Step 2: Run test to verify failure**

Run: `pytest tests/test_interfaces.py::test_model_node_accepts_model_endpoint_id_config -q`

Expected: FAIL because `model_endpoint_id` is not declared.

- [ ] **Step 3: Update node config contract and execution**

In `formaltrust_platform/nodes/models.py`, add `model_endpoint_id` as an optional config field and resolve it before falling back to explicit provider config:

```python
ConfigField(
    "model_endpoint_id",
    description="Shared model endpoint id. When set, base_url/model/api_key_env are resolved from the endpoint store.",
),
```

Use:

```python
if config.get("model_endpoint_id"):
    from formaltrust_platform.web_api import MODEL_ENDPOINTS_PATH
    from formaltrust_platform.model_endpoints import ModelEndpointStore, chat_with_endpoint

    endpoint = ModelEndpointStore(MODEL_ENDPOINTS_PATH).get(str(config["model_endpoint_id"]))
    result = chat_with_endpoint(endpoint, state.prompt or state.case.input, temperature=float(config.get("temperature", 0)))
    return {
        "model_response": ModelResponse(
            content=result.answer,
            model=str(result.model_snapshot["model"]),
            raw=result.raw,
            latency_ms=result.latency_ms,
        ),
        "metrics": {"model_called": True, "model_snapshot": result.model_snapshot},
    }
```

Keep explicit `base_url`, `model`, and `api_key_env` behavior unchanged when `model_endpoint_id` is absent.

- [ ] **Step 4: Run interface tests**

Run: `pytest tests/test_interfaces.py::test_model_node_accepts_model_endpoint_id_config tests/test_interfaces.py::test_validate_config_flags_missing_unknown_and_wrong_type -q`

Expected: PASS.

- [ ] **Step 5: Commit**

```powershell
git add formaltrust_platform/nodes/models.py tests/test_interfaces.py
git commit -m "Allow model nodes to use shared endpoints"
```

### Task 4: Frontend API Types

**Files:**
- Modify: `ui/src/lib/api.ts`

- [ ] **Step 1: Add endpoint and QA types**

In `ui/src/lib/api.ts`, add:

```ts
export type ModelEndpoint = {
  endpoint_id: string
  name: string
  kind: string
  provider: string
  base_url: string | null
  model: string
  api_key_env: string | null
  capabilities: string[]
  status: 'unchecked' | 'available' | 'unavailable' | 'error' | string
  last_probe_at: string | null
  last_probe_error: string | null
  metadata: Record<string, unknown>
}

export type ModelEndpointProbe = {
  endpoint_id: string
  status: string
  checked_at: string
  models: string[]
  error: string | null
}

export type QaRunResult = {
  run_id: string
  run_type: 'qa'
  input: { prompt: string; case_id?: string | null }
  answer: string
  model_snapshot: Record<string, unknown>
  latency_ms: number
  evaluation: {
    passed: boolean
    label: string
    score: number
    reasons: string[]
  }
  raw: Record<string, unknown>
}
```

- [ ] **Step 2: Add API calls**

Add to `api`:

```ts
modelEndpoints: () => apiFetch<{ endpoints: ModelEndpoint[] }>('/api/model-endpoints'),
saveModelEndpoint: (endpoint: ModelEndpoint) =>
  apiFetch<{ endpoint: ModelEndpoint }>('/api/model-endpoints', {
    method: 'POST',
    body: JSON.stringify({ endpoint }),
  }),
probeModelEndpoint: (endpointId: string) =>
  apiFetch<{ probe: ModelEndpointProbe; endpoint: ModelEndpoint }>(
    `/api/model-endpoints/${encodeURIComponent(endpointId)}/probe`,
    { method: 'POST' },
  ),
ollamaModels: (baseUrl: string) =>
  apiFetch<{ models: string[] }>(`/api/ollama/models?base_url=${encodeURIComponent(baseUrl)}`),
runQa: (endpointId: string, prompt: string, temperature = 0) =>
  apiFetch<QaRunResult>('/api/qa/run', {
    method: 'POST',
    body: JSON.stringify({ endpoint_id: endpointId, prompt, temperature }),
  }),
```

- [ ] **Step 3: Run frontend lint**

Run: `cd ui; npm run lint`

Expected: PASS or only the existing `button.tsx` warning.

- [ ] **Step 4: Commit**

```powershell
git add ui/src/lib/api.ts
git commit -m "Add frontend model endpoint API types"
```

### Task 5: Desktop Workspaces and Endpoint Resource Panel

**Files:**
- Modify: `ui/src/App.tsx`
- Modify: `ui/src/index.css`

- [ ] **Step 1: Add workspace state and endpoint loading**

In `ui/src/App.tsx`, add:

```ts
type Workspace = 'model-endpoints' | 'qa' | 'agent-flow'
const [workspace, setWorkspace] = useState<Workspace>('qa')
const [modelEndpoints, setModelEndpoints] = useState<ModelEndpoint[]>([])
const [selectedEndpointId, setSelectedEndpointId] = useState('mock-offline')
```

Update bootstrap:

```ts
const [endpointResponse, catalogResponse, configResponse, datasetResponse, runResponse, jobResponse] = await Promise.all([
  api.modelEndpoints(),
  api.catalog(),
  api.configs(),
  api.datasets(),
  api.runs(),
  api.jobs(),
])
setModelEndpoints(endpointResponse.endpoints)
setSelectedEndpointId(endpointResponse.endpoints[0]?.endpoint_id ?? 'mock-offline')
```

- [ ] **Step 2: Add workspace switcher component**

Add a component:

```tsx
function WorkspaceSwitcher({
  workspace,
  onWorkspaceChange,
}: {
  workspace: Workspace
  onWorkspaceChange: (workspace: Workspace) => void
}) {
  const items: Array<{ id: Workspace; label: string }> = [
    { id: 'model-endpoints', label: '模型连接' },
    { id: 'qa', label: '问答' },
    { id: 'agent-flow', label: 'Agent 流程' },
  ]
  return (
    <div className="workspace-switcher">
      {items.map((item) => (
        <button
          key={item.id}
          type="button"
          className={cn('workspace-switcher-item', workspace === item.id && 'workspace-switcher-item-active')}
          onClick={() => onWorkspaceChange(item.id)}
        >
          {item.label}
        </button>
      ))}
    </div>
  )
}
```

- [ ] **Step 3: Add endpoint status pill**

Add:

```tsx
function EndpointPill({ endpoint }: { endpoint: ModelEndpoint | undefined }) {
  if (!endpoint) return <Badge variant="outline">未选择模型</Badge>
  return (
    <div className="endpoint-pill">
      <span>{endpoint.provider || endpoint.kind}</span>
      <span>{endpoint.model}</span>
      <Badge variant={endpoint.status === 'available' ? 'success' : endpoint.status === 'error' ? 'destructive' : 'secondary'}>
        {endpoint.status}
      </Badge>
    </div>
  )
}
```

- [ ] **Step 4: Add CSS**

Add to `ui/src/index.css`:

```css
.workspace-switcher {
  @apply flex gap-1 rounded-md border bg-card p-1 shadow-sm;
}

.workspace-switcher-item {
  @apply rounded-md px-3 py-1.5 text-sm text-muted-foreground transition-colors hover:bg-muted hover:text-foreground;
}

.workspace-switcher-item-active {
  @apply bg-primary text-primary-foreground hover:bg-primary hover:text-primary-foreground;
}

.endpoint-pill {
  @apply inline-flex min-w-0 items-center gap-2 rounded-md border bg-background px-2 py-1 text-xs;
}
```

- [ ] **Step 5: Run lint**

Run: `cd ui; npm run lint`

Expected: PASS or only existing `button.tsx` warning.

- [ ] **Step 6: Commit**

```powershell
git add ui/src/App.tsx ui/src/index.css
git commit -m "Add workspace switcher and endpoint summary"
```

### Task 6: QA Workspace

**Files:**
- Modify: `ui/src/App.tsx`
- Modify: `ui/src/index.css`

- [ ] **Step 1: Add QA state**

Add:

```ts
const [qaPrompt, setQaPrompt] = useState('请总结当前电网运行风险。')
const [qaResult, setQaResult] = useState<QaRunResult | null>(null)
```

- [ ] **Step 2: Add QA run function**

Add:

```ts
async function runQa() {
  setBusy('run')
  setNotice(null)
  try {
    const result = await api.runQa(selectedEndpointId, qaPrompt)
    setQaResult(result)
    setNotice('问答运行完成。')
  } catch (error) {
    setNotice(error instanceof Error ? error.message : String(error))
  } finally {
    setBusy('idle')
  }
}
```

- [ ] **Step 3: Add QA panel**

Add:

```tsx
function QaWorkspace({
  endpoints,
  selectedEndpointId,
  prompt,
  result,
  busy,
  onEndpointChange,
  onPromptChange,
  onRun,
}: {
  endpoints: ModelEndpoint[]
  selectedEndpointId: string
  prompt: string
  result: QaRunResult | null
  busy: BusyState
  onEndpointChange: (value: string) => void
  onPromptChange: (value: string) => void
  onRun: () => void
}) {
  const endpoint = endpoints.find((item) => item.endpoint_id === selectedEndpointId)
  return (
    <div className="workspace-stack">
      <div className="workspace-header">
        <div>
          <h2>问答</h2>
          <EndpointPill endpoint={endpoint} />
        </div>
        <Button onClick={onRun} disabled={busy !== 'idle'}>
          {busy === 'run' ? <Loader2 className="size-4 animate-spin" /> : <Play className="size-4" />}
          运行
        </Button>
      </div>
      <div className="workspace-two-column">
        <section className="workspace-panel">
          <Label>模型连接</Label>
          <select className={selectClass} value={selectedEndpointId} onChange={(event) => onEndpointChange(event.target.value)}>
            {endpoints.map((endpoint) => (
              <option key={endpoint.endpoint_id} value={endpoint.endpoint_id}>
                {endpoint.name} / {endpoint.model}
              </option>
            ))}
          </select>
          <Label>Prompt</Label>
          <Textarea value={prompt} onChange={(event) => onPromptChange(event.target.value)} className="min-h-40" />
        </section>
        <section className="workspace-panel">
          <h3>回答</h3>
          {result ? (
            <>
              <div className="qa-answer">{result.answer}</div>
              <pre className="json-preview">{JSON.stringify(result.model_snapshot, null, 2)}</pre>
            </>
          ) : (
            <div className="empty-state">运行后这里显示模型回答和快照。</div>
          )}
        </section>
      </div>
    </div>
  )
}
```

- [ ] **Step 4: Add CSS**

Add:

```css
.workspace-stack {
  @apply flex min-h-full flex-col gap-3;
}

.workspace-header {
  @apply flex items-center justify-between gap-3 rounded-md border bg-card px-3 py-2;
}

.workspace-two-column {
  @apply grid min-h-0 flex-1 grid-cols-2 gap-3;
}

.workspace-panel {
  @apply flex min-h-0 flex-col gap-3 rounded-md border bg-card p-3;
}

.qa-answer {
  @apply min-h-40 rounded-md border bg-background p-3 text-sm leading-6;
}

.json-preview {
  @apply max-h-72 overflow-auto rounded-md border bg-muted p-3 text-xs;
}

.empty-state {
  @apply rounded-md border border-dashed bg-muted/40 p-6 text-sm text-muted-foreground;
}
```

- [ ] **Step 5: Run lint and backend QA API test**

Run:

```powershell
cd ui; npm run lint
cd ..; pytest tests/test_web_api.py::test_web_api_model_endpoints_and_mock_qa_run -q
```

Expected: frontend lint passes with existing warning only; backend test passes.

- [ ] **Step 6: Commit**

```powershell
git add ui/src/App.tsx ui/src/index.css
git commit -m "Add QA workspace"
```

### Task 7: Agent Flow Endpoint Visibility

**Files:**
- Modify: `ui/src/App.tsx`
- Modify: `ui/src/index.css`

- [ ] **Step 1: Add endpoint summary extraction**

Add:

```ts
function endpointIdsFromConfig(config: ExperimentConfig): string[] {
  return Array.from(
    new Set(
      config.graph.nodes
        .map((node) => node.config.model_endpoint_id)
        .filter((value): value is string => typeof value === 'string' && value.length > 0),
    ),
  )
}
```

- [ ] **Step 2: Add Agent Flow header component**

Add:

```tsx
function AgentFlowHeader({
  draft,
  endpoints,
  onRun,
  busy,
}: {
  draft: ExperimentConfig
  endpoints: ModelEndpoint[]
  onRun: () => void
  busy: BusyState
}) {
  const endpointIds = endpointIdsFromConfig(draft)
  const resolved = endpointIds.map((id) => endpoints.find((endpoint) => endpoint.endpoint_id === id)).filter(Boolean)
  return (
    <div className="workspace-header">
      <div>
        <h2>Agent 流程</h2>
        <div className="endpoint-row">
          {resolved.length ? resolved.map((endpoint) => <EndpointPill key={endpoint!.endpoint_id} endpoint={endpoint} />) : <Badge variant="outline">未绑定共享模型连接</Badge>}
        </div>
      </div>
      <Button onClick={onRun} disabled={busy !== 'idle'}>
        <Play className="size-4" />
        运行流程
      </Button>
    </div>
  )
}
```

- [ ] **Step 3: Render Agent Flow workspace**

Wrap the existing configure/run/results panels inside `workspace === 'agent-flow'`, with `AgentFlowHeader` above the existing panel.

- [ ] **Step 4: Add CSS**

Add:

```css
.endpoint-row {
  @apply mt-2 flex flex-wrap gap-2;
}
```

- [ ] **Step 5: Run lint**

Run: `cd ui; npm run lint`

Expected: PASS or only existing warning.

- [ ] **Step 6: Commit**

```powershell
git add ui/src/App.tsx ui/src/index.css
git commit -m "Show model endpoints in agent flow"
```

### Task 8: Verification and Desktop Packaging Check

**Files:**
- Verify only unless fixes are needed.

- [ ] **Step 1: Run focused backend tests**

Run:

```powershell
pytest tests/test_model_endpoints.py tests/test_web_api.py tests/test_interfaces.py -q
```

Expected: PASS.

- [ ] **Step 2: Run frontend lint/build**

Run:

```powershell
cd ui
npm run lint
npm run build
```

Expected: lint passes with only known `button.tsx` warning; build passes.

- [ ] **Step 3: Start or open the desktop app**

Run the packaged app or dev server path used by this workspace. Confirm:

- Model Endpoints workspace shows mock and local Ollama.
- QA workspace shows selected endpoint in the header and can run mock QA.
- Agent Flow workspace still shows existing graph editor and displays endpoint badges when a node has `model_endpoint_id`.

- [ ] **Step 4: Commit verification fixes if any**

If a fix is needed:

```powershell
git add <changed files>
git commit -m "Stabilize QA and agent workspace integration"
```

