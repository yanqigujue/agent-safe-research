# Reportable Claim Review Verification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a reviewer-facing verifier for `paper_ready_claims.json` source claim/audit provenance.

**Architecture:** Implement `verify_reportable_claim_review_declaration` in `formaltrust_platform/experiments/eair_bench.py`, expose it as a Typer command, and add it to the generated live runbook between review declaration and strict claim audit. The verifier writes JSON/Markdown diagnostics before raising on failure, matching the existing artifact-audit pattern.

**Tech Stack:** Python, Typer CLI, pytest, existing EAIR reportable claim artifacts.

---

### Task 1: Red Verifier Test

**Files:**
- Modify: `tests/test_mvp.py`

- [x] **Step 1: Add a failing verifier test**

Add a test near `test_eair_record_reportable_claim_review_requires_passing_audit`:

```python
def test_eair_verify_reportable_claim_review_detects_source_audit_drift(tmp_path: Path) -> None:
    # Build a template claim, run citation audit, record review declaration.
    # Verify the declaration passes.
    # Mutate the source audit after review declaration.
    # Verify the declaration fails and writes source_claim_audit_sha256_matches=false.
```

Use real CLI commands:

```text
eair-audit-reportable-claims
eair-record-reportable-claim-review
eair-verify-reportable-claim-review
```

- [x] **Step 2: Run red test**

Run:

```powershell
pytest tests/test_mvp.py::test_eair_verify_reportable_claim_review_detects_source_audit_drift -q
```

Expected: FAIL because `eair-verify-reportable-claim-review` does not exist.

### Task 2: Implement Verifier

**Files:**
- Modify: `formaltrust_platform/experiments/eair_bench.py`
- Modify: `formaltrust_platform/cli.py`

- [x] **Step 1: Add `verify_reportable_claim_review_declaration`**

Implementation requirements:

- read reviewed claims JSON;
- compute reviewed claims SHA256;
- check `artifact_type`, `human_reviewed`, and `review_status`;
- load source claims and source audit paths from the reviewed manifest;
- compare source file hashes to `source_claims_sha256` and `source_claim_audit_sha256`;
- validate source audit type, pass status, errors, failed count, and `claims_path`;
- write JSON/Markdown when `output_dir` is supplied;
- raise `ValueError` after writing diagnostics if any checks fail.

- [x] **Step 2: Add CLI command**

Expose:

```text
formaltrust eair-verify-reportable-claim-review --claims paper_ready_claims.json --output-dir paper_ready_claim_review_verification
```

- [x] **Step 3: Run green verifier test**

Run:

```powershell
pytest tests/test_mvp.py::test_eair_verify_reportable_claim_review_detects_source_audit_drift -q
```

Expected: PASS.

### Task 3: Runbook Integration

**Files:**
- Modify: `tests/test_mvp.py`
- Modify: `formaltrust_platform/experiments/eair_bench.py`

- [x] **Step 1: Update runbook test**

Require command:

```text
paper_ready_claim_review_verification
```

Require artifacts:

```text
paper_ready_claim_review_verification/reportable_claim_review_verification.json
paper_ready_claim_review_verification/reportable_claim_review_verification.md
```

- [x] **Step 2: Run red runbook test**

Run:

```powershell
pytest tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar -q
```

Expected: FAIL because the verification command is not in the runbook.

- [x] **Step 3: Add runbook command and artifacts**

Insert the verifier after `paper_ready_claim_review_declaration` and before `paper_ready_claim_citation_audit`.

- [x] **Step 4: Run green runbook test**

Run:

```powershell
pytest tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar -q
```

Expected: PASS.

### Task 4: Fixtures, Docs, Verification

**Files:**
- Modify generated outputs under `outputs/eair_warrant_reportable_export/`
- Modify generated live runbook outputs
- Modify docs/logs.

- [x] **Step 1: Refresh fixture verification**

Run:

```powershell
python -m formaltrust_platform eair-verify-reportable-claim-review --claims outputs/eair_warrant_reportable_export/paper_ready_claims.json --output-dir outputs/eair_warrant_reportable_export/paper_ready_claim_review_verification
```

- [x] **Step 2: Regenerate live runbook**

Run:

```powershell
python -m formaltrust_platform eair-write-live-runbook --config examples/eair_prompt_protocol_matrix_live_template.yaml --output outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.md
```

- [x] **Step 3: Update docs/logs**

Document that review declaration provenance now has a reviewer-facing verifier.

- [x] **Step 4: Run focused tests**

Run:

```powershell
pytest tests/test_mvp.py -k "live_runbook or claim_template or reportable_claims or claim_bundle or claim_bundle_seal or reportable_export or reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence" -q
```

- [x] **Step 5: Run full tests**

Run:

```powershell
pytest -q
```
