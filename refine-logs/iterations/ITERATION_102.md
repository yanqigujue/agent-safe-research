# Iteration 102: Make the PCAA Boundary Explicit

## Goal

A fresh novelty scan surfaced a very close neighbor: **Proof-Carrying Agent Actions (PCAA)**. This makes generic "proof-carrying action" or action-certificate novelty unsafe. This iteration narrows the active paper to the RAG-specific **Evidence Warrant** object: a certificate payload for evidence admissibility over protected action fields.

## Updated One-Sentence Thesis

High-risk RAG-agent actions should execute only with evidence warrants whose claim/source/freshness/conflict payload proves that retrieved evidence may legitimately influence the action, arguments, approval status, and risk report.

## Current Strongest Contributions

1. **EAIR-Bench.** Benchmark contribution: discriminator cases test whether retrieved evidence is admissible for protected action fields, not merely whether an action has a certificate, attribution, permission, or faithful answer.
2. **Evidence Warrant / Proof-Carrying Action.** Representation contribution: the novelty is the RAG-specific warrant payload `W_a = (F_a, C_a, S_a, T_a, X_a, H_a)`, covering protected fields, required claims, source/support paths, freshness, conflicts/counter-evidence, and hard obligations.
3. **WarrantGuard / EAIR-Gate.** System contribution: the verifier accepts an action only when the evidence warrant is valid; `HardGate`, `EvidenceSufficient`, EAIR score, audits, and seals are obligations or diagnostics, not separate novelty claims.

## What Changed

- Changed the active paper title in `PAPER_PLAN.md` and `refine-logs/FINAL_PROPOSAL.md` to **WarrantGuard: Evidence Warrants for High-Risk RAG-Agent Actions**.
- Added an explicit evidence-warrant contract to both active documents.
- Added PCAA to the closest-neighbor novelty boundary.
- Marked generic proof-carrying action/action-certificate firstness as unsafe.
- Added a claim-map row stating that the PCAA-aware boundary is narrative/novelty-boundary evidence only, not an empirical result.

## Novelty Pressure Test

| Neighbor | Solves | Does not solve | WarrantGuard delta |
|---|---|---|---|
| PCAA | Generic proof-carrying agent actions, action certificates, verifiable policies, and runtime governance. | RAG-specific evidence admissibility over action arguments, approvals, risk reports, freshness, source diversity, and conflicts. | Evidence Warrant specializes the certificate payload around claim/source/conflict evidence for protected action fields. |
| AttriGuard | Causal attribution for context influence on tool/action behavior. | Whether influence is legitimate under evidence sufficiency and conflict constraints. | Warrant validity decides admissible influence, not only causal influence. |
| PlanGuard | Plan and parameter consistency. | Whether consistent actions are warranted by current independent evidence. | WarrantGuard rejects stale, source-collapsed, conflicted, or insufficient support. |
| PromptArmor | Prompt-injection detection and sanitization. | Replayable evidence support for action fields. | EAIR-Bench labels evidence influence as legitimate or hijack-style. |
| AgentSentry / CausalArmor / AIRGuard | Runtime tracing, causal shielding, and authority control. | Evidence sufficiency for authorized actions. | Permission and provenance are prerequisites, not the paper object. |
| RAGForensics / RAGChecker / ARES | RAG traceback, context relevance, and faithfulness. | Action arguments, approval flags, risk reports, and execution gates. | WarrantGuard evaluates protected action-field evidence admissibility. |

## Rejection Simulation

| Rejection | Current answer |
|---|---|
| This is just source attribution. | The active object is `W_a`, which must prove support, freshness, source diversity, and low conflict for action fields, not only identify sources. |
| This is just access control. | Access permission is placed in `H_a`; the paper claim requires evidence support via `C_a`, `S_a`, `T_a`, and `X_a`. |
| This is just RAG faithfulness. | Faithful generated text can still set unsafe parameters, approvals, or risk reports without a valid warrant. |
| This benchmark is synthetic and overfitted. | Claims remain capped by the L0-L4 ladder; live paired rows are required for the main empirical claim. |
| The method has too many hand-designed rules. | The method is the warrant contract; individual checks are contract obligations and diagnostics. |
| Novelty over PlanGuard/AttriGuard is unclear. | PCAA/PlanGuard/AttriGuard are now explicit neighbors, and the delta is RAG evidence admissibility over protected action fields. |

## Current Most Dangerous Rejection Risk

PCAA makes the phrase "Proof-Carrying Action" crowded. The paper must lead with "Evidence Warrant" and avoid any claim that generic action certificates are new.

## Claim-to-Artifact Map

| Claim | Artifact / table / test | Status |
|---|---|---|
| PCAA is treated as a close neighbor and generic action-certificate firstness is unsafe. | `PAPER_PLAN.md`; `refine-logs/FINAL_PROPOSAL.md`. | Narrative/novelty-boundary claim. |
| WarrantGuard has a compact evidence-warrant contract. | `PAPER_PLAN.md`; `refine-logs/FINAL_PROPOSAL.md`. | Method-definition claim. |
| Main legitimate-vs-hijack empirical claim still requires paired reportable rows. | `outputs/eair_warrant_reportable_export/reportable_influence_contrast_pair_table.json`. | Current `total_rows=0`; not yet supported. |
| Reviewed fixture claims remain artifact-chain claims only. | `outputs/eair_warrant_reportable_export/paper_ready_claims.json`; strict seal verification artifact. | L1 only. |

## Claims Not Yet Safe To Write

- First proof-carrying action system.
- Generic action-certificate novelty over PCAA.
- Superiority over official PCAA, AttriGuard, PlanGuard, PromptArmor, AgentSentry, CausalArmor, AIRGuard, RAGForensics, RAGChecker, or ARES.
- Live-model legitimate-vs-hijack separation.
- Deployment safety.

## Next Killer Experiment

Add a PCAA-aware discriminator table to the live experiment plan: compare certificate-shaped but evidence-insufficient actions against WarrantGuard evidence warrants. The decisive rows should show actions that satisfy generic permission/certificate shape but fail `T_a`, `S_a`, `X_a`, or `C_a` obligations, proving that the contribution is evidence admissibility rather than generic action certification.

## Source Check

- PCAA / Proof-Carrying Agent Actions: https://arxiv.org/abs/2606.04104
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

- `rg` confirms PCAA appears in the active novelty boundary in `PAPER_PLAN.md`, `refine-logs/FINAL_PROPOSAL.md`, and this iteration log.
- `rg` confirms the active title now uses **WarrantGuard: Evidence Warrants for High-Risk RAG-Agent Actions**.
- `rg` confirms the evidence-warrant contract `W_a = (F_a, C_a, S_a, T_a, X_a, H_a)` appears in both active documents.
- Direct trailing-whitespace scan over the touched Markdown files found no matches.
- `outputs/eair_warrant_reportable_export/reportable_influence_contrast_pair_table.json` still has `total_rows=0`; no L4 empirical claim was added.
- `outputs/eair_prompt_protocol_matrix_live/workflow_status/live_workflow_status.json` still reports `overall_status="blocked"` at `live_preflight` because `OPENAI_API_KEY` is not set.
- No code or generated experiment artifacts were changed in this iteration.
