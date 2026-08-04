import json
from pathlib import Path

import pytest

from formaltrust_platform.config import EdgeSpec, GraphConfig, NodeSpec
from formaltrust_platform.datasets import load_cases
from formaltrust_platform.graph import build_graph
from formaltrust_platform.interfaces import (
    AttackNode,
    EvaluatorNode,
    ModelNode,
    NodeConfigError,
    validate_config,
)
from formaltrust_platform.nodes.attacks import template_attack_node
from formaltrust_platform.nodes.evaluators import rule_evaluator_node
from formaltrust_platform.nodes.models import mock_model_node, openai_compatible_model_node
from formaltrust_platform.registry import NodeRegistry


def test_builtins_expose_category_and_config_requirements() -> None:
    registry = NodeRegistry.with_builtins()
    catalog = {d.node_id: d for d in registry.catalog()}

    assert set(catalog) == {
        "analysis.claim_extraction",
        "attack.evidence_rag_poisoning",
        "attack.template",
        "evaluate.action",
        "evaluate.rules",
        "guardrail.evidence_action_gate",
        "guardrail.input.noop",
        "guardrail.output.noop",
        "model.deepseek_action",
        "model.metadata_action",
        "model.mock",
        "model.openai_compatible",
        "retrieval.conflict_aware_rerank",
    }
    assert catalog["model.openai_compatible"].category == "model"
    required = {f.name for f in catalog["model.openai_compatible"].config_fields if f.required}
    assert required == {"base_url", "model", "api_key_env"}
    # The API key field declares that its value names an env var (a secret).
    api_key = next(f for f in catalog["model.openai_compatible"].config_fields if f.name == "api_key_env")
    assert api_key.secret_env is True


def test_validate_config_flags_missing_unknown_and_wrong_type() -> None:
    registry = NodeRegistry.with_builtins()
    descriptor = registry.describe("model.openai_compatible")

    missing = validate_config(descriptor, {}, check_env=False)
    assert any("missing required config 'base_url'" in m for m in missing)

    unknown = validate_config(
        descriptor,
        {"base_url": "u", "model": "m", "api_key_env": "K", "bogus": 1},
        check_env=False,
    )
    assert any("unknown config field 'bogus'" in m for m in unknown)

    wrong_type = validate_config(
        descriptor,
        {"base_url": "u", "model": "m", "api_key_env": "K", "timeout_seconds": "soon"},
        check_env=False,
    )
    assert any("timeout_seconds' should be float" in m for m in wrong_type)


def test_validate_config_reports_missing_secret_env(monkeypatch: pytest.MonkeyPatch) -> None:
    registry = NodeRegistry.with_builtins()
    descriptor = registry.describe("model.openai_compatible")
    monkeypatch.delenv("FT_TEST_MISSING_KEY", raising=False)

    issues = validate_config(
        descriptor,
        {"base_url": "u", "model": "m", "api_key_env": "FT_TEST_MISSING_KEY"},
        check_env=True,
    )
    assert any("FT_TEST_MISSING_KEY" in m and "not set" in m for m in issues)

    # The same config is structurally valid when the env check is off (assembly time).
    assert validate_config(
        descriptor,
        {"base_url": "u", "model": "m", "api_key_env": "FT_TEST_MISSING_KEY"},
        check_env=False,
    ) == []


def test_build_graph_fails_fast_on_missing_required_config() -> None:
    registry = NodeRegistry.with_builtins()
    graph = GraphConfig(
        nodes=[NodeSpec(name="model", node_id="model.openai_compatible", config={"model": "m", "api_key_env": "K"})],
        edges=[EdgeSpec(from_node="START", to="model"), EdgeSpec(from_node="model", to="END")],
    )

    with pytest.raises(NodeConfigError) as exc:
        build_graph(graph, registry)

    message = str(exc.value)
    assert "model" in message
    assert "model.openai_compatible" in message
    assert "base_url" in message


def test_plain_callables_remain_registerable_without_a_descriptor() -> None:
    registry = NodeRegistry.with_builtins()

    def custom(state, config):
        return {"metrics": {"seen": True}}

    registry.register("custom.node", custom)

    assert registry.get("custom.node") is custom
    assert registry.describe("custom.node").category == "custom"
    assert registry.describe("custom.node").config_fields == []


def test_builtin_nodes_satisfy_their_role_protocols() -> None:
    assert isinstance(template_attack_node, AttackNode)
    assert isinstance(mock_model_node, ModelNode)
    assert isinstance(openai_compatible_model_node, ModelNode)
    assert isinstance(rule_evaluator_node, EvaluatorNode)


def _core(cases) -> list[tuple]:
    return [(c.id, c.input, c.expected_behavior, c.tags) for c in cases]


def test_load_cases_treats_jsonl_json_and_csv_equivalently(tmp_path: Path) -> None:
    rows = [
        {"id": "c1", "input": "hello", "expected_behavior": "be safe", "tags": ["x", "y"]},
        {"id": "c2", "input": "世界"},
    ]
    jsonl_path = tmp_path / "cases.jsonl"
    jsonl_path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows), encoding="utf-8")
    json_path = tmp_path / "cases.json"
    json_path.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
    csv_path = tmp_path / "cases.csv"
    csv_path.write_text(
        "id,input,expected_behavior,tags\nc1,hello,be safe,x;y\nc2,世界,,\n",
        encoding="utf-8",
    )

    expected = [("c1", "hello", "be safe", ["x", "y"]), ("c2", "世界", None, [])]
    assert _core(load_cases(jsonl_path)) == expected
    assert _core(load_cases(json_path)) == expected
    assert _core(load_cases(csv_path)) == expected


def test_csv_extra_columns_become_metadata(tmp_path: Path) -> None:
    csv_path = tmp_path / "cases.csv"
    csv_path.write_text("id,input,domain\nc1,hello,power\n", encoding="utf-8")

    cases = load_cases(csv_path)
    assert cases[0].metadata == {"domain": "power"}


def test_load_cases_rejects_unsupported_extension(tmp_path: Path) -> None:
    bad = tmp_path / "cases.txt"
    bad.write_text("nope", encoding="utf-8")

    with pytest.raises(ValueError) as exc:
        load_cases(bad)
    assert "Unsupported dataset format" in str(exc.value)
