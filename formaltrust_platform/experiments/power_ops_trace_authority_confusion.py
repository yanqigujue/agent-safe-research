from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any, Mapping

from formaltrust_platform.experiments.afw_bench import (
    evaluate_authority_consumptions,
    evaluate_paired_rows,
)


SCOPE_KEYS = ("data_scope", "effect_scope", "delegation_scope", "time_scope")


def build_trace_authority_confusion_summary(
    *,
    fixture_path: str | Path,
    rows_out_path: str | Path | None = None,
    suite_id: str = "power_ops_trace_authority_confusion",
) -> dict[str, Any]:
    fixture = Path(fixture_path)
    cases = _load_cases(fixture)
    rows = generate_trace_authority_confusion_rows(cases)

    if rows_out_path is not None:
        write_trace_authority_confusion_rows(
            rows,
            fixture_path=fixture,
            rows_path=rows_out_path,
            source_case_count=len(cases),
        )

    capguard_summary = evaluate_paired_rows(rows, baseline="capguard")
    boundary_summary = evaluate_paired_rows(rows, baseline="boundary_scope_only")

    return {
        "artifact_type": "power_ops_trace_authority_confusion_summary",
        "suite_id": suite_id,
        "source_fixture_path": str(fixture),
        "source_case_count": len(cases),
        "generated_rows_path": str(rows_out_path) if rows_out_path is not None else "",
        "generated_row_count": len(rows),
        "legal_row_count": sum(1 for row in rows if row.get("expected", {}).get("legal") == "allow"),
        "authority_confusion_row_count": sum(
            1
            for row in rows
            if row.get("confusion_type") == "boundary_preserving_semantic_role_mutation"
        ),
        "boundary_preserved_row_count": sum(1 for row in rows if row.get("boundary_preserved")),
        "mutated_required_role_only_count": sum(
            1 for row in rows if row.get("mutated_need_fields") == ["required_role"]
        ),
        "capguard_legal_preservation_rate": float(
            capguard_summary.get("legal_preservation_rate", 0.0) or 0.0
        ),
        "capguard_confusion_block_rate": float(
            capguard_summary.get("laundering_block_rate", 0.0) or 0.0
        ),
        "capguard_false_allow_rate": float(capguard_summary.get("false_allow_rate", 0.0) or 0.0),
        "boundary_scope_only_false_allow_rate": float(
            boundary_summary.get("false_allow_rate", 0.0) or 0.0
        ),
        "capguard_summary": capguard_summary,
        "boundary_scope_only_summary": boundary_summary,
        "rows_digest": _rows_digest(rows),
    }


def generate_trace_authority_confusion_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        case_id = str(case.get("id", "<unknown-case>"))
        events = _trace_events(case)
        source_events = _source_events(events)
        capabilities = {
            source_id: capability
            for source_id, capability in (
                _capability_from_source_event(source_event) for source_event in source_events
            )
            if source_id
        }
        for consumption in _authority_consumptions(events):
            attributed_source_id = str(consumption.get("attributed_source_id", ""))
            capability = capabilities.get(attributed_source_id)
            if capability is None:
                continue
            if not _consumption_is_allowed_by_capability(capability, consumption):
                continue
            row = _authority_confusion_row(
                case_id=case_id,
                capability=capability,
                source_event=_source_event_by_id(source_events, attributed_source_id),
                legal_consumption=consumption,
            )
            rows.append(row)
    return rows


def write_trace_authority_confusion_rows(
    rows: list[dict[str, Any]],
    *,
    fixture_path: str | Path,
    rows_path: str | Path,
    source_case_count: int,
) -> None:
    target = Path(rows_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "artifact_type": "power_ops_trace_authority_confusion_rows",
        "source_fixture_path": str(fixture_path),
        "source_case_count": source_case_count,
        "generated_row_count": len(rows),
        "rows": rows,
    }
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def render_trace_authority_confusion_markdown(summary: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Trace-Derived Authority-Confusion Summary",
        "",
        "This artifact generates boundary-preserving role-confusion rows from legal trace consumptions.",
        "",
        "## Inputs",
        "",
        "| Item | Value |",
        "|---|---:|",
        f"| Suite ID | `{summary.get('suite_id', '')}` |",
        f"| Source cases | {int(summary.get('source_case_count', 0) or 0)} |",
        f"| Generated rows | {int(summary.get('generated_row_count', 0) or 0)} |",
        f"| Rows artifact | `{summary.get('generated_rows_path', '')}` |",
        "",
        "## Boundary-Preserving Mutation Check",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| authority_confusion_row_count | {int(summary.get('authority_confusion_row_count', 0) or 0)} |",
        f"| boundary_preserved_row_count | {int(summary.get('boundary_preserved_row_count', 0) or 0)} |",
        f"| mutated_required_role_only_count | {int(summary.get('mutated_required_role_only_count', 0) or 0)} |",
        "",
        "## Baseline Readback",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| capguard_legal_preservation_rate | {float(summary.get('capguard_legal_preservation_rate', 0.0) or 0.0):.3f} |",
        f"| capguard_confusion_block_rate | {float(summary.get('capguard_confusion_block_rate', 0.0) or 0.0):.3f} |",
        f"| capguard_false_allow_rate | {float(summary.get('capguard_false_allow_rate', 0.0) or 0.0):.3f} |",
        f"| boundary_scope_only_false_allow_rate | {float(summary.get('boundary_scope_only_false_allow_rate', 0.0) or 0.0):.3f} |",
        "",
        "## Rows",
        "",
        "| Row | Source type | Field | Legal role | Confused role |",
        "|---|---|---|---|---|",
    ]
    for row in _list_value(summary.get("rows_digest")):
        if not isinstance(row, Mapping):
            continue
        lines.append(
            "| `{row_id}` | {source_type} | `{field}` | `{legal_role}` | `{confused_role}` |".format(
                row_id=row.get("row_id", "<unknown>"),
                source_type=row.get("source_type", "<unknown>"),
                field=row.get("field", "<unknown>"),
                legal_role=row.get("legal_required_role", "<missing>"),
                confused_role=row.get("confused_required_role", "<missing>"),
            )
        )
    lines.append("")
    return "\n".join(lines)


