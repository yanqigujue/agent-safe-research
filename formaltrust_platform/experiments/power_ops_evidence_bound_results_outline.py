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


def build_evidence_bound_results_outline(
    *,
    paper_outline_path: str | Path,
    claim_ledger_readiness_path: str | Path,
    table_binding_path: str | Path,
) -> dict[str, Any]:
    paper_outline = _load_json(paper_outline_path)
    claim_sync = _load_json(claim_ledger_readiness_path)
    table_binding = _load_json(table_binding_path)

    ready_claims = [
        _claim_summary(claim)
        for claim in _list_value(claim_sync.get("supported_claims"))
        if isinstance(claim, Mapping) and bool(claim.get("paper_ready", False))
    ]
    result_claims = [
        claim
        for claim in ready_claims
        if _is_results_claim(claim.get("claim", ""))
    ]
    section_claims = [
        row
        for row in _list_value(paper_outline.get("claims_evidence_matrix"))
        if isinstance(row, Mapping) and "Results and Analysis" in str(row.get("section", ""))
    ]
    if str(claim_sync.get("readiness_status", "")) != "PASS" or not result_claims or not section_claims:
        return {
            "artifact_type": "power_ops_evidence_bound_results_outline",
            "source_paper_outline": str(paper_outline_path),
            "source_claim_ledger_readiness": str(claim_ledger_readiness_path),
            "source_table_binding": str(table_binding_path),
            "paper_section": "§5 Results and Analysis",
            "results_outline_status": "blocked_no_ready_result_claims",
            "results_outline": [],
            "forbidden_claim_hits": [],
        }

    table_rows = [
        row
        for row in _list_value(table_binding.get("rows"))
        if isinstance(row, Mapping)
    ]
    unsupported_table_rows = int(table_binding.get("unsupported_row_count", 0) or 0)
    outline = [
        _item(
            slot="fieldwise_repair_result",
            paragraph_goal=(
                "Report curated fieldwise repair as field preservation for authorized fields and "
                "removal of unauthorized fields, using only the fieldwise-repair result JSON and "
                "bound table row."
            ),
            source_claims=_pick_claims(result_claims, ("curated power-ops",)),
            evidence_paths=_evidence_for(section_claims, ("curated power-ops",)),
            table_refs=_table_refs(table_rows, "Current Result", ("fieldwise-repair",)),
        ),
        _item(
            slot="expanded_metamorphic_skill_results",
            paragraph_goal=(
                "Summarize expanded, metamorphic, and skill-authority fixtures as bounded "
                "regression evidence for field-level preservation and repair."
            ),
            source_claims=_pick_claims(result_claims, ("expanded 18-case", "metamorphic", "skill fixture")),
            evidence_paths=_evidence_for(section_claims, ("expanded 18-case", "metamorphic", "skill fixture")),
            table_refs=_table_refs(
                table_rows,
                "Current Result",
                ("expanded-fieldwise", "metamorphic", "skill-authority"),
            ),
        ),
        _item(
            slot="baseline_grid",
            paragraph_goal=(
                "Use the baseline grid to distinguish strict-block conservative collapse, "
                "provenance-only false allow, and fieldwise repair's current bounded behavior."
            ),
            source_claims=_pick_claims(result_claims, ("baseline grid",)),
            evidence_paths=_evidence_for(section_claims, ("baseline grid",)),
            table_refs=_table_refs(table_rows, "Baseline Grid", ()),
        ),
        _item(
            slot="performance_profile",
            paragraph_goal=(
                "Report performance as safety-preserving normal behavior, not wall-clock latency "
                "or operator workload reduction."
            ),
            source_claims=_pick_claims(result_claims, ("performance profile",)),
            evidence_paths=_evidence_for(section_claims, ("performance profile",)),
            table_refs=_table_refs(table_rows, "Performance Profile", ()),
        ),
        _item(
            slot="trace_replay_and_import",
            paragraph_goal=(
                "Report trace/span/OTLP replay and trace-import boundary behavior as L3 fixture "
                "evidence, not production telemetry."
            ),
            source_claims=_pick_claims(result_claims, ("trace/span/otlp", "trace import fixture")),
            evidence_paths=_evidence_for(section_claims, ("trace/span/otlp", "trace import fixture")),
            table_refs=_table_refs(
                table_rows,
                "Current Result",
                ("trace-repair", "span-otlp-repair", "trace-import"),
            ),
        ),
        _item(
            slot="multi_step_source_chain",
            paragraph_goal=(
                "Report the multi-step trace fixtures as covering planner, skill, tool metadata, "
                "memory, prior-step output, and user approval source chains."
            ),
            source_claims=_pick_claims(result_claims, ("multi-step trace import",)),
            evidence_paths=_evidence_for(section_claims, ("multi-step trace import",)),
            table_refs=_table_refs(table_rows, "Current Result", ("multistep-trace-import",)),
        ),
        _item(
            slot="claim_boundary",
            paragraph_goal=(
                "Close the results section by stating that all result claims are limited to local "
                "curated, bridge, and trace fixtures."
            ),
            source_claims=[],
            evidence_paths=[],
            table_refs=[],
            limitation_reason=(
                "No production telemetry; no wall-clock latency claim; no real workload reduction; "
                "no official neighboring-system superiority claim."
            ),
        ),
    ]
    outline_text = "\n".join(
        " ".join(
            [
                str(item.get("paragraph_goal", "")),
                str(item.get("limitation_reason", "")),
            ]
        )
        for item in outline
    )
    forbidden_hits = _forbidden_claim_hits(outline_text)
    if unsupported_table_rows:
        forbidden_hits.append({"phrase": "unsupported_table_rows", "count": str(unsupported_table_rows)})

    return {
        "artifact_type": "power_ops_evidence_bound_results_outline",
        "source_paper_outline": str(paper_outline_path),
        "source_claim_ledger_readiness": str(claim_ledger_readiness_path),
        "source_table_binding": str(table_binding_path),
        "paper_section": "§5 Results and Analysis",
        "section_goal": _section_goal(paper_outline, "Results and Analysis"),
        "results_outline_status": "ready" if not forbidden_hits else "blocked_forbidden_claim",
        "paper_ready_result_claim_count": len(result_claims),
        "fully_supported_table_row_count": int(table_binding.get("fully_supported_row_count", 0) or 0),
        "unsupported_table_row_count": unsupported_table_rows,
        "results_outline": outline,
        "forbidden_claim_hits": forbidden_hits,
    }


