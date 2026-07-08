import pytest
from pydantic import ValidationError

from formaltrust_platform.agent_interfaces import (
    AGENT_RUNTIME_SCHEMA_VERSION,
    AgentAction,
    AgentAuthorityConsumption,
    AgentAuthorityGrant,
    AgentComponentDescriptor,
    AgentRuntimeDescriptor,
    AgentRuntimeTrace,
    AgentTraceEvent,
    agent_interface_catalog,
)


def test_agent_runtime_trace_represents_codex_like_skill_tool_memory_flow() -> None:
    skill_authority = AgentAuthorityGrant(
        source_id="skill.report_formatter",
        source_type="skill",
        semantic_roles=["risk_report_formatting_authority"],
        fields=["risk_report"],
        operations=["format_report"],
        data_scope=["current_case"],
        effect_scope=["report_draft"],
    )
    skill = AgentComponentDescriptor(
        component_id="skill.report_formatter",
        kind="skill",
        name="Report formatter",
        provider="codex-like",
        authority=skill_authority,
    )
    tool = AgentComponentDescriptor(
        component_id="tool.dispatch_console",
        kind="tool",
        provider="mcp",
        requires_approval=True,
        side_effects=["dispatch_work_order"],
        payload={"mcp_server": "power-ops"},
    )
    memory = AgentComponentDescriptor(
        component_id="memory.operator_style",
        kind="memory",
        provider="runtime",
        payload={"memory_type": "preference", "writable": False},
    )
    action = AgentAction(
        action_id="action-1",
        decision="direct_execute",
        tool="tool.dispatch_console",
        risk_level="high",
        requires_human_approval=False,
        supporting_claims=["skill.report_formatter"],
        rationale="A formatting skill was incorrectly consumed as dispatch authority.",
        consumptions=[
            AgentAuthorityConsumption(
                field="side_effect",
                operation="dispatch_work_order",
                attributed_source_id="skill.report_formatter",
                required_role="dispatch_operation_authority",
                effect_scope="maintenance_dispatch",
            )
        ],
    )

    trace = AgentRuntimeTrace(
        runtime=AgentRuntimeDescriptor(
            agent_id="codex-like-power-agent",
            family="codex-like",
            component_ids=[skill.component_id, tool.component_id, memory.component_id],
        ),
        components=[skill, tool, memory],
        actions=[action],
        authorities=[skill_authority],
        events=[
            AgentTraceEvent(
                event_id="evt-1",
                event_type="skill.invoked",
                agent_id="codex-like-power-agent",
                component_id=skill.component_id,
                source_id=skill_authority.source_id,
                source_type=skill_authority.source_type,
                authority=skill_authority,
            ),
            AgentTraceEvent(
                event_id="evt-2",
                event_type="action.candidate",
                agent_id="codex-like-power-agent",
                action=action,
            ),
        ],
    )

    assert trace.schema_version == AGENT_RUNTIME_SCHEMA_VERSION
    assert {component.kind for component in trace.components} == {"skill", "tool", "memory"}
    assert trace.events[1].action is not None
    assert trace.events[1].action.consumptions[0].required_role == "dispatch_operation_authority"


def test_agent_trace_event_accepts_vendor_extensions_without_schema_changes() -> None:
    event = AgentTraceEvent(
        event_id="vendor-evt-1",
        event_type="langgraph.node.transition",
        agent_id="langgraph-agent",
        component_id="planner.graph",
        payload={"from": "retrieve", "to": "act"},
        metadata={"raw_event_name": "node_transition"},
    )

    assert event.event_type == "langgraph.node.transition"
    assert event.payload["to"] == "act"


def test_agent_interfaces_forbid_unstructured_extra_fields() -> None:
    with pytest.raises(ValidationError):
        AgentTraceEvent(
            event_id="bad-extra",
            event_type="custom",
            agent_id="agent",
            unexpected="put this in payload instead",
        )


def test_agent_interface_catalog_exposes_stable_models() -> None:
    catalog = agent_interface_catalog()
    model_names = {model["name"] for model in catalog["models"]}

    assert catalog["schema_version"] == AGENT_RUNTIME_SCHEMA_VERSION
    assert "skill" in catalog["canonical_component_kinds"]
    assert "action.candidate" in catalog["canonical_event_types"]
    assert "AgentRuntimeTrace" in model_names
    assert "AgentComponentDescriptor" in model_names
    assert "AgentTraceEvent" in model_names
