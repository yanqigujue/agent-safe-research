from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any, Mapping


def build_paper_figure_table_package(
    *,
    authority_confusion_grid_path: str | Path,
    statistical_robustness_path: str | Path,
    figure_dir: str | Path = "figures",
) -> dict[str, Any]:
    grid_path = Path(authority_confusion_grid_path)
    stat_path = Path(statistical_robustness_path)
    output_dir = Path(figure_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    grid = _load_json(grid_path)
    stat = _load_json(stat_path)

    baseline_svg = output_dir / "power_ops_authority_confusion_baseline_grid.svg"
    interval_svg = output_dir / "power_ops_statistical_interval_ladder.svg"
    tables_tex = output_dir / "power_ops_paper_tables.tex"

    _write_baseline_grid_svg(grid, baseline_svg)
    _write_interval_ladder_svg(stat, interval_svg)
    _write_tables_tex(grid, stat, tables_tex)

    figures = [
        {
            "figure_id": "fig:authority-confusion-baselines",
            "file": str(baseline_svg),
            "kind": "svg_bar_chart",
            "caption": "Baseline behavior on trace-derived authority-confusion rows.",
            "source_paths": [_stable_path(grid_path)],
        },
        {
            "figure_id": "fig:statistical-intervals",
            "file": str(interval_svg),
            "kind": "svg_interval_plot",
            "caption": "Wilson intervals for current fixture-level rates.",
            "source_paths": [_stable_path(stat_path)],
        },
    ]
    tables = [
        {
            "table_id": "tab:authority-confusion-baselines",
            "file": str(tables_tex),
            "caption": "Authority-confusion baseline grid.",
            "source_paths": [_stable_path(grid_path)],
        },
        {
            "table_id": "tab:statistical-robustness",
            "file": str(tables_tex),
            "caption": "Wilson 95% intervals for current fixture-level rates.",
            "source_paths": [_stable_path(stat_path)],
        },
    ]
    return {
        "artifact_type": "power_ops_paper_figure_table_package",
        "figure_dir": str(output_dir),
        "figure_count": len(figures),
        "table_count": len(tables),
        "figures": figures,
        "tables": tables,
        "latex_tables_path": str(tables_tex),
        "claim_boundary": "Figures and tables are evidence-bound to source JSON artifacts; they do not add new empirical claims.",
    }


def render_paper_figure_table_package_markdown(package: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Paper Figure/Table Package",
        "",
        "This evidence-bound package lists generated figures and tables with source JSON bindings.",
        "",
        "## Figures",
        "",
        "| ID | File | Source |",
        "|---|---|---|",
    ]
    for figure in _list_value(package.get("figures")):
        if not isinstance(figure, Mapping):
            continue
        lines.append(
            "| `{id}` | `{file}` | {source} |".format(
                id=figure.get("figure_id", ""),
                file=figure.get("file", ""),
                source=_join_paths(figure.get("source_paths")),
            )
        )
    lines.extend(
        [
            "",
            "## Tables",
            "",
            "| ID | File | Source |",
            "|---|---|---|",
        ]
    )
    for table in _list_value(package.get("tables")):
        if not isinstance(table, Mapping):
            continue
        lines.append(
            "| `{id}` | `{file}` | {source} |".format(
                id=table.get("table_id", ""),
                file=table.get("file", ""),
                source=_join_paths(table.get("source_paths")),
            )
        )
    lines.extend(["", str(package.get("claim_boundary", "")), ""])
    return "\n".join(lines)


def write_paper_figure_table_package(
    package: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_paper_figure_table_package_markdown(package), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(package, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_baseline_grid_svg(grid: Mapping[str, Any], target: Path) -> None:
    baselines = _mapping_value(grid.get("baselines"))
    names = list(baselines)
    metrics = [
        ("confusion block", "laundering_block_rate", "#2b7a78"),
        ("false allow", "false_allow_rate", "#d1495b"),
        ("false block", "false_block_rate", "#777777"),
    ]
    width, height = 900, 380
    left, top, plot_w, plot_h = 72, 38, 760, 230
    group_w = plot_w / max(len(names), 1)
    bar_w = 14
    parts = [_svg_header(width, height)]
    parts.append(f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" stroke="#222"/>')
    parts.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" stroke="#222"/>')
    for tick in range(0, 6):
        value = tick / 5
        y = top + plot_h - value * plot_h
        parts.append(f'<line x1="{left - 4}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}" stroke="#e6e6e6"/>')
        parts.append(f'<text x="{left - 10}" y="{y + 4:.1f}" text-anchor="end" font-size="11">{value:.1f}</text>')
    for i, name in enumerate(names):
        cx = left + i * group_w + group_w / 2
        for j, (_, key, color) in enumerate(metrics):
            value = float(_mapping_value(baselines[name]).get(key, 0.0) or 0.0)
            x = cx + (j - 1) * (bar_w + 3) - bar_w / 2
            bar_h = value * plot_h
            y = top + plot_h - bar_h
            parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w}" height="{bar_h:.1f}" fill="{color}"/>')
        parts.append(
            '<text x="{x:.1f}" y="{y}" transform="rotate(35 {x:.1f} {y})" font-size="11">{label}</text>'.format(
                x=cx - 42,
                y=top + plot_h + 44,
                label=html.escape(name),
            )
        )
    for j, (label, _, color) in enumerate(metrics):
        x = left + 40 + j * 160
        parts.append(f'<rect x="{x}" y="18" width="12" height="12" fill="{color}"/>')
        parts.append(f'<text x="{x + 18}" y="29" font-size="12">{html.escape(label)}</text>')
    parts.append(f'<text x="{left - 48}" y="{top + 102}" transform="rotate(-90 {left - 48} {top + 102})" font-size="12">rate</text>')
    parts.append("</svg>")
    target.write_text("\n".join(parts), encoding="utf-8")


def _write_interval_ladder_svg(summary: Mapping[str, Any], target: Path) -> None:
    intervals = _mapping_value(summary.get("intervals"))
    names = list(intervals)
    width = 900
    row_h = 46
    height = 80 + row_h * len(names)
    left, top, plot_w = 330, 38, 480
    parts = [_svg_header(width, height)]
    for tick in range(0, 6):
        value = tick / 5
        x = left + value * plot_w
        parts.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{height - 52}" stroke="#e6e6e6"/>')
        parts.append(f'<text x="{x:.1f}" y="{height - 28}" text-anchor="middle" font-size="11">{value:.1f}</text>')
    for i, name in enumerate(names):
        record = _mapping_value(intervals[name])
        ci = _mapping_value(record.get("ci95"))
        lower = float(ci.get("lower", 0.0) or 0.0)
        upper = float(ci.get("upper", 0.0) or 0.0)
        point = float(record.get("point_estimate", 0.0) or 0.0)
        y = top + 22 + i * row_h
        x1 = left + lower * plot_w
        x2 = left + upper * plot_w
        xp = left + point * plot_w
        parts.append(f'<text x="18" y="{y + 4:.1f}" font-size="12">{html.escape(name)}</text>')
        parts.append(f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}" stroke="#2b7a78" stroke-width="3"/>')
        parts.append(f'<circle cx="{xp:.1f}" cy="{y:.1f}" r="5" fill="#d1495b"/>')
    parts.append(f'<text x="{left + plot_w / 2:.1f}" y="{height - 8}" text-anchor="middle" font-size="12">Wilson 95% interval</text>')
    parts.append("</svg>")
    target.write_text("\n".join(parts), encoding="utf-8")


def _write_tables_tex(grid: Mapping[str, Any], stat: Mapping[str, Any], target: Path) -> None:
    lines = [
        "% Auto-generated from evidence JSON artifacts.",
        "\\begin{table}[t]",
        "\\centering",
        "\\caption{Authority-confusion baseline grid.}",
        "\\label{tab:authority-confusion-baselines}",
        "\\begin{tabular}{lrrrr}",
        "\\toprule",
        "Baseline & Legal preserve & Confusion block & False allow & False block \\\\",
        "\\midrule",
    ]
    for name, metrics in _mapping_value(grid.get("baselines")).items():
        row = _mapping_value(metrics)
        lines.append(
            "{name} & {legal:.3f} & {block:.3f} & {false_allow:.3f} & {false_block:.3f} \\\\".format(
                name=_latex_escape(name),
                legal=float(row.get("legal_preservation_rate", 0.0) or 0.0),
                block=float(row.get("laundering_block_rate", 0.0) or 0.0),
                false_allow=float(row.get("false_allow_rate", 0.0) or 0.0),
                false_block=float(row.get("false_block_rate", 0.0) or 0.0),
            )
        )
    lines.extend(
        [
            "\\bottomrule",
            "\\end{tabular}",
            "\\end{table}",
            "",
            "\\begin{table}[t]",
            "\\centering",
            "\\caption{Wilson 95\\% intervals for current fixture-level rates.}",
            "\\label{tab:statistical-robustness}",
            "\\begin{tabular}{lrrrr}",
            "\\toprule",
            "Metric & Successes & n & Lower & Upper \\\\",
            "\\midrule",
        ]
    )
    for name, record in _mapping_value(stat.get("intervals")).items():
        ci = _mapping_value(_mapping_value(record).get("ci95"))
        lines.append(
            "{name} & {successes} & {n} & {lower:.4f} & {upper:.4f} \\\\".format(
                name=_latex_escape(name),
                successes=int(ci.get("successes", 0) or 0),
                n=int(ci.get("n", 0) or 0),
                lower=float(ci.get("lower", 0.0) or 0.0),
                upper=float(ci.get("upper", 0.0) or 0.0),
            )
        )
    lines.extend(["\\bottomrule", "\\end{tabular}", "\\end{table}", ""])
    target.write_text("\n".join(lines), encoding="utf-8")


def _svg_header(width: int, height: int) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="Times New Roman, DejaVu Serif, serif">'
        '<rect width="100%" height="100%" fill="white"/>'
    )


def _latex_escape(value: str) -> str:
    return str(value).replace("_", "\\_").replace("%", "\\%")


def _join_paths(value: Any) -> str:
    paths = [str(item) for item in _list_value(value)]
    return ", ".join(f"`{path}`" for path in paths) if paths else "none"


def _stable_path(path: Path) -> str:
    return path.as_posix()


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


def _list_value(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return list(value)
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, set):
        return list(value)
    return [value]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate evidence-bound paper figures and tables.")
    parser.add_argument(
        "--authority-confusion-grid",
        default="docs/power_ops_authority_confusion_baseline_grid_2026-07-02.json",
    )
    parser.add_argument(
        "--statistical-robustness",
        default="docs/power_ops_statistical_robustness_2026-07-02.json",
    )
    parser.add_argument("--figure-dir", default="figures")
    parser.add_argument("--out-md")
    parser.add_argument("--out-json")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args(argv)

    package = build_paper_figure_table_package(
        authority_confusion_grid_path=args.authority_confusion_grid,
        statistical_robustness_path=args.statistical_robustness,
        figure_dir=args.figure_dir,
    )
    if args.out_md or args.out_json:
        write_paper_figure_table_package(
            package,
            markdown_path=args.out_md
            or "docs/power_ops_paper_figure_table_package_2026-07-02.md",
            json_path=args.out_json,
        )
        return 0

    if args.format == "json":
        print(json.dumps(package, ensure_ascii=False, indent=2))
    else:
        print(render_paper_figure_table_package_markdown(package))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
