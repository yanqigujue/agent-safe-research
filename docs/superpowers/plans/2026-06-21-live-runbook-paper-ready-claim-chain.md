# Live Runbook Paper-Ready Claim Chain Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the generated live prompt-protocol runbook include strict paper-ready claim audit, seal, and seal verification commands.

**Architecture:** Keep the existing diagnostic claim chain unchanged. Add a parallel strict chain in `write_live_runbook` that writes to separate `paper_ready_*` output directories and passes `--require-reviewed` to each strict command.

**Tech Stack:** Python, pytest, Typer CLI command strings, existing EAIR live runbook generator.

---

### Task 1: Red Test

**Files:**
- Modify: `tests/test_mvp.py`

- [x] **Step 1: Update runbook test**

Require these command names in `test_eair_write_live_runbook_includes_prompt_protocol_matrix_steps`:

```python
"paper_ready_claim_citation_audit",
"paper_ready_claim_bundle_seal",
"paper_ready_claim_bundle_seal_verification",
```

Assert each corresponding command contains `--require-reviewed`.

- [x] **Step 2: Run red test**

Run: `pytest tests/test_mvp.py::test_eair_write_live_runbook_includes_prompt_protocol_matrix_steps -q`

Expected: FAIL because the runbook has only the diagnostic claim chain.

### Task 2: Implementation

**Files:**
- Modify: `formaltrust_platform/experiments/eair_bench.py`

- [x] **Step 1: Add strict command strings**

Create strict command strings for:

```text
paper_ready_claim_citation_audit
paper_ready_claim_bundle_seal
paper_ready_claim_bundle_seal_verification
```

Use separate directories:

```text
paper_tables/paper_ready_claim_audit
paper_tables/paper_ready_claim_bundle_seal
paper_tables/paper_ready_claim_bundle_seal/verification
```

- [x] **Step 2: Add commands to runbook**

Append the strict commands after the default claim bundle seal verification command.

- [x] **Step 3: Add required artifacts**

Add JSON and Markdown outputs for the strict audit, strict seal, and strict verification directories.

- [x] **Step 4: Run green test**

Run: `pytest tests/test_mvp.py::test_eair_write_live_runbook_includes_prompt_protocol_matrix_steps -q`

Expected: PASS.

### Task 3: Artifacts, Docs, Verification

**Files:**
- Modify generated `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.md`
- Modify generated `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.json`
- Modify documentation and iteration logs.

- [x] **Step 1: Regenerate live runbook**

Run:

```powershell
python -m formaltrust_platform eair-write-live-runbook --config examples/eair_prompt_protocol_matrix_live_template.yaml --output outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.md
```

- [x] **Step 2: Update docs/logs**

Document that the runbook now contains both diagnostic and paper-ready claim chains.

- [x] **Step 3: Run focused tests**

Run:

```powershell
pytest tests/test_mvp.py -k "live_runbook or claim_template or reportable_claims or claim_bundle or claim_bundle_seal or reportable_export or reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence" -q
```

- [x] **Step 4: Run full tests**

Run: `pytest -q`
