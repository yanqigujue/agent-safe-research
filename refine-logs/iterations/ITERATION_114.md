# Iteration 114 - Front-Matter Claim Firewall

## Goal

Lock the paper's title, abstract, introduction opening, and contribution preview to claim-safe wording before any full-paper draft expands beyond the current evidence boundary.

## Updated One-Sentence Thesis

High-risk RAG-agent actions should execute only when a proof-carrying action `(a, W_a)` shows that protected fields are grounded in sufficient, fresh, source-diverse, low-conflict evidence.

## Current Strongest Contribution List

1. **EAIR-Bench.** A benchmark object for evidence-to-action admissibility: rows distinguish legitimate evidence influence from hijack-style influence over protected action fields.
2. **Evidence Warrant / Proof-Carrying Action.** A representation `(a, W_a)` where the warrant records protected fields, required claims, support paths/source clusters, freshness/currentness, conflicts/counter-evidence, and hard action obligations.
3. **WarrantGuard / EAIR-Gate.** A verifier pattern that allows execution only when field-level warrant obligations pass, while treating reportability audits and claim seals as reproducibility infrastructure rather than main novelty.

## What Changed

- Added `docs/eair_front_matter_kernel.md` as the copy-facing source for the title, claim-safe abstract, introduction skeleton, contribution preview, front-matter novelty boundary, allowed result preview, forbidden claims, and source anchors.
- Updated `docs/warrantguard_paper_kernel.md`, `PAPER_PLAN.md`, and `refine-logs/FINAL_PROPOSAL.md` to point front-matter drafting to the new kernel.
- Kept live-provider language blocked: the new kernel says current support is L1/L2 only and that live distinction requires reportability plus strict reviewed sealing.

## Novelty Pressure Test

| Neighbor | Solves | Does not solve for this paper | Current delta |
|---|---|---|---|
| PCAA | Runtime-neutral proof-carrying action certificates and governance checkpoints. | RAG-specific evidence admissibility for protected action fields. | We specialize proof-carrying actions into evidence warrants for decision, parameters, approval, risk level, and risk report. |
| AttriGuard | Causal attribution of tool invocations under indirect prompt injection. | Whether attributed evidence is sufficient, fresh, source-diverse, and low-conflict for each protected field. | Attribution is an input; admissibility is the new object. |
| PlanGuard | Planning-based consistency verification against indirect prompt injection. | Field-level evidence warrant obligations for action arguments, approval, and risk reports. | The question is whether evidence may legitimately influence a field, not only whether a plan remains consistent. |
| PromptArmor | Prompt-injection detection and sanitization. | Replayable evidence support for high-risk action fields. | We verify a field-level warrant rather than only detecting contaminated prompts. |
| AgentSentry | Inference-time or provenance-style defense for compromised agent execution. | Sufficiency/freshness/source-diversity/conflict obligations per protected field. | We narrow the object to evidence-to-action admissibility. |
| CausalArmor | Causal ablation guardrails for indirect prompt injection. | Legitimate-vs-hijack evidence influence under explicit warrant obligations. | We allow legitimate evidence influence when the warrant is valid. |
| AIRGuard | Runtime authority control for side effects. | Evidence adequacy when authority exists but the supporting evidence is stale, source-collapsed, conflicted, or insufficient. | Authority and evidence admissibility are complementary checks. |
| RAGForensics | Traceback of poisoned knowledge-base texts. | Action-field warrant validity after retrieval. | We target final structured action fields, not only poison traceback. |
| RAGChecker | Fine-grained RAG retrieval/generation diagnostics. | High-risk action parameter, approval, and risk-report validity. | We move from answer diagnostics to execution-bearing action warrants. |
| ARES | Automated RAG evaluation for context relevance, answer faithfulness, and answer relevance. | Evidence-to-action legitimacy and hard action obligations. | EAIR-Bench evaluates a different output object: a proof-carrying action. |

## Rejection Simulation

| Rejection | Front-matter repair |
|---|---|
| "This is just source attribution." | The abstract now says attribution identifies influence, but WarrantGuard asks whether the influence is admissible for each protected field. |
| "This is just access control." | The introduction skeleton separates permission from evidence admissibility: an authorized action can still have unsupported or stale parameters/risk reports. |
| "This is just RAG faithfulness." | The contribution list names protected action fields and hard action obligations, not only answer-groundedness. |
| "This benchmark is synthetic and overfitted to the method." | The result preview only claims reviewed fixture readiness, closest-neighbor discriminator rows, and a live promotion contract; it does not claim benchmark realism yet. |
| "The method has too many hand-designed rules." | The design pattern is now one warrant object plus verifier obligations. `HardGate`, `EvidenceSufficient`, soft scores, and seals remain obligations/diagnostics, not separate novelty claims. |
| "The novelty over PlanGuard/AttriGuard is unclear." | The novelty table forces the delta to the object level: evidence admissibility for protected action fields, rather than planning consistency or causal attribution. |

