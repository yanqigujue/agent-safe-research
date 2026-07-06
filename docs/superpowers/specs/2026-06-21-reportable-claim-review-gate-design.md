# Reportable Claim Review Gate Design

## Problem

`eair-write-reportable-claim-template` now avoids overwriting reviewed claim manifests, but the downstream citation audit can still pass a starter manifest with `claim_generation="template"`. That is useful for deterministic fixtures, yet too weak for a paper-ready claim packet.

## Design

Add an optional reviewed-manifest gate to the reportable claim citation audit:

- Default behavior stays compatible with template fixtures.
- `eair-audit-reportable-claims --require-reviewed` requires the manifest to state `claim_generation="human_reviewed"` or `human_reviewed=true`.
- The audit JSON/Markdown records whether review was required and whether the manifest passed the review gate.
- The gate fails before paper-facing sealing if authors try to treat a starter template as reviewed evidence.

This is deliberately an audit option, not a seal default, so template fixtures can continue to demonstrate the artifact chain while formal paper runs can opt into the stricter gate.

## Testing

Add a CLI regression test that creates a valid template manifest, runs `eair-audit-reportable-claims --require-reviewed`, verifies exit code 2 and a diagnostic JSON with `review_status="unreviewed"`, then marks the same manifest as human-reviewed and verifies the strict audit passes.
