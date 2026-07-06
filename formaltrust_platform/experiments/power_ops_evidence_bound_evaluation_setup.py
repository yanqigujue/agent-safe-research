from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping


DEFAULT_EXPANDED_DATASET_AUDIT = "docs/power_ops_action_invariance_expanded_dataset_audit_2026-07-02.json"
DEFAULT_BASELINE_GRID = "docs/power_ops_action_invariance_baseline_grid_2026-07-02.json"
DEFAULT_TRACE_IMPORT_RESULTS = "docs/power_ops_trace_import_results_2026-07-02.json"
DEFAULT_MULTISTEP_TRACE_IMPORT_RESULTS = "docs/power_ops_multistep_trace_import_results_2026-07-02.json"
DEFAULT_PLANNER_SKILL_TOOL_MEMORY_RESULTS = "docs/power_ops_planner_skill_tool_memory_results_2026-07-02.json"
DEFAULT_TABLE_BINDING = "docs/power_ops_action_invariance_table_evidence_binding_2026-07-02.json"
DEFAULT_DRAFT_CONSISTENCY_AUDIT = "docs/power_ops_action_invariance_paper_draft_consistency_audit_2026-07-02.json"
DEFAULT_OUT_MD = "docs/power_ops_action_invariance_evidence_bound_evaluation_setup_2026-07-02.md"
DEFAULT_OUT_JSON = "docs/power_ops_action_invariance_evidence_bound_evaluation_setup_2026-07-02.json"

FORBIDDEN_CLAIM_PHRASES = (
    "first llm-agent guardrail",
    "first runtime enforcement framework",
    "first least-privilege llm-agent security framework",
    "solves prompt injection",
    "proves production safety",
    "outperforms official neighboring systems",
    "reduces real human workload",
)


