# Reportable Claim Paper-Ready Seal Design

## Problem

`eair-audit-reportable-claims --require-reviewed` can reject unreviewed template manifests, but the final seal command can still seal a default unreviewed audit. That makes the strict paper-ready gate easy to bypass at the final submission-packet layer.

## Design

Add an optional strict mode to the seal command:

- `eair-seal-reportable-claim-bundle --require-reviewed`.
- Default seal behavior stays compatible with deterministic template-chain fixtures.
- Strict seal mode requires the supplied claim audit to have `require_reviewed=true`, `human_reviewed=true`, and `review_status="reviewed"`.
- The seal payload records `require_reviewed`, `human_reviewed`, and `review_status` from the claim audit.

This keeps diagnostics and paper-ready sealing separate: template fixtures can still be sealed for artifact-chain debugging, while paper submission packets need a reviewed audit.

## Testing

Add a CLI regression test that attempts strict sealing with an unreviewed but passing claim audit and verifies the seal is blocked. Then replace the audit with a reviewed strict audit and verify the strict seal succeeds and records `review_status="reviewed"`.
