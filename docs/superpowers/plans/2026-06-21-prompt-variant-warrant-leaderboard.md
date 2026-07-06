# Prompt-Variant WarrantGuard Leaderboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preserve prompt variants through replay and leaderboard reporting so proof-carrying prompt designs can be compared.

**Architecture:** Add optional `prompt_variant` to transcript loading and replay rows, aggregate prompt-variant groups in artifact summary, and update leaderboard rows/files to include the prompt variant dimension.

**Tech Stack:** Python, pytest, Typer CLI, JSONL replay fixtures, CSV/Markdown artifact writers.

---

### Task 1: Prompt Variant Replay and Summary

**Files:**
- Modify: `tests/test_mvp.py`
- Modify: `formaltrust_platform/experiments/eair_bench.py`

- [ ] **Step 1: Write failing test**

Create two transcript rows with the same model and condition but different `prompt_variant` values. Assert `prompt_variant_counts`, `by_model_prompt_condition`, and leaderboard order.

- [ ] **Step 2: Verify red**

Run:

```bash
pytest tests/test_mvp.py::test_eair_artifact_summary_leaderboard_distinguishes_prompt_variants -q
```

Expected failure:

```text
KeyError: 'prompt_variant_counts'
```

- [ ] **Step 3: Implement replay and aggregation**

Add `prompt_variant` to transcript loading, replay rows, replay manifest summaries, artifact aggregation, and leaderboard rows.

- [ ] **Step 4: Verify green**

Run the same test and expect `1 passed`.

### Task 2: Prompt Variant Matrix Artifacts

**Files:**
- Modify: `tests/test_mvp.py`
- Modify: `formaltrust_platform/experiments/eair_bench.py`

- [ ] **Step 1: Write failing file-output assertions**

Assert `artifact_summary_by_model_prompt_condition.csv/md` exist and include both prompt variants.

- [ ] **Step 2: Verify red**

Expected failure:

```text
FileNotFoundError: artifact_summary_by_model_prompt_condition.csv
```

- [ ] **Step 3: Implement file writers**

Write `artifact_summary_by_prompt_variant.csv/md` and `artifact_summary_by_model_prompt_condition.csv/md`.

- [ ] **Step 4: Verify green and subset**

Run:

```bash
pytest tests/test_mvp.py -k "artifact_summary or reportable_results or reportable_run_audit" -q
```

Expected: all selected tests pass.

### Task 3: Fixture, Artifacts, Docs

**Files:**
- Create: `examples/data/eair_prompt_variant_warrant_transcripts.jsonl`
- Modify: docs and refine logs

- [ ] **Step 1: Add deterministic prompt-variant fixture**

Add one proof-carrying transcript and one legacy action-only transcript for the same model and condition.

- [ ] **Step 2: Regenerate artifacts**

Run replay and artifact summary for the prompt-variant fixture.

- [ ] **Step 3: Read back outputs**

Confirm `proof_carrying` ranks above `legacy_action_only`.

- [ ] **Step 4: Full verification**

Run `pytest -q`.
