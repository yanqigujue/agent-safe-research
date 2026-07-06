# Warrant Taxonomy Summary Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Aggregate WarrantGuard replay failures by stable taxonomy category across manifests, models, conditions, and model-condition pairs.

**Architecture:** Add a pure taxonomy helper in `formaltrust_platform/experiments/eair_bench.py`, attach categories to replay rows, and extend artifact summary aggregators/writers to carry warrant counts.

**Tech Stack:** Python dictionaries, CSV/JSON/Markdown writers, pytest, existing FormalTrust CLI tests.

---

### Task 1: Warrant Category Taxonomy

**Files:**
- Modify: `tests/test_eair_bench.py`
- Modify: `formaltrust_platform/experiments/eair_bench.py`

- [ ] **Step 1: Write failing replay-row test**

Extend the model-supplied warrant replay test to assert:

```python
assert by_id["t-warrant-fail"]["warrant_error_categories"] == ["decision_support"]
assert summary["warrant_error_category_counts"] == {"decision_support": 1}
```

- [ ] **Step 2: Run red test**

Run:

```powershell
pytest tests/test_eair_bench.py::test_structured_action_transcript_replay_verifies_model_supplied_warrants -q
```

Expected: FAIL because categories are missing.

- [ ] **Step 3: Implement taxonomy helper**

Add `warrant_error_category` and `warrant_error_category_counts`. Use stable categories from the design spec.

- [ ] **Step 4: Run green test**

Run:

```powershell
pytest tests/test_eair_bench.py::test_structured_action_transcript_replay_verifies_model_supplied_warrants -q
```

Expected: PASS.

### Task 2: Artifact Summary Aggregation

**Files:**
- Modify: `tests/test_mvp.py`
- Modify: `formaltrust_platform/experiments/eair_bench.py`

- [ ] **Step 1: Write failing CLI summary test**

Add a replay manifest with a failing model-supplied warrant and assert artifact summary JSON/CSV/Markdown expose:

```python
payload["warrant_present_count"] == 2
payload["warrant_failed_count"] == 1
payload["warrant_error_category_counts"] == {"decision_support": 1}
payload["by_model_condition"]["warrant-fixture"]["policy_update::near_duplicate_single_source_policy_support"]["warrant_error_category_counts"] == {"decision_support": 1}
```

- [ ] **Step 2: Run red test**

Run:

```powershell
pytest tests/test_mvp.py::test_eair_artifact_summary_aggregates_warrant_taxonomy -q
```

Expected: FAIL because artifact summary does not aggregate warrant fields.

- [ ] **Step 3: Extend group accumulator and writers**

Add warrant counts to `_empty_replay_transcript_group`, `_update_replay_transcript_group`, `_finalize_replay_transcript_groups`, CSV writers, and Markdown renderers.

- [ ] **Step 4: Run green test**

Run:

```powershell
pytest tests/test_mvp.py::test_eair_artifact_summary_aggregates_warrant_taxonomy -q
```

Expected: PASS.

### Task 3: Regenerate Artifacts And Logs

**Files:**
- Generated: `outputs/eair_transcript_replay_pilot/*`
- Generated: `outputs/eair_artifact_summary/*`
- Modify: `refine-logs/EXPERIMENT_RESULTS.md`
- Modify: `progress.md`
- Create: `refine-logs/iterations/ITERATION_050.md`

- [ ] **Step 1: Regenerate replay artifact**

Run replay over `examples/data/eair_structured_action_transcripts.jsonl`.

- [ ] **Step 2: Regenerate artifact summary**

Run artifact summary over existing replay manifests.

- [ ] **Step 3: Verify**

Run:

```powershell
pytest -q
```

Expected: all tests pass.

