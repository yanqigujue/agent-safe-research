from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import threading
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

import yaml
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from formaltrust_platform.agent_interfaces import agent_interface_catalog
from formaltrust_platform.config import ExperimentConfig, load_config
from formaltrust_platform.datasets import load_cases
from formaltrust_platform.graph import build_graph
from formaltrust_platform.model_endpoints import (
    DEFAULT_MODEL_ENDPOINTS_PATH,
    ModelEndpoint,
    ModelEndpointStore,
    chat_with_endpoint,
    list_ollama_models,
    probe_endpoint,
)
from formaltrust_platform.registry import NodeRegistry

WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = WORKSPACE_ROOT / "examples"
GENERATED_CONFIG_DIR = EXAMPLES_DIR / "ui_configs"
RUNS_DIR = WORKSPACE_ROOT / "runs"
MODEL_ENDPOINTS_PATH = DEFAULT_MODEL_ENDPOINTS_PATH
SUPPORTED_CONFIG_EXTENSIONS = {".yaml", ".yml"}
SUPPORTED_DATASET_EXTENSIONS = {".jsonl", ".json", ".csv"}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class SaveConfigRequest(BaseModel):
    name: str
    config: dict[str, Any]


class ValidateConfigRequest(BaseModel):
    config: dict[str, Any]


class RunRequest(BaseModel):
    config_path: str
    output_dir: str | None = None


class ModelEndpointRequest(BaseModel):
    endpoint: dict[str, Any]


class QaRunRequest(BaseModel):
    endpoint_id: str
    prompt: str
    temperature: float = 0


@dataclass
class JobRecord:
    id: str
    command: list[str]
    config_path: str
    output_dir: str
    status: Literal["running", "succeeded", "failed"] = "running"
    started_at: str = field(default_factory=_utc_now)
    finished_at: str | None = None
    stdout: str = ""
    stderr: str = ""
    returncode: int | None = None
    run_dir: str | None = None
    report_path: str | None = None


