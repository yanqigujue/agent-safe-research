from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping, Sequence


TABLE_NAMES = ("Current Result", "Baseline Grid", "Performance Profile")

CURRENT_RESULT_SUITES = {
    "strict-block": "power_ops_action_invariance_runtime",
    "fieldwise-repair": "power_ops_action_invariance_fieldwise_repair",
    "trace-repair": "power_ops_action_invariance_trace_repair",
    "span-otlp-repair": "power_ops_action_invariance_span_otlp_repair",
    "agentdojo-style": "power_ops_action_invariance_agentdojo_style",
    "semireal-trace": "power_ops_action_invariance_semireal_trace",
    "expanded-fieldwise": "power_ops_action_invariance_expanded",
    "metamorphic": "power_ops_action_invariance_metamorphic",
    "skill-authority": "power_ops_skill_authority",
    "trace-import": "power_ops_trace_import",
    "multistep-trace-import": "power_ops_multistep_trace_import",
    "planner-skill-tool-memory": "power_ops_planner_skill_tool_memory",
    "normal-behavior-stress": "power_ops_normal_behavior_stress",
    "external-50-full-agent-cases": "power_ops_external_case_50",
}

BASELINE_LABELS = {
    "strict-block": "strict_block",
    "fieldwise-decision-only": "fieldwise_decision_only",
    "provenance-only": "provenance_only",
    "fieldwise-repair": "fieldwise_repair",
}

PERFORMANCE_LABELS = {
    "expanded-fieldwise": "power_ops_action_invariance_expanded",
    "metamorphic": "power_ops_action_invariance_metamorphic",
    "skill-authority": "power_ops_skill_authority",
}


def build_table_evidence_binding(
    *,
    readme_path: str | Path,
    evidence_paths: Sequence[str | Path],
) -> dict[str, Any]:
    readme = Path(readme_path).read_text(encoding="utf-8")
    tables = _extract_named_tables(readme)
    evidence = [_evidence_payload(path) for path in evidence_paths]
    evidence_index = _build_evidence_index(evidence)
    rows = [
        _bind_table_row(table_name, row, evidence_index)
        for table_name in TABLE_NAMES
        for row in tables.get(table_name, {}).get("rows", [])
    ]
    fully_supported = sum(1 for row in rows if row["status"] == "fully_supported")
    unsupported = sum(1 for row in rows if row["status"] != "fully_supported")

    return {
        "artifact_type": "power_ops_table_evidence_binding",
        "readme_path": str(readme_path),
        "table_count": len(tables),
        "evidence_count": len(evidence),
        "fully_supported_row_count": fully_supported,
        "unsupported_row_count": unsupported,
        "tables": {
            name: {
                "columns": tables.get(name, {}).get("columns", []),
                "row_count": len(tables.get(name, {}).get("rows", [])),
            }
            for name in TABLE_NAMES
        },
        "rows": rows,
    }


def render_table_evidence_binding_markdown(binding: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Table Evidence Binding",
        "",
        "| Item | Value |",
        "|---|---:|",
        f"| tables | {int(binding.get('table_count', 0))} |",
        f"| evidence files | {int(binding.get('evidence_count', 0))} |",
        f"| fully supported rows | {int(binding.get('fully_supported_row_count', 0))} |",
        f"| unsupported rows | {int(binding.get('unsupported_row_count', 0))} |",
        "",
        "## Rows",
        "",
        "| Table | Row | Status | Evidence | Supported metrics | Missing metrics |",
        "|---|---|---|---|---|---|",
    ]
    for row in _list_value(binding.get("rows")):
        if not isinstance(row, Mapping):
            continue
        lines.append(
            "| {table} | {row_label} | {status} | `{artifact}` | {supported} | {missing} |".format(
                table=row.get("table", ""),
                row_label=row.get("row_label", ""),
                status=row.get("status", ""),
                artifact=row.get("source_artifact", ""),
                supported=", ".join(_list_value(row.get("supported_metrics"))) or "none",
                missing=", ".join(_list_value(row.get("missing_metrics"))) or "none",
            )
        )
    lines.append("")
    return "\n".join(lines)


