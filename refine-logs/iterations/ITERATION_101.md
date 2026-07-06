# Iteration 101: Turn Closest Neighbors into Discriminator Conditions

## Goal

Reduce the most dangerous novelty ambiguity: a reviewer could still read WarrantGuard as action attribution, access control, plan checking, or RAG faithfulness with extra rules. This iteration rewrites the closest-neighbor boundary as a per-paper delta matrix and ties each delta to an EAIR-Bench discriminator condition.

## Updated One-Sentence Thesis

High-risk RAG-agent actions need proof-carrying evidence warrants, and the novelty claim should be tested by discriminator cases where attribution, plan consistency, authority control, or answer faithfulness can pass while evidence admissibility over protected action fields fails.

## Current Strongest Contributions

1. **EAIR-Bench.** A benchmark for evidence-to-action admissibility, with discriminator rows for poison-without-influence, legitimate evidence update, hijack support, stale support, single-source support, parameter hijack, insufficient evidence, and risk-report downgrade.
2. **Evidence Warrant / Proof-Carrying Action.** A representation in which action fields, arguments, approval status, risk metadata, source clusters, freshness, conflicts, and counter-evidence become a replayable execution precondition.
3. **WarrantGuard / EAIR-Gate.** A verifier pattern that treats permission and attribution as necessary diagnostics but makes execution depend on a valid evidence warrant.

## What Changed

- Replaced the broad closest-neighbor family table in `PAPER_PLAN.md` with a per-neighbor novelty delta matrix.
- Added the same reviewer-facing novelty boundary to the top of `refine-logs/FINAL_PROPOSAL.md`.
- Added a claim-to-artifact row tying closest-neighbor objections to live-matrix discriminator conditions.

## Novelty Pressure Test

| Neighbor | Solves | Does not solve | WarrantGuard delta | Discriminator |
|---|---|---|---|---|
| AttriGuard | Context/action causal attribution. | Whether influence is evidence-admissible. | Evidence warrant over protected action fields. | Paired `legitimate_evidence_update` and `parameter_level_hijack`. |
| PlanGuard | Plan and parameter consistency. | Whether a consistent action is warranted by current independent evidence. | Reject stale, single-source, conflicted, or insufficient support. | `near_duplicate_single_source_policy_support`, `stale_trusted_policy_support`. |
| PromptArmor | Prompt-injection detection and sanitization. | Replayable support for action arguments, approvals, and risk reports. | Proof-carrying action artifact. | `hijack_evidence_support` vs. `legitimate_evidence_update`. |
| AgentSentry | Temporal tracing and takeover defense. | Evidence sufficiency after authority remains intact. | High-risk decision can fail for insufficient warrant. | `insufficient_evidence_dangerous_decision`. |
| CausalArmor | Causal dominance or shielding. | Distinguishing benign from hijack influence. | Preserve legitimate influence and block hijack influence. | Populated pair table. |
| AIRGuard | Runtime authority and least privilege. | Evidence sufficiency for authorized actions. | Permission is necessary but not sufficient. | Allowed-tool stale or insufficient rows. |
| RAGForensics | Poison-source traceback. | Whether traced evidence may change action fields. | Evidence-to-action admissibility. | `poison_exposure_no_action_influence`. |
| RAGChecker / ARES | RAG relevance, faithfulness, and response quality. | Action parameters, approval flags, risk reports, execution gates. | Protected action-field warrant validity. | `parameter_level_hijack`, `risk_report_downgrade_no_tool`. |

## Rejection Simulation

| Rejection | Current answer |
|---|---|
| This is just source attribution. | The table now says exactly where attribution ends: influence can be traced but still inadmissible or legitimate. |
| This is just access control. | AIRGuard-style authority is separated from evidence warrant validity; allowed actions can fail. |
| This is just RAG faithfulness. | RAGChecker/ARES-style faithfulness is separated from action-field risk. |
| This benchmark is synthetic and overfitted. | Each discriminator is tied to a reviewer objection and must pass reportability before being cited. |
| The method has too many hand-designed rules. | Rules are verifier obligations for a named proof-carrying action pattern, not standalone novelty. |
| Novelty over PlanGuard/AttriGuard is unclear. | The closest-neighbor matrix now names the delta and required discriminator for each. |

