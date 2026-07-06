from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Mapping


DEFAULT_TEX = "paper/power_ops_action_invariance/main.tex"
DEFAULT_CHECKED_BIB = "paper/power_ops_action_invariance/references_checked.bib"
DEFAULT_SCAFFOLD_BIB = "paper/power_ops_action_invariance/references_scaffold.bib"
DEFAULT_OUT_MD = "docs/power_ops_action_invariance_latex_citation_gate_2026-07-02.md"
DEFAULT_OUT_JSON = "docs/power_ops_action_invariance_latex_citation_gate_2026-07-02.json"

CITE_RE = re.compile(r"\\cite\w*(?:\s*\[[^\]]*\]){0,2}\s*\{([^}]*)\}")
BIB_KEY_RE = re.compile(r"@\w+\s*\{\s*([^,\s]+)")


def build_latex_citation_gate(
    *,
    tex_path: str | Path = DEFAULT_TEX,
    checked_bib_path: str | Path = DEFAULT_CHECKED_BIB,
    scaffold_bib_path: str | Path | None = DEFAULT_SCAFFOLD_BIB,
) -> dict[str, Any]:
    tex = Path(tex_path).read_text(encoding="utf-8")
    checked_bib = Path(checked_bib_path).read_text(encoding="utf-8")
    checked_keys = _bib_keys(checked_bib)
    scaffold_keys = _bib_keys(Path(scaffold_bib_path).read_text(encoding="utf-8")) if scaffold_bib_path else set()
    citation_keys = _citation_keys(tex)
    unchecked = sorted(key for key in citation_keys if key not in checked_keys)
    pending_scaffold_only = sorted(key for key in unchecked if key in scaffold_keys)
    bibliography_uses_checked = "references_checked" in tex
    status = "PASS" if not unchecked and bibliography_uses_checked else "blocked_unchecked_citations"
    blockers = []
    if unchecked:
        blockers.append("unchecked citation keys are not present in references_checked.bib")
    if not bibliography_uses_checked:
        blockers.append("manuscript does not reference references_checked bibliography")

    return {
        "artifact_type": "power_ops_latex_citation_gate",
        "tex_path": str(tex_path),
        "checked_bib_path": str(checked_bib_path),
        "scaffold_bib_path": str(scaffold_bib_path) if scaffold_bib_path else "",
        "gate_status": status,
        "blockers": blockers,
        "citation_key_count": len(citation_keys),
        "checked_bib_key_count": len(checked_keys),
        "scaffold_bib_key_count": len(scaffold_keys),
        "citation_keys": sorted(citation_keys),
        "checked_bib_keys": sorted(checked_keys),
        "unchecked_citation_keys": unchecked,
        "pending_scaffold_only_keys": pending_scaffold_only,
        "bibliography_uses_checked": bibliography_uses_checked,
    }


def render_latex_citation_gate_markdown(gate: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops LaTeX Citation Gate",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Status | {gate.get('gate_status', '')} |",
        f"| Citation keys | {int(gate.get('citation_key_count', 0) or 0)} |",
        f"| Checked BibTeX keys | {int(gate.get('checked_bib_key_count', 0) or 0)} |",
        f"| Scaffold BibTeX keys | {int(gate.get('scaffold_bib_key_count', 0) or 0)} |",
        f"| Unchecked citations | {len(_list_value(gate.get('unchecked_citation_keys')))} |",
        f"| Pending scaffold-only citations | {len(_list_value(gate.get('pending_scaffold_only_keys')))} |",
        f"| Uses references_checked | {bool(gate.get('bibliography_uses_checked', False))} |",
        "",
    ]
    blockers = _list_value(gate.get("blockers"))
    if blockers:
        lines.extend(["## Blockers", ""])
        lines.extend(f"- {blocker}" for blocker in blockers)
        lines.append("")
    lines.extend(
        [
            "## Citation Keys",
            "",
            "| Key | Status |",
            "|---|---|",
        ]
    )
    checked = set(str(key) for key in _list_value(gate.get("checked_bib_keys")))
    pending_scaffold = set(str(key) for key in _list_value(gate.get("pending_scaffold_only_keys")))
    for key in _list_value(gate.get("citation_keys")):
        key_text = str(key)
        if key_text in checked:
            status = "checked"
        elif key_text in pending_scaffold:
            status = "pending_scaffold_only"
        else:
            status = "missing"
        lines.append(f"| {key_text} | {status} |")
    lines.append("")
    return "\n".join(lines)


def write_latex_citation_gate(
    gate: Mapping[str, Any],
    *,
    markdown_path: str | Path = DEFAULT_OUT_MD,
    json_path: str | Path | None = DEFAULT_OUT_JSON,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_latex_citation_gate_markdown(gate), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.write_text(json.dumps(gate, ensure_ascii=False, indent=2), encoding="utf-8")


def _citation_keys(tex: str) -> set[str]:
    keys: set[str] = set()
    for match in CITE_RE.finditer(tex):
        for key in match.group(1).split(","):
            stripped = key.strip()
            if stripped:
                keys.add(stripped)
    return keys


def _bib_keys(bibtex: str) -> set[str]:
    return {match.group(1).strip() for match in BIB_KEY_RE.finditer(bibtex)}


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
        description="Check that LaTeX citations use only keys from the checked bibliography."
    )
    parser.add_argument("--tex", default=DEFAULT_TEX)
    parser.add_argument("--checked-bib", default=DEFAULT_CHECKED_BIB)
    parser.add_argument("--scaffold-bib", default=DEFAULT_SCAFFOLD_BIB)
    parser.add_argument("--out-md", default=DEFAULT_OUT_MD)
    parser.add_argument("--out-json", default=DEFAULT_OUT_JSON)
    args = parser.parse_args(argv)

    gate = build_latex_citation_gate(
        tex_path=args.tex,
        checked_bib_path=args.checked_bib,
        scaffold_bib_path=args.scaffold_bib,
    )
    write_latex_citation_gate(gate, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
