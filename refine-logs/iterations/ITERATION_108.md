# Iteration 108: Compress the Claim Ledger into a Paper Kernel

## Goal

Turn the claim firewall from Iteration 107 into a paper-facing skeleton that can be used for the abstract, contribution list, threat model, results wording, section order, and figure/table plan without promoting fixture or dry-run evidence into live-provider claims.

## Updated One-Sentence Thesis

High-risk RAG-agent actions should execute only with an evidence warrant showing that protected action fields are grounded in sufficient, fresh, source-diverse, low-conflict evidence; current artifacts support this as a claim-safe design and artifact-chain contribution, while the live legitimate-vs-hijack empirical claim remains blocked.

## Current Strongest Contribution List

1. **EAIR-Bench.** A benchmark object for evidence-to-action admissibility: whether retrieved evidence may legitimately influence protected action fields.
2. **Evidence Warrant / Proof-Carrying Action.** A representation `(a, W_a)` whose warrant covers decision, tool arguments, approval status, risk level, risk report, supporting claims, source clusters, freshness, conflicts, and hard obligations.
3. **WarrantGuard / EAIR-Gate.** A verifier pattern: retrieve evidence, emit proof-carrying action, verify the warrant, then execute, block, replace, or route to review.

## What Changed

- Added `docs/warrantguard_paper_kernel.md`.
- The kernel contains a claim-safe abstract draft, the compressed three-part contribution list, the current threat model, the design pattern, allowed and forbidden result sentences, a section skeleton, and a figure/table plan.
- Updated `PAPER_PLAN.md` and `refine-logs/FINAL_PROPOSAL.md` so drafting starts from the kernel plus the ledger, not from older EAIR-only framing.

## Novelty Pressure Test

| Neighbor | What it solves | What it does not solve | Current WarrantGuard boundary |
|---|---|---|---|
| PCAA | Runtime-neutral proof-carrying action certificates and governance checkpoints. | RAG-specific evidence admissibility for action parameters, approvals, freshness, source diversity, and risk reports. | Safe delta: specialize proof-carrying actions into evidence warrants. Unsafe claim: generic PCAA firstness or PCAA failure. |
| AttriGuard | Action-level causal attribution for tool calls under indirect prompt injection. | Whether the attributed influence is admissible evidence for protected action fields. | Safe delta: admissibility, not influence detection. Needs live pair rows before empirical distinction. |
| PlanGuard | Planning-based consistency from isolated user intent. | Whether a plan-consistent action is sufficiently warranted by current, independent, low-conflict evidence. | Safe delta: evidence validity after plan consistency. Needs stale/single-source live rows. |
| PromptArmor | Prompt-injection detection and removal. | Replayable support for action arguments, approvals, and risk report fields. | Safe delta: warrant object after retrieval, not prompt sanitization alone. |
| AgentSentry | Temporal causal takeover localization and context purification. | Evidence sufficiency for high-risk actions that remain within authority. | Safe delta: evidence-insufficient dangerous decisions, not takeover alone. |
| CausalArmor | Causal-attribution guardrails for privileged action influence. | Preserving legitimate evidence updates while blocking hijack influence at the protected-field level. | Safe delta: paired admissible vs hijack influence; live claim still blocked. |
| AIRGuard | Runtime authority control and least-privilege side-effect enforcement. | Whether an authorized action has enough fresh, diverse, low-conflict evidence. | Safe delta: permission is necessary but not sufficient. |
| RAGForensics | Traceback of poisoned texts responsible for RAG attacks. | Whether traced evidence may legitimately change an action. | Safe delta: admissibility of evidence-to-action influence, not traceback. |
| RAGChecker / ARES | RAG retrieval/generation quality, faithfulness, context relevance, and answer relevance. | Action parameters, approval flags, risk reports, and execution gates. | Safe delta: action-field warrant validity, not answer faithfulness. |

If this delta is too weak, the paper must narrow further to "evidence-warrant admissibility for high-risk action fields" rather than broad agent safety.

## Rejection Simulation

