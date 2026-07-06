# Iteration 166: Evidence-Bound Evaluation Setup

## Status

complete

## Goal

Fill the missing section 4 evaluation setup with bounded prose sourced from dataset, baseline, trace, table-binding, and draft-audit artifacts, then integrate it into the assembled paper draft.

## TDD

Added `test_power_ops_evidence_bound_evaluation_setup_uses_dataset_trace_and_audits` to require:

- artifact type `power_ops_evidence_bound_evaluation_setup`;
- status `ready`;
- six section-4 paragraph slots;
- expanded case count `18`;
- baseline count `4`;
- trace-import case count `4`;
- multi-step trace count `1`;
- fully supported table rows `18`;
- forbidden claim hits `0`;
- blocked output when dataset oracle coverage is incomplete.

Observed red:

```text
ModuleNotFoundError: No module named 'formaltrust_platform.experiments.power_ops_evidence_bound_evaluation_setup'
```

Then updated integration tests to require:

- paper draft includes `evaluation_setup` between method and results;
- draft consistency audit checks 7 sections;
- paper-readiness default scan covers 16 writing artifacts.

Observed red:

```text
TypeError: build_evidence_bound_paper_draft() got an unexpected keyword argument 'evaluation_setup_path'
assert 6 == 7
assert 15 >= 16
```

## Implementation

- Added `formaltrust_platform/experiments/power_ops_evidence_bound_evaluation_setup.py`.
- Generated:
  - `docs/power_ops_action_invariance_evidence_bound_evaluation_setup_2026-07-02.md`
  - `docs/power_ops_action_invariance_evidence_bound_evaluation_setup_2026-07-02.json`
- Updated paper-draft assembly to include section `4 Evaluation Setup`.
- Updated draft consistency audit expected section list to include `evaluation_setup`.
- Added evaluation-setup JSON to `DEFAULT_WRITING_ARTIFACT_PATHS`.
- Regenerated paper draft, paper-readiness, and draft consistency audit artifacts.
- Updated README and PAPER_PLAN.

## Readback

```text
evaluation_setup: ready, paragraphs=6, expanded_cases=18, baselines=4, trace_import_cases=4, multistep_trace_cases=1, fully_supported_rows=18, forbidden_hits=0
paper_readiness: PASS, forbidden_scan_artifact_count=16, forbidden_hits=0
paper_draft: ready, sections=7, slots=abstract,introduction,related_work,method,evaluation_setup,results,limitations
draft_consistency_audit: PASS, sections=7, source_link_completeness=1.0, text_match_rate=1.0, unresolved_boundary_hits=0
```

## Verification

```text
pytest tests/test_power_ops_action_invariance.py::test_power_ops_evidence_bound_evaluation_setup_uses_dataset_trace_and_audits -q
1 passed

pytest tests/test_power_ops_action_invariance.py::test_power_ops_evidence_bound_paper_draft_assembles_ready_section_prose tests/test_power_ops_action_invariance.py::test_power_ops_paper_draft_consistency_audit_checks_sources_and_boundaries tests/test_power_ops_action_invariance.py::test_power_ops_paper_claim_readiness_default_scans_current_writing_artifacts -q
3 passed

pytest tests/test_power_ops_action_invariance.py -q
55 passed

pytest -q
255 passed
```

## Keep / Revise / Reject

keep

## Next

Iteration 167 should include the assembled 7-section paper draft in numeric-claim audit coverage.
