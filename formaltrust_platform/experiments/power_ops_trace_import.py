from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Mapping

from formaltrust_platform.experiments.afw_runtime_report import build_afw_runtime_run_summary
from formaltrust_platform.experiments.power_ops_action_invariance import (
    build_action_invariance_summary_from_case_payloads,
)

MULTI_STEP_REQUIRED_SOURCE_TYPES = (
    "memory",
    "prior_step_output",
    "tool_metadata",
    "user_approval",
)


def build_trace_import_summary_from_run_dir(
    run_dir: str | Path,
    *,
    suite_id: str = "power_ops_trace_import",
) -> dict[str, Any]:
    root = Path(run_dir)
    payloads = _load_case_payloads(root)
    cases = [_case_trace_import_digest(payload) for payload in payloads]
    runtime_summary = build_afw_runtime_run_summary(root)
    action_summary = build_action_invariance_summary_from_case_payloads(
        payloads,
        suite_id=f"{suite_id}_action_invariance",
    )

    boundary_counts = Counter(
        boundary
        for case in cases
        for boundary in case["trace_import_boundaries"]
    )
    source_type_counts: Counter[str] = Counter()
    for case in cases:
        for source_type, count in _mapping_value(case.get("source_type_counts")).items():
            source_type_counts[str(source_type)] += _int_value(count)
    source_type_counts_dict = dict(sorted(source_type_counts.items()))

    return {
        "artifact_type": "power_ops_trace_import_summary",
        "suite_id": suite_id,
        "run_dir": str(root),
        "run_id": root.name,
        "total_cases": len(cases),
        "passed_cases": int(runtime_summary.get("passed_cases", 0)),
        "failed_cases": int(runtime_summary.get("failed_cases", 0)),
        "boundary_counts": dict(sorted(boundary_counts.items())),
        "source_type_counts": source_type_counts_dict,
        "multi_step_source_type_coverage": _source_type_coverage(source_type_counts_dict),
        "invalid_trace_cases": sum(1 for case in cases if case["invalid_trace_schema"]),
        "missing_source_cases": sum(1 for case in cases if case["missing_attributed_source_ids"]),
        "duplicate_approval_cases": sum(1 for case in cases if case["duplicate_approval_source_ids"]),
        "expired_epoch_cases": sum(1 for case in cases if case["expired_epoch_fields"]),
        "missing_candidate_action_cases": sum(
            1 for case in cases if not case["has_candidate_action"]
        ),
        "trace_adapter_diagnostics": runtime_summary.get("trace_adapter_diagnostics", {}),
        "runtime_summary": runtime_summary,
        "action_invariance_summary": action_summary,
        "cases": cases,
    }


