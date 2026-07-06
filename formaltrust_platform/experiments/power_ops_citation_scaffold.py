from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Mapping, Sequence


DEFAULT_LIT_REVIEW = "docs/power_ops_action_invariance_lit_review_2026-07-02.md"
DEFAULT_BIB_PATH = "paper/power_ops_action_invariance/references_scaffold.bib"
DEFAULT_OUT_MD = "docs/power_ops_action_invariance_citation_scaffold_2026-07-02.md"
DEFAULT_OUT_JSON = "docs/power_ops_action_invariance_citation_scaffold_2026-07-02.json"

KEY_HINTS = (
    ("AgentSpec", "agentspec"),
    ("AgentVisor", "agentvisor"),
    ("AgentSentry", "agentsentry"),
    ("CaMeL", "camel"),
    ("ToolPrivBench", "toolprivbench"),
    ("RACG", "racg"),
    ("AgentDojo", "agentdojo"),
    ("InjecGuard", "injecguard"),
    ("Design Patterns for Securing LLM Agents", "secure_agent_design_patterns"),
    ("Towards Verifiably Safe Tool Use", "verifiably_safe_tool_use"),
    ("AI Agents with Formal Security Guarantees", "formal_security_agents"),
)


def build_citation_scaffold(*, lit_review_path: str | Path = DEFAULT_LIT_REVIEW) -> dict[str, Any]:
    lit_text = Path(lit_review_path).read_text(encoding="utf-8")
    entries = _extract_entries(lit_text)
    if not entries:
        return {
            "artifact_type": "power_ops_citation_scaffold",
            "lit_review_path": str(lit_review_path),
            "scaffold_status": "blocked_no_lit_entries",
            "blockers": ["No closest-work literature entries could be parsed"],
            "entry_count": 0,
            "metadata_pending_count": 0,
            "verified_source_count": 0,
            "caution_source_count": 0,
            "invented_reference_count": 0,
            "entries": [],
            "bibtex_text": "",
        }

    bibtex_text = _render_bibtex(entries)
    return {
        "artifact_type": "power_ops_citation_scaffold",
        "lit_review_path": str(lit_review_path),
        "scaffold_status": "ready",
        "blockers": [],
        "entry_count": len(entries),
        "metadata_pending_count": len(entries),
        "verified_source_count": sum(1 for entry in entries if str(entry.get("status", "")).startswith("verified")),
        "caution_source_count": sum(1 for entry in entries if str(entry.get("status", "")) == "caution"),
        "invented_reference_count": 0,
        "entries": entries,
        "bibtex_text": bibtex_text,
    }


def render_citation_scaffold_markdown(scaffold: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Citation Scaffold",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Status | {scaffold.get('scaffold_status', '')} |",
        f"| Entries | {int(scaffold.get('entry_count', 0) or 0)} |",
        f"| Metadata pending | {int(scaffold.get('metadata_pending_count', 0) or 0)} |",
        f"| Invented references | {int(scaffold.get('invented_reference_count', 0) or 0)} |",
        "",
        "## Entries",
        "",
        "| Key | Status | Title | URL |",
        "|---|---|---|---|",
    ]
    for entry in _list_value(scaffold.get("entries")):
        if not isinstance(entry, Mapping):
            continue
        lines.append(
            "| {key} | {status} | {title} | {url} |".format(
                key=_escape_table_text(str(entry.get("key", ""))),
                status=_escape_table_text(str(entry.get("status", ""))),
                title=_escape_table_text(str(entry.get("title", ""))),
                url=_escape_table_text(str(entry.get("url", ""))),
            )
        )
    lines.append("")
    return "\n".join(lines)


def write_citation_scaffold(
    scaffold: Mapping[str, Any],
    *,
    bib_path: str | Path = DEFAULT_BIB_PATH,
    markdown_path: str | Path = DEFAULT_OUT_MD,
    json_path: str | Path | None = DEFAULT_OUT_JSON,
) -> None:
    bib_target = Path(bib_path)
    bib_target.parent.mkdir(parents=True, exist_ok=True)
    bib_target.write_text(str(scaffold.get("bibtex_text", "")), encoding="utf-8")

    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_citation_scaffold_markdown(scaffold), encoding="utf-8")

    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(scaffold, ensure_ascii=False, indent=2), encoding="utf-8")


def _extract_entries(lit_text: str) -> list[dict[str, str]]:
    entries = []
    seen_keys = set()
    for line in lit_text.splitlines():
        match = re.match(r"^\|\s*\[(?P<title>[^\]]+)\]\((?P<url>[^)]+)\)(?P<meta>[^|]*)\|\s*(?P<status>[^|]+)\|", line)
        if not match:
            continue
        title = match.group("title").strip()
        url = match.group("url").strip()
        status = match.group("status").strip()
        key = _citation_key(title)
        if key in seen_keys:
            continue
        seen_keys.add(key)
        entries.append(
            {
                "key": key,
                "title": title,
                "url": url,
                "status": status,
                "metadata_status": "pending_citation_audit",
                "bibtex_status": "scaffold_only",
                "source": "closest_work_table",
            }
        )
    return entries


def _citation_key(title: str) -> str:
    for needle, key in KEY_HINTS:
        if needle.lower() in title.lower():
            return key
    slug = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")
    return slug[:48] or "unnamed_reference"


def _render_bibtex(entries: Sequence[Mapping[str, str]]) -> str:
    blocks = []
    for entry in entries:
        blocks.append(
            "\n".join(
                [
                    f"@misc{{{entry['key']},",
                    f"  title = {{{{{_bibtex_escape(entry['title'])}}}}},",
                    f"  howpublished = {{\\url{{{_bibtex_escape(entry['url'])}}}}},",
                    "  note = {Citation scaffold only; metadata pending citation audit; "
                    f"local verification status: {_bibtex_escape(entry['status'])}}}",
                    "}",
                ]
            )
        )
    return "\n\n".join(blocks) + "\n"


def _bibtex_escape(value: str) -> str:
    return value.replace("\\", "\\textbackslash{}").replace("{", "\\{").replace("}", "\\}")


def _escape_table_text(value: str) -> str:
    return value.replace("|", "\\|")


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
        description="Create a BibTeX scaffold from the power-ops literature review without inventing metadata."
    )
    parser.add_argument("--lit-review", default=DEFAULT_LIT_REVIEW)
    parser.add_argument("--bib-path", default=DEFAULT_BIB_PATH)
    parser.add_argument("--out-md", default=DEFAULT_OUT_MD)
    parser.add_argument("--out-json", default=DEFAULT_OUT_JSON)
    args = parser.parse_args(argv)

    scaffold = build_citation_scaffold(lit_review_path=args.lit_review)
    write_citation_scaffold(
        scaffold,
        bib_path=args.bib_path,
        markdown_path=args.out_md,
        json_path=args.out_json,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
