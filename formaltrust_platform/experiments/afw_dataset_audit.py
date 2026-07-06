from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence


DEFAULT_PAIRED_ROWS_PATH = Path("examples/afw_power_ops_rag_rows.json")
DEFAULT_RUNTIME_CASES_PATH = Path("examples/data/afw_runtime_power_ops_cases.jsonl")


def build_afw_dataset_annotation_audit(
    *,
    paired_rows_path: str | Path = DEFAULT_PAIRED_ROWS_PATH,
    runtime_cases_path: str | Path = DEFAULT_RUNTIME_CASES_PATH,
) -> dict[str, Any]:
    """Audit whether the AFW power-ops sample slice carries required labels."""

    paired_rows = _load_paired_rows(paired_rows_path)
    runtime_cases = _load_jsonl(runtime_cases_path)
    items = [
        *[_paired_row_item(row) for row in paired_rows],
        *[_runtime_case_item(case) for case in runtime_cases],
    ]
    summary = _summary(items, paired_rows=len(paired_rows), runtime_cases=len(runtime_cases))

    return {
        "artifact_type": "afw_dataset_annotation_audit",
        "inputs": {
            "paired_rows_path": str(Path(paired_rows_path)),
            "runtime_cases_path": str(Path(runtime_cases_path)),
        },
        "summary": summary,
        "source_type_counts": _count_by(items, "source_type"),
        "security_category_counts": _count_by(items, "security_category"),
        "severity_counts": _count_by(items, "severity"),
        "items": items,
    }


def render_afw_dataset_annotation_audit_markdown(audit: dict[str, Any]) -> str:
    lines = [
        "# AFW Dataset Annotation Audit",
        "",
        "## Inputs",
        "",
        "| Item | Value |",
        "|---|---|",
    ]
    for key, value in audit["inputs"].items():
        lines.append(f"| {key} | `{value}` |")

    lines.extend(
        [
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "|---|---:|",
        ]
    )
    for key, value in audit["summary"].items():
        lines.append(f"| {key} | {value} |")

    _append_count_table(lines, "Source Types", "Source type", audit["source_type_counts"])
    _append_count_table(
        lines,
        "Security Categories",
        "Security category",
        audit["security_category_counts"],
    )
    _append_count_table(lines, "Severity", "Severity", audit["severity_counts"])

    lines.extend(
        [
            "",
            "## Kappa Readiness",
            "",
            "| Item | Value |",
            "|---|---|",
            f"| Kappa status | {audit['summary']['kappa_status']} |",
            f"| Dataset scale status | {audit['summary']['dataset_scale_status']} |",
            "",
            "## Items",
            "",
            "| Item | Family | Source | Category | Severity | Expected behavior |",
            "|---|---|---|---|---|---|",
        ]
    )
    for item in audit["items"]:
        lines.append(
            "| `{item_id}` | {sample_family} | `{source_type}` | `{security_category}` | {severity} | {expected_behavior} |".format(
                item_id=item["item_id"],
                sample_family=item["sample_family"],
                source_type=item["source_type"],
                security_category=item["security_category"],
                severity=item["severity"],
                expected_behavior=item["expected_behavior"],
            )
        )

    lines.append("")
    return "\n".join(lines)


def write_afw_dataset_annotation_audit(
    *,
    paired_rows_path: str | Path = DEFAULT_PAIRED_ROWS_PATH,
    runtime_cases_path: str | Path = DEFAULT_RUNTIME_CASES_PATH,
    markdown_path: str | Path,
    json_path: str | Path,
) -> dict[str, Any]:
    audit = build_afw_dataset_annotation_audit(
        paired_rows_path=paired_rows_path,
        runtime_cases_path=runtime_cases_path,
    )
    Path(markdown_path).write_text(
        render_afw_dataset_annotation_audit_markdown(audit),
        encoding="utf-8",
    )
    Path(json_path).write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    return audit


def _load_paired_rows(path: str | Path) -> list[dict[str, Any]]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    return list(payload.get("rows", []))


def _load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _paired_row_item(row: dict[str, Any]) -> dict[str, Any]:
    source = row.get("source", {})
    expected = row.get("expected", {})
    laundered = row.get("laundered_consumption", {})
    legal = row.get("legal_consumption", {})
    field_family = _field_family(str(laundered.get("field", "")))
    legal_decision = expected.get("legal", "")
    laundered_decision = expected.get("laundered", "")

    return {
        "item_id": row.get("row_id", ""),
        "sample_family": "paired_row",
        "sample_origin": row.get("sample_origin") or "manual_seed",
        "source_type": source.get("source_type", "unknown"),
        "security_category": f"field_authority_laundering.{field_family}",
        "severity": _severity_from_field(field_family),
        "expected_behavior": f"legal={legal_decision}; laundered={laundered_decision}",
        "evaluation_standard": (
            "Cap(x) covers Need(s,f); legal consumption must match expected legal "
            "decision; laundered consumption must match expected laundered decision; "
            "no false allow/block."
        ),
        "annotation_basis": {
            "legal_field": legal.get("field", ""),
            "laundered_field": laundered.get("field", ""),
            "legal_required_role": legal.get("need", {}).get("required_role", ""),
            "laundered_required_role": laundered.get("need", {}).get("required_role", ""),
            "expected_reason": expected.get("reason", ""),
        },
    }


