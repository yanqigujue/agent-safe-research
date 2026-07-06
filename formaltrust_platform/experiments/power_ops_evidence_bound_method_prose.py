from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping


FORBIDDEN_CLAIM_PHRASES = (
    "first llm-agent guardrail",
    "first runtime enforcement framework",
    "first least-privilege llm-agent security framework",
    "solves prompt injection",
    "proves production safety",
    "outperforms official neighboring systems",
    "reduces real human workload",
)


METHOD_PARAGRAPHS = (
    (
        "formal_objects",
        (
            "We model each agent source as a capability object Cap(x) and each action field as an "
            "authority need Need(s,f), so authorization is checked at field granularity rather than "
            "at the whole-action level."
        ),
    ),
    (
        "coverage_rule",
        (
            "A capability covers a field only when role, field, operation, data scope, effect scope, "
            "delegation scope, time scope, and required obligations all match."
        ),
    ),
    (
        "minimal_witness_decision",
        (
            "For each field, CapGuard records a Minimal Authority Witness when coverage exists; "
            "otherwise the field decision becomes abstain or block depending on counter-authority "
            "and evidence completeness."
        ),
    ),
    (
        "repair_invariance",
        (
            "The repair target is ActionInvariant(a,a'): preserve allowed fields, prevent "
            "unauthorized fields, and implement Repair(a) as keep allowed fields plus remove, "
            "block, or route the rest."
        ),
    ),
    (
        "implementation_binding",
        (
            "The implementation binds these objects to existing FormalTrust metadata and metrics, "
            "including afw_source_events, afw_consumptions, candidate_action, "
            "afw_runtime_field_results, witness_audit, and final_action."
        ),
    ),
    (
        "claim_boundary",
        (
            "This method section is bounded to the local artifact and benchmark slice: no "
            "production telemetry, no real workload-reduction claim, and no official "
            "neighboring-system superiority claim."
        ),
    ),
)


def build_evidence_bound_method_prose(*, method_outline_path: str | Path) -> dict[str, Any]:
    outline = _load_json(method_outline_path)
    outline_items = [
        item
        for item in _list_value(outline.get("method_outline"))
        if isinstance(item, Mapping)
    ]
    if str(outline.get("method_outline_status", "")) != "ready" or not outline_items:
        return {
            "artifact_type": "power_ops_evidence_bound_method_prose",
            "source_method_outline": str(method_outline_path),
            "paper_section": str(outline.get("paper_section", "搂3 Formal Model and CapGuard")),
            "method_prose_status": "blocked_no_ready_outline",
            "paragraph_count": 0,
            "method_text": "",
            "paragraphs": [],
            "forbidden_claim_hits": [],
        }

    by_slot = {str(item.get("slot", "")): item for item in outline_items}
    paragraphs = [
        _paragraph(text=text, source_item=by_slot.get(slot, outline_items[0]))
        for slot, text in METHOD_PARAGRAPHS
    ]
    method_text = "\n\n".join(paragraph["text"] for paragraph in paragraphs)
    forbidden_hits = _forbidden_claim_hits(method_text)

    return {
        "artifact_type": "power_ops_evidence_bound_method_prose",
        "source_method_outline": str(method_outline_path),
        "paper_section": str(outline.get("paper_section", "搂3 Formal Model and CapGuard")),
        "method_prose_status": "ready" if not forbidden_hits else "blocked_forbidden_claim",
        "paragraph_count": len(paragraphs),
        "method_text": method_text,
        "paragraphs": paragraphs,
        "forbidden_claim_hits": forbidden_hits,
    }


def render_evidence_bound_method_prose_markdown(prose: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Evidence-Bound Method Prose",
        "",
        f"**Status:** {prose.get('method_prose_status', '')}",
        f"**Paper section:** {prose.get('paper_section', '')}",
        f"**Paragraph count:** {int(prose.get('paragraph_count', 0) or 0)}",
        f"**Forbidden claim hits:** {len(_list_value(prose.get('forbidden_claim_hits')))}",
        "",
        "## Method Prose",
        "",
        str(prose.get("method_text", "")),
        "",
        "## Paragraph Evidence",
        "",
        "| Slot | Paragraph | Formal refs | Source claims | Limitation reason |",
        "|---|---|---|---|---|",
    ]
    for paragraph in _list_value(prose.get("paragraphs")):
        if not isinstance(paragraph, Mapping):
            continue
        lines.append(
            "| {slot} | {text} | {refs} | {claims} | {limitation} |".format(
                slot=_escape_table_text(str(paragraph.get("slot", ""))),
                text=_escape_table_text(str(paragraph.get("text", ""))),
                refs=_escape_table_text("; ".join(str(ref) for ref in _list_value(paragraph.get("formal_refs")))),
                claims=_escape_table_text(_source_claim_labels(paragraph.get("source_claims"))),
                limitation=_escape_table_text(str(paragraph.get("limitation_reason", ""))),
            )
        )
    lines.append("")
    return "\n".join(lines)


def write_evidence_bound_method_prose(
    prose: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_evidence_bound_method_prose_markdown(prose), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(prose, ensure_ascii=False, indent=2), encoding="utf-8")


def _paragraph(*, text: str, source_item: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "slot": str(source_item.get("slot", "")),
        "text": text,
        "formal_refs": [str(ref) for ref in _list_value(source_item.get("source_refs")) if str(ref)],
        "source_claims": [
            _source_claim_summary(claim)
            for claim in _list_value(source_item.get("source_claims"))
            if isinstance(claim, Mapping)
        ],
        "limitation_reason": str(source_item.get("limitation_reason", "")),
    }


def _source_claim_summary(claim: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "claim": str(claim.get("claim", "")),
        "level": str(claim.get("level", "")),
        "paper_ready": bool(claim.get("paper_ready", False)),
        "evidence": [str(item) for item in _list_value(claim.get("evidence")) if str(item)],
    }


def _forbidden_claim_hits(text: str) -> list[dict[str, str]]:
    lowered = text.lower()
    return [
        {"phrase": phrase}
        for phrase in FORBIDDEN_CLAIM_PHRASES
        if phrase in lowered
    ]


def _source_claim_labels(source_claims: Any) -> str:
    labels = [
        f"{str(claim.get('level', ''))}:{str(claim.get('claim', ''))}"
        for claim in _list_value(source_claims)
        if isinstance(claim, Mapping)
    ]
    if not labels:
        return "none"
    return "; ".join(labels)


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


def _escape_table_text(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", "<br>")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate bounded method prose from evidence-bound power-ops method outline."
    )
    parser.add_argument(
        "--method-outline",
        default="docs/power_ops_action_invariance_evidence_bound_method_outline_2026-07-02.json",
    )
    parser.add_argument(
        "--out-md",
        default="docs/power_ops_action_invariance_evidence_bound_method_prose_2026-07-02.md",
    )
    parser.add_argument(
        "--out-json",
        default="docs/power_ops_action_invariance_evidence_bound_method_prose_2026-07-02.json",
    )
    args = parser.parse_args(argv)

    prose = build_evidence_bound_method_prose(method_outline_path=args.method_outline)
    write_evidence_bound_method_prose(prose, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
