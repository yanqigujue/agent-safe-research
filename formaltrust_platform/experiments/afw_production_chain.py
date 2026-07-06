from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence

import yaml


DEFAULT_MANIFEST_PATH = Path("examples/afw_power_ops_production_chain.yaml")
DEFAULT_MARKDOWN_PATH = Path("docs/power_ops_afw_production_chain_report_2026-07-01.md")
DEFAULT_JSON_PATH = Path("docs/power_ops_afw_production_chain_report_2026-07-01.json")

REQUIRED_MODEL_ROLES = ("embedding", "generation", "rerank")
EXPECTED_APIS = {
    "embedding": "embeddings",
    "generation": "chat_completions",
    "rerank": "rerank",
}


def build_afw_production_chain_report(manifest_path: str | Path = DEFAULT_MANIFEST_PATH) -> dict[str, Any]:
    """Validate a production-style multi-model RAG chain manifest for AFW."""

    manifest = _load_manifest(manifest_path)
    models = dict(manifest.get("models", {}))
    constraints = dict(manifest.get("constraints", {}))
    hardware = dict(manifest.get("hardware", {}))
    rag_flow = list(manifest.get("rag_flow", []))
    concurrency = dict(manifest.get("concurrency", {}))

    role_presence = {role: _has_role(models, role) for role in REQUIRED_MODEL_ROLES}
    api_compatibility = {
        role: str(models.get(role, {}).get("api", "missing")) for role in REQUIRED_MODEL_ROLES
    }
    api_compatibility_passes = all(api_compatibility[role] == EXPECTED_APIS[role] for role in REQUIRED_MODEL_ROLES)
    estimated_memory = sum(_as_float(model.get("estimated_memory_gb")) for model in models.values())
    max_memory = _as_float(constraints.get("max_total_model_memory_gb"))
    gpu_memory = _as_float(hardware.get("gpu_memory_gb"))
    memory_budget_passes = estimated_memory <= max_memory and estimated_memory <= gpu_memory
    rag_flow_contains_guardrail = "afw_capguard" in rag_flow if constraints.get("require_afw_guardrail", True) else True
    required_model_roles_covered = all(role_presence.values())
    ready = (
        required_model_roles_covered
        and rag_flow_contains_guardrail
        and memory_budget_passes
        and (api_compatibility_passes or not constraints.get("require_api_compatibility", True))
    )

    return {
        "artifact_type": "afw_production_chain_report",
        "inputs": {"manifest_path": str(Path(manifest_path))},
        "summary": {
            "scenario": str(manifest.get("scenario", "")),
            "model_roles_present": sorted(role for role, present in role_presence.items() if present),
            "required_model_roles_covered": required_model_roles_covered,
            "rag_flow_contains_guardrail": rag_flow_contains_guardrail,
            "estimated_model_memory_gb": round(estimated_memory, 3),
            "max_total_model_memory_gb": round(max_memory, 3),
            "gpu_memory_gb": round(gpu_memory, 3),
            "memory_budget_passes": memory_budget_passes,
            "api_compatibility_passes": api_compatibility_passes,
            "concurrency_target": int(concurrency.get("target_concurrent_operators", 0)),
            "production_readiness_status": (
                "manifest_validated_not_live_deployment" if ready else "manifest_needs_revision"
            ),
        },
        "checks": {
            "required_model_roles": role_presence,
            "api_compatibility": api_compatibility,
            "rag_flow": rag_flow,
            "memory": {
                "estimated_model_memory_gb": round(estimated_memory, 3),
                "max_total_model_memory_gb": round(max_memory, 3),
                "gpu_memory_gb": round(gpu_memory, 3),
                "passes": memory_budget_passes,
            },
        },
        "models": models,
        "constraints": constraints,
        "manifest": manifest,
    }


def render_afw_production_chain_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# AFW Production Chain Report",
        "",
        "This report validates a manifest for the implementation-plan style multi-model RAG chain. "
        "It is a deployment-readiness artifact, not evidence that live services were launched.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
    ]
    for key, value in report["summary"].items():
        lines.append(f"| {key} | {value} |")

    lines.extend(
        [
            "",
            "## Model Chain",
            "",
            "| Role | Model | API | Estimated memory GB | Input | Output |",
            "|---|---|---|---:|---|---|",
        ]
    )
    for role in REQUIRED_MODEL_ROLES:
        model = report["models"].get(role, {})
        lines.append(
            "| {role} | {model_id} | {api} | {memory} | {input} | {output} |".format(
                role=role,
                model_id=model.get("model_id", ""),
                api=model.get("api", ""),
                memory=model.get("estimated_memory_gb", ""),
                input=model.get("input", ""),
                output=model.get("output", ""),
            )
        )

    lines.extend(
        [
            "",
            "## Flow",
            "",
            " -> ".join(report["checks"]["rag_flow"]),
            "",
            "## Boundary",
            "",
            "Use this as evidence that the production-chain assumptions are explicit and machine-checkable. "
            "Do not claim live deployment, real GPU saturation, or real concurrent-user service behavior from this report alone.",
            "",
        ]
    )
    return "\n".join(lines)


def write_afw_production_chain_report(
    manifest_path: str | Path = DEFAULT_MANIFEST_PATH,
    *,
    markdown_path: str | Path = DEFAULT_MARKDOWN_PATH,
    json_path: str | Path = DEFAULT_JSON_PATH,
) -> dict[str, Any]:
    report = build_afw_production_chain_report(manifest_path)
    Path(markdown_path).write_text(render_afw_production_chain_markdown(report), encoding="utf-8")
    Path(json_path).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def _load_manifest(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}
    if not isinstance(payload, dict):
        raise ValueError("AFW production-chain manifest must be a mapping.")
    return payload


def _has_role(models: dict[str, Any], role: str) -> bool:
    model = models.get(role)
    return isinstance(model, dict) and model.get("role", role) == role


def _as_float(value: Any) -> float:
    if value is None:
        return 0.0
    return float(value)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write AFW production-chain manifest reports.")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST_PATH))
    parser.add_argument("--markdown", default=str(DEFAULT_MARKDOWN_PATH))
    parser.add_argument("--json", default=str(DEFAULT_JSON_PATH))
    args = parser.parse_args(argv)

    report = write_afw_production_chain_report(
        args.manifest,
        markdown_path=args.markdown,
        json_path=args.json,
    )
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
