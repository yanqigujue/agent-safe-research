# Iteration 090: Protected-Field Outcome Table

## Goal

Make the experiment answer the paper claim at the right granularity. After Iteration 089, each row knew which protected action fields it tested. This iteration adds a table that aggregates replay outcomes by protected field, so the paper can discuss parameter, approval, risk-report, decision, and tool warrants directly.

## Updated One-Sentence Thesis

High-risk RAG-agent actions should execute only when every protected action field carries an evidence warrant proving sufficient, fresh/current, source-diverse, low-conflict support.

## Current Strongest Contributions

1. **EAIR-Bench.** Benchmark contribution: evidence-to-action admissibility over protected action fields, with row-level and field-level experiment schema.
2. **Evidence Warrant / Proof-Carrying Action.** Representation contribution: `(a, W_a)` binds action fields to replayable support obligations.
3. **WarrantGuard / EAIR-Gate.** System contribution: verifies hard action obligations, warrant sufficiency, and counter-warrants before execution.

## What Changed

- Added `artifact_summary_by_model_prompt_protected_field.json/csv/md`.
- The table groups replay outcomes by `model`, `prompt_variant`, and `protected_action_field`.
- Regenerated the dry-run prompt matrix so the table exists under `outputs/eair_prompt_protocol_matrix_dry_run/summary`.
- Updated the live runbook required artifacts so live handoff must include the protected-field table.

## Novelty Pressure Test

| Neighbor | Solves | Remaining difference |
|---|---|---|
| AttriGuard / CausalArmor | Attribute action/tool-call influence to context. | The protected-field table evaluates whether the influence is warranted for a field such as `parameters` or `risk_report`. |
| PlanGuard / PromptArmor | Check plan consistency, intent/parameter deviations, and prompt-injection defenses. | The table asks whether the parameter/approval/risk-report field is evidence-admissible, not only instruction-consistent. |
| AIRGuard / Agent-Sentry / AgentSentry | Enforce authority and execution provenance. | The table can show allowed-tool/no-tool cases that still fail evidence warrants. |
| RAGForensics / RAGChecker / ARES | Diagnose RAG source/answer quality and faithfulness. | The table measures action-field warrant validity, including parameters and risk reports. |

## Rejection Simulation

| Rejection | Current answer |
|---|---|
| This is just source attribution. | The field table reports warrant outcomes for action fields, not only source responsibility. |
| This is just access control. | `parameters` rows expose hijacks where access control permits or replaces but WarrantGuard still records warrant failure. |
| This is just RAG faithfulness. | The `parameters` row for `parameter_level_hijack` directly targets action-parameter risk. |
| The benchmark is synthetic and overfitted. | The table makes the live matrix auditable by field, but current evidence remains dry-run until live provider transcripts exist. |
| The method has too many hand-designed rules. | The table is a reporting aggregation over protected fields, not another rule module. |
| Novelty over PlanGuard/AttriGuard is unclear. | The comparison object is now concrete: protected-field warrant validity under the same prompt matrix. |

## Current Most Dangerous Rejection Risk

The protected-field table is currently dry-run evidence. A reviewer can still reject live-model claims unless the same table is produced by a reportable live run.

## Claim-to-Artifact Map

| Claim | Artifact / table / test | Status |
|---|---|---|
| Replay outcomes can be aggregated by protected action field. | `artifact_summary_by_model_prompt_protected_field.json/csv/md`; `tests/test_mvp.py::test_eair_sampler_cli_writes_multi_condition_prompt_matrix_summary`. | Tested. |
| `parameters` failures answer RAG faithfulness/action-parameter risk. | `proof_carrying x parameters` row has `warrant_quality_score=0.0` and `rag_faithfulness_misses_action_parameter_risk`. | Dry-run supported. |
| Live handoff now requires the protected-field table. | `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.json`; runbook sidecar test. | Tested. |
| The verifier behavior was not changed. | Code changes only aggregate replay metrics and required artifacts. | Implementation-supported. |

## Claims Not Yet Safe To Write

- Live-model proof-carrying prompts improve protected-field warrant validity.
- WarrantGuard outperforms official AttriGuard, PlanGuard, PromptArmor, AgentSentry, CausalArmor, AIRGuard, RAGForensics, RAGChecker, or ARES.
- Real-world operational safety.
- Firstness over all action/provenance/RAG-evaluation benchmarks.

## Next Killer Experiment

Run the live prompt matrix and make the primary result table `model x prompt_variant x protected_action_field`, reporting warrant quality, candidate unsafe count, final unsafe count, influence counts, and reviewer-rejection coverage.

## Claim Boundary

This iteration adds a field-level result table and live-run required artifact. It does not add live-provider evidence or change WarrantGuard decisions.