def render_evidence_bound_results_outline_markdown(outline: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Evidence-Bound Results Outline",
        "",
        f"**Status:** {outline.get('results_outline_status', '')}",
        f"**Paper section:** {outline.get('paper_section', '')}",
        f"**Paper-ready result claims:** {int(outline.get('paper_ready_result_claim_count', 0) or 0)}",
        f"**Fully supported table rows:** {int(outline.get('fully_supported_table_row_count', 0) or 0)}",
        f"**Unsupported table rows:** {int(outline.get('unsupported_table_row_count', 0) or 0)}",
        f"**Forbidden claim hits:** {len(_list_value(outline.get('forbidden_claim_hits')))}",
        "",
        "## Results Outline",
        "",
        "| Slot | Paragraph goal | Evidence paths | Table refs | Source claims | Limitation reason |",
        "|---|---|---|---|---|---|",
    ]
    for item in _list_value(outline.get("results_outline")):
        if not isinstance(item, Mapping):
            continue
        lines.append(
            "| {slot} | {goal} | {evidence} | {tables} | {claims} | {limitation} |".format(
                slot=_escape_table_text(str(item.get("slot", ""))),
                goal=_escape_table_text(str(item.get("paragraph_goal", ""))),
                evidence=_escape_table_text("; ".join(str(path) for path in _list_value(item.get("evidence_paths")))),
                tables=_escape_table_text(_table_ref_labels(item.get("table_refs"))),
                claims=_escape_table_text(_source_claim_labels(item.get("source_claims"))),
                limitation=_escape_table_text(str(item.get("limitation_reason", ""))),
            )
        )
    lines.append("")
    return "\n".join(lines)


def write_evidence_bound_results_outline(
    outline: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_evidence_bound_results_outline_markdown(outline), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(outline, ensure_ascii=False, indent=2), encoding="utf-8")


