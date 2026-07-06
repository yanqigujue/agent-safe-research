from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Mapping


CLAIM_BOUNDARY = (
    "Wilson intervals describe this finite fixture evidence; they are not production population guarantees."
)


def build_statistical_robustness_summary(
    *,
    normal_behavior_path: str | Path,
    authority_confusion_grid_path: str | Path,
) -> dict[str, Any]:
    normal = _load_json(Path(normal_behavior_path))
    grid = _load_json(Path(authority_confusion_grid_path))
    row_count = int(grid.get("row_count", 0) or 0)
    baselines = _mapping_value(grid.get("baselines"))

    intervals = {
        "normal_authorized_field_preservation": _interval_record(
            label="normal_authorized_field_preservation",
            successes=int(normal.get("preserved_authorized_field_count", 0) or 0),
            total=int(normal.get("authorized_field_count", 0) or 0),
            source_path=str(normal_behavior_path),
            interpretation="authorized normal fields preserved under strict supervision",
        ),
        "capguard_confusion_block": _baseline_interval(
            baselines,
            "capguard",
            "laundering_block_rate",
            row_count,
            source_path=str(authority_confusion_grid_path),
            interpretation="trace-derived role-confusion rows blocked by role-aware CapGuard",
        ),
        "capguard_false_allow": _baseline_interval(
            baselines,
            "capguard",
            "false_allow_rate",
            row_count,
            source_path=str(authority_confusion_grid_path),
            interpretation="trace-derived role-confusion rows falsely allowed by CapGuard",
        ),
        "boundary_scope_only_false_allow": _baseline_interval(
            baselines,
            "boundary_scope_only",
            "false_allow_rate",
            row_count,
            source_path=str(authority_confusion_grid_path),
            interpretation="trace-derived role-confusion rows falsely allowed by boundary-only checking",
        ),
        "strict_block_false_block": _baseline_interval(
            baselines,
            "strict_block",
            "false_block_rate",
            row_count,
            source_path=str(authority_confusion_grid_path),
            interpretation="legal rows falsely blocked by strict whole-action blocking",
        ),
    }

    return {
        "artifact_type": "power_ops_statistical_robustness_summary",
        "interval_method": "wilson",
        "confidence": 0.95,
        "interval_count": len(intervals),
        "normal_behavior_path": str(normal_behavior_path),
        "authority_confusion_grid_path": str(authority_confusion_grid_path),
        "claim_boundary": CLAIM_BOUNDARY,
        "intervals": intervals,
    }


def render_statistical_robustness_markdown(summary: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Statistical Robustness Summary",
        "",
        "This artifact reports Wilson 95% intervals for current fixture-level point estimates.",
        "",
        "## Boundary",
        "",
        str(summary.get("claim_boundary", "")),
        "",
        "## Intervals",
        "",
        "| Metric | Successes | n | Point | Lower | Upper |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name, record in _mapping_value(summary.get("intervals")).items():
        ci = _mapping_value(record.get("ci95"))
        lines.append(
            "| `{name}` | {successes} | {n} | {point:.3f} | {lower:.4f} | {upper:.4f} |".format(
                name=name,
                successes=int(ci.get("successes", 0) or 0),
                n=int(ci.get("n", 0) or 0),
                point=float(record.get("point_estimate", 0.0) or 0.0),
                lower=float(ci.get("lower", 0.0) or 0.0),
                upper=float(ci.get("upper", 0.0) or 0.0),
            )
        )
    lines.append("")
    return "\n".join(lines)


def write_statistical_robustness_summary(
    summary: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_statistical_robustness_markdown(summary), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")


def _baseline_interval(
    baselines: Mapping[str, Any],
    baseline_name: str,
    rate_key: str,
    row_count: int,
    *,
    source_path: str,
    interpretation: str,
) -> dict[str, Any]:
    metrics = _mapping_value(baselines.get(baseline_name))
    successes = int(round(float(metrics.get(rate_key, 0.0) or 0.0) * row_count))
    return _interval_record(
        label=f"{baseline_name}_{rate_key}",
        successes=successes,
        total=row_count,
        source_path=source_path,
        interpretation=interpretation,
    )


def _interval_record(
    *,
    label: str,
    successes: int,
    total: int,
    source_path: str,
    interpretation: str,
) -> dict[str, Any]:
    return {
        "label": label,
        "point_estimate": round(successes / total, 6) if total else 0.0,
        "ci95": _wilson_ci95(successes, total),
        "source_path": source_path,
        "interpretation": interpretation,
    }


def _wilson_ci95(successes: int, total: int) -> dict[str, Any]:
    if total <= 0:
        raise ValueError("Wilson confidence interval requires at least one observation")
    z = 1.959963984540054
    p_hat = successes / total
    z2 = z * z
    denominator = 1.0 + z2 / total
    center = p_hat + z2 / (2.0 * total)
    margin = z * math.sqrt((p_hat * (1.0 - p_hat) + z2 / (4.0 * total)) / total)
    return {
        "method": "wilson",
        "confidence": 0.95,
        "successes": int(successes),
        "n": int(total),
        "lower": round((center - margin) / denominator, 4),
        "upper": round((center + margin) / denominator, 4),
    }


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} did not contain a JSON object")
    return payload


def _mapping_value(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    return {}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build Wilson-interval robustness summary for current power-ops results."
    )
    parser.add_argument(
        "--normal-behavior",
        default="docs/power_ops_normal_behavior_stress_results_2026-07-02.json",
    )
    parser.add_argument(
        "--authority-confusion-grid",
        default="docs/power_ops_authority_confusion_baseline_grid_2026-07-02.json",
    )
    parser.add_argument("--out-md")
    parser.add_argument("--out-json")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args(argv)

    summary = build_statistical_robustness_summary(
        normal_behavior_path=args.normal_behavior,
        authority_confusion_grid_path=args.authority_confusion_grid,
    )
    if args.out_md or args.out_json:
        write_statistical_robustness_summary(
            summary,
            markdown_path=args.out_md
            or "docs/power_ops_statistical_robustness_2026-07-02.md",
            json_path=args.out_json,
        )
        return 0

    if args.format == "json":
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_statistical_robustness_markdown(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