def render_trace_import_markdown(summary: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Trace Import Summary",
        "",
        "## Inputs",
        "",
        "| Item | Value |",
        "|---|---:|",
        f"| Suite ID | `{summary['suite_id']}` |",
        f"| Run ID | `{summary['run_id']}` |",
        f"| Total cases | {summary['total_cases']} |",
        f"| Passed cases | {summary['passed_cases']} |",
        f"| Failed cases | {summary['failed_cases']} |",
        "",
        "## Import Boundary Coverage",
        "",
        "| Boundary | Cases |",
        "|---|---:|",
    ]
    for boundary, count in _mapping_value(summary.get("boundary_counts")).items():
        lines.append(f"| {boundary} | {int(count)} |")

    source_type_counts = _mapping_value(summary.get("source_type_counts"))
    coverage = _mapping_value(summary.get("multi_step_source_type_coverage"))
    lines.extend(
        [
            "",
            "## Source Type Coverage",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| coverage_rate | {float(coverage.get('coverage_rate', 0.0)):.3f} |",
            f"| missing_source_types | {_join_inline_list(coverage.get('missing_source_types'))} |",
            "",
            "| Source type | Events |",
            "|---|---:|",
        ]
    )
    for source_type, count in source_type_counts.items():
        lines.append(f"| {source_type} | {int(count)} |")

    lines.extend(
        [
            "",
            "## Import Diagnostics",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| invalid_trace_cases | {int(summary.get('invalid_trace_cases', 0))} |",
            f"| missing_source_cases | {int(summary.get('missing_source_cases', 0))} |",
            f"| duplicate_approval_cases | {int(summary.get('duplicate_approval_cases', 0))} |",
            f"| expired_epoch_cases | {int(summary.get('expired_epoch_cases', 0))} |",
            f"| missing_candidate_action_cases | {int(summary.get('missing_candidate_action_cases', 0))} |",
        ]
    )

    diagnostics = _mapping_value(summary.get("trace_adapter_diagnostics"))
    lines.extend(
        [
            "",
            "## Adapter Diagnostics",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| cases_with_invalid_trace_schema | {int(diagnostics.get('cases_with_invalid_trace_schema', 0))} |",
            f"| invalid_events | {int(diagnostics.get('invalid_events', 0))} |",
            f"| unknown_events | {int(diagnostics.get('unknown_events', 0))} |",
            "",
            "| Invalid reason | Count |",
            "|---|---:|",
        ]
    )
    for reason, count in _mapping_value(diagnostics.get("invalid_event_reasons")).items():
        lines.append(f"| {reason} | {int(count)} |")

    action_summary = _mapping_value(summary.get("action_invariance_summary"))
    lines.extend(
        [
            "",
            "## Action-Invariance Readback",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| whole_action_block_rate | {float(action_summary.get('whole_action_block_rate', 0.0)):.3f} |",
            f"| authorized_final_field_preservation_rate | {float(action_summary.get('authorized_final_field_preservation_rate', 0.0)):.3f} |",
            f"| unauthorized_final_field_removal_rate | {float(action_summary.get('unauthorized_final_field_removal_rate', 0.0)):.3f} |",
            f"| repair_frame_validity_rate | {float(action_summary.get('repair_frame_validity_rate', 0.0)):.3f} |",
            "",
            "## Cases",
            "",
            "| Case | Boundary | Gate | Final | Missing source | Duplicate approval | Expired fields | Invalid trace |",
            "|---|---|---|---|---:|---:|---:|---:|",
        ]
    )
    for case in summary.get("cases", []):
        if not isinstance(case, Mapping):
            continue
        lines.append(
            "| `{case_id}` | {boundary} | `{gate}` | `{final}` | {missing} | {duplicate} | {expired} | {invalid} |".format(
                case_id=case.get("case_id", "<unknown>"),
                boundary=", ".join(str(item) for item in case.get("trace_import_boundaries", [])),
                gate=case.get("gate_decision", "missing"),
                final=case.get("final_decision", "missing"),
                missing=len(case.get("missing_attributed_source_ids", [])),
                duplicate=len(case.get("duplicate_approval_source_ids", [])),
                expired=len(case.get("expired_epoch_fields", [])),
                invalid=int(bool(case.get("invalid_trace_schema", False))),
            )
        )
    lines.append("")
    return "\n".join(lines)


