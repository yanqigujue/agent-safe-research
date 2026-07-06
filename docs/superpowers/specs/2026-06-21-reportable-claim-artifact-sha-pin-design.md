# Reportable Claim Artifact SHA Pin Design

## Problem

The claim citation audit records each cited artifact SHA256, but without a pinned expected SHA a claim can still pass after the artifact is regenerated or replaced, as long as the cited JSON path keeps the same value.

## Design

Allow each `eair_reportable_claims` entry to include:

```json
{
  "artifact_sha256": "<expected sha256>"
}
```

When present, `eair-audit-reportable-claims` checks the current artifact SHA256 against the expected value and records:

- `expected_artifact_sha256`
- `artifact_sha256`
- `artifact_sha256_matches`

The claim passes only when both the artifact SHA pin and the expected JSON value match.

## Boundary

The SHA pin is optional for compatibility. Strong paper-facing claim manifests should include it for every cited artifact.
