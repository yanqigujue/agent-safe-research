"""Extension interface contracts for the FormalTrust platform.

This module is the single source of truth for *what an extension must look like*
and *what configuration it requires*. Every pluggable part of the pipeline —
attack / guardrail / model / evaluator nodes, dataset loaders, reporters —
has a clear, documented contract here.

Three concepts:

* **Role protocols** (`AttackNode`, `GuardrailNode`, `ModelNode`,
  `EvaluatorNode`, `DatasetLoader`, `Reporter`) declare the call signature and,
  in their docstrings, the *input/output contract* of each role.
* **`ConfigField`** declares one configuration requirement (name, type,
  whether it is required, default, description, and whether it names a secret
  environment variable).
* **`NodeDescriptor`** binds a node implementation to its interface metadata
  (id, category, summary, config requirements). The `@node(...)` decorator is
  the ergonomic way to attach one.

`validate_config` checks a YAML node ``config`` block against a descriptor's
declared requirements and returns human-readable problems, so callers can fail
fast with a friendly diagnostic instead of a deep ``KeyError``.
"""

from __future__ import annotations

import os
from collections.abc import Callable, Mapping, Sequence
from typing import Any, Literal, Protocol, runtime_checkable

from pydantic import ConfigDict, Field

from formaltrust_platform.state import FormalTrustState, StrictModel, TestCase

# A node returns a *patch*: a dict whose keys must be a subset of
# ``FormalTrustState`` fields (enforced later by ``graph._apply_patch``).
NodePatch = dict[str, Any]

NodeCategory = Literal["attack", "guardrail", "model", "evaluator", "custom"]


@runtime_checkable
class Node(Protocol):
    """The universal node call signature shared by every role.

    A node reads from ``state``, reads its own settings from ``config`` (the
    YAML ``config`` block of this node), and returns a patch dict (or ``None``
    for "no change"). It must never mutate ``state`` in place.
    """

    def __call__(self, state: FormalTrustState, config: Mapping[str, Any]) -> NodePatch | None: ...


# Historically defined in ``registry.py``; kept here as the canonical alias.
NodeCallable = Callable[[FormalTrustState, Mapping[str, Any]], "NodePatch | None"]


@runtime_checkable
class AttackNode(Protocol):
    """Attack node contract.

    Reads:  ``state.case.input``.
    Writes: MUST return ``{"prompt": str}``; SHOULD also include
            ``{"attack": AttackResult}`` describing the transformation. May add
            ``retrieval_context`` for retrieval-style attacks.
    """

    def __call__(self, state: FormalTrustState, config: Mapping[str, Any]) -> NodePatch | None: ...


@runtime_checkable
class GuardrailNode(Protocol):
    """Guardrail node contract.

    An *input* guardrail reads/rewrites ``state.prompt`` before the model call;
    an *output* guardrail inspects ``state.model_response`` afterwards. A
    guardrail MAY block the pipeline by raising, or by recording an error via
    ``state.add_error(...)`` (which sets ``halted``). Returning ``None`` or a
    metrics-only patch means "allow".
    """

    def __call__(self, state: FormalTrustState, config: Mapping[str, Any]) -> NodePatch | None: ...


@runtime_checkable
class ModelNode(Protocol):
    """Model node contract.

    Reads:  ``state.prompt`` (falling back to ``state.case.input``).
    Writes: MUST return ``{"model_response": ModelResponse}``.
    Secrets MUST be read from environment variables (declared via a
    ``ConfigField(..., secret_env=True)``), never embedded in ``config``.
    """

    def __call__(self, state: FormalTrustState, config: Mapping[str, Any]) -> NodePatch | None: ...


@runtime_checkable
class EvaluatorNode(Protocol):
    """Evaluator node contract.

    Reads:  ``state.model_response``.
    Writes: MUST return ``{"evaluation": EvaluationResult}``.
    """

    def __call__(self, state: FormalTrustState, config: Mapping[str, Any]) -> NodePatch | None: ...


