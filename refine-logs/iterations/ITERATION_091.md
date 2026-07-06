# Iteration 091: Make Protected-Field Results Reportable

## Goal

Move the protected-field outcome table from a diagnostic summary into the paper-citable artifact chain. A field-level table is only useful for the paper if it survives reportability gates, export integrity audit, and reviewed claim sealing.

## Updated One-Sentence Thesis

High-risk RAG-agent actions should execute only when every protected action field carries an evidence warrant proving sufficient, fresh/current, source-diverse, low-conflict support.

## Current Strongest Contributions

1. **EAIR-Bench.** Benchmark contribution: evidence-to-action admissibility over protected action fields, with reportable field-level result tables.
2. **Evidence Warrant / Proof-Carrying Action.** Representation contribution: `(a, W_a)` binds action fields to replayable support obligations.
3. **WarrantGuard / EAIR-Gate.** System contribution: verifies hard action obligations, warrant sufficiency, and counter-warrants before execution.

## What Changed

- Added `protected_field_rows` to `reportable_results_export.json`.
- Added `reportable_protected_field_table.json/csv/md`.
- Extended export integrity audit so `reportable_protected_field_table.json` must match `reportable_results_export.json`.
- Updated live runbook required artifacts to include the reportable protected-field table.
- Refreshed the fixture replay, summary, reportable export, export integrity audit, paper-ready claim audit, review declaration, and claim bundle seal.

## Novelty Pressure Test

| Neighbor | Solves | Remaining difference |
|---|---|---|
| AttriGuard / CausalArmor | Attribute action/tool-call influence to retrieved or untrusted context. | The reportable table asks whether each protected action field has an admissible warrant, not only whether context influenced it. |
| PlanGuard / PromptArmor | Check plan/instruction consistency and prompt-injection effects. | The reportable table separates instruction compliance from evidence warrant validity for fields such as `risk_report`. |
| AIRGuard / Agent-Sentry / AgentSentry | Enforce authority, provenance, and runtime control boundaries. | The reportable table can cite allowed-action failures caused by insufficient evidence support. |
| RAGForensics / RAGChecker / ARES | Diagnose source, answer, and RAG faithfulness quality. | The reportable table is action-field-level: decision/tool/risk-report warrants, not answer faithfulness alone. |

## Rejection Simulation

| Rejection | Current answer |
|---|---|
| This is just source attribution. | The reviewed claim now cites `protected_field_rows.1.warrant_quality_score`, a risk-report field result rather than a source attribution score. |
| This is just access control. | The reportable row can show WarrantGuard blocks evidence-insufficient actions even when the issue is a field warrant, not tool permission. |
| This is just RAG faithfulness. | The paper can cite field-level warrant failure for `risk_report`; future live rows can do the same for `parameters`. |
| The benchmark is synthetic and overfitted. | The reportable chain is still fixture-level; the next live run must reproduce the same protected-field table. |
| The method has too many hand-designed rules. | This iteration adds reporting and audit propagation only, not new verifier rules. |
| Novelty over PlanGuard/AttriGuard is unclear. | The reportable evidence object is now concrete: a protected-field warrant table with reviewed claims. |

## Current Most Dangerous Rejection Risk

The protected-field reportable claim is still based on the reportable fixture, not a live provider matrix. It supports the artifact-chain claim but not live-model reliability.

## Claim-to-Artifact Map

| Claim | Artifact / table / test | Status |
|---|---|---|
| Protected-field rows are part of the reportable export. | `outputs/eair_warrant_reportable_export/reportable_results_export.json`; `tests/test_mvp.py::test_eair_export_reportable_results_includes_warrant_taxonomy_columns`. | Tested and regenerated. |
| Reportable protected-field child table matches export rows. | `outputs/eair_warrant_reportable_export/reportable_protected_field_table.json`; export integrity audit; `tests/test_mvp.py::test_eair_audit_reportable_export_detects_protected_field_table_row_mismatch`. | Tested and audited. |
| A field-level claim can be reviewed and sealed. | `outputs/eair_warrant_reportable_export/paper_ready_claims.json`; `paper_ready_claim_bundle_seal/verification`. | Reviewed and verified. |
| Live handoff requires the reportable protected-field table. | `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.json`; live runbook sidecar test. | Tested and regenerated. |

## Claims Not Yet Safe To Write

- Live-model proof-carrying prompts improve protected-field warrant validity.
- WarrantGuard outperforms official AttriGuard, PlanGuard, PromptArmor, AgentSentry, CausalArmor, AIRGuard, RAGForensics, RAGChecker, or ARES.
- Real-world operational safety.
- Firstness over all action/provenance/RAG-evaluation benchmarks.

## Next Killer Experiment

Run the live prompt matrix and make `reportable_protected_field_table.*` the primary paper table: compare proof-carrying prompts against legacy action-only prompts by protected field, especially `parameters`, `requires_human_approval`, and `risk_report`.

## Claim Boundary

This iteration strengthens reportability and claim sealing. It does not add live-provider evidence or change WarrantGuard verifier decisions.
