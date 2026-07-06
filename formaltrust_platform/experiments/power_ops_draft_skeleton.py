from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping


def build_draft_skeleton(artifact_map_path: str | Path) -> dict[str, Any]:
    artifact_map = _load_json(artifact_map_path)
    sections = [
        _section_skeleton(section)
        for section in _list_value(artifact_map.get("section_plan"))
        if isinstance(section, Mapping)
    ]
    paragraphs = [
        _paragraph_skeleton(claim)
        for claim in _list_value(artifact_map.get("claims_evidence_matrix"))
        if isinstance(claim, Mapping)
    ]
    result_readback = [
        _result_readback(artifact)
        for artifact in _list_value(artifact_map.get("result_artifacts"))
        if isinstance(artifact, Mapping)
    ]
    forbidden_hits = _forbidden_claim_hits(
        paragraphs=paragraphs,
        forbidden_claims=_list_value(artifact_map.get("forbidden_claims")),
    )

    return {
        "artifact_type": "power_ops_action_invariance_draft_skeleton",
        "source_artifact_map": str(artifact_map_path),
        "title": artifact_map.get("title", "Field-Level Action Invariance"),
        "date": artifact_map.get("date", "unknown"),
        "sections": sections,
        "paragraphs": paragraphs,
        "result_readback": result_readback,
        "forbidden_claim_hits": forbidden_hits,
        "claim_bound_paragraph_count": len(paragraphs),
        "evidence_bound_paragraph_count": sum(1 for paragraph in paragraphs if paragraph["evidence"]),
        "next_revision_rules": [
            "Keep every result sentence attached to one or more evidence artifacts.",
            "Do not promote fixture evidence into production telemetry evidence.",
            "Keep wall-clock latency and operator workload as missing-evidence limitations.",
        ],
    }


def render_draft_skeleton_markdown(skeleton: Mapping[str, Any]) -> str:
    paragraphs_by_section: dict[str, list[Mapping[str, Any]]] = {}
    for paragraph in _list_value(skeleton.get("paragraphs")):
        if isinstance(paragraph, Mapping):
            paragraphs_by_section.setdefault(str(paragraph.get("section", "")), []).append(paragraph)

    lines = [
        "# Power-Ops Action Invariance Draft Skeleton",
        "",
        f"**Title:** {skeleton.get('title', '')}",
        f"**Date:** {skeleton.get('date', '')}",
        f"**Claim-bound paragraphs:** {int(skeleton.get('claim_bound_paragraph_count', 0))}",
        f"**Evidence-bound paragraphs:** {int(skeleton.get('evidence_bound_paragraph_count', 0))}",
        f"**Forbidden claim hits:** {len(_list_value(skeleton.get('forbidden_claim_hits')))}",
        "",
        "## Draft Sections",
        "",
    ]

    for section in _list_value(skeleton.get("sections")):
        if not isinstance(section, Mapping):
            continue
        section_name = str(section.get("section", ""))
        lines.extend(
            [
                f"## {section_name}",
                "",
                f"**Purpose:** {section.get('goal', '')}",
                f"**Evidence discipline:** {section.get('evidence_role', '')}",
                "",
            ]
        )
        section_paragraphs = paragraphs_by_section.get(section_name, [])
        if not section_paragraphs:
            lines.extend(
                [
                    "- Draft note: no supported claim is currently assigned to this section.",
                    "",
                ]
            )
            continue
        for paragraph in section_paragraphs:
            evidence = ", ".join(f"`{item}`" for item in _list_value(paragraph.get("evidence")))
            lines.extend(
                [
                    f"- Claim ({paragraph.get('level', '')}): {paragraph.get('claim', '')}",
                    f"  Evidence: {evidence}",
                    f"  Safe use: {paragraph.get('safe_use', '')}",
                    f"  Draft stub: {paragraph.get('draft_stub', '')}",
                    "",
                ]
            )

    lines.extend(
        [
            "## Result Readback",
            "",
            "| Artifact | Path | Key readback |",
            "|---|---|---|",
        ]
    )
    for artifact in _list_value(skeleton.get("result_readback")):
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
    for rule in _list_value(skeleton.get("next_revision_rules")):
        lines.append(f"- {rule}")
    lines.append("")
    return "\n".join(lines)


def write_draft_skeleton(
    skeleton: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_draft_skeleton_markdown(skeleton), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(skeleton, ensure_ascii=False, indent=2), encoding="utf-8")


def _section_skeleton(section: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "section": str(section.get("section", "")),
        "goal": str(section.get("goal", "")),
        "evidence_role": str(section.get("evidence_role", "")),
    }


def _paragraph_skeleton(claim: Mapping[str, Any]) -> dict[str, Any]:
    claim_text = str(claim.get("claim", ""))
    level = str(claim.get("level", ""))
    evidence = [str(item) for item in _list_value(claim.get("evidence")) if str(item)]
    safe_use = str(claim.get("safe_use", "Use with the stated evidence level."))
    return {
        "claim": claim_text,
        "level": level,
        "section": str(claim.get("section", "")),
        "evidence": evidence,
        "safe_use": safe_use,
        "draft_stub": _draft_stub_for_claim(claim_text, level, evidence),
    }


def _draft_stub_for_claim(claim: str, level: str, evidence: list[str]) -> str:
    if evidence:
        evidence_phrase = " and ".join(Path(item).name for item in evidence[:2])
        return f"Use this {level} claim only with evidence from {evidence_phrase}."
    return f"Use this {level} claim only after adding explicit evidence."


def _result_readback(artifact: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_type": str(artifact.get("artifact_type", "")),
        "path": str(artifact.get("path", "")),
        "key_readback": str(artifact.get("key_readback", "")),
    }


def _forbidden_claim_hits(
    *,
    paragraphs: list[Mapping[str, Any]],
    forbidden_claims: list[Any],
) -> list[dict[str, Any]]:
    draft_text = "\n".join(
        str(paragraph.get("claim", "")) + "\n" + str(paragraph.get("draft_stub", ""))
        for paragraph in paragraphs
    ).lower()
    hits: list[dict[str, Any]] = []
    for claim in forbidden_claims:
        phrase = str(claim)
        if phrase and phrase.lower() in draft_text:
            hits.append({"claim": phrase})
    return hits


def _load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build an evidence-bound paper draft skeleton for power-ops action invariance."
    )
    parser.add_argument(
        "--artifact-map",
        default="docs/power_ops_action_invariance_paper_outline_2026-07-02.json",
    )
    parser.add_argument(
        "--out-md",
        default="docs/power_ops_action_invariance_draft_skeleton_2026-07-02.md",
    )
    parser.add_argument(
        "--out-json",
        default="docs/power_ops_action_invariance_draft_skeleton_2026-07-02.json",
    )
    args = parser.parse_args(argv)

    skeleton = build_draft_skeleton(args.artifact_map)
    write_draft_skeleton(skeleton, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
