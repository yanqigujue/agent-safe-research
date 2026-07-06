# Iteration 146: Writing-Artifact Readiness Coverage

## Status

complete

## Goal

Ensure the paper-claim readiness gate scans all current writing artifacts by default, including the new abstract and introduction artifacts.

## TDD

Added `test_power_ops_paper_claim_readiness_default_scans_current_writing_artifacts`.

Observed red:

```text
assert 2 >= 6
```

The default readiness CLI scanned only the draft skeleton and prose draft.

## Implementation

- Added `DEFAULT_WRITING_ARTIFACT_PATHS` to `formaltrust_platform/experiments/power_ops_paper_claim_readiness.py`.
- Included:
  - `docs/power_ops_action_invariance_draft_skeleton_2026-07-02.json`
  - `docs/power_ops_action_invariance_prose_draft_2026-07-02.json`
  - `docs/power_ops_action_invariance_readiness_bound_abstract_2026-07-02.json`
  - `docs/power_ops_action_invariance_evidence_bound_abstract_2026-07-02.json`
  - `docs/power_ops_action_invariance_evidence_bound_intro_2026-07-02.json`
  - `docs/power_ops_action_invariance_evidence_bound_intro_prose_2026-07-02.json`
- Added `artifact_paths` to the `forbidden_claim_scan` JSON output.

## Regenerated Artifacts

- `docs/power_ops_action_invariance_numeric_claim_audit_2026-07-02.md/json`
- `docs/power_ops_action_invariance_residual_numeric_triage_2026-07-02.md/json`
- `docs/power_ops_action_invariance_paper_claim_readiness_2026-07-02.md/json`
- `docs/power_ops_action_invariance_claim_ledger_readiness_2026-07-02.md/json`
- `docs/power_ops_action_invariance_readiness_bound_abstract_2026-07-02.md/json`
- `docs/power_ops_action_invariance_evidence_bound_abstract_2026-07-02.md/json`
- `docs/power_ops_action_invariance_evidence_bound_intro_2026-07-02.md/json`
- `docs/power_ops_action_invariance_evidence_bound_intro_prose_2026-07-02.md/json`

## Readback

```text
numeric: supported=22, table-binding=184, context-rule=11, ignored-context=53, unsupported=0
triage: needs_evidence=0, categories={}
paper_readiness: PASS, blockers=0, forbidden_scan_artifact_count=6, forbidden_hits=0
claim_ledger_readiness: PASS, paper_ready_supported_claims=11, forbidden_claims=7
```

## Verification

```text
pytest tests/test_power_ops_action_invariance.py::test_power_ops_evidence_bound_intro_prose_keeps_paragraph_evidence tests/test_power_ops_action_invariance.py::test_power_ops_paper_claim_readiness_default_scans_current_writing_artifacts -q
2 passed

pytest tests/test_power_ops_action_invariance.py -q
42 passed

pytest -q
242 passed
```

## Keep / Revise / Reject

keep

## Next

Iteration 38 should build an evidence-bound method-section outline from the formal model, CapGuard flow, and claim ledger.
