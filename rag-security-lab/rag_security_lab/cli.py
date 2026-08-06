from __future__ import annotations

import argparse
import json
from pathlib import Path

from .components import attacks, datasets, generators, retrievers  # noqa: F401
from .config import load_config
from .registry import ATTACKS, DATASETS, GENERATORS, RETRIEVERS
from .runner import run_experiment


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="rag-security-lab")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run or validate an experiment configuration")
    run_parser.add_argument("--config", required=True, help="YAML or JSON experiment config")
    run_parser.add_argument("--project-root", default=".", help="Root used to resolve relative paths")
    run_parser.add_argument("--output-root", default="", help="Optional output directory override")
    run_parser.add_argument("--dry-run", action="store_true", help="Load and validate without writing artifacts")

    subparsers.add_parser("components", help="List registered component types")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "components":
        print(
            json.dumps(
                {
                    "datasets": DATASETS.names(),
                    "attacks": ATTACKS.names(),
                    "retrievers": RETRIEVERS.names(),
                    "generators": GENERATORS.names(),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    config = load_config(args.config)
    output_override = Path(args.output_root).resolve() if args.output_root else None
    result = run_experiment(
        config,
        Path(args.project_root),
        dry_run=args.dry_run,
        output_root_override=output_override,
    )
    if isinstance(result, Path):
        print(f"Experiment completed: {result}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

