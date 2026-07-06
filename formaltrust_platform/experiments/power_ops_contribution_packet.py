from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping


DEFAULT_OUT_MD = "docs/power_ops_action_invariance_contribution_packet_2026-07-02.md"
DEFAULT_OUT_JSON = "docs/power_ops_action_invariance_contribution_packet_2026-07-02.json"

FORBIDDEN_HEADLINE_TOKENS = (
    "first",
    "only",
    "officially better",
    "production-proven",
    "solves prompt injection",
)


def build_contribution_packet() -> dict[str, Any]:
    claims = [
        {
            "claim_id": "C1_field_level_authority_witness",
            "short_claim": "The method checks authority at the action-field level and records the minimal capability evidence behind preserved fields.",
            "why_it_matters": "This narrows runtime supervision from whole-action refusal to auditable field-level authority coverage.",
            "formal_refs": [
                "docs/power_ops_action_invariance_formal_model_2026-07-02.md",
                "docs/power_ops_action_invariance_claim_to_paragraph_map_2026-07-02.md",
            ],
            "code_paths": [
                "formaltrust_platform/experiments/power_ops_action_invariance.py",
                "formaltrust_platform/nodes/afw.py",
            ],
            "evidence_paths": [
                "docs/power_ops_action_invariance_results_2026-07-02.json",
                "docs/power_ops_action_invariance_claim_to_paragraph_map_2026-07-02.json",
                "docs/power_ops_action_invariance_paragraph_evidence_packets_2026-07-02.json",
            ],
            "boundary_tags": [
                "not_generic_agent_guardrail_firstness",
                "not_production_telemetry",
            ],
        },
        {
            "claim_id": "C2_fieldwise_action_invariance",
            "short_claim": "Under strict intervention, fieldwise repair preserves authorized final-action fields while removing unauthorized fields.",
            "why_it_matters": "This directly targets over-conservatism: safe fields remain executable instead of being lost in whole-action blocking.",
            "formal_refs": [
                "docs/power_ops_action_invariance_formal_model_2026-07-02.md",
                "docs/power_ops_action_invariance_repair_validity_2026-07-02.md",
            ],
            "code_paths": [
                "formaltrust_platform/experiments/power_ops_action_invariance.py",
                "formaltrust_platform/experiments/power_ops_action_invariance_baselines.py",
            ],
            "evidence_paths": [
                "docs/power_ops_action_invariance_fieldwise_repair_results_2026-07-02.json",
                "docs/power_ops_action_invariance_baseline_grid_2026-07-02.json",
                "docs/power_ops_action_invariance_table_evidence_binding_2026-07-02.json",
            ],
            "boundary_tags": [
                "fixture_level_result",
                "not_operator_workload_reduction",
                "not_wall_clock_latency",
            ],
        },
        {
            "claim_id": "C3_non_rag_authority_sources",
            "short_claim": "The authority abstraction can consume skill manifests, tool metadata, memory, prior-step outputs, and approvals, not only RAG documents.",
            "why_it_matters": "This lets the same action-invariance check apply to skill-driven agents where retrieval is absent or secondary.",
            "formal_refs": [
                "docs/power_ops_skill_authority_model_2026-07-02.md",
                "docs/power_ops_trace_import_contract_2026-07-02.md",
            ],
            "code_paths": [
                "formaltrust_platform/experiments/power_ops_trace_import.py",
                "formaltrust_platform/experiments/power_ops_planner_skill_tool_memory.py",
                "formaltrust_platform/experiments/power_ops_action_invariance.py",
            ],
            "evidence_paths": [
                "docs/power_ops_skill_authority_results_2026-07-02.json",
                "docs/power_ops_skill_authority_dataset_audit_2026-07-02.json",
                "docs/power_ops_trace_import_results_2026-07-02.json",
                "docs/power_ops_multistep_trace_import_results_2026-07-02.json",
                "docs/power_ops_planner_skill_tool_memory_results_2026-07-02.json",
            ],
            "boundary_tags": [
                "not_rag_only",
                "not_deployment_claim",
                "not_official_benchmark_superiority",
            ],
        },
    ]
    safe_headline = (
        "Field-level action invariance for power-operation agents: preserve authorized fields, "
        "remove unsupported fields, and keep every paper claim evidence-bound."
    )
    forbidden_hits = _forbidden_hits(safe_headline)
    return {
        "artifact_type": "power_ops_contribution_packet",
        "packet_status": "ready" if not forbidden_hits else "blocked_forbidden_headline",
        "safe_headline": safe_headline,
        "claim_count": len(claims),
        "forbidden_headline_count": len(forbidden_hits),
        "forbidden_headline_hits": forbidden_hits,
        "all_claims_have_code_evidence": all(bool(claim["code_paths"]) for claim in claims),
        "all_claims_have_result_evidence": all(bool(claim["evidence_paths"]) for claim in claims),
        "all_claims_have_boundary": all(bool(claim["boundary_tags"]) for claim in claims),
        "claims": claims,
    }


def render_contribution_packet_markdown(packet: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Contribution Packet",
        "",
        f"**Status:** {packet.get('packet_status', '')}",
        "",
        f"**Safe headline:** {packet.get('safe_headline', '')}",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Claims | {int(packet.get('claim_count', 0) or 0)} |",
        f"| Forbidden headline hits | {int(packet.get('forbidden_headline_count', 0) or 0)} |",
        f"| All claims have code evidence | {bool(packet.get('all_claims_have_code_evidence', False))} |",
        f"| All claims have result evidence | {bool(packet.get('all_claims_have_result_evidence', False))} |",
        f"| All claims have boundary | {bool(packet.get('all_claims_have_boundary', False))} |",
        "",
        "## Claims",
        "",
    ]
    for claim in _list_value(packet.get("claims")):
        if not isinstance(claim, Mapping):
            continue
        lines.extend(
            [
                f"### {claim.get('claim_id', '')}",
                "",
                str(claim.get("short_claim", "")),
                "",
                f"Why it matters: {claim.get('why_it_matters', '')}",
                "",
                "Evidence:",
            ]
        )
        for path in _list_value(claim.get("evidence_paths")):
            lines.append(f"- `{path}`")
        lines.append("")
        lines.append("Code:")
        for path in _list_value(claim.get("code_paths")):
            lines.append(f"- `{path}`")
        lines.append("")
        lines.append("Boundaries:")
        for tag in _list_value(claim.get("boundary_tags")):
            lines.append(f"- `{tag}`")
        lines.append("")
    return "\n".join(lines)


def write_contribution_packet(
    packet: Mapping[str, Any],
    *,
    markdown_path: str | Path = DEFAULT_OUT_MD,
    json_path: str | Path | None = DEFAULT_OUT_JSON,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_contribution_packet_markdown(packet), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.write_text(json.dumps(packet, ensure_ascii=False, indent=2), encoding="utf-8")


def _forbidden_hits(text: str) -> list[str]:
    lowered = text.lower()
    return [token for token in FORBIDDEN_HEADLINE_TOKENS if token in lowered]


def _list_value(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return list(value)
    if isinstance(value, tuple | set):
        return list(value)
    return [value]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate a reviewer-facing contribution packet for Power-Ops action invariance."
    )
    parser.add_argument("--out-md", default=DEFAULT_OUT_MD)
    parser.add_argument("--out-json", default=DEFAULT_OUT_JSON)
    args = parser.parse_args(argv)
    packet = build_contribution_packet()
    write_contribution_packet(packet, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
