from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from formaltrust_platform.state import FormalTrustState, state_to_dict


def write_case_artifact(run_dir: Path, state: FormalTrustState) -> Path:
    case_dir = run_dir / "cases"
    case_dir.mkdir(parents=True, exist_ok=True)
    path = case_dir / f"{_safe_name(state.case.id)}.json"
    path.write_text(json.dumps(state_to_dict(state), ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def write_results(run_dir: Path, summary: dict[str, Any], states: list[FormalTrustState]) -> Path:
    path = run_dir / "results.json"
    payload = {"summary": summary, "cases": [state_to_dict(state) for state in states]}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def _safe_name(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in value)