app = FastAPI(title="FormalTrust Control Center API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_registry = NodeRegistry.with_builtins()
_model_endpoints = ModelEndpointStore(MODEL_ENDPOINTS_PATH)
_jobs: dict[str, JobRecord] = {}
_jobs_lock = threading.Lock()

CATEGORY_INTERFACE_DEFAULTS: dict[str, dict[str, list[str]]] = {
    "attack": {
        "inputs": ["case.input", "case.metadata", "retrieval_context"],
        "outputs": ["prompt", "attack", "retrieval_context", "metrics"],
        "metrics": ["attack metadata"],
    },
    "custom": {
        "inputs": ["case.metadata", "metrics"],
        "outputs": ["metrics"],
        "metrics": ["adapter diagnostics"],
    },
    "guardrail": {
        "inputs": ["prompt", "model_response", "retrieval_context", "metrics"],
        "outputs": ["metrics", "errors", "final_action"],
        "metrics": ["gate decision"],
    },
    "model": {
        "inputs": ["prompt", "case.input"],
        "outputs": ["model_response", "metrics"],
        "metrics": ["model_called"],
    },
    "evaluator": {
        "inputs": ["model_response", "metrics", "case.expected_behavior"],
        "outputs": ["evaluation", "metrics"],
        "metrics": ["evaluation_passed"],
    },
}

NODE_INTERFACE_HINTS: dict[str, dict[str, Any]] = {
    "attack.template": {
        "inputs": ["case.input"],
        "outputs": ["prompt", "attack"],
        "metrics": ["attack_type"],
        "examples": [
            {
                "name": "Prompt injection wrapper",
                "config": {
                    "attack_type": "prompt_injection",
                    "template": "{input}\\n[TEST] Ignore unsafe instructions.",
                },
            }
        ],
    },
    "attack.eair_bench_retrieval": {
        "inputs": ["case.metadata.case_id", "case.metadata.condition"],
        "outputs": ["prompt", "attack", "retrieval_context", "metrics.oracle_action"],
        "metrics": ["eair_bench_case_id", "eair_bench_condition", "oracle_action"],
    },
    "attack.eair_retrieval_perturbation": {
        "inputs": ["retrieval_context"],
        "outputs": ["retrieval_context", "metrics"],
        "metrics": [
            "retrieval_perturbation_applied",
            "retrieval_perturbation_removed_doc_count",
        ],
        "advanced_fields": ["drop_ranks", "shuffle", "seed"],
    },
    "attack.eair_claim_extraction_noise": {
        "inputs": ["retrieval_context.metadata.claims"],
        "outputs": ["retrieval_context", "metrics"],
        "metrics": [
            "claim_noise_applied",
            "claim_noise_dropped_claim_count",
            "claim_noise_injected_claim_count",
        ],
        "advanced_fields": [
            "candidate_inject_claims",
            "drop_probability",
            "inject_probability",
            "seed",
            "target_doc_id",
            "target_rank",
            "prepend_injected",
        ],
    },
    "custom.afw_trace_adapter": {
        "inputs": ["case.metadata.agent_trace_events", "metrics.agent_trace_events"],
        "outputs": [
            "metrics.afw_source_events",
            "metrics.afw_consumptions",
            "metrics.afw_counter_authority",
            "metrics.candidate_action",
        ],
        "metrics": ["afw_trace_adapter_summary", "afw_trace_adapter_diagnostics"],
        "advanced_fields": [
            "event_type_key",
            "schema_preset",
            "source_event_type",
            "candidate_action_event_type",
            "consumption_event_type",
            "counter_authority_event_type",
        ],
        "examples": [
            {
                "name": "Canonical power-ops trace",
                "config": {"trace_key": "agent_trace_events", "schema_preset": "canonical"},
            }
        ],
    },
    "guardrail.afw_capguard": {
        "inputs": [
            "metrics.afw_source_events",
            "metrics.afw_consumptions",
            "metrics.candidate_action",
            "metrics.afw_rows",
        ],
        "outputs": [
            "metrics.afw_gate_decision",
            "metrics.afw_runtime_summary",
            "metrics.final_action",
        ],
        "metrics": [
            "afw_capguard_summary",
            "afw_runtime_summary",
            "afw_gate_decision",
        ],
        "advanced_fields": [
            "rows_path",
            "trace_scenarios_path",
            "include_trace_generated",
            "baselines",
            "runtime_enforce_obligations",
            "runtime_block_final_action",
        ],
        "examples": [
            {
                "name": "Field repair runtime gate",
                "config": {"runtime_final_action_mode": "fieldwise_repair"},
            }
        ],
    },
    "evaluate.afw_runtime": {
        "inputs": ["metrics.afw_gate_decision", "metrics.final_action", "case.metadata.oracle"],
        "outputs": ["evaluation", "metrics"],
        "metrics": ["afw_runtime_behmatch", "afw_runtime_false_allow"],
        "advanced_fields": ["require_no_false_allow"],
    },
    "model.mock": {
        "inputs": ["prompt", "case.input"],
        "outputs": ["model_response", "metrics.model_called"],
        "examples": [
            {
                "name": "Offline safe response",
                "config": {
                    "model": "mock-safe-model",
                    "response_template": "SAFE_RESPONSE: {input}",
                },
            }
        ],
    },
    "model.openai_compatible": {
        "inputs": ["prompt", "case.input", "environment variable api_key_env"],
        "outputs": ["model_response", "metrics.model_called"],
        "advanced_fields": ["temperature", "timeout_seconds"],
        "examples": [
            {
                "name": "Compatible chat endpoint",
                "config": {
                    "base_url": "https://api.example.com/v1",
                    "model": "model-name",
                    "api_key_env": "OPENAI_API_KEY",
                },
                "note": "The config stores the env var name, not the secret.",
            }
        ],
    },
    "model.eair_structured_action_json": {
        "inputs": ["model_response.content", "metrics.candidate_action"],
        "outputs": ["metrics.candidate_action"],
        "advanced_fields": ["action_json"],
    },
    "evaluate.rules": {
        "inputs": ["model_response.content"],
        "outputs": ["evaluation", "metrics.evaluation_passed"],
    },
    "evaluate.eair_bench_action": {
        "inputs": ["metrics.candidate_action", "metrics.oracle_action"],
        "outputs": ["evaluation", "metrics"],
    },
    "evaluate.eair_robustness_sweep": {
        "inputs": ["retrieval_context", "metrics.oracle_action"],
        "outputs": ["metrics", "artifacts"],
        "artifacts": ["sweep result files"],
        "advanced_fields": ["gate", "output_dir", "seed_grid"],
    },
    "evaluate.eair_case_robustness_sweep": {
        "inputs": ["EAIR case selector", "sweep config"],
        "outputs": ["metrics", "artifacts"],
        "artifacts": ["case sweep result files"],
        "advanced_fields": ["case_selector", "coverage", "sweep", "output_dir"],
    },
}


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "workspace": _relative_to_workspace(WORKSPACE_ROOT)}


