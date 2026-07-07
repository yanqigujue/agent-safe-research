from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from formaltrust_platform.datasets import load_cases


BENCH_DIR = Path("benchmarks/llm_error_bench_v1")
DATASET_PATH = BENCH_DIR / "llm_error_bench_v1.jsonl"
SUMMARY_PATH = BENCH_DIR / "summary.json"
SCHEMA_PATH = BENCH_DIR / "schema.json"
SOURCES_PATH = BENCH_DIR / "sources.json"
README_PATH = BENCH_DIR / "README.md"


def _rows() -> list[dict]:
    return [
        json.loads(line)
        for line in DATASET_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def test_llm_error_bench_v1_artifacts_exist_and_are_loadable() -> None:
    assert DATASET_PATH.exists()
    assert SUMMARY_PATH.exists()
    assert SCHEMA_PATH.exists()
    assert SOURCES_PATH.exists()
    assert README_PATH.exists()

    cases = load_cases(DATASET_PATH)
    assert len(cases) == 2500


def test_llm_error_bench_v1_distribution_and_required_metadata() -> None:
    rows = _rows()
    assert len(rows) == 2500
    assert len({row["id"] for row in rows}) == 2500
    assert len({_normalize(row["input"]) for row in rows}) == 2500

    metadata = [row["metadata"] for row in rows]
    required_keys = {
        "benchmark_version",
        "domain_group",
        "domain",
        "subdomain",
        "language",
        "task_type",
        "source_type",
        "verification_status",
        "is_adversarial",
        "trap_type",
        "expected_model_failure",
        "risk_level",
        "difficulty",
        "correct_answer",
        "weak_model_answer",
        "weak_answer_label",
        "evaluation",
    }
    for item in metadata:
        assert required_keys.issubset(item)
        assert item["benchmark_version"] == "llm_error_bench_v1"
        assert item["weak_answer_label"] in {"correct", "incorrect"}
        assert item["evaluation"]["primary_metric"] in {"exact_choice", "safety_label", "rubric_match"}

    domain_counts = Counter(item["domain_group"] for item in metadata)
    assert domain_counts == {"power_grid": 2000, "non_power": 500}

    weak_answer_counts = Counter(item["weak_answer_label"] for item in metadata)
    assert weak_answer_counts["incorrect"] >= 2000
    assert weak_answer_counts["correct"] >= 250

    task_types = {item["task_type"] for item in metadata}
    assert {
        "direct_qa",
        "error_identification",
        "correction",
        "multiple_choice",
        "true_false",
        "scenario_decision",
    }.issubset(task_types)

    source_types = {item["source_type"] for item in metadata}
    assert {
        "official_standard_anchor",
        "public_incident_anchor",
        "public_dataset_anchor",
        "synthetic_manual",
    }.issubset(source_types)

    trap_types = {item["trap_type"] for item in metadata}
    assert {
        "safety_overconfidence",
        "missing_condition",
        "constraint_violation",
        "terminology_confusion",
        "false_premise",
        "negation_trap",
        "unsafe_correction",
    }.issubset(trap_types)


def test_llm_error_bench_v1_summary_matches_dataset() -> None:
    rows = _rows()
    summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
    metadata = [row["metadata"] for row in rows]

    assert summary["dataset_id"] == "llm_error_bench_v1"
    assert summary["total_rows"] == len(rows)
    assert summary["domain_group_counts"] == dict(Counter(item["domain_group"] for item in metadata))
    assert summary["weak_answer_label_counts"] == dict(
        Counter(item["weak_answer_label"] for item in metadata)
    )
    assert summary["task_type_counts"] == dict(Counter(item["task_type"] for item in metadata))


def _normalize(value: str) -> str:
    return " ".join(value.lower().split())
