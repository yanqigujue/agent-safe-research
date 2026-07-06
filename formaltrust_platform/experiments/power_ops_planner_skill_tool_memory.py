from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping

from formaltrust_platform.experiments.power_ops_trace_import import (
    build_trace_import_summary_from_run_dir,
)

REQUIRED_SOURCE_TYPES = (
    "memory",
    "prior_step_output",
    "skill",
    "tool_metadata",
    "user_approval",
)


def build_planner_skill_tool_memory_summary_from_run_dir(
    run_dir: str | Path,
    *,
    suite_id: str = "power_ops_planner_skill_tool_memory",
) -> dict[str, Any]:
    trace_summary = build_trace_import_summary_from_run_dir(run_dir, suite_id=suite_id)
    action_summary = _mapping_value(trace_summary.get("action_invariance_summary"))
    action_field_counts = _mapping_value(action_summary.get("field_counts"))
    source_type_counts = _mapping_value(trace_summary.get("source_type_counts"))

    return {
        "artifact_type": "power_ops_planner_skill_tool_memory_summary",
        "suite_id": suite_id,
        "run_dir": trace_summary.get("run_dir", ""),
        "run_id": trace_summary.get("run_id", ""),
        "total_cases": int(trace_summary.get("total_cases", 0) or 0),
        "passed_cases": int(trace_summary.get("passed_cases", 0) or 0),
        "failed_cases": int(trace_summary.get("failed_cases", 0) or 0),
        "boundary_counts": _mapping_value(trace_summary.get("boundary_counts")),
        "source_type_counts": dict(sorted((str(k), int(v)) for k, v in source_type_counts.items())),
        "source_chain_coverage": _source_chain_coverage(source_type_counts),
        "field_counts": {
            "authorized_fields": int(action_field_counts.get("authorized_fields", 0) or 0),
            "unauthorized_fields": int(action_field_counts.get("unauthorized_fields", 0) or 0),
            "preserved_authorized_fields": int(
                action_field_counts.get("preserved_authorized_fields", 0) or 0
            ),
            "removed_unauthorized_fields": int(
                action_field_counts.get("prevented_unauthorized_fields", 0) or 0
            ),
        },
        "whole_action_block_rate": float(action_summary.get("whole_action_block_rate", 0.0) or 0.0),
        "authorized_final_field_preservation_rate": float(
            action_summary.get("authorized_final_field_preservation_rate", 0.0) or 0.0
        ),
        "unauthorized_final_field_removal_rate": float(
            action_summary.get("unauthorized_final_field_removal_rate", 0.0) or 0.0
        ),
        "repair_frame_validity_rate": float(
            action_summary.get("repair_frame_validity_rate", 0.0) or 0.0
        ),
        "trace_import_summary": trace_summary,
        "action_invariance_summary": action_summary,
    }


def render_planner_skill_tool_memory_markdown(summary: Mapping[str, Any]) -> str:
    coverage = _mapping_value(summary.get("source_chain_coverage"))
    lines = [
        "# Power-Ops Planner-Skill-Tool-Memory Summary",
        "",
        "## Inputs",
        "",
        "| Item | Value |",
        "|---|---:|",
        f"| Suite ID | `{summary.get('suite_id', '')}` |",
        f"| Run ID | `{summary.get('run_id', '')}` |",
        f"| Total cases | {int(summary.get('total_cases', 0) or 0)} |",
        f"| Passed cases | {int(summary.get('passed_cases', 0) or 0)} |",
        f"| Failed cases | {int(summary.get('failed_cases', 0) or 0)} |",
        "",
        "## Source Chain Coverage",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| coverage_rate | {float(coverage.get('coverage_rate', 0.0) or 0.0):.3f} |",
        f"| missing_source_types | {_join_inline_list(coverage.get('missing_source_types'))} |",
        "",
        "| Source type | Events |",
        "|---|---:|",
    ]
    for source_type, count in _mapping_value(summary.get("source_type_counts")).items():
        lines.append(f"| {source_type} | {int(count)} |")

    field_counts = _mapping_value(summary.get("field_counts"))
    lines.extend(
        [
            "",
            "## Action-Invariance Readback",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| authorized_fields | {int(field_counts.get('authorized_fields', 0) or 0)} |",
            f"| unauthorized_fields | {int(field_counts.get('unauthorized_fields', 0) or 0)} |",
            f"| preserved_authorized_fields | {int(field_counts.get('preserved_authorized_fields', 0) or 0)} |",
            f"| removed_unauthorized_fields | {int(field_counts.get('removed_unauthorized_fields', 0) or 0)} |",
            f"| whole_action_block_rate | {float(summary.get('whole_action_block_rate', 0.0) or 0.0):.3f} |",
            f"| authorized_final_field_preservation_rate | {float(summary.get('authorized_final_field_preservation_rate', 0.0) or 0.0):.3f} |",
            f"| unauthorized_final_field_removal_rate | {float(summary.get('unauthorized_final_field_removal_rate', 0.0) or 0.0):.3f} |",
            f"| repair_frame_validity_rate | {float(summary.get('repair_frame_validity_rate', 0.0) or 0.0):.3f} |",
            "",
        ]
    )
    return "\n".join(lines)


def write_planner_skill_tool_memory_report(
    summary: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_planner_skill_tool_memory_markdown(summary), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")


def _source_chain_coverage(source_type_counts: Mapping[str, Any]) -> dict[str, Any]:
    covered = [
        source_type
        for source_type in REQUIRED_SOURCE_TYPES
        if int(source_type_counts.get(source_type, 0) or 0) > 0
    ]
    missing = [source_type for source_type in REQUIRED_SOURCE_TYPES if source_type not in covered]
    return {
        "required_source_types": list(REQUIRED_SOURCE_TYPES),
        "covered_source_types": covered,
        "missing_source_types": missing,
        "coverage_rate": _ratio_float(len(covered), len(REQUIRED_SOURCE_TYPES), default=1.0),
    }


def _mapping_value(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    return {}


def _join_inline_list(value: Any) -> str:
    items = [str(item) for item in _list_value(value) if str(item)]
    return ", ".join(items) if items else "none"


def _list_value(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return list(value)
    if isinstance(value, tuple | set):
        return list(value)
    return [value]


def _ratio_float(numerator: int, denominator: int, *, default: float = 0.0) -> float:
    if denominator == 0:
        return default
    return numerator / denominator


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Summarize the planner-skill-tool-memory power-ops action-invariance benchmark."
    )
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--suite-id", default="power_ops_planner_skill_tool_memory")
    parser.add_argument("--out-md")
    parser.add_argument("--out-json")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args(argv)

    summary = build_planner_skill_tool_memory_summary_from_run_dir(
        args.run_dir,
        suite_id=args.suite_id,
    )
    if args.out_md or args.out_json:
        write_planner_skill_tool_memory_report(
            summary,
            markdown_path=args.out_md or Path(args.run_dir) / "planner_skill_tool_memory.md",
            json_path=args.out_json,
        )
        return 0

    if args.format == "json":
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_planner_skill_tool_memory_markdown(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
