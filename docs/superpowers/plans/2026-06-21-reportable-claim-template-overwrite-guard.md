# Reportable Claim Template Overwrite Guard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prevent `eair-write-reportable-claim-template` from silently overwriting an existing human-reviewed `reportable_claims.json`.

**Architecture:** Keep the guard at the template writer boundary so both Python callers and CLI callers get the same protection. Expose one explicit CLI escape hatch, `--force`, for intentional regeneration.

**Tech Stack:** Python, Typer CLI, pytest, existing EAIR benchmark helpers.

---

### Task 1: Add Overwrite-Guard Test

**Files:**
- Modify: `tests/test_mvp.py`

- [ ] **Step 1: Write the failing test**

Add `test_eair_write_reportable_claim_template_refuses_existing_output_without_force` near the existing claim-template test. The test should create valid export and integrity audit inputs, pre-create `reportable_claims.json` with `human_reviewed`, run the CLI without `--force`, assert exit code 2 and unchanged content, then rerun with `--force` and assert `claim_generation == "template"`.

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_mvp.py::test_eair_write_reportable_claim_template_refuses_existing_output_without_force -q`

Expected: FAIL because the current command overwrites the file and exits 0.

### Task 2: Implement Guard

**Files:**
- Modify: `formaltrust_platform/experiments/eair_bench.py`
- Modify: `formaltrust_platform/cli.py`

- [ ] **Step 1: Add `force` to the Python function**

Change `write_reportable_claim_template` to accept `force: bool = False`. Before writing or loading artifacts, if `target.exists()` and `force` is false, raise `ValueError("reportable claim template output already exists: ...; pass --force to overwrite")`.

- [ ] **Step 2: Add CLI option**

Add `force: bool = typer.Option(False, "--force", help="Overwrite an existing reportable_claims.json.")` to `eair_write_reportable_claim_template_command`, and pass it into `write_reportable_claim_template`.

- [ ] **Step 3: Run test to verify it passes**

Run: `pytest tests/test_mvp.py::test_eair_write_reportable_claim_template_refuses_existing_output_without_force -q`

Expected: PASS.

### Task 3: Refresh Artifacts and Documentation

**Files:**
- Modify: `docs/eair_artifact_readme.md`
- Modify: `PAPER_PLAN.md`
- Modify: `docs/rag_agent_research_directions.md`
- Modify: `refine-logs/EXPERIMENT_RESULTS.md`
- Modify: `refine-logs/CLAIM_EVIDENCE_AUDIT.md`
- Modify: `refine-logs/FINAL_PROPOSAL.md`
- Modify: `refine-logs/EXPERIMENT_PLAN.md`
- Modify: `task_plan.md`
- Modify: `progress.md`
- Create: `refine-logs/iterations/ITERATION_076.md`

- [ ] **Step 1: Refresh fixture deliberately**

Run `eair-write-reportable-claim-template` on the fixture with `--force`, then rerun claim audit, bundle seal, and seal verification.

- [ ] **Step 2: Document the boundary**

Record that template generation refuses to overwrite existing claim manifests unless the caller passes `--force`.

### Task 4: Verify

**Files:**
- Test only

- [ ] **Step 1: Run focused tests**

Run: `pytest tests/test_mvp.py -k "claim_template or live_runbook or reportable_claims or claim_bundle or claim_bundle_seal or reportable_export or reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence" -q`

- [ ] **Step 2: Run full tests**

Run: `pytest -q`
