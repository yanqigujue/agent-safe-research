from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence


DEFAULT_DRAFT_PATH = "docs/power_ops_action_invariance_evidence_bound_paper_draft_2026-07-02.json"
DEFAULT_CLAIM_LEDGER_READINESS = "docs/power_ops_action_invariance_claim_ledger_readiness_2026-07-02.json"
DEFAULT_DRAFT_CONSISTENCY_AUDIT = "docs/power_ops_action_invariance_paper_draft_consistency_audit_2026-07-02.json"
DEFAULT_OUT_MD = "docs/power_ops_action_invariance_claim_to_paragraph_map_2026-07-02.md"
DEFAULT_OUT_JSON = "docs/power_ops_action_invariance_claim_to_paragraph_map_2026-07-02.json"

FORBIDDEN_CLAIM_PHRASES = (
    "first llm-agent guardrail",
    "first runtime enforcement framework",
    "first least-privilege llm-agent security framework",
    "solves prompt injection",
    "proves production safety",
    "outperforms official neighboring systems",
    "reduces real human workload",
)

BOUNDARY_PATTERNS = (
    ("production_telemetry_excluded", ("production telemetry", "production-safety", "deployment safety")),
    ("operator_workload_excluded", ("operator workload", "workload reduction", "human workload", "operator-time")),
    ("official_superiority_excluded", ("official benchmark superiority", "official neighboring-system superiority")),
    ("latency_excluded", ("wall-clock latency", "speed result")),
    ("firstness_excluded", ("firstness", "generic agent-security firstness")),
    ("prompt_injection_solution_excluded", ("prompt-injection solution", "solves prompt injection")),
)

CLAIM_KEYWORDS = (
    (
        "fieldwise repair final-action mode exists",
        (
            "fieldwise repair",
            "final-action",
            "capguard",
            "actioninvariant",
            "minimal authority witness",
            "authority need",
        ),
    ),
    (
        "curated power-ops fieldwise repair preserves authorized fields and removes unauthorized fields",
        ("curated", "field preservation", "authorized fields", "unauthorized fields", "fieldwise-repair row"),
    ),
    (
        "expanded 18-case power-ops fieldwise repair preserves authorized fields and removes unauthorized fields",
        ("expanded", "18-case", "18 cases"),
    ),
    (
        "metamorphic authority-confusion tests preserve authorized fields while removing or reviewing mutated unsafe fields",
        ("metamorphic", "authority-confusion", "mutated unsafe"),
    ),
    (
        "no-RAG skill-driven fixture lifts skill, tool metadata, approval, memory, and prior-step outputs into field-level capabilities",
        (
            "skill",
            "no-rag",
            "skill-manifest",
            "skill manifests",
            "skill-driven",
            "multi-source authority",
            "tool metadata",
            "approval",
            "memory",
            "prior-step",
        ),
    ),
    (
        "current artifact reports a safety-preserving normal-behavior performance profile",
        ("performance", "normal-behavior", "latency proxy"),
    ),
    (
        "baseline grid shows strict-block collapse and provenance-only false allow on curated cases",
        ("baseline", "strict-block", "provenance-only", "strict blocking"),
    ),
    (
        "trace/span/OTLP replay feeds fieldwise repair",
        ("trace/span/otlp", "span/otlp", "trace replay", "otlp"),
    ),
    (
        "trace import fixture covers malformed trace, missing source, duplicate approval, and expired epoch boundaries",
        ("trace-import", "trace import", "malformed", "duplicate approval", "expired epoch"),
    ),
    (
        "multi-step trace import covers planner, skill, tool metadata, memory, prior-step output, and user approval source chains",
        (
            "multi-step",
            "source-chain",
            "planner",
            "skill",
            "memory",
            "prior-step output",
            "tool metadata",
            "user approval",
            "planner-skill-tool-memory",
        ),
    ),
    (
        "AgentDojo-style and semi-real power trace bridge fixtures are expressible",
        ("agentdojo-style", "semi-real", "bridge fixtures", "bridge"),
    ),
)


