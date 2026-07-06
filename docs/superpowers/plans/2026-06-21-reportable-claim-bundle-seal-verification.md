# Reportable Claim Bundle Seal Verification Plan

## Acceptance Criteria

- Add a red CLI test where seal content is modified but `seal_payload_sha256` is not updated.
- Implement `verify_reportable_claim_bundle_seal`.
- Add `formaltrust eair-verify-reportable-claim-bundle-seal`.
- Write JSON/Markdown diagnostics before blocking on mismatch.
- Generate fixture verification under `outputs/eair_warrant_reportable_export/bundle_seal/verification`.
- Run focused and full tests.

## Verification Commands

```powershell
pytest tests/test_mvp.py::test_eair_verify_reportable_claim_bundle_seal_detects_payload_hash_mismatch -q
python -m formaltrust_platform eair-verify-reportable-claim-bundle-seal --seal outputs/eair_warrant_reportable_export/bundle_seal/reportable_claim_bundle_seal.json --output-dir outputs/eair_warrant_reportable_export/bundle_seal/verification
pytest tests/test_mvp.py -k "reportable_claims or claim_bundle or claim_bundle_seal or reportable_export or reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence or live_runbook" -q
pytest -q
```
