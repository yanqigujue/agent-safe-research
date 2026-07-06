# Reportable Claim Review Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a strict paper-ready audit mode that rejects unreviewed template claim manifests.

**Architecture:** Extend `audit_reportable_claim_citations` with a `require_reviewed` flag. Keep normal claim value/hash checks unchanged; add a manifest-level review status to the audit payload and expose the flag through Typer.

**Tech Stack:** Python, Typer CLI, pytest, existing EAIR reportable claim audit helpers.

---

### Task 1: Red Test

**Files:**
- Modify: `tests/test_mvp.py`

- [ ] **Step 1: Write the failing test**

Add `test_eair_audit_reportable_claims_require_reviewed_rejects_template_manifest`. It should create one reportable artifact and one valid `eair_reportable_claims` manifest with `claim_generation="template"`. Invoke `eair-audit-reportable-claims --require-reviewed` and assert exit code 2, `review_status == "unreviewed"`, and an error mentioning `human-reviewed`. Then set `claim_generation="human_reviewed"` and `human_reviewed=true`, rerun the same command, and assert exit code 0 and `review_status == "reviewed"`.

- [ ] **Step 2: Run the red test**

Run: `pytest tests/test_mvp.py::test_eair_audit_reportable_claims_require_reviewed_rejects_template_manifest -q`

Expected: FAIL because `--require-reviewed` does not exist.

### Task 2: Implementation

**Files:**
- Modify: `formaltrust_platform/experiments/eair_bench.py`
- Modify: `formaltrust_platform/cli.py`

- [ ] **Step 1: Add library flag**

Change `audit_reportable_claim_citations` to accept `require_reviewed: bool = False`. Compute `review_status` from manifest fields:

```python
reviewed = payload.get("human_reviewed") is True or payload.get("claim_generation") == "human_reviewed"
review_status = "reviewed" if reviewed else "unreviewed"
```

When `require_reviewed` is true and `reviewed` is false, append an error that says the manifest must be human-reviewed.

- [ ] **Step 2: Add audit payload fields**

Add `require_reviewed`, `review_status`, and `human_reviewed` to the audit JSON/Markdown.

- [ ] **Step 3: Add CLI option**

Add `require_reviewed: bool = typer.Option(False, "--require-reviewed", help="Require a human-reviewed claim manifest.")` and pass it to `audit_reportable_claim_citations`.

- [ ] **Step 4: Run the green test**

Run: `pytest tests/test_mvp.py::test_eair_audit_reportable_claims_require_reviewed_rejects_template_manifest -q`

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
- Create: `refine-logs/iterations/ITERATION_077.md`

- [ ] **Step 1: Document the strict mode**

State that template manifests are initialization artifacts and `--require-reviewed` is the paper-ready audit gate.

- [ ] **Step 2: Run focused tests**

Run: `pytest tests/test_mvp.py -k "claim_template or reportable_claims or claim_bundle or claim_bundle_seal or reportable_export or reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence" -q`

- [ ] **Step 3: Run full tests**

Run: `pytest -q`
