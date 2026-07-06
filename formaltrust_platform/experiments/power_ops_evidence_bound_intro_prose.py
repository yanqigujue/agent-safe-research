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


def build_evidence_bound_intro_prose(*, intro_outline_path: str | Path) -> dict[str, Any]:
    intro = _load_json(intro_outline_path)
    outline = [
        item
        for item in _list_value(intro.get("paragraph_outline"))
        if isinstance(item, Mapping)
    ]
    if str(intro.get("intro_status", "")) != "ready" or not outline:
        return {
            "artifact_type": "power_ops_evidence_bound_intro_prose",
            "source_intro_outline": str(intro_outline_path),
            "intro_prose_status": "blocked_no_ready_outline",
            "intro_text": "",
            "paragraphs": [],
            "forbidden_claim_hits": [],
        }

    by_slot = {str(item.get("slot", "")): item for item in outline}
    paragraphs = [
        _paragraph(
            text=(
                "Strict supervision of high-risk power-operation LLM agents should not collapse every "
                "mixed-authority action into a full block; it should preserve authorized work while "
                "removing invalid authority fields."
            ),
            source_item=by_slot.get("problem", outline[0]),
        ),
        _paragraph(
            text=(
                "The current paper therefore frames the problem as field-scoped authority preservation "
                "under intervention, not as a firstness, production-safety, or generic agent-security "
                "claim."
            ),
            source_item=by_slot.get("gap", outline[0]),
        ),
        _paragraph(
            text=(
                "Our artifact instantiates this boundary through fieldwise repair and a "
                "readiness-linked claim ledger that keeps each writing claim tied to evidence."
            ),
            source_item=by_slot.get("method", outline[0]),
        ),
        _paragraph(
            text=(
                "The current paper-ready pool covers curated, expanded, metamorphic, skill, baseline, "
                "and trace evidence, while treating these fixtures as bounded evaluation artifacts."
            ),
            source_item=by_slot.get("evidence", outline[0]),
        ),
        _paragraph(
            text=(
                "We explicitly leave production telemetry, real operator workload reduction, and "
                "official neighboring-system superiority outside the current claim set."
            ),
            source_item=by_slot.get("boundary", outline[0]),
        ),
    ]
    intro_text = "\n\n".join(paragraph["text"] for paragraph in paragraphs)
    forbidden_hits = _forbidden_claim_hits(intro_text)

    return {
        "artifact_type": "power_ops_evidence_bound_intro_prose",
        "source_intro_outline": str(intro_outline_path),
        "intro_prose_status": "ready" if not forbidden_hits else "blocked_forbidden_claim",
        "paragraph_count": len(paragraphs),
        "intro_text": intro_text,
        "paragraphs": paragraphs,
        "forbidden_claim_hits": forbidden_hits,
    }


def render_evidence_bound_intro_prose_markdown(prose: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Evidence-Bound Introduction Prose",
        "",
        f"**Status:** {prose.get('intro_prose_status', '')}",
        f"**Paragraph count:** {int(prose.get('paragraph_count', 0))}",
        f"**Forbidden claim hits:** {len(_list_value(prose.get('forbidden_claim_hits')))}",
        "",
        "## Introduction Prose",
        "",
        str(prose.get("intro_text", "")),
        "",
        "## Paragraph Evidence",
        "",
        "| Slot | Paragraph | Source claims | Limitation reason |",
        "|---|---|---|---|",
    ]
    for paragraph in _list_value(prose.get("paragraphs")):
        if not isinstance(paragraph, Mapping):
            continue
        lines.append(
            "| {slot} | {text} | {claims} | {limitation} |".format(
                slot=_escape_table_text(str(paragraph.get("slot", ""))),
                text=_escape_table_text(str(paragraph.get("text", ""))),
                claims=_escape_table_text(_source_claim_labels(paragraph.get("source_claims"))),
                limitation=_escape_table_text(str(paragraph.get("limitation_reason", ""))),
            )
        )
    lines.append("")
    return "\n".join(lines)


def write_evidence_bound_intro_prose(
    prose: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_evidence_bound_intro_prose_markdown(prose), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(prose, ensure_ascii=False, indent=2), encoding="utf-8")


def _paragraph(*, text: str, source_item: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "slot": str(source_item.get("slot", "")),
        "text": text,
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
        description="Generate bounded introduction prose from evidence-bound power-ops intro outline."
    )
    parser.add_argument(
        "--intro-outline",
        default="docs/power_ops_action_invariance_evidence_bound_intro_2026-07-02.json",
    )
    parser.add_argument(
        "--out-md",
        default="docs/power_ops_action_invariance_evidence_bound_intro_prose_2026-07-02.md",
    )
    parser.add_argument(
        "--out-json",
        default="docs/power_ops_action_invariance_evidence_bound_intro_prose_2026-07-02.json",
    )
    args = parser.parse_args(argv)

    prose = build_evidence_bound_intro_prose(intro_outline_path=args.intro_outline)
    write_evidence_bound_intro_prose(prose, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
