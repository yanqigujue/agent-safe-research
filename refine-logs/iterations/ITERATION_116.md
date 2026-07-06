# Iteration 116 - Evidence-Warrant Design Pattern Spine

## Goal

Make the design memorable as one proof-carrying evidence-warrant pattern instead of a stack of named checks, scores, and audit artifacts.

## Updated One-Sentence Thesis

High-risk RAG-agent actions should execute only when the agent externalizes its evidence basis as a proof-carrying action `(a, W_a)` whose protected fields pass field-level warrant obligations.

## Current Strongest Contribution List

1. **EAIR-Bench.** Defines evidence-to-action admissibility cases: legitimate influence, hijack influence, insufficient evidence, stale support, source collapse, conflicts, and no-action influence.
2. **Evidence Warrant / Proof-Carrying Action.** Defines `(a, W_a)` as the representation that moves support from ambient retrieved context into auditable protected-field obligations.
3. **WarrantGuard / EAIR-Gate.** Implements the gate: retrieve evidence -> emit `(a, W_a)` -> verify field-level warrant obligations -> execute, block, replace, or route to review.

## What Changed

- Added `docs/eair_design_pattern_spine.md` as the source for Figure 1 captioning, Algorithm 1 shape, component demotion, and design-pattern rejection responses.
- Updated `docs/warrantguard_paper_kernel.md`, `PAPER_PLAN.md`, `refine-logs/FINAL_PROPOSAL.md`, and `docs/eair_front_matter_kernel.md` to point to the design-pattern spine.
- Did not add any new system module or claim. `HardGate`, support checks, scores, audits, and seals remain obligations/diagnostics around `W_a`.

## Novelty Pressure Test

| Neighbor | What it solves | What it does not solve | Design-pattern delta |
|---|---|---|---|
| PCAA | Proof-carrying action framing and governance checkpoints. | RAG-specific evidence warrant payload for protected fields. | WarrantGuard specializes proof-carrying actions to field-level evidence admissibility. |
| AttriGuard | Causal attribution of context/tool influence. | Whether attributed influence is legitimate for each action field. | Attribution is input evidence; warrant validity is the decision object. |
| PlanGuard | Plan/action consistency under injection pressure. | Whether a consistent plan is grounded in sufficient, fresh, source-diverse, low-conflict evidence. | A plan-consistent action can still fail warrant validity. |
| PromptArmor | Prompt-injection detection and sanitization. | Proof that emitted action fields are evidence-grounded. | The unit under verification is `(a, W_a)`, not only a prompt. |
| AgentSentry | Takeover tracing/provenance and compromised-agent defense. | Evidence sufficiency for an authorized high-risk action. | WarrantGuard targets evidence-insufficient actions even without takeover. |
| CausalArmor | Causal shielding against indirect prompt injection. | Preserving legitimate evidence influence while blocking unsupported field changes. | The pattern permits valid evidence influence instead of suppressing all influence. |
| AIRGuard | Runtime authority and least-privilege control. | Evidence admissibility after authority is satisfied. | Permission is a precondition; warrant validity decides evidence use. |
| RAGForensics | Poison-source traceback and forensic attribution. | Whether traced evidence should affect a protected action field. | Traceback is not enough; the action field needs a valid warrant. |
| RAGChecker | Fine-grained RAG retrieval/generation diagnostics. | Action parameters, approval, risk reports, and execution gates. | The output object is a proof-carrying action, not only a generated answer. |
| ARES | Automated RAG evaluation for context relevance, faithfulness, and answer relevance. | Evidence-to-action legitimacy and hard action obligations. | WarrantGuard evaluates action-field admissibility rather than answer quality. |

## Rejection Simulation

| Rejection | Design-pattern response |
|---|---|
| "This is just source attribution." | Source attribution says what influenced the action; the warrant says whether that influence is admissible for each protected field. |
| "This is just access control." | Access control says whether the action is permitted; WarrantGuard also requires evidence support for parameters, approval, risk, and report fields. |
| "This is just RAG faithfulness." | Faithful text can still justify an unsafe parameter or stale risk report; `ValidField` is action-field validity, not answer grounding. |
| "This benchmark is synthetic and overfitted to the method." | The design pattern is L0; empirical promotion still requires the live experiment spine and L4 sealed pair. |
| "The method has too many hand-designed rules." | The paper now presents one proof-carrying action object with field obligations, not a bag of checkers. |
| "The novelty over PlanGuard/AttriGuard is unclear." | Plan consistency and attribution can both hold while the evidence warrant fails; legitimate influence can pass when the warrant is valid. |

