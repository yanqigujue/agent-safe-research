from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping

from formaltrust_platform.experiments.afw_bench import evaluate_paired_rows, load_paired_rows


BASELINES = (
    "capguard",
    "permission_only",
    "boundary_scope_only",
    "field_attribution_only",
    "strict_block",
)


def build_authority_confusion_baseline_grid(
    *,
    rows_path: str | Path,
    baseline_names: tuple[str, ...] = BASELINES,
) -> dict[str, Any]:
    path = Path(rows_path)
    rows = load_paired_rows(path)
    baselines = {
        baseline: _compact_baseline_result(evaluate_paired_rows(rows, baseline=baseline))
        for baseline in baseline_names
    }
    capguard = baselines.get("capguard", {})
    boundary_scope = baselines.get("boundary_scope_only", {})

    return {
        "artifact_type": "power_ops_authority_confusion_baseline_grid",
        "rows_path": str(path),
        "row_count": len(rows),
        "baseline_count": len(baselines),
        "baselines": baselines,
        "boundary_blind_baselines": [
            name
            for name, metrics in baselines.items()
            if float(metrics.get("legal_preservation_rate", 0.0) or 0.0) == 1.0
            and float(metrics.get("false_allow_rate", 0.0) or 0.0) == 1.0
        ],
        "overconservative_baselines": [
            name
            for name, metrics in baselines.items()
            if float(metrics.get("false_block_rate", 0.0) or 0.0) == 1.0
        ],
        "capguard_role_confusion_advantage": _round_float(
            float(capguard.get("laundering_block_rate", 0.0) or 0.0)
            - float(boundary_scope.get("laundering_block_rate", 0.0) or 0.0)
        ),
        "role_aware_best_baseline": "capguard"
        if float(capguard.get("laundering_block_rate", 0.0) or 0.0) == 1.0
        and float(capguard.get("legal_preservation_rate", 0.0) or 0.0) == 1.0
        else "",
        "claim_boundary": "This grid evaluates trace-derived authority-confusion rows only; it is not a production benchmark.",
    }


def render_authority_confusion_baseline_grid_markdown(grid: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Authority-Confusion Baseline Grid",
        "",
        "This grid compares role-aware checking with boundary-only, attribution-only, permissive, and strict-block variants.",
        "",
        "## Aggregate",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| row_count | {int(grid.get('row_count', 0) or 0)} |",
        f"| baseline_count | {int(grid.get('baseline_count', 0) or 0)} |",
        f"| capguard_role_confusion_advantage | {float(grid.get('capguard_role_confusion_advantage', 0.0) or 0.0):.3f} |",
        "",
        "## Baselines",
        "",
        "| Baseline | Legal preservation | Confusion block | False allow | False block |",
        "|---|---:|---:|---:|---:|",
    ]
    for name, metrics in _mapping_value(grid.get("baselines")).items():
        lines.append(
            "| `{name}` | {legal:.3f} | {block:.3f} | {false_allow:.3f} | {false_block:.3f} |".format(
                name=name,
                legal=float(metrics.get("legal_preservation_rate", 0.0) or 0.0),
                block=float(metrics.get("laundering_block_rate", 0.0) or 0.0),
                false_allow=float(metrics.get("false_allow_rate", 0.0) or 0.0),
                false_block=float(metrics.get("false_block_rate", 0.0) or 0.0),
            )
        )

    lines.extend(
        [
            "",
            "## Diagnosis",
            "",
            f"- Boundary-blind baselines: {_join_inline(grid.get('boundary_blind_baselines'))}.",
            f"- Overconservative baselines: {_join_inline(grid.get('overconservative_baselines'))}.",
            f"- Role-aware best baseline: `{grid.get('role_aware_best_baseline', '')}`.",
            "",
        ]
    )
    return "\n".join(lines)


def write_authority_confusion_baseline_grid(
    grid: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_authority_confusion_baseline_grid_markdown(grid), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(grid, ensure_ascii=False, indent=2), encoding="utf-8")


def _compact_baseline_result(result: Mapping[str, Any]) -> dict[str, Any]:
    keys = (
        "baseline",
        "total_rows",
        "legal_preservation_rate",
        "laundering_block_rate",
        "laundering_reject_rate",
        "false_allow_rate",
        "false_block_rate",
        "abstain_rate",
        "same_source_contrast_gap",
        "legal_witness_compression_rate",
    )
    compact = {key: result.get(key) for key in keys}
    compact["field_family_results"] = result.get("field_family_results", {})
    return compact


def _mapping_value(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    return {}


def _join_inline(value: Any) -> str:
    if not isinstance(value, list) or not value:
        return "none"
    return ", ".join(f"`{item}`" for item in value)


def _round_float(value: float) -> float:
    return round(value, 6)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate baselines on trace-derived power-ops authority-confusion rows."
    )
    parser.add_argument(
        "--rows",
        default="examples/data/power_ops_trace_authority_confusion_rows.json",
    )
    parser.add_argument("--out-md")
    parser.add_argument("--out-json")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args(argv)

    grid = build_authority_confusion_baseline_grid(rows_path=args.rows)
    if args.out_md or args.out_json:
        write_authority_confusion_baseline_grid(
            grid,
            markdown_path=args.out_md
            or "docs/power_ops_authority_confusion_baseline_grid_2026-07-02.md",
            json_path=args.out_json,
        )
        return 0

    if args.format == "json":
        print(json.dumps(grid, ensure_ascii=False, indent=2))
    else:
        print(render_authority_confusion_baseline_grid_markdown(grid))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
