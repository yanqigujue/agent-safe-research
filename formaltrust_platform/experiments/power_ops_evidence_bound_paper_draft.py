from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping


TITLE = "Field-Level Action Invariance for Power-Operation LLM Agents"

FORBIDDEN_CLAIM_PHRASES = (
    "first llm-agent guardrail",
    "first runtime enforcement framework",
    "first least-privilege llm-agent security framework",
    "solves prompt injection",
    "proves production safety",
    "outperforms official neighboring systems",
    "reduces real human workload",
)


def build_evidence_bound_paper_draft(
    *,
    abstract_path: str | Path,
    intro_prose_path: str | Path,
    related_work_prose_path: str | Path,
    method_prose_path: str | Path,
    evaluation_setup_path: str | Path,
    results_prose_path: str | Path,
    limitations_prose_path: str | Path,
    conclusion_path: str | Path,
) -> dict[str, Any]:
    section_specs = [
        (
            "abstract",
            "Abstract",
            abstract_path,
            "abstract_status",
            "abstract_text",
            "power_ops_evidence_bound_abstract",
        ),
        (
            "introduction",
            "1 Introduction",
            intro_prose_path,
            "intro_prose_status",
            "intro_text",
            "power_ops_evidence_bound_intro_prose",
        ),
        (
            "related_work",
            "2 Related Work and Novelty Boundary",
            related_work_prose_path,
            "related_work_prose_status",
            "related_work_text",
            "power_ops_evidence_bound_related_work_prose",
        ),
        (
            "method",
            "3 Formal Model and CapGuard",
            method_prose_path,
            "method_prose_status",
            "method_text",
            "power_ops_evidence_bound_method_prose",
        ),
        (
            "evaluation_setup",
            "4 Evaluation Setup",
            evaluation_setup_path,
            "evaluation_setup_status",
            "evaluation_setup_text",
            "power_ops_evidence_bound_evaluation_setup",
        ),
        (
            "results",
            "5 Results and Analysis",
            results_prose_path,
            "results_prose_status",
            "results_text",
            "power_ops_evidence_bound_results_prose",
        ),
        (
            "limitations",
            "6 Limitations and Next Experiments",
            limitations_prose_path,
            "limitations_prose_status",
            "limitations_text",
            "power_ops_evidence_bound_limitations_prose",
        ),
        (
            "conclusion",
            "7 Conclusion",
            conclusion_path,
            "conclusion_status",
            "conclusion_text",
            "power_ops_evidence_bound_conclusion",
        ),
    ]

    loaded_sections = [
        _section_from_spec(
            slot=slot,
            heading=heading,
            path=path,
            status_key=status_key,
            text_key=text_key,
            expected_artifact_type=expected_artifact_type,
        )
        for slot, heading, path, status_key, text_key, expected_artifact_type in section_specs
    ]
    not_ready = [
        {
            "slot": section["slot"],
            "source_path": section["source_path"],
            "source_status": section["source_status"],
            "artifact_type": section["artifact_type"],
        }
        for section in loaded_sections
        if section["source_status"] != "ready" or not section["text"]
    ]
    if not_ready:
        return {
            "artifact_type": "power_ops_evidence_bound_paper_draft",
            "title": TITLE,
            "paper_draft_status": "blocked_section_not_ready",
            "blocked_sections": not_ready,
            "sections": [],
            "paper_text": "",
            "forbidden_claim_hits": [],
        }

    paper_text = "\n\n".join(section["text"] for section in loaded_sections)
    forbidden_hits = _forbidden_claim_hits(paper_text)
    return {
        "artifact_type": "power_ops_evidence_bound_paper_draft",
        "title": TITLE,
        "paper_draft_status": "ready" if not forbidden_hits else "blocked_forbidden_claim",
        "section_count": len(loaded_sections),
        "sections": loaded_sections,
        "paper_text": paper_text,
        "forbidden_claim_hits": forbidden_hits,
    }


