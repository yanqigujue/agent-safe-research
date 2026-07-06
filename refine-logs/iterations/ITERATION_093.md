# Iteration 093: Lock The Live Matrix To Reviewer-Rejection Conditions

## Goal

Replace the old 3-condition live prompt matrix with a decisive reviewer-rejection slice. The next live run should answer the paper's core objections directly instead of sampling a convenient smoke test.

## Updated One-Sentence Thesis

High-risk RAG-agent actions should execute only when every protected action field carries a warrant whose evidence is admissible under sufficiency, freshness/currentness, source diversity, and low-conflict obligations.

## Current Strongest Contributions

1. **EAIR-Bench.** Benchmark contribution: conditions are selected by reviewer-rejection pressure, not by generic attack coverage.
2. **Evidence Warrant / Proof-Carrying Action.** Representation contribution: `(a, W_a)` makes each protected field cite support obligations that can fail independently from prompt adherence, attribution, authority, or answer faithfulness.
3. **WarrantGuard / EAIR-Gate.** System contribution: verifies field-level warrant admissibility and exports the same protected-field rows into reportable claims.

## What Changed

- Updated `examples/eair_prompt_protocol_matrix_live_template.yaml` from 3 scenarios to 7 decisive scenarios:
  - `approval_bypass::poison_exposure_no_action_influence`
  - `policy_update::legitimate_evidence_update`
  - `parameter_setting::parameter_level_hijack`
  - `dispatch_control::insufficient_evidence_dangerous_decision`
  - `policy_update::near_duplicate_single_source_policy_support`
  - `policy_update::stale_trusted_policy_support`
  - `approval_bypass::risk_report_downgrade_no_tool`
- Added a regression test requiring the default live matrix to expose those 7 conditions and plan 21 transcripts.
- Regenerated `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.{md,json}`.
- Regenerated live preflight/status artifacts; the workflow remains blocked because `OPENAI_API_KEY` is not set.
- Updated `PAPER_PLAN.md` and `refine-logs/FINAL_PROPOSAL.md` so the active proposal points to the 21-transcript decisive slice.

## Novelty Pressure Test

| Neighbor | Solves | Remaining difference |
|---|---|---|
| AttriGuard / CausalArmor | Action/tool or privileged-decision causal attribution against untrusted context. | The live slice includes legitimate influence, source diversity, stale support, and field-level warrant failures, not only untrusted dominance. |
| PlanGuard / PromptArmor | Plan consistency, hard constraints, intent/parameter verification, and prompt-injection removal. | The live slice asks whether action fields are evidence-admissible even when the prompt protocol or plan is followed. |
| AIRGuard / Agent-Sentry / AgentSentry | Authority control, provenance bounds, or temporal causal takeover mitigation. | The live slice includes allowed/no-tool actions that can still fail evidence sufficiency or risk-report warrant obligations. |
| RAGForensics / RAGChecker / ARES | Poison traceback and RAG retrieval/answer evaluation. | The live slice evaluates decision/tool/parameter/approval/risk-report warrant validity rather than answer faithfulness or poisoned-text localization. |

## Rejection Simulation

| Rejection | Current answer |
|---|---|
| This is just source attribution. | The live matrix now includes legitimate evidence influence and near-duplicate/stale support, forcing the result to judge admissible support, not only source responsibility. |
| This is just access control. | The slice includes allowed/no-tool failures: insufficient evidence and risk-report downgrade. |
| This is just RAG faithfulness. | The slice includes `parameter_level_hijack` and `risk_report_downgrade_no_tool`, which are action-field failures. |
| The benchmark is synthetic and overfitted. | The fixed live matrix is still not live evidence until API-key sampling succeeds, but its conditions are now tied to reviewer objections instead of method convenience. |
| The method has too many hand-designed rules. | This iteration changes the live experiment contract only; it adds no verifier rules. |
| Novelty over PlanGuard/AttriGuard is unclear. | The decisive slice now explicitly covers cases where plan consistency or causal attribution is adjacent but not identical to warrant admissibility. |

## Current Most Dangerous Rejection Risk

The live experiment is still blocked at preflight because `OPENAI_API_KEY` is not set. The paper can cite the locked live workflow contract, not live-model results.

## Claim-to-Artifact Map

| Claim | Artifact / table / test | Status |
|---|---|---|
| The default live matrix targets the reviewer-rejection slice. | `examples/eair_prompt_protocol_matrix_live_template.yaml`; `tests/test_mvp.py::test_eair_prompt_protocol_live_template_targets_reviewer_rejection_slice`. | Tested. |
| The live runbook plans the same 7-condition x 3-prompt workflow. | `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.json`. | Regenerated. |
| The workflow still has no live-provider evidence. | `outputs/eair_prompt_protocol_matrix_live/live_preflight/live_run_doctor.json`; `outputs/eair_prompt_protocol_matrix_live/workflow_status/live_workflow_status.json`. | Blocked by missing `OPENAI_API_KEY`. |
| The live table can feed field-level reviewed claims after sampling. | `outputs/eair_warrant_reportable_export/paper_ready_claim_audit/reportable_claim_citation_audit.md`; Iteration 092 claim-template test. | Artifact-chain supported, not live-supported. |

## Claims Not Yet Safe To Write

- Live-model proof-carrying prompts improve protected-field warrant validity.
- WarrantGuard outperforms official AttriGuard, PlanGuard, PromptArmor, AgentSentry, CausalArmor, AIRGuard, RAGForensics, RAGChecker, or ARES.
- Real-world operational safety.
- Firstness over all action/provenance/RAG-evaluation benchmarks.
- Live prompt-matrix conclusions while the preflight blocker remains unresolved.

## Next Killer Experiment

Set `OPENAI_API_KEY`, run the 21-transcript live prompt matrix, and regenerate the reportable protected-field table plus reviewed claim bundle. The main table should compare `legacy_action_only`, `proof_carrying`, and `proof_carrying_strict` across the 7 reviewer-rejection conditions.

## Claim Boundary

This iteration strengthens experiment design and reproducibility. It does not add live-provider evidence or change WarrantGuard verifier decisions.
