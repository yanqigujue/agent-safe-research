from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from formaltrust_platform.config import load_config
from formaltrust_platform.interfaces import NodeConfigError
from formaltrust_platform.runner import ExperimentRunner

app = typer.Typer(help="FormalTrust modular validation platform CLI.")


@app.callback()
def main() -> None:
    """Run modular LLM trustworthiness validation experiments."""


@app.command("run")
def run_command(
    config: Path = typer.Option(..., "--config", "-c", help="Path to experiment YAML config."),
    output_dir: Optional[Path] = typer.Option(None, "--output-dir", help="Override output run directory."),
) -> None:
    experiment_config = load_config(config)
    if output_dir is not None:
        experiment_config = experiment_config.with_output_dir(output_dir)

    try:
        result = ExperimentRunner().run(experiment_config)
    except NodeConfigError as exc:
        # A node's config violates its declared interface — surface it cleanly
        # instead of as a traceback.
        typer.echo(f"Config error: {exc}", err=True)
        raise typer.Exit(code=2) from exc

    typer.echo(f"Run directory: {result.run_dir}")
    typer.echo(f"Report: {result.report_path}")
