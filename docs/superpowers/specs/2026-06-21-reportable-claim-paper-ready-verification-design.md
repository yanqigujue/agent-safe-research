# Reportable Claim Paper-Ready Verification Design

## Problem

`eair-seal-reportable-claim-bundle --require-reviewed` prevents creating a paper-ready seal from an unreviewed audit, but the verifier still treats a default diagnostic seal as `passed=true` if hashes match. A reviewer needs a strict verification mode that rejects diagnostic template-chain seals when checking a paper-ready packet.

## Design

Add an optional strict mode to seal verification:

- `eair-verify-reportable-claim-bundle-seal --require-reviewed`.
- Default verification remains a pure integrity check for diagnostic seals.
- Strict verification additionally requires the seal payload to have `require_reviewed=true`, `human_reviewed=true`, and `review_status="reviewed"`.
- The verification JSON/Markdown records `require_reviewed`, `human_reviewed`, and `review_status` so reviewer-facing reports expose whether the packet is paper-ready.

This completes the paper-ready chain:

```text
strict claim audit -> strict seal -> strict seal verification
```

## Testing

Add a CLI regression test that verifies a diagnostic unreviewed seal passes default verification but fails `--require-reviewed`; then create a reviewed strict seal and verify `--require-reviewed` passes.
