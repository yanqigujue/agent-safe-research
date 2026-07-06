from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence

from formaltrust_platform.experiments.afw_bench import (
    evaluate_paired_rows,
    generate_authority_confusion_rows,
    load_paired_rows,
    load_trace_scenarios_as_rows,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
POWER_OPS_ROWS_PATH = REPO_ROOT / "examples" / "afw_power_ops_rag_rows.json"
POWER_OPS_TRACE_SCENARIOS_PATH = REPO_ROOT / "examples" / "afw_power_ops_trace_scenarios.json"


def build_power_ops_report(
    *,
    rows_path: str | Path = POWER_OPS_ROWS_PATH,
    trace_scenarios_path: str | Path = POWER_OPS_TRACE_SCENARIOS_PATH,
) -> dict[str, Any]:
    """Build a deterministic summary for the power-operations AFW slice."""

    rag_rows = load_paired_rows(rows_path)
    adapted_trace_rows = load_trace_scenarios_as_rows(trace_scenarios_path)
    generated_trace_rows = generate_authority_confusion_rows(trace_scenarios_path)
    generated_roles = sorted(
        {row["laundered_consumption"]["need"]["required_role"] for row in generated_trace_rows}
    )

    return {
        "inputs": {
            "rag_rows_path": str(Path(rows_path)),
            "trace_scenarios_path": str(Path(trace_scenarios_path)),
            "rag_rows": len(rag_rows),
            "rag_row_origins": _row_origin_counts(rag_rows),
            "rag_source_types": sorted({row["source"]["source_type"] for row in rag_rows}),
            "trace_scenarios": len(adapted_trace_rows),
            "generated_trace_rows": len(generated_trace_rows),
            "trace_source_types": sorted({row["source"]["source_type"] for row in adapted_trace_rows}),
            "generated_target_roles": generated_roles,
            "generated_target_role_count": len(generated_roles),
        },
        "rag_rows": {
            "capguard": _compact_summary(evaluate_paired_rows(rag_rows, baseline="capguard")),
            "permission_only": _compact_summary(
                evaluate_paired_rows(rag_rows, baseline="permission_only")
            ),
            "field_attribution_only": _compact_summary(
                evaluate_paired_rows(rag_rows, baseline="field_attribution_only")
            ),
        },
        "trace_rows": {
            "adapted_capguard": _compact_summary(
                evaluate_paired_rows(adapted_trace_rows, baseline="capguard")
            ),
            "generated_capguard": _compact_summary(
                evaluate_paired_rows(generated_trace_rows, baseline="capguard")
            ),
            "generated_boundary_scope_only": _compact_summary(
                evaluate_paired_rows(generated_trace_rows, baseline="boundary_scope_only")
            ),
            "generated_rows": [_generated_row_digest(row) for row in generated_trace_rows],
        },
    }


def build_power_ops_plausibility_audit_sheet(
    *,
    trace_scenarios_path: str | Path = POWER_OPS_TRACE_SCENARIOS_PATH,
) -> dict[str, Any]:
    generated_trace_rows = generate_authority_confusion_rows(trace_scenarios_path)
    entries = [_audit_entry(row) for row in generated_trace_rows]
    ready_count = sum(1 for entry in entries if entry["precheck_status"] == "ready_for_human_audit")
    return {
        "artifact_type": "power_ops_afw_plausibility_audit_sheet",
        "trace_scenarios_path": str(Path(trace_scenarios_path)),
        "total_generated_rows": len(entries),
        "ready_for_human_audit": ready_count,
        "source_types": sorted({entry["source_type"] for entry in entries}),
        "target_roles": sorted({entry["laundered_role"] for entry in entries}),
        "entries": entries,
    }


def build_power_ops_coverage_matrix(
    *,
    rows_path: str | Path = POWER_OPS_ROWS_PATH,
    trace_scenarios_path: str | Path = POWER_OPS_TRACE_SCENARIOS_PATH,
) -> dict[str, Any]:
    rag_rows = load_paired_rows(rows_path)
    generated_trace_rows = generate_authority_confusion_rows(trace_scenarios_path)
    source_type_counts = _count_by(rag_rows, lambda row: row["source"]["source_type"])
    origin_counts = _row_origin_counts(rag_rows)
    laundered_family_counts = _count_by(
        rag_rows, lambda row: _field_family(row["laundered_consumption"]["field"])
    )
    generated_target_role_counts = _count_by(
        generated_trace_rows,
        lambda row: row["laundered_consumption"]["need"]["required_role"],
    )
    required_source_types = {
        "derived_artifact",
        "evidence",
        "memory",
        "skill",
        "tool_metadata",
        "user_approval",
    }
    required_laundered_families = {
        "answer",
        "approval",
        "data_scope",
        "delegation",
        "parameters",
        "risk_report",
        "side_effect",
    }
    return {
        "artifact_type": "power_ops_afw_coverage_matrix",
        "rows_path": str(Path(rows_path)),
        "trace_scenarios_path": str(Path(trace_scenarios_path)),
        "rag_rows": len(rag_rows),
        "generated_trace_rows": len(generated_trace_rows),
        "source_type_counts": source_type_counts,
        "row_origin_counts": origin_counts,
        "laundered_field_family_counts": laundered_family_counts,
        "generated_target_role_counts": generated_target_role_counts,
        "coverage_gaps": {
            "missing_source_types": sorted(required_source_types - set(source_type_counts)),
            "missing_laundered_field_families": sorted(
                required_laundered_families - set(laundered_family_counts)
            ),
            "human_plausibility_labels": "pending",
            "live_model_traces": "pending",
        },
    }


def render_power_ops_report_markdown(report: dict[str, Any]) -> str:
    inputs = report["inputs"]
    lines = [
        "# Power Operations AFW Report",
        "",
        "## Inputs",
        "",
        "| Item | Value |",
        "|---|---:|",
        f"| RAG rows | {inputs['rag_rows']} |",
        f"| RAG row origins | {len(inputs['rag_row_origins'])} |",
        f"| RAG source types | {len(inputs['rag_source_types'])} |",
        f"| Trace scenarios | {inputs['trace_scenarios']} |",
        f"| Generated trace rows | {inputs['generated_trace_rows']} |",
        f"| Trace source types | {len(inputs['trace_source_types'])} |",
        f"| Generated target roles | {inputs['generated_target_role_count']} |",
        "",
        "## RAG Rows",
        "",
        _summary_table(report["rag_rows"]),
        "",
        "## Trace-Derived Rows",
        "",
        _summary_table(
            {
                "capguard": report["trace_rows"]["generated_capguard"],
                "boundary_scope_only": report["trace_rows"]["generated_boundary_scope_only"],
            }
        ),
        "",
        "| Generated row | Legal role | Laundered role | Held fixed |",
        "|---|---|---|---|",
    ]
    for row in report["trace_rows"]["generated_rows"]:
        held_fixed = ", ".join(row["held_fixed"])
        lines.append(
            f"| `{row['row_id']}` | `{row['legal_role']}` | `{row['laundered_role']}` | {held_fixed} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_power_ops_coverage_matrix_markdown(matrix: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Power Operations AFW Coverage Matrix",
            "",
            "## Summary",
            "",
            "| Item | Value |",
            "|---|---:|",
            f"| RAG paired rows | {matrix['rag_rows']} |",
            f"| Generated trace rows | {matrix['generated_trace_rows']} |",
            f"| Source types | {len(matrix['source_type_counts'])} |",
            f"| Laundered field families | {len(matrix['laundered_field_family_counts'])} |",
            f"| Generated target roles | {len(matrix['generated_target_role_counts'])} |",
            "",
            "## RAG Row Origins",
            "",
            _count_table(matrix["row_origin_counts"]),
            "",
            "## Source Types",
            "",
            _count_table(matrix["source_type_counts"]),
            "",
            "## Laundered Field Families",
            "",
            _count_table(matrix["laundered_field_family_counts"]),
            "",
            "## Top Generated Target Roles",
            "",
            _count_table(matrix["generated_target_role_counts"]),
            "",
            "## Coverage Gaps",
            "",
            "| Gap | Value |",
            "|---|---|",
            f"| Missing source types | {', '.join(matrix['coverage_gaps']['missing_source_types']) or 'none'} |",
            f"| Missing laundered field families | {', '.join(matrix['coverage_gaps']['missing_laundered_field_families']) or 'none'} |",
            f"| Human plausibility labels | {matrix['coverage_gaps']['human_plausibility_labels']} |",
            f"| Live model traces | {matrix['coverage_gaps']['live_model_traces']} |",
            "",
        ]
    )


