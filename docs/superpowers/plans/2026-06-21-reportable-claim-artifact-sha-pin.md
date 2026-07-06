# Reportable Claim Artifact SHA Pin Plan

## Acceptance Criteria

- Add a red test where a cited artifact has the expected JSON value but a different SHA256 from the claim manifest.
- Make `eair-audit-reportable-claims` block on `artifact_sha256 mismatch`.
- Preserve existing value-mismatch behavior.
- Update fixture `reportable_claims.json` with artifact SHA pins.
- Regenerate fixture claim audit and verify `artifact_sha256_matches=true`.
- Run focused and full tests.

## Verification Commands

```powershell
pytest tests/test_mvp.py::test_eair_audit_reportable_claims_detects_artifact_sha256_mismatch -q
pytest tests/test_mvp.py::test_eair_audit_reportable_claims_detects_metric_mismatch tests/test_mvp.py::test_eair_audit_reportable_claims_detects_artifact_sha256_mismatch -q
python -m formaltrust_platform eair-audit-reportable-claims --claims outputs/eair_warrant_reportable_export/reportable_claims.json --output-dir outputs/eair_warrant_reportable_export/claim_audit
pytest tests/test_mvp.py -k "reportable_claims or reportable_export or reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence or live_runbook" -q
pytest -q
```
