# Iteration 078: Paper-Ready Claim Seal

## Goal

Carry the reviewed-claim gate into the final sealed claim packet.

## Design

`eair-seal-reportable-claim-bundle` now has a strict mode:

```text
--require-reviewed
```

Default sealing remains available for deterministic template-chain diagnostics. Strict sealing requires the supplied claim audit to have:

```text
require_reviewed=true
human_reviewed=true
review_status=reviewed
```

## Changes

- Added `require_reviewed` to `seal_reportable_claim_bundle`.
- Added `--require-reviewed` to `eair-seal-reportable-claim-bundle`.
- Strict seal mode rejects unreviewed or non-strict claim audits.
- Seal JSON and Markdown now record:
  - `require_reviewed`
  - `human_reviewed`
  - `review_status`
- Refreshed default diagnostic seal and seal verification artifacts.

## TDD Record

Red check:

```text
pytest tests/test_mvp.py::test_eair_seal_reportable_claim_bundle_require_reviewed_rejects_unreviewed_audit -q
failed because eair-seal-reportable-claim-bundle did not accept --require-reviewed
```

Second red check:

```text
pytest tests/test_mvp.py::test_eair_seal_reportable_claim_bundle_require_reviewed_rejects_unreviewed_audit -q
failed because seal Markdown did not show review_status
```

Green check:

```text
pytest tests/test_mvp.py::test_eair_seal_reportable_claim_bundle_require_reviewed_rejects_unreviewed_audit -q
1 passed
```

## Artifact Refresh

Default diagnostic fixture:

```text
claim_audit=3/3
require_reviewed=false
human_reviewed=false
review_status=unreviewed
sealed=true
seal_payload_sha256=cb4977988522a8f34f748cac2f45eb8f20c7d7daf648c75f8c5603d4a7cab380
seal_verification passed=true
```

## Verification

Focused:

```text
pytest tests/test_mvp.py -k "claim_template or reportable_claims or claim_bundle or claim_bundle_seal or reportable_export or reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence" -q
20 passed, 28 deselected
```

Full:

```text
pytest -q
105 passed
```

## Claim Boundary

Supported:

```text
The final claim bundle seal can require a reviewed strict claim audit before producing a paper-ready packet.
```

Not supported:

```text
The seal does not judge whether the human review was scientifically correct.
```