def render_power_ops_audit_sheet_markdown(sheet: dict[str, Any]) -> str:
    lines = [
        "# Power Operations AFW Plausibility Audit Sheet",
        "",
        "## Summary",
        "",
        "| Item | Value |",
        "|---|---:|",
        f"| Generated rows | {sheet['total_generated_rows']} |",
        f"| Ready for human audit | {sheet['ready_for_human_audit']} |",
        f"| Source types | {len(sheet['source_types'])} |",
        f"| Target roles | {len(sheet['target_roles'])} |",
        "",
        "## Audit Rows",
        "",
        "| Row | Source | Field | Legal role | Laundered role | Precheck | Human plausible | Notes |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for entry in sheet["entries"]:
        lines.append(
            "| `{row_id}` | `{source_type}` | `{field}` | `{legal_role}` | `{laundered_role}` | {status} |  |  |".format(
                row_id=entry["row_id"],
                source_type=entry["source_type"],
                field=entry["field"],
                legal_role=entry["legal_role"],
                laundered_role=entry["laundered_role"],
                status=entry["precheck_status"],
            )
        )
    lines.append("")
    return "\n".join(lines)


def _compact_summary(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "baseline": summary["baseline"],
        "total_rows": summary["total_rows"],
        "legal_preservation_rate": summary["legal_preservation_rate"],
        "laundering_block_rate": summary["laundering_block_rate"],
        "false_allow_rate": summary["false_allow_rate"],
        "false_block_rate": summary["false_block_rate"],
        "abstain_rate": summary["abstain_rate"],
        "same_source_contrast_gap": summary["same_source_contrast_gap"],
        "field_family_results": summary["field_family_results"],
    }


def _row_origin_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        origin = row.get("sample_origin", "manual_paired_row")
        counts[origin] = counts.get(origin, 0) + 1
    return dict(sorted(counts.items()))


def _count_by(rows: list[dict[str, Any]], key_fn) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        key = str(key_fn(row))
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))


