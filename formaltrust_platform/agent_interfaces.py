"""Stable Agent runtime interface contracts for FormalTrust.

FormalTrust executes graphs of nodes. Agent runtimes, however, expose a wider
surface: models, tools, skills, memory, approvals, plans, delegated subagents,
and traces. This module defines a small versioned interface that can represent
those surfaces without baking in one framework's vocabulary.

Design rules:

* Keep the platform state stable. Normalized agent objects live in
  ``case.metadata``, ``metrics``, or ``artifacts``; they do not add top-level
  ``FormalTrustState`` fields.
* Use a small stable core plus ``payload`` / ``metadata`` extension maps.
* Prefer one generic component descriptor over per-framework classes.
* Treat canonical event and component names as recommendations, not hard
  validation gates, so new agent runtimes can still be imported.
"""

from __future__ import annotations

from typing import Any

from pydantic import Field

from formaltrust_platform.state import StrictModel


AGENT_RUNTIME_SCHEMA_VERSION = "agent-runtime-interface/v1"

CANONICAL_COMPONENT_KINDS = [
    "model",
    "planner",
    "retriever",
    "skill",
    "tool",
    "memory",
    "approval",
    "guardrail",
    "evaluator",
    "subagent",
    "runtime",
    "custom",
]

CANONICAL_EVENT_TYPES = [
    "agent.started",
    "agent.finished",
    "model.called",
    "plan.created",
    "plan.step.selected",
    "retrieval.performed",
    "skill.discovered",
    "skill.selected",
    "skill.invoked",
    "skill.output",
    "tool.selected",
    "tool.called",
    "tool.result",
    "memory.read",
    "memory.write",
    "approval.requested",
    "approval.granted",
    "approval.denied",
    "delegation.created",
    "subagent.spawned",
    "action.candidate",
    "action.final",
    "authority.granted",
    "authority.consumed",
    "authority.counter",
    "error",
    "custom",
]

CANONICAL_SOURCE_TYPES = [
    "evidence",
    "skill",
    "tool_metadata",
    "memory",
    "user_approval",
    "prior_step_output",
    "model",
    "planner",
    "system",
    "human",
    "custom",
]

CANONICAL_ACTION_FIELDS = [
    "decision",
    "tool",
    "tool_arguments",
    "parameters",
    "requires_human_approval",
    "risk_level",
    "risk_report",
    "data_scope",
    "side_effect",
    "delegation",
    "rationale",
]


class AgentJsonSchema(StrictModel):
    """Optional JSON-schema-style IO contract."""

    schema_id: str | None = None
    json_schema: dict[str, Any] = Field(default_factory=dict)
    required_fields: list[str] = Field(default_factory=list)
    semantic_roles: list[str] = Field(default_factory=list)
    description: str = ""


class AgentAuthorityGrant(StrictModel):
    """Capability/authority granted by a source or required by a field.

    This is the common manifest shape for evidence, skill output, tool metadata,
    memory, user approval, prior-step output, and delegated subagents.
    """

    grant_id: str | None = None
    source_id: str
    source_type: str
    semantic_roles: list[str] = Field(default_factory=list)
    fields: list[str] = Field(default_factory=list)
    operations: list[str] = Field(default_factory=list)
    data_scope: list[str] = Field(default_factory=list)
    effect_scope: list[str] = Field(default_factory=list)
    delegation_scope: list[str] = Field(default_factory=list)
    time_scope: dict[str, Any] = Field(default_factory=dict)
    obligations: list[str] = Field(default_factory=list)
    counter_authority: list[str] = Field(default_factory=list)
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    payload: dict[str, Any] = Field(default_factory=dict)


