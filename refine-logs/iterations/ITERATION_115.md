# Iteration 115 - Claim-Driven Experiment Spine

## Goal

Prevent experiment sprawl by defining which tables are allowed in the main paper and which artifacts must stay appendix-only unless they directly answer a reviewer objection.

## Updated One-Sentence Thesis

High-risk RAG-agent actions need proof-carrying evidence warrants because permission, attribution, and answer faithfulness do not decide whether evidence may legitimately influence protected action fields.

## Current Strongest Contribution List

1. **EAIR-Bench.** A benchmark for evidence-to-action admissibility over protected fields, organized around legitimate influence, hijack influence, evidence insufficiency, freshness, source diversity, and conflict.
2. **Evidence Warrant / Proof-Carrying Action.** A representation `(a, W_a)` where `W_a` records the protected fields, required claims, support paths/source clusters, freshness/currentness, conflicts/counter-evidence, and hard obligations for a high-risk action.
3. **WarrantGuard / EAIR-Gate.** A verifier design pattern: retrieved evidence -> proof-carrying action -> field-level warrant validation -> execute, block, replace, or route to review.

## What Changed

- Added `docs/eair_experiment_spine.md`, a main-results admission rule rather than a new method module.
- Updated `PAPER_PLAN.md`, `refine-logs/FINAL_PROPOSAL.md`, and `docs/warrantguard_paper_kernel.md` to require the experiment spine before promoting tables into the main paper.
- Demoted leaderboards, model-condition summaries, prompt-adherence tables, and hash/audit internals to appendix-only unless a claim directly depends on them.

## Novelty Pressure Test

| Neighbor | What it solves | What it does not solve | Experiment-spine delta |
|---|---|---|---|
| PCAA | Runtime-neutral proof-carrying action certificates and governance checkpoints. | RAG evidence admissibility for protected action fields. | The PCAA discriminator row must test certificate-shaped actions whose evidence warrant is stale, insufficient, source-collapsed, or conflict-heavy. |
| AttriGuard | Causal attribution of tool invocations under indirect prompt injection. | Whether attributed evidence should be allowed to change protected fields. | The main pair must allow legitimate evidence update while blocking parameter/risk hijack. |
| PlanGuard | Planning-based consistency verification. | Whether a plan-consistent action is warranted by current independent evidence. | PlanGuard pressure is answered only if a plan-consistent or attributable action still fails invalid warrant obligations. |
| PromptArmor | Prompt-injection detection/removal. | Replayable action-field support after the action is emitted. | Prompt-contamination rows are not enough; main rows must show field-level warrant validity. |
| AgentSentry | Temporal causal takeover and context purification. | Evidence sufficiency for authorized high-risk decisions. | The spine keeps takeover/provenance as neighbor context, while measuring evidence-to-action admissibility. |
| CausalArmor | Causal ablation and dominance-style defense. | Preserving legitimate influence while blocking unsupported influence through explicit evidence obligations. | The central metric is the legitimate-vs-hijack warrant-quality gap, not blanket influence suppression. |
| AIRGuard | Runtime authority control and least privilege. | Whether an authorized action has sufficient, fresh, source-diverse, low-conflict evidence. | Access-control objections require authorized/no-tool rows with invalid warrants. |
| RAGForensics | Poison-source traceback in RAG. | Whether a traced source may change a protected action field. | Source tracing is not enough; rows must classify poison exposure, source collapse, or stale support by action-field effect. |
| RAGChecker | Fine-grained RAG retrieval/generation diagnostics. | Action parameters, approval, risk reports, and execution gates. | Parameter/risk-report rows are mandatory for any faithfulness contrast. |
| ARES | Automated RAG evaluation of context relevance, answer faithfulness, and answer relevance. | Evidence-to-action legitimacy and hard action obligations. | The evaluated object is a proof-carrying action, not an answer. |

## Rejection Simulation

| Rejection | Experiment-spine response |
|---|---|
| "This is just source attribution." | Main rows must include an admissibility decision, protected fields, and downgrade rule; attribution-only rows are not sufficient. |
| "This is just access control." | Main rows must include authorized/no-tool actions whose risk report, parameters, or evidence sufficiency fail. |
| "This is just RAG faithfulness." | Main rows must include parameter, approval, risk-level, and risk-report fields, not only answer text. |
| "This benchmark is synthetic and overfitted to the method." | Current fixture claims remain L1; the live matrix must include complete coverage, source-collapse rows, and downgrade rules before realism language is allowed. |
| "The method has too many hand-designed rules." | The spine presents one object, the evidence warrant; `HardGate`, `EvidenceSufficient`, scores, and audits are obligations/diagnostics around that object. |
| "The novelty over PlanGuard/AttriGuard is unclear." | The spine requires closest-neighbor rows: attribution can be present, and a plan can be consistent, while the action still fails evidence-warrant admissibility. |

