# Iteration 171: Paper Draft Edit Gate

## Status

complete

## Goal

Protect the paragraph evidence chain from unsynchronized direct edits by adding a hash-based gate across the assembled paper draft, claim-to-paragraph map, and reviewer-facing paragraph evidence packets.

## TDD

Added `test_power_ops_paper_draft_edit_gate_detects_stale_paragraph_artifacts` to require:

- artifact type `power_ops_paper_draft_edit_gate`;
- PASS on the current synchronized artifact chain;
- draft-to-map hash match;
- packet-to-map hash match;
- zero stale artifacts;
- FAIL when the draft changes without regenerating the paragraph map;
- FAIL when the paragraph map changes without regenerating paragraph evidence packets.

Observed red:

```text
ModuleNotFoundError: No module named 'formaltrust_platform.experiments.power_ops_paper_draft_edit_gate'
```

## Implementation

- Added `draft_content_sha256` to `formaltrust_platform/experiments/power_ops_claim_to_paragraph_map.py`.
- Added `paragraph_map_content_sha256` and carried `draft_content_sha256` into `formaltrust_platform/experiments/power_ops_paragraph_evidence_packets.py`.
- Added `formaltrust_platform/experiments/power_ops_paper_draft_edit_gate.py`.
- Regenerated:
  - `docs/power_ops_action_invariance_claim_to_paragraph_map_2026-07-02.md/json`
  - `docs/power_ops_action_invariance_paragraph_evidence_packets_2026-07-02.md/json`
  - `docs/power_ops_action_invariance_paper_draft_edit_gate_2026-07-02.md/json`
- Updated README, PAPER_PLAN, task_plan, findings, and progress.

## Readback

```text
paper_draft_edit_gate: PASS
draft_map_hash_matches=True
packet_map_hash_matches=True
stale_artifact_count=0
```

## Verification

```text
pytest tests/test_power_ops_action_invariance.py::test_power_ops_paper_draft_edit_gate_detects_stale_paragraph_artifacts -q
1 passed

pytest tests/test_power_ops_action_invariance.py::test_power_ops_paper_draft_edit_gate_detects_stale_paragraph_artifacts tests/test_power_ops_action_invariance.py::test_power_ops_paragraph_evidence_packets_compress_claim_map_for_reviewers tests/test_power_ops_action_invariance.py::test_power_ops_claim_to_paragraph_map_covers_assembled_draft_sections -q
3 passed

pytest tests/test_power_ops_action_invariance.py -q
59 passed

pytest -q
259 passed
```

## Keep / Revise / Reject

keep

## Next

Iteration 172 should export the assembled bounded draft into an evidence-bound LaTeX manuscript skeleton with source comments and edit-gate checks.
