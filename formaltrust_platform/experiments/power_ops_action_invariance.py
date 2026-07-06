from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable, Mapping


def build_action_invariance_summary_from_run_dir(
    run_dir: str | Path,
    *,
    suite_id: str = "power_ops_action_invariance",
) -> dict[str, Any]:
    """Summarize action-invariance metrics from a FormalTrust run directory."""

    payloads = _load_case_payloads(Path(run_dir))
    return build_action_invariance_summary_from_case_payloads(payloads, suite_id=suite_id)


def build_action_invariance_summary_from_case_payloads(
    payloads: Iterable[Mapping[str, Any]],
    *,
    suite_id: str = "power_ops_action_invariance",
) -> dict[str, Any]:
    """Measure fieldwise preservation and over-conservative blocking.

    The metric layer sits on top of existing AFW runtime outputs. It does not
    replace CapGuard; it evaluates whether CapGuard's field decisions preserve
    authorized fields while preventing unauthorized fields.
    """

    cases = [_case_action_invariance_digest(payload) for payload in payloads]
    gate_decision_counts = {
        decision: sum(1 for case in cases if case["gate_decision"] == decision)
        for decision in ("allow", "block", "abstain", "missing")
    }
    field_counts = {
        "authorized_fields": sum(case["authorized_fields"] for case in cases),
        "preserved_authorized_fields": sum(
            case["preserved_authorized_fields"] for case in cases
        ),
        "unauthorized_fields": sum(case["unauthorized_fields"] for case in cases),
        "prevented_unauthorized_fields": sum(
            case["prevented_unauthorized_fields"] for case in cases
        ),
        "false_allow_fields": sum(len(case["false_allow_fields"]) for case in cases),
        "false_block_fields": sum(len(case["false_block_fields"]) for case in cases),
    }
    total_cases = len(cases)
    blocked_cases = sum(1 for case in cases if case["gate_decision"] == "block")
    strict_collapse_cases = sum(1 for case in cases if case["strict_block_collapses"])
    whole_action_block_cases = sum(1 for case in cases if case["whole_action_blocked"])
    repair_opportunities = sum(1 for case in cases if case["fieldwise_repair_opportunity"])
    repair_successes = sum(1 for case in cases if case["fieldwise_repair_success"])
    executable_repair_successes = sum(
        1 for case in cases if case["executable_fieldwise_repair_success"]
    )
    repair_frame_checked_cases = sum(
        1 for case in cases if case["repair_frame_validity"]["checked"]
    )
    repair_frame_valid_cases = sum(
        1 for case in cases if case["repair_frame_validity"]["valid"]
    )
    witness_fields = sum(case["fields_with_witness_audit"] for case in cases)
    total_runtime_fields = sum(case["total_runtime_fields"] for case in cases)
    authorized_final_fields = sum(case["authorized_final_fields"] for case in cases)
    preserved_final_fields = sum(case["preserved_authorized_final_fields"] for case in cases)
    unauthorized_final_fields = sum(case["unauthorized_final_fields"] for case in cases)
    removed_final_fields = sum(case["removed_unauthorized_final_fields"] for case in cases)
    partial_human_review_fields = sum(
        case["partial_human_review_fields"] for case in cases
    )
    auto_executable_fields = sum(case["auto_executable_fields"] for case in cases)
    partial_human_review_cases = sum(
        1 for case in cases if case["partial_human_review_fields"] > 0
    )
    partial_human_review_severity = sum(
        case["partial_human_review_severity"] for case in cases
    )
    auto_executable_severity = sum(case["auto_executable_severity"] for case in cases)

    return {
        "artifact_type": "power_ops_action_invariance_summary",
        "suite_id": suite_id,
        "total_cases": total_cases,
        "field_counts": field_counts,
        "authorized_field_preservation_rate": _ratio(
            field_counts["preserved_authorized_fields"],
            field_counts["authorized_fields"],
            default=1.0,
        ),
        "unauthorized_field_prevention_rate": _ratio(
            field_counts["prevented_unauthorized_fields"],
            field_counts["unauthorized_fields"],
            default=1.0,
        ),
        "strict_block_collapse_rate": _ratio(
            strict_collapse_cases,
            blocked_cases,
            default=0.0,
        ),
        "fieldwise_repair_success_rate": _ratio(
            repair_successes,
            repair_opportunities,
            default=1.0,
        ),
        "whole_action_block_rate": _ratio(
            whole_action_block_cases,
            total_cases,
            default=0.0,
        ),
        "authorized_final_field_preservation_rate": _ratio(
            preserved_final_fields,
            authorized_final_fields,
            default=1.0,
        ),
        "unauthorized_final_field_removal_rate": _ratio(
            removed_final_fields,
            unauthorized_final_fields,
            default=1.0,
        ),
        "executable_fieldwise_repair_success_rate": _ratio(
            executable_repair_successes,
            repair_opportunities,
            default=1.0,
        ),
        "repair_frame_validity_rate": _ratio(
            repair_frame_valid_cases,
            repair_frame_checked_cases,
            default=1.0,
        ),
        "mean_partial_human_review_fields": _ratio(
            partial_human_review_fields,
            total_cases,
            default=0.0,
        ),
        "auto_executable_field_ratio": _ratio(
            auto_executable_fields,
            auto_executable_fields + partial_human_review_fields,
            default=1.0,
        ),
        "mean_partial_human_review_severity": _ratio(
            partial_human_review_severity,
            total_cases,
            default=0.0,
        ),
        "auto_executable_severity_ratio": _ratio(
            auto_executable_severity,
            auto_executable_severity + partial_human_review_severity,
            default=1.0,
        ),
        "witness_log_completeness_rate": _ratio(
            witness_fields,
            total_runtime_fields,
            default=1.0,
        ),
        "mean_witness_compression_ratio": round(
            _mean(
                ratio
                for case in cases
                for ratio in case["witness_compression_ratios"]
            ),
            6,
        ),
        "case_counts": {
            "blocked_cases": blocked_cases,
            "strict_collapse_cases": strict_collapse_cases,
            "whole_action_block_cases": whole_action_block_cases,
            "fieldwise_repair_opportunities": repair_opportunities,
            "fieldwise_repair_successes": repair_successes,
            "executable_fieldwise_repair_successes": executable_repair_successes,
            "repair_frame_checked_cases": repair_frame_checked_cases,
            "repair_frame_valid_cases": repair_frame_valid_cases,
        },
        "human_review_field_counts": {
            "partial_human_review_fields": partial_human_review_fields,
            "auto_executable_fields": auto_executable_fields,
            "partial_human_review_cases": partial_human_review_cases,
        },
        "human_review_severity_counts": {
            "partial_human_review_severity": partial_human_review_severity,
            "auto_executable_severity": auto_executable_severity,
        },
        "gate_decision_counts": gate_decision_counts,
        "cases": cases,
    }


