from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def build_afw_runtime_run_summary(run_dir: str | Path) -> dict[str, Any]:
    """Summarize AFW runtime guardrail/evaluator outputs from a FormalTrust run."""

    root = Path(run_dir)
    payloads = _load_case_payloads(root)
    cases = [_case_digest(payload) for payload in payloads]
    total_cases = len(cases)
    passed_cases = sum(1 for case in cases if case["evaluation_passed"])
    field_counts = {
        "total_runtime_fields": sum(case["total_runtime_fields"] for case in cases),
        "prevented_fields": sum(len(case["prevented_fields"]) for case in cases),
        "false_allow_fields": sum(len(case["false_allow_fields"]) for case in cases),
        "false_block_fields": sum(len(case["false_block_fields"]) for case in cases),
    }
    expected_allow_fields = sum(case["expected_allow_fields"] for case in cases)
    source_type_counts = _count_source_types(cases)
    runtime_gate_counts = _runtime_gate_counts(cases)
    runtime_field_decision_counts = _runtime_field_decision_counts(cases)
    counter_authority_counts = _counter_authority_counts(cases)
    witness_audit_counts = _witness_audit_counts(cases)
    witness_audit_compression = _witness_audit_compression(cases)

    return {
        "artifact_type": "afw_runtime_run_summary",
        "run_dir": str(root),
        "run_id": root.name,
        "total_cases": total_cases,
        "passed_cases": passed_cases,
        "failed_cases": total_cases - passed_cases,
        "mean_afw_behmatch": _mean([case["afw_behmatch"] for case in cases]),
        "field_counts": field_counts,
        "source_type_counts": source_type_counts,
        "runtime_gate_counts": runtime_gate_counts,
        "runtime_field_decision_counts": runtime_field_decision_counts,
        "counter_authority_counts": counter_authority_counts,
        "witness_audit_counts": witness_audit_counts,
        "witness_audit_compression": witness_audit_compression,
        "trace_adapter_diagnostics": _trace_adapter_diagnostics(payloads),
        "k_metrics": {
            "k1_safe_behavior_match_rate": _ratio(
                sum(1 for case in cases if case["k1_safe_behavior_match"]),
                total_cases,
            ),
            "k2_risk_discovery_proxy": _ratio(
                field_counts["prevented_fields"],
                field_counts["prevented_fields"] + field_counts["false_allow_fields"],
            ),
            "k3_safety_issue_reduction_proxy": _ratio(
                field_counts["prevented_fields"],
                field_counts["prevented_fields"] + field_counts["false_allow_fields"],
            ),
            "k4_utility_preservation_proxy": _ratio(
                expected_allow_fields - field_counts["false_block_fields"],
                expected_allow_fields,
                default=1.0,
            ),
        },
        "cases": cases,
    }


def build_afw_runtime_suite_summary(
    run_dirs: list[str | Path],
    *,
    suite_id: str = "afw_runtime_suite",
) -> dict[str, Any]:
    """Summarize several AFW runtime runs as one validation suite."""

    run_summaries = [build_afw_runtime_run_summary(run_dir) for run_dir in run_dirs]
    total_cases = sum(int(summary["total_cases"]) for summary in run_summaries)
    passed_cases = sum(int(summary["passed_cases"]) for summary in run_summaries)
    field_counts = _sum_named_counts(
        run_summaries,
        "field_counts",
        ("total_runtime_fields", "prevented_fields", "false_allow_fields", "false_block_fields"),
    )
    witness_audit_counts = _sum_named_counts(
        run_summaries,
        "witness_audit_counts",
        (
            "total_fields_with_witness_audit",
            "covers_need_fields",
            "missing_role_fields",
            "undischarged_obligation_fields",
        ),
    )
    witness_audit_compression = _suite_witness_audit_compression(run_summaries)

    return {
        "artifact_type": "afw_runtime_suite_summary",
        "suite_id": suite_id,
        "total_runs": len(run_summaries),
        "total_cases": total_cases,
        "passed_cases": passed_cases,
        "failed_cases": total_cases - passed_cases,
        "mean_afw_behmatch": _weighted_mean(
            (
                float(summary.get("mean_afw_behmatch", 0.0)),
                int(summary.get("total_cases", 0)),
            )
            for summary in run_summaries
        ),
        "k_metrics": _suite_k_metrics(run_summaries, field_counts),
        "field_counts": field_counts,
        "source_type_counts": _merge_named_count_key(run_summaries, "source_type_counts"),
        "runtime_gate_counts": _merge_named_count_key(run_summaries, "runtime_gate_counts"),
        "runtime_field_decision_counts": _merge_named_count_key(
            run_summaries,
            "runtime_field_decision_counts",
        ),
        "counter_authority_counts": _merge_named_count_key(
            run_summaries,
            "counter_authority_counts",
        ),
        "witness_audit_counts": witness_audit_counts,
        "witness_audit_compression": witness_audit_compression,
        "trace_adapter_diagnostics": _suite_trace_adapter_diagnostics(run_summaries),
        "runs": [_suite_run_digest(summary) for summary in run_summaries],
    }


