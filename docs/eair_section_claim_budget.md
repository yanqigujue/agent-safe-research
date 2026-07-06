# EAIR Section Claim Budget

This file is the main-body drafting budget for **WarrantGuard: Evidence Warrants for High-Risk RAG-Agent Actions**. It says what each section may claim, what evidence it must cite, what must move to appendix, and what must be deleted.

Use with:

- `docs/eair_front_matter_kernel.md` for title, abstract, and introduction wording.
- `docs/eair_design_pattern_spine.md` for Figure 1 and Algorithm 1.
- `docs/eair_related_work_positioning.md` for novelty boundaries.
- `docs/eair_experiment_spine.md` for main-results table admission.
- `docs/eair_claim_ledger.md` for evidence tiers.

## Paper Type

Until live L4 evidence exists, write the main paper as:

```text
Benchmark + representation + reference verifier + artifact-chain readiness paper.
```

Do not write it as:

```text
Live empirical superiority paper.
```

## Updated One-Sentence Thesis

High-risk RAG-agent actions should carry an evidence warrant because the safety question is not merely whether evidence was cited, a tool was permitted, an answer was faithful, evidence force was calibrated, environment state was grounded, or a certificate exists, but whether evidence carries an in-scope capability for each protected action field.

## Section Budget

| Section | Purpose | Allowed claims | Required evidence | Forbidden claims |
|---|---|---|---|---|
| Abstract | State the object and evidence boundary. | WarrantGuard proposes proof-carrying actions with field-level evidence warrants; current artifacts are L1/L2; live L4 is pending. | `docs/eair_front_matter_kernel.md`; `docs/eair_claim_ledger.md`; live workflow status. | Live model behavior, official baseline wins, deployment safety, firstness. |
| 1. Introduction | Make the missing question obvious. | High-risk RAG agents act, not just answer; permission, attribution, faithfulness, force calibration, grounding, and generic certification do not decide evidence capabilities for protected action fields. | `docs/eair_design_pattern_spine.md`; `figures/fig1_eair_main_chain.svg`. | "Existing systems fail" or "WarrantGuard solves agent safety." |
| 2. Related Work | Position the object, not superiority. | PCAA, FORCEBENCH, EnvTrustBench, Prism-Reranker, MiniScope, ToolPrivBench, Causality Laundering/ARM, AttriGuard, PlanGuard, PromptArmor, AgentSentry, CausalArmor, AIRGuard, RAGForensics, RAGChecker, and ARES are close or complementary neighbors. | `docs/eair_related_work_positioning.md`; source anchors. | Prior-work failure, official implementation comparisons, first benchmark claims. |
| 3. Threat Model | Define the attack surface. | Attacker controls retrieved/stale/source-collapsed/conflicting evidence or tool descriptions, not model weights, WarrantGuard, or claim seals. | `docs/eair_threat_model_kernel.md`; live runbook condition descriptors. | Deployment guarantees or unrestricted adversary claims. |
| 4. Evidence Warrant | Define the paper object. | `(a, W_a)` carries protected fields and evidence field capabilities: required claims, support paths, freshness, conflicts, and hard obligations. | `docs/eair_warrant_formalism_kernel.md`; `docs/eair_design_pattern_spine.md`; `docs/eair_innovation_pressure_test.md`. | `HardGate`, `EvidenceSufficient`, or scores as standalone novelty. |
| 5. EAIR-Bench | Define benchmark rows. | Rows test field-scoped evidence capabilities: legitimate, hijack, insufficient, stale, source-collapsed, conflict-heavy, and no-action influence. | `docs/eair_experiment_spine.md`; `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.json`. | Benchmark realism or official baseline failures. |
| 6. WarrantGuard | Define the reference verifier. | WarrantGuard verifies field-level evidence capabilities and routes fail cases to block, replace, or review. | `docs/eair_warrant_formalism_kernel.md`; `formaltrust_platform/experiments/eair_bench.py`; tests. | Universal safety, better access control, or score-as-proof language. |
| 7. Experiments | Report only claim-serving artifacts. | L1 reviewed fixture packets, L1 offline pair readiness, L2 dry-run contrast, and live workflow blocked status. | `outputs/eair_warrant_reportable_export/paper_ready_claims.json`; `outputs/eair_warrant_pair_reportable_export/reportable_influence_contrast_pair_table.json`; dry-run contrast table; live status JSON. | L3/L4 live claims, official baseline wins, leaderboard safety claims. |
| 8. Limitations | Make claim boundaries defensible. | No live-provider L4 yet; no official prior-work baselines; benchmark realism not proven; deployment safety out of scope. | `docs/eair_claim_ledger.md`; `docs/eair_live_killer_experiment_contract.md`. | Softening limitations into future-work optimism. |