class AgentComponentDescriptor(StrictModel):
    """Framework-neutral descriptor for a model, skill, tool, memory, etc."""

    component_id: str
    kind: str
    name: str = ""
    provider: str = ""
    version: str = ""
    description: str = ""
    input_contract: AgentJsonSchema = Field(default_factory=AgentJsonSchema)
    output_contract: AgentJsonSchema = Field(default_factory=AgentJsonSchema)
    authority: AgentAuthorityGrant | None = None
    side_effects: list[str] = Field(default_factory=list)
    requires_approval: bool = False
    payload: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentRuntimeDescriptor(StrictModel):
    """Top-level identity and advertised surface of the agent under test."""

    agent_id: str
    name: str = ""
    family: str = "custom"
    version: str = ""
    description: str = ""
    model_component_id: str | None = None
    planner_component_id: str | None = None
    component_ids: list[str] = Field(default_factory=list)
    default_authority: AgentAuthorityGrant | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentAuthorityConsumption(StrictModel):
    """A field-level edge from an action field to a source authority grant."""

    field: str
    operation: str
    attributed_source_id: str
    required_role: str = ""
    data_scope: str | None = None
    effect_scope: str | None = None
    delegation_scope: str | None = None
    evidence: list[str] = Field(default_factory=list)
    payload: dict[str, Any] = Field(default_factory=dict)


class AgentAction(StrictModel):
    """Normalized candidate or final action emitted by an agent."""

    decision: str
    tool: str = "none"
    risk_level: str = "unknown"
    requires_human_approval: bool = False
    supporting_claims: list[str] = Field(default_factory=list)
    rationale: str = ""
    action_id: str | None = None
    parameters: dict[str, Any] = Field(default_factory=dict)
    side_effects: list[str] = Field(default_factory=list)
    consumptions: list[AgentAuthorityConsumption] = Field(default_factory=list)
    payload: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentTraceEvent(StrictModel):
    """Canonical trace event after adapting a framework-specific log."""

    event_id: str
    event_type: str
    agent_id: str
    timestamp: str | None = None
    span_id: str | None = None
    parent_span_id: str | None = None
    step_id: str | None = None
    component_id: str | None = None
    source_id: str | None = None
    source_type: str | None = None
    action: AgentAction | None = None
    authority: AgentAuthorityGrant | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentRuntimeTrace(StrictModel):
    """Versioned envelope for importing one agent runtime trace."""

    schema_version: str = AGENT_RUNTIME_SCHEMA_VERSION
    runtime: AgentRuntimeDescriptor
    components: list[AgentComponentDescriptor] = Field(default_factory=list)
    events: list[AgentTraceEvent] = Field(default_factory=list)
    actions: list[AgentAction] = Field(default_factory=list)
    authorities: list[AgentAuthorityGrant] = Field(default_factory=list)
    payload: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


def agent_interface_catalog() -> dict[str, Any]:
    """Return JSON-schema-backed descriptions for external tools and the UI."""

    models = [
        AgentRuntimeTrace,
        AgentRuntimeDescriptor,
        AgentComponentDescriptor,
        AgentAuthorityGrant,
        AgentAction,
        AgentAuthorityConsumption,
        AgentTraceEvent,
    ]
    return {
        "schema_version": AGENT_RUNTIME_SCHEMA_VERSION,
        "storage_policy": (
            "Store normalized agent runtime objects under case.metadata, metrics, or artifacts; "
            "do not add FormalTrustState top-level fields."
        ),
        "canonical_component_kinds": CANONICAL_COMPONENT_KINDS,
        "canonical_event_types": CANONICAL_EVENT_TYPES,
        "canonical_source_types": CANONICAL_SOURCE_TYPES,
        "canonical_action_fields": CANONICAL_ACTION_FIELDS,
        "models": [
            {
                "name": model.__name__,
                "schema": model.model_json_schema(),
            }
            for model in models
        ],
    }


__all__ = [
    "AGENT_RUNTIME_SCHEMA_VERSION",
    "CANONICAL_ACTION_FIELDS",
    "CANONICAL_COMPONENT_KINDS",
    "CANONICAL_EVENT_TYPES",
    "CANONICAL_SOURCE_TYPES",
    "AgentAction",
    "AgentAuthorityConsumption",
    "AgentAuthorityGrant",
    "AgentComponentDescriptor",
    "AgentJsonSchema",
    "AgentRuntimeDescriptor",
    "AgentRuntimeTrace",
    "AgentTraceEvent",
    "agent_interface_catalog",
]
