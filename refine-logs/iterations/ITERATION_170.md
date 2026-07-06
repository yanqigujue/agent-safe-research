# Iteration 170: Paragraph Evidence Packets

## Status

complete

## Goal

Compress the complete claim-to-paragraph map into reviewer-facing claim packets and audit source-only rows so the paragraph evidence layer is usable without reading every row manually.

## TDD

Added `test_power_ops_paragraph_evidence_packets_compress_claim_map_for_reviewers` to require:

- artifact type `power_ops_paragraph_evidence_packets`;
- PASS status on the current claim-to-paragraph map;
- reviewer packet count smaller than raw paragraph count;
- audit compression ratio above `0.5`;
- source-only rows audited;
- no source-only rows needing stronger claim binding;
- FAIL when a source-only row loses evidence refs, boundary flags, and recognizable context.

Observed red:

```text
ModuleNotFoundError: No module named 'formaltrust_platform.experiments.power_ops_paragraph_evidence_packets'
```

## Implementation

- Added `formaltrust_platform/experiments/power_ops_paragraph_evidence_packets.py`.
- Generated:
  - `docs/power_ops_action_invariance_paragraph_evidence_packets_2026-07-02.md`
  - `docs/power_ops_action_invariance_paragraph_evidence_packets_2026-07-02.json`
- Grouped paragraph rows by source claim into reviewer-facing claim packets.
- Added source-only row audit resolutions:
  - `related_work_context`
  - `evaluation_audit_context`
  - `boundary_only`
  - `needs_stronger_claim_binding`
- Updated README, PAPER_PLAN, task_plan, findings, and progress.

## Readback

```text
paragraph_evidence_packets: PASS
paragraph_count=41
claim_packet_count=11
source_only_row_count=11
source_only_packet_count=3
reviewer_packet_count=14
audit_compression_ratio=0.658537
needs_stronger_binding_count=0
boundary_only_source_row_count=7
forbidden_hits=0
```

## Verification

```text
pytest tests/test_power_ops_action_invariance.py::test_power_ops_paragraph_evidence_packets_compress_claim_map_for_reviewers -q
1 passed

pytest tests/test_power_ops_action_invariance.py::test_power_ops_paragraph_evidence_packets_compress_claim_map_for_reviewers tests/test_power_ops_action_invariance.py::test_power_ops_claim_to_paragraph_map_covers_assembled_draft_sections tests/test_power_ops_action_invariance.py::test_power_ops_current_numeric_audit_includes_assembled_paper_draft -q
3 passed

pytest tests/test_power_ops_action_invariance.py -q
58 passed

pytest -q
258 passed
```

## Keep / Revise / Reject

keep

## Next

Iteration 171 should add a paper-draft edit gate that marks paragraph map and packet artifacts stale when the assembled paper draft changes without regeneration.
