from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Mapping, Sequence


SECTION_PLAN = [
    {
        "section": "§0 Abstract",
        "goal": "State the action-invariance problem, the fieldwise authority method, and the strongest bounded result.",
        "evidence_role": "Summarize L1-L4 evidence without promoting it to production evidence.",
    },
    {
        "section": "§1 Introduction",
        "goal": "Motivate conservative collapse under strict supervision in power-operation agents.",
        "evidence_role": "Use safe claims and forbidden-claim boundary from the claim ledger.",
    },
    {
        "section": "§2 Related Work and Novelty Boundary",
        "goal": "Position against attribution-only, access-control-only, RAG faithfulness, and generic agent guardrails.",
        "evidence_role": "Use the claim ledger to avoid firstness or official-baseline superiority claims.",
    },
    {
        "section": "§3 Formal Model and CapGuard",
        "goal": "Define Cap(x), Need(s,f), field coverage, minimal authority witnesses, and repair-frame invariance.",
        "evidence_role": "Map implementation claims to FormalTrust nodes and tests.",
    },
    {
        "section": "§4 Test Framework and Power-Ops Benchmark Slice",
        "goal": "Describe curated, expanded, metamorphic, skill-driven, trace, and bridge fixtures.",
        "evidence_role": "Bind each fixture to dataset/YAML/report artifacts.",
    },
    {
        "section": "§5 Results and Analysis",
        "goal": "Report field preservation, unsafe-field removal, over-conservatism, performance profile, and trace-import behavior.",
        "evidence_role": "Use result JSON files as the source for every numeric claim.",
    },
    {
        "section": "§6 Limitations and Next Experiments",
        "goal": "State missing production trace, wall-clock latency, operator workload, and official benchmark gaps.",
        "evidence_role": "Keep future work separated from supported claims.",
    },
]


FIGURE_PLAN = [
    {
        "id": "Fig. 1",
        "type": "Architecture",
        "description": "Cap/Need/CapGuard field-level authorization path for power-operation agent actions.",
        "data_source": "figures/power_ops_action_invariance_architecture.svg",
        "priority": "HIGH",
    },
    {
        "id": "Fig. 2",
        "type": "Repair frame",
        "description": "Action-invariance repair: preserve authorized fields and remove unauthorized fields.",
        "data_source": "figures/power_ops_action_invariance_repair_frame.svg",
        "priority": "HIGH",
    },
    {
        "id": "Fig. 3",
        "type": "Evidence ladder",
        "description": "Claim boundary ladder from implementation to production evidence.",
        "data_source": "figures/power_ops_action_invariance_result_ladder.svg",
        "priority": "MEDIUM",
    },
    {
        "id": "Table 1",
        "type": "Main result table",
        "description": "Curated, expanded, metamorphic, skill, trace, and trace-import results.",
        "data_source": "docs/power_ops_action_invariance_figure_table_package_2026-07-02.md",
        "priority": "HIGH",
    },
    {
        "id": "Table 2",
        "type": "Over-conservatism profile",
        "description": "Normal behavior preservation versus unsafe-field removal and whole-action blocking.",
        "data_source": "docs/power_ops_action_invariance_performance_2026-07-02.json",
        "priority": "HIGH",
    },
]


def build_paper_artifact_map(
    *,
    claim_ledger_path: str | Path,
    result_paths: Sequence[str | Path] = (),
    venue: str = "ICLR",
) -> dict[str, Any]:
    claim_ledger = _load_json(claim_ledger_path)
    claims = _list_value(claim_ledger.get("supported_claims"))
    rows = [_claim_matrix_row(claim) for claim in claims if isinstance(claim, Mapping)]
    level_counts = Counter(str(row["level"]) for row in rows)
    result_artifacts = [_result_artifact_digest(path) for path in result_paths]

    return {
        "artifact_type": "power_ops_paper_artifact_map",
        "title": "Field-Level Action Invariance for Power-Operation LLM Agents",
        "venue": venue,
        "paper_type": "method + empirical artifact",
        "date": "2026-07-02",
        "one_sentence_contribution": (
            "Strict supervision for high-risk power-operation agents should preserve "
            "authorized action fields while removing only fields whose authority needs "
            "are not covered by source-derived capabilities."
        ),
        "section_plan": SECTION_PLAN,
        "claims_evidence_matrix": rows,
        "evidence_level_counts": dict(sorted(level_counts.items())),
        "figure_plan": FIGURE_PLAN,
        "result_artifacts": result_artifacts,
        "claim_ledger_path": str(claim_ledger_path),
        "forbidden_claims": _list_value(claim_ledger.get("forbidden_claims")),
        "next_steps": [
            "Draft LaTeX sections from this outline.",
            "Add real or semi-real multi-step trace import before any production-trace claim.",
            "Measure wall-clock latency; current latency remains a field-check proxy.",
            "Run official external benchmarks before any superiority claim.",
        ],
    }