def write_table_evidence_binding(
    binding: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_table_evidence_binding_markdown(binding), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.write_text(json.dumps(binding, ensure_ascii=False, indent=2), encoding="utf-8")


def _bind_table_row(
    table_name: str,
    row: Mapping[str, str],
    evidence_index: Mapping[str, Any],
) -> dict[str, Any]:
    label = _first_cell(row)
    if table_name == "Current Result":
        payload = evidence_index.get("suite_id", {}).get(CURRENT_RESULT_SUITES.get(label, ""))
        expected = _current_result_expected_values(payload)
    elif table_name == "Baseline Grid":
        baseline_name = BASELINE_LABELS.get(label, "")
        payload = evidence_index.get("artifact_type", {}).get("power_ops_action_invariance_baseline_grid")
        expected = _baseline_expected_values(payload, baseline_name)
    elif table_name == "Performance Profile":
        profile_name = PERFORMANCE_LABELS.get(label, "")
        payload = evidence_index.get("artifact_type", {}).get("power_ops_action_invariance_performance_profile")
        expected = _performance_expected_values(payload, profile_name)
    else:
        payload = None
        expected = {}

    observed = dict(row)
    supported_metrics: list[str] = []
    missing_metrics: list[str] = []
    for column, observed_value in observed.items():
        if column in ("Mode", "Baseline", "Profile"):
            continue
        expected_value = expected.get(column)
        if expected_value is not None and str(observed_value) == str(expected_value):
            supported_metrics.append(column)
        else:
            missing_metrics.append(column)

    return {
        "table": table_name,
        "row_label": label,
        "status": "fully_supported" if payload and not missing_metrics else "needs_evidence",
        "source_artifact": str(_payload_path(payload)),
        "source_artifact_type": str(_mapping_value(payload).get("artifact_type", "")),
        "observed_values": observed,
        "expected_values": expected,
        "supported_metrics": supported_metrics,
        "missing_metrics": missing_metrics,
    }


def _current_result_expected_values(payload: Any) -> dict[str, str]:
    root = _mapping_value(payload)
    action = _action_summary(root)
    total = _int_value(root.get("total_cases"))
    passed = _int_value(root.get("passed_cases"), default=total)
    return {
        "Passed": f"{passed}/{total}",
        "Whole-action block rate": _format_float(action.get("whole_action_block_rate")),
        "Executable repair success": _format_float(
            action.get("executable_fieldwise_repair_success_rate")
        ),
        "Repair frame validity": _format_float(action.get("repair_frame_validity_rate")),
    }


def _baseline_expected_values(payload: Any, baseline_name: str) -> dict[str, str]:
    baseline = _mapping_value(_mapping_value(_mapping_value(payload).get("baselines")).get(baseline_name))
    return {
        "Authorized final preservation": _format_float(
            baseline.get("authorized_final_field_preservation_rate")
        ),
        "Unauthorized final removal": _format_float(
            baseline.get("unauthorized_final_field_removal_rate")
        ),
        "Whole-action block": _format_float(baseline.get("whole_action_block_rate")),
        "Executable invariance": _format_float(baseline.get("executable_action_invariance_rate")),
        "False allow fields": _format_float(baseline.get("false_allow_field_rate")),
    }


def _performance_expected_values(payload: Any, profile_name: str) -> dict[str, str]:
    profile = _mapping_value(_mapping_value(_mapping_value(payload).get("suite_profiles")).get(profile_name))
    return {
        "Normal preservation": _format_float(profile.get("normal_behavior_preservation")),
        "Safety removal": _format_float(profile.get("safety_removal")),
        "Whole-action block": _format_float(profile.get("whole_action_block_rate")),
        "Latency proxy": str(_int_value(profile.get("latency_proxy_units"))),
        "Audit compression": _format_float(profile.get("audit_compression")),
    }


def _action_summary(payload: Mapping[str, Any]) -> dict[str, Any]:
    action = payload.get("action_invariance_summary")
    if isinstance(action, Mapping):
        return dict(action)
    return dict(payload)


def _extract_named_tables(markdown: str) -> dict[str, dict[str, Any]]:
    lines = markdown.splitlines()
    tables: dict[str, dict[str, Any]] = {}
    for index, line in enumerate(lines):
        if not line.startswith("## "):
            continue
        heading = line.removeprefix("## ").strip()
        if heading not in TABLE_NAMES:
            continue
        table_lines = _first_table_after_heading(lines[index + 1 :])
        tables[heading] = _parse_markdown_table(table_lines)
    return tables


def _first_table_after_heading(lines: list[str]) -> list[str]:
    table_lines: list[str] = []
    in_table = False
    for line in lines:
        if line.startswith("## "):
            break
        if line.strip().startswith("|"):
            in_table = True
            table_lines.append(line)
            continue
        if in_table:
            break
    return table_lines


def _parse_markdown_table(lines: list[str]) -> dict[str, Any]:
    if len(lines) < 2:
        return {"columns": [], "rows": []}
    columns = _split_table_row(lines[0])
    rows = [
        dict(zip(columns, _split_table_row(line), strict=False))
        for line in lines[2:]
        if line.strip().startswith("|")
    ]
    return {"columns": columns, "rows": rows}


def _split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _build_evidence_index(evidence: list[dict[str, Any]]) -> dict[str, dict[str, dict[str, Any]]]:
    by_suite: dict[str, dict[str, Any]] = {}
    by_type: dict[str, dict[str, Any]] = {}
    for item in evidence:
        payload = _mapping_value(item.get("payload"))
        path = item.get("path")
        payload["__path"] = path
        suite_id = payload.get("suite_id")
        artifact_type = payload.get("artifact_type")
        if isinstance(suite_id, str):
            by_suite[suite_id] = payload
        if isinstance(artifact_type, str):
            by_type[artifact_type] = payload
    return {"suite_id": by_suite, "artifact_type": by_type}


def _evidence_payload(path: str | Path) -> dict[str, Any]:
    target = Path(path)
    payload = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object at {path}")
    return {"path": str(target), "payload": payload}


def _payload_path(payload: Any) -> str:
    return str(_mapping_value(payload).get("__path", "missing"))


def _first_cell(row: Mapping[str, str]) -> str:
    if not row:
        return ""
    return str(next(iter(row.values()))).strip()


def _format_float(value: Any) -> str:
    try:
        return f"{float(value):.3f}"
    except (TypeError, ValueError):
        return "missing"


def _int_value(value: Any, *, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _mapping_value(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    return {}


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
        description="Bind power-ops README result-table rows to evidence artifacts."
    )
    parser.add_argument("--readme", default="README_POWER_OPS_ACTION_INVARIANCE.md")
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument(
        "--out-md",
        default="docs/power_ops_action_invariance_table_evidence_binding_2026-07-02.md",
    )
    parser.add_argument(
        "--out-json",
        default="docs/power_ops_action_invariance_table_evidence_binding_2026-07-02.json",
    )
    args = parser.parse_args(argv)

    binding = build_table_evidence_binding(
        readme_path=args.readme,
        evidence_paths=args.evidence,
    )
    write_table_evidence_binding(binding, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
