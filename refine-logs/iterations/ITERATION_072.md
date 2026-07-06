# Iteration 072: Reportable Claim Bundle Seal

## Goal

Create an archival packet for structured paper claims and their cited reportable artifacts.

## Implemented

- Added `seal_reportable_claim_bundle`.
- Added CLI command `eair-seal-reportable-claim-bundle`.
- Seal output includes:
  - `claims_sha256`
  - `claim_audit_sha256`
  - cited artifact paths and SHA256s
  - `seal_payload_sha256`
- Generated fixture seal:
  - `outputs/eair_warrant_reportable_export/bundle_seal/reportable_claim_bundle_seal.json`
  - `outputs/eair_warrant_reportable_export/bundle_seal/reportable_claim_bundle_seal.md`

## Red-Green

Red check:

```text
pytest tests/test_mvp.py::test_eair_seal_reportable_claim_bundle_writes_hash_locked_packet -q
failed because eair-seal-reportable-claim-bundle did not exist
```

Green check:

```text
pytest tests/test_mvp.py::test_eair_seal_reportable_claim_bundle_writes_hash_locked_packet -q
1 passed
```

## Fixture Readback

```text
sealed=true
claim_count=4
passed_claim_count=4
cited_artifacts=2
seal_payload_sha256=e812019c797337ac8a07ec5b2d3cf1fa3790e9d9069304530406ef26308dda28
```

## Boundary

The seal archives structured claim evidence. It does not independently rerun model sampling or parse free-form paper prose.
