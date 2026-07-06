# Iteration 094: Expose Reviewer-Rejection Coverage In The Live Runbook

## Goal

Make the live prompt matrix self-explaining to reviewers. The runbook should not only list conditions; it should prove which rejection risks each condition is meant to answer.

## Updated One-Sentence Thesis

High-risk RAG-agent actions should execute only when each protected action field carries an evidence warrant whose admissibility is tested against explicit reviewer-rejection coverage: attribution, access control, RAG faithfulness, source diversity, freshness, and PlanGuard/AttriGuard novelty pressure.

## Current Strongest Contributions

1. **EAIR-Bench.** Benchmark contribution: conditions are selected and reported by reviewer-rejection coverage, not merely by attack taxonomy.
2. **Evidence Warrant / Proof-Carrying Action.** Representation contribution: `(a, W_a)` binds each protected field to replayable obligations and condition-level rejection coverage.
3. **WarrantGuard / EAIR-Gate.** System contribution: verifies field-level warrant admissibility and exports the same protected-field evidence into reportable claim chains.

## What Changed

- Added `approval_bypass::hijack_evidence_support` to the default live prompt matrix.
- The live matrix now plans 24 transcripts over 8 conditions x 3 prompt variants.
- `check_live_sampling_config`, `doctor_live_run_config`, `live_workflow_status`, and `write_live_runbook` now carry:
  - `condition_threat_model_rows`
  - `reviewer_rejection_coverage`
- The rendered live runbook now includes a `Reviewer-Rejection Coverage` table and a condition-level threat-model table.
- Regenerated `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.{md,json}`, live preflight, and workflow status artifacts.

## Novelty Pressure Test

| Neighbor | Solves | Remaining difference |
|---|---|---|
| AttriGuard / CausalArmor | Action/tool or privileged-decision causal attribution under indirect prompt injection. | The live matrix now includes both legitimate influence and hijack influence, and reports this as warrant admissibility coverage rather than causal attribution alone. |
| PlanGuard / PromptArmor | Planning-based consistency verification or prompt-injection detection/removal. | `hijack_evidence_support` is explicitly tagged for `planguard_attriguard_novelty`; the object is evidence warrant legitimacy for protected fields after action generation. |
| AIRGuard / Agent-Sentry / AgentSentry | Authority control, provenance bounds, temporal takeover, and execution integrity. | The live matrix includes allowed/no-tool failures where authority checks are insufficient. |
| RAGForensics / RAGChecker / ARES | Source traceback or retrieval/answer evaluation. | The live matrix reports action-field obligations and reviewer-rejection coverage, not only answer/context quality. |

## Rejection Simulation

| Rejection | Current answer |
|---|---|
| This is just source attribution. | Coverage includes `source_attribution_only` but pairs it with field obligations such as `legitimate_influence_separation`, `source_diverse_support`, and `fresh_current_support`. |
| This is just access control. | Coverage includes `access_control_only` across parameter hijack, insufficient evidence, and risk-report downgrade conditions. |
| This is just RAG faithfulness. | Coverage includes RAG-faithfulness pressure, but the rows target `parameters`, `risk_report`, `decision`, and `tool`. |
| The benchmark is synthetic and overfitted. | The runbook now exposes a fixed reviewer-rejection coverage map; it still requires live sampling before any result claim. |
| The method has too many hand-designed rules. | This iteration adds reporting of existing threat descriptors only; it adds no verifier rule. |
| Novelty over PlanGuard/AttriGuard is unclear. | The runbook now has an explicit `planguard_attriguard_novelty` coverage row tied to `hijack_evidence_support`. |

## Current Most Dangerous Rejection Risk

The runbook is stronger, but live-provider evidence is still absent. `OPENAI_API_KEY` is not set, so the paper can cite the 24-transcript workflow contract but not live-model results.

## Claim-to-Artifact Map

| Claim | Artifact / table / test | Status |
|---|---|---|
| The live runbook exposes reviewer-rejection coverage. | `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.md`; `tests/test_mvp.py::test_eair_prompt_protocol_live_template_reports_reviewer_rejection_coverage`. | Tested and regenerated. |
| The default live matrix covers PlanGuard/AttriGuard novelty pressure. | `approval_bypass::hijack_evidence_support` row in `condition_threat_model_rows`; coverage key `planguard_attriguard_novelty`. | Tested and regenerated. |
| The live matrix is now 8 conditions x 3 prompt variants. | `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.json`; `tests/test_mvp.py::test_eair_prompt_protocol_live_template_targets_reviewer_rejection_slice`. | Tested and regenerated. |
| Live-provider evidence is still missing. | `outputs/eair_prompt_protocol_matrix_live/live_preflight/live_run_doctor.json`; `outputs/eair_prompt_protocol_matrix_live/workflow_status/live_workflow_status.json`. | Blocked by missing `OPENAI_API_KEY`. |

## Claims Not Yet Safe To Write

- Live-model proof-carrying prompts improve protected-field warrant validity.
- WarrantGuard outperforms official AttriGuard, PlanGuard, PromptArmor, AgentSentry, CausalArmor, AIRGuard, RAGForensics, RAGChecker, or ARES.
- Real-world operational safety.
- Firstness over all action/provenance/RAG-evaluation benchmarks.
- Live prompt-matrix conclusions while the preflight blocker remains unresolved.

## Next Killer Experiment

Set `OPENAI_API_KEY`, run the 24-transcript live prompt matrix, and regenerate the reportable protected-field table plus reviewed claim bundle. The main table should stratify results by `reviewer_rejection_coverage` and protected action field.

## Claim Boundary

This iteration strengthens live experiment design and reviewer-facing coverage reporting. It does not add live-provider evidence or change WarrantGuard verifier decisions.
