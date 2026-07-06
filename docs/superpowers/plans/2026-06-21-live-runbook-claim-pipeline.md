# Live Runbook Claim Pipeline Plan

## Acceptance Criteria

- Add a red test requiring claim-audit, bundle-seal, and seal-verification commands in the live runbook.
- Extend `_live_runbook_payload`.
- Add claim pipeline artifacts to `required_artifacts`.
- Regenerate `RUN_LIVE_PROMPT_MATRIX.md` and `.json`.
- Run focused and full tests.

## Verification Commands

```powershell
pytest tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar -q
python -m formaltrust_platform eair-write-live-runbook --config examples/eair_prompt_protocol_matrix_live_template.yaml --output outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.md
pytest tests/test_mvp.py -k "live_runbook or reportable_claims or claim_bundle or claim_bundle_seal or reportable_export or reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence" -q
pytest -q
```
