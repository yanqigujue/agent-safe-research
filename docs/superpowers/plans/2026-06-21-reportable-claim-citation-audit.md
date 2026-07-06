# Reportable Claim Citation Audit Plan

## Acceptance Criteria

- Add a red CLI test where a claim expects the wrong artifact value.
- Implement `audit_reportable_claim_citations`.
- Add `formaltrust eair-audit-reportable-claims`.
- Write JSON/Markdown audit files before blocking on mismatch.
- Generate a fixture claim manifest under `outputs/eair_warrant_reportable_export`.
- Run the claim audit and verify all fixture claims pass.
- Update research and artifact documentation.

## Verification Commands

```powershell
pytest tests/test_mvp.py::test_eair_audit_reportable_claims_detects_metric_mismatch -q
python -m formaltrust_platform eair-audit-reportable-claims --claims outputs/eair_warrant_reportable_export/reportable_claims.json --output-dir outputs/eair_warrant_reportable_export/claim_audit
pytest tests/test_mvp.py -k "reportable_claims or reportable_export or reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence or live_runbook" -q
pytest -q
```
