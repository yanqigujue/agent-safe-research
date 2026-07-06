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


def build_evidence_bound_intro(
    *,
    skeleton_path: str | Path,
    abstract_path: str | Path,
) -> dict[str, Any]:
    skeleton = _load_json(skeleton_path)
    abstract = _load_json(abstract_path)
    bullets = [
        item
        for item in _list_value(skeleton.get("intro_contribution_bullets"))
        if isinstance(item, Mapping)
    ]
    if str(skeleton.get("abstract_status", "")) != "ready" or not bullets:
        return {
            "artifact_type": "power_ops_evidence_bound_intro",
            "source_skeleton": str(skeleton_path),
            "source_abstract": str(abstract_path),
            "intro_status": "blocked_no_ready_bullets",
            "paragraph_outline": [],
            "forbidden_claim_hits": [],
        }

    by_slot = {str(item.get("slot", "")): item for item in bullets}
    formulation = by_slot.get("formulation", bullets[0])
    implementation = by_slot.get("implementation", bullets[0])
    evaluation = by_slot.get("evaluation", bullets[-1])
    boundary = by_slot.get("boundary", bullets[-1])

    paragraphs = [
        _paragraph(
            slot="problem",
            role="Motivate field-level action invariance for supervised high-risk power-operation agents.",
            outline_text=(
                "Open with the problem that strict supervision should preserve authorized work while "
                "removing invalid authority fields."
            ),
            source_item=formulation,
        ),
        _paragraph(
            slot="gap",
            role="Separate the paper from generic runtime enforcement or broad agent safety.",
            outline_text=(
                "State the gap as field-scoped authority preservation under intervention, not a claim "
                "of production safety or firstness."
            ),
            source_item=boundary,
            limitation_reason="Keep firstness, production, workload, and official-superiority claims out.",
        ),
        _paragraph(
            slot="method",
            role="Introduce fieldwise repair and auditable claim readiness.",
            outline_text=(
                "Describe the implementation as fieldwise repair plus claim/readiness artifacts that keep "
                "each statement evidence-bound."
            ),
            source_item=implementation,
        ),
        _paragraph(
            slot="evidence",
            role="Summarize only the paper-ready evidence pool.",
            outline_text=(
                "List curated, expanded, metamorphic, skill, baseline, and trace evidence without promoting "
                "the fixtures into deployment evidence."
            ),
            source_item=evaluation,
        ),
        _paragraph(
            slot="boundary",
            role="End the introduction preview with explicit limitations.",
            outline_text=(
                "Close the introduction preview by saying there is no production telemetry, no real operator "
                "workload reduction claim, and no official neighboring-system superiority claim."
            ),
            source_item=boundary,
            limitation_reason="No production telemetry; no real workload reduction; no official superiority.",
        ),
    ]
    outline_text = "\n".join(item["outline_text"] for item in paragraphs)
    forbidden_hits = _forbidden_claim_hits(outline_text)

    return {
        "artifact_type": "power_ops_evidence_bound_intro",
        "source_skeleton": str(skeleton_path),
        "source_abstract": str(abstract_path),
        "abstract_status": str(abstract.get("abstract_status", "")),
        "intro_status": "ready" if not forbidden_hits else "blocked_forbidden_claim",
        "paragraph_outline": paragraphs,
        "forbidden_claim_hits": forbidden_hits,
    }


def render_evidence_bound_intro_markdown(intro: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Evidence-Bound Introduction Outline",
        "",
        f"**Status:** {intro.get('intro_status', '')}",
        f"**Forbidden claim hits:** {len(_list_value(intro.get('forbidden_claim_hits')))}",
        "",
        "## Paragraph Outline",
        "",
        "| Slot | Role | Outline | Source claims | Limitation reason |",
        "|---|---|---|---|---|",
    ]
    for paragraph in _list_value(intro.get("paragraph_outline")):
        if not isinstance(paragraph, Mapping):
            continue
        lines.append(
            "| {slot} | {role} | {outline} | {claims} | {limitation} |".format(
                slot=_escape_table_text(str(paragraph.get("slot", ""))),
                role=_escape_table_text(str(paragraph.get("role", ""))),
                outline=_escape_table_text(str(paragraph.get("outline_text", ""))),
                claims=_escape_table_text(_source_claim_labels(paragraph.get("source_claims"))),
                limitation=_escape_table_text(str(paragraph.get("limitation_reason", ""))),
            )
        )
    lines.append("")
    return "\n".join(lines)


def write_evidence_bound_intro(
    intro: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_evidence_bound_intro_markdown(intro), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(intro, ensure_ascii=False, indent=2), encoding="utf-8")


def _paragraph(
    *,
    slot: str,
    role: str,
    outline_text: str,
    source_item: Mapping[str, Any],
    limitation_reason: str = "",
) -> dict[str, Any]:
    return {
        "slot": slot,
        "role": role,
        "outline_text": outline_text,
        "source_claims": [
            _source_claim_summary(claim)
            for claim in _list_value(source_item.get("source_claims"))
            if isinstance(claim, Mapping)
        ],
        "limitation_reason": limitation_reason,
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
    return value.replace("|", "\\|")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate introduction outline from evidence-bound power-ops abstract artifacts."
    )
    parser.add_argument(
        "--skeleton",
        default="docs/power_ops_action_invariance_readiness_bound_abstract_2026-07-02.json",
    )
    parser.add_argument(
        "--abstract",
        default="docs/power_ops_action_invariance_evidence_bound_abstract_2026-07-02.json",
    )
    parser.add_argument(
        "--out-md",
        default="docs/power_ops_action_invariance_evidence_bound_intro_2026-07-02.md",
    )
    parser.add_argument(
        "--out-json",
        default="docs/power_ops_action_invariance_evidence_bound_intro_2026-07-02.json",
    )
    args = parser.parse_args(argv)

    intro = build_evidence_bound_intro(
        skeleton_path=args.skeleton,
        abstract_path=args.abstract,
    )
    write_evidence_bound_intro(intro, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