## Required Section-To-Artifact Matrix

| Claim | Section | Current tier | Artifact |
|---|---|---|---|
| The paper object is field-scoped evidence capability for protected high-risk action fields. | Abstract, Intro, Method | L0 | `docs/eair_claim_ledger.md`; `docs/eair_warrant_formalism_kernel.md`; `docs/eair_innovation_pressure_test.md` |
| Figure 1 teaches "Retrieved evidence is not context; it is a bounded capability to change fields." | Intro, Method | L0 | `figures/fig1_eair_main_chain.svg`; `docs/eair_design_pattern_spine.md` |
| The threat model targets evidence-to-action hijack, not generic RAG poisoning. | Threat Model | L0 | `docs/eair_threat_model_kernel.md` |
| EAIR-Bench rows are labeled by capability-bearing vs hijack-style influence over protected fields. | EAIR-Bench | L0/protocol | `docs/eair_experiment_spine.md`; live runbook |
| The reviewed fixture packet can carry closest-neighbor discriminator rows. | Experiments | L1 | `outputs/eair_warrant_reportable_export/paper_ready_claims.json` |
| The offline paired fixture records legitimate quality `1.0`, hijack quality `0.0`, and gap `1.0`. | Experiments | L1 fixture only | `outputs/eair_warrant_pair_reportable_export/reportable_influence_contrast_pair_table.json` |
| Dry-run proof-carrying prompts can rehearse legitimate-update vs parameter-hijack contrast. | Experiments | L2 dry-run only | `outputs/eair_prompt_protocol_matrix_dry_run/summary/artifact_summary_influence_contrast_table.json` |
| Live WarrantGuard distinction is blocked. | Abstract, Results, Limitations | Boundary | `outputs/eair_prompt_protocol_matrix_live/workflow_status/live_workflow_status.json` |

## Table Budget For Main Paper

Main text should contain only tables that carry the thesis.

| ID | Main text or appendix | Purpose |
|---|---|---|
| Figure 1 | Main | Design pattern: evidence -> `(a, W_a)` -> WarrantGuard -> execution decision. |
| Table 1 | Main | Threat model and protected fields. |
| Table 2 | Main | Closest-neighbor delta, including FORCEBENCH as cited-RAG warrant-strength pressure. |
| Table 3 | Main | Warrant object and field-level validity semantics. |
| Table 4 | Main | Claim-serving artifact chain: L1 fixture, L1 offline pair, L2 dry-run, live blocked. |
| Table 5 | Main or appendix | Live promotion contract if page budget allows; otherwise appendix with one paragraph in main text. |
| Leaderboards | Appendix | Diagnostic ranking only. |
| Prompt-adherence and protocol-legitimacy tables | Appendix | Reproducibility support only. |
| Hash seals and claim-audit internals | Appendix | Audit support only. |

## Novelty Pressure Update

FORCEBENCH / "Relevant Is Not Warranted" is a useful new pressure source because it argues that relevant cited sources can under-warrant over-strong RAG claims. EnvTrustBench is similarly dangerous because it targets overtrust in stale, incorrect, or malicious environment evidence. These are close in vocabulary and motivation, but their objects are not field-capability consumption for high-risk action execution.

Safe delta:

