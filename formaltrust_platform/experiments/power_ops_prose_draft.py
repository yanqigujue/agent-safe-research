from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping


FORBIDDEN_CLAIM_PHRASES = (
    "first LLM-agent guardrail",
    "first runtime enforcement framework",
    "first least-privilege LLM-agent security framework",
    "solves prompt injection",
    "proves production safety",
    "outperforms official neighboring systems",
    "reduces real human workload without operator-time evidence",
)


def build_prose_draft(skeleton_path: str | Path) -> dict[str, Any]:
    skeleton = _load_json(skeleton_path)
    result_readback = [
        _mapping_value(item)
        for item in _list_value(skeleton.get("result_readback"))
        if isinstance(item, Mapping)
    ]
    claim_paragraphs = [
        _mapping_value(paragraph)
        for paragraph in _list_value(skeleton.get("paragraphs"))
        if isinstance(paragraph, Mapping)
    ]
    paragraphs_by_section: dict[str, list[dict[str, Any]]] = {}
    for paragraph in claim_paragraphs:
        paragraphs_by_section.setdefault(str(paragraph.get("section", "")), []).append(paragraph)

    sections = [
        _prose_section(
            section=_mapping_value(section),
            claim_paragraphs=paragraphs_by_section.get(str(_mapping_value(section).get("section", "")), []),
            result_readback=result_readback,
        )
        for section in _list_value(skeleton.get("sections"))
        if isinstance(section, Mapping)
    ]
    forbidden_hits = _forbidden_claim_hits(sections)

    return {
        "artifact_type": "power_ops_action_invariance_prose_draft",
        "source_skeleton": str(skeleton_path),
        "title": skeleton.get("title", "Field-Level Action Invariance"),
        "date": skeleton.get("date", "unknown"),
        "sections": sections,
        "result_readback": result_readback,
        "forbidden_claim_hits": forbidden_hits,
        "revision_rules": [
            "Treat every prose paragraph as bounded by its evidence list.",
            "Use result readback for numeric statements before copying any number into the paper.",
            "Keep deployment, workload, and official benchmark claims in limitations until evidence exists.",
        ],
    }


def render_prose_draft_markdown(draft: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Action Invariance Prose Draft",
        "",
        f"**Title:** {draft.get('title', '')}",
        f"**Date:** {draft.get('date', '')}",
        f"**Forbidden claim hits:** {len(_list_value(draft.get('forbidden_claim_hits')))}",
        "",
    ]

    for section in _list_value(draft.get("sections")):
        if not isinstance(section, Mapping):
            continue
        lines.extend(
            [
                f"## {section.get('section', '')}",
                "",
                f"**Purpose:** {section.get('goal', '')}",
                "",
            ]
        )
        for paragraph in _list_value(section.get("paragraphs")):
            if not isinstance(paragraph, Mapping):
                continue
            lines.extend(
                [
                    str(paragraph.get("text", "")),
                    "",
                    f"Evidence: {_inline_code_list(paragraph.get('evidence'))}",
                    f"Safe use: {paragraph.get('safe_use', '')}",
                ]
            )
            support_readback = str(paragraph.get("support_readback", ""))
            if support_readback:
                lines.append(f"Result readback: {support_readback}")
            lines.append("")

    lines.extend(
        [
            "## Result Readback",
            "",
            "| Artifact | Path | Key readback |",
            "|---|---|---|",
        ]
    )
    for artifact in _list_value(draft.get("result_readback")):
        if isinstance(artifact, Mapping):
            lines.append(
                "| {artifact_type} | `{path}` | {readback} |".format(
                    artifact_type=artifact.get("artifact_type", ""),
                    path=artifact.get("path", ""),
                    readback=artifact.get("key_readback", ""),
                )
            )

    lines.extend(
        [
            "",
            "## Revision Rules",
            "",
        ]
    )
    for rule in _list_value(draft.get("revision_rules")):
        lines.append(f"- {rule}")
    lines.append("")
    return "\n".join(lines)


