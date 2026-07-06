# WarrantGuard Full Baseline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `warrantguard_full` as a first-class EAIR-Bench baseline with warrant diagnostics in raw results, summary tables, and reports.

**Architecture:** Extend the existing `formaltrust_platform.experiments.eair_bench` benchmark module in place. Keep WarrantGuard deterministic in this iteration by building warrants from existing candidate actions, then verify those warrants before applying the existing full EAIR gate behavior.

**Tech Stack:** Python dataclasses, pytest, existing EAIR-Bench synthetic pilot, Markdown/JSON/CSV report writers.

---

### Task 1: Register Baseline And Summary Contract

**Files:**
- Modify: `tests/test_eair_bench.py`
- Modify: `formaltrust_platform/experiments/eair_bench.py`

- [ ] **Step 1: Write the failing test**

Add:

```python
def test_warrantguard_full_baseline_records_warrant_diagnostics() -> None:
    clean = run_experiment([_sample("clean_sufficient_evidence")], ["warrantguard_full"])[0]
    insufficient = run_experiment(
        [_sample("near_duplicate_single_source_policy_support")], ["warrantguard_full"]
    )[0]

    assert "warrantguard_full" in BASELINES
    assert clean.gate_decision == "allow"
    assert clean.warrant_passed is True
    assert clean.warrant_error_count == 0
    assert clean.clean_utility_success is True

    assert insufficient.gate_decision == "block"
    assert insufficient.warrant_passed is False
    assert insufficient.warrant_error_count >= 1
    assert "decision_warrant_insufficient" in insufficient.warrant_errors
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```powershell
pytest tests/test_eair_bench.py::test_warrantguard_full_baseline_records_warrant_diagnostics -q
```

Expected: FAIL because `warrantguard_full` is unknown or the warrant fields do not exist.

- [ ] **Step 3: Implement minimal data fields**

Add `warrant_passed`, `warrant_error_count`, `warrant_warning_count`, `warrant_errors`, and `warrant_warnings` to `CaseResult`.

- [ ] **Step 4: Implement `apply_warrantguard_full`**

The function should build a warrant, verify it, block or replace on verification failure, and otherwise call `apply_eair_full`.

- [ ] **Step 5: Route `_run_one`**

Add `warrantguard_full` to `BASELINES` and dispatch it in `_run_one`.

- [ ] **Step 6: Run the focused test**

Run:

```powershell
pytest tests/test_eair_bench.py::test_warrantguard_full_baseline_records_warrant_diagnostics -q
```

Expected: PASS.

### Task 2: Report Warrant Metrics

**Files:**
- Modify: `tests/test_eair_bench.py`
- Modify: `formaltrust_platform/experiments/eair_bench.py`

- [ ] **Step 1: Write the failing report test**

Add assertions to `test_report_summarizes_closest_neighbor_baselines`:

```python
assert "warrantguard_full" in report
assert "warrant_failure_rate" in report
assert "WarrantGuard" in report
```

- [ ] **Step 2: Run the report test to verify it fails**

Run:

```powershell
pytest tests/test_eair_bench.py::test_report_summarizes_closest_neighbor_baselines -q
```

Expected: FAIL until report columns and key findings are updated.

- [ ] **Step 3: Extend `_aggregate` and `_render_report`**

Add `warrant_failure_rate` and `mean_warrant_error_count` to aggregate metrics and report tables.

- [ ] **Step 4: Run focused report test**

Run:

```powershell
pytest tests/test_eair_bench.py::test_report_summarizes_closest_neighbor_baselines -q
```

Expected: PASS.

### Task 3: Regenerate Pilot Artifacts

**Files:**
- Generated: `outputs/eair_bench_pilot/summary.json`
- Generated: `outputs/eair_bench_pilot/baseline_summary.csv`
- Generated: `outputs/eair_bench_pilot/case_results.json`
- Generated: `outputs/eair_bench_pilot/report.md`
- Modify: `refine-logs/EXPERIMENT_RESULTS.md`
- Modify: `progress.md`

- [ ] **Step 1: Run the deterministic pilot**

Run:

```powershell
@'
from pathlib import Path
from formaltrust_platform.experiments.eair_bench import BASELINES, build_benchmark, run_experiment

run_experiment(build_benchmark(), BASELINES, output_dir=Path("outputs/eair_bench_pilot"))
'@ | python -
```

Expected: output files are rewritten and include `warrantguard_full`.

- [ ] **Step 2: Record result interpretation**

Update experiment results and progress logs with the observed `warrantguard_full` metrics.

- [ ] **Step 3: Verify everything**

Run:

```powershell
pytest -q
```

Expected: all tests pass.
