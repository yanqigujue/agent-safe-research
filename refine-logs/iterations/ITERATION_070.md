# Iteration 070: Reportable Claim Citation Audit

## Goal

Make paper-facing numeric claims machine-checkable against reportable artifacts.

## Implemented

- Added `audit_reportable_claim_citations`.
- Added CLI command `eair-audit-reportable-claims`.
- Added dotted JSON path resolution with list-index support.
- Added output artifacts:
  - `reportable_claim_citation_audit.json`
  - `reportable_claim_citation_audit.md`
- Added fixture claim manifest:
  - `outputs/eair_warrant_reportable_export/reportable_claims.json`
- Generated fixture audit:
  - `outputs/eair_warrant_reportable_export/claim_audit/reportable_claim_citation_audit.json`

## Red-Green

Red check:

```text
pytest tests/test_mvp.py::test_eair_audit_reportable_claims_detects_metric_mismatch -q
failed because eair-audit-reportable-claims did not exist
```

Green check:

```text
pytest tests/test_mvp.py::test_eair_audit_reportable_claims_detects_metric_mismatch -q
1 passed
```

## Fixture Readback

```text
claim_count=4
passed_claim_count=4
failed_claim_count=0
```

Checked fixture claims:

- `warrant_leaderboard.0.warrant_quality_score == 0.0`
- `protocol_legitimacy_by_prompt_variant.0.adherence_legitimacy_gap == 1.0`
- `reportable_export_integrity_audit.passed == true`
- `checked_child_artifacts.0.rows_match_export == true`

## Boundary

This audits structured claim manifests. It does not yet parse free-form paper prose.
