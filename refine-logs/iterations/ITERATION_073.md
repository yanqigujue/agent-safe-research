# Iteration 073: Reportable Claim Bundle Seal Verification

## Goal

Make sealed claim packets independently re-verifiable.

## Implemented

- Added `verify_reportable_claim_bundle_seal`.
- Added CLI command `eair-verify-reportable-claim-bundle-seal`.
- Verification checks:
  - `seal_payload_sha256`
  - claim manifest SHA256
  - claim audit SHA256
  - cited artifact SHA256s
- Generated fixture verification:
  - `outputs/eair_warrant_reportable_export/bundle_seal/verification/reportable_claim_bundle_seal_verification.json`
  - `outputs/eair_warrant_reportable_export/bundle_seal/verification/reportable_claim_bundle_seal_verification.md`

## Red-Green

Red check:

```text
pytest tests/test_mvp.py::test_eair_verify_reportable_claim_bundle_seal_detects_payload_hash_mismatch -q
failed because eair-verify-reportable-claim-bundle-seal did not exist
```

Green check:

```text
pytest tests/test_mvp.py::test_eair_verify_reportable_claim_bundle_seal_detects_payload_hash_mismatch -q
1 passed
```

## Fixture Readback

```text
passed=true
expected_seal_payload_sha256=e812019c797337ac8a07ec5b2d3cf1fa3790e9d9069304530406ef26308dda28
actual_seal_payload_sha256=e812019c797337ac8a07ec5b2d3cf1fa3790e9d9069304530406ef26308dda28
cited_artifact sha256_matches=true for 2 artifacts
```

## Boundary

This verifies an archival packet. It does not produce new model-behavior evidence.