## Most Dangerous Rejection Risk

The biggest risk is still front-matter overclaim: a reviewer may read the L1 offline pair and L2 dry-run preview as evidence that WarrantGuard has already demonstrated live-model legitimate-vs-hijack distinction. The new kernel counters this by requiring every abstract/results sentence to state that live-provider claims are blocked until the live matrix passes reportability and strict reviewed sealing.

## Claim-to-Artifact Map

| Claim | Current status | Artifact/test |
|---|---|---|
| Evidence-warrant admissibility is the paper object. | Safe L0. | `docs/eair_claim_ledger.md`, `docs/eair_threat_model_kernel.md`, `docs/eair_warrant_formalism_kernel.md` |
| The three contribution names are EAIR-Bench, Evidence Warrant / Proof-Carrying Action, and WarrantGuard / EAIR-Gate. | Safe L0. | `docs/eair_front_matter_kernel.md`, `docs/warrantguard_paper_kernel.md`, `PAPER_PLAN.md` |
| Related-work novelty boundary is object-level, not prior-work failure. | Safe L0. | `docs/eair_related_work_positioning.md`, `docs/eair_front_matter_kernel.md` |
| Reviewed fixture packets can export closest-neighbor discriminator rows. | Safe L1. | `outputs/eair_warrant_reportable_export/paper_ready_claims.json` |
| Offline paired fixture can carry legitimate quality `1.0`, hijack quality `0.0`, gap `1.0`. | Safe L1, fixture only. | `outputs/eair_warrant_pair_reportable_export/reportable_influence_contrast_pair_table.json` |
| Deterministic proof-carrying prompts can rehearse legitimate update vs parameter hijack. | Safe L2, dry-run only. | `outputs/eair_prompt_protocol_matrix_dry_run/summary/artifact_summary_influence_contrast_table.json` |
| Live-provider WarrantGuard distinction. | Not safe. | Blocked by `outputs/eair_prompt_protocol_matrix_live/workflow_status/live_workflow_status.json` |

## Claims That Still Cannot Be Written

- WarrantGuard outperforms AttriGuard, PlanGuard, PromptArmor, AgentSentry, CausalArmor, AIRGuard, RAGForensics, RAGChecker, ARES, or any official baseline.
- WarrantGuard distinguishes legitimate from hijack influence in live models.
- EAIR-Bench is realistic or non-overfit beyond current fixture/dry-run evidence.
- Evidence warrants are the first proof-carrying action mechanism.
- Access control, attribution, or RAG faithfulness systems fail on EAIR-Bench without official baseline implementation and reportable artifacts.

## Next Killer Experiment

Unblock the live prompt-protocol matrix with `OPENAI_API_KEY` and run a same-model legitimate-vs-hijack pair experiment where every row declares protected action fields, warrant obligations, nearest-neighbor rejection answered, and downgrade rule. The killer table should show whether WarrantGuard can allow legitimate evidence updates while blocking parameter/risk/approval hijacks under live-provider reportability and strict reviewed sealing.

## Source Check

- PCAA: https://arxiv.org/abs/2606.04104
- AttriGuard: https://arxiv.org/abs/2603.10749
- PlanGuard: https://arxiv.org/abs/2604.10134
- PromptArmor: https://arxiv.org/abs/2507.15219
- AgentSentry: https://arxiv.org/html/2602.22724v1
- CausalArmor: https://arxiv.org/html/2602.07918v1
- AIRGuard: https://arxiv.org/html/2605.28914v1
- RAGForensics: https://arxiv.org/html/2504.21668v2
- RAGChecker: https://arxiv.org/abs/2408.08067
- ARES: https://arxiv.org/abs/2311.09476

## Verification

- Passed: front-matter pointer search confirms `docs/eair_front_matter_kernel.md` is referenced from `docs/warrantguard_paper_kernel.md`, `PAPER_PLAN.md`, and `refine-logs/FINAL_PROPOSAL.md`.
- Passed: live blocked-status check confirms `overall_status = blocked`, `blocked_stage = live_preflight`, `api_key_env = OPENAI_API_KEY`, and `api_key_env_present = false`.
- Passed: trailing whitespace scan returned no matches.
- Passed: `git diff --check -- docs\eair_front_matter_kernel.md docs\warrantguard_paper_kernel.md PAPER_PLAN.md refine-logs\FINAL_PROPOSAL.md refine-logs\iterations\ITERATION_114.md`.
- Passed: `pytest -q` reports `122 passed`.
