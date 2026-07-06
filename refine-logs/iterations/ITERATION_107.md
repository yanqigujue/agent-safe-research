# Iteration 107: Add a Paper-Safe Claim Ledger

## Goal

Prevent the paper from overclaiming while the live matrix is still blocked. Iteration 106 created an offline paired-contrast packet; this iteration converts the current evidence state into a reviewer-facing claim ledger that separates safe L0/L1/L2 wording from forbidden L3/L4 wording.

## Updated One-Sentence Thesis

High-risk RAG-agent actions need evidence warrants, but the paper may claim the legitimate-vs-hijack distinction only at the evidence tier actually supported by the current artifacts.

## Current Strongest Contributions

1. **EAIR-Bench.** Benchmark contribution: evidence-to-action admissibility over protected action fields, with legitimate and hijack influence as the core contrast.
2. **Evidence Warrant / Proof-Carrying Action.** Representation contribution: `(a, W_a)` carries replayable support for action fields, approval status, and risk metadata.
3. **WarrantGuard / EAIR-Gate.** System contribution: the verifier allows legitimate evidence influence and blocks hijack influence by checking warrant validity.

## What Changed

- Added `docs/eair_claim_ledger.md`.
- The ledger records:
  - current thesis and contribution contract
  - L0-L4 evidence tiers
  - paper-safe claim sentences
  - forbidden claims until live evidence exists
  - rejection-response wording
  - novelty source anchors
  - next claim upgrade
- Updated `PAPER_PLAN.md` and `refine-logs/FINAL_PROPOSAL.md` to use the ledger as the claim firewall.

## Novelty Pressure Test

| Neighbor | Solves | What it does not solve | Ledger boundary |
|---|---|---|---|
| PCAA | Generic proof-carrying action framing. | RAG-specific evidence warrants over protected action fields. | Do not claim proof-carrying firstness. |
| AttriGuard / RAGForensics | Attribution and traceback. | Whether evidence influence is admissible. | Safe claim: WarrantGuard asks admissibility; no official superiority claim. |
| PlanGuard | Plan/action consistency. | Evidence freshness, sufficiency, source diversity, and conflict. | Safe claim: close neighbor; no PlanGuard failure claim. |
| PromptArmor / AgentSentry / CausalArmor | Injection defense, takeover tracing, causal shielding. | Warranted action-field support after evidence influence. | Safe claim: different object and threat model. |
| AIRGuard | Authority/access control. | Evidence-insufficient authorized decisions. | Safe claim: access is necessary but insufficient. |
| RAGChecker / ARES | RAG faithfulness/evaluation. | Action parameters, approval, risk report, execution gate. | Safe claim: action-field admissibility is not answer faithfulness. |

## Rejection Simulation

| Rejection | Ledger answer |
|---|---|
| This is just source attribution. | The paper-safe claim says the object is admissibility of evidence influence over protected action fields, not source identity. |
| This is just access control. | The ledger states access permission is necessary but not sufficient; warrant validity is separate. |
| This is just RAG faithfulness. | The ledger restricts the novelty claim to action arguments, approval flags, risk reports, and gates. |
| This benchmark is synthetic and overfitted. | The ledger labels fixture and dry-run evidence as L1/L2 and forbids L3/L4 wording. |
| The method has too many hand-designed rules. | The ledger sells the warrant object and verifier pattern, not individual checker names. |
| Novelty over PlanGuard/AttriGuard is unclear. | The ledger names them as closest neighbors and limits the delta to evidence-warrant admissibility. |

## Current Most Dangerous Rejection Risk

The biggest risk is narrative overreach: writing the offline paired fixture as if it were live-provider evidence. The ledger now explicitly forbids that wording.

## Claim-to-Artifact Map

| Claim | Artifact / table / test | Status |
|---|---|---|
| Safe claim boundaries are explicit. | `docs/eair_claim_ledger.md`. | New paper-control artifact. |
| Offline pair packet is claim-audited but non-live. | `outputs/eair_warrant_pair_reportable_export/paper_ready_claims.json`; ledger L1 table. | Safe only as fixture. |
| Warrant fixture has 15 reviewed claims but no pair claim. | `outputs/eair_warrant_reportable_export/paper_ready_claims.json`; ledger L1 table. | Safe as fixture. |
| Live claims are blocked. | `outputs/eair_prompt_protocol_matrix_live/workflow_status/live_workflow_status.json`; ledger forbidden-claims table. | Not safe. |
| Novelty pressure is sourced. | `docs/eair_claim_ledger.md` source anchor table. | Narrative boundary. |

## Claims Not Yet Safe To Write

- Live WarrantGuard legitimate-vs-hijack distinction.
- Superiority over official PCAA, AttriGuard, PlanGuard, PromptArmor, AgentSentry, CausalArmor, AIRGuard, RAGForensics, RAGChecker, or ARES.
- Generic proof-carrying action firstness.
- Benchmark realism claims beyond fixture/dry-run/live-plan boundaries.
- Deployment safety.

## Next Killer Experiment

Run the live matrix and upgrade the ledger's L3/L4 rows from forbidden to allowed only if:

1. live preflight passes,
2. `reportable_influence_contrast_pair_table.*` contains same-`model x prompt_variant` legitimate and hijack rows,
3. closest-neighbor discriminator rows include the planned PCAA/PlanGuard/AttriGuard/access-control/RAG-faithfulness objections,
4. all claims pass audit, review verification, and strict seal verification.

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

- `docs/eair_claim_ledger.md` added and references the current reviewed 15-claim warrant fixture packet, the 7-claim offline paired packet, and the blocked live workflow.
- `PAPER_PLAN.md` now points abstract/introduction/results drafting to the ledger.
- `refine-logs/FINAL_PROPOSAL.md` now points the active experiment schema to the ledger.
- Direct evidence checks:
  - `outputs\eair_warrant_reportable_export\paper_ready_claims.json`: `review_claim_count=15`.
  - `outputs\eair_warrant_pair_reportable_export\paper_ready_claims.json`: `review_claim_count=7` and boundary says not live-provider behavior.
  - `outputs\eair_warrant_pair_reportable_export\reportable_influence_contrast_pair_table.json`: `total_rows=1`, gap `1.0`.
  - `outputs\eair_prompt_protocol_matrix_live\workflow_status\live_workflow_status.json`: `overall_status="blocked"`, `api_key_env_present=false`.
- `pytest -q`: passed, 122 tests.
- Trailing-whitespace scan over touched docs found no matches.
- `git diff --check` over touched docs reported no whitespace errors.
