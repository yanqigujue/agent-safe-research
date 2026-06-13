from __future__ import annotations

import json
from pathlib import Path

from formaltrust_platform.state import TestCase


def load_jsonl_cases(path: str | Path) -> list[TestCase]:
    dataset_path = Path(path)
    cases: list[TestCase] = []
    with dataset_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                payload = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {dataset_path}:{line_number}: {exc}") from exc
            cases.append(TestCase.model_validate(payload))
    return cases

