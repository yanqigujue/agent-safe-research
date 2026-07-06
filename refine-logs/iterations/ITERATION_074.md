# Iteration 074: Live Runbook Claim Pipeline

## Goal

Make the sealed-claim evidence factory part of the default live runbook.

## Implemented

- Added live runbook commands:
  - `reportable_claim_citation_audit`
  - `reportable_claim_bundle_seal`
  - `reportable_claim_bundle_seal_verification`
- Added required artifacts:
  - `reportable_claims.json`
  - `reportable_claim_citation_audit.json`
  - `reportable_claim_citation_audit.md`
  - `reportable_claim_bundle_seal.json`
  - `reportable_claim_bundle_seal.md`
  - `reportable_claim_bundle_seal_verification.json`
  - `reportable_claim_bundle_seal_verification.md`
- Regenerated:
  - `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.md`
  - `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.json`

## Red-Green

Red check:

```text
pytest tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar -q
failed because the runbook stopped after reportable_export_integrity_audit
```

Green check:

```text
pytest tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar -q
1 passed
```

## Readback

The regenerated JSON runbook now has 13 commands, ending with:

```text
reportable_claim_citation_audit
reportable_claim_bundle_seal
reportable_claim_bundle_seal_verification
```

## Boundary

The runbook points to `paper_tables/reportable_claims.json`; authors still need to create the structured claim manifest from paper claims.
