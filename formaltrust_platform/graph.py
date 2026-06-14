from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from langgraph.graph import END, START, StateGraph
from pydantic import ValidationError

from formaltrust_platform.config import GraphConfig, NodeSpec
from formaltrust_platform.interfaces import NodeConfigError, validate_config
from formaltrust_platform.registry import NodeCallable, NodeRegistry
from formaltrust_platform.state import FormalTrustState, state_to_dict


class NodePatchError(ValueError):
    pass


def build_graph(config: GraphConfig, registry: NodeRegistry):
    graph = StateGraph(FormalTrustState)
    node_names = {node.name for node in config.nodes}

    for node_spec in config.nodes:
        descriptor = registry.describe(node_spec.node_id)
        # Fail fast (once, at assembly time) with a friendly diagnostic instead
        # of a deep KeyError inside the node. Secrets are not checked here so a
        # graph can be validated offline; nodes still read keys at run time.
        issues = validate_config(descriptor, node_spec.config, check_env=False)
        if issues:
            joined = "; ".join(issues)
            raise NodeConfigError(
                f"Node '{node_spec.name}' ({node_spec.node_id}) has invalid config: {joined}"
            )
        graph.add_node(node_spec.name, _wrap_node(node_spec, descriptor.func))

    for edge in config.edges:
        source = _edge_endpoint(edge.from_node, node_names)
        target = _edge_endpoint(edge.to, node_names)
        if edge.condition:
            false_target = _edge_endpoint(edge.else_to or "END", node_names)
            graph.add_conditional_edges(
                source,
                _condition(edge.condition),
                {True: target, False: false_target},
            )
        else:
            graph.add_edge(source, target)

    return graph.compile()


def _wrap_node(node_spec: NodeSpec, node: NodeCallable):
    def wrapped(raw_state: FormalTrustState | Mapping[str, Any]) -> dict[str, Any]:
        state = FormalTrustState.model_validate(raw_state)
        if state.halted:
            return state_to_dict(state)

        try:
            patch = node(state, node_spec.config) or {}
            next_state = _apply_patch(state, patch)
            next_state = next_state.add_trace(node_spec.name, "ok", f"Node '{node_spec.name}' completed")
            return state_to_dict(next_state)
        except NodePatchError as exc:
            errored = state.add_error(
                node_spec.name,
                str(exc),
                error_type="InvalidNodePatch",
                hint="Return only fields defined by FormalTrustState.",
            )
            return state_to_dict(errored)
        except ValidationError as exc:
            errored = state.add_error(
                node_spec.name,
                f"Node returned data that does not match FormalTrustState: {exc}",
                error_type="StateValidationError",
                hint="Check nested field shapes and Pydantic model types.",
            )
            return state_to_dict(errored)
        except Exception as exc:  # noqa: BLE001 - node failures must be captured as artifacts
            errored = state.add_error(node_spec.name, str(exc), error_type=type(exc).__name__)
            return state_to_dict(errored)

    return wrapped


def _apply_patch(state: FormalTrustState, patch: Mapping[str, Any]) -> FormalTrustState:
    allowed = FormalTrustState.allowed_patch_fields()
    invalid = [field for field in patch if field not in allowed]
    if invalid:
        raise NodePatchError(f"Invalid state patch field '{invalid[0]}'")

    merged = state.model_dump(mode="python")
    for field, value in patch.items():
        if field in {"metrics", "artifacts"} and isinstance(value, Mapping):
            merged[field] = {**merged.get(field, {}), **dict(value)}
        else:
            merged[field] = value
    return FormalTrustState.model_validate(merged)


def _edge_endpoint(name: str | None, node_names: set[str]) -> str:
    if name == "START":
        return START
    if name == "END" or name is None:
        return END
    if name not in node_names:
        known = ", ".join(sorted(node_names))
        raise ValueError(f"Graph edge references unknown node '{name}'. Known nodes: {known}")
    return name


def _condition(name: str):
    if name == "has_errors":
        return lambda state: bool(FormalTrustState.model_validate(state).errors)
    if name == "no_errors":
        return lambda state: not bool(FormalTrustState.model_validate(state).errors)
    if name == "halted":
        return lambda state: bool(FormalTrustState.model_validate(state).halted)
    raise ValueError("Unknown condition '%s'. Supported conditions: has_errors, no_errors, halted" % name)

