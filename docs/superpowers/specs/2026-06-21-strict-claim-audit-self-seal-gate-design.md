# Strict Claim Audit Self-Seal Gate Design

## Problem

`paper_ready_claims.json` now carries `review_manifest_payload_sha256`, and `eair-verify-reportable-claim-review` can detect edits to the reviewed manifest. However, `eair-audit-reportable-claims --require-reviewed` still treats `human_reviewed=true` as sufficient and does not enforce the self-seal. A caller could skip the review verifier and run strict claim audit on a post-declaration edited reviewed manifest.

## Design

Extend `eair-audit-reportable-claims --require-reviewed` so reviewed manifests must pass their self-seal check.

When `require_reviewed=true` and the manifest is reviewed:

- require `review_manifest_payload_sha256`;
- recompute the canonical manifest payload hash excluding `review_manifest_payload_sha256`;
- fail if the recomputed hash differs.

The claim audit JSON/Markdown should expose:

```text
expected_review_manifest_payload_sha256
actual_review_manifest_payload_sha256
review_manifest_payload_sha256_matches
```

Default non-strict audit remains compatible with template-chain diagnostics.

## Boundary

This gate checks reviewed-manifest integrity before claim-value auditing completes. It does not judge the quality of human review and does not replace source provenance verification.

## Testing

Use TDD:

- Create a valid reviewed manifest through `eair-record-reportable-claim-review`.
- Mutate only claim text in `paper_ready_claims.json`.
- Verify `eair-audit-reportable-claims --require-reviewed` fails with `review_manifest_payload_sha256 mismatch`.
- Verify the audit artifact records `review_manifest_payload_sha256_matches=false`.
