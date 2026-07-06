# Live Runbook Paper-Ready Claim Chain Design

## Problem

The live prompt-protocol runbook currently includes the default reportable claim template, claim audit, claim seal, and seal verification commands. Those commands are useful for diagnostics, but they do not require the strict paper-ready reviewed gates added in Iterations 077-079.

## Design

Extend `write_live_runbook` with a second paper-ready claim chain:

```text
paper_ready_claim_citation_audit
paper_ready_claim_bundle_seal
paper_ready_claim_bundle_seal_verification
```

Each command uses `--require-reviewed`. The default diagnostic chain remains in the runbook because it is useful immediately after template generation. The paper-ready chain gives the author/reviewer a concrete handoff after `reportable_claims.json` has been human-reviewed.

Required artifacts should include the strict output directories:

```text
paper_ready_claim_audit/reportable_claim_citation_audit.json
paper_ready_claim_bundle_seal/reportable_claim_bundle_seal.json
paper_ready_claim_bundle_seal/verification/reportable_claim_bundle_seal_verification.json
```

## Testing

Update the live-runbook regression test so it requires the three paper-ready command names and verifies that each contains `--require-reviewed`.
