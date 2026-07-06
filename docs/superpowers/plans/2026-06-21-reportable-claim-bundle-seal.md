# Reportable Claim Bundle Seal Plan

## Acceptance Criteria

- Add a red CLI test for `eair-seal-reportable-claim-bundle`.
- Implement seal generation from a passed claim audit.
- Record claim manifest SHA256, claim audit SHA256, cited artifact SHA256s, and seal payload SHA256.
- Generate a fixture seal under `outputs/eair_warrant_reportable_export/bundle_seal`.
- Update artifact and research docs.
- Run focused and full tests.

## Verification Commands

```powershell
pytest tests/test_mvp.py::test_eair_seal_reportable_claim_bundle_writes_hash_locked_packet -q
python -m formaltrust_platform eair-seal-reportable-claim-bundle --claims outputs/eair_warrant_reportable_export/reportable_claims.json --claim-audit outputs/eair_warrant_reportable_export/claim_audit/reportable_claim_citation_audit.json --output-dir outputs/eair_warrant_reportable_export/bundle_seal
pytest tests/test_mvp.py -k "reportable_claims or claim_bundle or reportable_export or reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence or live_runbook" -q
pytest -q
```
