# Iteration 082: Reportable Claim Review Verification

## Goal

Make reviewed-claim declaration provenance independently verifiable.

## Changes

- Added `verify_reportable_claim_review_declaration`.
- Added CLI command:
  - `eair-verify-reportable-claim-review`
- The verifier checks:
  - reviewed claims artifact type;
  - `human_reviewed=true`;
  - `review_status=reviewed`;
  - source claims path/hash;
  - source claim audit path/hash;
  - source claim audit type;
  - source claim audit pass status;
  - source claim audit `claims_path` alignment.
- The verifier writes:
  - `reportable_claim_review_verification.json`
  - `reportable_claim_review_verification.md`
- The live runbook now includes:
  - `paper_ready_claim_review_verification`

## TDD

Red checks:

- `test_eair_verify_reportable_claim_review_detects_source_audit_drift` failed because `eair-verify-reportable-claim-review` did not exist.
- The live-runbook test failed because `paper_ready_claim_review_verification` was not in the runbook.

Green checks:

- The verifier test passes after adding the function and CLI command.
- The runbook test passes after inserting the verifier command and required artifacts.

## Fixture Readback

```text
passed=true
human_reviewed=true
review_status=reviewed
source_claims_sha256_matches=true
source_claim_audit_sha256_matches=true
source_claim_audit_passed=true
```

## Runbook Readback

```text
commands=19
paper_ready_claim_review_verification=true
required verifier artifact=true
```

## Verification

```text
pytest tests/test_mvp.py::test_eair_verify_reportable_claim_review_detects_source_audit_drift -q
1 passed

pytest tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar -q
1 passed

pytest tests/test_mvp.py -k "live_runbook or claim_template or reportable_claims or claim_bundle or claim_bundle_seal or reportable_export or reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence" -q
23 passed, 28 deselected

pytest -q
108 passed
```

## Claim Boundary

This verifier checks review-declaration provenance and source-audit drift. It does not judge whether the human review was scientifically correct.