| Rejection | Paper-kernel response |
|---|---|
| This is just source attribution. | The kernel says attribution asks which evidence influenced output; WarrantGuard asks whether influence is admissible for each protected action field. |
| This is just access control. | The threat model requires authorized actions to still fail when evidence is insufficient, stale, source-collapsed, or conflicted. |
| This is just RAG faithfulness. | The benchmark object is action-field validity for parameters, approval, risk report, and gates, not answer textual grounding. |
| The benchmark is synthetic and overfitted. | The kernel labels current results as L1 fixture and L2 dry-run only; the live matrix is the required upgrade before a main empirical claim. |
| The method has too many hand-designed rules. | The contribution is the proof-carrying evidence warrant and verifier pattern; HardGate and score names are implementation obligations. |
| Novelty over PlanGuard/AttriGuard is unclear. | The related-work skeleton makes them closest neighbors and states the specific discriminator rows needed before stronger claims. |

## Current Most Dangerous Rejection Risk

The most dangerous rejection remains: "This is a positioned system with fixture artifacts, not a demonstrated empirical result." The paper can survive this only if it is written as a design/benchmark/artifact contribution now, or if the next live matrix produces sealed same-model legitimate-vs-hijack pair rows.

## Claim-to-Artifact Map

| Claim | Artifact / table / test | Current status |
|---|---|---|
| Paper-safe claim boundary exists. | `docs/eair_claim_ledger.md`; `docs/warrantguard_paper_kernel.md`. | Safe L0/L1/L2 drafting control. |
| Closest-neighbor discriminator rows are auditable. | `outputs/eair_warrant_reportable_export/reportable_closest_neighbor_discriminator_table.json`; `outputs/eair_warrant_reportable_export/paper_ready_claims.json`. | L1 reviewed fixture claim only. |
| Offline paired contrast can pass through the claim chain. | `outputs/eair_warrant_pair_reportable_export/reportable_influence_contrast_pair_table.json`; `outputs/eair_warrant_pair_reportable_export/paper_ready_claims.json`. | L1 artifact-chain readiness; non-live. |
| Dry-run rows expose legitimate-vs-hijack contrast. | `outputs/eair_prompt_protocol_matrix_dry_run/summary/artifact_summary_influence_contrast_table.json`. | L2 deterministic/pilot evidence. |
| Live model behavior is blocked. | `outputs/eair_prompt_protocol_matrix_live/workflow_status/live_workflow_status.json`. | No L3/L4 claim. |

## Claims Not Yet Safe To Write

- WarrantGuard distinguishes legitimate evidence influence from hijack influence on live-provider outputs.
- WarrantGuard outperforms PCAA, AttriGuard, PlanGuard, PromptArmor, AgentSentry, CausalArmor, AIRGuard, RAGForensics, RAGChecker, ARES, or RAGAS-style faithfulness baselines.
- EAIR-Bench is realistic beyond the current fixture, dry-run, and planned live-matrix boundaries.
- Proof-carrying action firstness.
- Deployment safety for high-risk RAG agents.

## Next Killer Experiment

Run the locked 24-transcript live matrix and promote the main empirical claim only if the same `model x prompt_variant` produces reportable legitimate and hijack influence rows in `reportable_influence_contrast_pair_table.*`, passes coverage, provenance, prompt adherence, protocol legitimacy, reportability audit, claim audit, and strict reviewed seal verification. The table must answer the five paper-critical questions: PRE/RHE false positives, attribution-only overblocking, faithfulness misses action-parameter risk, access control misses evidence-insufficient decisions, and WarrantGuard preserves legitimate influence while blocking hijack influence.

## Source Check

Checked public abstracts/landing pages on 2026-06-22 for novelty boundaries:

- PCAA: https://arxiv.org/abs/2606.04104
- AttriGuard: https://arxiv.org/abs/2603.10749
- PlanGuard: https://arxiv.org/abs/2604.10134
- PromptArmor: https://arxiv.org/abs/2507.15219
- AgentSentry: https://arxiv.org/abs/2602.22724
- CausalArmor: https://arxiv.org/abs/2602.07918
- AIRGuard: https://arxiv.org/abs/2605.28914
- RAGForensics: https://arxiv.org/abs/2504.21668
- RAGChecker: https://papers.nips.cc/paper_files/paper/2024/hash/27245589131d17368cccdfa990cbf16e-Abstract-Datasets_and_Benchmarks_Track.html
- ARES: https://arxiv.org/abs/2311.09476

No official baseline failure or superiority claim is supported by this source check.

## Verification

- Key-string checks passed for the paper kernel, claim ledger, plan handoff, proposal handoff, and this iteration log.
- Live workflow status still reports `overall_status="blocked"`, `blocked_stage="live_preflight"`, and `api_key_env_present=false`.
- Trailing-whitespace scan found no matches.
- `git diff --check` passed on touched documents.
- `pytest -q` passed: 122 tests.
