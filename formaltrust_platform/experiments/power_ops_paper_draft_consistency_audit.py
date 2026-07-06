from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping


DEFAULT_DRAFT_PATH = "docs/power_ops_action_invariance_evidence_bound_paper_draft_2026-07-02.json"
DEFAULT_OUT_MD = "docs/power_ops_action_invariance_paper_draft_consistency_audit_2026-07-02.md"
DEFAULT_OUT_JSON = "docs/power_ops_action_invariance_paper_draft_consistency_audit_2026-07-02.json"

EXPECTED_SECTIONS = (
    {
        "slot": "abstract",
        "heading": "Abstract",
        "artifact_type": "power_ops_evidence_bound_abstract",
        "status_key": "abstract_status",
        "text_key": "abstract_text",
    },
    {
        "slot": "introduction",
        "heading": "1 Introduction",
        "artifact_type": "power_ops_evidence_bound_intro_prose",
        "status_key": "intro_prose_status",
        "text_key": "intro_text",
    },
    {
        "slot": "related_work",
        "heading": "2 Related Work and Novelty Boundary",
        "artifact_type": "power_ops_evidence_bound_related_work_prose",
        "status_key": "related_work_prose_status",
        "text_key": "related_work_text",
    },
    {
        "slot": "method",
        "heading": "3 Formal Model and CapGuard",
        "artifact_type": "power_ops_evidence_bound_method_prose",
        "status_key": "method_prose_status",
        "text_key": "method_text",
    },
    {
        "slot": "evaluation_setup",
        "heading": "4 Evaluation Setup",
        "artifact_type": "power_ops_evidence_bound_evaluation_setup",
        "status_key": "evaluation_setup_status",
        "text_key": "evaluation_setup_text",
    },
    {
        "slot": "results",
        "heading": "5 Results and Analysis",
        "artifact_type": "power_ops_evidence_bound_results_prose",
        "status_key": "results_prose_status",
        "text_key": "results_text",
    },
    {
        "slot": "limitations",
        "heading": "6 Limitations and Next Experiments",
        "artifact_type": "power_ops_evidence_bound_limitations_prose",
        "status_key": "limitations_prose_status",
        "text_key": "limitations_text",
    },
    {
        "slot": "conclusion",
        "heading": "7 Conclusion",
        "artifact_type": "power_ops_evidence_bound_conclusion",
        "status_key": "conclusion_status",
        "text_key": "conclusion_text",
    },
)

UNRESOLVED_BOUNDARY_PHRASES = (
    "todo",
    "tbd",
    "citation needed",
    "needs_evidence",
    "needs evidence",
    "unsupported_numeric_claim",
    "blocked_section_not_ready",
    "blocked_no_ready",
)


def audit_evidence_bound_paper_draft(*, draft_path: str | Path = DEFAULT_DRAFT_PATH) -> dict[str, Any]:
    draft = _load_json(draft_path)
    sections = _list_value(draft.get("sections"))
    expected_slots = [str(spec["slot"]) for spec in EXPECTED_SECTIONS]
    actual_slots = [
        str(section.get("slot", ""))
        for section in sections
        if isinstance(section, Mapping)
    ]
    section_checks = [
        _check_section(index=index, section=sections[index] if index < len(sections) else {}, spec=spec)
        for index, spec in enumerate(EXPECTED_SECTIONS)
    ]
    unresolved_hits = _unresolved_boundary_hits(_draft_text(draft))
    forbidden_hits = _list_value(draft.get("forbidden_claim_hits"))

    source_complete = sum(1 for row in section_checks if row["source_exists"] and row["source_status_ready"])
    text_matches = sum(1 for row in section_checks if row["text_matches_source"])
    mismatches = [row for row in section_checks if not row["text_matches_source"]]
    blockers: list[str] = []

    section_order_matches = actual_slots == expected_slots
    if draft.get("paper_draft_status") != "ready":
        blockers.append(f"paper_draft_status={draft.get('paper_draft_status')}")
    if not section_order_matches:
        blockers.append("section order does not match expected paper order")
    if source_complete != len(EXPECTED_SECTIONS):
        blockers.append("one or more section sources are missing, stale, or not ready")
    if mismatches:
        blockers.append(f"{len(mismatches)} section texts do not match their source artifacts")
    if forbidden_hits:
        blockers.append(f"{len(forbidden_hits)} forbidden claim hits remain in paper draft")
    if unresolved_hits:
        blockers.append(f"{len(unresolved_hits)} unresolved boundary placeholders remain in paper draft")

    return {
        "artifact_type": "power_ops_paper_draft_consistency_audit",
        "draft_path": str(draft_path),
        "audit_status": "PASS" if not blockers else "FAIL",
        "passed": not blockers,
        "blockers": blockers,
        "section_count": len(sections),
        "expected_slots": expected_slots,
        "actual_slots": actual_slots,
        "section_order_matches": section_order_matches,
        "source_link_completeness_rate": _rate(source_complete, len(EXPECTED_SECTIONS)),
        "text_match_rate": _rate(text_matches, len(EXPECTED_SECTIONS)),
        "mismatch_count": len(mismatches),
        "forbidden_claim_hit_count": len(forbidden_hits),
        "unresolved_boundary_hit_count": len(unresolved_hits),
        "unresolved_boundary_hits": unresolved_hits,
        "section_checks": section_checks,
    }