def render_evidence_bound_paper_draft_markdown(draft: Mapping[str, Any]) -> str:
    lines = [
        f"# {draft.get('title', TITLE)}",
        "",
        f"**Status:** {draft.get('paper_draft_status', '')}",
        f"**Section count:** {int(draft.get('section_count', 0) or 0)}",
        f"**Forbidden claim hits:** {len(_list_value(draft.get('forbidden_claim_hits')))}",
        "",
    ]
    for section in _list_value(draft.get("sections")):
        if not isinstance(section, Mapping):
            continue
        lines.extend(
            [
                f"## {section.get('heading', '')}",
                "",
                str(section.get("text", "")),
                "",
                "<!-- source: {path}; status: {status}; artifact: {artifact} -->".format(
                    path=section.get("source_path", ""),
                    status=section.get("source_status", ""),
                    artifact=section.get("artifact_type", ""),
                ),
                "",
            ]
        )
    return "\n".join(lines)


def write_evidence_bound_paper_draft(
    draft: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_evidence_bound_paper_draft_markdown(draft), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(draft, ensure_ascii=False, indent=2), encoding="utf-8")


def _section_from_spec(
    *,
    slot: str,
    heading: str,
    path: str | Path,
    status_key: str,
    text_key: str,
    expected_artifact_type: str,
) -> dict[str, Any]:
    payload = _load_json(path)
    artifact_type = str(payload.get("artifact_type", ""))
    status = str(payload.get(status_key, ""))
    text = str(payload.get(text_key, ""))
    if artifact_type != expected_artifact_type:
        status = f"blocked_unexpected_artifact_type:{artifact_type}"
    return {
        "slot": slot,
        "heading": heading,
        "source_path": str(path),
        "artifact_type": artifact_type,
        "source_status": status,
        "text": text,
        "forbidden_claim_hit_count": len(_list_value(payload.get("forbidden_claim_hits"))),
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Assemble bounded power-ops section prose into one evidence-bound paper draft."
    )
    parser.add_argument(
        "--abstract",
        default="docs/power_ops_action_invariance_evidence_bound_abstract_2026-07-02.json",
    )
    parser.add_argument(
        "--intro-prose",
        default="docs/power_ops_action_invariance_evidence_bound_intro_prose_2026-07-02.json",
    )
    parser.add_argument(
        "--related-work-prose",
        default="docs/power_ops_action_invariance_evidence_bound_related_work_prose_2026-07-02.json",
    )
    parser.add_argument(
        "--method-prose",
        default="docs/power_ops_action_invariance_evidence_bound_method_prose_2026-07-02.json",
    )
    parser.add_argument(
        "--evaluation-setup",
        default="docs/power_ops_action_invariance_evidence_bound_evaluation_setup_2026-07-02.json",
    )
    parser.add_argument(
        "--results-prose",
        default="docs/power_ops_action_invariance_evidence_bound_results_prose_2026-07-02.json",
    )
    parser.add_argument(
        "--limitations-prose",
        default="docs/power_ops_action_invariance_evidence_bound_limitations_prose_2026-07-02.json",
    )
    parser.add_argument(
        "--conclusion",
        default="docs/power_ops_action_invariance_evidence_bound_conclusion_2026-07-02.json",
    )
    parser.add_argument(
        "--out-md",
        default="docs/power_ops_action_invariance_evidence_bound_paper_draft_2026-07-02.md",
    )
    parser.add_argument(
        "--out-json",
        default="docs/power_ops_action_invariance_evidence_bound_paper_draft_2026-07-02.json",
    )
    args = parser.parse_args(argv)

    draft = build_evidence_bound_paper_draft(
        abstract_path=args.abstract,
        intro_prose_path=args.intro_prose,
        related_work_prose_path=args.related_work_prose,
        method_prose_path=args.method_prose,
        evaluation_setup_path=args.evaluation_setup,
        results_prose_path=args.results_prose,
        limitations_prose_path=args.limitations_prose,
        conclusion_path=args.conclusion,
    )
    write_evidence_bound_paper_draft(draft, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
