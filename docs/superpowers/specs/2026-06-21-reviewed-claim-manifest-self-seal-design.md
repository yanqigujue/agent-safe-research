# Reviewed Claim Manifest Self-Seal Design

## Problem

`eair-verify-reportable-claim-review` verifies that the source claim manifest and source citation audit still match the hashes recorded inside `paper_ready_claims.json`. However, the reviewed manifest itself does not carry a stable self-seal. If someone edits `paper_ready_claims.json` after the review declaration, the verifier can still pass as long as the recorded source files are unchanged.

## Design

Add a self-seal field to reviewed claim manifests:

```text
review_manifest_payload_sha256
```

`eair-record-reportable-claim-review` computes this hash over the canonical reviewed manifest payload after all review fields are added, excluding `review_manifest_payload_sha256` itself. The existing source claim/audit hashes remain unchanged.

`eair-verify-reportable-claim-review` recomputes the same canonical hash and records:

```text
expected_review_manifest_payload_sha256
actual_review_manifest_payload_sha256
review_manifest_payload_sha256_matches
```

If the self-seal is missing or mismatched, verification fails and writes diagnostics.

## Boundary

The self-seal detects post-declaration edits to `paper_ready_claims.json`. It does not prove that the human review was good and does not replace the strict claim citation audit.

## Testing

Use TDD:

- Update the review declaration test to require `review_manifest_payload_sha256`.
- Add a verifier regression that mutates `paper_ready_claims.json` after declaration while leaving source claim/audit files unchanged.
- Verify `eair-verify-reportable-claim-review` fails with `review_manifest_payload_sha256_matches=false`.
- Refresh the deterministic paper-ready fixture.