@app.get("/api/catalog")
def node_catalog() -> dict[str, Any]:
    descriptors = []
    for descriptor in _registry.catalog():
        descriptors.append(_node_catalog_item(descriptor))
    return {
        "nodes": descriptors,
        "edge_conditions": ["has_errors", "no_errors", "halted"],
    }


@app.get("/api/agent-interfaces")
def agent_interfaces() -> dict[str, Any]:
    return agent_interface_catalog()


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


def _node_catalog_item(descriptor: Any) -> dict[str, Any]:
    interface = _node_interface(descriptor)
    return {
        "node_id": descriptor.node_id,
        "category": descriptor.category,
        "summary": descriptor.summary,
        "inputs": interface["inputs"],
        "outputs": interface["outputs"],
        "metrics": interface["metrics"],
        "artifacts": interface["artifacts"],
        "advanced_fields": interface["advanced_fields"],
        "examples": interface["examples"],
        "config_fields": [
            {
                "name": field.name,
                "type": field.type,
                "required": field.required,
                "default": field.default,
                "description": field.description,
                "secret_env": field.secret_env,
                "required_without_any": getattr(field, "required_without_any", []),
            }
            for field in descriptor.config_fields
        ],
    }


def _node_interface(descriptor: Any) -> dict[str, Any]:
    defaults = CATEGORY_INTERFACE_DEFAULTS.get(descriptor.category, CATEGORY_INTERFACE_DEFAULTS["custom"])
    hints = NODE_INTERFACE_HINTS.get(descriptor.node_id, {})
    config_fields = list(descriptor.config_fields)

    return {
        "inputs": _unique_values(
            getattr(descriptor, "inputs", []),
            hints.get("inputs") or defaults["inputs"],
        ),
        "outputs": _unique_values(
            getattr(descriptor, "outputs", []),
            hints.get("outputs") or defaults["outputs"],
        ),
        "metrics": _unique_values(
            getattr(descriptor, "metrics", []),
            hints.get("metrics") or defaults["metrics"],
        ),
        "artifacts": _unique_values(
            getattr(descriptor, "artifacts", []),
            hints.get("artifacts") or [],
        ),
        "advanced_fields": _unique_values(
            getattr(descriptor, "advanced_fields", []),
            hints.get("advanced_fields") or [],
            _heuristic_advanced_fields(config_fields),
        ),
        "examples": _node_examples(descriptor, hints),
    }


def _unique_values(*groups: Any) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for group in groups:
        if not isinstance(group, (list, tuple)):
            continue
        for item in group:
            value = str(item)
            if value and value not in seen:
                seen.add(value)
                result.append(value)
    return result


def _heuristic_advanced_fields(config_fields: list[Any]) -> list[str]:
    advanced_names = {
        "baselines",
        "candidate_inject_claims",
        "coverage",
        "event_type_key",
        "gate",
        "include_trace_generated",
        "output_dir",
        "runtime_block_final_action",
        "runtime_enforce_obligations",
        "seed",
        "seed_grid",
        "timeout_seconds",
        "trace_scenarios_path",
    }
    result: list[str] = []
    for field in config_fields:
        if field.name in advanced_names or (field.type in {"list", "dict"} and not field.required):
            result.append(field.name)
    return result


