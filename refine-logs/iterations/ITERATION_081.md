# Iteration 081: Reportable Claim Review Declaration

## Goal

Close the workflow gap between generated claim templates and paper-ready reviewed claim manifests.

## Changes

- Added `record_reportable_claim_review`.
- Added CLI command:
  - `eair-record-reportable-claim-review`
- The command requires:
  - source `reportable_claims.json`;
  - passing `reportable_claim_citation_audit.json`;
  - reviewer identifier;
  - review note;
  - output path for `paper_ready_claims.json`.
- It refuses:
  - failed claim audits;
  - claim audits with errors;
  - claim audits whose `claims_path` does not match the supplied claims;
  - non-passing claim rows;
  - output paths that overwrite the source claims manifest.
- It writes:
  - `claim_generation=human_reviewed`;
  - `human_reviewed=true`;
  - `review_status=reviewed`;
  - `reviewer`;
  - `review_note`;
  - `reviewed_at_utc`;
  - `source_claims_sha256`;
  - `source_claim_audit_sha256`.
- Updated live runbook:
  - added `paper_ready_claim_review_declaration`;
  - strict audit and strict seal now consume `paper_ready_claims.json`.

## TDD

Red checks:

- `test_eair_record_reportable_claim_review_requires_passing_audit` failed because `eair-record-reportable-claim-review` did not exist.
- The live-runbook test failed because `paper_ready_claim_review_declaration` was missing.

Green checks:

- The review declaration test passes after adding the function and CLI command.
- The runbook test passes after inserting the declaration command and switching strict paper-ready inputs to `paper_ready_claims.json`.

## Fixture Readback

```text
paper_ready_claims:
  claim_generation=human_reviewed
  human_reviewed=true
  review_status=reviewed
  reviewer=paper-author
  source_claims_sha256=1069bdd8212f10c01d95c680d4ac4c1042f933335ef7de6c6a0997e7143f0833
  source_claim_audit_sha256=1d1deaa32625fa2c8fe2c8d58ce017642b7612e67b2ebf07bf75df2d00d42d8f

paper_ready_claim_audit:
  passed=true
  require_reviewed=true
  human_reviewed=true
  review_status=reviewed
  claims=3/3

paper_ready_claim_bundle_seal:
  sealed=true
  require_reviewed=true
  human_reviewed=true
  review_status=reviewed
  seal_payload_sha256=ec8f268e2b4421fb01004a84b867d4736d4b3f68ce99cbe7da1a9ab53cf7c75c

paper_ready_claim_bundle_seal_verification:
  passed=true
  require_reviewed=true
  seal_require_reviewed=true
  human_reviewed=true
  review_status=reviewed
```

## Verification

```text
pytest tests/test_mvp.py::test_eair_record_reportable_claim_review_requires_passing_audit -q
1 passed

pytest tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar -q
1 passed

pytest tests/test_mvp.py -k "live_runbook or claim_template or reportable_claims or claim_bundle or claim_bundle_seal or reportable_export or reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence" -q
23 passed, 27 deselected

pytest -q
107 passed
```

## Claim Boundary

This iteration records a declared human review and locks that declaration to the source claim manifest and citation audit. It does not prove that the reviewer made a correct scientific judgment.
