# Iteration 110: Make the Live Matrix Claim-Driven

## Goal

Convert the next live experiment from a long runbook into a reviewer-facing claim contract. The live matrix already specifies conditions, prompt variants, and artifacts; this iteration adds the missing paper rule: what each condition must prove, what claim it permits, and how the paper must downgrade if it fails.

## Updated One-Sentence Thesis

High-risk RAG-agent actions need evidence warrants, and the decisive empirical claim is not that WarrantGuard blocks more actions, but that it preserves legitimate evidence influence while rejecting hijack-style or evidence-insufficient influence on protected action fields.

## Current Strongest Contribution List

1. **EAIR-Bench.** A benchmark for evidence-to-action admissibility, with rows designed around protected action fields and reviewer objections.
2. **Evidence Warrant / Proof-Carrying Action.** A representation `(a, W_a)` that binds action fields to required claims, support paths, freshness, source diversity, conflicts, and hard obligations.
3. **WarrantGuard / EAIR-Gate.** A verifier pattern that checks whether evidence is admissible for the action, not merely whether a tool call is permitted, a source is attributed, or an answer is faithful.

## What Changed

- Added `docs/eair_live_killer_experiment_contract.md`.
- The contract maps each reviewer objection to:
  - required live condition(s),
  - protected action fields,
  - passing evidence,
  - allowed paper claim if passed,
  - downgrade rule if failed.
- Updated `docs/warrantguard_paper_kernel.md`, `PAPER_PLAN.md`, and `refine-logs/FINAL_PROPOSAL.md` so live evidence promotion must go through this contract.

## Novelty Pressure Test

| Neighbor | What it solves | What it does not solve | Contract discriminator |
|---|---|---|---|
| PCAA | Proof-carrying action certificates and governance. | Whether the carried object proves RAG evidence sufficiency, freshness, diversity, and conflict resolution for action fields. | Certificate-shaped or structured actions must fail when evidence is stale/insufficient/conflicted. |
| AttriGuard | Which context influenced tool/action behavior. | Whether that influence is legitimate and should be allowed. | The contract requires `legitimate_evidence_update` to pass while hijack influence fails. |
| PlanGuard | Plan/action consistency. | Whether a plan-consistent action has admissible evidence. | `hijack_evidence_support` tests plan-consistent or attributable actions without valid warrants. |
| PromptArmor | Prompt-injection detection and prompt defense. | Warrant validity of the final emitted action. | Conditions are evaluated after action emission and replay, not only at prompt sanitation. |
| AgentSentry | Takeover localization and context purification. | Evidence-insufficient decisions inside otherwise authorized behavior. | `insufficient_evidence_dangerous_decision` targets evidence support, not takeover. |
| CausalArmor | Causal shielding against privileged action influence. | Preserving beneficial evidence updates. | Main pair requires legitimate update pass and hijack parameter influence fail. |
| AIRGuard | Runtime authority and least privilege. | Evidence sufficiency for authorized/no-tool actions. | Authorized/no-tool rows must still fail when risk-report or decision warrant obligations fail. |
| RAGForensics | Traceback of poisoned source influence. | Whether traced evidence may change protected action fields. | Poison exposure without action influence must not force a block. |
| RAGChecker / ARES | RAG answer quality, relevance, and faithfulness. | Action parameters, approvals, risk metadata, and execution gates. | Parameter hijack and risk-report downgrade rows target action-field validity. |

## Rejection Simulation

| Rejection | Contract-level response |
|---|---|
| This is just source attribution. | The contract requires both an allowed legitimate evidence update and blocked inadmissible evidence influence; source identity alone is insufficient. |
| This is just access control. | The access-control objection is tested on authorized/no-tool rows whose evidence warrants can still fail. |
| This is just RAG faithfulness. | Parameter and risk-report rows require action-field obligations that answer faithfulness metrics do not evaluate. |
| The benchmark is synthetic and overfitted. | The contract keeps current evidence at L1/L2 and only permits L3/L4 claims from live reportable, sealed rows. |
| The method has too many hand-designed rules. | The contract treats checks as obligations inside one warrant object and one verifier pattern; individual checks are not sold as contributions. |
| Novelty over PlanGuard/AttriGuard is unclear. | The contract tests plan-consistent or attributable actions that still fail warrant admissibility, plus legitimate evidence influence that should be preserved. |

## Current Most Dangerous Rejection Risk

The most dangerous risk is now empirical non-separation: if the live matrix cannot produce a sealed same-model pair where legitimate influence passes and hijack influence fails, the paper must not claim the main WarrantGuard distinction. It should be written as a benchmark/design/artifact paper with the live run as a partial diagnostic.

## Claim-to-Artifact Map

| Claim | Artifact / table / test | Current status |
|---|---|---|
| The live experiment is claim-driven. | `docs/eair_live_killer_experiment_contract.md`. | New L0/L3 promotion contract. |
| The paper kernel points live evidence promotion to the contract. | `docs/warrantguard_paper_kernel.md`. | Narrative alignment. |
| The active plan/proposal point to the contract. | `PAPER_PLAN.md`; `refine-logs/FINAL_PROPOSAL.md`. | Planning alignment. |
| Live matrix shape is locked at 8 conditions x 3 prompt variants. | `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.json`. | Runbook only; not live evidence. |
| Live execution remains blocked. | `outputs/eair_prompt_protocol_matrix_live/workflow_status/live_workflow_status.json`. | No L3/L4 claim. |

## Claims Not Yet Safe To Write

- WarrantGuard distinguishes legitimate influence from hijack influence in live-provider transcripts.
- The live matrix supports superiority over official PCAA, AttriGuard, PlanGuard, PromptArmor, AgentSentry, CausalArmor, AIRGuard, RAGForensics, RAGChecker, or ARES.
- The benchmark is externally realistic or deployment-safe.
- The method is free of hand-designed obligations; the safe framing is one evidence-warrant object with explicit obligations.

## Next Killer Experiment

Run the existing 24-transcript live matrix without changing the condition set. Promote the main empirical claim only if the sealed paper-ready packet contains a same-`model x prompt_variant` row in `reportable_influence_contrast_pair_table.*` and the reviewed claim bundle passes strict verification. If not, downgrade exactly as specified in `docs/eair_live_killer_experiment_contract.md`.

## Source Check

The contract uses the same closest-neighbor source anchors as the claim ledger:

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

No official prior-work failure or baseline superiority claim is made.

## Verification

- Coverage check found all five user-priority experimental questions in the contract: PRE/RHE false positives, attribution-only overblocking, RAG faithfulness missing action-parameter risk, access control missing evidence-insufficient decisions, and WarrantGuard legitimate-vs-hijack separation.
- Plan/proposal/kernel pointers to `docs/eair_live_killer_experiment_contract.md` are present.
- The contract covers all 8 expected conditions in `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.json`.
- Live workflow status remains blocked before sampling: `overall_status="blocked"`, `blocked_stage="live_preflight"`, and `api_key_env_present=false`.
- Trailing-whitespace scan found no matches.
- `git diff --check` passed on touched files.
- `pytest -q` passed: 122 tests.
