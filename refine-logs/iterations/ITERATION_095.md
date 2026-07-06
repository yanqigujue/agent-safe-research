# Iteration 095: Make Reviewer-Rejection Evidence Reportable By Protected Field

## Goal

Move reviewer-rejection coverage from runbook prose into a paper-table artifact. The paper should be able to answer "just attribution / access control / faithfulness?" by pointing to `reviewer_rejection x protected_action_field` rows, not only to condition descriptions.

## Updated One-Sentence Thesis

High-risk RAG-agent actions should execute only when each protected action field carries an evidence warrant whose admissibility can be reported against explicit reviewer objections: source attribution, access control, RAG faithfulness, benchmark overfit, and novelty over causal/planning guards.

## Current Strongest Contributions

1. **EAIR-Bench.** Benchmark contribution: cases are indexed by evidence-to-action admissibility and reviewer-rejection coverage, not merely by retrieval poison or tool authorization.
2. **Evidence Warrant / Proof-Carrying Action.** Representation contribution: `(a, W_a)` binds each protected field to warrant obligations and makes action evidence support replayable.
3. **WarrantGuard / EAIR-Gate.** System contribution: verifies field-level warrant admissibility, exports reportable field tables, and now surfaces reviewer objections as auditable paper-table rows.

## What Changed

- Added `reviewer_rejection_protected_field_rows` to `reportable_results_export.json`.
- Added reportable child artifacts:
  - `reportable_reviewer_rejection_protected_field_table.json`
  - `reportable_reviewer_rejection_protected_field_table.csv`
  - `reportable_reviewer_rejection_protected_field_table.md`
- Extended `eair-audit-reportable-export` so it checks the new child table rows against the main export payload.
- Extended the live runbook required-artifact list to include the new table.
- Regenerated reportable export, integrity audit, claim audits, diagnostic seal, paper-ready reviewed claims, strict paper-ready audit, strict seal, strict seal verification, live runbook, live preflight, and workflow status.
- Updated `PAPER_PLAN.md` and `refine-logs/FINAL_PROPOSAL.md` so the main table shape is now `reviewer_rejection x protected_action_field`.

## Novelty Pressure Test

| Neighbor | Solves | Remaining difference |
|---|---|---|
| AttriGuard / CausalArmor | Causal attribution at tool/action decision points for indirect prompt injection. | Our reportable object is not just "which context caused the action"; it is whether each protected field has sufficient, fresh, source-diverse, low-conflict evidence. |
| PlanGuard / PromptArmor | Planning consistency, context isolation, prompt-injection detection/removal, and parameter-intent checks. | WarrantGuard measures whether action parameters and risk metadata are evidence-warranted, even when the plan or sanitized prompt looks valid. |
| AIRGuard / Agent-Sentry / AgentSentry | Runtime authority control, execution provenance bounds, and temporal causal takeover mitigation. | Authority/provenance can say whether an action is permitted or behaviorally bounded; WarrantGuard asks whether allowed high-risk fields are legitimately warranted by evidence. |
| RAGForensics / RAGChecker / ARES | Trace poisoned RAG sources or evaluate retrieval/answer quality. | The new table targets action fields (`decision`, `tool`, `risk_report`) under reviewer objections, not only answer faithfulness or context relevance. |

## Rejection Simulation

| Rejection | Current answer |
|---|---|
| This is just source attribution. | The new table has `source_attribution_only` rows tied to `decision`, `risk_report`, and `tool`, with warrant obligations and gate outcomes. |
| This is just access control. | The live matrix still tracks access-control-only objections, while the paper table can stratify allowed-tool failures by protected action field. |
| This is just RAG faithfulness. | RAG faithfulness neighbors evaluate answer/context quality; the reportable rows expose action-field warrant failures. |
| The benchmark is synthetic and overfitted. | Current rows remain fixture-backed, and the claim boundary says so; the same table is now ready for the locked 24-transcript live matrix. |
| The method has too many hand-designed rules. | This iteration adds no verifier rule. It only reports existing verifier outcomes in reviewer-facing table shape. |
| Novelty over PlanGuard/AttriGuard is unclear. | The artifact boundary is sharper: PlanGuard/AttriGuard pressure is not prose only; it is a reportable rejection dimension crossed with protected fields. |

## Current Most Dangerous Rejection Risk

The paper-table shape is much stronger, but the empirical claim is still blocked: the live provider workflow remains at `live_preflight` because `OPENAI_API_KEY` is not set.

## Claim-to-Artifact Map

| Claim | Artifact / table / test | Status |
|---|---|---|
| Reviewer objections can be reported by protected action field. | `outputs/eair_warrant_reportable_export/reportable_reviewer_rejection_protected_field_table.md`; `tests/test_mvp.py::test_eair_export_reportable_results_includes_warrant_taxonomy_columns`. | Tested and regenerated; fixture-backed. |
| The new reviewer-rejection child table is integrity checked. | `outputs/eair_warrant_reportable_export/integrity/reportable_export_integrity_audit.json`; `tests/test_mvp.py::test_eair_audit_reportable_export_detects_reviewer_rejection_protected_field_table_row_mismatch`. | Tested and regenerated. |
| The live runbook requires the new table before handoff. | `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.json`; `tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar`. | Tested and regenerated. |
| Existing paper-ready claim chain still passes after export drift. | `outputs/eair_warrant_reportable_export/paper_ready_claim_bundle_seal/verification/reportable_claim_bundle_seal_verification.json`. | Strict verification passes. |

## Claims Not Yet Safe To Write

- Live-model WarrantGuard reliability.
- Superiority over official AttriGuard, PlanGuard, PromptArmor, AgentSentry, Agent-Sentry, CausalArmor, AIRGuard, RAGForensics, RAGChecker, or ARES.
- Real-world deployment safety.
- Firstness over all action-provenance, RAG-evaluation, or agent-security benchmarks.
- Any conclusion from the 24-transcript live matrix until `OPENAI_API_KEY` is set and the run completes.

## Next Killer Experiment

Run the locked 24-transcript live matrix and publish the main result as `model x prompt_variant x reviewer_rejection x protected_action_field`, with companion protocol-legitimacy and paper-ready reviewed claim bundle artifacts. This is the experiment that can directly answer why PRE/RHE, attribution-only, RAG faithfulness, and access control fail different action-field risks.

## Verification

- `pytest tests\test_eair_bench.py -q`: 45 passed.
- `pytest tests\test_mvp.py -q`: 58 passed.
- `pytest -q`: 115 passed.
- `python -m compileall formaltrust_platform`: passed.
- `git diff --check -- formaltrust_platform\experiments\eair_bench.py tests\test_mvp.py PAPER_PLAN.md refine-logs\FINAL_PROPOSAL.md`: no whitespace errors; PowerShell reported the existing LF-to-CRLF warning for `tests/test_mvp.py`.

## Claim Boundary

This iteration strengthens reportability and reviewer-facing table shape. It does not add live-provider evidence and does not change WarrantGuard verifier decisions.
