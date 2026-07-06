# Iteration 077: Reportable Claim Review Gate

## Goal

Separate citation-correct template claims from paper-ready human-reviewed claims.

## Design

`eair-audit-reportable-claims` now has a strict mode:

```text
--require-reviewed
```

Default mode remains compatible with deterministic template-chain fixtures. Strict mode requires either `claim_generation="human_reviewed"` or `human_reviewed=true`.

## Changes

- Added `require_reviewed` to `audit_reportable_claim_citations`.
- Added audit payload fields:
  - `require_reviewed`
  - `human_reviewed`
  - `review_status`
- Added CLI option `--require-reviewed`.
- Added a regression test proving:
  - a template manifest fails strict audit even if value/hash checks pass;
  - the same manifest passes after being marked human reviewed.
- Refreshed the fixture claim audit, bundle seal, and seal verification artifacts.

## TDD Record

Red check:

```text
pytest tests/test_mvp.py::test_eair_audit_reportable_claims_require_reviewed_rejects_template_manifest -q
failed because --require-reviewed did not exist
```

Green check:

```text
pytest tests/test_mvp.py::test_eair_audit_reportable_claims_require_reviewed_rejects_template_manifest -q
1 passed
```

## Artifact Refresh

Default fixture audit remains a template-chain diagnostic:

```text
claim_audit=3/3
require_reviewed=false
human_reviewed=false
review_status=unreviewed
```

Seal refresh:

```text
sealed=true
seal_payload_sha256=e43a94815da53f29c40f17ef5125acf4e1b793ce5cba538aaf984afbdf9de4b6
seal_verification passed=true
```

## Verification

Focused:

```text
pytest tests/test_mvp.py -k "claim_template or reportable_claims or claim_bundle or claim_bundle_seal or reportable_export or reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence" -q
19 passed, 28 deselected
```

Full:

```text
pytest -q
104 passed
```

## Claim Boundary

Supported:

```text
The audit can require an explicit human-review marker before treating structured claims as paper-ready.
```

Not supported:

```text
The audit does not verify the quality of the human review itself.
```
