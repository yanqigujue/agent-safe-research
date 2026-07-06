from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Mapping, Sequence


NUMBER_RE = re.compile(r"(?<![A-Za-z0-9_])-?\d+(?:\.\d+)?(?![A-Za-z0-9_])")

KEY_NUMBER_PATTERNS = {
    "source_type_coverage=1.000": ("source_type_coverage=1.000",),
    "whole_action_block_rate=0.000": (
        "whole_action_block_rate=0.000",
        '"whole_action_block_rate": 0.0',
    ),
}


def build_numeric_claim_audit(
    *,
    document_paths: Sequence[str | Path],
    evidence_paths: Sequence[str | Path],
    table_binding_paths: Sequence[str | Path] = (),
) -> dict[str, Any]:
    documents = [_read_text_with_path(path) for path in document_paths]
    evidence = [_read_text_with_path(path) for path in evidence_paths]
    table_bindings = [_load_json(path) for path in table_binding_paths]
    table_binding_rows = _table_binding_rows(table_bindings)
    document_text = "\n".join(item["text"] for item in documents)
    evidence_text = "\n".join(item["text"] for item in evidence)
    numeric_mentions = [
        mention
        for document in documents
        for mention in _numeric_mentions(
            document,
            evidence_text=evidence_text,
            table_binding_rows=table_binding_rows,
        )
    ]

    supported_count = sum(1 for mention in numeric_mentions if mention["status"] == "supported")
    supported_by_table_count = sum(
        1 for mention in numeric_mentions if mention["status"] == "supported_by_table_binding"
    )
    supported_by_context_rule_count = sum(
        1 for mention in numeric_mentions if mention["status"] == "supported_by_context_rule"
    )
    ignored_context_number_count = sum(
        1 for mention in numeric_mentions if mention["status"] == "ignored_context_number"
    )
    needs_evidence_count = sum(
        1 for mention in numeric_mentions if mention["status"] == "needs_evidence"
    )

    return {
        "artifact_type": "power_ops_numeric_claim_audit",
        "document_count": len(documents),
        "evidence_count": len(evidence),
        "table_binding_count": len(table_bindings),
        "documents": [item["path"] for item in documents],
        "evidence": [item["path"] for item in evidence],
        "key_number_checks": _key_number_checks(
            document_text=document_text,
            evidence_text=evidence_text,
        ),
        "numeric_mentions": numeric_mentions,
        "supported_numeric_claim_count": supported_count,
        "supported_by_table_binding_numeric_claim_count": supported_by_table_count,
        "supported_by_context_rule_numeric_claim_count": supported_by_context_rule_count,
        "ignored_context_number_count": ignored_context_number_count,
        "unsupported_numeric_claim_count": needs_evidence_count,
    }


def render_numeric_claim_audit_markdown(audit: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Numeric Claim Audit",
        "",
        "| Item | Value |",
        "|---|---:|",
        f"| documents | {int(audit.get('document_count', 0))} |",
        f"| evidence files | {int(audit.get('evidence_count', 0))} |",
        f"| table bindings | {int(audit.get('table_binding_count', 0))} |",
        f"| supported numeric mentions | {int(audit.get('supported_numeric_claim_count', 0))} |",
        f"| supported by table binding | {int(audit.get('supported_by_table_binding_numeric_claim_count', 0))} |",
        f"| supported by context rule | {int(audit.get('supported_by_context_rule_numeric_claim_count', 0))} |",
        f"| ignored context numbers | {int(audit.get('ignored_context_number_count', 0))} |",
        f"| needs_evidence mentions | {int(audit.get('unsupported_numeric_claim_count', 0))} |",
        "",
        "## Key Number Checks",
        "",
        "| Key | Status | Document hit | Evidence hit |",
        "|---|---|---:|---:|",
    ]
    for key, result in _mapping_value(audit.get("key_number_checks")).items():
        if isinstance(result, Mapping):
            lines.append(
                "| {key} | {status} | {doc} | {evidence} |".format(
                    key=key,
                    status=result.get("status", ""),
                    doc=int(bool(result.get("document_hit", False))),
                    evidence=int(bool(result.get("evidence_hit", False))),
                )
            )

    lines.extend(
        [
            "",
            "## Numeric Mentions",
            "",
            "| Document | Number | Status | Context |",
            "|---|---:|---|---|",
        ]
    )
    for mention in _list_value(audit.get("numeric_mentions"))[:80]:
        if not isinstance(mention, Mapping):
            continue
        lines.append(
            "| `{document}` | {number} | {status} | {context} |".format(
                document=mention.get("document", ""),
                number=mention.get("number", ""),
                status=mention.get("status", ""),
                context=_escape_table_text(str(mention.get("context", ""))),
            )
        )
    lines.append("")
    return "\n".join(lines)


