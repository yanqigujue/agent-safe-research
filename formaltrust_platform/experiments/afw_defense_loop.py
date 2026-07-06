from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence

from formaltrust_platform.experiments.afw_bench import evaluate_paired_rows, load_paired_rows


DEFAULT_ROWS_PATH = Path("examples/afw_power_ops_rag_rows.json")
DEFAULT_MARKDOWN_PATH = Path("docs/power_ops_afw_defense_loop_report_2026-07-01.md")
DEFAULT_JSON_PATH = Path("docs/power_ops_afw_defense_loop_report_2026-07-01.json")


def build_afw_defense_loop_report(
    *,
    rows_path: str | Path = DEFAULT_ROWS_PATH,
    baseline_names: Sequence[str] = ("permission_only", "boundary_scope_only"),
) -> dict[str, Any]:
    """Build a measure-locate-defend-retest report for the AFW power-ops slice."""

    rows = load_paired_rows(rows_path)
    capguard = evaluate_paired_rows(rows, baseline="capguard")
    comparisons = [
        _baseline_comparison(
            evaluate_paired_rows(rows, baseline=baseline),
            capguard,
        )
        for baseline in baseline_names
    ]
    k2_min_risk_discovery_lift = min(
        (item["risk_discovery_lift"] for item in comparisons),
        default=0.0,
    )
    k3_min_safety_issue_reduction = min(
        (item["safety_issue_reduction"] for item in comparisons),
        default=0.0,
    )
    general_ability_drop = 1.0 - capguard["legal_preservation_rate"]

    return {
        "artifact_type": "afw_defense_loop_report",
        "inputs": {
            "rows_path": str(Path(rows_path)),
            "baseline_names": list(baseline_names),
        },
        "summary": {
            "rows": len(rows),
            "defense": "capguard",
            "k2_min_risk_discovery_lift": round(k2_min_risk_discovery_lift, 6),
            "k3_min_safety_issue_reduction": round(k3_min_safety_issue_reduction, 6),
            "k4_utility_preservation": round(capguard["legal_preservation_rate"], 6),
            "general_ability_drop": round(general_ability_drop, 6),
            "passes_proxy_gates": (
                k2_min_risk_discovery_lift >= 0.10
                and k3_min_safety_issue_reduction >= 0.20
                and general_ability_drop <= 0.10
            ),
            "claim_scope": "afw_power_ops_subset_proxy_not_project_level",
        },
        "loop_steps": [
            {
                "step": "measure",
                "evidence": "Run weak baselines on the same power-ops paired rows.",
            },
            {
                "step": "locate",
                "evidence": "Collect laundered rows false-allowed by each baseline.",
            },
            {
                "step": "defend",
                "evidence": "Apply CapGuard field-authority coverage checks.",
            },
            {
                "step": "retest",
                "evidence": "Rerun the same rows and compare false allows and legal preservation.",
            },
        ],
        "capguard_summary": _summary_digest(capguard),
        "baseline_comparisons": comparisons,
    }


def render_afw_defense_loop_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# AFW Defense Loop Report",
        "",
        "Loop: measure -> locate -> defend -> retest",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---:|",
    ]
    for key, value in report["summary"].items():
        lines.append(f"| {key} | {value} |")

    lines.extend(
        [
            "",
            "## Baseline Comparisons",
            "",
            "| Baseline | Before false allows | After false allows | Risk discovery lift | Safety issue reduction |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for item in report["baseline_comparisons"]:
        lines.append(
            "| {baseline} | {before} | {after} | {risk:.3f} | {safety:.3f} |".format(
                baseline=item["baseline"],
                before=item["before_false_allow_count"],
                after=item["after_false_allow_count"],
                risk=item["risk_discovery_lift"],
                safety=item["safety_issue_reduction"],
            )
        )

    lines.extend(
        [
            "",
            "## Located False Allows",
            "",
            "| Baseline | Rows |",
            "|---|---|",
        ]
    )
    for item in report["baseline_comparisons"]:
        rows = ", ".join(f"`{row_id}`" for row_id in item["located_false_allow_rows"]) or "none"
        lines.append(f"| {item['baseline']} | {rows} |")

    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            "These metrics are AFW power-ops subset proxies. They should not be reported "
            "as full project-level K2/K3/K4 until evaluated on the broader project dataset.",
            "",
        ]
    )
    return "\n".join(lines)


def write_afw_defense_loop_report(
    *,
    rows_path: str | Path = DEFAULT_ROWS_PATH,
    baseline_names: Sequence[str] = ("permission_only", "boundary_scope_only"),
    markdown_path: str | Path = DEFAULT_MARKDOWN_PATH,
    json_path: str | Path = DEFAULT_JSON_PATH,
) -> dict[str, Any]:
    report = build_afw_defense_loop_report(
        rows_path=rows_path,
        baseline_names=baseline_names,
    )
    Path(markdown_path).write_text(render_afw_defense_loop_markdown(report), encoding="utf-8")
    Path(json_path).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def _baseline_comparison(baseline: dict[str, Any], capguard: dict[str, Any]) -> dict[str, Any]:
    before_false_allow_rows = _false_allow_rows(baseline)
    after_false_allow_rows = _false_allow_rows(capguard)
    before_count = len(before_false_allow_rows)
    after_count = len(after_false_allow_rows)
    return {
        "baseline": baseline["baseline"],
        "before": _summary_digest(baseline),
        "after": _summary_digest(capguard),
        "before_false_allow_count": before_count,
        "after_false_allow_count": after_count,
        "risk_discovery_lift": round(
            capguard["laundering_block_rate"] - baseline["laundering_block_rate"],
            6,
        ),
        "safety_issue_reduction": _ratio(before_count - after_count, before_count, default=1.0),
        "utility_preservation_after": round(capguard["legal_preservation_rate"], 6),
        "located_false_allow_rows": before_false_allow_rows,
    }


def _summary_digest(summary: dict[str, Any]) -> dict[str, Any]:
    total_rows = summary["total_rows"]
    false_allow_count = len(_false_allow_rows(summary))
    false_block_count = round(summary["false_block_rate"] * total_rows)
    return {
        "baseline": summary["baseline"],
        "total_rows": total_rows,
        "legal_preservation_rate": round(summary["legal_preservation_rate"], 6),
        "laundering_block_rate": round(summary["laundering_block_rate"], 6),
        "false_allow_rate": round(summary["false_allow_rate"], 6),
        "false_block_rate": round(summary["false_block_rate"], 6),
        "false_allow_count": false_allow_count,
        "false_block_count": false_block_count,
    }


def _false_allow_rows(summary: dict[str, Any]) -> list[str]:
    return [
        result["row_id"]
        for result in summary["row_results"]
        if result["laundered_decision"] == "allow"
    ]


def _ratio(numerator: float, denominator: float, *, default: float = 0.0) -> float:
    if denominator == 0:
        return default
    return round(numerator / denominator, 6)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write AFW defense-loop reports.")
    parser.add_argument("--rows", default=str(DEFAULT_ROWS_PATH))
    parser.add_argument(
        "--baseline",
        action="append",
        dest="baselines",
        default=None,
        help="Baseline name to include. May be supplied multiple times.",
    )
    parser.add_argument("--markdown", default=str(DEFAULT_MARKDOWN_PATH))
    parser.add_argument("--json", default=str(DEFAULT_JSON_PATH))
    args = parser.parse_args(argv)

    report = write_afw_defense_loop_report(
        rows_path=args.rows,
        baseline_names=args.baselines or ["permission_only", "boundary_scope_only"],
        markdown_path=args.markdown,
        json_path=args.json,
    )
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