def _item(
    *,
    slot: str,
    paragraph_goal: str,
    source_claims: list[dict[str, Any]],
    evidence_paths: list[str],
    table_refs: list[dict[str, Any]],
    limitation_reason: str = "",
) -> dict[str, Any]:
    return {
        "slot": slot,
        "paragraph_goal": paragraph_goal,
        "evidence_paths": _unique(evidence_paths),
        "table_refs": table_refs,
        "source_claims": source_claims,
        "limitation_reason": limitation_reason,
    }


def _is_results_claim(claim: Any) -> bool:
    lowered = str(claim).lower()
    return any(
        token in lowered
        for token in (
            "curated power-ops",
            "expanded 18-case",
            "metamorphic",
            "skill fixture",
            "performance profile",
            "baseline grid",
            "trace/span/otlp",
            "trace import fixture",
            "multi-step trace import",
        )
    )


def _pick_claims(claims: list[dict[str, Any]], keywords: tuple[str, ...]) -> list[dict[str, Any]]:
    picked: list[dict[str, Any]] = []
    for claim in claims:
        lowered = claim["claim"].lower()
        if any(keyword.lower() in lowered for keyword in keywords):
            picked.append(claim)
    return picked


def _evidence_for(section_claims: list[Mapping[str, Any]], keywords: tuple[str, ...]) -> list[str]:
    evidence: list[str] = []
    for row in section_claims:
        claim = str(row.get("claim", "")).lower()
        if any(keyword.lower() in claim for keyword in keywords):
            evidence.extend(_normalize_path(path) for path in _list_value(row.get("evidence")))
    return _unique(evidence)


def _table_refs(table_rows: list[Mapping[str, Any]], table: str, labels: tuple[str, ...]) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    label_set = {label.lower() for label in labels}
    for row in table_rows:
        if str(row.get("table", "")) != table:
            continue
        label = str(row.get("row_label", ""))
        if label_set and label.lower() not in label_set:
            continue
        refs.append(
            {
                "table": str(row.get("table", "")),
                "row_label": label,
                "status": str(row.get("status", "")),
                "source_artifact": _normalize_path(str(row.get("source_artifact", ""))),
                "supported_metrics": [
                    str(metric)
                    for metric in _list_value(row.get("supported_metrics"))
                    if str(metric)
                ],
            }
        )
    return refs


def _section_goal(paper_outline: Mapping[str, Any], section_keyword: str) -> str:
    for item in _list_value(paper_outline.get("section_plan")):
        if not isinstance(item, Mapping):
            continue
        if section_keyword.lower() in str(item.get("section", "")).lower():
            return str(item.get("goal", ""))
    return ""


def _claim_summary(claim: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "claim": str(claim.get("claim", "")),
        "level": str(claim.get("level", "")),
        "paper_ready": bool(claim.get("paper_ready", False)),
        "evidence": [
            _normalize_path(str(item))
            for item in _list_value(claim.get("evidence"))
            if str(item)
        ],
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


def _normalize_path(path: str) -> str:
    return path.replace("\\", "/")


def _unique(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def _escape_table_text(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", "<br>")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate an evidence-bound results outline from paper-ready power-ops artifacts."
    )
    parser.add_argument(
        "--paper-outline",
        default="docs/power_ops_action_invariance_paper_outline_2026-07-02.json",
    )
    parser.add_argument(
        "--claim-ledger-readiness",
        default="docs/power_ops_action_invariance_claim_ledger_readiness_2026-07-02.json",
    )
    parser.add_argument(
        "--table-binding",
        default="docs/power_ops_action_invariance_table_evidence_binding_2026-07-02.json",
    )
    parser.add_argument(
        "--out-md",
        default="docs/power_ops_action_invariance_evidence_bound_results_outline_2026-07-02.md",
    )
    parser.add_argument(
        "--out-json",
        default="docs/power_ops_action_invariance_evidence_bound_results_outline_2026-07-02.json",
    )
    args = parser.parse_args(argv)

    outline = build_evidence_bound_results_outline(
        paper_outline_path=args.paper_outline,
        claim_ledger_readiness_path=args.claim_ledger_readiness,
        table_binding_path=args.table_binding,
    )
    write_evidence_bound_results_outline(outline, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
