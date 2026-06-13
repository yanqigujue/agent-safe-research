from __future__ import annotations

from pathlib import Path

from formaltrust_platform.config import ExperimentConfig
from formaltrust_platform.state import FormalTrustState


def write_markdown_report(
    run_dir: Path,
    config: ExperimentConfig,
    summary: dict[str, int | str],
    states: list[FormalTrustState],
) -> Path:
    lines: list[str] = [
        f"# FormalTrust Run Report: {config.experiment_name}",
        "",
        "## Summary",
        f"- Run ID: `{summary['run_id']}`",
        f"- Total cases: {summary['total_cases']}",
        f"- Passed cases: {summary['passed_cases']}",
        f"- Failed cases: {summary['failed_cases']}",
        "",
        "## Cases",
    ]

    for state in states:
        response = state.model_response.content if state.model_response else "<no response>"
        eval_label = state.evaluation.label if state.evaluation else "<not evaluated>"
        lines.extend(
            [
                "",
                f"### {state.case.id}",
                f"- Tags: {', '.join(state.case.tags) if state.case.tags else '<none>'}",
                f"- Evaluation: `{eval_label}`",
                f"- Errors: {len(state.errors)}",
                "",
                "Prompt:",
                "```text",
                state.prompt or state.case.input,
                "```",
                "Response:",
                "```text",
                response,
                "```",
            ]
        )

        if state.errors:
            lines.append("Errors:")
            for error in state.errors:
                lines.append(f"- `{error.node}` {error.error_type}: {error.message}")
                if error.hint:
                    lines.append(f"  Hint: {error.hint}")

        lines.append("Trace:")
        for event in state.trace:
            lines.append(f"- `{event.node}` {event.status}: {event.message}")

    path = run_dir / "report.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path

