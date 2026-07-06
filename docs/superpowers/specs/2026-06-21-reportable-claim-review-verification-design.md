# Reportable Claim Review Verification Design

## Problem

`paper_ready_claims.json` now records the source claim manifest hash and source citation-audit hash, but the workflow does not yet have a reviewer-facing command that recomputes those hashes. A reviewed manifest can therefore carry useful provenance fields without a dedicated verifier that checks whether its source artifacts still match.

## Design

Add:

```text
formaltrust eair-verify-reportable-claim-review
```

The command takes:

```text
--claims paper_ready_claims.json
--output-dir paper_ready_claim_review_verification
```

It verifies:

- `artifact_type == "eair_reportable_claims"`;
- `human_reviewed == true`;
- `review_status == "reviewed"`;
- `source_claims_path` exists;
- `source_claims_sha256` matches the current source claim file;
- `source_claim_audit_path` exists;
- `source_claim_audit_sha256` matches the current source audit file;
- source audit `artifact_type == "eair_reportable_claim_citation_audit"`;
- source audit `passed == true`;
- source audit has no errors or failed claims;
- source audit `claims_path` matches `source_claims_path`.

It writes:

```text
reportable_claim_review_verification.json
reportable_claim_review_verification.md
```

The verifier is intentionally narrower than the strict claim audit, seal, and seal verifier. It checks review-declaration provenance, not claim value correctness from scratch.

## Runbook Integration

Insert a command after `paper_ready_claim_review_declaration`:

```text
paper_ready_claim_review_verification
```

The strict paper-ready audit still runs after verification.

## Testing

Use TDD:

- Create a reviewed claim manifest through `eair-record-reportable-claim-review`.
- Verify `eair-verify-reportable-claim-review` passes and writes JSON/Markdown.
- Modify the source audit after review declaration.
- Verify the same command fails and records `source_claim_audit_sha256_matches=false`.
- Update the live-runbook test to require the verification command and required artifacts.
