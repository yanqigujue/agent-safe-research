# Iteration 083: Reviewed Claim Manifest Self-Seal

## Goal

Detect post-declaration edits to `paper_ready_claims.json` itself.

## Changes

- Added `review_manifest_payload_sha256` to reviewed claim manifests.
- Updated canonical payload hashing to ignore:
  - `seal_payload_sha256`
  - `review_manifest_payload_sha256`
- Extended `eair-verify-reportable-claim-review` with:
  - `expected_review_manifest_payload_sha256`
  - `actual_review_manifest_payload_sha256`
  - `review_manifest_payload_sha256_matches`
- Updated Markdown verification output to show the self-seal match.
- Refreshed the strict paper-ready fixture chain.

## TDD

Red checks:

- The review declaration test failed because `review_manifest_payload_sha256` did not exist.
- The manifest-drift test failed because the verifier did not record `review_manifest_payload_sha256_matches`.

Green checks:

- The review declaration writes a 64-character self-seal.
- The verifier passes on a fresh reviewed manifest.
- The verifier fails after `paper_ready_claims.json` is edited post-declaration while source files remain unchanged.

## Fixture Readback

```text
review_manifest_payload_sha256=b874803fc8c861e327657e8778ba8bb922ec39ec9e68646474945d81dfe31e5e
review_manifest_payload_sha256_matches=true
source_claims_sha256_matches=true
source_claim_audit_sha256_matches=true
paper_ready_claim_bundle_seal=7adf75e100e08d294dadf75f7a156a43786f59c6b2f5a38c71b1f4c7ab1b3b76
```

## Verification

```text
pytest tests/test_mvp.py::test_eair_record_reportable_claim_review_requires_passing_audit tests/test_mvp.py::test_eair_verify_reportable_claim_review_detects_reviewed_manifest_drift -q
2 passed

pytest tests/test_mvp.py -k "live_runbook or claim_template or reportable_claims or claim_bundle or claim_bundle_seal or reportable_export or reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence" -q
23 passed, 29 deselected

pytest -q
109 passed
```

## Claim Boundary

The self-seal detects payload drift in the reviewed manifest. It does not judge review quality or replace the strict claim citation audit.
