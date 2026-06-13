from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class TestCase(StrictModel):
    id: str
    input: str
    expected_behavior: str | None = None
    tags: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class RetrievedDocument(StrictModel):
    doc_id: str
    content: str
    source: str = "mock"
    poisoned: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


class AttackResult(StrictModel):
    attack_type: str
    prompt: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class ModelResponse(StrictModel):
    content: str
    model: str
    raw: dict[str, Any] = Field(default_factory=dict)
    latency_ms: float | None = None


class EvaluationResult(StrictModel):
    passed: bool
    label: str
    score: float = 0.0
    reasons: list[str] = Field(default_factory=list)


class ErrorRecord(StrictModel):
    node: str
    error_type: str
    message: str
    hint: str | None = None
    timestamp: str = Field(default_factory=utc_now_iso)


class TraceEvent(StrictModel):
    node: str
    status: str
    message: str
    timestamp: str = Field(default_factory=utc_now_iso)
    data: dict[str, Any] = Field(default_factory=dict)


class FormalTrustState(StrictModel):
    run_id: str
    case: TestCase
    prompt: str | None = None
    attack: AttackResult | None = None
    retrieval_context: list[RetrievedDocument] = Field(default_factory=list)
    model_response: ModelResponse | None = None
    evaluation: EvaluationResult | None = None
    metrics: dict[str, Any] = Field(default_factory=dict)
    errors: list[ErrorRecord] = Field(default_factory=list)
    trace: list[TraceEvent] = Field(default_factory=list)
    artifacts: dict[str, str] = Field(default_factory=dict)
    halted: bool = False

    @classmethod
    def allowed_patch_fields(cls) -> set[str]:
        return set(cls.model_fields)

    def add_trace(self, node: str, status: str, message: str, **data: Any) -> "FormalTrustState":
        return self.model_copy(
            update={
                "trace": [
                    *self.trace,
                    TraceEvent(node=node, status=status, message=message, data=data),
                ]
            }
        )

    def add_error(
        self,
        node: str,
        message: str,
        *,
        error_type: str = "NodeExecutionError",
        hint: str | None = None,
    ) -> "FormalTrustState":
        return self.model_copy(
            update={
                "errors": [
                    *self.errors,
                    ErrorRecord(node=node, error_type=error_type, message=message, hint=hint),
                ],
                "halted": True,
                "trace": [
                    *self.trace,
                    TraceEvent(node=node, status="error", message=message),
                ],
            }
        )


def state_to_dict(state: FormalTrustState) -> dict[str, Any]:
    return state.model_dump(mode="json")

