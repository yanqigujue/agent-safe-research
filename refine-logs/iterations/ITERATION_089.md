# Iteration 089: Make the Live Matrix Claim-Driven

## Goal

Turn the threat model from prose into an experiment schema. Each prompt-matrix row must now state which protected action field is under attack, which warrant obligation should pass or fail, and which reviewer rejection the row is meant to answer.

## Updated One-Sentence Thesis

High-risk RAG-agent actions should execute only when every protected action field carries an evidence warrant proving sufficient, fresh/current, source-diverse, low-conflict support.

## Current Strongest Contributions

1. **EAIR-Bench.** Benchmark contribution: evidence-to-action admissibility over protected action fields, now exposed as row-level experiment schema.
2. **Evidence Warrant / Proof-Carrying Action.** Representation contribution: `(a, W_a)` binds action fields to replayable support obligations.
3. **WarrantGuard / EAIR-Gate.** System contribution: verifies hard action obligations, warrant sufficiency, and counter-warrants before execution.

## What Changed

- Added `ThreatModelDescriptor` coverage for each EAIR-Bench condition.
- Added `protected_action_fields`, `warrant_obligations`, and `reviewer_rejections_answered` to sampled transcripts and replay rows.
- Aggregated the same schema into replay summaries and model x prompt x condition summary tables.
- Regenerated `outputs/eair_prompt_protocol_matrix_dry_run`.

## Novelty Pressure Test

| Neighbor | Solves | Remaining difference |
|---|---|---|
| AttriGuard / CausalArmor | Action or tool-call causal attribution. | The matrix now labels whether influence is legitimate or hijack relative to protected action-field warrant obligations. |
| PlanGuard / PromptArmor | Plan consistency, parameter deviation checks, and IPI defenses. | The row schema asks whether the parameter, approval, or risk-report field is warranted by evidence, not only whether the plan obeys instructions. |
| AIRGuard / Agent-Sentry / AgentSentry | Authority, provenance, and runtime takeover controls. | The row schema separates allowed actions from evidence-insufficient actions. |
| RAGForensics / RAGChecker / ARES | Source traceback, RAG diagnostics, and faithfulness-style evaluation. | The row schema names action fields and warrant obligations, including parameter and risk-report failures. |

## Rejection Simulation

| Rejection | Current answer |
|---|---|
| This is just source attribution. | Each row names the protected action field and warrant obligation, not only responsible sources. |
| This is just access control. | Rows such as `parameter_level_hijack` and `risk_report_downgrade_no_tool` are allowed-tool or no-tool cases that still fail evidence warrants. |
| This is just RAG faithfulness. | Rows now explicitly label `parameters`, `risk_report`, and `requires_human_approval` as evaluated fields. |
| The benchmark is synthetic and overfitted. | The schema forces live/dry-run rows to declare which claim they test; it does not by itself prove external realism. |
| The method has too many hand-designed rules. | The new labels are experiment obligations derived from protected fields, not extra verifier modules. |
| Novelty over PlanGuard/AttriGuard is unclear. | The row schema gives the closest-neighbor comparison a concrete object: action-field warrant admissibility. |

## Current Most Dangerous Rejection Risk

The benchmark may still look synthetic unless the next live matrix uses this schema with fixed scenarios, held-out prompt variants, and reportability gates.

## Claim-to-Artifact Map

| Claim | Artifact / table / test | Status |
|---|---|---|
| Every sampled prompt-matrix transcript can carry action-field threat-model labels. | `formaltrust_platform/experiments/eair_bench.py`; `tests/test_mvp.py::test_eair_sampler_cli_expands_prompt_variants_for_dry_run`. | Tested. |
| Replay reports expose the same labels at row level. | `outputs/eair_prompt_protocol_matrix_dry_run/replay/structured_action_transcript_replay_report.md`. | Regenerated dry-run artifact. |
| Model x prompt x condition summaries expose protected-field, obligation, and rejection coverage counts. | `outputs/eair_prompt_protocol_matrix_dry_run/summary/artifact_summary_by_model_prompt_condition.csv`; `tests/test_mvp.py::test_eair_sampler_cli_writes_multi_condition_prompt_matrix_summary`. | Tested and regenerated. |
| `parameter_level_hijack` specifically tests parameter/risk/approval warrant failures. | `artifact_summary.json` shows `parameters`, `parameter_claim_support`, and `rag_faithfulness_misses_action_parameter_risk` for that row. | Dry-run supported. |

## Claims Not Yet Safe To Write

- Live-model warrant reliability.
- Real-world deployment safety.
- Official failures of AttriGuard, PlanGuard, PromptArmor, AgentSentry, CausalArmor, AIRGuard, RAGForensics, RAGChecker, or ARES.
- Firstness over all RAG-agent security or provenance benchmarks.

## Next Killer Experiment

Run the live prompt matrix under this fixed schema and report, for each protected field, whether proof-carrying prompts improve warrant validity without overblocking legitimate evidence influence.

## Claim Boundary

This iteration makes the experiment schema claim-driven and regenerates a dry-run matrix. It does not add live-provider evidence.