def build_claim_to_paragraph_map(
    *,
    draft_path: str | Path = DEFAULT_DRAFT_PATH,
    claim_ledger_readiness_path: str | Path = DEFAULT_CLAIM_LEDGER_READINESS,
    draft_consistency_audit_path: str | Path = DEFAULT_DRAFT_CONSISTENCY_AUDIT,
) -> dict[str, Any]:
    draft = _load_json(draft_path)
    claim_readiness = _load_json(claim_ledger_readiness_path)
    draft_audit = _load_json(draft_consistency_audit_path)
    supported_claims = _claim_index(_list_value(claim_readiness.get("supported_claims")))

    rows: list[dict[str, Any]] = []
    sections = [
        section
        for section in _list_value(draft.get("sections"))
        if isinstance(section, Mapping)
    ]
    for section_index, section in enumerate(sections, start=1):
        rows.extend(
            _paragraph_rows_for_section(
                section_index=section_index,
                section=section,
                supported_claims=supported_claims,
            )
        )

    forbidden_hits = _forbidden_claim_hits(str(draft.get("paper_text", "")))
    unmapped_count = sum(1 for row in rows if row["claim_binding_status"] == "unmapped")
    claim_mapped_count = sum(1 for row in rows if row["claim_binding_status"] == "claim_mapped")
    source_mapped_count = sum(1 for row in rows if row["claim_binding_status"] == "source_mapped")
    boundary_count = sum(1 for row in rows if row["boundary_flags"])
    source_linked = sum(1 for row in rows if row["source_exists"])
    bound_rows = sum(1 for row in rows if row["claim_binding_status"] != "unmapped")

    blockers: list[str] = []
    if draft.get("paper_draft_status") != "ready":
        blockers.append(f"paper_draft_status={draft.get('paper_draft_status')}")
    if not bool(claim_readiness.get("readiness_passed", False)):
        blockers.append("claim ledger readiness is not passed")
    if draft_audit.get("audit_status") != "PASS":
        blockers.append("paper draft consistency audit is not passed")
    if unmapped_count:
        blockers.append(f"{unmapped_count} paragraph rows are unmapped")
    if forbidden_hits:
        blockers.append(f"{len(forbidden_hits)} forbidden claim hits remain in draft text")

    return {
        "artifact_type": "power_ops_claim_to_paragraph_map",
        "draft_path": str(draft_path),
        "draft_content_sha256": _draft_content_sha256(draft),
        "claim_ledger_readiness_path": str(claim_ledger_readiness_path),
        "draft_consistency_audit_path": str(draft_consistency_audit_path),
        "map_status": "PASS" if not blockers else "FAIL",
        "passed": not blockers,
        "blockers": blockers,
        "section_count": len(sections),
        "paragraph_count": len(rows),
        "source_link_completeness_rate": _rate(source_linked, len(rows)),
        "claim_or_source_binding_rate": _rate(bound_rows, len(rows)),
        "claim_mapped_paragraph_count": claim_mapped_count,
        "source_mapped_paragraph_count": source_mapped_count,
        "boundary_marked_paragraph_count": boundary_count,
        "unmapped_paragraph_count": unmapped_count,
        "forbidden_claim_hits": forbidden_hits,
        "paragraph_rows": rows,
    }


def render_claim_to_paragraph_map_markdown(paragraph_map: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Claim-to-Paragraph Map",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Map status | {paragraph_map.get('map_status', 'FAIL')} |",
        f"| Sections | {int(paragraph_map.get('section_count', 0) or 0)} |",
        f"| Paragraph rows | {int(paragraph_map.get('paragraph_count', 0) or 0)} |",
        f"| Source-link completeness | {float(paragraph_map.get('source_link_completeness_rate', 0.0) or 0.0):.3f} |",
        f"| Claim-or-source binding | {float(paragraph_map.get('claim_or_source_binding_rate', 0.0) or 0.0):.3f} |",
        f"| Claim-mapped paragraphs | {int(paragraph_map.get('claim_mapped_paragraph_count', 0) or 0)} |",
        f"| Boundary-marked paragraphs | {int(paragraph_map.get('boundary_marked_paragraph_count', 0) or 0)} |",
        f"| Unmapped paragraphs | {int(paragraph_map.get('unmapped_paragraph_count', 0) or 0)} |",
        "",
        "## Blockers",
        "",
    ]
    blockers = _list_value(paragraph_map.get("blockers"))
    if blockers:
        lines.extend(f"- {blocker}" for blocker in blockers)
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "## Paragraph Rows",
            "",
            "| Section | Para | Status | Claims | Refs | Boundary | Source |",
            "|---|---:|---|---:|---:|---|---|",
        ]
    )
    for row in _list_value(paragraph_map.get("paragraph_rows")):
        if not isinstance(row, Mapping):
            continue
        lines.append(
            "| {section} | {para} | {status} | {claims} | {refs} | {boundary} | {source} |".format(
                section=_escape_table_text(str(row.get("slot", ""))),
                para=int(row.get("paragraph_index", 0) or 0),
                status=_escape_table_text(str(row.get("claim_binding_status", ""))),
                claims=len(_list_value(row.get("source_claims"))),
                refs=len(_list_value(row.get("evidence_refs"))),
                boundary=_escape_table_text(",".join(str(flag) for flag in _list_value(row.get("boundary_flags")))),
                source=_escape_table_text(str(row.get("source_path", ""))),
            )
        )
    lines.append("")
    return "\n".join(lines)