def render_paper_outline_markdown(artifact_map: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Action Invariance Paper Outline",
        "",
        f"**Title:** {artifact_map['title']}",
        f"**Venue:** {artifact_map['venue']}",
        f"**Type:** {artifact_map['paper_type']}",
        f"**Date:** {artifact_map['date']}",
        "",
        f"**One-sentence contribution:** {artifact_map['one_sentence_contribution']}",
        "",
        "## Claims-Evidence Matrix",
        "",
        "| Claim | Level | Section | Evidence | Safe use |",
        "|---|---|---|---|---|",
    ]
    for row in artifact_map.get("claims_evidence_matrix", []):
        if not isinstance(row, Mapping):
            continue
        evidence = "<br>".join(f"`{item}`" for item in _list_value(row.get("evidence")))
        lines.append(
            "| {claim} | {level} | {section} | {evidence} | {safe_use} |".format(
                claim=str(row.get("claim", "")),
                level=str(row.get("level", "")),
                section=str(row.get("section", "")),
                evidence=evidence,
                safe_use=str(row.get("safe_use", "")),
            )
        )

    lines.extend(
        [
            "",
            "## Section Plan",
            "",
            "| Section | Goal | Evidence role |",
            "|---|---|---|",
        ]
    )
    for section in artifact_map.get("section_plan", []):
        if isinstance(section, Mapping):
            lines.append(
                "| {section} | {goal} | {role} |".format(
                    section=section.get("section", ""),
                    goal=section.get("goal", ""),
                    role=section.get("evidence_role", ""),
                )
            )

    lines.extend(
        [
            "",
            "## Figure And Table Plan",
            "",
            "| ID | Type | Description | Data source | Priority |",
            "|---|---|---|---|---|",
        ]
    )
    for item in artifact_map.get("figure_plan", []):
        if isinstance(item, Mapping):
            lines.append(
                "| {id} | {type} | {description} | `{data_source}` | {priority} |".format(
                    id=item.get("id", ""),
                    type=item.get("type", ""),
                    description=item.get("description", ""),
                    data_source=item.get("data_source", ""),
                    priority=item.get("priority", ""),
                )
            )

    lines.extend(
        [
            "",
            "## Result Artifacts",
            "",
            "| Artifact | Path | Key readback |",
            "|---|---|---|",
        ]
    )
    for artifact in artifact_map.get("result_artifacts", []):
        if isinstance(artifact, Mapping):
            lines.append(
                "| {artifact_type} | `{path}` | {readback} |".format(
                    artifact_type=artifact.get("artifact_type", ""),
                    path=artifact.get("path", ""),
                    readback=artifact.get("key_readback", ""),
                )
            )

    lines.extend(
        [
            "",
            "## Forbidden Claims",
            "",
        ]
    )
    for claim in artifact_map.get("forbidden_claims", []):
        lines.append(f"- {claim}")

    lines.extend(
        [
            "",
            "## Next Steps",
            "",
        ]
    )
    for step in artifact_map.get("next_steps", []):
        lines.append(f"- {step}")
    lines.append("")
    return "\n".join(lines)


def write_paper_outline(
    artifact_map: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_paper_outline_markdown(artifact_map), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(artifact_map, ensure_ascii=False, indent=2), encoding="utf-8")


def _claim_matrix_row(claim: Mapping[str, Any]) -> dict[str, Any]:
    claim_text = str(claim.get("claim", ""))
    return {
        "claim": claim_text,
        "level": str(claim.get("level", "")),
        "section": _section_for_claim(claim_text),
        "evidence": _list_value(claim.get("evidence")),
        "safe_use": _safe_use_for_claim(claim_text),
    }


def _section_for_claim(claim: str) -> str:
    lowered = claim.lower()
    if "fieldwise repair final-action" in lowered or "fieldwise repair final action" in lowered:
        return "§3 Formal Model and CapGuard"
    if "trace import" in lowered:
        return "§5 Results and Analysis"
    if any(
        token in lowered
        for token in (
            "curated",
            "expanded",
            "metamorphic",
            "skill",
            "performance",
            "baseline",
            "trace/span",
            "otlp",
        )
    ):
        return "§5 Results and Analysis"
    if "agentdojo" in lowered or "semi-real" in lowered:
        return "§6 Limitations and Next Experiments"
    return "§1 Introduction"