def write_prose_draft(
    draft: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_prose_draft_markdown(draft), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.write_text(json.dumps(draft, ensure_ascii=False, indent=2), encoding="utf-8")


def _prose_section(
    *,
    section: Mapping[str, Any],
    claim_paragraphs: list[Mapping[str, Any]],
    result_readback: list[Mapping[str, Any]],
) -> dict[str, Any]:
    section_name = str(section.get("section", ""))
    if not claim_paragraphs:
        paragraphs = [_no_evidence_paragraph(section)]
    else:
        paragraphs = [
            _prose_paragraph_from_claim(
                claim=paragraph,
                result_readback=result_readback,
            )
            for paragraph in claim_paragraphs
        ]
    return {
        "section": section_name,
        "goal": str(section.get("goal", "")),
        "paragraphs": paragraphs,
    }


def _no_evidence_paragraph(section: Mapping[str, Any]) -> dict[str, Any]:
    section_name = str(section.get("section", ""))
    goal = str(section.get("goal", ""))
    return {
        "source_claim": "",
        "text": (
            f"This section should be drafted around its purpose, but it currently has no "
            f"supported claim assigned in the artifact map: {goal}"
        ),
        "section": section_name,
        "evidence": [],
        "safe_use": "Use as structure only until a supported claim is assigned.",
        "support_readback": "",
        "evidence_status": "no_supported_claim",
    }


def _prose_paragraph_from_claim(
    *,
    claim: Mapping[str, Any],
    result_readback: list[Mapping[str, Any]],
) -> dict[str, Any]:
    claim_text = str(claim.get("claim", ""))
    level = str(claim.get("level", ""))
    evidence = [str(item) for item in _list_value(claim.get("evidence")) if str(item)]
    safe_use = str(claim.get("safe_use", "Use with the stated evidence level."))
    support_readback = _support_readback_for_evidence(evidence, result_readback)
    text = (
        f"The current artifact supports the following bounded {level} statement: "
        f"{claim_text}. This paragraph should be cited only with the attached evidence "
        f"and interpreted under its safe-use constraint."
    )
    return {
        "source_claim": claim_text,
        "text": text,
        "section": str(claim.get("section", "")),
        "level": level,
        "evidence": evidence,
        "safe_use": safe_use,
        "support_readback": support_readback,
        "evidence_status": "evidence_bound" if evidence else "missing_evidence",
    }


def _support_readback_for_evidence(
    evidence: list[str],
    result_readback: list[Mapping[str, Any]],
) -> str:
    matches: list[str] = []
    normalized_evidence = {_normalize_path(item) for item in evidence}
    for artifact in result_readback:
        artifact_path = _normalize_path(str(artifact.get("path", "")))
        if artifact_path in normalized_evidence:
            readback = str(artifact.get("key_readback", ""))
            if readback:
                matches.append(readback)
    return " | ".join(matches)


def _forbidden_claim_hits(sections: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
    draft_text = "\n".join(
        str(paragraph.get("text", ""))
        for section in sections
        for paragraph in _list_value(section.get("paragraphs"))
        if isinstance(paragraph, Mapping)
    ).lower()
    hits: list[dict[str, Any]] = []
    for phrase in FORBIDDEN_CLAIM_PHRASES:
        if phrase.lower() in draft_text:
            hits.append({"claim": phrase})
    return hits


def _normalize_path(value: str) -> str:
    return value.replace("\\", "/")


def _inline_code_list(value: Any) -> str:
    items = [str(item) for item in _list_value(value) if str(item)]
    if not items:
        return "none"
    return ", ".join(f"`{item}`" for item in items)


def _load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object at {path}")
    return payload


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
        description="Build an evidence-constrained prose draft for power-ops action invariance."
    )
    parser.add_argument(
        "--skeleton",
        default="docs/power_ops_action_invariance_draft_skeleton_2026-07-02.json",
    )
    parser.add_argument(
        "--out-md",
        default="docs/power_ops_action_invariance_prose_draft_2026-07-02.md",
    )
    parser.add_argument(
        "--out-json",
        default="docs/power_ops_action_invariance_prose_draft_2026-07-02.json",
    )
    args = parser.parse_args(argv)

    draft = build_prose_draft(args.skeleton)
    write_prose_draft(draft, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
