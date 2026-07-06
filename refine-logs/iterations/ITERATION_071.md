# Iteration 071: Reportable Claim Artifact SHA Pins

## Goal

Bind structured paper claims to exact artifact versions, not only artifact paths and values.

## Implemented

- `eair_reportable_claims` entries may now include `artifact_sha256`.
- `eair-audit-reportable-claims` compares the expected SHA with the current cited artifact SHA.
- Claim results now include:
  - `expected_artifact_sha256`
  - `artifact_sha256`
  - `artifact_sha256_matches`
- Fixture claim manifest now pins the SHA256 of:
  - `reportable_results_export.json`
  - `reportable_export_integrity_audit.json`

## Red-Green

Red check:

```text
pytest tests/test_mvp.py::test_eair_audit_reportable_claims_detects_artifact_sha256_mismatch -q
failed because the audit passed when artifact value matched but artifact SHA differed
```

Green check:

```text
pytest tests/test_mvp.py::test_eair_audit_reportable_claims_detects_artifact_sha256_mismatch -q
1 passed
```

## Fixture Readback

```text
claim_count=4
passed_claim_count=4
failed_claim_count=0
artifact_sha256_matches=true for all four fixture claims
```

## Boundary

This pins structured claims to JSON artifact versions. It still does not parse arbitrary prose automatically.
