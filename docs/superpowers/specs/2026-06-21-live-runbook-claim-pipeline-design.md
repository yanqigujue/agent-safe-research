# Live Runbook Claim Pipeline Design

## Problem

The live prompt-protocol runbook included reportable export integrity, but the newer claim citation audit, claim bundle seal, and seal verification steps were still only documented separately. That makes the end-to-end evidence factory easy to skip during live-paper handoff.

## Design

Extend the live runbook command sequence after `reportable_export_integrity_audit`:

1. `reportable_claim_citation_audit`
2. `reportable_claim_bundle_seal`
3. `reportable_claim_bundle_seal_verification`

The runbook points to `paper_tables/reportable_claims.json` as an author-prepared structured claim manifest. It does not auto-generate paper claims.

## Boundary

The runbook remains protocol documentation, not live-model evidence. The claim manifest must be authored from paper claims after reportable tables are created.
