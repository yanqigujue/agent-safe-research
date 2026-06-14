from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from formaltrust_platform.artifacts import write_case_artifact, write_results
from formaltrust_platform.config import ExperimentConfig
from formaltrust_platform.datasets import load_cases
from formaltrust_platform.graph import build_graph
from formaltrust_platform.registry import NodeRegistry
from formaltrust_platform.report import write_markdown_report
from formaltrust_platform.state import FormalTrustState, state_to_dict


@dataclass(frozen=True)
class ExperimentResult:
    run_id: str
    run_dir: Path
    report_path: Path
    summary: dict[str, Any]


class ExperimentRunner:
    def __init__(self, registry: NodeRegistry | None = None) -> None:
        self.registry = registry or NodeRegistry.with_builtins()

    def run(self, config: ExperimentConfig) -> ExperimentResult:
        run_id = _new_run_id(config.experiment_name)
        run_dir = config.output_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)

        cases = load_cases(config.dataset_path)
        app = build_graph(config.graph, self.registry)
        states: list[FormalTrustState] = []

        for case in cases:
            initial_state = FormalTrustState(run_id=run_id, case=case)
            try:
                raw_result = app.invoke(state_to_dict(initial_state))
                state = FormalTrustState.model_validate(raw_result)
            except Exception as exc:  # noqa: BLE001 - top-level case failure must not stop batch
                state = initial_state.add_error(
                    "__graph__",
                    str(exc),
                    error_type=type(exc).__name__,
                    hint="Check graph configuration and node contracts.",
                )
            write_case_artifact(run_dir, state)
            states.append(state)

        summary = _summarize(run_id, states)
        write_results(run_dir, summary, states)
        report_path = write_markdown_report(run_dir, config, summary, states)
        return ExperimentResult(run_id=run_id, run_dir=run_dir, report_path=report_path, summary=summary)


def _summarize(run_id: str, states: list[FormalTrustState]) -> dict[str, Any]:
    failed = 0
    for state in states:
        if state.errors or (state.evaluation is not None and not state.evaluation.passed):
            failed += 1
    total = len(states)
    return {
        "run_id": run_id,
        "total_cases": total,
        "passed_cases": total - failed,
        "failed_cases": failed,
    }


def _new_run_id(experiment_name: str) -> str:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    slug = "".join(ch.lower() if ch.isalnum() else "-" for ch in experiment_name).strip("-")
    return f"{stamp}-{slug or 'formaltrust'}"