## Current Most Dangerous Rejection Risk

The novelty boundary is now clearer in prose, but it is still not empirically defended against official implementations of AttriGuard, PlanGuard, AIRGuard, or RAG evaluation baselines. The current discriminator mapping is a protocol claim until live rows and baseline reproductions exist.

## Claim-to-Artifact Map

| Claim | Artifact / table / test | Status |
|---|---|---|
| Closest-neighbor objections map to concrete discriminator conditions. | `PAPER_PLAN.md`; `refine-logs/FINAL_PROPOSAL.md`; `examples/eair_prompt_protocol_matrix_live_template.yaml`; `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.json`. | Narrative/protocol-supported. |
| Main legitimate-vs-hijack claim requires paired rows. | `outputs/eair_warrant_reportable_export/reportable_influence_contrast_pair_table.json`; pair-table tests from Iteration 099. | Gate exists; current `total_rows=0`. |
| Dry-run influence contrast suggests the design pattern can preserve legitimate influence while blocking hijack influence. | `outputs/eair_prompt_protocol_matrix_dry_run/summary/artifact_summary_influence_contrast_table.*`. | L2 only. |
| Reviewed fixture claims remain artifact-chain claims. | `outputs/eair_warrant_reportable_export/paper_ready_claims.json`; strict seal verification artifact. | L1 only. |

## Claims Not Yet Safe To Write

- Superiority over official AttriGuard, PlanGuard, PromptArmor, AgentSentry, CausalArmor, AIRGuard, RAGForensics, RAGChecker, or ARES.
- Any official prior-work failure claim without running or citing a faithful reproduction.
- Live-model legitimate-vs-hijack separation.
- Firstness claims.
- Deployment safety.

## Next Killer Experiment

After unblocking the live matrix, report a "closest-neighbor discriminator table" whose rows are the eight planned EAIR-Bench conditions and whose columns are attribution-only, access-control, RAG-faithfulness-style, prompt/plan consistency, and WarrantGuard outcomes. The main paper claim should require that WarrantGuard is the only column that simultaneously allows legitimate evidence influence, blocks hijack influence, and rejects stale/single-source/insufficient support on paired live rows.

## Source Check

- AttriGuard: https://arxiv.org/abs/2603.10749
- PlanGuard: https://arxiv.org/abs/2604.10134
- PromptArmor: https://arxiv.org/abs/2507.15219
- CausalArmor: https://arxiv.org/abs/2602.07918
- AgentSentry: https://arxiv.org/abs/2602.22724
- AIRGuard: https://arxiv.org/abs/2605.28914
- RAGForensics: https://arxiv.org/abs/2504.21668
- RAGChecker: https://arxiv.org/abs/2408.08067
- ARES: https://arxiv.org/abs/2311.09476

## Verification

- `rg` confirms `PAPER_PLAN.md` now has `Closest-neighbor novelty delta matrix` and `refine-logs/FINAL_PROPOSAL.md` has `Reviewer-facing novelty boundary`.
- `rg` confirms the old broad closest-neighbor table is no longer present in the touched active section.
- Direct trailing-whitespace scan over `PAPER_PLAN.md`, `refine-logs/FINAL_PROPOSAL.md`, and this iteration log found no matches.
- `outputs/eair_warrant_reportable_export/reportable_influence_contrast_pair_table.json` still has `total_rows=0`, so this iteration adds no L4 empirical claim.
- `outputs/eair_prompt_protocol_matrix_live/workflow_status/live_workflow_status.json` still reports `overall_status="blocked"` at `live_preflight` because `OPENAI_API_KEY` is not set.
- No code or generated experiment artifacts were changed in this iteration.
