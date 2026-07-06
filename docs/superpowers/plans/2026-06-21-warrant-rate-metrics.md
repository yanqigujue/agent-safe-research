# Warrant Rate Metrics Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `warrant_present_rate`, `warrant_failure_rate`, and `warrant_valid_rate` to replay, artifact summary, and reportable export outputs.

**Architecture:** Reuse existing warrant count fields and compute rounded ratios with one shared helper. Thread the rates through summaries, group finalizers, CSV writers, Markdown tables, and reportable export rows.

**Tech Stack:** Python, JSON/CSV/Markdown artifact writers, pytest.

---

### Task 1: TDD Rate Contract

**Files:**
- Modify: `tests/test_eair_bench.py`
- Modify: `tests/test_mvp.py`
- Modify: `formaltrust_platform/experiments/eair_bench.py`

- [ ] **Step 1: Write failing assertions**

Assert replay, artifact summary, and reportable export outputs expose:

```python
assert summary["warrant_present_rate"] == 1.0
assert summary["warrant_failure_rate"] == 0.5
assert summary["warrant_valid_rate"] == 0.5
```

- [ ] **Step 2: Run red tests**

Run:

```powershell
pytest tests/test_eair_bench.py::test_structured_action_transcript_replay_verifies_model_supplied_warrants tests/test_mvp.py::test_eair_artifact_summary_aggregates_warrant_taxonomy tests/test_mvp.py::test_eair_export_reportable_results_includes_warrant_taxonomy_columns -q
```

Expected: FAIL because rate fields are missing.

- [ ] **Step 3: Implement rates**

Add `_ratio`, replay summary rates, artifact summary group rates, and reportable export rate columns.

- [ ] **Step 4: Run green tests**

Run the same command. Expected: PASS.

### Task 2: Refresh Artifacts

**Files:**
- Generated: `outputs/eair_transcript_replay_pilot/*`
- Generated: `outputs/eair_warrant_artifact_summary/*`
- Generated: `outputs/eair_warrant_reportable_export/*`

- [ ] **Step 1: Regenerate replay and summary artifacts**

Run replay, warrant artifact summary, and reportable export chain.

- [ ] **Step 2: Verify**

Run:

```powershell
pytest -q
```

Expected: all tests pass.

