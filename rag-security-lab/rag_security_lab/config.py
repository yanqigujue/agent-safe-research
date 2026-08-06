from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass
class ExperimentConfig:
    source_path: Path
    raw: dict[str, Any]

    @property
    def name(self) -> str:
        return str(self.raw["experiment"]["name"])

    @property
    def seed(self) -> int:
        return int(self.raw["experiment"].get("seed", 2026))

    @property
    def fingerprint(self) -> str:
        payload = json.dumps(self.raw, ensure_ascii=False, sort_keys=True).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()[:10]

    def section(self, name: str) -> dict[str, Any]:
        value = self.raw.get(name, {})
        if not isinstance(value, dict):
            raise ValueError(f"Config section '{name}' must be an object.")
        return deepcopy(value)

    def resolved(self, project_root: Path) -> dict[str, Any]:
        data = deepcopy(self.raw)
        data["_resolved"] = {
            "config_path": str(self.source_path.resolve()),
            "project_root": str(project_root.resolve()),
            "fingerprint": self.fingerprint,
        }
        return data


def load_config(path: str | Path) -> ExperimentConfig:
    config_path = Path(path).resolve()
    if not config_path.exists():
        raise FileNotFoundError(f"Config file does not exist: {config_path}")
    text = config_path.read_text(encoding="utf-8")
    if config_path.suffix.lower() == ".json":
        raw = json.loads(text)
    elif config_path.suffix.lower() in {".yaml", ".yml"}:
        raw = yaml.safe_load(text)
    else:
        raise ValueError("Config must be .yaml, .yml, or .json")
    if not isinstance(raw, dict):
        raise ValueError("Config root must be an object.")
    validate_config(raw)
    return ExperimentConfig(config_path, raw)


def validate_config(raw: dict[str, Any]) -> None:
    for section in ["experiment", "dataset", "queries", "attack", "retriever"]:
        if not isinstance(raw.get(section), dict):
            raise ValueError(f"Missing or invalid required section: {section}")
    if not str(raw["experiment"].get("name", "")).strip():
        raise ValueError("experiment.name is required")
    for section in ["dataset", "attack", "retriever"]:
        if not str(raw[section].get("type", "")).strip():
            raise ValueError(f"{section}.type is required")
    query_mode = raw["queries"].get("mode", "all")
    if query_mode not in {"all", "ids", "attack_targets", "filter"}:
        raise ValueError("queries.mode must be all, ids, attack_targets, or filter")
    top_k = raw["retriever"].get("top_k", 5)
    top_ks = top_k if isinstance(top_k, list) else [top_k]
    if not top_ks or any(int(value) < 1 for value in top_ks):
        raise ValueError("retriever.top_k must contain positive integers")


def resolve_path(value: str | Path, project_root: Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else project_root / path