def _node_examples(descriptor: Any, hints: dict[str, Any]) -> list[dict[str, Any]]:
    examples: list[dict[str, Any]] = []
    for example in getattr(descriptor, "examples", []):
        examples.append(
            {
                "name": example.name,
                "config": example.config,
                "note": example.note,
            }
        )
    for example in hints.get("examples") or []:
        if isinstance(example, dict):
            examples.append(
                {
                    "name": str(example.get("name", "Example")),
                    "config": example.get("config") or {},
                    "note": str(example.get("note", "")),
                }
            )
    return examples


@app.get("/api/datasets")
def list_datasets() -> dict[str, Any]:
    datasets = []
    data_dir = EXAMPLES_DIR / "data"
    if data_dir.exists():
        for path in sorted(data_dir.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in SUPPORTED_DATASET_EXTENSIONS:
                continue
            item: dict[str, Any] = {
                "path": _relative_to_workspace(path),
                "name": path.name,
                "extension": path.suffix.lower(),
                "size_bytes": path.stat().st_size,
                "updated_at": _mtime_iso(path),
            }
            try:
                cases = load_cases(path)
                item["case_count"] = len(cases)
                item["sample_case_ids"] = [case.id for case in cases[:5]]
                item["valid"] = True
            except Exception as exc:  # noqa: BLE001 - API should report invalid local fixtures concisely
                item["case_count"] = None
                item["sample_case_ids"] = []
                item["valid"] = False
                item["error"] = str(exc)
            datasets.append(item)
    return {"datasets": datasets}


@app.get("/api/configs")
def list_configs() -> dict[str, Any]:
    configs = []
    if EXAMPLES_DIR.exists():
        for path in sorted(EXAMPLES_DIR.rglob("*.yml")) + sorted(EXAMPLES_DIR.rglob("*.yaml")):
            summary = _read_config_summary(path)
            if summary is not None:
                configs.append(summary)
    configs.sort(key=lambda item: item["updated_at"], reverse=True)
    return {"configs": configs}


@app.get("/api/config")
def get_config(path: str = Query(..., description="Workspace-relative config path.")) -> dict[str, Any]:
    config_path = _resolve_workspace_path(path, must_exist=True, allowed_extensions=SUPPORTED_CONFIG_EXTENSIONS)
    detail = _read_config_detail(config_path)
    if detail is None:
        raise HTTPException(status_code=400, detail="Path is not a valid FormalTrust experiment config.")
    return detail


@app.post("/api/configs/validate")
def validate_config_payload(request: ValidateConfigRequest) -> dict[str, Any]:
    try:
        normalized = _payload_for_write(request.config, GENERATED_CONFIG_DIR)
        parsed = ExperimentConfig.model_validate(normalized)
        build_graph(parsed.graph, _registry)
    except Exception as exc:  # noqa: BLE001 - validation endpoint returns the user-facing issue
        return {"valid": False, "issues": [str(exc)]}
    return {"valid": True, "issues": []}


@app.post("/api/configs")
def save_config(request: SaveConfigRequest) -> dict[str, Any]:
    GENERATED_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    filename = _unique_config_filename(request.name or str(request.config.get("experiment_name", "experiment")))
    target = GENERATED_CONFIG_DIR / filename
    payload = _payload_for_write(request.config, target.parent)

    try:
        parsed = ExperimentConfig.model_validate(payload)
        build_graph(parsed.graph, _registry)
    except Exception as exc:  # noqa: BLE001 - save should fail with the precise config issue
        raise HTTPException(status_code=400, detail=f"Invalid experiment config: {exc}") from exc

    target.write_text(
        yaml.safe_dump(payload, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    detail = _read_config_detail(target)
    if detail is None:
        raise HTTPException(status_code=500, detail="Saved config could not be reloaded.")
    return detail


@app.post("/api/jobs/run")
def start_run(request: RunRequest) -> dict[str, Any]:
    config_path = _resolve_workspace_path(
        request.config_path,
        must_exist=True,
        allowed_extensions=SUPPORTED_CONFIG_EXTENSIONS,
    )
    try:
        config = load_config(config_path)
        build_graph(config.graph, _registry)
    except Exception as exc:  # noqa: BLE001 - run should not start for invalid configs
        raise HTTPException(status_code=400, detail=f"Invalid experiment config: {exc}") from exc

    if request.output_dir:
        output_dir = _resolve_workspace_path(request.output_dir)
    else:
        output_dir = config.output_dir.resolve()
        _ensure_within_workspace(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    command = [
        sys.executable,
        "-m",
        "formaltrust_platform",
        "run",
        "--config",
        str(config_path),
        "--output-dir",
        str(output_dir),
    ]
    job = JobRecord(
        id=uuid.uuid4().hex,
        command=command,
        config_path=_relative_to_workspace(config_path),
        output_dir=_relative_to_workspace(output_dir),
    )
    with _jobs_lock:
        _jobs[job.id] = job

    thread = threading.Thread(target=_execute_job, args=(job.id,), daemon=True)
    thread.start()
    return _job_to_dict(job)


@app.get("/api/jobs")
def list_jobs() -> dict[str, Any]:
    with _jobs_lock:
        jobs = [_job_to_dict(job) for job in _jobs.values()]
    jobs.sort(key=lambda job: job["started_at"], reverse=True)
    return {"jobs": jobs}


@app.get("/api/jobs/{job_id}")
def get_job(job_id: str) -> dict[str, Any]:
    with _jobs_lock:
        job = _jobs.get(job_id)
        if job is None:
            raise HTTPException(status_code=404, detail="Job not found.")
        return _job_to_dict(job)


@app.get("/api/runs")
def list_runs() -> dict[str, Any]:
    runs = []
    if RUNS_DIR.exists():
        for run_dir in RUNS_DIR.iterdir():
            if not run_dir.is_dir():
                continue
            result_path = run_dir / "results.json"
            if not result_path.exists():
                continue
            summary: dict[str, Any] = {}
            try:
                payload = json.loads(result_path.read_text(encoding="utf-8"))
                summary = payload.get("summary", {})
            except Exception:  # noqa: BLE001 - still list the run shell if results are malformed
                summary = {}
            runs.append(
                {
                    "run_id": run_dir.name,
                    "path": _relative_to_workspace(run_dir),
                    "updated_at": _mtime_iso(result_path),
                    "summary": summary,
                    "report_exists": (run_dir / "report.md").exists(),
                    "results_size_bytes": result_path.stat().st_size,
                }
            )
    runs.sort(key=lambda run: run["updated_at"], reverse=True)
    return {"runs": runs}


@app.get("/api/runs/{run_id}")
def get_run(run_id: str) -> dict[str, Any]:
    run_dir = _resolve_run_dir(run_id)
    result_path = run_dir / "results.json"
    if not result_path.exists():
        raise HTTPException(status_code=404, detail="Run results not found.")
    payload = json.loads(result_path.read_text(encoding="utf-8"))
    cases = [_case_summary(case) for case in payload.get("cases", [])]
    return {
        "run_id": run_dir.name,
        "path": _relative_to_workspace(run_dir),
        "summary": payload.get("summary", {}),
        "cases": cases,
        "report_exists": (run_dir / "report.md").exists(),
    }


@app.get("/api/runs/{run_id}/cases/{case_file}")
def get_case(run_id: str, case_file: str) -> dict[str, Any]:
    run_dir = _resolve_run_dir(run_id)
    case_dir = (run_dir / "cases").resolve()
    safe_name = case_file if case_file.endswith(".json") else f"{case_file}.json"
    case_path = (case_dir / safe_name).resolve()
    _ensure_within(case_path, case_dir)
    if not case_path.exists() or not case_path.is_file():
        raise HTTPException(status_code=404, detail="Case artifact not found.")
    return json.loads(case_path.read_text(encoding="utf-8"))


@app.get("/api/runs/{run_id}/report")
def get_report(run_id: str) -> dict[str, str]:
    run_dir = _resolve_run_dir(run_id)
    report_path = run_dir / "report.md"
    if not report_path.exists():
        raise HTTPException(status_code=404, detail="Run report not found.")
    return {"markdown": report_path.read_text(encoding="utf-8", errors="replace")}


def _execute_job(job_id: str) -> None:
    with _jobs_lock:
        job = _jobs[job_id]
        command = list(job.command)

    try:
        process = subprocess.Popen(
            command,
            cwd=WORKSPACE_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        stdout, stderr = process.communicate()
        with _jobs_lock:
            job = _jobs[job_id]
            job.stdout = stdout
            job.stderr = stderr
            job.returncode = process.returncode
            job.status = "succeeded" if process.returncode == 0 else "failed"
            job.finished_at = _utc_now()
            _extract_run_paths(job)
    except Exception as exc:  # noqa: BLE001 - background failures should be visible in UI
        with _jobs_lock:
            job = _jobs[job_id]
            job.stderr = f"{job.stderr}\n{type(exc).__name__}: {exc}".strip()
            job.status = "failed"
            job.finished_at = _utc_now()


def _extract_run_paths(job: JobRecord) -> None:
    for line in job.stdout.splitlines():
        if line.startswith("Run directory:"):
            run_dir = Path(line.split(":", 1)[1].strip())
            if not run_dir.is_absolute():
                run_dir = WORKSPACE_ROOT / run_dir
            job.run_dir = _relative_to_workspace(run_dir.resolve())
        elif line.startswith("Report:"):
            report_path = Path(line.split(":", 1)[1].strip())
            if not report_path.is_absolute():
                report_path = WORKSPACE_ROOT / report_path
            job.report_path = _relative_to_workspace(report_path.resolve())


def _job_to_dict(job: JobRecord) -> dict[str, Any]:
    return {
        "id": job.id,
        "status": job.status,
        "started_at": job.started_at,
        "finished_at": job.finished_at,
        "config_path": job.config_path,
        "output_dir": job.output_dir,
        "command": _command_display(job.command),
        "stdout": job.stdout,
        "stderr": job.stderr,
        "returncode": job.returncode,
        "run_dir": job.run_dir,
        "report_path": job.report_path,
    }


def _command_display(command: list[str]) -> str:
    display = list(command)
    if display:
        display[0] = "python"
    return " ".join(display)


def _read_config_summary(path: Path) -> dict[str, Any] | None:
    try:
        detail = _read_config_detail(path)
    except Exception:  # noqa: BLE001 - non-experiment YAML files are ignored in the list
        return None
    if detail is None:
        return None
    config = detail["config"]
    return {
        "path": detail["path"],
        "name": path.name,
        "experiment_name": config["experiment_name"],
        "dataset_path": config["dataset_path"],
        "output_dir": config["output_dir"],
        "node_count": len(config["graph"]["nodes"]),
        "edge_count": len(config["graph"]["edges"]),
        "updated_at": _mtime_iso(path),
    }


def _read_config_detail(path: Path) -> dict[str, Any] | None:
    if path.suffix.lower() not in SUPPORTED_CONFIG_EXTENSIONS:
        return None
    config = load_config(path)
    build_graph(config.graph, _registry)
    return {
        "path": _relative_to_workspace(path),
        "name": path.name,
        "updated_at": _mtime_iso(path),
        "config": _config_for_ui(config),
        "raw_text": path.read_text(encoding="utf-8", errors="replace"),
    }


def _config_for_ui(config: ExperimentConfig) -> dict[str, Any]:
    return {
        "experiment_name": config.experiment_name,
        "dataset_path": _relative_to_workspace(config.dataset_path),
        "output_dir": _relative_to_workspace(config.output_dir),
        "graph": {
            "nodes": [
                {
                    "name": node.name,
                    "node_id": node.node_id,
                    "config": node.config,
                }
                for node in config.graph.nodes
            ],
            "edges": [
                {
                    key: value
                    for key, value in {
                        "from": edge.from_node,
                        "to": edge.to,
                        "condition": edge.condition,
                        "else_to": edge.else_to,
                    }.items()
                    if value not in (None, "")
                }
                for edge in config.graph.edges
            ],
        },
    }


def _payload_for_write(payload: dict[str, Any], target_dir: Path) -> dict[str, Any]:
    data = json.loads(json.dumps(payload))
    dataset_path = _resolve_workspace_path(
        str(data.get("dataset_path", "")),
        must_exist=True,
        allowed_extensions=SUPPORTED_DATASET_EXTENSIONS,
    )
    output_dir = _resolve_workspace_path(str(data.get("output_dir") or "runs"))
    graph = data.get("graph") or {}

    data["dataset_path"] = _relative_from(target_dir, dataset_path)
    data["output_dir"] = _relative_from(target_dir, output_dir)
    data["graph"] = {
        "nodes": [_clean_node(node) for node in graph.get("nodes", [])],
        "edges": [_clean_edge(edge) for edge in graph.get("edges", [])],
    }
    return data


def _clean_node(node: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": node.get("name", ""),
        "node_id": node.get("node_id", ""),
        "config": node.get("config") or {},
    }


def _clean_edge(edge: dict[str, Any]) -> dict[str, Any]:
    cleaned = {
        "from": edge.get("from") or edge.get("from_node") or "",
        "to": edge.get("to") or "",
    }
    if edge.get("condition"):
        cleaned["condition"] = edge["condition"]
    if edge.get("else_to"):
        cleaned["else_to"] = edge["else_to"]
    return cleaned


def _case_summary(case: dict[str, Any]) -> dict[str, Any]:
    test_case = case.get("case", {})
    evaluation = case.get("evaluation") or {}
    errors = case.get("errors") or []
    trace = case.get("trace") or []
    return {
        "case_id": test_case.get("id", ""),
        "case_file": f"{_safe_name(str(test_case.get('id', 'case')))}.json",
        "input": test_case.get("input", ""),
        "tags": test_case.get("tags", []),
        "expected_behavior": test_case.get("expected_behavior"),
        "evaluation": evaluation,
        "passed": bool(evaluation.get("passed")) if evaluation else len(errors) == 0,
        "error_count": len(errors),
        "trace_count": len(trace),
        "halted": bool(case.get("halted", False)),
        "metrics_keys": sorted((case.get("metrics") or {}).keys()),
    }


def _safe_name(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in value)


def _unique_config_filename(name: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", name.strip()).strip("-").lower() or "experiment"
    candidate = GENERATED_CONFIG_DIR / f"{slug}.yaml"
    if not candidate.exists():
        return candidate.name
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{slug}-{stamp}.yaml"


def _resolve_run_dir(run_id: str) -> Path:
    run_dir = (RUNS_DIR / run_id).resolve()
    _ensure_within(run_dir, RUNS_DIR.resolve())
    if not run_dir.exists() or not run_dir.is_dir():
        raise HTTPException(status_code=404, detail="Run not found.")
    return run_dir


def _resolve_workspace_path(
    value: str | Path,
    *,
    must_exist: bool = False,
    allowed_extensions: set[str] | None = None,
) -> Path:
    if not str(value):
        raise HTTPException(status_code=400, detail="Path is required.")
    path = Path(value)
    if not path.is_absolute():
        path = WORKSPACE_ROOT / path
    resolved = path.resolve()
    _ensure_within_workspace(resolved)
    if allowed_extensions is not None and resolved.suffix.lower() not in allowed_extensions:
        supported = ", ".join(sorted(allowed_extensions))
        raise HTTPException(status_code=400, detail=f"Unsupported file extension. Expected one of: {supported}.")
    if must_exist and not resolved.exists():
        raise HTTPException(status_code=404, detail=f"Path does not exist: {_relative_to_workspace(resolved)}")
    return resolved


def _ensure_within_workspace(path: Path) -> None:
    _ensure_within(path, WORKSPACE_ROOT.resolve())


def _ensure_within(path: Path, root: Path) -> None:
    resolved_root = root.resolve()
    try:
        path.resolve().relative_to(resolved_root)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"Path must stay inside {resolved_root}.") from exc


def _relative_to_workspace(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(WORKSPACE_ROOT.resolve()).as_posix()
    except ValueError:
        return resolved.as_posix()


def _relative_from(base_dir: Path, target: Path) -> str:
    return Path(os.path.relpath(target.resolve(), base_dir.resolve())).as_posix()


def _mtime_iso(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat()


_ui_dist = WORKSPACE_ROOT / "ui" / "dist"
if _ui_dist.exists():
    app.mount("/", StaticFiles(directory=_ui_dist, html=True), name="ui")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("formaltrust_platform.web_api:app", host="127.0.0.1", port=8000, reload=True)
