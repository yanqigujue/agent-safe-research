# Reportable Claim Review Declaration Design

## Problem

The paper-ready claim chain now requires `human_reviewed=true`, but the current workflow still leaves that transition to manual JSON editing. That is too weak for the evidence-factory story: the system can audit, seal, and verify reviewed packets, but it does not yet create an auditable handoff from a generated template manifest to a reviewed manifest.

## Design

Add a review declaration command:

```text
formaltrust eair-record-reportable-claim-review
```

The command takes:

```text
--claims reportable_claims.json
--claim-audit claim_audit/reportable_claim_citation_audit.json
--reviewer <reviewer-id>
--review-note <short declaration>
--output paper_ready_claims.json
```

It refuses to mark claims reviewed unless the supplied claim citation audit passed, references the same source claims path, has no failed claims, and has no errors. It writes a new reviewed manifest instead of modifying the source manifest in place.

The output keeps `artifact_type="eair_reportable_claims"` and sets:

```text
claim_generation="human_reviewed"
human_reviewed=true
review_status="reviewed"
```

It also records reviewer metadata and content hashes:

```text
reviewer
review_note
reviewed_at_utc
source_claims_path
source_claims_sha256
source_claim_audit_path
source_claim_audit_sha256
review_claim_count
review_passed_claim_count
```

This is a declaration artifact, not proof that the scientific review was good.

## Runbook Integration

The live prompt-protocol runbook should include a paper-ready review declaration step between the diagnostic claim audit and the strict paper-ready audit:

```text
reportable_claim_citation_audit
paper_ready_claim_review_declaration
paper_ready_claim_citation_audit --claims paper_ready_claims.json --require-reviewed
paper_ready_claim_bundle_seal --claims paper_ready_claims.json --require-reviewed
paper_ready_claim_bundle_seal_verification --require-reviewed
```

## Testing

Use TDD:

- Add a CLI regression test that verifies the review command rejects a failed claim audit.
- Verify it writes a reviewed manifest when the audit passes.
- Verify strict `eair-audit-reportable-claims --require-reviewed` accepts the reviewed manifest.
- Update the live-runbook test to require the review declaration command and `paper_ready_claims.json`.
