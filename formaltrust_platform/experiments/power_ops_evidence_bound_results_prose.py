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


RESULTS_PARAGRAPHS = (
    (
        "fieldwise_repair_result",
        (
            "The curated fieldwise-repair row is the first §5 result paragraph: it is framed as "
            "field preservation for authorized fields and removal of unauthorized fields, with the "
            "claim bounded to the fieldwise-repair result JSON and its fully supported table row."
        ),
    ),
    (
        "expanded_metamorphic_skill_results",
        (
            "The expanded, metamorphic, and skill-authority fixtures extend the regression surface "
            "across larger case coverage, authority-confusion mutations, and no-RAG skill-driven "
            "multi-source authority without turning those fixtures into deployment evidence."
        ),
    ),
    (
        "baseline_grid",
        (
            "The baseline-grid paragraph should compare coarse intervention behavior with the "
            "fieldwise repair frame: strict blocking captures conservative collapse, provenance-only "
            "captures unsafe preservation, and fieldwise repair remains a bounded artifact result."
        ),
    ),
    (
        "performance_profile",
        (
            "The performance paragraph treats performance as safety-preserving normal behavior under "
            "the current fixtures, not as wall-clock latency, human workload reduction, or production "
            "operator efficiency."
        ),
    ),
    (
        "trace_replay_and_import",
        (
            "The trace paragraph groups trace replay, span/OTLP replay, and trace import as fixture "
            "evidence that external action records can feed the same fieldwise repair analysis; it "
            "does not claim production telemetry."
        ),
    ),
    (
        "multi_step_source_chain",
        (
            "The multi-step trace paragraph reports source-chain coverage for planner outputs, "
            "skills, tool metadata, memory, prior-step output, and user approval as local fixture "
            "evidence for multi-source authority accounting."
        ),
    ),
    (
        "claim_boundary",
        (
            "The results section closes by keeping every empirical statement inside the current "
            "curated, bridge, and trace-fixture boundary: no production telemetry, no official "
            "neighboring-system superiority claim, no real workload reduction, and no wall-clock "
            "latency claim."
        ),
    ),
)


def build_evidence_bound_results_prose(*, results_outline_path: str | Path) -> dict[str, Any]:
    outline = _load_json(results_outline_path)
    outline_items = [
        item
        for item in _list_value(outline.get("results_outline"))
        if isinstance(item, Mapping)
    ]
    if str(outline.get("results_outline_status", "")) != "ready" or not outline_items:
        return {
            "artifact_type": "power_ops_evidence_bound_results_prose",
            "source_results_outline": str(results_outline_path),
            "paper_section": str(outline.get("paper_section", "§5 Results and Analysis")),
            "results_prose_status": "blocked_no_ready_outline",
            "paragraph_count": 0,
            "results_text": "",
            "paragraphs": [],
            "forbidden_claim_hits": [],
        }

    by_slot = {str(item.get("slot", "")): item for item in outline_items}
    paragraphs = [
        _paragraph(text=text, source_item=by_slot.get(slot, outline_items[0]))
        for slot, text in RESULTS_PARAGRAPHS
    ]
    results_text = "\n\n".join(paragraph["text"] for paragraph in paragraphs)
    forbidden_hits = _forbidden_claim_hits(results_text)

    return {
        "artifact_type": "power_ops_evidence_bound_results_prose",
        "source_results_outline": str(results_outline_path),
        "paper_section": str(outline.get("paper_section", "§5 Results and Analysis")),
        "results_prose_status": "ready" if not forbidden_hits else "blocked_forbidden_claim",
        "paragraph_count": len(paragraphs),
        "results_text": results_text,
        "paragraphs": paragraphs,
        "forbidden_claim_hits": forbidden_hits,
    }


def render_evidence_bound_results_prose_markdown(prose: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Evidence-Bound Results Prose",
        "",
        f"**Status:** {prose.get('results_prose_status', '')}",
        f"**Paper section:** {prose.get('paper_section', '')}",
        f"**Paragraph count:** {int(prose.get('paragraph_count', 0) or 0)}",
        f"**Forbidden claim hits:** {len(_list_value(prose.get('forbidden_claim_hits')))}",
        "",
        "## Results Prose",
        "",
        str(prose.get("results_text", "")),
        "",
        "## Paragraph Evidence",
        "",
        "| Slot | Paragraph | Evidence paths | Table refs | Source claims | Limitation reason |",
        "|---|---|---|---|---|---|",
    ]
    for paragraph in _list_value(prose.get("paragraphs")):
        if not isinstance(paragraph, Mapping):
            continue
        lines.append(
            "| {slot} | {text} | {evidence} | {tables} | {claims} | {limitation} |".format(
                slot=_escape_table_text(str(paragraph.get("slot", ""))),
                text=_escape_table_text(str(paragraph.get("text", ""))),
                evidence=_escape_table_text("; ".join(str(path) for path in _list_value(paragraph.get("evidence_paths")))),
                tables=_escape_table_text(_table_ref_labels(paragraph.get("table_refs"))),
                claims=_escape_table_text(_source_claim_labels(paragraph.get("source_claims"))),
                limitation=_escape_table_text(str(paragraph.get("limitation_reason", ""))),
            )
        )
    lines.append("")
    return "\n".join(lines)


def write_evidence_bound_results_prose(
    prose: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_evidence_bound_results_prose_markdown(prose), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(prose, ensure_ascii=False, indent=2), encoding="utf-8")


def _paragraph(*, text: str, source_item: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "slot": str(source_item.get("slot", "")),
        "text": text,
        "evidence_paths": [str(path) for path in _list_value(source_item.get("evidence_paths")) if str(path)],
        "table_refs": [
            dict(ref)
            for ref in _list_value(source_item.get("table_refs"))
            if isinstance(ref, Mapping)
        ],
        "source_claims": [
            dict(claim)
            for claim in _list_value(source_item.get("source_claims"))
            if isinstance(claim, Mapping)
        ],
        "limitation_reason": str(source_item.get("limitation_reason", "")),
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


def _table_ref_labels(table_refs: Any) -> str:
    labels = [
        f"{str(ref.get('table', ''))}:{str(ref.get('row_label', ''))}:{str(ref.get('status', ''))}"
        for ref in _list_value(table_refs)
        if isinstance(ref, Mapping)
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
        description="Generate bounded results prose from an evidence-bound results outline."
    )
    parser.add_argument(
        "--results-outline",
        default="docs/power_ops_action_invariance_evidence_bound_results_outline_2026-07-02.json",
    )
    parser.add_argument(
        "--out-md",
        default="docs/power_ops_action_invariance_evidence_bound_results_prose_2026-07-02.md",
    )
    parser.add_argument(
        "--out-json",
        default="docs/power_ops_action_invariance_evidence_bound_results_prose_2026-07-02.json",
    )
    args = parser.parse_args(argv)

    prose = build_evidence_bound_results_prose(results_outline_path=args.results_outline)
    write_evidence_bound_results_prose(prose, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