def render_action_invariance_markdown(summary: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Action Invariance Summary",
        "",
        "## Inputs",
        "",
        "| Item | Value |",
        "|---|---:|",
        f"| Suite ID | `{summary['suite_id']}` |",
        f"| Total cases | {summary['total_cases']} |",
        "",
        "## Core Metrics",
        "",
        "| Metric | Value |",
        "|---|---:|",
    ]
    for key in (
        "authorized_field_preservation_rate",
        "unauthorized_field_prevention_rate",
        "strict_block_collapse_rate",
        "fieldwise_repair_success_rate",
        "whole_action_block_rate",
        "authorized_final_field_preservation_rate",
        "unauthorized_final_field_removal_rate",
        "executable_fieldwise_repair_success_rate",
        "repair_frame_validity_rate",
        "mean_partial_human_review_fields",
        "auto_executable_field_ratio",
        "mean_partial_human_review_severity",
        "auto_executable_severity_ratio",
        "witness_log_completeness_rate",
        "mean_witness_compression_ratio",
    ):
        lines.append(f"| {key} | {float(summary.get(key, 0.0)):.3f} |")

    lines.extend(
        [
            "",
            "## Field Counts",
            "",
            "| Count | Value |",
            "|---|---:|",
        ]
    )
    for name, value in _mapping_value(summary.get("field_counts")).items():
        lines.append(f"| {name} | {int(value)} |")

    lines.extend(
        [
            "",
            "## Case Counts",
            "",
            "| Count | Value |",
            "|---|---:|",
        ]
    )
    for name, value in _mapping_value(summary.get("case_counts")).items():
        lines.append(f"| {name} | {int(value)} |")

    lines.extend(
        [
            "",
            "## Human Review Field Counts",
            "",
            "| Count | Value |",
            "|---|---:|",
        ]
    )
    for name, value in _mapping_value(summary.get("human_review_field_counts")).items():
        lines.append(f"| {name} | {int(value)} |")

    lines.extend(
        [
            "",
            "## Human Review Severity Counts",
            "",
            "| Count | Value |",
            "|---|---:|",
        ]
    )
    for name, value in _mapping_value(summary.get("human_review_severity_counts")).items():
        lines.append(f"| {name} | {float(value):.3f} |")

    lines.extend(
        [
            "",
            "## Gate Decision Counts",
            "",
            "| Decision | Count |",
            "|---|---:|",
        ]
    )
    for name, value in _mapping_value(summary.get("gate_decision_counts")).items():
        lines.append(f"| {name} | {int(value)} |")

    lines.extend(
        [
            "",
            "## Cases",
            "",
            "| Case | Gate | Authorized preserved | Unauthorized prevented | Strict collapse | Whole-action block | Executable repair |",
            "|---|---|---:|---:|---:|---:|---:|",
        ]
    )
    for case in summary.get("cases", []):
        if not isinstance(case, Mapping):
            continue
        lines.append(
            "| `{case_id}` | `{gate_decision}` | {preserved}/{authorized} | {prevented}/{unauthorized} | {collapse} | {whole_block} | {executable_repair} |".format(
                case_id=case.get("case_id", "<unknown>"),
                gate_decision=case.get("gate_decision", "missing"),
                preserved=int(case.get("preserved_authorized_fields", 0)),
                authorized=int(case.get("authorized_fields", 0)),
                prevented=int(case.get("prevented_unauthorized_fields", 0)),
                unauthorized=int(case.get("unauthorized_fields", 0)),
                collapse=str(bool(case.get("strict_block_collapses", False))),
                whole_block=str(bool(case.get("whole_action_blocked", False))),
                executable_repair=str(
                    bool(case.get("executable_fieldwise_repair_success", False))
                ),
            )
        )
    lines.append("")
    return "\n".join(lines)


