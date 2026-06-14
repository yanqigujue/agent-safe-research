from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from formaltrust_platform.interfaces import DatasetLoader
from formaltrust_platform.state import TestCase

# Columns that map directly onto TestCase fields; every other CSV column is
# folded into TestCase.metadata.
_CSV_CORE_FIELDS = {"id", "input", "expected_behavior"}
_CSV_TAG_SEPARATOR = ";"


def load_jsonl_cases(path: str | Path) -> list[TestCase]:
    """Load one JSON object per line (the original built-in format)."""

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


def load_json_cases(path: str | Path) -> list[TestCase]:
    """Load a single JSON array of case objects."""

    dataset_path = Path(path)
    with dataset_path.open("r", encoding="utf-8") as handle:
        try:
            payload = json.load(handle)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON dataset {dataset_path}: {exc}") from exc
    if not isinstance(payload, list):
        raise ValueError(f"JSON dataset {dataset_path} must be a list of case objects.")
    return [TestCase.model_validate(item) for item in payload]


def load_csv_cases(path: str | Path) -> list[TestCase]:
    """Load CSV rows.

    ``id`` / ``input`` / ``expected_behavior`` columns map to the matching
    fields, ``tags`` is split on ``;``, and any remaining columns are collected
    into ``metadata``.
    """

    dataset_path = Path(path)
    cases: list[TestCase] = []
    with dataset_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row_number, row in enumerate(reader, start=2):  # row 1 is the header
            payload: dict[str, Any] = {}
            metadata: dict[str, Any] = {}
            for raw_key, value in row.items():
                if raw_key is None:
                    continue
                column = raw_key.strip()
                if column in _CSV_CORE_FIELDS:
                    if value not in (None, ""):
                        payload[column] = value
                elif column == "tags":
                    tags = [t.strip() for t in (value or "").split(_CSV_TAG_SEPARATOR) if t.strip()]
                    if tags:
                        payload["tags"] = tags
                elif value not in (None, ""):
                    metadata[column] = value
            if metadata:
                payload["metadata"] = metadata
            try:
                cases.append(TestCase.model_validate(payload))
            except Exception as exc:  # noqa: BLE001 - surface row context with the validation error
                raise ValueError(f"Invalid CSV row at {dataset_path}:{row_number}: {exc}") from exc
    return cases


# Reference loaders keyed by file extension. Each conforms to the
# ``DatasetLoader`` interface; register your own here (or pass it explicitly)
# to support additional formats.
_LOADERS: dict[str, DatasetLoader] = {
    ".jsonl": load_jsonl_cases,
    ".json": load_json_cases,
    ".csv": load_csv_cases,
}


def load_cases(path: str | Path) -> list[TestCase]:
    """Load a dataset, dispatching to a loader by file extension.

    Supported out of the box: ``.jsonl``, ``.json``, ``.csv``. All loaders
    return an equivalent ``list[TestCase]``.
    """

    dataset_path = Path(path)
    suffix = dataset_path.suffix.lower()
    loader = _LOADERS.get(suffix)
    if loader is None:
        supported = ", ".join(sorted(_LOADERS))
        raise ValueError(
            f"Unsupported dataset format '{suffix or dataset_path.name}'. "
            f"Supported extensions: {supported}."
        )
    return loader(dataset_path)
