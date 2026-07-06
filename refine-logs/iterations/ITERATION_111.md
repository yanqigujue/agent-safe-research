# Iteration 111: Lock the Related-Work Delta

## Goal

Prevent the Related Work section from drifting back into broad safety positioning. The closest neighbors are too close to wave away: PCAA owns proof-carrying action framing, AttriGuard and RAGForensics own influence/attribution territory, PlanGuard and AIRGuard own plan/authority guards, and RAGChecker/ARES own RAG evaluation. This iteration narrows the copy-facing delta to one object: evidence-warrant admissibility for protected high-risk action fields.

## Updated One-Sentence Thesis

WarrantGuard is not a better attribution, access-control, plan-guard, or RAG-faithfulness system; it is a proof-carrying action pattern in which high-risk RAG-agent actions execute only when their protected fields carry admissible evidence warrants.

## Current Strongest Contribution List

1. **EAIR-Bench.** Benchmark contribution: evidence-to-action admissibility over protected fields, with reviewer objections mapped to conditions.
2. **Evidence Warrant / Proof-Carrying Action.** Representation contribution: `(a, W_a)` binds protected fields to support claims, source paths, freshness, conflict/counter-evidence, and hard obligations.
3. **WarrantGuard / EAIR-Gate.** System contribution: a verifier pattern for evidence-warrant admissibility, not a claim of official prior-work superiority.

## What Changed

- Added `docs/eair_related_work_positioning.md`.
- The new kernel provides:
  - a related-work thesis,
  - a safe paragraph skeleton,
  - closest-neighbor delta table,
  - claims allowed now,
  - claims to delete,
  - artifact map for related-work sentences,
  - fallback if novelty pressure gets worse.
- Updated `docs/warrantguard_paper_kernel.md`, `PAPER_PLAN.md`, and `refine-logs/FINAL_PROPOSAL.md` to use this file as the copy-facing related-work kernel.

## Novelty Pressure Test

| Neighbor | What it solves | What it does not solve | Current delta |
|---|---|---|---|
| PCAA | Proof-carrying action framing and verifiable governance. | RAG evidence admissibility for action parameters, approvals, risk levels, and risk reports. | Warrant payload specialization; no proof-carrying firstness claim. |
| AttriGuard | Action-level context influence and attribution. | Whether attributed influence should be allowed. | Admissibility of influence, including preserving legitimate updates. |
| PlanGuard | Plan/action consistency. | Whether a consistent plan is warranted by current independent evidence. | Reject plan-consistent but stale/source-collapsed/insufficient warrants. |
| PromptArmor | Prompt injection detection and defense. | Replayable warrant support for the final action artifact. | Verify emitted proof-carrying action, not only prompt cleanliness. |
| AgentSentry | Takeover tracing and purification. | Evidence-insufficient high-risk actions inside authorized behavior. | Focus on warrant sufficiency and protected fields. |
| CausalArmor | Causal shielding for privileged actions. | Positive separation between legitimate and hijack evidence influence. | Main pair must allow legitimate influence and block hijack influence. |
| AIRGuard | Authority and least-privilege execution. | Evidence validity after permission passes. | Permission is necessary but not sufficient. |
| RAGForensics | Poison-source traceback and forensic attribution. | Whether traced evidence may change protected action fields. | Source identity is not enough; warrant admissibility is required. |
| RAGChecker / ARES | RAG answer quality, retrieval quality, and faithfulness evaluation. | Action parameters, approval flags, risk reports, and execution gates. | Action-field warrant validity is the measured object. |

If this still feels too close, the fallback is to narrow the submission to EAIR-Bench plus evidence-warrant artifact auditing, with WarrantGuard as the reference verifier.

## Rejection Simulation

| Rejection | Related-work response |
|---|---|
| This is just source attribution. | The related-work kernel says attribution identifies influence; WarrantGuard evaluates whether the influence is admissible for a protected action field. |
| This is just access control. | The kernel puts AIRGuard/access control in related work and states permission is a precondition, not the paper object. |
| This is just RAG faithfulness. | The kernel separates answer faithfulness from action parameters, approvals, risk metadata, and execution gates. |
| The benchmark is synthetic and overfitted. | The kernel keeps current discriminator evidence at L1/runbook level and sends empirical promotion to the live contract. |
| The method has too many hand-designed rules. | The safe copy sells one warrant object and verifier pattern, not individual checker names. |
| Novelty over PlanGuard/AttriGuard is unclear. | The kernel names them as closest neighbors and states the delta as evidence-warrant admissibility, with official superiority claims forbidden. |

## Current Most Dangerous Rejection Risk

The most dangerous rejection is now "the object is a relabeling of proof-carrying actions plus attribution." The defense is to keep the paper's object narrow: RAG evidence-warrant payloads for protected action fields, with live claims only after the contract produces sealed pair rows.

## Claim-to-Artifact Map

| Claim | Artifact / table / test | Current status |
|---|---|---|
| Related-work delta is narrowed to evidence-warrant admissibility. | `docs/eair_related_work_positioning.md`. | New L0 paper kernel. |
| PCAA/AttriGuard/PlanGuard are closest neighbors, not defeated baselines. | `docs/eair_related_work_positioning.md`; `docs/eair_claim_ledger.md`. | Narrative boundary. |
| Source-attribution-only discriminator rows exist. | `outputs/eair_warrant_reportable_export/reportable_closest_neighbor_discriminator_table.json`; `paper_ready_claims.json`. | L1 fixture only. |
| Live empirical delta requires a sealed legitimate-vs-hijack pair. | `docs/eair_live_killer_experiment_contract.md`. | Promotion contract; no live evidence. |
| Paper kernel and plan use the new related-work source. | `docs/warrantguard_paper_kernel.md`; `PAPER_PLAN.md`; `refine-logs/FINAL_PROPOSAL.md`. | Planning alignment. |

## Claims Not Yet Safe To Write

- Official prior-work failure or superiority against PCAA, AttriGuard, PlanGuard, PromptArmor, AgentSentry, CausalArmor, AIRGuard, RAGForensics, RAGChecker, or ARES.
- Proof-carrying action firstness.
- Live-provider legitimate-vs-hijack distinction.
- General deployment safety or external benchmark realism.

## Next Killer Experiment

Run the existing 24-transcript live matrix and require the paper-ready reviewed packet to contain same-`model x prompt_variant` legitimate-vs-hijack pair rows. Related-work claims should remain positioning-only unless those rows pass the live promotion contract.

## Source Check

The related-work kernel uses these source anchors:

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

No official baseline-failure claim is made from these anchors.

## Verification

- Related-work kernel names all nearest neighbors required by the goal: PCAA, AttriGuard, PlanGuard, PromptArmor, AgentSentry, CausalArmor, AIRGuard, RAGForensics, RAGChecker, and ARES.
- Allowed and forbidden claim boundaries are present; dangerous wording such as "outperforms", "fail", and "first" appears only in deletion or boundary contexts.
- Paper kernel, plan, and proposal point to `docs/eair_related_work_positioning.md`.
- Live workflow status remains blocked: `overall_status="blocked"`, `blocked_stage="live_preflight"`, and `api_key_env_present=false`.
- Trailing-whitespace scan found no matches.
- `git diff --check` passed on touched files.
- `pytest -q` passed: 122 tests.
