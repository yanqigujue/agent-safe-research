# Reportable Claim Paper-Ready Verification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let reviewers verify that a sealed claim packet is paper-ready, not merely hash-consistent.

**Architecture:** Extend `verify_reportable_claim_bundle_seal` with `require_reviewed=False`. Default mode keeps existing hash verification. Strict mode checks review fields in the seal payload and records those fields in the verification artifact.

**Tech Stack:** Python, Typer CLI, pytest, existing EAIR claim bundle seal verifier.

---

### Task 1: Red Test

**Files:**
- Modify: `tests/test_mvp.py`

- [ ] **Step 1: Write the failing test**

Add `test_eair_verify_reportable_claim_bundle_seal_require_reviewed_rejects_diagnostic_seal`. The test should create a valid seal payload with correct hashes but `require_reviewed=false`, `human_reviewed=false`, `review_status="unreviewed"`. Default verification should pass. Verification with `--require-reviewed` should exit 2 and write a verification JSON with `passed=false`. Then change the seal to `require_reviewed=true`, `human_reviewed=true`, `review_status="reviewed"`, recompute `seal_payload_sha256`, and verify strict mode passes.

- [ ] **Step 2: Run red test**

Run: `pytest tests/test_mvp.py::test_eair_verify_reportable_claim_bundle_seal_require_reviewed_rejects_diagnostic_seal -q`

Expected: FAIL because `eair-verify-reportable-claim-bundle-seal` does not accept `--require-reviewed`.

### Task 2: Implementation

**Files:**
- Modify: `formaltrust_platform/experiments/eair_bench.py`
- Modify: `formaltrust_platform/cli.py`

- [ ] **Step 1: Add library flag**

Change `verify_reportable_claim_bundle_seal` to accept `require_reviewed: bool = False`.

- [ ] **Step 2: Add strict verification checks**

If `require_reviewed` is true, require:

```python
seal_payload.get("require_reviewed") is True
seal_payload.get("human_reviewed") is True
seal_payload.get("review_status") == "reviewed"
```

- [ ] **Step 3: Record review fields**

Add `require_reviewed`, `human_reviewed`, and `review_status` to the verification JSON/Markdown.

- [ ] **Step 4: Add CLI option**

Add `--require-reviewed` to `eair-verify-reportable-claim-bundle-seal` and pass it to `verify_reportable_claim_bundle_seal`.

- [ ] **Step 5: Run green test**

Run: `pytest tests/test_mvp.py::test_eair_verify_reportable_claim_bundle_seal_require_reviewed_rejects_diagnostic_seal -q`

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
- Create: `refine-logs/iterations/ITERATION_079.md`

- [ ] **Step 1: Refresh default fixture verification**

Rerun default seal verification so diagnostic artifacts include review status fields.

- [ ] **Step 2: Document strict verification**

State that default verification checks integrity and `--require-reviewed` checks paper-ready review status.

- [ ] **Step 3: Run focused tests**

Run: `pytest tests/test_mvp.py -k "claim_template or reportable_claims or claim_bundle or claim_bundle_seal or reportable_export or reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence" -q`

- [ ] **Step 4: Run full tests**

Run: `pytest -q`
