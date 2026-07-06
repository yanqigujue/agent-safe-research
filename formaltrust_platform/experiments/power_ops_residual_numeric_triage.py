from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Mapping


def build_residual_numeric_triage(audit_path: str | Path) -> dict[str, Any]:
    audit = _load_json(audit_path)
    needs_evidence = [
        mention
        for mention in _list_value(audit.get("numeric_mentions"))
        if isinstance(mention, Mapping) and mention.get("status") == "needs_evidence"
    ]
    triaged = [_triage_mention(mention) for mention in needs_evidence]
    counts = Counter(str(item["category"]) for item in triaged)

    return {
        "artifact_type": "power_ops_residual_numeric_triage",
        "source_audit": str(audit_path),
        "total_needs_evidence_mentions": len(needs_evidence),
        "category_counts": dict(sorted(counts.items())),
        "triaged_mentions": triaged,
        "recommended_next_actions": _recommended_next_actions(counts),
    }


def render_residual_numeric_triage_markdown(triage: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Residual Numeric Triage",
        "",
        "| Item | Value |",
        "|---|---:|",
        f"| needs_evidence mentions | {int(triage.get('total_needs_evidence_mentions', 0))} |",
        "",
        "## Category Counts",
        "",
        "| Category | Count |",
        "|---|---:|",
    ]
    for category, count in _mapping_value(triage.get("category_counts")).items():
        lines.append(f"| {category} | {int(count)} |")

    lines.extend(
        [
            "",
            "## Mentions",
            "",
            "| Document | Number | Category | Reason | Action | Context |",
            "|---|---:|---|---|---|---|",
        ]
    )
    for item in _list_value(triage.get("triaged_mentions")):
        if not isinstance(item, Mapping):
            continue
        lines.append(
            "| `{document}` | {number} | {category} | {reason} | {action} | {context} |".format(
                document=item.get("document", ""),
                number=item.get("number", ""),
                category=item.get("category", ""),
                reason=item.get("reason", ""),
                action=item.get("recommended_action", ""),
                context=_escape_table_text(str(item.get("context", ""))),
            )
        )

    lines.extend(
        [
            "",
            "## Recommended Next Actions",
            "",
        ]
    )
    for action in _list_value(triage.get("recommended_next_actions")):
        lines.append(f"- {action}")
    lines.append("")
    return "\n".join(lines)


def write_residual_numeric_triage(
    triage: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_residual_numeric_triage_markdown(triage), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.write_text(json.dumps(triage, ensure_ascii=False, indent=2), encoding="utf-8")


def _triage_mention(mention: Mapping[str, Any]) -> dict[str, Any]:
    context = str(mention.get("context", ""))
    category, reason, action = _classify_context(context)
    return {
        "document": str(mention.get("document", "")),
        "number": str(mention.get("number", "")),
        "context": context,
        "category": category,
        "reason": reason,
        "recommended_action": action,
    }


def _classify_context(context: str) -> tuple[str, str, str]:
    lowered = context.lower()
    if "current result on the 10-case" in lowered:
        return (
            "rewrite_needed",
            "The Current Result table now mixes multiple suites, not only the 10-case curated suite.",
            "Rewrite this table lead-in to say that rows come from multiple result artifacts.",
        )
    if "baseline grid on the 10-case" in lowered:
        return (
            "parser_extension",
            "The baseline table lead-in is supported by baseline-grid metadata but not recognized by the numeric parser.",
            "Extend the audit parser to bind table lead-in counts to the table artifact.",
        )
    if "only current baseline" in lowered:
        return (
            "parser_extension",
            "This comparative sentence is supported by baseline-grid rows but needs sentence-level binding.",
            "Add sentence-level support from the baseline grid or rewrite as a table-bound note.",
        )
    if any(token in lowered for token in ("expanded 18-case", "suite_count=3", "baseline_count=4", "10-case power-ops suite")):
        return (
            "parser_extension",
            "The number appears in a supported artifact readback or claim phrase but lacks a parser rule.",
            "Add artifact-specific parser support or keep it adjacent to explicit evidence.",
        )
    if any(
        token in lowered
        for token in (
            "| round |",
            "continuous iteration queue",
            "completed:",
            "next:",
            "forbidden claim hits",
            "**date:**",
            "next experiments",
            "contribution",
            "**formaltrust artifact.**",
            "**power-ops evaluation slice.**",
            "multi-step trace fixture",
            "repair-frame action invariance",
            "conservative collapse",
            "large-sample power-ops suite",
            "no-rag",
            "三个点",
            "下一轮",
        )
    ):
        return (
            "context_only",
            "The number is a list index, date/status count, queue round, or structural note.",
            "Do not treat this as a paper result claim.",
        )
    return (
        "parser_extension",
        "The number may be evidence-backed, but the current audit does not have a matching rule.",
        "Inspect this mention before paper use and either add parser support or rewrite.",
    )


def _recommended_next_actions(counts: Counter[str]) -> list[str]:
    actions: list[str] = []
    if counts.get("rewrite_needed", 0):
        actions.append("Rewrite over-broad result-table lead-ins before using them in paper prose.")
    if counts.get("parser_extension", 0):
        actions.append("Add parser rules for table lead-ins, claim phrases, and result-readback snippets.")
    if counts.get("context_only", 0):
        actions.append("Exclude context-only numbers from paper result-claim audits.")
    return actions


def _load_json(path: str | Path) -> dict[str, Any]:
    target = Path(path)
    payload = json.loads(target.read_text(encoding="utf-8"))
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


def _escape_table_text(value: str) -> str:
    return value.replace("|", "\\|")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Classify unresolved numeric mentions from the power-ops numeric audit."
    )
    parser.add_argument(
        "--audit",
        default="docs/power_ops_action_invariance_numeric_claim_audit_2026-07-02.json",
    )
    parser.add_argument(
        "--out-md",
        default="docs/power_ops_action_invariance_residual_numeric_triage_2026-07-02.md",
    )
    parser.add_argument(
        "--out-json",
        default="docs/power_ops_action_invariance_residual_numeric_triage_2026-07-02.json",
    )
    args = parser.parse_args(argv)

    triage = build_residual_numeric_triage(args.audit)
    write_residual_numeric_triage(triage, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