def render_paper_draft_consistency_audit_markdown(audit: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Paper Draft Consistency Audit",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Audit status | {audit.get('audit_status', 'FAIL')} |",
        f"| Section count | {audit.get('section_count', 0)} |",
        f"| Section order matches | {audit.get('section_order_matches', False)} |",
        f"| Source-link completeness | {audit.get('source_link_completeness_rate', 0.0):.3f} |",
        f"| Text match rate | {audit.get('text_match_rate', 0.0):.3f} |",
        f"| Mismatch count | {audit.get('mismatch_count', 0)} |",
        f"| Unresolved boundary hits | {audit.get('unresolved_boundary_hit_count', 0)} |",
        "",
        "## Blockers",
        "",
    ]
    blockers = _list_value(audit.get("blockers"))
    if blockers:
        lines.extend(f"- {blocker}" for blocker in blockers)
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "## Section Checks",
            "",
            "| Slot | Source exists | Source ready | Artifact matches | Text matches source |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for row in _list_value(audit.get("section_checks")):
        if not isinstance(row, Mapping):
            continue
        lines.append(
            "| {slot} | {exists} | {ready} | {artifact} | {text} |".format(
                slot=row.get("slot", ""),
                exists=row.get("source_exists", False),
                ready=row.get("source_status_ready", False),
                artifact=row.get("artifact_type_matches", False),
                text=row.get("text_matches_source", False),
            )
        )
    lines.append("")
    return "\n".join(lines)


def write_paper_draft_consistency_audit(
    audit: Mapping[str, Any],
    *,
    markdown_path: str | Path = DEFAULT_OUT_MD,
    json_path: str | Path | None = DEFAULT_OUT_JSON,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_paper_draft_consistency_audit_markdown(audit), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")


def _check_section(*, index: int, section: Any, spec: Mapping[str, str]) -> dict[str, Any]:
    section_map = section if isinstance(section, Mapping) else {}
    source_path = str(section_map.get("source_path", ""))
    source_payload: dict[str, Any] = {}
    source_exists = False
    if source_path:
        source = Path(source_path)
        source_exists = source.exists()
        if source_exists:
            source_payload = _load_json(source)

    source_status = str(source_payload.get(spec["status_key"], ""))
    source_text = str(source_payload.get(spec["text_key"], ""))
    actual_text = str(section_map.get("text", ""))
    return {
        "index": index,
        "slot": str(section_map.get("slot", "")),
        "expected_slot": spec["slot"],
        "heading": str(section_map.get("heading", "")),
        "expected_heading": spec["heading"],
        "source_path": source_path,
        "source_exists": source_exists,
        "source_status": source_status,
        "source_status_ready": source_status == "ready",
        "artifact_type": str(section_map.get("artifact_type", "")),
        "expected_artifact_type": spec["artifact_type"],
        "artifact_type_matches": str(section_map.get("artifact_type", "")) == spec["artifact_type"],
        "section_slot_matches": str(section_map.get("slot", "")) == spec["slot"],
        "section_heading_matches": str(section_map.get("heading", "")) == spec["heading"],
        "text_matches_source": source_exists and actual_text == source_text and bool(actual_text),
        "text_length": len(actual_text),
        "source_text_length": len(source_text),
    }


def _draft_text(draft: Mapping[str, Any]) -> str:
    parts = [str(draft.get("paper_text", ""))]
    for section in _list_value(draft.get("sections")):
        if isinstance(section, Mapping):
            parts.append(str(section.get("text", "")))
    return "\n".join(parts)


def _unresolved_boundary_hits(text: str) -> list[dict[str, str]]:
    lowered = text.lower()
    return [
        {"phrase": phrase}
        for phrase in UNRESOLVED_BOUNDARY_PHRASES
        if phrase in lowered
    ]


def _load_json(path: str | Path) -> dict[str, Any]:
    target = Path(path)
    payload = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object at {path}")
    return payload


def _list_value(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return list(value)
    if isinstance(value, tuple | set):
        return list(value)
    return [value]


def _rate(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return round(numerator / denominator, 4)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit assembled power-ops paper draft consistency.")
    parser.add_argument("--draft", default=DEFAULT_DRAFT_PATH)
    parser.add_argument("--out-md", default=DEFAULT_OUT_MD)
    parser.add_argument("--out-json", default=DEFAULT_OUT_JSON)
    args = parser.parse_args(argv)

    audit = audit_evidence_bound_paper_draft(draft_path=args.draft)
    write_paper_draft_consistency_audit(audit, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
