from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable, Mapping


def audit_power_ops_action_invariance_dataset(dataset_path: str | Path) -> dict[str, Any]:
    """Audit coverage for a power-ops action-invariance JSONL dataset."""

    cases = _load_jsonl(Path(dataset_path))
    total_cases = len(cases)
    source_type_counts: dict[str, int] = {}
    gate_decision_counts: dict[str, int] = {}
    field_counts: dict[str, int] = {}
    role_counts: dict[str, int] = {}
    tag_counts: dict[str, int] = {}
    severity_counts: dict[str, int] = {}
    risk_level_counts: dict[str, int] = {}
    case_shape_counts = {
        "candidate_action": 0,
        "afw_source_events": 0,
        "afw_consumptions": 0,
        "afw_oracle": 0,
        "action_invariance_oracle": 0,
    }
    oracle_covered_cases = 0
    authorized_fields = 0
    unauthorized_fields = 0

    for case in cases:
        metadata = _mapping_value(case.get("metadata"))
        for tag in _list_value(case.get("tags")):
            if isinstance(tag, str):
                _increment(tag_counts, tag)

        candidate_action = _mapping_value(metadata.get("candidate_action"))
        if candidate_action:
            case_shape_counts["candidate_action"] += 1
            _increment(risk_level_counts, str(candidate_action.get("risk_level", "missing")))

        source_events = [
            event for event in _list_value(metadata.get("afw_source_events")) if isinstance(event, Mapping)
        ]
        if source_events:
            case_shape_counts["afw_source_events"] += 1
        for event in source_events:
            _increment(source_type_counts, str(event.get("source_type", "missing")))

        consumptions = [
            item for item in _list_value(metadata.get("afw_consumptions")) if isinstance(item, Mapping)
        ]
        if consumptions:
            case_shape_counts["afw_consumptions"] += 1
        for consumption in consumptions:
            field = consumption.get("field")
            if isinstance(field, str):
                _increment(field_counts, field)
            need = _mapping_value(consumption.get("need"))
            role = need.get("required_role")
            if isinstance(role, str):
                _increment(role_counts, role)

        afw_oracle = _mapping_value(metadata.get("afw_oracle"))
        if afw_oracle:
            case_shape_counts["afw_oracle"] += 1
        gate = afw_oracle.get("expected_gate_decision")
        if isinstance(gate, str):
            _increment(gate_decision_counts, gate)

        action_oracle = _mapping_value(metadata.get("action_invariance_oracle"))
        if action_oracle:
            case_shape_counts["action_invariance_oracle"] += 1
        auth = [field for field in _list_value(action_oracle.get("authorized_fields")) if isinstance(field, str)]
        unauth = [
            field for field in _list_value(action_oracle.get("unauthorized_fields")) if isinstance(field, str)
        ]
        authorized_fields += len(auth)
        unauthorized_fields += len(unauth)
        if afw_oracle and action_oracle and auth and unauth:
            oracle_covered_cases += 1

        for severity in _field_severity_values(metadata, action_oracle):
            _increment(severity_counts, severity)

    return {
        "artifact_type": "power_ops_action_invariance_dataset_audit",
        "dataset_path": str(Path(dataset_path)),
        "total_cases": total_cases,
        "case_shape_counts": case_shape_counts,
        "oracle_covered_cases": oracle_covered_cases,
        "oracle_coverage_rate": _ratio(oracle_covered_cases, total_cases, default=0.0),
        "source_type_counts": source_type_counts,
        "gate_decision_counts": gate_decision_counts,
        "field_counts": field_counts,
        "required_role_counts": role_counts,
        "tag_counts": tag_counts,
        "severity_counts": severity_counts,
        "risk_level_counts": risk_level_counts,
        "authorized_fields": authorized_fields,
        "unauthorized_fields": unauthorized_fields,
    }


def render_dataset_audit_markdown(audit: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Action Invariance Dataset Audit",
        "",
        "## Inputs",
        "",
        "| Item | Value |",
        "|---|---:|",
        f"| Dataset | `{audit['dataset_path']}` |",
        f"| Total cases | {audit['total_cases']} |",
        f"| Oracle coverage rate | {float(audit['oracle_coverage_rate']):.3f} |",
        f"| Authorized fields | {audit['authorized_fields']} |",
        f"| Unauthorized fields | {audit['unauthorized_fields']} |",
    ]
    for title, key in (
        ("Case Shape Counts", "case_shape_counts"),
        ("Gate Decision Counts", "gate_decision_counts"),
        ("Source Type Counts", "source_type_counts"),
        ("Field Counts", "field_counts"),
        ("Required Role Counts", "required_role_counts"),
        ("Severity Counts", "severity_counts"),
        ("Risk Level Counts", "risk_level_counts"),
        ("Tag Counts", "tag_counts"),
    ):
        lines.extend(["", f"## {title}", "", "| Key | Count |", "|---|---:|"])
        for name, value in sorted(_mapping_value(audit.get(key)).items()):
            lines.append(f"| `{name}` | {int(value)} |")
    lines.append("")
    return "\n".join(lines)


def write_dataset_audit_report(
    audit: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    md_path = Path(markdown_path)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(render_dataset_audit_markdown(audit), encoding="utf-8")
    if json_path is not None:
        json_out = Path(json_path)
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")


def _field_severity_values(
    metadata: Mapping[str, Any],
    oracle: Mapping[str, Any],
) -> list[str]:
    labels: list[str] = []
    for source in (metadata.get("field_severity"), oracle.get("field_severity")):
        if not isinstance(source, Mapping):
            continue
        for value in source.values():
            if isinstance(value, str):
                labels.append(value.strip().lower() or "missing")
            elif isinstance(value, int | float):
                labels.append(str(value))
            else:
                labels.append("missing")
    return labels


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            payload = json.loads(stripped)
            if not isinstance(payload, dict):
                raise ValueError(f"{path}:{line_no} is not a JSON object")
            cases.append(payload)
    return cases


def _increment(counts: dict[str, int], key: str) -> None:
    counts[key] = counts.get(key, 0) + 1


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


def _ratio(numerator: int, denominator: int, *, default: float = 0.0) -> float:
    if denominator == 0:
        return default
    return numerator / denominator


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit coverage for a power-ops action-invariance JSONL dataset."
    )
    parser.add_argument("dataset_path")
    parser.add_argument("--out-md")
    parser.add_argument("--out-json")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args(argv)

    audit = audit_power_ops_action_invariance_dataset(args.dataset_path)
    if args.out_md or args.out_json:
        write_dataset_audit_report(
            audit,
            markdown_path=args.out_md or Path(args.dataset_path).with_suffix(".audit.md"),
            json_path=args.out_json,
        )
        return 0

    if args.format == "json":
        print(json.dumps(audit, ensure_ascii=False, indent=2))
    else:
        print(render_dataset_audit_markdown(audit))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