## Most Dangerous Rejection Risk

The most dangerous risk is that reviewers remember individual checker names instead of the object being verified. If the paper foregrounds `HardGate`, `EvidenceSufficient`, and `warrant_quality_score`, the method looks hand-designed. The fix is to make Figure 1 and Algorithm 1 repeat the same pattern: no warrant, no high-risk action.

## Claim-to-Artifact Map

| Claim | Status | Artifact/table/test |
|---|---|---|
| The reviewer memory hook is "No warrant, no high-risk action." | Safe L0. | `docs/eair_design_pattern_spine.md` |
| Figure 1 shows the proof-carrying action as the object being verified. | Safe L0. | `figures/fig1_eair_main_chain.svg`; `docs/eair_design_pattern_spine.md` |
| Algorithm 1 should be one warrant-validation algorithm, not independent checkers. | Safe L0. | `docs/eair_design_pattern_spine.md`; `docs/eair_warrant_formalism_kernel.md` |
| Components such as `HardGate`, support checks, scores, audits, and seals are obligations/diagnostics, not novelty claims. | Safe L0. | `docs/eair_design_pattern_spine.md`; `docs/eair_claim_ledger.md`; `docs/eair_experiment_spine.md` |
| Live WarrantGuard legitimate-vs-hijack distinction. | Not safe. | Still blocked by missing live L4 paired rows and reviewed seal. |

## Claims That Still Cannot Be Written

- "This is the first proof-carrying action system."
- "HardGate is the main technical novelty."
- "The warrant-quality score proves safety."
- "WarrantGuard outperforms PCAA, AttriGuard, PlanGuard, PromptArmor, AgentSentry, CausalArmor, AIRGuard, RAGForensics, RAGChecker, or ARES."
- "Figure 1 proves deployment safety."
- "The current artifact chain proves live-provider legitimate-vs-hijack distinction."

## Next Killer Experiment

The next experiment remains the locked live L4 pair: same `model x prompt_variant`, valid legitimate evidence-update row, invalid parameter/risk hijack row, positive `warrant_quality_gap`, reportability pass, reviewed `paper_ready_claims.json`, and strict bundle seal. The design-pattern spine narrows what that experiment must demonstrate: not that a pile of checks fires, but that a proof-carrying action with a valid warrant executes while a proof-carrying action with an invalid warrant does not.

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

- Passed: design-pattern pointer search confirms `docs/eair_design_pattern_spine.md` is referenced from `docs/warrantguard_paper_kernel.md`, `docs/eair_front_matter_kernel.md`, `PAPER_PLAN.md`, and `refine-logs/FINAL_PROPOSAL.md`.
- Passed: component-demotion and forbidden-claim guardrail search confirms `HardGate`, support checks, scores, audits, and seals are framed as obligations/diagnostics, not separate novelty claims.
- Passed: Figure 1 text/order check confirms the SVG order is `Retrieved Evidence` -> `Proof-Carrying Action` -> `WarrantGuard` -> `Execution Decision`, and the formula now matches `HardGate(a,H_a)`, `VerifyWarrant(a,W_a,K_q)`, and `CounterWarrant(a,W_a,K_q)`.
- Limited: pixel/screenshot rendering was attempted through local converters and Playwright, but no SVG converter was installed and Playwright browsers were unavailable; visual overlap was therefore not screenshot-verified in this iteration.
- Passed: live blocked-status check confirms `overall_status = blocked`, `blocked_stage = live_preflight`, `api_key_env = OPENAI_API_KEY`, and `api_key_env_present = false`.
- Passed: trailing whitespace scan returned no matches.
- Passed: `git diff --check -- docs\eair_design_pattern_spine.md docs\warrantguard_paper_kernel.md docs\eair_front_matter_kernel.md PAPER_PLAN.md refine-logs\FINAL_PROPOSAL.md refine-logs\iterations\ITERATION_116.md figures\fig1_eair_main_chain.svg`.
- Passed: `pytest -q` reports `122 passed`.
