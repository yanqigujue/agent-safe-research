# Reportable Claim Template Plan

## Acceptance Criteria

- Add a red CLI test for `eair-write-reportable-claim-template`.
- Implement the template generator with artifact SHA pins.
- Generate the fixture `reportable_claims.json`.
- Rerun claim audit, bundle seal, and seal verification.
- Add the template command to the live runbook.
- Regenerate the live runbook.
- Run focused and full tests.

## Verification Commands

```powershell
pytest tests/test_mvp.py::test_eair_write_reportable_claim_template_pins_export_and_integrity_artifacts -q
python -m formaltrust_platform eair-write-reportable-claim-template --export outputs/eair_warrant_reportable_export/reportable_results_export.json --integrity-audit outputs/eair_warrant_reportable_export/integrity/reportable_export_integrity_audit.json --output outputs/eair_warrant_reportable_export/reportable_claims.json
python -m formaltrust_platform eair-audit-reportable-claims --claims outputs/eair_warrant_reportable_export/reportable_claims.json --output-dir outputs/eair_warrant_reportable_export/claim_audit
python -m formaltrust_platform eair-seal-reportable-claim-bundle --claims outputs/eair_warrant_reportable_export/reportable_claims.json --claim-audit outputs/eair_warrant_reportable_export/claim_audit/reportable_claim_citation_audit.json --output-dir outputs/eair_warrant_reportable_export/bundle_seal
python -m formaltrust_platform eair-verify-reportable-claim-bundle-seal --seal outputs/eair_warrant_reportable_export/bundle_seal/reportable_claim_bundle_seal.json --output-dir outputs/eair_warrant_reportable_export/bundle_seal/verification
pytest tests/test_mvp.py -k "claim_template or live_runbook or reportable_claims or claim_bundle or claim_bundle_seal or reportable_export or reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence" -q
pytest -q
```
