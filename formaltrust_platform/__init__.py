"""FormalTrust modular validation platform MVP."""

from formaltrust_platform.agent_interfaces import (
    AGENT_RUNTIME_SCHEMA_VERSION,
    CANONICAL_ACTION_FIELDS,
    CANONICAL_COMPONENT_KINDS,
    CANONICAL_EVENT_TYPES,
    CANONICAL_SOURCE_TYPES,
    AgentAction,
    AgentAuthorityConsumption,
    AgentAuthorityGrant,
    AgentComponentDescriptor,
    AgentJsonSchema,
    AgentRuntimeDescriptor,
    AgentRuntimeTrace,
    AgentTraceEvent,
    agent_interface_catalog,
)
from formaltrust_platform.config import ExperimentConfig, load_config
from formaltrust_platform.datasets import load_cases, load_jsonl_cases
from formaltrust_platform.interfaces import (
    AttackNode,
    ConfigField,
    DatasetLoader,
    EvaluatorNode,
    GuardrailNode,
    ModelNode,
    Node,
    NodeCategory,
    NodeConfigError,
    NodeDescriptor,
    Reporter,
    node,
    validate_config,
)
from formaltrust_platform.registry import NodeRegistry, UnknownNodeError
from formaltrust_platform.runner import ExperimentResult, ExperimentRunner

__all__ = [
    # Core runtime
    "ExperimentConfig",
    "ExperimentResult",
    "ExperimentRunner",
    "NodeRegistry",
    "UnknownNodeError",
    "load_config",
    "load_cases",
    "load_jsonl_cases",
    # Agent runtime interfaces
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
    # Extension interfaces
    "node",
    "ConfigField",
    "NodeDescriptor",
    "NodeCategory",
    "NodeConfigError",
    "validate_config",
    "Node",
    "AttackNode",
    "GuardrailNode",
    "ModelNode",
    "EvaluatorNode",
    "DatasetLoader",
    "Reporter",
]
