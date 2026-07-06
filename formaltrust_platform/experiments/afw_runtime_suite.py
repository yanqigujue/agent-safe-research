from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from formaltrust_platform.config import load_config
from formaltrust_platform.experiments.afw_runtime_report import (
    build_afw_runtime_suite_summary,
    render_afw_runtime_suite_markdown,
)
from formaltrust_platform.runner import ExperimentRunner


@dataclass(frozen=True)
class AFWRuntimeConfigSuiteResult:
    run_dirs: list[Path]
    summary: dict
    markdown_path: Path
    json_path: Path


def run_afw_runtime_config_suite(
    config_paths: Sequence[str | Path],
    *,
    output_dir: str | Path = Path("runs"),
    report_dir: str | Path = Path("docs"),
    suite_id: str = "afw_runtime_config_suite",
    output_stem: str = "afw_runtime_config_suite_report",
) -> AFWRuntimeConfigSuiteResult:
    """Run AFW runtime YAML configs and write a suite-level Markdown/JSON report."""

    if not config_paths:
        raise ValueError("At least one runtime config path is required.")

    output_root = Path(output_dir).resolve()
    report_root = Path(report_dir).resolve()
    report_root.mkdir(parents=True, exist_ok=True)

    runner = ExperimentRunner()
    run_dirs: list[Path] = []
    for config_path in config_paths:
        config = load_config(config_path).with_output_dir(output_root)
        result = runner.run(config)
        run_dirs.append(result.run_dir)

    summary = build_afw_runtime_suite_summary(run_dirs, suite_id=suite_id)
    markdown_path = report_root / f"{output_stem}.md"
    json_path = report_root / f"{output_stem}.json"
    markdown_path.write_text(render_afw_runtime_suite_markdown(summary), encoding="utf-8")
    json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    return AFWRuntimeConfigSuiteResult(
        run_dirs=run_dirs,
        summary=summary,
        markdown_path=markdown_path,
        json_path=json_path,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run AFW runtime validation configs and write a suite report."
    )
    parser.add_argument("configs", nargs="+", help="Runtime YAML config paths to execute.")
    parser.add_argument("--output-dir", default="runs", help="Directory for FormalTrust runs.")
    parser.add_argument("--report-dir", default="docs", help="Directory for suite report files.")
    parser.add_argument("--suite-id", default="afw_runtime_config_suite")
    parser.add_argument("--output-stem", default="afw_runtime_config_suite_report")
    args = parser.parse_args(argv)

    result = run_afw_runtime_config_suite(
        args.configs,
        output_dir=args.output_dir,
        report_dir=args.report_dir,
        suite_id=args.suite_id,
        output_stem=args.output_stem,
    )
    print(json.dumps(
        {
            "run_dirs": [str(path) for path in result.run_dirs],
            "markdown_path": str(result.markdown_path),
            "json_path": str(result.json_path),
            "total_runs": result.summary["total_runs"],
            "total_cases": result.summary["total_cases"],
            "passed_cases": result.summary["passed_cases"],
        },
        ensure_ascii=False,
        indent=2,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
