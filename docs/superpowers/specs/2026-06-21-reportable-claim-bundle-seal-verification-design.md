# Reportable Claim Bundle Seal Verification Design

## Problem

A claim bundle seal archives claim evidence, but reviewers and future reruns need a command that verifies the seal still matches the current filesystem state.

## Design

Add `eair-verify-reportable-claim-bundle-seal`.

The verifier checks:

- seal artifact type and `sealed=true`;
- `seal_payload_sha256` over the canonical seal payload;
- claim manifest SHA256;
- claim audit SHA256;
- every cited artifact SHA256.

It writes:

- `reportable_claim_bundle_seal_verification.json`
- `reportable_claim_bundle_seal_verification.md`

On mismatch, it writes diagnostics and exits with a blocking error.

## Boundary

This verifies a sealed packet against local files. It does not rerun model sampling, replay, or natural-language paper parsing.
