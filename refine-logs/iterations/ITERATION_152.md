# Iteration 152: Related-Work Readiness Coverage

## Status

complete

## Goal

Add the new related-work outline writing artifact to the default paper-readiness forbidden-claim scan.

## TDD

Updated `test_power_ops_paper_claim_readiness_default_scans_current_writing_artifacts` to require:

- at least 9 scanned writing artifacts;
- `docs/power_ops_action_invariance_evidence_bound_related_work_outline_2026-07-02.json` in `artifact_paths`.

Observed red:

```text
assert 8 >= 9
```

## Implementation

- Added related-work outline JSON to `DEFAULT_WRITING_ARTIFACT_PATHS` in `formaltrust_platform/experiments/power_ops_paper_claim_readiness.py`.
- Refreshed numeric audit, residual triage, paper readiness, claim-ledger readiness, abstract, introduction, method, and related-work artifacts.
- Updated README and PAPER_PLAN with related-work outline and 9-artifact readiness coverage.

## Readback

```text
numeric: supported=22, table-binding=184, context-rule=11, ignored-context=62, unsupported=0
triage: needs_evidence=0, categories={}
paper_readiness: PASS, blockers=0, forbidden_scan_artifact_count=9, forbidden_hits=0
related_work_outline: ready, neighbor_count=9, slots=6, forbidden_hits=0
```

## Verification

```text
pytest tests/test_power_ops_action_invariance.py::test_power_ops_evidence_bound_related_work_outline_uses_lit_and_firewall tests/test_power_ops_action_invariance.py::test_power_ops_paper_claim_readiness_default_scans_current_writing_artifacts -q
2 passed

pytest tests/test_power_ops_action_invariance.py -q
45 passed

pytest -q
245 passed
```

## Keep / Revise / Reject

keep

## Next

Iteration 153 should turn the §2 related-work outline into bounded related-work prose with neighbor/source binding.
