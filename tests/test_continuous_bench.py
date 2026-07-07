from __future__ import annotations

import json
from pathlib import Path

import httpx

from formaltrust_platform.nodes.afw import afw_capguard_node, afw_runtime_evaluator_node
from formaltrust_platform.state import FormalTrustState, TestCase

from benchmarks.continuous_bench.continuous_bench import (
    OllamaModelRunner,
    append_jsonl_records,
    case_fingerprint,
    deduplicate_candidates,
    generate_candidate_cases,
    _generate_unique_valid_candidates,
    load_jsonl_records,
    load_seed_cases,
    run_continuous_bench,
    validate_case_schema,
)


SEED_PATH = Path("benchmarks/llm_error_bench_v1/llm_error_bench_v1.jsonl")


def test_seed_cases_from_llm_error_bench_v1_are_loadable() -> None:
    cases = load_seed_cases(SEED_PATH)

    assert len(cases) == 2500
    assert all(isinstance(case, TestCase) for case in cases)
    assert {"power_grid", "non_power"}.issubset(
        {case.metadata["domain_group"] for case in cases}
    )
    assert {
        "multiple_choice",
        "true_false",
        "correction",
        "scenario_decision",
        "error_identification",
        "direct_qa",
    }.issubset({case.metadata["task_type"] for case in cases})


def test_generator_emits_complete_schema_for_qa_and_agent_cases() -> None:
    cases = generate_candidate_cases(batch_size=16, iteration=2, seed_path=SEED_PATH)

    assert len(cases) == 16
    assert {case["metadata"]["scenario_kind"] for case in cases} == {"qa", "agent"}
    assert all(validate_case_schema(case) == [] for case in cases)
    assert any("电网" in case["input"] or "停电" in case["input"] for case in cases)
    assert any(case["metadata"]["domain_group"] == "non_power" for case in cases)


def test_agent_cases_are_afw_compatible() -> None:
    agent_case = next(
        case
        for case in generate_candidate_cases(batch_size=12, iteration=1, seed_path=SEED_PATH)
        if case["metadata"]["scenario_kind"] == "agent"
    )
    metadata = agent_case["metadata"]

    assert metadata["agent_failure_type"] in {
        "rag_retrieval_error",
        "rag_evidence_pollution",
        "tool_wrong_parameter",
        "skill_misuse",
        "memory_misuse",
        "approval_scope_expansion",
        "prior_step_as_authorization",
        "authority_conflict_power_dispatch",
        "multi_source_conflict",
        "counter_authority_ignored",
        "plan_step_order_error",
    }
    assert isinstance(metadata["agent_trace_events"], list)
    assert metadata["agent_trace_events"]
    assert isinstance(metadata["candidate_action"], dict)
    assert metadata["candidate_action"]["requires_human_approval"] is False
    assert metadata["afw_oracle"]["expected_gate_decision"] in {"allow", "block"}
    assert metadata["action_invariance_oracle"]["unauthorized_fields"]

    TestCase.model_validate(agent_case)


def test_agent_generation_scales_with_source_anchored_variants() -> None:
    cases = generate_candidate_cases(batch_size=100, iteration=9, seed_path=SEED_PATH)
    agent_cases = [case for case in cases if case["metadata"]["scenario_kind"] == "agent"]

    assert len(agent_cases) == 50
    assert len({case_fingerprint(case) for case in agent_cases}) == 50
    assert all(case["metadata"]["source_ref"]["url"].startswith("https://") for case in agent_cases)
    assert all("operational_context" in case["metadata"] for case in agent_cases)
    assert {"power_grid", "non_power"}.issubset(
        {case["metadata"]["domain_group"] for case in agent_cases}
    )


def test_agent_case_runs_through_afw_runtime_gate_and_evaluator() -> None:
    agent_case = next(
        case
        for case in generate_candidate_cases(batch_size=12, iteration=1, seed_path=SEED_PATH)
        if case["metadata"]["scenario_kind"] == "agent"
    )
    state = FormalTrustState(run_id="continuous-afw", case=TestCase.model_validate(agent_case))

    gate_patch = afw_capguard_node(state, {"runtime_final_action_mode": "fieldwise_repair"})
    gated_state = state.model_copy(update={"metrics": {**state.metrics, **gate_patch["metrics"]}})
    eval_patch = afw_runtime_evaluator_node(gated_state, {})

    assert gate_patch["metrics"]["afw_gate_decision"] == "block"
    assert gate_patch["metrics"]["final_action"]["decision"] == "fieldwise_repaired"
    assert eval_patch["evaluation"].passed is True


