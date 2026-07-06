# Reportable Claim Citation Audit Design

## Problem

Reportable exports and integrity audits protect artifacts, but a paper draft can still cite the wrong number or cite a result without a machine-checkable link back to the artifact field that supports it.

## Design

Add `eair-audit-reportable-claims`.

Input is a JSON claim manifest:

```json
{
  "artifact_type": "eair_reportable_claims",
  "claims": [
    {
      "claim_id": "fixture_warrant_quality_zero",
      "text": "The reportable WarrantGuard fixture has warrant_quality_score 0.0.",
      "artifact_path": "outputs/eair_warrant_reportable_export/reportable_results_export.json",
      "json_path": "warrant_leaderboard.0.warrant_quality_score",
      "expected": 0.0
    }
  ]
}
```

The audit:

- loads each cited artifact;
- records the artifact SHA256;
- resolves a simple dotted JSON path with list indices;
- compares the actual value to the expected value by canonical JSON equality;
- writes `reportable_claim_citation_audit.json` and `.md`;
- blocks on mismatch.

## Boundary

This first version audits structured claim manifests, not free-form prose. It is meant to sit between reportable artifacts and paper writing: authors turn paper claims into structured claim citations, then the audit verifies the values.
