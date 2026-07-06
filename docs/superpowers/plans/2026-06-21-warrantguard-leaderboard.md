# WarrantGuard Leaderboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add sorted WarrantGuard leaderboard artifacts for artifact summaries and reportable exports.

**Architecture:** Reuse existing `by_model_condition` metrics and reportable model-condition rows. Add one leaderboard row builder, one CSV/Markdown/JSON writer, and call them from existing artifact-summary and reportable-export output functions.

**Tech Stack:** Python, Typer CLI through existing commands, pytest, CSV/JSON/Markdown artifact writers.

---

### Task 1: Artifact Summary Leaderboard

**Files:**
- Modify: `tests/test_mvp.py`
- Modify: `formaltrust_platform/experiments/eair_bench.py`

- [ ] **Step 1: Write the failing artifact-summary test**

Add assertions in `test_eair_artifact_summary_aggregates_warrant_taxonomy`:

```python
leaderboard = payload["warrant_leaderboard"]
assert leaderboard[0]["rank"] == 1
assert leaderboard[0]["condition"] == "approval_bypass::clean_sufficient_evidence"
assert leaderboard[0]["warrant_quality_score"] == 1.0
assert leaderboard[-1]["condition"] == condition_key
assert leaderboard[-1]["warrant_quality_score"] == 0.0
assert (summary_dir / "artifact_summary_warrant_leaderboard.json").exists()
assert "warrant_quality_score" in (summary_dir / "artifact_summary_warrant_leaderboard.csv").read_text(encoding="utf-8")
assert "WarrantGuard Leaderboard" in (summary_dir / "artifact_summary_warrant_leaderboard.md").read_text(encoding="utf-8")
```

- [ ] **Step 2: Run the failing test**

Run:

```bash
pytest tests/test_mvp.py::test_eair_artifact_summary_aggregates_warrant_taxonomy -q
```

Expected: fail with `KeyError: 'warrant_leaderboard'`.

- [ ] **Step 3: Implement minimal artifact-summary leaderboard**

Add `_warrant_leaderboard_rows_from_model_conditions`, `_write_warrant_leaderboard_outputs`, and call them from `summarize_replay_artifact_manifests` and `_write_replay_artifact_summary_outputs`.

- [ ] **Step 4: Run the artifact-summary test**

Run:

```bash
pytest tests/test_mvp.py::test_eair_artifact_summary_aggregates_warrant_taxonomy -q
```

Expected: pass.

### Task 2: Reportable Export Leaderboard

**Files:**
- Modify: `tests/test_mvp.py`
- Modify: `formaltrust_platform/experiments/eair_bench.py`

- [ ] **Step 1: Write the failing reportable-export test**

Add assertions in `test_eair_export_reportable_results_includes_warrant_taxonomy_columns`:

```python
assert export_json["warrant_leaderboard"][0]["rank"] == 1
assert export_json["warrant_leaderboard"][0]["warrant_quality_score"] == 0.0
assert (export_dir / "reportable_warrant_leaderboard.json").exists()
assert "warrant_quality_score" in (export_dir / "reportable_warrant_leaderboard.csv").read_text(encoding="utf-8")
assert "WarrantGuard Leaderboard" in (export_dir / "reportable_warrant_leaderboard.md").read_text(encoding="utf-8")
```

- [ ] **Step 2: Run the failing reportable-export test**

Run:

```bash
pytest tests/test_mvp.py::test_eair_export_reportable_results_includes_warrant_taxonomy_columns -q
```

Expected: fail with `KeyError: 'warrant_leaderboard'`.

- [ ] **Step 3: Implement minimal reportable leaderboard**

Build `warrant_leaderboard` from `by_model_condition` in `export_reportable_results` and write `reportable_warrant_leaderboard.*`.

- [ ] **Step 4: Run focused reportable-export test**

Run:

```bash
pytest tests/test_mvp.py::test_eair_export_reportable_results_includes_warrant_taxonomy_columns -q
```

Expected: pass.

### Task 3: Artifacts, Docs, Verification

**Files:**
- Modify: `PAPER_PLAN.md`
- Modify: `refine-logs/EXPERIMENT_RESULTS.md`
- Modify: `refine-logs/CLAIM_EVIDENCE_AUDIT.md`
- Modify: `refine-logs/FINAL_PROPOSAL.md`
- Modify: `refine-logs/EXPERIMENT_PLAN.md`
- Modify: `docs/rag_agent_research_directions.md`
- Modify: `task_plan.md`
- Modify: `progress.md`
- Create: `refine-logs/iterations/ITERATION_054.md`

- [ ] **Step 1: Regenerate artifacts**

Run replay, summary, audit, and export commands for existing warrant fixtures.

- [ ] **Step 2: Read back leaderboard fields**

Use Python to confirm leaderboard files exist and ranks/quality scores are readable.

- [ ] **Step 3: Run full tests**

Run:

```bash
pytest -q
```

Expected: all tests pass.

- [ ] **Step 4: Update docs**

Record Iteration 054 as a reporting-layer leaderboard, not a new safety claim.