def write_trace_import_report(
    summary: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_trace_import_markdown(summary), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")


def _case_trace_import_digest(payload: Mapping[str, Any]) -> dict[str, Any]:
    case = _mapping_value(payload.get("case"))
    metadata = _mapping_value(case.get("metadata"))
    metrics = _mapping_value(payload.get("metrics"))
    diagnostics = _mapping_value(metrics.get("afw_trace_adapter_diagnostics"))
    adapter_summary = _mapping_value(metrics.get("afw_trace_adapter_summary"))
    final_action = _mapping_value(metrics.get("final_action"))
    source_events = [
        event
        for event in _list_value(metrics.get("afw_source_events"))
        if isinstance(event, Mapping)
    ]
    consumptions = [
        consumption
        for consumption in _list_value(metrics.get("afw_consumptions"))
        if isinstance(consumption, Mapping)
    ]
    source_type_counts = Counter(
        str(event["source_type"])
        for event in source_events
        if isinstance(event.get("source_type"), str) and event.get("source_type")
    )

    source_ids = {
        str(event["source_id"])
        for event in source_events
        if isinstance(event.get("source_id"), str)
    }
    duplicate_approval_source_ids = _duplicate_approval_source_ids(source_events)
    missing_source_ids = sorted(
        {
            str(consumption["attributed_source_id"])
            for consumption in consumptions
            if isinstance(consumption.get("attributed_source_id"), str)
            and consumption["attributed_source_id"] not in source_ids
        }
    )
    expired_epoch_fields = _expired_epoch_fields(source_events, consumptions)

    return {
        "case_id": str(case.get("id", "<unknown>")),
        "trace_import_boundaries": _trace_import_boundaries(metadata),
        "gate_decision": str(metrics.get("afw_gate_decision", "missing")),
        "final_decision": str(final_action.get("decision", "missing")),
        "invalid_trace_schema": diagnostics.get("schema_contract_status") == "invalid",
        "invalid_events": int(diagnostics.get("invalid_events", 0)),
        "unknown_events": int(diagnostics.get("unknown_events", 0)),
        "source_event_count": len(source_events),
        "source_type_counts": dict(sorted(source_type_counts.items())),
        "consumption_count": len(consumptions),
        "has_candidate_action": bool(adapter_summary.get("has_candidate_action", False)),
        "missing_attributed_source_ids": missing_source_ids,
        "duplicate_approval_source_ids": duplicate_approval_source_ids,
        "expired_epoch_fields": expired_epoch_fields,
    }


def _trace_import_boundaries(metadata: Mapping[str, Any]) -> list[str]:
    boundary = metadata.get("trace_import_boundary")
    if isinstance(boundary, str) and boundary:
        return [boundary]
    if isinstance(boundary, list):
        return [item for item in boundary if isinstance(item, str) and item]
    trace_import = metadata.get("trace_import")
    if isinstance(trace_import, Mapping):
        nested = trace_import.get("boundary")
        if isinstance(nested, str) and nested:
            return [nested]
        if isinstance(nested, list):
            return [item for item in nested if isinstance(item, str) and item]
    return ["unspecified"]


def _duplicate_approval_source_ids(source_events: list[Mapping[str, Any]]) -> list[str]:
    counts: Counter[str] = Counter()
    approval_ids: set[str] = set()
    for event in source_events:
        source_id = event.get("source_id")
        if not isinstance(source_id, str):
            continue
        counts[source_id] += 1
        if event.get("source_type") == "user_approval":
            approval_ids.add(source_id)
    return sorted(source_id for source_id, count in counts.items() if count > 1 and source_id in approval_ids)


def _expired_epoch_fields(
    source_events: list[Mapping[str, Any]],
    consumptions: list[Mapping[str, Any]],
) -> list[str]:
    scopes_by_source_id: dict[str, set[str]] = {}
    for event in source_events:
        source_id = event.get("source_id")
        if not isinstance(source_id, str):
            continue
        manifest = event.get("authority_manifest")
        if not isinstance(manifest, Mapping):
            continue
        time_scopes = {
            str(scope)
            for scope in _list_value(manifest.get("time_scope"))
            if isinstance(scope, str) and scope
        }
        if time_scopes:
            scopes_by_source_id.setdefault(source_id, set()).update(time_scopes)

    expired_fields: list[str] = []
    for consumption in consumptions:
        source_id = consumption.get("attributed_source_id")
        field = consumption.get("field")
        need = consumption.get("need")
        if not isinstance(source_id, str) or not isinstance(field, str) or not isinstance(need, Mapping):
            continue
        required_time_scope = need.get("time_scope")
        if not isinstance(required_time_scope, str) or not required_time_scope:
            continue
        available = scopes_by_source_id.get(source_id, set())
        if available and required_time_scope not in available:
            expired_fields.append(field)
    return sorted(set(expired_fields))


def _load_case_payloads(run_dir: Path) -> list[dict[str, Any]]:
    case_dir = run_dir / "cases"
    if not case_dir.is_dir():
        raise ValueError(f"FormalTrust run directory has no cases directory: {run_dir}")
    payloads: list[dict[str, Any]] = []
    for path in sorted(case_dir.glob("*.json")):
        with path.open("r", encoding="utf-8") as handle:
            payloads.append(json.load(handle))
    return payloads


def _mapping_value(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    return {}


def _source_type_coverage(source_type_counts: Mapping[str, Any]) -> dict[str, Any]:
    required = list(MULTI_STEP_REQUIRED_SOURCE_TYPES)
    covered = [
        source_type
        for source_type in required
        if _int_value(source_type_counts.get(source_type)) > 0
    ]
    missing = [source_type for source_type in required if source_type not in covered]
    return {
        "required_source_types": required,
        "covered_source_types": covered,
        "missing_source_types": missing,
        "coverage_rate": _ratio_float(len(covered), len(required), default=1.0),
    }


def _join_inline_list(value: Any) -> str:
    items = [str(item) for item in _list_value(value) if str(item)]
    return ", ".join(items) if items else "none"


def _int_value(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _ratio_float(numerator: int, denominator: int, *, default: float = 0.0) -> float:
    if denominator == 0:
        return default
    return numerator / denominator


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
        description="Summarize power-ops trace import behavior from a FormalTrust run."
    )
    subparsers = parser.add_subparsers(dest="command")
    summarize = subparsers.add_parser("summarize")
    summarize.add_argument("--run-dir", required=True)
    summarize.add_argument("--suite-id", default="power_ops_trace_import")
    summarize.add_argument("--out-md")
    summarize.add_argument("--out-json")
    summarize.add_argument("--format", choices=["markdown", "json"], default="markdown")

    parser.add_argument("--run-dir")
    parser.add_argument("--suite-id", default="power_ops_trace_import")
    parser.add_argument("--out-md")
    parser.add_argument("--out-json")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args(argv)

    run_dir = args.run_dir
    if run_dir is None:
        parser.error("--run-dir is required")

    summary = build_trace_import_summary_from_run_dir(run_dir, suite_id=args.suite_id)
    if args.out_md or args.out_json:
        write_trace_import_report(
            summary,
            markdown_path=args.out_md or Path(run_dir) / "trace_import.md",
            json_path=args.out_json,
        )
        return 0

    if args.format == "json":
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_trace_import_markdown(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