def render_afw_runtime_suite_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# AFW Runtime Suite Summary",
        "",
        "## Inputs",
        "",
        "| Item | Value |",
        "|---|---:|",
        f"| Suite ID | `{summary['suite_id']}` |",
        f"| Total runs | {summary['total_runs']} |",
        f"| Total cases | {summary['total_cases']} |",
        f"| Passed cases | {summary['passed_cases']} |",
        f"| Failed cases | {summary['failed_cases']} |",
        f"| Mean AFW BehMatch | {summary['mean_afw_behmatch']:.3f} |",
        "",
        "## K Metrics",
        "",
        "| Metric | Value |",
        "|---|---:|",
    ]
    for metric, value in summary["k_metrics"].items():
        lines.append(f"| {metric} | {value:.3f} |")

    _append_count_table(lines, "Field Counts", "Count", summary["field_counts"])
    _append_count_table(lines, "Runtime Decisions", "Metric", {
        "allow_cases": summary["runtime_gate_counts"].get("allow", 0),
        "block_cases": summary["runtime_gate_counts"].get("block", 0),
        "abstain_cases": summary["runtime_gate_counts"].get("abstain", 0),
        "missing_cases": summary["runtime_gate_counts"].get("missing", 0),
        "allow_fields": summary["runtime_field_decision_counts"].get("allow", 0),
        "block_fields": summary["runtime_field_decision_counts"].get("block", 0),
        "abstain_fields": summary["runtime_field_decision_counts"].get("abstain", 0),
    })
    _append_count_table(lines, "Counter-Authority", "Metric", summary["counter_authority_counts"])
    _append_count_table(lines, "Authority Witness Audit", "Metric", {
        **summary["witness_audit_counts"],
        **summary["witness_audit_compression"],
    })
    _append_count_table(lines, "Source Types", "Source type", summary["source_type_counts"])

    diagnostics = summary["trace_adapter_diagnostics"]
    _append_count_table(lines, "Trace Adapter Diagnostics", "Metric", {
        "cases_with_invalid_trace_schema": diagnostics.get("cases_with_invalid_trace_schema", 0),
        "invalid_events": diagnostics.get("invalid_events", 0),
        "unknown_events": diagnostics.get("unknown_events", 0),
    })
    _append_count_table(lines, "Invalid Trace Reasons", "Reason", diagnostics.get("invalid_event_reasons", {}))
    _append_count_table(lines, "Ignored Trace Event Types", "Event type", diagnostics.get("ignored_event_types", {}))

    lines.extend(
        [
            "",
            "## Runs",
            "",
            "| Run | Cases | Passed | Mean BehMatch | Prevented | False allow | False block |",
            "|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for run in summary["runs"]:
        lines.append(
            "| `{run_id}` | {total_cases} | {passed_cases} | {mean_afw_behmatch:.3f} | {prevented_fields} | {false_allow_fields} | {false_block_fields} |".format(
                run_id=run["run_id"],
                total_cases=run["total_cases"],
                passed_cases=run["passed_cases"],
                mean_afw_behmatch=run["mean_afw_behmatch"],
                prevented_fields=run["field_counts"]["prevented_fields"],
                false_allow_fields=run["field_counts"]["false_allow_fields"],
                false_block_fields=run["field_counts"]["false_block_fields"],
            )
        )
    lines.append("")
    return "\n".join(lines)


def render_afw_runtime_run_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# AFW Runtime Run Summary",
        "",
        "## Inputs",
        "",
        "| Item | Value |",
        "|---|---:|",
        f"| Run ID | `{summary['run_id']}` |",
        f"| Total cases | {summary['total_cases']} |",
        f"| Passed cases | {summary['passed_cases']} |",
        f"| Failed cases | {summary['failed_cases']} |",
        f"| Mean AFW BehMatch | {summary['mean_afw_behmatch']:.3f} |",
        "",
        "## K Metrics",
        "",
        "| Metric | Value |",
        "|---|---:|",
    ]
    for metric, value in summary["k_metrics"].items():
        lines.append(f"| {metric} | {value:.3f} |")

    lines.extend(
        [
            "",
            "## Field Counts",
            "",
            "| Count | Value |",
            "|---|---:|",
        ]
    )
    for name, value in summary["field_counts"].items():
        lines.append(f"| {name} | {value} |")

    lines.extend(
        [
            "",
            "## Source Types",
            "",
            "| Source type | Cases |",
            "|---|---:|",
        ]
    )
    for source_type, count in summary["source_type_counts"].items():
        lines.append(f"| {source_type} | {count} |")

    gate_counts = summary.get("runtime_gate_counts", {})
    field_decision_counts = summary.get("runtime_field_decision_counts", {})
    lines.extend(
        [
            "",
            "## Runtime Decisions",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| allow_cases | {int(gate_counts.get('allow', 0))} |",
            f"| block_cases | {int(gate_counts.get('block', 0))} |",
            f"| abstain_cases | {int(gate_counts.get('abstain', 0))} |",
            f"| missing_cases | {int(gate_counts.get('missing', 0))} |",
            f"| allow_fields | {int(field_decision_counts.get('allow', 0))} |",
            f"| block_fields | {int(field_decision_counts.get('block', 0))} |",
            f"| abstain_fields | {int(field_decision_counts.get('abstain', 0))} |",
        ]
    )

    counter_authority = summary.get("counter_authority_counts", {})
    lines.extend(
        [
            "",
            "## Counter-Authority",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| cases_with_counter_authority | {int(counter_authority.get('cases_with_counter_authority', 0))} |",
            f"| counter_authority_events | {int(counter_authority.get('counter_authority_events', 0))} |",
        ]
    )

    witness_counts = summary.get("witness_audit_counts", {})
    witness_compression = summary.get("witness_audit_compression", {})
    lines.extend(
        [
            "",
            "## Authority Witness Audit",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| total_fields_with_witness_audit | {int(witness_counts.get('total_fields_with_witness_audit', 0))} |",
            f"| covers_need_fields | {int(witness_counts.get('covers_need_fields', 0))} |",
            f"| missing_role_fields | {int(witness_counts.get('missing_role_fields', 0))} |",
            f"| undischarged_obligation_fields | {int(witness_counts.get('undischarged_obligation_fields', 0))} |",
            f"| full_context_capability_count | {int(witness_compression.get('full_context_capability_count', 0))} |",
            f"| witness_capability_count | {int(witness_compression.get('witness_capability_count', 0))} |",
            f"| irrelevant_capability_count | {int(witness_compression.get('irrelevant_capability_count', 0))} |",
            f"| mean_compression_ratio | {float(witness_compression.get('mean_compression_ratio', 0.0)):.3f} |",
        ]
    )

    diagnostics = summary.get("trace_adapter_diagnostics", {})
    lines.extend(
        [
            "",
            "## Trace Adapter Diagnostics",
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
    for reason, count in diagnostics.get("invalid_event_reasons", {}).items():
        lines.append(f"| {reason} | {count} |")
    lines.extend(
        [
            "",
            "| Ignored event type | Count |",
            "|---|---:|",
        ]
    )
    for event_type, count in diagnostics.get("ignored_event_types", {}).items():
        lines.append(f"| {event_type} | {count} |")

    lines.extend(
        [
            "",
            "## Cases",
            "",
            "| Case | Gate | Final decision | BehMatch | Prevented | Abstained | Counter auth | False allow | False block |",
            "|---|---|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for case in summary["cases"]:
        lines.append(
            "| `{case_id}` | `{gate_decision}` | `{final_decision}` | {afw_behmatch:.3f} | {prevented} | {abstained} | {counter_authority} | {false_allow} | {false_block} |".format(
                case_id=case["case_id"],
                gate_decision=case["gate_decision"],
                final_decision=case["final_decision"],
                afw_behmatch=case["afw_behmatch"],
                prevented=len(case["prevented_fields"]),
                abstained=len(case.get("abstained_fields", [])),
                counter_authority=int(case.get("counter_authority_events", 0)),
                false_allow=len(case["false_allow_fields"]),
                false_block=len(case["false_block_fields"]),
            )
        )
    lines.append("")
    return "\n".join(lines)


def _append_count_table(
    lines: list[str],
    title: str,
    key_label: str,
    counts: dict[str, Any],
) -> None:
    lines.extend(
        [
            "",
            f"## {title}",
            "",
            f"| {key_label} | Value |",
            "|---|---:|",
        ]
    )
    for name, value in counts.items():
        if isinstance(value, float):
            lines.append(f"| {name} | {value:.3f} |")
        else:
            lines.append(f"| {name} | {int(value)} |")


def _load_case_payloads(run_dir: Path) -> list[dict[str, Any]]:
    case_dir = run_dir / "cases"
    if not case_dir.is_dir():
        raise ValueError(f"AFW runtime run directory has no cases directory: {run_dir}")

    payloads: list[dict[str, Any]] = []
    for path in sorted(case_dir.glob("*.json")):
        with path.open("r", encoding="utf-8") as handle:
            payloads.append(json.load(handle))
    return payloads


def _case_digest(payload: dict[str, Any]) -> dict[str, Any]:
    metrics = payload.get("metrics", {})
    evaluation = payload.get("evaluation") or {}
    final_action = metrics.get("final_action") or {}
    runtime_summary = metrics.get("afw_runtime_summary", {})
    if not isinstance(runtime_summary, dict):
        runtime_summary = {}
    oracle = payload.get("case", {}).get("metadata", {}).get("afw_oracle", {})
    expected_fields = oracle.get("expected_field_decisions", {})
    false_allow_fields = list(metrics.get("afw_runtime_false_allow_fields", []))
    false_block_fields = list(metrics.get("afw_runtime_false_block_fields", []))
    prevented_fields = list(metrics.get("afw_runtime_prevented_fields", []))
    abstained_fields = _list_metric(runtime_summary.get("abstained_fields"))
    counter_authority = metrics.get("afw_counter_authority")
    counter_authority_events = len(counter_authority) if isinstance(counter_authority, list) else 0
    witness_audits = _runtime_witness_audits(metrics)
    primary_witness_audit = witness_audits[0] if witness_audits else {}

    return {
        "case_id": payload.get("case", {}).get("id", "<unknown>"),
        "evaluation_passed": bool(evaluation.get("passed", False)),
        "afw_behmatch": float(metrics.get("afw_behmatch", 0.0)),
        "k1_safe_behavior_match": bool(metrics.get("afw_k1_safe_behavior_match", False)),
        "gate_decision": str(metrics.get("afw_gate_decision", "missing")),
        "final_decision": str(final_action.get("decision", "missing")),
        "total_runtime_fields": int(
            runtime_summary.get("total_fields", 0)
        ),
        "prevented_fields": prevented_fields,
        "abstained_fields": abstained_fields,
        "runtime_field_decision_counts": _field_decision_counts(runtime_summary),
        "counter_authority_events": counter_authority_events,
        "witness_audits": witness_audits,
        "witness_audit": primary_witness_audit,
        "false_allow_fields": false_allow_fields,
        "false_block_fields": false_block_fields,
        "source_types": _case_source_types(payload),
        "expected_allow_fields": sum(
            1 for decision in expected_fields.values() if decision == "allow"
        )
        if isinstance(expected_fields, dict)
        else 0,
    }


def _list_metric(value: Any) -> list[Any]:
    if isinstance(value, list):
        return list(value)
    return []


def _field_decision_counts(runtime_summary: dict[str, Any]) -> dict[str, int]:
    decision_counts = runtime_summary.get("decision_counts", {})
    if not isinstance(decision_counts, dict):
        decision_counts = {}
    return {
        "allow": int(decision_counts.get("allow", 0)),
        "block": int(decision_counts.get("block", 0)),
        "abstain": int(decision_counts.get("abstain", 0)),
    }


def _runtime_witness_audits(metrics: dict[str, Any]) -> list[dict[str, Any]]:
    results = metrics.get("afw_runtime_field_results")
    if not isinstance(results, list):
        return []
    audits: list[dict[str, Any]] = []
    for result in results:
        if not isinstance(result, dict):
            continue
        witness_audit = result.get("witness_audit")
        if isinstance(witness_audit, dict):
            audits.append(dict(witness_audit))
    return audits


def _case_source_types(payload: dict[str, Any]) -> list[str]:
    metadata = payload.get("case", {}).get("metadata", {})
    source_types: set[str] = set()

    capabilities = metadata.get("afw_capabilities", [])
    if isinstance(capabilities, list):
        source_types.update(
            capability["source_type"]
            for capability in capabilities
            if isinstance(capability, dict) and isinstance(capability.get("source_type"), str)
        )

    source_events = metadata.get("afw_source_events", [])
    if isinstance(source_events, list):
        source_types.update(
            source_event["source_type"]
            for source_event in source_events
            if isinstance(source_event, dict) and isinstance(source_event.get("source_type"), str)
        )

    if not source_types:
        capability_sources = payload.get("metrics", {}).get("afw_runtime_capability_sources", [])
        if isinstance(capability_sources, list):
            source_types.update(
                capability["source_type"]
                for capability in capability_sources
                if isinstance(capability, dict) and isinstance(capability.get("source_type"), str)
            )

    source_types = sorted(source_types)
    return list(source_types)


def _count_source_types(cases: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for case in cases:
        for source_type in case["source_types"]:
            counts[source_type] = counts.get(source_type, 0) + 1
    return dict(sorted(counts.items()))


def _runtime_gate_counts(cases: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"allow": 0, "block": 0, "abstain": 0, "missing": 0}
    for case in cases:
        gate = case.get("gate_decision")
        if gate in {"allow", "block", "abstain"}:
            counts[str(gate)] += 1
        else:
            counts["missing"] += 1
    return counts


def _runtime_field_decision_counts(cases: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"allow": 0, "block": 0, "abstain": 0}
    for case in cases:
        decision_counts = case.get("runtime_field_decision_counts", {})
        if not isinstance(decision_counts, dict):
            continue
        for decision in counts:
            counts[decision] += int(decision_counts.get(decision, 0))
    return counts


def _counter_authority_counts(cases: list[dict[str, Any]]) -> dict[str, int]:
    counter_events = [
        int(case.get("counter_authority_events", 0))
        for case in cases
    ]
    return {
        "cases_with_counter_authority": sum(1 for count in counter_events if count > 0),
        "counter_authority_events": sum(counter_events),
    }


def _suite_run_digest(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": summary["run_id"],
        "run_dir": summary["run_dir"],
        "total_cases": summary["total_cases"],
        "passed_cases": summary["passed_cases"],
        "failed_cases": summary["failed_cases"],
        "mean_afw_behmatch": summary["mean_afw_behmatch"],
        "field_counts": summary["field_counts"],
        "runtime_gate_counts": summary.get("runtime_gate_counts", {}),
        "runtime_field_decision_counts": summary.get("runtime_field_decision_counts", {}),
        "counter_authority_counts": summary.get("counter_authority_counts", {}),
        "witness_audit_counts": summary.get("witness_audit_counts", {}),
        "witness_audit_compression": summary.get("witness_audit_compression", {}),
        "trace_adapter_diagnostics": summary.get("trace_adapter_diagnostics", {}),
    }


def _sum_named_counts(
    summaries: list[dict[str, Any]],
    key: str,
    names: tuple[str, ...],
) -> dict[str, int]:
    return {
        name: sum(int(_mapping_value(summary.get(key)).get(name, 0)) for summary in summaries)
        for name in names
    }


def _merge_named_count_key(summaries: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for summary in summaries:
        for name, value in _mapping_value(summary.get(key)).items():
            counts[str(name)] = counts.get(str(name), 0) + int(value)
    return dict(sorted(counts.items()))


def _suite_k_metrics(
    summaries: list[dict[str, Any]],
    field_counts: dict[str, int],
) -> dict[str, float]:
    return {
        "k1_safe_behavior_match_rate": _weighted_metric(
            summaries,
            "k1_safe_behavior_match_rate",
        ),
        "k2_risk_discovery_proxy": _ratio(
            field_counts["prevented_fields"],
            field_counts["prevented_fields"] + field_counts["false_allow_fields"],
        ),
        "k3_safety_issue_reduction_proxy": _ratio(
            field_counts["prevented_fields"],
            field_counts["prevented_fields"] + field_counts["false_allow_fields"],
        ),
        "k4_utility_preservation_proxy": _weighted_metric(
            summaries,
            "k4_utility_preservation_proxy",
        ),
    }


def _weighted_metric(summaries: list[dict[str, Any]], metric: str) -> float:
    return _weighted_mean(
        (
            float(_mapping_value(summary.get("k_metrics")).get(metric, 0.0)),
            int(summary.get("total_cases", 0)),
        )
        for summary in summaries
    )


def _suite_witness_audit_compression(summaries: list[dict[str, Any]]) -> dict[str, float | int]:
    compression_summaries = [
        _mapping_value(summary.get("witness_audit_compression"))
        for summary in summaries
    ]
    witness_counts = [
        int(_mapping_value(summary.get("witness_audit_counts")).get("total_fields_with_witness_audit", 0))
        for summary in summaries
    ]
    return {
        "full_context_capability_count": sum(
            int(compression.get("full_context_capability_count", 0))
            for compression in compression_summaries
        ),
        "witness_capability_count": sum(
            int(compression.get("witness_capability_count", 0))
            for compression in compression_summaries
        ),
        "irrelevant_capability_count": sum(
            int(compression.get("irrelevant_capability_count", 0))
            for compression in compression_summaries
        ),
        "mean_compression_ratio": round(
            _weighted_mean(
                (
                    float(compression.get("mean_compression_ratio", 0.0)),
                    witness_counts[index],
                )
                for index, compression in enumerate(compression_summaries)
            ),
            6,
        ),
    }


def _suite_trace_adapter_diagnostics(summaries: list[dict[str, Any]]) -> dict[str, Any]:
    diagnostics = [_mapping_value(summary.get("trace_adapter_diagnostics")) for summary in summaries]
    invalid_event_reasons: dict[str, int] = {}
    ignored_event_types: dict[str, int] = {}
    for item in diagnostics:
        _merge_count_dict(invalid_event_reasons, item.get("invalid_event_reasons"))
        _merge_count_dict(ignored_event_types, item.get("ignored_event_types"))
    return {
        "cases_with_invalid_trace_schema": sum(
            int(item.get("cases_with_invalid_trace_schema", 0)) for item in diagnostics
        ),
        "invalid_events": sum(int(item.get("invalid_events", 0)) for item in diagnostics),
        "unknown_events": sum(int(item.get("unknown_events", 0)) for item in diagnostics),
        "invalid_event_reasons": dict(sorted(invalid_event_reasons.items())),
        "ignored_event_types": dict(sorted(ignored_event_types.items())),
    }


def _witness_audit_counts(cases: list[dict[str, Any]]) -> dict[str, int]:
    audits = _all_witness_audits(cases)
    return {
        "total_fields_with_witness_audit": len(audits),
        "covers_need_fields": sum(1 for audit in audits if bool(audit.get("covers_need"))),
        "missing_role_fields": sum(1 for audit in audits if _list_metric(audit.get("missing_roles"))),
        "undischarged_obligation_fields": sum(
            1 for audit in audits if _list_metric(audit.get("undischarged_obligations"))
        ),
    }


def _witness_audit_compression(cases: list[dict[str, Any]]) -> dict[str, float | int]:
    audits = _all_witness_audits(cases)
    full_context_count = sum(int(audit.get("full_context_capability_count", 0)) for audit in audits)
    witness_count = sum(int(audit.get("witness_capability_count", 0)) for audit in audits)
    irrelevant_count = sum(int(audit.get("irrelevant_capability_count", 0)) for audit in audits)
    compression_values = [float(audit.get("compression_ratio", 0.0)) for audit in audits]
    return {
        "full_context_capability_count": full_context_count,
        "witness_capability_count": witness_count,
        "irrelevant_capability_count": irrelevant_count,
        "mean_compression_ratio": round(_mean(compression_values), 6),
    }


def _all_witness_audits(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    audits: list[dict[str, Any]] = []
    for case in cases:
        case_audits = case.get("witness_audits", [])
        if isinstance(case_audits, list):
            audits.extend(audit for audit in case_audits if isinstance(audit, dict))
    return audits


def _trace_adapter_diagnostics(payloads: list[dict[str, Any]]) -> dict[str, Any]:
    cases_with_invalid_trace_schema = 0
    invalid_events = 0
    unknown_events = 0
    invalid_event_reasons: dict[str, int] = {}
    ignored_event_types: dict[str, int] = {}

    for payload in payloads:
        diagnostics = payload.get("metrics", {}).get("afw_trace_adapter_diagnostics")
        if not isinstance(diagnostics, dict):
            continue
        if diagnostics.get("schema_contract_status") == "invalid":
            cases_with_invalid_trace_schema += 1
        invalid_events += int(diagnostics.get("invalid_events", 0))
        unknown_events += int(diagnostics.get("unknown_events", 0))
        _merge_count_dict(invalid_event_reasons, diagnostics.get("invalid_event_reasons"))
        _merge_count_dict(ignored_event_types, diagnostics.get("ignored_event_types"))

    return {
        "cases_with_invalid_trace_schema": cases_with_invalid_trace_schema,
        "invalid_events": invalid_events,
        "unknown_events": unknown_events,
        "invalid_event_reasons": dict(sorted(invalid_event_reasons.items())),
        "ignored_event_types": dict(sorted(ignored_event_types.items())),
    }


def _merge_count_dict(target: dict[str, int], value: Any) -> None:
    if not isinstance(value, dict):
        return
    for key, count in value.items():
        if isinstance(key, str):
            target[key] = target.get(key, 0) + int(count)


def _mapping_value(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    return {}


def _mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def _weighted_mean(values: Any) -> float:
    total_weight = 0
    weighted_sum = 0.0
    for value, weight in values:
        total_weight += int(weight)
        weighted_sum += float(value) * int(weight)
    if total_weight == 0:
        return 0.0
    return weighted_sum / total_weight


def _ratio(numerator: int, denominator: int, *, default: float = 0.0) -> float:
    if denominator == 0:
        return default
    return numerator / denominator


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Summarize an AFW runtime FormalTrust run.")
    parser.add_argument("--run-dir", required=True, help="FormalTrust run directory.")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--out", help="Optional output path.")
    args = parser.parse_args(argv)

    summary = build_afw_runtime_run_summary(args.run_dir)
    if args.format == "json":
        rendered = json.dumps(summary, ensure_ascii=False, indent=2)
    else:
        rendered = render_afw_runtime_run_markdown(summary)

    if args.out:
        Path(args.out).write_text(rendered, encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
