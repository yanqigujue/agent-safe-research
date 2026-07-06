from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Mapping


DEFAULT_DRAFT_PATH = "docs/power_ops_action_invariance_evidence_bound_paper_draft_2026-07-02.json"
DEFAULT_PARAGRAPH_MAP = "docs/power_ops_action_invariance_claim_to_paragraph_map_2026-07-02.json"
DEFAULT_EDIT_GATE = "docs/power_ops_action_invariance_paper_draft_edit_gate_2026-07-02.json"
DEFAULT_TEX_PATH = "paper/power_ops_action_invariance/main.tex"
DEFAULT_OUT_MD = "docs/power_ops_action_invariance_latex_manuscript_2026-07-02.md"
DEFAULT_OUT_JSON = "docs/power_ops_action_invariance_latex_manuscript_2026-07-02.json"

FORBIDDEN_CLAIM_PHRASES = (
    "first llm-agent guardrail",
    "first runtime enforcement framework",
    "first least-privilege llm-agent security framework",
    "solves prompt injection",
    "proves production safety",
    "outperforms official neighboring systems",
    "reduces real human workload",
)


def build_latex_manuscript(
    *,
    draft_path: str | Path = DEFAULT_DRAFT_PATH,
    paragraph_map_path: str | Path = DEFAULT_PARAGRAPH_MAP,
    edit_gate_path: str | Path = DEFAULT_EDIT_GATE,
) -> dict[str, Any]:
    draft = _load_json(draft_path)
    paragraph_map = _load_json(paragraph_map_path)
    edit_gate = _load_json(edit_gate_path)

    blockers = _readiness_blockers(draft, paragraph_map, edit_gate)
    if blockers:
        return {
            "artifact_type": "power_ops_latex_manuscript",
            "latex_status": "blocked_edit_gate_failed",
            "blockers": blockers,
            "draft_path": str(draft_path),
            "paragraph_map_path": str(paragraph_map_path),
            "edit_gate_path": str(edit_gate_path),
            "edit_gate_status": str(edit_gate.get("gate_status", "")),
            "section_count": 0,
            "paragraph_count": 0,
            "paragraph_comment_count": 0,
            "tex_text": "",
            "forbidden_claim_hits": [],
        }

    rows_by_ref = _paragraph_rows_by_ref(paragraph_map)
    tex_text, paragraph_count, paragraph_comment_count = _render_tex(draft, rows_by_ref)
    forbidden_hits = _forbidden_claim_hits(str(draft.get("paper_text", "")))
    return {
        "artifact_type": "power_ops_latex_manuscript",
        "latex_status": "ready" if not forbidden_hits else "blocked_forbidden_claim",
        "blockers": [f"{len(forbidden_hits)} forbidden claim hits"] if forbidden_hits else [],
        "draft_path": str(draft_path),
        "paragraph_map_path": str(paragraph_map_path),
        "edit_gate_path": str(edit_gate_path),
        "edit_gate_status": str(edit_gate.get("gate_status", "")),
        "section_count": len(_sections(draft)),
        "paragraph_count": paragraph_count,
        "paragraph_comment_count": paragraph_comment_count,
        "tex_path": DEFAULT_TEX_PATH,
        "tex_text": tex_text,
        "forbidden_claim_hits": forbidden_hits,
    }


def render_latex_manuscript_markdown(manuscript: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops LaTeX Manuscript",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Status | {manuscript.get('latex_status', '')} |",
        f"| Sections | {int(manuscript.get('section_count', 0) or 0)} |",
        f"| Paragraphs | {int(manuscript.get('paragraph_count', 0) or 0)} |",
        f"| Paragraph comments | {int(manuscript.get('paragraph_comment_count', 0) or 0)} |",
        f"| Forbidden claim hits | {len(_list_value(manuscript.get('forbidden_claim_hits')))} |",
        "",
        "## Blockers",
        "",
    ]
    blockers = _list_value(manuscript.get("blockers"))
    if blockers:
        lines.extend(f"- {blocker}" for blocker in blockers)
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Output",
            "",
            f"- tex: `{manuscript.get('tex_path', DEFAULT_TEX_PATH)}`",
            "",
        ]
    )
    return "\n".join(lines)


def write_latex_manuscript(
    manuscript: Mapping[str, Any],
    *,
    tex_path: str | Path = DEFAULT_TEX_PATH,
    markdown_path: str | Path = DEFAULT_OUT_MD,
    json_path: str | Path | None = DEFAULT_OUT_JSON,
) -> None:
    tex_target = Path(tex_path)
    tex_target.parent.mkdir(parents=True, exist_ok=True)
    tex_target.write_text(str(manuscript.get("tex_text", "")), encoding="utf-8")

    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_latex_manuscript_markdown(manuscript), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(manuscript, ensure_ascii=False, indent=2), encoding="utf-8")


