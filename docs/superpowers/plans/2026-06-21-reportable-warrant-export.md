# Reportable Warrant Export Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add WarrantGuard taxonomy columns to reportable model-condition export tables.

**Architecture:** Reuse existing `by_model_condition` warrant fields from artifact summaries and pass them through `_reportable_model_condition_rows`, CSV writer, and Markdown renderer.

**Tech Stack:** Python, Typer CLI tests, CSV/JSON/Markdown artifacts, pytest.

---

### Task 1: TDD Reportable Export Columns

**Files:**
- Modify: `tests/test_mvp.py`
- Modify: `formaltrust_platform/experiments/eair_bench.py`

- [ ] **Step 1: Write failing test**

Create `test_eair_export_reportable_results_includes_warrant_taxonomy_columns` with a live-marked `(action, warrant)` transcript whose warrant fails with `decision_support`.

- [ ] **Step 2: Run red test**

Run:

```powershell
pytest tests/test_mvp.py::test_eair_export_reportable_results_includes_warrant_taxonomy_columns -q
```

Expected: FAIL because exported rows do not include warrant fields.

- [ ] **Step 3: Implement export pass-through**

Add `warrant_present_count`, `warrant_failed_count`, and `warrant_error_category_counts_json` to `_reportable_model_condition_rows`, reportable CSV fields, and Markdown renderer.

- [ ] **Step 4: Run green test**

Run:

```powershell
pytest tests/test_mvp.py::test_eair_export_reportable_results_includes_warrant_taxonomy_columns -q
```

Expected: PASS.

### Task 2: Generate Reportable Warrant Export Artifact

**Files:**
- Generated: `outputs/eair_warrant_live_fixture_replay/*`
- Generated: `outputs/eair_warrant_live_fixture_summary/*`
- Generated: `outputs/eair_warrant_live_fixture_audit/*`
- Generated: `outputs/eair_warrant_reportable_export/*`

- [ ] **Step 1: Create live-marked fixture transcript**

Use a provider-style model name and `sampling_mode=live`.

- [ ] **Step 2: Replay, summarize, audit, export**

Run the full CLI chain.

- [ ] **Step 3: Verify**

Read back the export JSON/CSV/Markdown and run `pytest -q`.

