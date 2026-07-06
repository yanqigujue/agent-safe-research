# Reportable Claim Paper-Ready Seal Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prevent a final paper-ready claim bundle seal from being created from an unreviewed claim audit.

**Architecture:** Extend `seal_reportable_claim_bundle` with `require_reviewed=False`. In strict mode, inspect the supplied claim audit's review fields and block unless it came from a reviewed strict audit. Record review status in the seal payload for reviewer-facing evidence.

**Tech Stack:** Python, Typer CLI, pytest, existing EAIR reportable claim bundle seal helpers.

---

### Task 1: Red Test

**Files:**
- Modify: `tests/test_mvp.py`

- [ ] **Step 1: Write the failing test**

Add `test_eair_seal_reportable_claim_bundle_require_reviewed_rejects_unreviewed_audit`. The test should create:

- a valid `eair_reportable_claims` manifest;
- a passing claim audit with `require_reviewed=false`, `human_reviewed=false`, `review_status="unreviewed"`;
- a strict seal CLI invocation with `--require-reviewed` that exits 2 and writes a blocked seal JSON;
- a reviewed claim audit with `require_reviewed=true`, `human_reviewed=true`, `review_status="reviewed"`;
- a strict seal CLI invocation that exits 0 and records `review_status="reviewed"`.

- [ ] **Step 2: Run red test**

Run: `pytest tests/test_mvp.py::test_eair_seal_reportable_claim_bundle_require_reviewed_rejects_unreviewed_audit -q`

Expected: FAIL because `eair-seal-reportable-claim-bundle` does not accept `--require-reviewed`.

### Task 2: Implementation

**Files:**
- Modify: `formaltrust_platform/experiments/eair_bench.py`
- Modify: `formaltrust_platform/cli.py`

- [ ] **Step 1: Add library flag**

Change `seal_reportable_claim_bundle` to accept `require_reviewed: bool = False`.

- [ ] **Step 2: Enforce strict seal gate**

If `require_reviewed` is true, require the claim audit to have:

```python
claim_audit.get("require_reviewed") is True
claim_audit.get("human_reviewed") is True
claim_audit.get("review_status") == "reviewed"
```

Append concise errors if those checks fail.

- [ ] **Step 3: Record review fields in seal payload**

Add `require_reviewed`, `human_reviewed`, and `review_status` to the seal payload.

- [ ] **Step 4: Add CLI option**

Add `--require-reviewed` to `eair-seal-reportable-claim-bundle` and pass it to `seal_reportable_claim_bundle`.

- [ ] **Step 5: Run green test**

Run: `pytest tests/test_mvp.py::test_eair_seal_reportable_claim_bundle_require_reviewed_rejects_unreviewed_audit -q`

Expected: PASS.

### Task 3: Docs And Verification

**Files:**
- Modify: `docs/eair_artifact_readme.md`
- Modify: `PAPER_PLAN.md`
- Modify: `docs/rag_agent_research_directions.md`
- Modify: `refine-logs/EXPERIMENT_PLAN.md`
- Modify: `refine-logs/EXPERIMENT_RESULTS.md`
- Modify: `refine-logs/CLAIM_EVIDENCE_AUDIT.md`
- Modify: `refine-logs/FINAL_PROPOSAL.md`
- Modify: `task_plan.md`
- Modify: `progress.md`
- Create: `refine-logs/iterations/ITERATION_078.md`

- [ ] **Step 1: Refresh default fixture seal**

Rerun default claim audit, seal, and seal verification for deterministic template-chain diagnostics.

- [ ] **Step 2: Document strict paper-ready sealing**

State that default sealing is diagnostic and `--require-reviewed` is the paper-ready submission-packet gate.

- [ ] **Step 3: Run focused tests**

Run: `pytest tests/test_mvp.py -k "claim_template or reportable_claims or claim_bundle or claim_bundle_seal or reportable_export or reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence" -q`

- [ ] **Step 4: Run full tests**

Run: `pytest -q`