def _count_table(counts: dict[str, int]) -> str:
    lines = ["| Item | Count |", "|---|---:|"]
    for item, count in counts.items():
        lines.append(f"| `{item}` | {count} |")
    return "\n".join(lines)


def _field_family(field: str) -> str:
    if field == "requires_human_approval":
        return "approval"
    if field in {"risk_level", "risk_report"} or field.startswith("risk_report."):
        return "risk_report"
    if field in {"data_read_scope", "data_write_scope"}:
        return "data_scope"
    if field.startswith("parameters."):
        return "parameters"
    if field.startswith("answer."):
        return "answer"
    return field


def _summary_table(summaries: dict[str, dict[str, Any]]) -> str:
    lines = [
        "| Baseline | Rows | Legal preservation | Laundering block | False allow | False block |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for label, summary in summaries.items():
        lines.append(
            "| {label} | {rows} | {legal:.3f} | {block:.3f} | {false_allow:.3f} | {false_block:.3f} |".format(
                label=label,
                rows=summary["total_rows"],
                legal=summary["legal_preservation_rate"],
                block=summary["laundering_block_rate"],
                false_allow=summary["false_allow_rate"],
                false_block=summary["false_block_rate"],
            )
        )
    return "\n".join(lines)


def _generated_row_digest(row: dict[str, Any]) -> dict[str, Any]:
    legal = row["legal_consumption"]
    laundered = row["laundered_consumption"]
    return {
        "row_id": row["row_id"],
        "legal_role": legal["need"]["required_role"],
        "laundered_role": laundered["need"]["required_role"],
        "held_fixed": [
            key
            for key, is_fixed in {
                "field": legal["field"] == laundered["field"],
                "operation": legal["operation"] == laundered["operation"],
                "attributed_source_id": legal.get("attributed_source_id")
                == laundered.get("attributed_source_id"),
                "data_scope": legal["need"].get("data_scope") == laundered["need"].get("data_scope"),
                "effect_scope": legal["need"].get("effect_scope")
                == laundered["need"].get("effect_scope"),
                "time_scope": legal["need"].get("time_scope") == laundered["need"].get("time_scope"),
            }.items()
            if is_fixed
        ],
    }


def _audit_entry(row: dict[str, Any]) -> dict[str, Any]:
    digest = _generated_row_digest(row)
    legal = row["legal_consumption"]
    laundered = row["laundered_consumption"]
    required_fixed = {
        "field",
        "operation",
        "attributed_source_id",
        "data_scope",
        "effect_scope",
        "time_scope",
    }
    held_fixed = set(digest["held_fixed"])
    role_changed = digest["legal_role"] != digest["laundered_role"]
    missing_fixed = sorted(required_fixed - held_fixed)
    ready = not missing_fixed and role_changed
    return {
        **digest,
        "source_type": row["source"]["source_type"],
        "field": legal["field"],
        "operation": legal["operation"],
        "legal_value": legal.get("value"),
        "laundered_value": laundered.get("value"),
        "precheck_status": "ready_for_human_audit" if ready else "needs_schema_review",
        "precheck_reasons": {
            "missing_fixed_dimensions": missing_fixed,
            "role_changed": role_changed,
        },
        "human_plausible": None,
        "human_notes": "",
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render the power-operations AFW deterministic report.")
    parser.add_argument("--artifact", choices=("report", "audit", "coverage"), default="report")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--out", type=Path, help="Optional output path.")
    args = parser.parse_args(argv)

    artifact = (
        build_power_ops_plausibility_audit_sheet()
        if args.artifact == "audit"
        else build_power_ops_coverage_matrix()
        if args.artifact == "coverage"
        else build_power_ops_report()
    )
    text = (
        json.dumps(artifact, indent=2, ensure_ascii=False)
        if args.format == "json"
        else (
            render_power_ops_audit_sheet_markdown(artifact)
            if args.artifact == "audit"
            else render_power_ops_coverage_matrix_markdown(artifact)
            if args.artifact == "coverage"
            else render_power_ops_report_markdown(artifact)
        )
    )

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
