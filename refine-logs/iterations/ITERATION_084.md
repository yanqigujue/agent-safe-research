# Iteration 084: Strict Claim Audit Self-Seal Gate

## Goal

Make reviewed-manifest integrity mandatory for strict paper-ready claim audit.

## Changes

- `eair-audit-reportable-claims --require-reviewed` now checks `review_manifest_payload_sha256`.
- Strict claim audit records:
  - `expected_review_manifest_payload_sha256`
  - `actual_review_manifest_payload_sha256`
  - `review_manifest_payload_sha256_matches`
- Audit Markdown now renders `review_manifest_payload_sha256_matches`.
- Refreshed strict paper-ready audit, seal, and seal verification artifacts.

## TDD

Red check:

- `test_eair_audit_reportable_claims_require_reviewed_rejects_self_seal_mismatch` failed because strict audit accepted a tampered reviewed manifest.

Green check:

- The same test now passes. Strict audit fails with `review_manifest_payload_sha256 mismatch`, while the underlying claim value result still passes.

## Fixture Readback

```text
paper_ready_claim_audit:
  passed=true
  require_reviewed=true
  review_status=reviewed
  review_manifest_payload_sha256_matches=true
  claims=3/3

paper_ready_claim_bundle_seal:
  sealed=true
  require_reviewed=true
  review_status=reviewed
  seal_payload_sha256=c8643b61925d46d7cbbcab4eb75a16b9e922c716142d2003623320daad1eeca6

paper_ready_claim_bundle_seal_verification:
  passed=true
  require_reviewed=true
  review_status=reviewed
```

## Verification

```text
pytest tests/test_mvp.py::test_eair_audit_reportable_claims_require_reviewed_rejects_self_seal_mismatch -q
1 passed

pytest tests/test_mvp.py -k "live_runbook or claim_template or reportable_claims or claim_bundle or claim_bundle_seal or reportable_export or reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence" -q
24 passed, 29 deselected

pytest -q
110 passed
```

## Claim Boundary

This gate proves reviewed-manifest integrity relative to its self-seal before paper-ready audit succeeds. It does not judge human review quality.