@runtime_checkable
class DatasetLoader(Protocol):
    """Dataset loader contract: turn a dataset file path into test cases."""

    def __call__(self, path: str) -> list[TestCase]: ...


@runtime_checkable
class Reporter(Protocol):
    """Reporter contract: render a run into an artifact file and return its path."""

    def __call__(self, run_dir: Any, config: Any, summary: Any, states: Any) -> Any: ...


ConfigType = Literal["str", "int", "float", "bool", "list", "dict"]

_TYPE_MAP: dict[str, tuple[type, ...]] = {
    "str": (str,),
    "int": (int,),
    "float": (int, float),
    "bool": (bool,),
    "list": (list,),
    "dict": (dict, Mapping),
}


class ConfigField(StrictModel):
    """One declared configuration requirement for a node.

    ``secret_env=True`` marks a field whose *value is the name of an
    environment variable* holding a secret (e.g. an API key). The platform
    only ever checks that the variable exists — it never copies the secret
    into the config or any artifact.
    """

    name: str
    type: ConfigType = "str"
    required: bool = False
    default: Any = None
    description: str = ""
    secret_env: bool = False

    def __init__(self, name: str, **data: Any) -> None:
        # Ergonomic positional name: ConfigField("base_url", required=True, ...)
        super().__init__(name=name, **data)


class NodeDescriptor(StrictModel):
    """Interface metadata bound to a node implementation."""

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    node_id: str
    category: NodeCategory = "custom"
    summary: str = ""
    config_fields: list[ConfigField] = Field(default_factory=list)
    func: Callable[..., Any]


class NodeConfigError(ValueError):
    """Raised at graph-assembly time when a node's config violates its contract."""


def node(
    node_id: str,
    *,
    category: NodeCategory,
    summary: str = "",
    config_fields: Sequence[ConfigField] = (),
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Declare a node's interface inline and attach it to the function.

    The decorated function stays a plain callable (so it can still be called or
    registered directly); the descriptor is stashed on ``func.__node_descriptor__``
    and picked up by ``NodeRegistry.register``.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func.__node_descriptor__ = NodeDescriptor(  # type: ignore[attr-defined]
            node_id=node_id,
            category=category,
            summary=summary,
            config_fields=list(config_fields),
            func=func,
        )
        return func

    return decorator


def get_descriptor(func: Callable[..., Any]) -> NodeDescriptor | None:
    """Return the descriptor attached by ``@node``, or ``None`` for plain callables."""

    return getattr(func, "__node_descriptor__", None)


def validate_config(
    descriptor: NodeDescriptor,
    config: Mapping[str, Any],
    *,
    check_env: bool = True,
) -> list[str]:
    """Validate ``config`` against a descriptor's declared requirements.

    Returns a list of human-readable problems (empty means valid). Checks:
    missing required fields, wrong value types, unknown fields, and — when
    ``check_env`` is True — that ``secret_env`` fields name an environment
    variable that is actually set. ``check_env`` is False at graph-assembly
    time so a graph can be validated offline without secrets present.
    """

    issues: list[str] = []
    declared = {field.name: field for field in descriptor.config_fields}

    for field in descriptor.config_fields:
        present = field.name in config
        if not present:
            if field.required:
                detail = f" ({field.description})" if field.description else ""
                issues.append(f"missing required config '{field.name}'{detail}")
            continue

        value = config[field.name]
        expected = _TYPE_MAP.get(field.type)
        if expected is not None and value is not None and not isinstance(value, expected):
            issues.append(
                f"config '{field.name}' should be {field.type}, got {type(value).__name__}"
            )
        if check_env and field.secret_env and isinstance(value, str) and value and os.getenv(value) is None:
            issues.append(
                f"config '{field.name}' names environment variable '{value}', which is not set"
            )

    for key in config:
        if key not in declared:
            issues.append(f"unknown config field '{key}'")

    return issues