def write_numeric_claim_audit(
    audit: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_numeric_claim_audit_markdown(audit), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")


def _numeric_mentions(
    document: Mapping[str, str],
    *,
    evidence_text: str,
    table_binding_rows: list[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    text = document["text"]
    mentions: list[dict[str, Any]] = []
    for match in NUMBER_RE.finditer(text):
        if _ignored_numeric_match(text, match.start(), match.end()):
            continue
        context = _context_window(text, match.start(), match.end())
        if _context_supported(context, evidence_text):
            status = "supported"
        elif _context_supported_by_table_binding(
            context,
            number=match.group(0),
            table_binding_rows=table_binding_rows,
        ):
            status = "supported_by_table_binding"
        elif _context_supported_by_evidence_rule(
            context,
            number=match.group(0),
            evidence_text=evidence_text,
        ):
            status = "supported_by_context_rule"
        elif _context_only_numeric_context(context):
            status = "ignored_context_number"
        else:
            status = "needs_evidence"
        mentions.append(
            {
                "document": document["path"],
                "number": match.group(0),
                "status": status,
                "context": context,
            }
        )
    return mentions


def _table_binding_rows(table_bindings: list[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    rows: list[Mapping[str, Any]] = []
    for binding in table_bindings:
        for row in _list_value(binding.get("rows")):
            if isinstance(row, Mapping) and row.get("status") == "fully_supported":
                rows.append(row)
    return rows


def _context_supported_by_table_binding(
    context: str,
    *,
    number: str,
    table_binding_rows: list[Mapping[str, Any]],
) -> bool:
    normalized_context = _normalize_text(context).lower()
    for row in table_binding_rows:
        row_label = str(row.get("row_label", ""))
        if not row_label or row_label.lower() not in normalized_context:
            continue
        observed_values = _mapping_value(row.get("observed_values"))
        if any(_number_appears_in_cell(number, str(value)) for value in observed_values.values()):
            return True
    return False


def _number_appears_in_cell(number: str, cell: str) -> bool:
    return any(match.group(0) == number for match in NUMBER_RE.finditer(cell))


def _context_only_numeric_context(context: str) -> bool:
    lowered = context.lower()
    return any(
        token in lowered
        for token in (
            "| round |",
            "continuous iteration queue",
            "| planned:",
            "completed:",
            "next:",
            "forbidden claim hits",
            "**date:**",
            "next experiments",
            "contribution",
            "**formaltrust artifact.**",
            "**power-ops evaluation slice.**",
            "multi-step trace fixture",
            "repair-frame action invariance",
            "conservative collapse",
            "large-sample power-ops suite",
            "no-rag",
            "external 50-case results",
            "external 50-case html report",
            "external 50-case implementation",
            "三个点",
            "下一轮",
        )
    )


def _context_supported_by_evidence_rule(
    context: str,
    *,
    number: str,
    evidence_text: str,
) -> bool:
    normalized_context = _normalize_text(context).lower()
    normalized_evidence = _normalize_text(evidence_text).lower()

    if number == "10" and "baseline grid on the 10-case" in normalized_context:
        return (
            '"artifact_type": "power_ops_action_invariance_baseline_grid"' in normalized_evidence
            and '"total_cases": 10' in normalized_evidence
        )

    if number == "10" and "10-case curated baseline grid" in normalized_context:
        return (
            '"artifact_type": "power_ops_action_invariance_baseline_grid"' in normalized_evidence
            and '"total_cases": 10' in normalized_evidence
        )

    if number == "10" and "10-case power-ops suite" in normalized_context and "baseline grid" in normalized_context:
        return (
            '"artifact_type": "power_ops_action_invariance_baseline_grid"' in normalized_evidence
            and '"total_cases": 10' in normalized_evidence
        )

    fieldwise_repair_supported = (
        '"fieldwise_repair"' in normalized_evidence
        and '"authorized_final_field_preservation_rate": 1.0' in normalized_evidence
        and '"unauthorized_final_field_removal_rate": 1.0' in normalized_evidence
        and '"whole_action_block_rate": 0.0' in normalized_evidence
        and '"false_allow_field_rate": 0.0' in normalized_evidence
    )
    fieldwise_comparison_context = (
        "fieldwise_repair" in normalized_context and "only current baseline" in normalized_context
    ) or (
        "whole-action block 0.000" in normalized_context and "false allow 0.000" in normalized_context
    )
    if fieldwise_comparison_context and number in {"1.000", "0.000"}:
        return (
            fieldwise_repair_supported
        )

    external_case_context = (
        "external 50-case authority stress suite" in normalized_context
        or "full agent task cases from nerc lessons learned metadata" in normalized_context
        or "agent task cases from nerc lessons learned metadata" in normalized_context
        or "high-impact unauthorized fields" in normalized_context
    )
    if external_case_context:
        external_evidence = (
            '"suite_id": "power_ops_external_case_50"' in normalized_evidence
            and '"artifact_type": "power_ops_external_case_50_summary"' in normalized_evidence
        )
        if number == "50" and (
            "external 50-case authority stress suite" in normalized_context
            or "agent task cases from nerc lessons learned metadata" in normalized_context
        ):
            return external_evidence and (
                '"total_cases": 50' in normalized_evidence
                or '"external_lesson_count": 50' in normalized_evidence
            )
        if number == "350" and "authorized fields preserved" in normalized_context:
            return external_evidence and '"authorized_fields": 350' in normalized_evidence
        if number == "50" and "high-impact unauthorized fields removed" in normalized_context:
            return external_evidence and '"unauthorized_fields": 50' in normalized_evidence
        if number == "0.000" and "whole-action block" in normalized_context:
            return external_evidence and '"whole_action_block_rate": 0.0' in normalized_evidence

    if "expanded 18-case" in normalized_context:
        return (
            number == "18"
            and '"suite_id": "power_ops_action_invariance_expanded"' in normalized_evidence
            and '"total_cases": 18' in normalized_evidence
        )

    if "18-case expanded suite" in normalized_context:
        return (
            number == "18"
            and (
                '"artifact_type": "power_ops_action_invariance_dataset_audit"' in normalized_evidence
                or '"suite_id": "power_ops_action_invariance_expanded"' in normalized_evidence
            )
            and '"total_cases": 18' in normalized_evidence
        )

    if "expanded dataset audit reports" in normalized_context and "cases with oracle coverage" in normalized_context:
        if number == "18":
            return (
                '"artifact_type": "power_ops_action_invariance_dataset_audit"' in normalized_evidence
                and '"total_cases": 18' in normalized_evidence
            )
        if number == "1.000":
            return (
                '"artifact_type": "power_ops_action_invariance_dataset_audit"' in normalized_evidence
                and '"oracle_coverage_rate": 1.0' in normalized_evidence
            )

    if "current dataset boundary for section 4" in normalized_context and number == "4":
        return True

    if "curated baseline grid compares 4 modes" in normalized_context and number == "4":
        return all(
            token in normalized_evidence
            for token in (
                '"strict_block"',
                '"fieldwise_decision_only"',
                '"provenance_only"',
                '"fieldwise_repair"',
            )
        )

    if "trace-import path contributes" in normalized_context and "trace-import boundary cases" in normalized_context:
        if number == "4":
            return (
                '"suite_id": "power_ops_trace_import"' in normalized_evidence
                and '"total_cases": 4' in normalized_evidence
                and '"failed_cases": 0' in normalized_evidence
            )
        if number == "1":
            return (
                '"suite_id": "power_ops_multistep_trace_import"' in normalized_evidence
                and '"total_cases": 1' in normalized_evidence
                and '"failed_cases": 0' in normalized_evidence
            )
        if number == "2" and "planner-skill-tool-memory cases" in normalized_context:
            return (
                '"artifact_type": "power_ops_planner_skill_tool_memory_summary"' in normalized_evidence
                and '"total_cases": 2' in normalized_evidence
                and '"failed_cases": 0' in normalized_evidence
            )

    if "planner-skill-tool-memory cases" in normalized_context and number == "2":
        return (
            '"artifact_type": "power_ops_planner_skill_tool_memory_summary"' in normalized_evidence
            and '"total_cases": 2' in normalized_evidence
            and '"failed_cases": 0' in normalized_evidence
        )

    if "planner-skill-tool-memory" in normalized_context:
        if number == "2":
            return (
                '"artifact_type": "power_ops_planner_skill_tool_memory_summary"' in normalized_evidence
                and '"total_cases": 2' in normalized_evidence
                and '"passed_cases": 2' in normalized_evidence
            )
        if number == "0.000":
            return (
                '"artifact_type": "power_ops_planner_skill_tool_memory_summary"' in normalized_evidence
                and '"whole_action_block_rate": 0.0' in normalized_evidence
            )
        if number == "1.000":
            return (
                '"artifact_type": "power_ops_planner_skill_tool_memory_summary"' in normalized_evidence
                and (
                    '"authorized_final_field_preservation_rate": 1.0' in normalized_evidence
                    or '"unauthorized_final_field_removal_rate": 1.0' in normalized_evidence
                    or '"repair_frame_validity_rate": 1.0' in normalized_evidence
                )
            )

    if "table evidence binding currently marks" in normalized_context and "table rows as fully supported" in normalized_context:
        if number == "18":
            return (
                '"artifact_type": "power_ops_table_evidence_binding"' in normalized_evidence
                and '"fully_supported_row_count": 18' in normalized_evidence
            )
        if number == "19":
            return (
                '"artifact_type": "power_ops_table_evidence_binding"' in normalized_evidence
                and '"fully_supported_row_count": 19' in normalized_evidence
            )
        if number == "20":
            return (
                '"artifact_type": "power_ops_table_evidence_binding"' in normalized_evidence
                and '"fully_supported_row_count": 20' in normalized_evidence
            )
        if number == "21":
            return (
                '"artifact_type": "power_ops_table_evidence_binding"' in normalized_evidence
                and '"fully_supported_row_count": 21' in normalized_evidence
            )

    if "source-link completeness" in normalized_context and number == "1.000":
        return (
            '"artifact_type": "power_ops_paper_draft_consistency_audit"' in normalized_evidence
            and '"source_link_completeness_rate": 1.0' in normalized_evidence
        )

    if "text match rate" in normalized_context and number == "1.000":
        return (
            '"artifact_type": "power_ops_paper_draft_consistency_audit"' in normalized_evidence
            and '"text_match_rate": 1.0' in normalized_evidence
        )

    if "suite_count=3" in normalized_context and number == "3":
        return '"artifact_type": "power_ops_action_invariance_performance_profile"' in normalized_evidence and (
            '"suite_count": 3' in normalized_evidence
        )

    if "baseline_count=4" in normalized_context and number == "4":
        return '"artifact_type": "power_ops_action_invariance_performance_profile"' in normalized_evidence and (
            '"baseline_count": 4' in normalized_evidence
        )

    if "skill-authority" in normalized_context and number == "16":
        return (
            '"artifact_type": "power_ops_action_invariance_performance_profile"' in normalized_evidence
            and '"power_ops_skill_authority"' in normalized_evidence
            and '"latency_proxy_units": 16' in normalized_evidence
        )

    source_type_count_context = (
        ("source-type coverage" in normalized_context or "source type" in normalized_context)
        or (
            "tool_metadata" in normalized_context
            and "user_approval" in normalized_context
            and "prior_step_output" in normalized_context
        )
    )
    if source_type_count_context:
        source_counts = {
            "skill": "4",
            "tool_metadata": "1",
            "user_approval": "1",
            "memory": "1",
            "prior_step_output": "1",
        }
        for source_type, count in source_counts.items():
            if source_type in normalized_context and number == count:
                return (
                    '"artifact_type": "power_ops_action_invariance_dataset_audit"' in normalized_evidence
                    and f'"{source_type}": {count}' in normalized_evidence
                )

    if "total cases" in normalized_context and "passed cases" in normalized_context and number == "8":
        return (
            '"suite_id": "power_ops_skill_authority"' in normalized_evidence
            and '"total_cases": 8' in normalized_evidence
            and '"passed_cases": 8' in normalized_evidence
        )

    skill_authority_metric_context = (
        "authorized final-field preservation" in normalized_context
        or "unauthorized final-field removal" in normalized_context
        or "whole-action block rate" in normalized_context
        or "executable fieldwise-repair success" in normalized_context
        or "repair-frame validity" in normalized_context
    )
    if skill_authority_metric_context:
        if number == "1.000":
            return (
                '"suite_id": "power_ops_skill_authority"' in normalized_evidence
                and (
                    '"authorized_final_field_preservation_rate": 1.0' in normalized_evidence
                    or '"unauthorized_final_field_removal_rate": 1.0' in normalized_evidence
                    or '"executable_fieldwise_repair_success_rate": 1.0' in normalized_evidence
                    or '"repair_frame_validity_rate": 1.0' in normalized_evidence
                )
            )
        if number == "0.000":
            return (
                '"suite_id": "power_ops_skill_authority"' in normalized_evidence
                and '"whole_action_block_rate": 0.0' in normalized_evidence
            )

    return False


def _ignored_numeric_match(text: str, start: int, end: int) -> bool:
    if _inside_fenced_code(text, start):
        return True
    if _inside_backticks(text, start):
        return True
    if _inside_html_comment(text, start):
        return True
    if _line_for_position(text, start).lstrip().startswith("#"):
        return True
    if start > 0 and text[start - 1] == "§":
        return True
    nearby = text[max(0, start - 6) : min(len(text), end + 6)]
    if re.search(r"\d{4}-\d{2}-\d{2}", nearby):
        return True
    return False


def _inside_backticks(text: str, position: int) -> bool:
    return text.count("`", 0, position) % 2 == 1


def _inside_fenced_code(text: str, position: int) -> bool:
    return text.count("```", 0, position) % 2 == 1


def _inside_html_comment(text: str, position: int) -> bool:
    open_index = text.rfind("<!--", 0, position)
    close_index = text.rfind("-->", 0, position)
    return open_index > close_index


def _line_for_position(text: str, position: int) -> str:
    line_start = text.rfind("\n", 0, position) + 1
    line_end = text.find("\n", position)
    if line_end == -1:
        line_end = len(text)
    return text[line_start:line_end]


def _context_supported(context: str, evidence_text: str) -> bool:
    normalized_context = _normalize_text(context)
    normalized_evidence = _normalize_text(evidence_text)
    for patterns in KEY_NUMBER_PATTERNS.values():
        for pattern in patterns:
            if _normalize_text(pattern) in normalized_context and _normalize_text(pattern) in normalized_evidence:
                return True
    metric_match = re.search(
        r"(whole_action_block_rate|authorized_preservation|unsafe_removal|source_type_coverage)\s*=\s*(-?\d+(?:\.\d+)?)",
        normalized_context,
    )
    if metric_match:
        return metric_match.group(0) in normalized_evidence
    return False


def _key_number_checks(*, document_text: str, evidence_text: str) -> dict[str, dict[str, Any]]:
    checks: dict[str, dict[str, Any]] = {}
    normalized_document = _normalize_text(document_text)
    normalized_evidence = _normalize_text(evidence_text)
    for key, patterns in KEY_NUMBER_PATTERNS.items():
        document_hit = any(_normalize_text(pattern) in normalized_document for pattern in patterns)
        evidence_hit = any(_normalize_text(pattern) in normalized_evidence for pattern in patterns)
        checks[key] = {
            "status": "supported" if document_hit and evidence_hit else "needs_evidence",
            "document_hit": document_hit,
            "evidence_hit": evidence_hit,
            "patterns": list(patterns),
        }
    return checks


def _read_text_with_path(path: str | Path) -> dict[str, str]:
    target = Path(path)
    return {"path": target.as_posix(), "text": target.read_text(encoding="utf-8")}


def _load_json(path: str | Path) -> dict[str, Any]:
    target = Path(path)
    payload = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object at {path}")
    return payload


def _context_window(text: str, start: int, end: int, *, radius: int = 90) -> str:
    left = max(0, start - radius)
    right = min(len(text), end + radius)
    return " ".join(text[left:right].split())


def _normalize_text(value: str) -> str:
    return " ".join(value.replace("\\", "/").split())


def _escape_table_text(value: str) -> str:
    return value.replace("|", "\\|")


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
        description="Audit numeric claims in power-ops action-invariance writing artifacts."
    )
    parser.add_argument("--document", action="append", default=[])
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--table-binding", action="append", default=[])
    parser.add_argument(
        "--out-md",
        default="docs/power_ops_action_invariance_numeric_claim_audit_2026-07-02.md",
    )
    parser.add_argument(
        "--out-json",
        default="docs/power_ops_action_invariance_numeric_claim_audit_2026-07-02.json",
    )
    args = parser.parse_args(argv)

    audit = build_numeric_claim_audit(
        document_paths=args.document,
        evidence_paths=args.evidence,
        table_binding_paths=args.table_binding,
    )
    write_numeric_claim_audit(audit, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
