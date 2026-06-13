from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field


class NodeSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    node_id: str
    config: dict[str, Any] = Field(default_factory=dict)


class EdgeSpec(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    from_node: str = Field(alias="from")
    to: str
    condition: str | None = None
    else_to: str | None = None


class GraphConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nodes: list[NodeSpec]
    edges: list[EdgeSpec]


class ExperimentConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    experiment_name: str
    dataset_path: Path
    output_dir: Path = Path("runs")
    graph: GraphConfig

    def with_output_dir(self, output_dir: Path) -> "ExperimentConfig":
        return self.model_copy(update={"output_dir": output_dir.resolve()})


def load_config(path: str | Path) -> ExperimentConfig:
    config_path = Path(path).resolve()
    with config_path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}

    config = ExperimentConfig.model_validate(payload)
    base_dir = config_path.parent
    dataset_path = _resolve_path(config.dataset_path, base_dir)
    output_dir = _resolve_path(config.output_dir, base_dir)
    return config.model_copy(update={"dataset_path": dataset_path, "output_dir": output_dir})


def _resolve_path(path: Path, base_dir: Path) -> Path:
    if path.is_absolute():
        return path.resolve()
    return (base_dir / path).resolve()

