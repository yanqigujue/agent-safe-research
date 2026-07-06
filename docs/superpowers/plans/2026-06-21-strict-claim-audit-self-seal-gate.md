# Strict Claim Audit Self-Seal Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `eair-audit-reportable-claims --require-reviewed` reject reviewed manifests whose `review_manifest_payload_sha256` self-seal is missing or mismatched.

**Architecture:** Add self-seal validation inside `audit_reportable_claim_citations` only for strict reviewed audits. Keep default diagnostic audits unchanged. Record the expected/actual self-seal fields in the audit payload and Markdown so downstream seal artifacts expose the integrity status.

**Tech Stack:** Python, Typer CLI, pytest, existing EAIR reportable claim artifacts.

---

### Task 1: Red Strict-Audit Test

**Files:**
- Modify: `tests/test_mvp.py`

- [x] **Step 1: Add failing test**

Add a test near the reportable-claim review tests:

```python
def test_eair_audit_reportable_claims_require_reviewed_rejects_self_seal_mismatch(tmp_path: Path) -> None:
    # Create template claims.
    # Run diagnostic citation audit.
    # Record reviewed manifest.
    # Mutate only reviewed claim text.
    # Run eair-audit-reportable-claims --require-reviewed.
    # Assert exit 2, mismatch error, and audit JSON review_manifest_payload_sha256_matches=false.
```

- [x] **Step 2: Run red test**

Run:

```powershell
pytest tests/test_mvp.py::test_eair_audit_reportable_claims_require_reviewed_rejects_self_seal_mismatch -q
```

Expected: FAIL because strict claim audit currently accepts the mutated reviewed manifest.

### Task 2: Implementation

**Files:**
- Modify: `formaltrust_platform/experiments/eair_bench.py`

- [x] **Step 1: Add validation in `audit_reportable_claim_citations`**

When `require_reviewed` and `human_reviewed` are true:

```python
expected = str(payload.get("review_manifest_payload_sha256") or "")
actual = _hash_canonical_payload(payload)
matches = bool(expected and actual == expected)
if not expected:
    errors.append("reviewed claims missing review_manifest_payload_sha256")
elif not matches:
    errors.append("review_manifest_payload_sha256 mismatch")
```

- [x] **Step 2: Add audit fields**

Add these fields to the audit payload:

```text
expected_review_manifest_payload_sha256
actual_review_manifest_payload_sha256
review_manifest_payload_sha256_matches
```

- [x] **Step 3: Add Markdown row**

Render `review_manifest_payload_sha256_matches`.

- [x] **Step 4: Run green test**

Run:

```powershell
pytest tests/test_mvp.py::test_eair_audit_reportable_claims_require_reviewed_rejects_self_seal_mismatch -q
```

Expected: PASS.

### Task 3: Fixture and Docs

**Files:**
- Modify generated strict fixture under `outputs/eair_warrant_reportable_export/`
- Modify docs/logs.

- [x] **Step 1: Refresh strict claim audit, seal, and verification**

Run:

```powershell
python -m formaltrust_platform eair-audit-reportable-claims --claims outputs/eair_warrant_reportable_export/paper_ready_claims.json --output-dir outputs/eair_warrant_reportable_export/paper_ready_claim_audit --require-reviewed
python -m formaltrust_platform eair-seal-reportable-claim-bundle --claims outputs/eair_warrant_reportable_export/paper_ready_claims.json --claim-audit outputs/eair_warrant_reportable_export/paper_ready_claim_audit/reportable_claim_citation_audit.json --output-dir outputs/eair_warrant_reportable_export/paper_ready_claim_bundle_seal --require-reviewed
python -m formaltrust_platform eair-verify-reportable-claim-bundle-seal --seal outputs/eair_warrant_reportable_export/paper_ready_claim_bundle_seal/reportable_claim_bundle_seal.json --output-dir outputs/eair_warrant_reportable_export/paper_ready_claim_bundle_seal/verification --require-reviewed
```

- [x] **Step 2: Update docs/logs**

Document that strict claim audit now enforces reviewed-manifest self-seal.

- [x] **Step 3: Run focused tests**

Run:

```powershell
pytest tests/test_mvp.py -k "live_runbook or claim_template or reportable_claims or claim_bundle or claim_bundle_seal or reportable_export or reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence" -q
```

- [x] **Step 4: Run full tests**

Run:

```powershell
pytest -q
```
