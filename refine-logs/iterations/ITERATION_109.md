# Iteration 109: Fix the Hero Figure Around the Evidence-Warrant Object

## Goal

Make the paper's first visual match the compressed design pattern. The previous Fig. 1 ordering risked making WarrantGuard look like a chain of hand-designed components before the proof-carrying action object existed. This iteration rewrites the hero figure so the object and threat model are legible at a skim: evidence first, proof-carrying action second, WarrantGuard third, execution decision last.

## Updated One-Sentence Thesis

High-risk RAG-agent actions should execute only when the emitted proof-carrying action `(a, W_a)` carries an evidence warrant proving that protected action fields are grounded in sufficient, fresh, source-diverse, low-conflict evidence.

## Current Strongest Contribution List

1. **EAIR-Bench.** The benchmark object is evidence-to-action admissibility over protected action fields, especially legitimate versus hijack evidence influence.
2. **Evidence Warrant / Proof-Carrying Action.** The representation contribution is the object `(a, W_a)`, where `W_a` binds action fields to support claims, source paths, freshness, conflicts, and hard obligations.
3. **WarrantGuard / EAIR-Gate.** The system contribution is the verifier pattern: accept, block, replace, or route a high-risk action by checking warrant admissibility, not just permission, attribution, or faithfulness.

## What Changed

- Rewrote `figures/fig1_eair_main_chain.svg` around the four-step pattern:
  - Retrieved Evidence
  - Proof-Carrying Action `(a, W_a)`
  - WarrantGuard
  - Execution Decision
- Removed the visual implication that `Claim Graph`, `Warrant Builder`, and `Warrant Verifier` are separate headline contributions.
- Added a bottom callout that permission, attribution, and answer faithfulness are necessary but insufficient checks.
- Updated `docs/warrantguard_paper_kernel.md`, `PAPER_PLAN.md`, and `refine-logs/FINAL_PROPOSAL.md` to make this SVG the current hero figure.

## Novelty Pressure Test

| Neighbor | What it solves | What it does not solve | Fig. 1 pressure-test answer |
|---|---|---|---|
| PCAA | Proof-carrying action framing and governance. | RAG evidence-warrant payload for action-field admissibility. | Fig. 1 names `(a, W_a)` but makes the payload evidence-specific. |
| AttriGuard | Which context influenced an action. | Whether influence is admissible for protected action fields. | The bottom callout separates source attribution from evidence admissibility. |
| PlanGuard | Plan/action consistency. | Current, source-diverse, low-conflict warrant support. | WarrantGuard is shown after the proof-carrying action, not as a planner. |
| PromptArmor | Prompt-injection detection and prompt defense. | Replayable warrant support after retrieval. | The figure starts from retrieved evidence and verifies emitted action artifacts. |
| AgentSentry | Takeover tracing and context purification. | Evidence-insufficient high-risk actions inside authorized behavior. | Execution is gated by warrant validity, not only provenance cleanup. |
| CausalArmor | Causal influence shielding for privileged actions. | Preserving legitimate evidence influence while blocking hijack influence. | The figure says evidence may influence action only through `W_a`, not that all influence is unsafe. |
| AIRGuard | Runtime permission and authority control. | Whether an authorized action has valid evidence support. | Permission is explicitly demoted to a necessary but insufficient check. |
| RAGForensics | Poison-source traceback. | Whether traced evidence is admissible for action fields. | The figure asks admissibility of the evidence-to-action link. |
| RAGChecker / ARES | RAG answer quality and faithfulness. | Parameters, approval, risk report, and execution decisions. | The figure's protected object is an action, not an answer. |

## Rejection Simulation

| Rejection | Figure-level fix |
|---|---|
| This is just source attribution. | Fig. 1 now says source attribution is necessary but insufficient and centers evidence admissibility for action fields. |
| This is just access control. | Permission is shown as insufficient; execution depends on `VerifyWarrant(a,W_a)` and `CounterWarrant(a,W_a)`. |
| This is just RAG faithfulness. | The figure verifies a proof-carrying action and its parameters/approval/risk report, not answer text. |
| The benchmark is synthetic and overfitted. | Fig. 1 is clearly L0 design-pattern evidence, not a result figure. It does not imply empirical superiority. |
| The method has too many hand-designed rules. | The visual contribution is one object plus one verifier pattern, not a row of named submodules. |
| Novelty over PlanGuard/AttriGuard is unclear. | The visual contrast says the missing object is the admissible evidence warrant, not planning or attribution alone. |

## Current Most Dangerous Rejection Risk

The biggest risk after this edit is empirical rather than visual: the paper's front matter can now explain the object cleanly, but the main legitimate-vs-hijack live claim is still unsupported until L4 live pair rows exist.

## Claim-to-Artifact Map

| Claim | Artifact / table / test | Current status |
|---|---|---|
| The design pattern is visible in the hero figure. | `figures/fig1_eair_main_chain.svg`; key-string and XML validation. | L0 design artifact. |
| The hero figure is aligned with the paper kernel. | `docs/warrantguard_paper_kernel.md` Fig. 1 row. | L0 narrative alignment. |
| The active paper plan points to the corrected figure. | `PAPER_PLAN.md`; `refine-logs/FINAL_PROPOSAL.md`. | Planning alignment. |
| Current live matrix is still blocked. | `outputs/eair_prompt_protocol_matrix_live/workflow_status/live_workflow_status.json`. | No L3/L4 claim. |

## Claims Not Yet Safe To Write

- The figure proves WarrantGuard works on live-provider outputs.
- The figure proves superiority over PCAA, AttriGuard, PlanGuard, PromptArmor, AgentSentry, CausalArmor, AIRGuard, RAGForensics, RAGChecker, or ARES.
- The method has no hand-designed obligations; the safer claim is that obligations instantiate one warrant object.
- EAIR-Bench is realistic beyond current fixture, dry-run, and planned live-matrix evidence.

## Next Killer Experiment

Run the locked 24-transcript live matrix and report a same-`model x prompt_variant` legitimate-vs-hijack pair table. The hero figure will then pair with a result table that answers the five critical objections: PRE/RHE false positives, attribution-only overblocking, RAG faithfulness missing action-parameter risk, access control missing evidence-insufficient dangerous decisions, and WarrantGuard preserving legitimate influence while blocking hijack influence.

## Source Check

Novelty boundaries remain anchored to the closest-neighbor source set used by the claim ledger:

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

The figure makes no official prior-work failure claim.

## Verification

- SVG XML validation passed.
- Key-string checks found the corrected Fig. 1 sequence and paper-plan pointers.
- Live workflow status remains blocked before sampling: `overall_status="blocked"`, `blocked_stage="live_preflight"`, and `api_key_env_present=false`.
- Trailing-whitespace scan found no matches.
- `git diff --check` passed on touched files.
- `pytest -q` passed: 122 tests.
- Visual rendering was not claimed: local `view_image` could not process SVG and no `magick`, `rsvg-convert`, or `inkscape` renderer was available.