def test_deduplication_rejects_duplicate_fingerprints() -> None:
    base = generate_candidate_cases(batch_size=2, iteration=4, seed_path=SEED_PATH)[0]
    duplicate = json.loads(json.dumps(base, ensure_ascii=False))
    duplicate["id"] = f"{base['id']}-copy"

    unique, rejected = deduplicate_candidates([base, duplicate], existing_fingerprints=set())

    assert len(unique) == 1
    assert len(rejected) == 1
    assert rejected[0]["rejected_reason"] == "duplicate_candidate"
    assert case_fingerprint(base) == case_fingerprint(duplicate)


def test_unique_candidate_generation_tops_up_after_existing_duplicates() -> None:
    first_batch = generate_candidate_cases(batch_size=20, iteration=12, seed_path=SEED_PATH)
    existing = {case_fingerprint(case) for case in first_batch[:8]}

    unique, invalid, duplicate, generated = _generate_unique_valid_candidates(
        batch_size=20,
        iteration=12,
        seed_path=SEED_PATH,
        existing_fingerprints=existing,
    )

    assert len(unique) == 20
    assert invalid == []
    assert duplicate
    assert generated > 20
    assert len({case_fingerprint(case) for case in unique}) == 20


def test_jsonl_pools_are_append_only(tmp_path: Path) -> None:
    path = tmp_path / "accepted_bench.jsonl"
    append_jsonl_records(path, [{"id": "a"}])
    append_jsonl_records(path, [{"id": "b"}])

    assert [record["id"] for record in load_jsonl_records(path)] == ["a", "b"]


def test_ollama_runner_uses_mock_transport_and_preserves_raw_output() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode("utf-8"))
        assert payload["model"] == "qwen2.5:7b"
        assert payload["format"] == "json"
        return httpx.Response(
            200,
            json={
                "response": json.dumps(
                    {
                        "answer": "C",
                        "final_decision": "block",
                        "requires_human_approval": True,
                    }
                )
            },
        )

    case = generate_candidate_cases(batch_size=1, iteration=5, seed_path=SEED_PATH)[0]
    runner = OllamaModelRunner(model="qwen2.5:7b", transport=httpx.MockTransport(handler))

    result = runner.evaluate_case(case)

    assert result["ok"] is True
    assert result["model"] == "qwen2.5:7b"
    assert result["model_raw_output"]
    assert result["model_parsed_output"]["final_decision"] == "block"


def test_run_continuous_bench_appends_evaluated_accepted_rejected_and_summary(
    tmp_path: Path,
) -> None:
    responses = iter(
        [
            {"response": '{"answer":"unsafe direct execution","final_decision":"allow"}'},
            {"response": "not json but I would directly execute without approval"},
            {"response": '{"answer":"C","selected_option":"C","final_decision":"block"}'},
            {"response": '{"answer":"needs human approval","final_decision":"block"}'},
        ]
        * 4
    )

    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=next(responses))

    result = run_continuous_bench(
        batch_size=4,
        iterations=1,
        model="qwen2.5:7b",
        output_dir=tmp_path,
        seed_path=SEED_PATH,
        transport=httpx.MockTransport(handler),
    )
    run_continuous_bench(
        batch_size=4,
        iterations=1,
        model="qwen2.5:7b",
        output_dir=tmp_path,
        seed_path=SEED_PATH,
        transport=httpx.MockTransport(handler),
    )

    accepted = load_jsonl_records(tmp_path / "accepted_bench.jsonl")
    mixed_bench = load_jsonl_records(tmp_path / "mixed_bench.jsonl")
    evaluated = load_jsonl_records(tmp_path / "evaluated_pool.jsonl")
    rejected = load_jsonl_records(tmp_path / "rejected_pool.jsonl")
    summary = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))

    assert result["generated"] == 4
    assert result["evaluated"] == 4
    assert result["bench"] == 4
    assert len(evaluated) == 8
    assert len(mixed_bench) == 8
    assert accepted
    assert rejected
    assert all("model_raw_output" in record for record in evaluated)
    assert {record["model_answer_label"] for record in mixed_bench} <= {"correct", "incorrect"}
    assert all(record["bench_reason"] for record in mixed_bench)
    assert all(
        ("accepted_reason" in record) or ("rejected_reason" in record)
        for record in [*accepted, *rejected]
    )
    assert summary["totals"]["bench"] == 8
    assert summary["totals"]["evaluated"] == 8
    assert 0.0 <= summary["latest_run"]["model_pass_rate"] <= 1.0
    assert summary["bench_label_distribution"]
    assert 0.0 <= summary["latest_run"]["model_error_rate"] <= 1.0
    assert summary["failure_mode_distribution"]
