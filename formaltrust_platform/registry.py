from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from formaltrust_platform.state import FormalTrustState

NodeCallable = Callable[[FormalTrustState, Mapping[str, Any]], dict[str, Any] | None]


class UnknownNodeError(KeyError):
    pass


class NodeRegistry:
    def __init__(self) -> None:
        self._nodes: dict[str, NodeCallable] = {}

    @classmethod
    def with_builtins(cls) -> "NodeRegistry":
        registry = cls()
        from formaltrust_platform.nodes.attacks import template_attack_node
        from formaltrust_platform.nodes.evaluators import rule_evaluator_node
        from formaltrust_platform.nodes.guardrails import input_noop_guardrail_node, output_noop_guardrail_node
        from formaltrust_platform.nodes.models import mock_model_node, openai_compatible_model_node

        registry.register("attack.template", template_attack_node)
        registry.register("guardrail.input.noop", input_noop_guardrail_node)
        registry.register("guardrail.output.noop", output_noop_guardrail_node)
        registry.register("model.mock", mock_model_node)
        registry.register("model.openai_compatible", openai_compatible_model_node)
        registry.register("evaluate.rules", rule_evaluator_node)
        return registry

    def register(self, node_id: str, node: NodeCallable) -> None:
        self._nodes[node_id] = node

    def get(self, node_id: str) -> NodeCallable:
        try:
            return self._nodes[node_id]
        except KeyError as exc:
            registered = ", ".join(sorted(self._nodes)) or "<none>"
            raise UnknownNodeError(
                f"Unknown node id '{node_id}'. Available registered node ids: {registered}"
            ) from exc

    def ids(self) -> list[str]:
        return sorted(self._nodes)

