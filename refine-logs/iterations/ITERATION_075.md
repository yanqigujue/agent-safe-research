# Iteration 075: Reportable Claim Template

## Goal

Reduce manual friction in creating `reportable_claims.json`.

## Implemented

- Added `write_reportable_claim_template`.
- Added CLI command `eair-write-reportable-claim-template`.
- Template claims include artifact SHA pins.
- Generated fixture claim manifest from:
  - `reportable_results_export.json`
  - `reportable_export_integrity_audit.json`
- Reran fixture:
  - claim citation audit
  - claim bundle seal
  - seal verification
- Added `reportable_claim_template` to the live prompt-protocol runbook.

## Red-Green

Red checks:

```text
pytest tests/test_mvp.py::test_eair_write_reportable_claim_template_pins_export_and_integrity_artifacts -q
failed because eair-write-reportable-claim-template did not exist

pytest tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar -q
failed because the runbook did not include reportable_claim_template
```

Green checks:

```text
pytest tests/test_mvp.py::test_eair_write_reportable_claim_template_pins_export_and_integrity_artifacts -q
1 passed

pytest tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar -q
1 passed
```

## Fixture Readback

```text
template_claim_count=3
claim_audit=3/3
sealed=true
seal_payload_sha256=8a6169e8e0595b0a6344ddb5b2ff31cf8fab5d55e8aeb4492be46ce0c89d27af
seal_verification passed=true
```

## Boundary

The template is a starter. Authors still need to review wording and add paper-specific claims.
