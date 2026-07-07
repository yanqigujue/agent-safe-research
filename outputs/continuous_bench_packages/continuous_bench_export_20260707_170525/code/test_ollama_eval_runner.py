from __future__ import annotations

import importlib.util
from pathlib import Path


MODULE_PATH = Path("benchmarks/llm_error_bench_v1/run_ollama_eval.py")


def _load_module():
    spec = importlib.util.spec_from_file_location("run_ollama_eval", MODULE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_extract_choice_prefers_explicit_option_marker() -> None:
    runner = _load_module()

    assert runner.extract_choice("我选择 C。因为需要先确认授权。") == "C"
    assert runner.extract_choice("Correct option: B") == "B"


def test_evaluate_exact_choice_uses_correct_option() -> None:
    runner = _load_module()
    row = {
        "id": "case-1",
        "metadata": {
            "task_type": "multiple_choice",
            "correct_option": "C",
            "evaluation": {"primary_metric": "exact_choice"},
        },
    }

    result = runner.evaluate_response(row, "答案是 C，不能直接执行。")

    assert result["passed"] is True
    assert result["predicted"] == "C"


def test_evaluate_safety_label_detects_unsafe_weak_answer_rejection() -> None:
    runner = _load_module()
    row = {
        "id": "case-2",
        "metadata": {
            "weak_answer_label": "incorrect",
            "evaluation": {"primary_metric": "safety_label"},
        },
    }

    result = runner.evaluate_response(row, "这个回答是错误的，不应绕过审批。")

    assert result["passed"] is True
    assert result["expected"] == "incorrect"


def test_build_summary_counts_completed_rows() -> None:
    runner = _load_module()
    records = [
        {
            "id": "a",
            "ok": True,
            "heuristic_eval": {"passed": True},
            "metadata": {"task_type": "direct_qa", "domain_group": "power_grid"},
        },
        {
            "id": "b",
            "ok": True,
            "heuristic_eval": {"passed": False},
            "metadata": {"task_type": "direct_qa", "domain_group": "non_power"},
        },
    ]

    summary = runner.build_summary(records, model="qwen2.5:7b")

    assert summary["model"] == "qwen2.5:7b"
    assert summary["completed_rows"] == 2
    assert summary["heuristic_passed"] == 1
    assert summary["task_type_counts"] == {"direct_qa": 2}


def test_config_for_json_serializes_path_values() -> None:
    runner = _load_module()
    config = runner.config_for_json({"dataset": Path("data.jsonl"), "model": "qwen"}, Path("out"))

    assert config["dataset"] == "data.jsonl"
    assert config["output_dir"] == "out"
