from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Document:
    doc_id: str
    text: str
    question: str = ""
    answer: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_poison(self) -> bool:
        return bool(self.metadata.get("is_poison", False))

    @property
    def target_qid(self) -> str | None:
        return self.metadata.get("target_qid")

    @property
    def target_topic(self) -> str | None:
        return self.metadata.get("target_topic")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Query:
    query_id: str
    text: str
    reference_answer: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class RetrievalHit:
    rank: int
    score: float
    document: Document

    def to_dict(self) -> dict[str, Any]:
        return {
            "rank": self.rank,
            "score": round(float(self.score), 8),
            "doc_id": self.document.doc_id,
            "is_poison": self.document.is_poison,
            "target_qid": self.document.target_qid,
            "target_topic": self.document.target_topic,
            "metadata": self.document.metadata,
        }


@dataclass
class AttackResult:
    documents: list[Document]
    poison_documents: list[Document]
    target_answers: dict[str, str] = field(default_factory=dict)
    target_topics: dict[str, str] = field(default_factory=dict)
    stats: dict[str, Any] = field(default_factory=dict)

    @property
    def target_ids(self) -> set[str]:
        return set(self.target_answers) | set(self.target_topics)

