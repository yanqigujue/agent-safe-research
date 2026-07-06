# Iteration 113: Collapse Rules Into Evidence-Warrant Semantics

## Goal

Address the "too many hand-designed rules" rejection by making the method formalism explicit. HardGate, VerifyWarrant, CounterWarrant, `warrant_quality_score`, and pair gaps should not read like a pile of contributions. They should read as obligations and diagnostics around one proof-carrying object: `(a, W_a)`.

## Updated One-Sentence Thesis

WarrantGuard's method contribution is evidence-warrant admissibility: a high-risk RAG-agent action executes only if every protected field in `(a, W_a)` satisfies field-level support, freshness, source-diversity, conflict, counter-evidence, and hard-obligation checks.

## Current Strongest Contribution List

1. **EAIR-Bench.** Benchmark contribution: row-level evidence-to-action admissibility threats and legitimate-vs-hijack influence contrast.
2. **Evidence Warrant / Proof-Carrying Action.** Representation contribution: `(a, W_a)` with `W_a = (F_a, C_a, S_a, T_a, X_a, H_a)`.
3. **WarrantGuard / EAIR-Gate.** System contribution: one admissibility verifier pattern, with checker names treated as obligations rather than standalone novelty.

## What Changed

- Added `docs/eair_warrant_formalism_kernel.md`.
- The formalism defines:
  - core objects `q`, `K_q`, `a`, `F_a`, `C_a`, `S_a`, `T_a`, `X_a`, `H_a`, and `W_a`,
  - `ValidField(f, a, W_a, K_q)`,
  - warrant validity and counter-warrant semantics,
  - execution semantics,
  - legitimate, hijack, insufficient, and no-action influence semantics,
  - `warrant_quality_score` and pair gap as diagnostics,
  - rejection-response mapping and artifact map.
- Updated `docs/warrantguard_paper_kernel.md`, `PAPER_PLAN.md`, and `refine-logs/FINAL_PROPOSAL.md` to use this file as the method formalism source.

## Novelty Pressure Test

| Neighbor | Solves | What it does not solve | Formalism delta |
|---|---|---|---|
| PCAA | Proof-carrying action certificates and governance. | RAG-specific field-level evidence admissibility payload. | `W_a` specializes the proof object to support, freshness, diversity, conflict, and hard obligations. |
| AttriGuard | Attribution of context influence on actions. | Whether attributed influence is admissible. | `ValidField` separates admissible influence from hijack influence. |
| PlanGuard | Plan/action consistency. | Whether a consistent plan has admissible evidence support. | A plan can be consistent while `SupportOK`, `FreshOK`, or `DiversityOK` fails. |
| PromptArmor | Prompt-injection defense. | Warrant validity of the final action object. | Formalism evaluates `(a, W_a)` after retrieval/emission. |
| AgentSentry | Takeover provenance and purification. | Evidence-insufficient high-risk actions inside authority. | `ValidField` targets field support and counter-evidence. |
| CausalArmor | Causal shielding against privileged influence. | Preserving beneficial evidence updates. | Formalism allows legitimate influence when `ValidField` holds. |
| AIRGuard | Permission and least privilege. | Evidence validity after permission. | `HardGate` is necessary but not sufficient. |
| RAGForensics | Poison-source traceback. | Whether traced evidence may change a field. | Source identity does not imply `ValidField`. |
| RAGChecker / ARES | RAG answer quality and faithfulness. | Action parameters, approval, risk report, and gates. | Formalism evaluates action fields, not answer text. |

## Rejection Simulation

| Rejection | Formalism response |
|---|---|
| This is just source attribution. | Attribution is not enough; `ValidField` decides whether influence is admissible. |
| This is just access control. | `HardGate` is only one conjunct; execution also requires `VerifyWarrant` and `CounterWarrant`. |
| This is just RAG faithfulness. | Faithful text can still fail parameter, approval, risk-report, freshness, diversity, or conflict obligations. |
| This benchmark is synthetic and overfitted. | The formalism maps each row to a specific `ValidField` failure mode; empirical promotion still requires live reportability. |
| The method has too many hand-designed rules. | The rules are obligations inside `W_a`; the paper contribution is the representation and admissibility semantics. |
| Novelty over PlanGuard/AttriGuard is unclear. | Plan consistency and attribution can hold while field-level warrant validity fails. |

## Current Most Dangerous Rejection Risk

The strongest remaining risk is that the formalism is persuasive but current evidence remains L1/L2. The paper can present the formal object now, but cannot claim live legitimate-vs-hijack separation until L4 evidence exists.

## Claim-to-Artifact Map

| Claim | Artifact / table / test | Current status |
|---|---|---|
| The method formalism is one evidence-warrant object, not a rule pile. | `docs/eair_warrant_formalism_kernel.md`. | New L0 method kernel. |
| `warrant_quality_score` is a diagnostic metric. | `formaltrust_platform/experiments/eair_bench.py::_warrant_quality_score`; `tests/test_eair_bench.py`; `tests/test_mvp.py`. | Implemented/tested metric. |
| Pair gap is diagnostic until live sealed. | `outputs/eair_warrant_pair_reportable_export/reportable_influence_contrast_pair_table.json`; `docs/eair_live_killer_experiment_contract.md`. | L1 offline pair; L4 missing. |
| Paper kernel and plan point to formalism. | `docs/warrantguard_paper_kernel.md`; `PAPER_PLAN.md`; `refine-logs/FINAL_PROPOSAL.md`. | Planning alignment. |

## Claims Not Yet Safe To Write

- `warrant_quality_score` proves safety.
- Positive pair gap proves deployment safety or official prior-work superiority.
- HardGate, VerifyWarrant, and CounterWarrant are separate novelty contributions.
- Live-provider WarrantGuard legitimate-vs-hijack distinction.
- Generic proof-carrying action firstness.

## Next Killer Experiment

Run the locked 24-transcript live matrix and report same-`model x prompt_variant` pair rows. The method claim should be promoted only if `ValidField`-style obligations produce a sealed positive live pair gap while preserving legitimate influence and blocking hijack influence.

## Source Check

The formalism pressure test uses these closest-neighbor anchors:

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

No official baseline-failure claim is made.

## Verification

- The formalism kernel contains `ValidField`, `Execute(a)`, `warrant_quality_score`, and `warrant_quality_gap`.
- Paper kernel, plan, and proposal point to `docs/eair_warrant_formalism_kernel.md`.
- `warrant_quality_score` formula matches `_warrant_quality_score` in `formaltrust_platform/experiments/eair_bench.py`.
- Offline pair fixture matches the formal pair-gap semantics: legitimate quality `1.0`, hijack quality `0.0`, gap `1.0`.
- Live workflow remains blocked: `overall_status="blocked"`, `blocked_stage="live_preflight"`, and `api_key_env_present=false`.
- Trailing-whitespace scan found no matches.
- `git diff --check` passed on touched files.
- `pytest -q` passed: 122 tests.