def build_evidence_bound_evaluation_setup(
    *,
    expanded_dataset_audit_path: str | Path = DEFAULT_EXPANDED_DATASET_AUDIT,
    baseline_grid_path: str | Path = DEFAULT_BASELINE_GRID,
    trace_import_results_path: str | Path = DEFAULT_TRACE_IMPORT_RESULTS,
    multistep_trace_import_results_path: str | Path = DEFAULT_MULTISTEP_TRACE_IMPORT_RESULTS,
    planner_skill_tool_memory_results_path: str | Path = DEFAULT_PLANNER_SKILL_TOOL_MEMORY_RESULTS,
    table_binding_path: str | Path = DEFAULT_TABLE_BINDING,
    draft_consistency_audit_path: str | Path = DEFAULT_DRAFT_CONSISTENCY_AUDIT,
) -> dict[str, Any]:
    expanded = _load_json(expanded_dataset_audit_path)
    baseline = _load_json(baseline_grid_path)
    trace = _load_json(trace_import_results_path)
    multistep = _load_json(multistep_trace_import_results_path)
    planner_chain = _load_json(planner_skill_tool_memory_results_path)
    table = _load_json(table_binding_path)
    draft_audit = _load_json(draft_consistency_audit_path)

    blockers = _readiness_blockers(
        expanded,
        baseline,
        trace,
        multistep,
        planner_chain,
        table,
        draft_audit,
    )
    if blockers:
        return {
            "artifact_type": "power_ops_evidence_bound_evaluation_setup",
            "evaluation_setup_status": "blocked_incomplete_evidence",
            "blockers": blockers,
            "paragraphs": [],
            "evaluation_setup_text": "",
            "forbidden_claim_hits": [],
        }

    expanded_case_count = int(expanded.get("total_cases", 0) or 0)
    baseline_case_count = int(baseline.get("total_cases", 0) or 0)
    baseline_count = len(_mapping_value(baseline.get("baselines")))
    trace_case_count = int(trace.get("total_cases", 0) or 0)
    multistep_case_count = int(multistep.get("total_cases", 0) or 0)
    planner_chain_case_count = int(planner_chain.get("total_cases", 0) or 0)
    fully_supported_rows = int(table.get("fully_supported_row_count", 0) or 0)
    source_types = ", ".join(sorted(_mapping_value(expanded.get("source_type_counts")).keys()))
    source_types = source_types or "not recorded"

    paths = {
        "expanded": str(expanded_dataset_audit_path),
        "baseline": str(baseline_grid_path),
        "trace": str(trace_import_results_path),
        "multistep": str(multistep_trace_import_results_path),
        "planner_chain": str(planner_skill_tool_memory_results_path),
        "table": str(table_binding_path),
        "draft_audit": str(draft_consistency_audit_path),
    }
    paragraphs = [
        {
            "slot": "benchmark_scope",
            "text": (
                "We evaluate field-level action invariance with a bounded power-operation setup: "
                f"a {baseline_case_count}-case curated baseline grid, an {expanded_case_count}-case expanded suite, "
                "and trace replay fixtures that are treated as audit inputs rather than production telemetry."
            ),
            "source_paths": [paths["baseline"], paths["expanded"], paths["trace"]],
        },
        {
            "slot": "dataset_and_cases",
            "text": (
                f"The expanded dataset audit reports {expanded_case_count} cases with oracle coverage "
                f"{float(expanded.get('oracle_coverage_rate', 0.0) or 0.0):.3f} across source types "
                f"{source_types}; this is the current dataset boundary for section 4."
            ),
            "source_paths": [paths["expanded"]],
        },
        {
            "slot": "baselines",
            "text": (
                f"The {baseline_case_count}-case curated baseline grid compares {baseline_count} modes: "
                "strict-block, fieldwise-decision-only, provenance-only, and fieldwise-repair."
            ),
            "source_paths": [paths["baseline"]],
        },
        {
            "slot": "trace_imports",
            "text": (
                f"The trace-import path contributes {trace_case_count} trace-import boundary cases and "
                f"{multistep_case_count} multi-step source-chain case, plus "
                f"{planner_chain_case_count} planner-skill-tool-memory cases; these fixtures check malformed, "
                "missing-source, duplicate-approval, expired-epoch, and multi-source import behavior."
            ),
            "source_paths": [paths["trace"], paths["multistep"], paths["planner_chain"]],
        },
        {
            "slot": "metrics_and_audits",
            "text": (
                f"Table evidence binding currently marks {fully_supported_rows} table rows as fully supported, "
                f"while the assembled draft audit reports source-link completeness "
                f"{float(draft_audit.get('source_link_completeness_rate', 0.0) or 0.0):.3f} and text match rate "
                f"{float(draft_audit.get('text_match_rate', 0.0) or 0.0):.3f}."
            ),
            "source_paths": [paths["table"], paths["draft_audit"]],
        },
        {
            "slot": "claim_boundary",
            "text": (
                "This setup supports fixture-level evaluation claims only: it does not claim production telemetry, "
                "wall-clock latency, operator workload reduction, or official benchmark superiority."
            ),
            "source_paths": [paths["expanded"], paths["table"], paths["draft_audit"]],
        },
    ]
    setup_text = "\n\n".join(paragraph["text"] for paragraph in paragraphs)
    forbidden_hits = _forbidden_claim_hits(setup_text)
    return {
        "artifact_type": "power_ops_evidence_bound_evaluation_setup",
        "evaluation_setup_status": "ready" if not forbidden_hits else "blocked_forbidden_claim",
        "blockers": [f"{len(forbidden_hits)} forbidden claim hits"] if forbidden_hits else [],
        "expanded_case_count": expanded_case_count,
        "baseline_case_count": baseline_case_count,
        "baseline_count": baseline_count,
        "trace_import_case_count": trace_case_count,
        "multistep_trace_case_count": multistep_case_count,
        "planner_chain_case_count": planner_chain_case_count,
        "fully_supported_table_rows": fully_supported_rows,
        "paragraph_count": len(paragraphs),
        "paragraphs": paragraphs,
        "evaluation_setup_text": setup_text,
        "forbidden_claim_hits": forbidden_hits,
    }


