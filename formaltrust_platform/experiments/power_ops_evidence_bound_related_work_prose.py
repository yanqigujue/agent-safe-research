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

RELATED_WORK_PARAGRAPHS = (
    (
        "runtime_enforcement_neighbors",
        (
            "AgentSpec and formal-security-agent work already establish broad runtime enforcement "
            "and formal monitoring as neighboring territory. We therefore frame this paper around a "
            "narrower object: field-level action invariance inside a structured candidate action."
        ),
    ),
    (
        "prompt_injection_privilege_neighbors",
        (
            "AgentVisor, AgentSentry, and CaMeL cover semantic privilege separation, safe "
            "continuation, and capability-style prompt-injection defenses. Our positioning is that "
            "CapGuard repairs structured action fields after authority decisions and records why "
            "preserved fields remain allowed."
        ),
    ),
    (
        "least_privilege_capability_neighbors",
        (
            "ToolPrivBench and RACG make least privilege and capability minimization close "
            "neighbors. The distinction here is below tool exposure: after a mixed action is "
            "formed, each field must still be justified by the authority of its source."
        ),
    ),
    (
        "over_conservatism_neighbors",
        (
            "InjecGuard, AgentSentry, and AgentVisor already motivate over-defense and security "
            "utility tradeoffs. We use that motivation only to define a measurable failure mode: "
            "authorized final-field loss under strict intervention."
        ),
    ),
    (
        "action_invariance_delta",
        (
            "The safe contribution is field-level action invariance with authority witnesses and "
            "repair-frame validity: preserve authorized fields, remove invalid fields, and expose "
            "the evidence that supports every preserved field."
        ),
    ),
    (
        "claim_boundary",
        (
            "The related-work boundary is explicit. The current artifact does not use production "
            "telemetry, does not make an official neighboring-system superiority claim, does not "
            "claim generic agent-security firstness, and does not claim real workload reduction."
        ),
    ),
)


def build_evidence_bound_related_work_prose(
    *,
    related_work_outline_path: str | Path,
) -> dict[str, Any]:
    outline = _load_json(related_work_outline_path)
    outline_items = [
        item
        for item in _list_value(outline.get("related_work_outline"))
        if isinstance(item, Mapping)
    ]
    if str(outline.get("related_work_outline_status", "")) != "ready" or not outline_items:
        return {
            "artifact_type": "power_ops_evidence_bound_related_work_prose",
            "source_related_work_outline": str(related_work_outline_path),
            "paper_section": str(outline.get("paper_section", "§2 Related Work and Novelty Boundary")),
            "related_work_prose_status": "blocked_no_ready_outline",
            "paragraph_count": 0,
            "related_work_text": "",
            "paragraphs": [],
            "forbidden_claim_hits": [],
        }

    by_slot = {str(item.get("slot", "")): item for item in outline_items}
    paragraphs = [
        _paragraph(text=text, source_item=by_slot.get(slot, outline_items[0]))
        for slot, text in RELATED_WORK_PARAGRAPHS
    ]
    related_work_text = "\n\n".join(paragraph["text"] for paragraph in paragraphs)
    forbidden_hits = _forbidden_claim_hits(related_work_text)

    return {
        "artifact_type": "power_ops_evidence_bound_related_work_prose",
        "source_related_work_outline": str(related_work_outline_path),
        "paper_section": str(outline.get("paper_section", "§2 Related Work and Novelty Boundary")),
        "related_work_prose_status": "ready" if not forbidden_hits else "blocked_forbidden_claim",
        "paragraph_count": len(paragraphs),
        "related_work_text": related_work_text,
        "paragraphs": paragraphs,
        "forbidden_claim_hits": forbidden_hits,
    }


def render_evidence_bound_related_work_prose_markdown(prose: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Evidence-Bound Related Work Prose",
        "",
        f"**Status:** {prose.get('related_work_prose_status', '')}",
        f"**Paper section:** {prose.get('paper_section', '')}",
        f"**Paragraph count:** {int(prose.get('paragraph_count', 0) or 0)}",
        f"**Forbidden claim hits:** {len(_list_value(prose.get('forbidden_claim_hits')))}",
        "",
        "## Related Work Prose",
        "",
        str(prose.get("related_work_text", "")),
        "",
        "## Paragraph Evidence",
        "",
        "| Slot | Paragraph | Neighbors | Source refs | Safe delta | Boundary |",
        "|---|---|---|---|---|---|",
    ]
    for paragraph in _list_value(prose.get("paragraphs")):
        if not isinstance(paragraph, Mapping):
            continue
        lines.append(
            "| {slot} | {text} | {neighbors} | {refs} | {delta} | {boundary} |".format(
                slot=_escape_table_text(str(paragraph.get("slot", ""))),
                text=_escape_table_text(str(paragraph.get("text", ""))),
                neighbors=_escape_table_text("; ".join(str(x) for x in _list_value(paragraph.get("neighbor_papers")))),
                refs=_escape_table_text("; ".join(str(x) for x in _list_value(paragraph.get("source_refs")))),
                delta=_escape_table_text(str(paragraph.get("safe_delta", ""))),
                boundary=_escape_table_text(str(paragraph.get("claim_boundary", ""))),
            )
        )
    lines.append("")
    return "\n".join(lines)


def write_evidence_bound_related_work_prose(
    prose: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_evidence_bound_related_work_prose_markdown(prose), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(prose, ensure_ascii=False, indent=2), encoding="utf-8")


def _paragraph(*, text: str, source_item: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "slot": str(source_item.get("slot", "")),
        "text": text,
        "neighbor_papers": [str(item) for item in _list_value(source_item.get("neighbor_papers")) if str(item)],
        "pressure": str(source_item.get("pressure", "")),
        "safe_delta": str(source_item.get("safe_delta", "")),
        "claim_boundary": str(source_item.get("claim_boundary", "")),
        "source_refs": [str(ref) for ref in _list_value(source_item.get("source_refs")) if str(ref)],
    }


def _forbidden_claim_hits(text: str) -> list[dict[str, str]]:
    lowered = text.lower()
    return [
        {"phrase": phrase}
        for phrase in FORBIDDEN_CLAIM_PHRASES
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


def _escape_table_text(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", "<br>")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate bounded related-work prose from an evidence-bound outline."
    )
    parser.add_argument(
        "--related-work-outline",
        default="docs/power_ops_action_invariance_evidence_bound_related_work_outline_2026-07-02.json",
    )
    parser.add_argument(
        "--out-md",
        default="docs/power_ops_action_invariance_evidence_bound_related_work_prose_2026-07-02.md",
    )
    parser.add_argument(
        "--out-json",
        default="docs/power_ops_action_invariance_evidence_bound_related_work_prose_2026-07-02.json",
    )
    args = parser.parse_args(argv)

    prose = build_evidence_bound_related_work_prose(related_work_outline_path=args.related_work_outline)
    write_evidence_bound_related_work_prose(prose, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