def write_claim_to_paragraph_map(
    paragraph_map: Mapping[str, Any],
    *,
    markdown_path: str | Path = DEFAULT_OUT_MD,
    json_path: str | Path | None = DEFAULT_OUT_JSON,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_claim_to_paragraph_map_markdown(paragraph_map), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(paragraph_map, ensure_ascii=False, indent=2), encoding="utf-8")


def _paragraph_rows_for_section(
    *,
    section_index: int,
    section: Mapping[str, Any],
    supported_claims: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    source_path = str(section.get("source_path", ""))
    source_payload: dict[str, Any] = {}
    source_exists = False
    if source_path:
        source = Path(source_path)
        source_exists = source.exists()
        if source_exists:
            source_payload = _load_json(source)

    section_text = str(section.get("text", ""))
    source_units = _source_units_for_section(section_text, source_payload)
    paragraphs = _split_paragraphs(section_text)

    rows = []
    for paragraph_index, paragraph_text in enumerate(paragraphs, start=1):
        source_unit = _matching_source_unit(paragraph_text, source_units)
        source_claims = _claim_rows(_list_value(source_unit.get("source_claims")))
        if not source_claims:
            source_claims = _infer_supported_claims(paragraph_text, supported_claims)
        evidence_refs = _evidence_refs(source_unit, source_claims)
        boundary_flags = _boundary_flags(paragraph_text, source_unit)
        binding_status = _binding_status(
            source_path=source_path,
            source_exists=source_exists,
            source_claims=source_claims,
            evidence_refs=evidence_refs,
        )
        rows.append(
            {
                "section_index": section_index,
                "slot": str(section.get("slot", "")),
                "heading": str(section.get("heading", "")),
                "paragraph_index": paragraph_index,
                "source_unit_slot": str(source_unit.get("slot") or source_unit.get("source_slot") or ""),
                "source_path": source_path,
                "source_exists": source_exists,
                "source_artifact_type": str(source_payload.get("artifact_type", "")),
                "claim_binding_status": binding_status,
                "boundary_flags": boundary_flags,
                "source_claims": source_claims,
                "evidence_refs": evidence_refs,
                "paragraph_text": paragraph_text,
            }
        )
    return rows


def _source_units_for_section(section_text: str, source_payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    paragraphs = [
        dict(row)
        for row in _list_value(source_payload.get("paragraphs"))
        if isinstance(row, Mapping)
    ]
    if paragraphs:
        return paragraphs

    sentences = [
        row
        for row in _list_value(source_payload.get("sentences"))
        if isinstance(row, Mapping)
    ]
    if sentences:
        return [_aggregate_sentence_units(section_text, sentences)]

    return []


def _aggregate_sentence_units(section_text: str, sentences: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    claims: list[Mapping[str, Any]] = []
    refs: list[str] = []
    slots: list[str] = []
    for sentence in sentences:
        slots.append(str(sentence.get("source_slot", "")))
        claims.extend(
            claim
            for claim in _list_value(sentence.get("source_claims"))
            if isinstance(claim, Mapping)
        )
        refs.extend(_string_values(sentence.get("source_refs")))
    return {
        "slot": "aggregated_sentences",
        "source_slot": ",".join(slot for slot in slots if slot),
        "text": section_text,
        "source_claims": _dedupe_claims(claims),
        "source_refs": refs,
    }


def _matching_source_unit(paragraph_text: str, source_units: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    for unit in source_units:
        if str(unit.get("text", "")).strip() == paragraph_text.strip():
            return dict(unit)
    return {}


def _claim_rows(claims: Sequence[Any]) -> list[dict[str, Any]]:
    return [
        {
            "claim": str(claim.get("claim", "")),
            "level": str(claim.get("level", "")),
            "paper_ready": bool(claim.get("paper_ready", False)),
            "evidence": _string_values(claim.get("evidence")),
        }
        for claim in claims
        if isinstance(claim, Mapping) and str(claim.get("claim", ""))
    ]


def _infer_supported_claims(
    paragraph_text: str,
    supported_claims: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    text = paragraph_text.lower()
    inferred = []
    for claim_text, keywords in CLAIM_KEYWORDS:
        if claim_text not in supported_claims:
            continue
        if any(keyword.lower() in text for keyword in keywords):
            claim = supported_claims[claim_text]
            inferred.append(
                {
                    "claim": claim_text,
                    "level": str(claim.get("level", "")),
                    "paper_ready": bool(claim.get("paper_ready", False)),
                    "evidence": _string_values(claim.get("evidence")),
                    "inferred_from_text": True,
                }
            )
    return _dedupe_claims(inferred)


def _evidence_refs(source_unit: Mapping[str, Any], source_claims: Sequence[Mapping[str, Any]]) -> list[str]:
    refs: list[str] = []
    for key in ("evidence_paths", "source_paths", "source_refs", "formal_refs"):
        refs.extend(_string_values(source_unit.get(key)))
    for table_ref in _list_value(source_unit.get("table_refs")):
        if isinstance(table_ref, Mapping):
            refs.extend(_string_values(table_ref.get("source_artifact")))
    for claim in source_claims:
        refs.extend(_string_values(claim.get("evidence")))
    return _dedupe_strings(refs)


def _boundary_flags(paragraph_text: str, source_unit: Mapping[str, Any]) -> list[str]:
    text = " ".join(
        [
            paragraph_text,
            str(source_unit.get("limitation_reason", "")),
            " ".join(_string_values(source_unit.get("excluded_claims"))),
            str(source_unit.get("claim_boundary", "")),
        ]
    ).lower()
    return [
        label
        for label, patterns in BOUNDARY_PATTERNS
        if any(pattern in text for pattern in patterns)
    ]


def _binding_status(
    *,
    source_path: str,
    source_exists: bool,
    source_claims: Sequence[Mapping[str, Any]],
    evidence_refs: Sequence[str],
) -> str:
    if not source_path or not source_exists:
        return "unmapped"
    if source_claims:
        return "claim_mapped"
    if evidence_refs:
        return "source_mapped"
    return "source_mapped"


def _claim_index(claims: Sequence[Any]) -> dict[str, Mapping[str, Any]]:
    return {
        str(claim.get("claim", "")): dict(claim)
        for claim in claims
        if isinstance(claim, Mapping) and str(claim.get("claim", ""))
    }


def _forbidden_claim_hits(text: str) -> list[dict[str, str]]:
    lowered = text.lower()
    return [
        {"phrase": phrase}
        for phrase in FORBIDDEN_CLAIM_PHRASES
        if phrase in lowered
    ]


def _split_paragraphs(text: str) -> list[str]:
    return [part.strip() for part in text.split("\n\n") if part.strip()]


def _draft_content_sha256(draft: Mapping[str, Any]) -> str:
    sections = [
        {
            "slot": str(section.get("slot", "")),
            "heading": str(section.get("heading", "")),
            "source_path": str(section.get("source_path", "")),
            "text": str(section.get("text", "")),
        }
        for section in _list_value(draft.get("sections"))
        if isinstance(section, Mapping)
    ]
    payload = {
        "paper_draft_status": str(draft.get("paper_draft_status", "")),
        "title": str(draft.get("title", "")),
        "sections": sections,
    }
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


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


def _string_values(value: Any) -> list[str]:
    values: list[str] = []
    for item in _list_value(value):
        if isinstance(item, str) and item:
            values.append(item)
    return values


def _dedupe_strings(values: Sequence[str]) -> list[str]:
    seen = set()
    deduped = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            deduped.append(value)
    return deduped


def _dedupe_claims(claims: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    deduped: list[dict[str, Any]] = []
    seen = set()
    for claim in claims:
        claim_text = str(claim.get("claim", ""))
        if not claim_text or claim_text in seen:
            continue
        seen.add(claim_text)
        deduped.append(dict(claim))
    return deduped


def _rate(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return round(numerator / denominator, 6)


def _escape_table_text(value: str) -> str:
    return value.replace("|", "\\|")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Map assembled power-ops paper paragraphs back to source claims and evidence."
    )
    parser.add_argument("--draft", default=DEFAULT_DRAFT_PATH)
    parser.add_argument("--claim-ledger-readiness", default=DEFAULT_CLAIM_LEDGER_READINESS)
    parser.add_argument("--draft-consistency-audit", default=DEFAULT_DRAFT_CONSISTENCY_AUDIT)
    parser.add_argument("--out-md", default=DEFAULT_OUT_MD)
    parser.add_argument("--out-json", default=DEFAULT_OUT_JSON)
    args = parser.parse_args(argv)

    paragraph_map = build_claim_to_paragraph_map(
        draft_path=args.draft,
        claim_ledger_readiness_path=args.claim_ledger_readiness,
        draft_consistency_audit_path=args.draft_consistency_audit,
    )
    write_claim_to_paragraph_map(paragraph_map, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
