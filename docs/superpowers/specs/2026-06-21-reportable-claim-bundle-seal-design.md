# Reportable Claim Bundle Seal Design

## Problem

Claim citation audits verify individual structured claims, but a paper submission also needs a compact packet that says which claim manifest, which claim audit, and which cited artifacts were reviewed together.

## Design

Add `eair-seal-reportable-claim-bundle`.

Inputs:

- `reportable_claims.json`
- `reportable_claim_citation_audit.json`

The seal:

- requires the claim audit to pass;
- checks the audit points to the provided claim manifest;
- requires all claim results to pass and artifact SHA pins to match;
- recomputes current SHA256 for cited artifacts;
- writes `reportable_claim_bundle_seal.json` and `.md`;
- records a `seal_payload_sha256` over the seal payload.

## Boundary

This is an archival seal over structured claims and their audited artifacts. It does not replace the claim citation audit and does not parse free-form paper prose.
