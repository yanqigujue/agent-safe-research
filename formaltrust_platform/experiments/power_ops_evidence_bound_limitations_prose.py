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

LIMITATION_PARAGRAPHS = (
    (
        "production_trace_gap",
        (
            "The current trace evidence remains fixture, bridge, span, OTLP, and import evidence. "
            "It supports local replay and import behavior, but production telemetry and live "
            "deployment safety remain outside the supported claim set."
        ),
    ),
    (
        "latency_gap",
        (
            "The current performance profile is a safety-preserving normal-behavior profile with "
            "a field-check proxy. It is not a wall-clock latency measurement and should not be read "
            "as a speed result."
        ),
    ),
    (
        "operator_workload_gap",
        (
            "The artifact has no operator-time study or human-subject workload measurement. Any "
            "real workload-reduction statement remains an excluded claim until reviewer-burden or "
            "operator-time evidence exists."
        ),
    ),
    (
        "official_benchmark_gap",
        (
            "The AgentDojo-style and semi-real bridge fixtures show that the interface can express "
            "neighboring benchmark shapes. They do not establish official benchmark superiority."
        ),
    ),
    (
        "forbidden_firstness_security_claims",
        (
            "The paper should not frame the artifact as a generic firstness, general runtime "
            "enforcement, least-privilege, or prompt-injection solution. The defensible scope is "
            "field-level action invariance with authority witnesses and repair validity."
        ),
    ),
    (
        "next_experiments",
        (
            "The next experiments follow directly from the excluded-claim binding: collect reviewed "
            "traces, measure wall-clock timing, run operator workload studies, and run official "
            "benchmark comparisons under pre-registered rules."
        ),
    ),
)


def build_evidence_bound_limitations_prose(
    *,
    limitations_outline_path: str | Path,
) -> dict[str, Any]:
    outline = _load_json(limitations_outline_path)
    outline_items = [
        item
        for item in _list_value(outline.get("limitations_outline"))
        if isinstance(item, Mapping)
    ]
    if str(outline.get("limitations_outline_status", "")) != "ready" or not outline_items:
        return {
            "artifact_type": "power_ops_evidence_bound_limitations_prose",
            "source_limitations_outline": str(limitations_outline_path),
            "paper_section": str(outline.get("paper_section", "§6 Limitations and Next Experiments")),
            "limitations_prose_status": "blocked_no_ready_outline",
            "paragraph_count": 0,
            "limitations_text": "",
            "paragraphs": [],
            "forbidden_claim_hits": [],
        }

    by_slot = {str(item.get("slot", "")): item for item in outline_items}
    paragraphs = [
        _paragraph(text=text, source_item=by_slot.get(slot, outline_items[0]))
        for slot, text in LIMITATION_PARAGRAPHS
    ]
    limitations_text = "\n\n".join(paragraph["text"] for paragraph in paragraphs)
    forbidden_hits = _forbidden_claim_hits(limitations_text)

    return {
        "artifact_type": "power_ops_evidence_bound_limitations_prose",
        "source_limitations_outline": str(limitations_outline_path),
        "paper_section": str(outline.get("paper_section", "§6 Limitations and Next Experiments")),
        "limitations_prose_status": "ready" if not forbidden_hits else "blocked_forbidden_claim",
        "paragraph_count": len(paragraphs),
        "limitations_text": limitations_text,
        "paragraphs": paragraphs,
        "forbidden_claim_hits": forbidden_hits,
    }


def render_evidence_bound_limitations_prose_markdown(prose: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Evidence-Bound Limitations Prose",
        "",
        f"**Status:** {prose.get('limitations_prose_status', '')}",
        f"**Paper section:** {prose.get('paper_section', '')}",
        f"**Paragraph count:** {int(prose.get('paragraph_count', 0) or 0)}",
        f"**Forbidden claim hits:** {len(_list_value(prose.get('forbidden_claim_hits')))}",
        "",
        "## Limitations Prose",
        "",
        str(prose.get("limitations_text", "")),
        "",
        "## Paragraph Evidence",
        "",
        "| Slot | Paragraph | Excluded claim binding | Future work | Source refs |",
        "|---|---|---|---|---|",
    ]
    for paragraph in _list_value(prose.get("paragraphs")):
        if not isinstance(paragraph, Mapping):
            continue
        lines.append(
            "| {slot} | {text} | {excluded} | {future} | {refs} |".format(
                slot=_escape_table_text(str(paragraph.get("slot", ""))),
                text=_escape_table_text(str(paragraph.get("text", ""))),
                excluded=_escape_table_text(_excluded_claim_binding_label(paragraph)),
                future=_escape_table_text("; ".join(str(work) for work in _list_value(paragraph.get("future_work")))),
                refs=_escape_table_text("; ".join(str(ref) for ref in _list_value(paragraph.get("source_refs")))),
            )
        )
    lines.append("")
    return "\n".join(lines)


def write_evidence_bound_limitations_prose(
    prose: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_evidence_bound_limitations_prose_markdown(prose), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(prose, ensure_ascii=False, indent=2), encoding="utf-8")


def _paragraph(*, text: str, source_item: Mapping[str, Any]) -> dict[str, Any]:
    excluded_claims = [
        str(claim)
        for claim in _list_value(source_item.get("excluded_claims"))
        if str(claim)
    ]
    future_work = [
        str(work)
        for work in _list_value(source_item.get("future_work"))
        if str(work)
    ]
    return {
        "slot": str(source_item.get("slot", "")),
        "text": text,
        "excluded_claims": excluded_claims,
        "excluded_claim_count": len(excluded_claims),
        "future_work": future_work,
        "source_refs": [
            str(ref)
            for ref in _list_value(source_item.get("source_refs"))
            if str(ref)
        ],
    }


def _excluded_claim_binding_label(paragraph: Mapping[str, Any]) -> str:
    count = int(paragraph.get("excluded_claim_count", 0) or 0)
    if count == 0:
        return "none"
    return f"{count} excluded claim binding"


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
        description="Generate bounded limitations prose from an evidence-bound limitations outline."
    )
    parser.add_argument(
        "--limitations-outline",
        default="docs/power_ops_action_invariance_evidence_bound_limitations_outline_2026-07-02.json",
    )
    parser.add_argument(
        "--out-md",
        default="docs/power_ops_action_invariance_evidence_bound_limitations_prose_2026-07-02.md",
    )
    parser.add_argument(
        "--out-json",
        default="docs/power_ops_action_invariance_evidence_bound_limitations_prose_2026-07-02.json",
    )
    args = parser.parse_args(argv)

    prose = build_evidence_bound_limitations_prose(limitations_outline_path=args.limitations_outline)
    write_evidence_bound_limitations_prose(prose, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