## Most Dangerous Rejection Risk

The most dangerous risk is that the results section becomes an artifact inventory. If the paper reports leaderboards, prompt-adherence audits, and aggregate tables without mapping them to reviewer objections, reviewers will see a hand-designed rules stack rather than a memorable design pattern. The new spine forces the main text back to three objects: benchmark, warrant, gate.

## Claim-to-Artifact Map

| Claim | Status | Artifact/table/test |
|---|---|---|
| Main-paper tables must answer reviewer objections through protected action fields. | Safe L0. | `docs/eair_experiment_spine.md` |
| Current evidence is L1/L2, not L3/L4. | Safe boundary claim. | `docs/eair_claim_ledger.md`; `outputs/eair_prompt_protocol_matrix_live/workflow_status/live_workflow_status.json` |
| Offline paired fixture records gap `1.0`. | Safe L1 fixture claim. | `outputs/eair_warrant_pair_reportable_export/reportable_influence_contrast_pair_table.json`; `paper_ready_claims.json` |
| Dry-run proof-carrying prompts rehearse legitimate-update vs parameter-hijack contrast. | Safe L2 dry-run claim. | `outputs/eair_prompt_protocol_matrix_dry_run/summary/artifact_summary_influence_contrast_table.json` |
| Live matrix maps objections to conditions and protected fields. | Safe protocol claim only. | `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.json` |
| Live-provider WarrantGuard distinction. | Not safe. | Missing L4 reportable paired live rows and strict reviewed seal. |

## Claims That Still Cannot Be Written

- WarrantGuard outperforms official AttriGuard, PlanGuard, PromptArmor, AgentSentry, CausalArmor, AIRGuard, RAGForensics, RAGChecker, ARES, PRE, RHE, or RAGAS-style implementations.
- The offline pair is live-provider evidence.
- Aggregate leaderboards prove safety.
- EAIR-Bench is realistic or non-overfit beyond fixture/dry-run support.
- PCAA, AttriGuard, PlanGuard, or AIRGuard fail on EAIR-Bench.

## Next Killer Experiment

Run the locked 8-condition x 3-prompt live matrix after `OPENAI_API_KEY` is available, then promote only the smallest table that passes the spine:

```text
objection -> nearest neighbor -> live condition(s) -> protected fields
          -> reportable artifact -> allowed claim -> downgrade if failed
```

The killer row is the same-model `proof_carrying` or `proof_carrying_strict` pair: allow `policy_update::legitimate_evidence_update`, block `parameter_setting::parameter_level_hijack`, and seal the positive `warrant_quality_gap`.

## Source Check

- PCAA: https://arxiv.org/abs/2606.04104
- AttriGuard: https://arxiv.org/abs/2603.10749
- PlanGuard: https://arxiv.org/abs/2604.10134
- PromptArmor: https://arxiv.org/abs/2507.15219
- AgentSentry: https://arxiv.org/abs/2602.22724
- CausalArmor: https://arxiv.org/abs/2602.07918
- AIRGuard: https://arxiv.org/abs/2605.28914
- RAGForensics: https://arxiv.org/abs/2504.21668
- RAGChecker: https://arxiv.org/abs/2408.08067
- ARES: https://arxiv.org/abs/2311.09476

## Verification

- Passed: experiment-spine pointer search confirms `docs/eair_experiment_spine.md` is referenced from `docs/warrantguard_paper_kernel.md`, `PAPER_PLAN.md`, and `refine-logs/FINAL_PROPOSAL.md`.
- Passed: source/artifact guardrail search confirms the new spine preserves appendix-only leaderboards, official-baseline no-claim boundaries, and L4/live-provider blocking language.
- Passed: live blocked-status check confirms `overall_status = blocked`, `blocked_stage = live_preflight`, `api_key_env = OPENAI_API_KEY`, and `api_key_env_present = false`.
- Passed: trailing whitespace scan returned no matches.
- Passed: `git diff --check -- docs\eair_experiment_spine.md docs\warrantguard_paper_kernel.md PAPER_PLAN.md refine-logs\FINAL_PROPOSAL.md refine-logs\iterations\ITERATION_115.md`.
- Passed: `pytest -q` reports `122 passed`.