def _runtime_case_item(case: dict[str, Any]) -> dict[str, Any]:
    metadata = case.get("metadata", {})
    consumptions = list(metadata.get("afw_consumptions", []))
    source_events = list(metadata.get("afw_source_events", []))
    oracle = metadata.get("afw_oracle", {})
    candidate_action = metadata.get("candidate_action", {})
    field_decisions = dict(oracle.get("expected_field_decisions", {}))
    first_field = next(iter(field_decisions), consumptions[0].get("field", "") if consumptions else "")
    field_family = _field_family(str(first_field))
    source_type = source_events[0].get("source_type", "unknown") if source_events else "unknown"

    return {
        "item_id": case.get("id", ""),
        "sample_family": "runtime_case",
        "sample_origin": "runtime_validation",
        "source_type": source_type,
        "security_category": f"runtime_field_authority.{field_family}",
        "severity": _runtime_severity(candidate_action, field_family),
        "expected_behavior": _runtime_expected_behavior(oracle),
        "evaluation_standard": (
            "AFW runtime evaluator must match afw_oracle expected gate, final "
            "decision, and field decisions; no false allow/block."
        ),
        "annotation_basis": {
            "risk_level": candidate_action.get("risk_level", ""),
            "candidate_decision": candidate_action.get("decision", ""),
            "expected_gate_decision": oracle.get("expected_gate_decision", ""),
            "expected_final_decision": oracle.get("expected_final_decision", ""),
            "expected_field_decisions": field_decisions,
        },
    }


def _runtime_expected_behavior(oracle: dict[str, Any]) -> str:
    field_decisions = dict(oracle.get("expected_field_decisions", {}))
    fields = ",".join(f"{field}:{decision}" for field, decision in sorted(field_decisions.items()))
    return (
        f"gate={oracle.get('expected_gate_decision', '')}; "
        f"final={oracle.get('expected_final_decision', '')}; fields={fields}"
    )


def _summary(items: list[dict[str, Any]], *, paired_rows: int, runtime_cases: int) -> dict[str, Any]:
    annotation_fields = (
        "security_category",
        "severity",
        "expected_behavior",
        "evaluation_standard",
    )
    counts = {
        f"items_with_{field}": sum(1 for item in items if item.get(field))
        for field in annotation_fields
    }
    fully_labeled_items = sum(1 for item in items if all(item.get(field) for field in annotation_fields))
    return {
        "paired_rows": paired_rows,
        "runtime_cases": runtime_cases,
        "total_audited_items": len(items),
        **counts,
        "fully_labeled_items": fully_labeled_items,
        "kappa_status": "pending_human_double_annotation",
        "dataset_scale_status": "afw_specialized_subset_not_full_pdf_scale",
    }


def _field_family(field: str) -> str:
    if field.startswith("requires_human_approval") or "approval" in field:
        return "approval"
    if field.startswith("risk_report"):
        return "risk_report"
    if field.startswith("side_effect"):
        return "side_effect"
    if field.startswith("parameters"):
        return "parameters"
    if field.startswith("data_read_scope"):
        return "data_scope"
    if field.startswith("delegation"):
        return "delegation"
    if field.startswith("answer"):
        return "answer"
    return field or "unknown"


def _severity_from_field(field_family: str) -> str:
    if field_family in {"parameters", "side_effect"}:
        return "critical"
    if field_family in {"approval", "data_scope", "delegation", "risk_level", "risk_report"}:
        return "high"
    if field_family == "answer":
        return "medium"
    return "medium"


def _runtime_severity(candidate_action: dict[str, Any], field_family: str) -> str:
    if field_family in {"parameters", "side_effect"}:
        return "critical"
    risk_level = str(candidate_action.get("risk_level", "")).lower()
    if risk_level in {"critical", "high", "medium", "low"}:
        return risk_level
    return _severity_from_field(field_family)


def _count_by(items: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        value = str(item.get(key) or "unknown")
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def _append_count_table(
    lines: list[str],
    title: str,
    key_label: str,
    counts: dict[str, int],
) -> None:
    lines.extend(["", f"## {title}", "", f"| {key_label} | Count |", "|---|---:|"])
    for key, value in counts.items():
        lines.append(f"| {key} | {value} |")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write AFW dataset annotation audit reports.")
    parser.add_argument("--paired-rows", default=str(DEFAULT_PAIRED_ROWS_PATH))
    parser.add_argument("--runtime-cases", default=str(DEFAULT_RUNTIME_CASES_PATH))
    parser.add_argument(
        "--markdown",
        default="docs/power_ops_afw_dataset_annotation_audit_2026-07-01.md",
    )
    parser.add_argument(
        "--json",
        default="docs/power_ops_afw_dataset_annotation_audit_2026-07-01.json",
    )
    args = parser.parse_args(argv)
    audit = write_afw_dataset_annotation_audit(
        paired_rows_path=args.paired_rows,
        runtime_cases_path=args.runtime_cases,
        markdown_path=args.markdown,
        json_path=args.json,
    )
    print(json.dumps(audit["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
