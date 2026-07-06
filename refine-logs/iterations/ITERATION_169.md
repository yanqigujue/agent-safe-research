# Iteration 169: Claim-to-Paragraph Map

## Status

complete

## Goal

Map every assembled paper-draft paragraph to source claims, evidence references, and forbidden-claim boundary tags so future prose edits remain paragraph-level auditable.

## TDD

Added `test_power_ops_claim_to_paragraph_map_covers_assembled_draft_sections` to require:

- artifact type `power_ops_claim_to_paragraph_map`;
- PASS status on the current assembled draft;
- all assembled draft sections represented;
- no unmapped paragraph rows;
- source-link and claim-or-source binding rates equal to `1.0`;
- at least one claim-mapped paragraph and at least one boundary-marked paragraph;
- FAIL when a section loses its `source_path`.

Observed red:

```text
ModuleNotFoundError: No module named 'formaltrust_platform.experiments.power_ops_claim_to_paragraph_map'
```

## Implementation

- Added `formaltrust_platform/experiments/power_ops_claim_to_paragraph_map.py`.
- Generated:
  - `docs/power_ops_action_invariance_claim_to_paragraph_map_2026-07-02.md`
  - `docs/power_ops_action_invariance_claim_to_paragraph_map_2026-07-02.json`
- The map reads the assembled paper draft, section source JSONs, claim-ledger readiness, and draft consistency audit.
- It lifts existing `paragraphs`, `sentences`, `source_claims`, `evidence_paths`, `source_refs`, `formal_refs`, and `table_refs` into paragraph rows.
- It marks boundary flags for production telemetry, operator workload, latency, official-superiority, firstness, and prompt-injection-solution exclusions.
- Updated README, PAPER_PLAN, task_plan, findings, and progress.

## Readback

```text
claim_to_paragraph_map: PASS
section_count=8
paragraph_count=41
source_link_completeness_rate=1.0
claim_or_source_binding_rate=1.0
claim_mapped_paragraph_count=30
source_mapped_paragraph_count=11
boundary_marked_paragraph_count=18
unmapped_paragraph_count=0
forbidden_hits=0
```

## Verification

```text
pytest tests/test_power_ops_action_invariance.py::test_power_ops_claim_to_paragraph_map_covers_assembled_draft_sections -q
1 passed

pytest tests/test_power_ops_action_invariance.py::test_power_ops_claim_to_paragraph_map_covers_assembled_draft_sections tests/test_power_ops_action_invariance.py::test_power_ops_current_numeric_audit_includes_assembled_paper_draft tests/test_power_ops_action_invariance.py::test_power_ops_paper_claim_readiness_default_scans_current_writing_artifacts -q
3 passed

pytest tests/test_power_ops_action_invariance.py -q
57 passed

pytest -q
257 passed
```

## Keep / Revise / Reject

keep

## Next

Iteration 170 should compress the paragraph map into reviewer-facing claim packets and audit source-only paragraphs that may need stronger claim binding or explicit boundary-only status.
