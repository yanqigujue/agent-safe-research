# Iteration 079: Paper-Ready Seal Verification

## Goal

Let reviewers verify that a claim bundle seal is paper-ready, not merely hash-consistent.

## Design

`eair-verify-reportable-claim-bundle-seal` now has a strict mode:

```text
--require-reviewed
```

Default verification remains an integrity check. Strict verification additionally requires the seal payload to record:

```text
require_reviewed=true
human_reviewed=true
review_status=reviewed
```

## Changes

- Added `require_reviewed` to `verify_reportable_claim_bundle_seal`.
- Added `--require-reviewed` to `eair-verify-reportable-claim-bundle-seal`.
- Strict verification rejects diagnostic seals even when all hashes match.
- Verification JSON and Markdown now record:
  - `require_reviewed`
  - `seal_require_reviewed`
  - `human_reviewed`
  - `review_status`
- Refreshed default diagnostic verification artifact.

## TDD Record

Red check:

```text
pytest tests/test_mvp.py::test_eair_verify_reportable_claim_bundle_seal_require_reviewed_rejects_diagnostic_seal -q
failed because eair-verify-reportable-claim-bundle-seal did not accept --require-reviewed
```

Green check:

```text
pytest tests/test_mvp.py::test_eair_verify_reportable_claim_bundle_seal_require_reviewed_rejects_diagnostic_seal -q
1 passed
```

## Artifact Refresh

Default diagnostic verification:

```text
passed=true
require_reviewed=false
seal_require_reviewed=false
human_reviewed=false
review_status=unreviewed
expected_seal_payload_sha256=cb4977988522a8f34f748cac2f45eb8f20c7d7daf648c75f8c5603d4a7cab380
actual_seal_payload_sha256=cb4977988522a8f34f748cac2f45eb8f20c7d7daf648c75f8c5603d4a7cab380
```

## Verification

Focused:

```text
pytest tests/test_mvp.py -k "claim_template or reportable_claims or claim_bundle or claim_bundle_seal or reportable_export or reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence" -q
21 passed, 28 deselected
```

Full:

```text
pytest -q
106 passed
```

## Claim Boundary

Supported:

```text
Reviewers can distinguish a hash-consistent diagnostic seal from a paper-ready reviewed seal.
```

Not supported:

```text
Strict verification does not judge whether the human review was scientifically correct.
```