def _safe_use_for_claim(claim: str) -> str:
    lowered = claim.lower()
    if "trace import" in lowered:
        return "Use as L3 trace-fixture evidence, not production telemetry."
    if "performance" in lowered:
        return "Use as normal-behavior preservation profile; latency is only a proxy."
    if "baseline" in lowered:
        return "Use as ablation evidence on curated cases only."
    if "agentdojo" in lowered or "semi-real" in lowered:
        return "Use as bridge evidence, not official benchmark superiority."
    return "Use with the stated evidence level."


def _result_artifact_digest(path: str | Path) -> dict[str, Any]:
    target = Path(path)
    payload = _load_json(target)
    artifact_type = str(payload.get("artifact_type", "unknown_artifact"))
    return {
        "path": str(target),
        "artifact_type": artifact_type,
        "suite_id": payload.get("suite_id"),
        "total_cases": payload.get("total_cases"),
        "key_readback": _key_readback(payload),
    }


def _key_readback(payload: Mapping[str, Any]) -> str:
    artifact_type = payload.get("artifact_type")
    if artifact_type == "power_ops_trace_import_summary":
        action = _mapping_value(payload.get("action_invariance_summary"))
        boundary_counts = _mapping_value(payload.get("boundary_counts"))
        coverage = _mapping_value(payload.get("multi_step_source_type_coverage"))
        readback = (
            "boundary_count={boundary_count}; boundary_case_total={boundary_total}; "
            "whole_action_block_rate={block:.3f}; authorized_preservation={preserve:.3f}; "
            "unsafe_removal={remove:.3f}"
        ).format(
            boundary_count=len(boundary_counts),
            boundary_total=sum(_int_value(count) for count in boundary_counts.values()),
            block=_float_value(action.get("whole_action_block_rate", 0.0)),
            preserve=_float_value(action.get("authorized_final_field_preservation_rate", 0.0)),
            remove=_float_value(action.get("unauthorized_final_field_removal_rate", 0.0)),
        )
        if coverage:
            readback += "; source_type_coverage={coverage:.3f}".format(
                coverage=_float_value(coverage.get("coverage_rate", 0.0))
            )
        return readback
    if artifact_type == "power_ops_planner_skill_tool_memory_summary":
        coverage = _mapping_value(payload.get("source_chain_coverage"))
        return (
            "cases={cases}; source_chain_coverage={coverage:.3f}; "
            "authorized_preservation={preserve:.3f}; unsafe_removal={remove:.3f}; "
            "whole_action_block_rate={block:.3f}"
        ).format(
            cases=_int_value(payload.get("total_cases")),
            coverage=_float_value(coverage.get("coverage_rate", 0.0)),
            preserve=_float_value(payload.get("authorized_final_field_preservation_rate", 0.0)),
            remove=_float_value(payload.get("unauthorized_final_field_removal_rate", 0.0)),
            block=_float_value(payload.get("whole_action_block_rate", 0.0)),
        )
    if artifact_type == "power_ops_action_invariance_performance_profile":
        best = _mapping_value(payload.get("best_baseline_for_normal_behavior"))
        return (
            "suite_count={suite_count}; baseline_count={baseline_count}; best_baseline={best}"
        ).format(
            suite_count=int(payload.get("suite_count", 0)),
            baseline_count=int(payload.get("baseline_count", 0)),
            best=best.get("name", "missing"),
        )
    return "artifact_type={artifact_type}".format(artifact_type=artifact_type)


def _load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object at {path}")
    return payload


def _mapping_value(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    return {}


def _int_value(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _float_value(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


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
        description="Build a paper outline and artifact map for the power-ops action-invariance direction."
    )
    parser.add_argument(
        "--claim-ledger",
        default="docs/power_ops_action_invariance_claim_ledger_2026-07-02.json",
    )
    parser.add_argument("--result", action="append", default=[])
    parser.add_argument("--venue", default="ICLR")
    parser.add_argument("--out-md", default="docs/power_ops_action_invariance_paper_outline_2026-07-02.md")
    parser.add_argument("--out-json", default="docs/power_ops_action_invariance_paper_outline_2026-07-02.json")
    args = parser.parse_args(argv)

    artifact_map = build_paper_artifact_map(
        claim_ledger_path=args.claim_ledger,
        result_paths=args.result,
        venue=args.venue,
    )
    write_paper_outline(artifact_map, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
