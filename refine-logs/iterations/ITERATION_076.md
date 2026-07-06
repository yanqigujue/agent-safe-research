# Iteration 076: Reportable Claim Template Overwrite Guard

## Goal

Prevent `eair-write-reportable-claim-template` from silently overwriting an existing human-reviewed `reportable_claims.json`.

## Design

The claim-template writer is an initialization helper. It now treats an existing output file as protected by default and requires explicit `--force` for regeneration.

## Changes

- Added `force: bool = False` to `write_reportable_claim_template`.
- Added CLI option `--force` to `eair-write-reportable-claim-template`.
- Added a regression test that:
  - pre-creates `reportable_claims.json` with `claim_generation=human_reviewed`;
  - verifies the command fails without `--force`;
  - verifies the reviewed file remains unchanged;
  - verifies `--force` regenerates the template.
- Updated artifact documentation, paper plan, research direction notes, experiment logs, and claim-evidence audit notes.

## TDD Record

Red check:

```text
pytest tests/test_mvp.py::test_eair_write_reportable_claim_template_refuses_existing_output_without_force -q
failed because the command exited 0 and overwrote the existing file
```

Green check:

```text
pytest tests/test_mvp.py::test_eair_write_reportable_claim_template_refuses_existing_output_without_force -q
1 passed
```

## Artifact Refresh

Forced template refresh:

```text
python -m formaltrust_platform eair-write-reportable-claim-template --export outputs/eair_warrant_reportable_export/reportable_results_export.json --integrity-audit outputs/eair_warrant_reportable_export/integrity/reportable_export_integrity_audit.json --output outputs/eair_warrant_reportable_export/reportable_claims.json --force
claims: 3
```

Downstream checks:

```text
claim_audit=3/3
sealed=true
seal_payload_sha256=8a6169e8e0595b0a6344ddb5b2ff31cf8fab5d55e8aeb4492be46ce0c89d27af
seal_verification passed=true
```

## Verification

Focused:

```text
pytest tests/test_mvp.py -k "claim_template or live_runbook or reportable_claims or claim_bundle or claim_bundle_seal or reportable_export or reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence" -q
20 passed, 26 deselected
```

Full:

```text
pytest -q
103 passed
```

## Claim Boundary

Supported:

```text
The evidence factory can initialize structured paper-claim manifests while protecting reviewed manifests from accidental regeneration.
```

Not supported:

```text
The overwrite guard does not judge the scientific strength of human-authored paper claims.
```
