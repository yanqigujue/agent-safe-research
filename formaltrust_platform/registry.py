from __future__ import annotations

from formaltrust_platform.interfaces import (
    NodeCallable,
    NodeCategory,
    NodeDescriptor,
    get_descriptor,
)

# ``NodeCallable`` is re-exported for backwards compatibility — it used to be
# defined in this module.
__all__ = ["NodeCallable", "NodeCategory", "NodeDescriptor", "NodeRegistry", "UnknownNodeError"]


class UnknownNodeError(KeyError):
    pass


class NodeRegistry:
    """A discoverable catalog of node implementations keyed by ``node_id``.

    Each entry is a :class:`NodeDescriptor` carrying the node's category, a
    summary, and its declared configuration requirements. The registry supports
    two registration styles:

    * ``register(func)`` for a ``@node(...)``-decorated function (uses its
      declared descriptor), and
    * ``register(node_id, func)`` for a plain callable (recorded as an
      uncategorised ``custom`` node with no declared config).
    """

    def __init__(self) -> None:
        self._nodes: dict[str, NodeDescriptor] = {}

    @classmethod
    def with_builtins(cls) -> "NodeRegistry":
        registry = cls()
        from formaltrust_platform.nodes.attacks import template_attack_node
        from formaltrust_platform.nodes.evaluators import rule_evaluator_node
        from formaltrust_platform.nodes.evidence_action import (
            action_evaluator_node,
            claim_extraction_node,
            conflict_aware_rerank_node,
            deepseek_action_model_node,
            evidence_action_gate_node,
            evidence_rag_poisoning_node,
            metadata_action_model_node,
        )
        from formaltrust_platform.nodes.guardrails import (
            input_noop_guardrail_node,
            output_noop_guardrail_node,
        )
        from formaltrust_platform.nodes.models import mock_model_node, openai_compatible_model_node

        for builtin in (
            template_attack_node,
            input_noop_guardrail_node,
            output_noop_guardrail_node,
            mock_model_node,
            openai_compatible_model_node,
            rule_evaluator_node,
            evidence_rag_poisoning_node,
            conflict_aware_rerank_node,
            claim_extraction_node,
            metadata_action_model_node,
            deepseek_action_model_node,
            evidence_action_gate_node,
            action_evaluator_node,
        ):
            registry.register(builtin)
        return registry

    def register(self, node_or_id, node=None) -> None:
        """Register a node.

        ``register(func)`` — ``func`` must be ``@node(...)``-decorated.
        ``register(node_id, func)`` — register any callable under ``node_id``;
        if ``func`` carries a descriptor it is reused (re-keyed to ``node_id``),
        otherwise a plain ``custom`` descriptor is created.
        """

        if node is None:
            func = node_or_id
            descriptor = get_descriptor(func)
            if descriptor is None:
                raise TypeError(
                    "register(func) requires a function declared with @node(...); "
                    "use register(node_id, func) for plain callables."
                )
            self._nodes[descriptor.node_id] = descriptor
            return

        node_id = node_or_id
        func = node
        descriptor = get_descriptor(func)
        if descriptor is None:
            descriptor = NodeDescriptor(node_id=node_id, category="custom", func=func)
        elif descriptor.node_id != node_id:
            descriptor = descriptor.model_copy(update={"node_id": node_id})
        self._nodes[node_id] = descriptor

    def get(self, node_id: str) -> NodeCallable:
        return self._descriptor(node_id).func

    def describe(self, node_id: str) -> NodeDescriptor:
        """Return the full interface descriptor for a registered node."""

        return self._descriptor(node_id)

    def catalog(self) -> list[NodeDescriptor]:
        """List every registered node's interface, ordered by category then id."""

        return sorted(self._nodes.values(), key=lambda d: (d.category, d.node_id))

    def ids(self) -> list[str]:
        return sorted(self._nodes)

    def _descriptor(self, node_id: str) -> NodeDescriptor:
        try:
            return self._nodes[node_id]
        except KeyError as exc:
            registered = ", ".join(sorted(self._nodes)) or "<none>"
            raise UnknownNodeError(
                f"Unknown node id '{node_id}'. Available registered node ids: {registered}"
            ) from exc