def render_evidence_bound_evaluation_setup_markdown(setup: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Evidence-Bound Evaluation Setup",
        "",
        f"**Status:** {setup.get('evaluation_setup_status', '')}",
        "",
        "## 4 Evaluation Setup",
        "",
    ]
    for paragraph in _list_value(setup.get("paragraphs")):
        if not isinstance(paragraph, Mapping):
            continue
        lines.extend(
            [
                str(paragraph.get("text", "")),
                "",
                "<!-- slot: {slot}; sources: {sources} -->".format(
                    slot=paragraph.get("slot", ""),
                    sources=", ".join(str(path) for path in _list_value(paragraph.get("source_paths"))),
                ),
                "",
            ]
        )
    return "\n".join(lines)


def write_evidence_bound_evaluation_setup(
    setup: Mapping[str, Any],
    *,
    markdown_path: str | Path = DEFAULT_OUT_MD,
    json_path: str | Path | None = DEFAULT_OUT_JSON,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_evidence_bound_evaluation_setup_markdown(setup), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(setup, ensure_ascii=False, indent=2), encoding="utf-8")


def _readiness_blockers(
    expanded: Mapping[str, Any],
    baseline: Mapping[str, Any],
    trace: Mapping[str, Any],
    multistep: Mapping[str, Any],
    planner_chain: Mapping[str, Any],
    table: Mapping[str, Any],
    draft_audit: Mapping[str, Any],
) -> list[str]:
    blockers: list[str] = []
    if float(expanded.get("oracle_coverage_rate", 0.0) or 0.0) < 1.0:
        blockers.append("expanded dataset oracle coverage is incomplete")
    if int(baseline.get("total_cases", 0) or 0) <= 0 or not _mapping_value(baseline.get("baselines")):
        blockers.append("baseline grid is incomplete")
    if int(trace.get("failed_cases", 0) or 0) != 0:
        blockers.append("trace import has failed cases")
    if int(multistep.get("failed_cases", 0) or 0) != 0:
        blockers.append("multi-step trace import has failed cases")
    if int(planner_chain.get("failed_cases", 0) or 0) != 0:
        blockers.append("planner-skill-tool-memory benchmark has failed cases")
    if float(_mapping_value(planner_chain.get("source_chain_coverage")).get("coverage_rate", 0.0) or 0.0) < 1.0:
        blockers.append("planner-skill-tool-memory source-chain coverage is incomplete")
    if int(table.get("unsupported_row_count", 0) or 0) != 0:
        blockers.append("table evidence binding has unsupported rows")
    if draft_audit.get("audit_status") != "PASS":
        blockers.append("paper draft consistency audit does not pass")
    return blockers


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
    parser = argparse.ArgumentParser(description="Build bounded section 4 evaluation setup prose.")
    parser.add_argument("--expanded-dataset-audit", default=DEFAULT_EXPANDED_DATASET_AUDIT)
    parser.add_argument("--baseline-grid", default=DEFAULT_BASELINE_GRID)
    parser.add_argument("--trace-import-results", default=DEFAULT_TRACE_IMPORT_RESULTS)
    parser.add_argument("--multistep-trace-import-results", default=DEFAULT_MULTISTEP_TRACE_IMPORT_RESULTS)
    parser.add_argument("--planner-skill-tool-memory-results", default=DEFAULT_PLANNER_SKILL_TOOL_MEMORY_RESULTS)
    parser.add_argument("--table-binding", default=DEFAULT_TABLE_BINDING)
    parser.add_argument("--draft-consistency-audit", default=DEFAULT_DRAFT_CONSISTENCY_AUDIT)
    parser.add_argument("--out-md", default=DEFAULT_OUT_MD)
    parser.add_argument("--out-json", default=DEFAULT_OUT_JSON)
    args = parser.parse_args(argv)

    setup = build_evidence_bound_evaluation_setup(
        expanded_dataset_audit_path=args.expanded_dataset_audit,
        baseline_grid_path=args.baseline_grid,
        trace_import_results_path=args.trace_import_results,
        multistep_trace_import_results_path=args.multistep_trace_import_results,
        planner_skill_tool_memory_results_path=args.planner_skill_tool_memory_results,
        table_binding_path=args.table_binding,
        draft_consistency_audit_path=args.draft_consistency_audit,
    )
    write_evidence_bound_evaluation_setup(setup, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