def _render_tex(
    draft: Mapping[str, Any],
    rows_by_ref: Mapping[tuple[str, int], Mapping[str, Any]],
) -> tuple[str, int, int]:
    title = _latex_escape(str(draft.get("title", "Field-Level Action Invariance for Power-Operation LLM Agents")))
    lines = [
        r"\documentclass[11pt]{article}",
        r"\usepackage[T1]{fontenc}",
        r"\usepackage{lmodern}",
        r"\usepackage{hyperref}",
        r"\usepackage{booktabs}",
        r"\usepackage[margin=1in]{geometry}",
        "",
        f"\\title{{{title}}}",
        r"\author{Anonymous Authors}",
        r"\date{}",
        "",
        r"\begin{document}",
        r"\maketitle",
        "",
    ]
    paragraph_count = 0
    paragraph_comment_count = 0
    for section in _sections(draft):
        slot = str(section.get("slot", ""))
        heading = str(section.get("heading", ""))
        paragraphs = _split_paragraphs(str(section.get("text", "")))
        lines.append(_section_source_comment(section))
        if slot == "abstract":
            lines.append(r"\begin{abstract}")
        else:
            lines.append(f"\\section{{{_latex_escape(_section_title(heading))}}}")
        lines.append("")

        for index, paragraph in enumerate(paragraphs, start=1):
            paragraph_count += 1
            row = rows_by_ref.get((slot, index), {})
            if row:
                paragraph_comment_count += 1
                lines.append(_paragraph_map_comment(row))
            lines.append(_latex_escape(_clean_text(paragraph)))
            lines.append("")

        if slot == "abstract":
            lines.append(r"\end{abstract}")
            lines.append("")

    lines.append(r"\end{document}")
    lines.append("")
    return "\n".join(lines), paragraph_count, paragraph_comment_count


def _readiness_blockers(
    draft: Mapping[str, Any],
    paragraph_map: Mapping[str, Any],
    edit_gate: Mapping[str, Any],
) -> list[str]:
    blockers: list[str] = []
    if draft.get("paper_draft_status") != "ready":
        blockers.append(f"paper draft status is {draft.get('paper_draft_status')}")
    if paragraph_map.get("map_status") != "PASS":
        blockers.append(f"paragraph map status is {paragraph_map.get('map_status')}")
    if edit_gate.get("gate_status") != "PASS":
        blockers.append("edit gate is not PASS")
    if int(edit_gate.get("stale_artifact_count", 0) or 0):
        blockers.append("paragraph evidence artifacts are stale")
    return blockers


def _sections(draft: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    return [
        section
        for section in _list_value(draft.get("sections"))
        if isinstance(section, Mapping)
    ]


def _paragraph_rows_by_ref(paragraph_map: Mapping[str, Any]) -> dict[tuple[str, int], Mapping[str, Any]]:
    rows = {}
    for row in _list_value(paragraph_map.get("paragraph_rows")):
        if not isinstance(row, Mapping):
            continue
        rows[(str(row.get("slot", "")), int(row.get("paragraph_index", 0) or 0))] = row
    return rows


def _section_source_comment(section: Mapping[str, Any]) -> str:
    return "% source: slot={slot}; path={path}; artifact={artifact}".format(
        slot=section.get("slot", ""),
        path=section.get("source_path", ""),
        artifact=section.get("artifact_type", ""),
    )


def _paragraph_map_comment(row: Mapping[str, Any]) -> str:
    return "% paragraph-map: slot={slot}; paragraph={paragraph}; status={status}; claims={claims}; refs={refs}; boundaries={boundaries}".format(
        slot=row.get("slot", ""),
        paragraph=row.get("paragraph_index", ""),
        status=row.get("claim_binding_status", ""),
        claims=len(_list_value(row.get("source_claims"))),
        refs=len(_list_value(row.get("evidence_refs"))),
        boundaries=",".join(_string_values(row.get("boundary_flags"))),
    )


def _section_title(heading: str) -> str:
    return re.sub(r"^\d+\s+", "", heading).strip()


def _clean_text(text: str) -> str:
    return text.replace("\u00a7", "Section ").replace("搂", "Section ")


def _latex_escape(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in text)


def _forbidden_claim_hits(text: str) -> list[dict[str, str]]:
    lowered = text.lower()
    return [
        {"phrase": phrase}
        for phrase in FORBIDDEN_CLAIM_PHRASES
        if phrase in lowered
    ]


def _split_paragraphs(text: str) -> list[str]:
    return [part.strip() for part in text.split("\n\n") if part.strip()]


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
    return [item for item in _list_value(value) if isinstance(item, str) and item]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Export the bounded power-ops paper draft as a source-commented LaTeX manuscript."
    )
    parser.add_argument("--draft", default=DEFAULT_DRAFT_PATH)
    parser.add_argument("--paragraph-map", default=DEFAULT_PARAGRAPH_MAP)
    parser.add_argument("--edit-gate", default=DEFAULT_EDIT_GATE)
    parser.add_argument("--tex-path", default=DEFAULT_TEX_PATH)
    parser.add_argument("--out-md", default=DEFAULT_OUT_MD)
    parser.add_argument("--out-json", default=DEFAULT_OUT_JSON)
    args = parser.parse_args(argv)

    manuscript = build_latex_manuscript(
        draft_path=args.draft,
        paragraph_map_path=args.paragraph_map,
        edit_gate_path=args.edit_gate,
    )
    write_latex_manuscript(
        manuscript,
        tex_path=args.tex_path,
        markdown_path=args.out_md,
        json_path=args.out_json,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