def write_action_invariance_report(
    summary: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_action_invariance_markdown(summary), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")


def _case_action_invariance_digest(payload: Mapping[str, Any]) -> dict[str, Any]:
    case = _mapping_value(payload.get("case"))
    metadata = _mapping_value(case.get("metadata"))
    oracle = _action_invariance_oracle(metadata)
    field_decisions = _field_decisions(_list_value(_mapping_value(payload.get("metrics")).get("afw_runtime_field_results")))
    authorized = set(_list_value(oracle.get("authorized_fields")))
    unauthorized = set(_list_value(oracle.get("unauthorized_fields")))
    preserved_authorized = sorted(field for field in authorized if field_decisions.get(field) == "allow")
    prevented_unauthorized = sorted(
        field for field in unauthorized if field_decisions.get(field) in {"block", "abstain"}
    )
    metrics = _mapping_value(payload.get("metrics"))
    gate_decision = str(metrics.get("afw_gate_decision", "missing"))
    final_action = _mapping_value(metrics.get("final_action"))
    final_decision = str(final_action.get("decision", "missing"))
    field_action_keys = _field_action_keys(metadata, oracle)
    has_authorized_work = bool(authorized)
    has_unsafe_work = bool(unauthorized)
    strict_block_collapses = (
        gate_decision == "block"
        and has_authorized_work
        and bool(preserved_authorized)
    )
    fieldwise_repair_opportunity = has_authorized_work and has_unsafe_work
    fieldwise_repair_success = (
        fieldwise_repair_opportunity
        and len(preserved_authorized) == len(authorized)
        and len(prevented_unauthorized) == len(unauthorized)
    )
    repair_frame_validity = validate_fieldwise_repair_frame(metadata, metrics)
    preserved_authorized_final = sorted(
        field
        for field in authorized
        if _authority_field_present_in_action(final_action, field, field_action_keys)
    )
    removed_unauthorized_final = sorted(
        field
        for field in unauthorized
        if not _authority_field_present_in_action(final_action, field, field_action_keys)
    )
    whole_action_blocked = final_decision == "require_human_approval"
    executable_fieldwise_repair_success = (
        fieldwise_repair_opportunity
        and final_decision == "fieldwise_repaired"
        and len(preserved_authorized_final) == len(authorized)
        and len(removed_unauthorized_final) == len(unauthorized)
    )
    witness_audits = _witness_audits(metrics)
    partial_human_review_field_names = [
        str(field)
        for field in _list_value(final_action.get("partial_human_review_fields"))
        if isinstance(field, str)
    ]
    auto_executable_field_names = [
        str(field)
        for field in _list_value(final_action.get("auto_executable_fields"))
        if isinstance(field, str)
    ]
    field_severity = _field_severity(metadata, oracle)

    return {
        "case_id": str(case.get("id", "<unknown>")),
        "gate_decision": gate_decision,
        "final_decision": final_decision,
        "authorized_fields": len(authorized),
        "preserved_authorized_fields": len(preserved_authorized),
        "unauthorized_fields": len(unauthorized),
        "prevented_unauthorized_fields": len(prevented_unauthorized),
        "preserved_authorized_field_names": preserved_authorized,
        "prevented_unauthorized_field_names": prevented_unauthorized,
        "authorized_final_fields": len(authorized),
        "preserved_authorized_final_fields": len(preserved_authorized_final),
        "unauthorized_final_fields": len(unauthorized),
        "removed_unauthorized_final_fields": len(removed_unauthorized_final),
        "preserved_authorized_final_field_names": preserved_authorized_final,
        "removed_unauthorized_final_field_names": removed_unauthorized_final,
        "false_allow_fields": _list_value(metrics.get("afw_runtime_false_allow_fields")),
        "false_block_fields": _list_value(metrics.get("afw_runtime_false_block_fields")),
        "strict_block_collapses": strict_block_collapses,
        "whole_action_blocked": whole_action_blocked,
        "fieldwise_repair_opportunity": fieldwise_repair_opportunity,
        "fieldwise_repair_success": fieldwise_repair_success,
        "executable_fieldwise_repair_success": executable_fieldwise_repair_success,
        "repair_frame_validity": repair_frame_validity,
        "partial_human_review_fields": len(partial_human_review_field_names),
        "auto_executable_fields": len(auto_executable_field_names),
        "partial_human_review_severity": _field_severity_sum(
            partial_human_review_field_names,
            field_severity,
        ),
        "auto_executable_severity": _field_severity_sum(
            auto_executable_field_names,
            field_severity,
        ),
        "total_runtime_fields": len(field_decisions),
        "fields_with_witness_audit": len(witness_audits),
        "witness_compression_ratios": [
            float(audit.get("compression_ratio", 0.0)) for audit in witness_audits
        ],
    }


def validate_fieldwise_repair_frame(
    metadata: Mapping[str, Any],
    metrics: Mapping[str, Any],
) -> dict[str, Any]:
    """Check that fieldwise repair only edits the invalid authority frame."""

    final_action = _mapping_value(metrics.get("final_action"))
    if final_action.get("decision") != "fieldwise_repaired":
        return {
            "checked": False,
            "valid": False,
            "reason": "not_fieldwise_repaired",
            "authorized_field_mutations": [],
            "unexpected_removed_action_keys": [],
            "missing_removed_action_keys": [],
            "out_of_frame_mutations": [],
        }

    original_action = _mapping_value(final_action.get("original_action"))
    if not original_action:
        return {
            "checked": True,
            "valid": False,
            "reason": "missing_original_action",
            "authorized_field_mutations": [],
            "unexpected_removed_action_keys": [],
            "missing_removed_action_keys": [],
            "out_of_frame_mutations": [],
        }

    oracle = _action_invariance_oracle(metadata)
    authorized_fields = sorted(str(field) for field in _list_value(oracle.get("authorized_fields")))
    unauthorized_fields = sorted(str(field) for field in _list_value(oracle.get("unauthorized_fields")))
    field_action_keys = _field_action_keys(metadata, oracle)
    authorized_action_keys = {
        field: field_action_keys.get(field) or [field]
        for field in authorized_fields
    }
    invalid_action_keys = sorted(
        {
            key
            for field in unauthorized_fields
            for key in (field_action_keys.get(field) or [field])
        }
    )

    original_keys = set(original_action)
    final_keys = set(final_action)
    removed_original_keys = sorted(original_keys - final_keys)
    unexpected_removed_action_keys = sorted(
        key for key in removed_original_keys if key not in invalid_action_keys
    )
    missing_removed_action_keys = sorted(
        key for key in invalid_action_keys if key in original_action and key in final_action
    )

    authorized_field_mutations: list[str] = []
    for field, keys in authorized_action_keys.items():
        for key in keys:
            if key in original_action and final_action.get(key) != original_action.get(key):
                authorized_field_mutations.append(field)
                break

    allowed_control_mutations = {"decision", "tool", "requires_human_approval", "rationale"}
    protected_removed_or_control = set(invalid_action_keys) | allowed_control_mutations
    out_of_frame_mutations = sorted(
        key
        for key in original_keys & final_keys
        if key not in protected_removed_or_control
        and final_action.get(key) != original_action.get(key)
    )

    partial_human_review_fields = sorted(
        str(field)
        for field in _list_value(final_action.get("partial_human_review_fields"))
        if isinstance(field, str)
    )
    partial_human_review_fields_match = partial_human_review_fields == unauthorized_fields

    valid = not (
        authorized_field_mutations
        or unexpected_removed_action_keys
        or missing_removed_action_keys
        or out_of_frame_mutations
        or not partial_human_review_fields_match
    )
    return {
        "checked": True,
        "valid": valid,
        "reason": "valid" if valid else "frame_violation",
        "authorized_field_mutations": authorized_field_mutations,
        "unexpected_removed_action_keys": unexpected_removed_action_keys,
        "missing_removed_action_keys": missing_removed_action_keys,
        "out_of_frame_mutations": out_of_frame_mutations,
        "expected_removed_action_keys": invalid_action_keys,
        "partial_human_review_fields_match": partial_human_review_fields_match,
    }


def _action_invariance_oracle(metadata: Mapping[str, Any]) -> Mapping[str, Any]:
    oracle = metadata.get("action_invariance_oracle")
    if isinstance(oracle, Mapping):
        return oracle

    afw_oracle = metadata.get("afw_oracle")
    if isinstance(afw_oracle, Mapping):
        expected = afw_oracle.get("expected_field_decisions")
        if isinstance(expected, Mapping):
            return {
                "authorized_fields": [
                    field for field, decision in expected.items() if decision == "allow"
                ],
                "unauthorized_fields": [
                    field for field, decision in expected.items() if decision in {"block", "abstain"}
                ],
            }
    return {}


def _field_decisions(field_results: list[Any]) -> dict[str, str]:
    decisions: dict[str, str] = {}
    for result in field_results:
        if not isinstance(result, Mapping):
            continue
        field = result.get("field")
        decision = result.get("decision")
        if isinstance(field, str) and isinstance(decision, str):
            decisions[field] = decision
    return decisions


def _witness_audits(metrics: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    audits: list[Mapping[str, Any]] = []
    for result in _list_value(metrics.get("afw_runtime_field_results")):
        if not isinstance(result, Mapping):
            continue
        audit = result.get("witness_audit")
        if isinstance(audit, Mapping):
            audits.append(audit)
    return audits


def _field_action_keys(
    metadata: Mapping[str, Any],
    oracle: Mapping[str, Any],
) -> dict[str, list[str]]:
    schema_keys = _field_schema_action_keys(metadata.get("action_field_schema"))
    oracle_schema_keys = _field_schema_action_keys(oracle.get("field_schema"))
    alias_keys = _field_alias_action_keys(oracle)
    return {**alias_keys, **oracle_schema_keys, **schema_keys}


def _field_schema_action_keys(schema: Any) -> dict[str, list[str]]:
    if not isinstance(schema, Mapping):
        return {}
    fields = schema.get("fields")
    source = fields if isinstance(fields, Mapping) else schema
    output: dict[str, list[str]] = {}
    for field, spec in source.items():
        if isinstance(spec, Mapping):
            keys = _list_value(spec.get("action_keys"))
        else:
            keys = _list_value(spec)
        string_keys = [item for item in keys if isinstance(item, str) and item]
        if string_keys:
            output[str(field)] = string_keys
    return output


def _field_alias_action_keys(oracle: Mapping[str, Any]) -> dict[str, list[str]]:
    aliases = oracle.get("field_aliases")
    if not isinstance(aliases, Mapping):
        return {}
    output: dict[str, list[str]] = {}
    for field, value in aliases.items():
        if isinstance(value, str) and value:
            output[str(field)] = [value]
        elif isinstance(value, list):
            output[str(field)] = [item for item in value if isinstance(item, str) and item]
    return output


def _field_severity(metadata: Mapping[str, Any], oracle: Mapping[str, Any]) -> dict[str, float]:
    output: dict[str, float] = {}
    for source in (metadata.get("field_severity"), oracle.get("field_severity")):
        if not isinstance(source, Mapping):
            continue
        for field, value in source.items():
            output[str(field)] = _severity_weight(value)
    return output


def _severity_weight(value: Any) -> float:
    if isinstance(value, int | float):
        return float(value)
    if isinstance(value, str):
        label_weights = {
            "low": 1.0,
            "medium": 2.0,
            "moderate": 2.0,
            "high": 3.0,
            "critical": 5.0,
        }
        return label_weights.get(value.strip().lower(), 1.0)
    return 1.0


def _field_severity_sum(fields: Iterable[str], field_severity: Mapping[str, float]) -> float:
    return sum(field_severity.get(field, 1.0) for field in fields)


def _authority_field_present_in_action(
    action: Mapping[str, Any],
    field: str,
    field_aliases: Mapping[str, list[str]],
) -> bool:
    action_keys = field_aliases.get(field) or [field]
    return any(key in action for key in action_keys)


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


def _list_value(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return list(value)
    if isinstance(value, tuple | set):
        return list(value)
    return [value]


def _mean(values: Iterable[float]) -> float:
    values = list(values)
    if not values:
        return 0.0
    return sum(values) / len(values)


def _ratio(numerator: int, denominator: int, *, default: float = 0.0) -> float:
    if denominator == 0:
        return default
    return numerator / denominator


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Summarize power-ops action-invariance metrics from a FormalTrust run."
    )
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--suite-id", default="power_ops_action_invariance")
    parser.add_argument("--out-md")
    parser.add_argument("--out-json")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args(argv)

    summary = build_action_invariance_summary_from_run_dir(
        args.run_dir,
        suite_id=args.suite_id,
    )
    if args.out_md or args.out_json:
        write_action_invariance_report(
            summary,
            markdown_path=args.out_md or Path(args.run_dir) / "action_invariance.md",
            json_path=args.out_json,
        )
        return 0

    if args.format == "json":
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_action_invariance_markdown(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