```text
FORCEBENCH asks whether a cited passage warrants a textual claim.
EnvTrustBench asks whether agent behavior tracks true environment evidence.
WarrantGuard asks whether retrieved evidence carries capabilities for action
fields such as parameters, approval, risk level, and risk report before execution.
```

Do not claim FORCEBENCH or EnvTrustBench fail on EAIR-Bench. Treat them as supporting evidence that "relevant/cited/grounded" is weaker than "field-capability-bearing," then narrow our object to proof-carrying high-risk actions.

## Rejection Simulation

| Rejection | Section-level repair |
|---|---|
| "This is just source attribution." | Related Work and Method must distinguish influence tracing from field capability for protected fields. |
| "This is just access control." | Threat Model and WarrantGuard sections must cover authorized/no-tool actions with invalid warrants. |
| "This is just RAG faithfulness." | EAIR-Bench and Experiments must foreground `parameters`, `requires_human_approval`, `risk_level`, and `risk_report`, not answer text. |
| "This benchmark is synthetic and overfitted to the method." | Experiments must label current evidence as L1/L2 and route realism/generalization language to the live L4 promotion contract. |
| "The method has too many hand-designed rules." | Method must present one warrant object and one Algorithm 1; individual checks are field obligations. |
| "The novelty over PlanGuard/AttriGuard is unclear." | Related Work must state that plan consistency and attribution can both hold while field capability fails. |

## Claims That Must Not Enter Main Text

- WarrantGuard outperforms official PCAA, AttriGuard, PlanGuard, PromptArmor, AgentSentry, CausalArmor, AIRGuard, RAGForensics, RAGChecker, ARES, FORCEBENCH, PRE/RHE, or RAGAS-style implementations.
- FORCEBENCH, PCAA, AttriGuard, PlanGuard, or AIRGuard fail on EAIR-Bench.
- The offline pair is live-provider evidence.
- The live matrix has produced L3/L4 rows.
- EAIR-Bench is realistic, representative, or deployment-proven.
- WarrantGuard solves agent safety or proves deployment safety.
- `warrant_quality_score` is a safety proof.

## Next Killer Experiment

The next experiment remains one smallest live table, not a broader system:

```text
same model x prompt_variant
  legitimate_evidence_update -> valid warrant -> execute/allow
  parameter_level_hijack     -> invalid warrant -> block/replace/review
  positive warrant_quality_gap
  reportability + reviewed claim seal
```

If this fails, the paper should stay a benchmark/design/artifact-chain paper and state the failure as a diagnostic, not hide it with aggregate leaderboards.

## Source Anchors

- PCAA: https://arxiv.org/abs/2606.04104
- Proof-Carrying Certificates for LLM Pipelines: https://arxiv.org/abs/2605.16407
- Confused Deputy / capability security: https://dl.acm.org/doi/10.1145/54289.871709
- Towards Verifiably Safe Tool Use for LLM Agents: https://arxiv.org/abs/2601.08012
- AttriGuard: https://arxiv.org/abs/2603.10749
- PlanGuard: https://arxiv.org/abs/2604.10134
- PromptArmor: https://arxiv.org/abs/2507.15219
- AgentSentry: https://arxiv.org/abs/2602.22724
- CausalArmor: https://arxiv.org/abs/2602.07918
- AIRGuard: https://arxiv.org/abs/2605.28914
- RAGForensics: https://arxiv.org/abs/2504.21668
- RAGChecker: https://arxiv.org/abs/2408.08067
- ARES: https://arxiv.org/abs/2311.09476
- FORCEBENCH / Relevant Is Not Warranted: https://arxiv.org/abs/2605.28044
- EnvTrustBench: https://arxiv.org/abs/2605.08828
- Prism-Reranker: https://arxiv.org/abs/2604.23734
- MiniScope: https://arxiv.org/abs/2512.11147
- ToolPrivBench / When Lower Privileges Suffice: https://arxiv.org/html/2606.20023
- Causality Laundering / ARM: https://arxiv.org/abs/2604.04035
