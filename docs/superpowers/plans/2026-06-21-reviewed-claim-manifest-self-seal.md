# Reviewed Claim Manifest Self-Seal Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a self-seal hash to `paper_ready_claims.json` and make review verification detect post-declaration edits to the reviewed manifest itself.

**Architecture:** Extend the existing canonical payload hashing helper to ignore both `seal_payload_sha256` and `review_manifest_payload_sha256`. Add `review_manifest_payload_sha256` when recording a review declaration, then make `verify_reportable_claim_review_declaration` recompute and validate it.

**Tech Stack:** Python, Typer CLI, pytest, existing EAIR reportable claim artifacts.

---

### Task 1: Red Self-Seal Tests

**Files:**
- Modify: `tests/test_mvp.py`

- [x] **Step 1: Update the review declaration test**

Require `review_manifest_payload_sha256` to exist and be a 64-character hex string in `test_eair_record_reportable_claim_review_requires_passing_audit`.

- [x] **Step 2: Add a tamper regression**

Add a test near the review verifier test:

```python
def test_eair_verify_reportable_claim_review_detects_reviewed_manifest_drift(tmp_path: Path) -> None:
    # Create a reviewed manifest through the CLI.
    # Verify it passes.
    # Mutate paper_ready_claims.json itself, leaving source claim/audit unchanged.
    # Verify eair-verify-reportable-claim-review fails and writes
    # review_manifest_payload_sha256_matches=false.
```

- [x] **Step 3: Run red tests**

Run:

```powershell
pytest tests/test_mvp.py::test_eair_record_reportable_claim_review_requires_passing_audit tests/test_mvp.py::test_eair_verify_reportable_claim_review_detects_reviewed_manifest_drift -q
```

Expected: FAIL because `review_manifest_payload_sha256` is not written or verified.

### Task 2: Implementation

**Files:**
- Modify: `formaltrust_platform/experiments/eair_bench.py`

- [x] **Step 1: Update canonical hash helper**

Change `_hash_canonical_payload` so it excludes:

```python
{"seal_payload_sha256", "review_manifest_payload_sha256"}
```

- [x] **Step 2: Add self-seal when recording review**

In `record_reportable_claim_review`, after constructing `reviewed_payload`, set:

```python
reviewed_payload["review_manifest_payload_sha256"] = _hash_canonical_payload(reviewed_payload)
```

- [x] **Step 3: Verify self-seal**

In `verify_reportable_claim_review_declaration`, compute:

```python
expected_review_manifest_payload_sha256 = reviewed_payload.get("review_manifest_payload_sha256", "")
actual_review_manifest_payload_sha256 = _hash_canonical_payload(reviewed_payload)
```

Record expected, actual, and match fields. Fail if missing or mismatched.

- [x] **Step 4: Update Markdown**

Render `review_manifest_payload_sha256_matches`.

- [x] **Step 5: Run green tests**

Run:

```powershell
pytest tests/test_mvp.py::test_eair_record_reportable_claim_review_requires_passing_audit tests/test_mvp.py::test_eair_verify_reportable_claim_review_detects_reviewed_manifest_drift -q
```

Expected: PASS.

### Task 3: Fixture and Docs

**Files:**
- Modify generated fixture under `outputs/eair_warrant_reportable_export/`
- Modify docs/logs.

- [x] **Step 1: Regenerate reviewed claim fixture**

Run:

```powershell
python -m formaltrust_platform eair-record-reportable-claim-review --claims outputs/eair_warrant_reportable_export/reportable_claims.json --claim-audit outputs/eair_warrant_reportable_export/claim_audit/reportable_claim_citation_audit.json --reviewer paper-author --review-note "Reviewed claim text and cited artifact values." --reviewed-at-utc 2026-06-21T00:00:00Z --output outputs/eair_warrant_reportable_export/paper_ready_claims.json --force
```

- [x] **Step 2: Rerun review verification and strict packet chain**

Run the review verifier, strict claim audit, strict seal, and strict seal verification.

- [x] **Step 3: Update docs/logs**

Document the self-seal and fixture readback.

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
