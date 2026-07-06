# Iteration 112: Make the Threat Model Row-Level

## Goal

Sharpen the threat model so the paper is not mistaken for generic access control, source attribution, or RAG faithfulness. The project already had condition descriptors in the live runbook; this iteration turns them into a paper-facing threat-model kernel that binds attacker capability, protected action fields, warrant obligations, benchmark rows, and claim boundaries.

## Updated One-Sentence Thesis

High-risk RAG-agent actions are unsafe when attacker-shaped evidence can determine protected action fields without an admissible warrant; WarrantGuard's object is the evidence warrant that decides whether such influence may execute.

## Current Strongest Contribution List

1. **EAIR-Bench.** Benchmark contribution: row-level evidence-to-action admissibility threats over protected fields.
2. **Evidence Warrant / Proof-Carrying Action.** Representation contribution: `(a, W_a)` binds each protected field to required claims, support paths, freshness, conflicts, and hard obligations.
3. **WarrantGuard / EAIR-Gate.** System contribution: a verifier pattern that executes only when the action's evidence warrant is admissible.

## What Changed

- Added `docs/eair_threat_model_kernel.md`.
- The kernel defines:
  - one-sentence threat model,
  - system under test,
  - protected action fields,
  - attacker capability and trusted boundary,
  - attack success,
  - non-goals,
  - acceptance condition,
  - row-level EAIR-Bench threat table,
  - rejection-response boundary,
  - paper-safe use rules.
- Updated `docs/warrantguard_paper_kernel.md`, `PAPER_PLAN.md`, and `refine-logs/FINAL_PROPOSAL.md` to use the new threat-model source.

## Novelty Pressure Test

| Neighbor | Solves | Threat-model gap for this paper | WarrantGuard object |
|---|---|---|---|
| PCAA | Proof-carrying action governance. | Certificate-shaped actions can still carry stale, insufficient, or conflicted RAG evidence. | Evidence-specific warrant payload for protected fields. |
| AttriGuard | Context influence attribution. | Attribution does not decide whether influence is admissible. | Field-level evidence admissibility. |
| PlanGuard | Plan/action consistency. | Consistent plans can be supported by stale or source-collapsed evidence. | Warrant validity after plan consistency. |
| PromptArmor | Prompt-injection defense. | Prompt cleanliness does not prove final action-field support. | Verify emitted proof-carrying action. |
| AgentSentry | Takeover tracing and context purification. | Authorized behavior can still be evidence-insufficient. | Sufficient support and counter-evidence obligations. |
| CausalArmor | Causal shielding around privileged influence. | Blocking all influence would reject legitimate updates. | Legitimate-vs-hijack influence separation. |
| AIRGuard | Runtime permission and authority. | Permission does not imply evidence support. | Authorized actions still need valid warrants. |
| RAGForensics | Poison-source traceback. | Traceback does not decide whether evidence may change action fields. | Admissibility of traced evidence. |
| RAGChecker / ARES | RAG answer quality and faithfulness. | Answer faithfulness misses parameters, approval, risk report, and execution gate. | Action-field warrant obligations. |

## Rejection Simulation

| Rejection | Threat-model response |
|---|---|
| This is just source attribution. | The threat model says source identity is insufficient; the question is admissibility for each protected action field. |
| This is just access control. | The attacker can produce authorized/no-tool actions with unsupported risk reports, approval bypasses, or dangerous decisions. |
| This is just RAG faithfulness. | The protected object is a high-risk action with parameters, approval, risk level, and risk report, not an answer. |
| The benchmark is synthetic and overfitted. | Each row is tied to an explicit attacker move and protected field, but current claims remain L1/L2 until live evidence exists. |
| The method has too many hand-designed rules. | Obligations are fields of one evidence warrant, not separate novelty claims. |
| Novelty over PlanGuard/AttriGuard is unclear. | Plan consistency and attribution can hold while the warrant remains stale, insufficient, source-collapsed, or conflicted. |

## Current Most Dangerous Rejection Risk

The biggest risk is still live evidence: the threat model is now sharper, but the paper cannot claim live WarrantGuard separation until the locked live matrix produces sealed same-model legitimate-vs-hijack pair rows.

## Claim-to-Artifact Map

| Claim | Artifact / table / test | Current status |
|---|---|---|
| Threat model is explicit and row-level. | `docs/eair_threat_model_kernel.md`. | New L0 paper kernel. |
| Threat rows match planned live condition descriptors. | `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.json`; threat-model kernel. | Protocol-supported, not live. |
| Source-attribution and source-diversity discriminator rows exist. | `outputs/eair_warrant_reportable_export/reportable_closest_neighbor_discriminator_table.json`; `paper_ready_claims.json`. | L1 fixture only. |
| Live claim promotion is gated. | `docs/eair_live_killer_experiment_contract.md`. | Promotion contract. |
| Kernel/plan/proposal point to threat-model source. | `docs/warrantguard_paper_kernel.md`; `PAPER_PLAN.md`; `refine-logs/FINAL_PROPOSAL.md`. | Planning alignment. |

## Claims Not Yet Safe To Write

- Live-provider WarrantGuard legitimate-vs-hijack distinction.
- Official prior-work failure or superiority over PCAA, AttriGuard, PlanGuard, PromptArmor, AgentSentry, CausalArmor, AIRGuard, RAGForensics, RAGChecker, or ARES.
- Deployment safety.
- That planned threat rows are live model behavior.
- That all external evidence influence is malicious.

## Next Killer Experiment

Run the existing 24-transcript live matrix and require each threat row to pass reportability before citation. The main claim still requires same-`model x prompt_variant` legitimate-vs-hijack rows in `reportable_influence_contrast_pair_table.*` plus strict reviewed seal verification.

## Source Check

The threat-model novelty boundary uses the same nearest-work anchors as the related-work kernel:

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

No official baseline failure claim is made.

## Verification

- All 8 planned live conditions appear in `docs/eair_threat_model_kernel.md`.
- The kernel contains attacker capability, trusted boundary, attack success, non-goals, acceptance condition, threat rows, rejection-response boundary, and paper-safe use rules.
- Paper kernel, plan, and proposal point to `docs/eair_threat_model_kernel.md`.
- Live workflow status remains blocked: `overall_status="blocked"`, `blocked_stage="live_preflight"`, and `api_key_env_present=false`.
- Trailing-whitespace scan found no matches.
- `git diff --check` passed on touched files.
- `pytest -q` passed: 122 tests.
