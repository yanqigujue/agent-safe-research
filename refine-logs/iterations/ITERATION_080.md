# Iteration 080: Live Runbook Paper-Ready Claim Handoff

## Goal

Carry the reviewed claim-packet boundary into the generated live prompt-protocol runbook.

## Changes

- Added three paper-ready runbook command slots:
  - `paper_ready_claim_citation_audit`
  - `paper_ready_claim_bundle_seal`
  - `paper_ready_claim_bundle_seal_verification`
- Required `--require-reviewed` on each paper-ready command.
- Kept the default diagnostic chain unchanged:
  - `reportable_claim_template`
  - `reportable_claim_citation_audit`
  - `reportable_claim_bundle_seal`
  - `reportable_claim_bundle_seal_verification`
- Added required artifact entries for:
  - `paper_ready_claim_audit/reportable_claim_citation_audit.json`
  - `paper_ready_claim_bundle_seal/reportable_claim_bundle_seal.json`
  - `paper_ready_claim_bundle_seal/verification/reportable_claim_bundle_seal_verification.json`
- Changed the Markdown renderer to enumerate all commands from the JSON payload, preventing claim-chain commands from being JSON-only.
- Regenerated:
  - `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.md`
  - `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.json`

## TDD

Red checks:

- The runbook JSON-sidecar test failed because the strict `paper_ready_*` command names were missing.
- A second red check failed because the Markdown runbook did not render claim commands at all.

Green checks:

- The same runbook regression now passes with strict commands in JSON and Markdown.

## Readback

```text
commands=17
required_artifacts=47
strict_commands=3
strict_flags=3
```

## Verification

```text
pytest tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar -q
1 passed

pytest tests/test_mvp.py -k "live_runbook or claim_template or reportable_claims or claim_bundle or claim_bundle_seal or reportable_export or reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence" -q
23 passed, 26 deselected

pytest -q
106 passed
```

## Claim Boundary

This iteration does not prove that a specific claim manifest has been reviewed. It makes the reviewer-executable strict audit, strict seal, and strict verification path explicit in the live runbook.
