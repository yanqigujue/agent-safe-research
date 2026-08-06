from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..models import Document
from ..registry import DATASETS


@DATASETS.register("elecbench")
class ElecbenchDataset:
    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config

    def load(self, project_root: Path) -> list[Document]:
        value = self.config.get("path", "知识库污染数据集/Elecbench中文版")
        data_dir = Path(value)
        if not data_dir.is_absolute():
            data_dir = project_root / data_dir
        if not data_dir.exists():
            raise FileNotFoundError(f"Elecbench directory not found: {data_dir}")

        documents: list[Document] = []
        for path in sorted(data_dir.glob("*.jsonl")):
            topic = path.stem.replace("_zh", "")
            with path.open("r", encoding="utf-8") as handle:
                for row_index, line in enumerate(handle):
                    if not line.strip():
                        continue
                    row = json.loads(line)
                    question = row.get("input") or row.get("perturbed_input") or row.get("perturbed input") or ""
                    answer = row.get("output") or ""
                    input_class = row.get("input_class", topic)
                    index_class = row.get("index_class", "")
                    doc_id = f"{path.stem}:{row_index}"
                    text = (
                        f"来源: Elecbench中文版/{path.name}\n"
                        f"主题: {input_class}\n"
                        f"问题: {question}\n"
                        f"参考答案: {answer}\n"
                        f"样本类型: {index_class}"
                    )
                    documents.append(
                        Document(
                            doc_id=doc_id,
                            text=text,
                            question=question,
                            answer=answer,
                            metadata={
                                "source_file": path.name,
                                "row_index": row_index,
                                "topic": topic,
                                "input_class": input_class,
                                "index_class": index_class,
                                "is_poison": False,
                            },
                        )
                    )
        if not documents:
            raise ValueError(f"No JSONL documents found in {data_dir}")
        return documents


@DATASETS.register("jsonl")
class GenericJsonlDataset:
    """Load a custom JSONL corpus using configurable field names."""

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config

    def load(self, project_root: Path) -> list[Document]:
        value = self.config.get("path")
        if not value:
            raise ValueError("dataset.path is required for dataset.type=jsonl")
        path = Path(value)
        if not path.is_absolute():
            path = project_root / path
        fields = self.config.get("fields", {})
        id_field = fields.get("id", "doc_id")
        text_field = fields.get("text", "text")
        question_field = fields.get("question", "question")
        answer_field = fields.get("answer", "answer")
        documents: list[Document] = []
        with path.open("r", encoding="utf-8") as handle:
            for index, line in enumerate(handle):
                if not line.strip():
                    continue
                row = json.loads(line)
                documents.append(
                    Document(
                        doc_id=str(row.get(id_field, f"{path.stem}:{index}")),
                        text=str(row.get(text_field, "")),
                        question=str(row.get(question_field, "")),
                        answer=str(row.get(answer_field, "")),
                        metadata={**row.get("metadata", {}), "source_file": path.name, "row_index": index},
                    )
                )
        return documents