def write_trace_authority_confusion_report(
    summary: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_trace_authority_confusion_markdown(summary), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")


def _load_cases(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if isinstance(payload, list):
        return [dict(case) for case in payload if isinstance(case, Mapping)]
    if isinstance(payload, Mapping):
        cases = payload.get("cases", [])
        if isinstance(cases, list):
            return [dict(case) for case in cases if isinstance(case, Mapping)]
    raise ValueError("Power-Ops trace fixture must be a case list or contain a 'cases' list")


def _trace_events(case: Mapping[str, Any]) -> list[dict[str, Any]]:
    metadata = case.get("metadata", {})
    if not isinstance(metadata, Mapping):
        return []
    events = metadata.get("agent_trace_events", [])
    if not isinstance(events, list):
        return []
    return [dict(event) for event in events if isinstance(event, Mapping)]


def _source_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [event for event in events if event.get("event_type") == "source_event"]


def _authority_consumptions(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [event for event in events if event.get("event_type") == "authority_consumption"]


def _source_event_by_id(source_events: list[dict[str, Any]], source_id: str) -> dict[str, Any]:
    for source_event in source_events:
        if source_event.get("source_id") == source_id:
            return source_event
    return {"source_id": source_id, "source_type": "unknown"}


def _capability_from_source_event(source_event: Mapping[str, Any]) -> tuple[str, dict[str, Any] | None]:
    source_id = str(source_event.get("source_id", ""))
    if not source_id:
        return "", None

    manifest, inferred_from = _source_manifest(source_event)
    if manifest is None:
        return source_id, None

    roles = _first_list(manifest, "semantic_roles", "output_semantic_roles")
    fields = _first_list(manifest, "fields", "allowed_fields")
    operations = _first_list(manifest, "operations", "allowed_operations")
    if not roles or not fields or not operations:
        return source_id, None

    capability = {
        "source_id": source_id,
        "semantic_roles": roles,
        "fields": fields,
        "operations": operations,
        "data_scope": _first_list(manifest, "data_scope", "allowed_data_scope"),
        "effect_scope": _first_list(manifest, "effect_scope", "allowed_effect_scope"),
        "delegation_scope": _first_list(manifest, "delegation_scope", "allowed_delegation_scope"),
        "time_scope": _first_list(manifest, "time_scope", "allowed_time_scope"),
        "obligations": _first_list(manifest, "obligations", "output_obligations"),
        "inferred_from": inferred_from,
    }
    return source_id, capability


def _source_manifest(source_event: Mapping[str, Any]) -> tuple[Mapping[str, Any] | None, str]:
    for key in ("authority_manifest", "skill_manifest", "tool_manifest"):
        value = source_event.get(key)
        if isinstance(value, Mapping):
            return value, key
    return None, ""


def _first_list(mapping: Mapping[str, Any], *keys: str) -> list[Any]:
    for key in keys:
        value = mapping.get(key)
        if isinstance(value, list):
            return list(value)
        if value is not None:
            return [value]
    return []


def _consumption_is_allowed_by_capability(
    capability: dict[str, Any], consumption: Mapping[str, Any]
) -> bool:
    result = evaluate_authority_consumptions([capability], [dict(consumption)])
    return result["decision_counts"]["allow"] == 1


def _authority_confusion_row(
    *,
    case_id: str,
    capability: dict[str, Any],
    source_event: Mapping[str, Any],
    legal_consumption: Mapping[str, Any],
) -> dict[str, Any]:
    legal = copy.deepcopy(dict(legal_consumption))
    laundered = copy.deepcopy(legal)
    legal_need = _normalized_scalar_role_need(legal.get("need", {}))
    confused_need = copy.deepcopy(legal_need)
    original_role = str(legal_need["required_role"])
    confused_need["required_role"] = _confused_role(original_role, capability)
    legal["need"] = legal_need
    laundered["need"] = confused_need

    row = {
        "row_id": f"{case_id}::{legal.get('field', '<unknown-field>')}::required_role_confusion",
        "source": {
            "source_id": source_event.get("source_id", capability.get("source_id", "")),
            "source_type": source_event.get("source_type", "unknown"),
            "case_id": case_id,
        },
        "capabilities": [copy.deepcopy(capability)],
        "legal_consumption": legal,
        "laundered_consumption": laundered,
        "expected": {"legal": "allow", "laundered": "block"},
        "generated_from_case_id": case_id,
        "generated_from_source_id": capability.get("source_id", ""),
        "confusion_type": "boundary_preserving_semantic_role_mutation",
        "boundary_preserved": _boundary_preserved(legal, laundered),
        "mutated_need_fields": _mutated_need_fields(legal, laundered),
        "nearest_neighbor_objection": [
            "The field, operation, attributed source, and scope boundaries are unchanged; only the semantic role is mutated."
        ],
    }
    return row


def _normalized_scalar_role_need(raw_need: Any) -> dict[str, Any]:
    need = dict(raw_need) if isinstance(raw_need, Mapping) else {}
    if "required_role" not in need and isinstance(need.get("required_roles"), list):
        roles = need.pop("required_roles")
        if len(roles) == 1:
            need["required_role"] = roles[0]
    if not need.get("required_role"):
        raise ValueError("Authority-confusion generation requires a scalar required_role")
    need.pop("required_roles", None)
    return need


def _confused_role(original_role: str, capability: Mapping[str, Any]) -> str:
    candidate = f"confused::{original_role}"
    roles = set(str(role) for role in _list_value(capability.get("semantic_roles")))
    while candidate in roles:
        candidate = f"confused::{candidate}"
    return candidate


def _boundary_preserved(legal: Mapping[str, Any], laundered: Mapping[str, Any]) -> bool:
    if legal.get("field") != laundered.get("field"):
        return False
    if legal.get("operation") != laundered.get("operation"):
        return False
    if legal.get("attributed_source_id") != laundered.get("attributed_source_id"):
        return False
    legal_need = legal.get("need", {})
    laundered_need = laundered.get("need", {})
    if not isinstance(legal_need, Mapping) or not isinstance(laundered_need, Mapping):
        return False
    return all(legal_need.get(scope) == laundered_need.get(scope) for scope in SCOPE_KEYS)


def _mutated_need_fields(legal: Mapping[str, Any], laundered: Mapping[str, Any]) -> list[str]:
    legal_need = legal.get("need", {})
    laundered_need = laundered.get("need", {})
    if not isinstance(legal_need, Mapping) or not isinstance(laundered_need, Mapping):
        return []
    keys = sorted(set(legal_need) | set(laundered_need))
    return [key for key in keys if legal_need.get(key) != laundered_need.get(key)]


def _rows_digest(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    digest: list[dict[str, Any]] = []
    for row in rows:
        legal = row.get("legal_consumption", {})
        laundered = row.get("laundered_consumption", {})
        legal_need = legal.get("need", {}) if isinstance(legal, Mapping) else {}
        laundered_need = laundered.get("need", {}) if isinstance(laundered, Mapping) else {}
        digest.append(
            {
                "row_id": row.get("row_id", ""),
                "source_type": row.get("source", {}).get("source_type", ""),
                "field": legal.get("field", "") if isinstance(legal, Mapping) else "",
                "legal_required_role": legal_need.get("required_role", "")
                if isinstance(legal_need, Mapping)
                else "",
                "confused_required_role": laundered_need.get("required_role", "")
                if isinstance(laundered_need, Mapping)
                else "",
            }
        )
    return digest


def _list_value(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return list(value)
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, set):
        return list(value)
    return [value]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate trace-derived boundary-preserving authority-confusion rows."
    )
    parser.add_argument(
        "--fixture",
        default="examples/data/power_ops_planner_skill_tool_memory_fixture.json",
    )
    parser.add_argument("--rows-out", default="examples/data/power_ops_trace_authority_confusion_rows.json")
    parser.add_argument("--out-md")
    parser.add_argument("--out-json")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args(argv)

    summary = build_trace_authority_confusion_summary(
        fixture_path=args.fixture,
        rows_out_path=args.rows_out,
    )
    if args.out_md or args.out_json:
        write_trace_authority_confusion_report(
            summary,
            markdown_path=args.out_md or "docs/power_ops_trace_authority_confusion_results_2026-07-02.md",
            json_path=args.out_json,
        )
        return 0

    if args.format == "json":
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_trace_authority_confusion_markdown(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
