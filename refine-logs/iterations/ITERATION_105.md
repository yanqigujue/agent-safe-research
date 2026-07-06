# Iteration 105: Promote Closest-Neighbor Discriminators to Reportable Artifacts

## Goal

Turn the closest-neighbor novelty pressure test from a live-runbook planning artifact into a reportable, integrity-audited, reviewed claim path. The goal is not to add a new guard or benchmark condition, but to make the paper's "not just attribution/access control/RAG faithfulness/PCAA" distinction citeable as an artifact-chain claim with a strict boundary.

## Updated One-Sentence Thesis

High-risk RAG-agent actions need evidence warrants, and the reportable export must show not only warrant quality by action field but also which closest prior-work objection each warrant failure discriminates against.

## Current Strongest Contributions

1. **EAIR-Bench.** Benchmark contribution: rows are organized around evidence-to-action admissibility and now carry reportable closest-neighbor discriminator views.
2. **Evidence Warrant / Proof-Carrying Action.** Representation contribution: `(a, W_a)` is not a generic action certificate; `W_a` must prove sufficiency, freshness, source diversity, conflict handling, and hard action obligations for protected fields.
3. **WarrantGuard / EAIR-Gate.** System contribution: WarrantGuard is the verifier pattern that rejects authorized, attributed, faithful, plan-consistent, or certificate-shaped actions when their evidence warrant is invalid.

## What Changed

- Added `closest_neighbor_discriminator_rows` to `reportable_results_export.json`.
- Added `reportable_closest_neighbor_discriminator_table.json/csv/md`.
- Added integrity-audit coverage for `reportable_closest_neighbor_discriminator_table.json`.
- Added starter claim-template support for `closest_neighbor_discriminator_count_*`.
- Refreshed `reportable_claims.json`, `paper_ready_claims.json`, claim audits, review verification, and strict bundle seals.
- Regenerated the live runbook so `reportable_closest_neighbor_discriminator_table.*` is a required live handoff artifact.
- Updated `PAPER_PLAN.md` and `refine-logs/FINAL_PROPOSAL.md` from 13 reviewed claims to 15 reviewed claims.

## Novelty Pressure Test

| Neighbor | Solves | What it does not solve | Current discriminator artifact |
|---|---|---|---|
| PCAA | Generic proof-carrying action certificates and runtime governance. | RAG-specific evidence-warrant validity over protected action fields. | Live plan row only; reportable fixture does not yet contain PCAA rows. |
| AttriGuard / RAGForensics | Attribution or traceback of context/source influence. | Whether influence is admissible for action fields. | `source_attribution_only` row in `reportable_closest_neighbor_discriminator_table.json`. |
| PlanGuard | Plan and parameter consistency. | Whether a consistent plan is warranted by current, independent evidence. | Planned live rows; not yet reportable live evidence. |
| PromptArmor | Prompt-injection defense. | Replayable action-field evidence warrants after the prompt is clean. | Planned live rows; not yet reportable live evidence. |
| AgentSentry / CausalArmor | Takeover tracing and causal shielding. | Distinguishing legitimate evidence updates from hijack influence. | Still gated by `reportable_influence_contrast_pair_table.json`, currently `total_rows=0`. |
| AIRGuard | Authority and access-control checks. | Authorized actions with insufficient, stale, or conflicted support. | Planned live rows; not yet reportable live evidence. |
| RAGChecker / ARES | RAG faithfulness and answer-quality diagnostics. | Action arguments, approval flags, risk reports, and execution gates. | Planned live rows; not yet reportable live evidence. |
| Synthetic-overfit critique | Benchmark realism and method overfitting. | Whether reportable rows explicitly identify the tested discriminator. | `benchmark_overfit_source_diversity` row in the new reportable table. |

## Rejection Simulation

| Rejection | New answer | Remaining boundary |
|---|---|---|
| This is just source attribution. | The reportable table shows source-attribution rows failing `source_diverse_support` across `decision`, `tool`, and `risk_report`. | Fixture-backed only; no official RAGForensics comparison claim. |
| This is just access control. | The runbook and closest-neighbor map keep access-control objections separate from warrant obligations. | Needs live authorized-but-evidence-insufficient rows. |
| This is just RAG faithfulness. | The live plan maps RAG faithfulness objections to protected action fields and warrant obligations. | Needs reportable live rows for parameter/risk-report failures. |
| This benchmark is synthetic and overfitted. | The reportable export now states which closest-neighbor discriminator each reviewed fixture row supports. | Still needs live-model reportability and preferably external dataset diversity. |
| Too many hand-designed rules. | Rules are compressed into warrant obligations and closest-neighbor discriminator rows, not sold as separate modules. | Reviewer may still ask for ablations on obligation subsets. |
| Novelty over PlanGuard/AttriGuard is unclear. | The paper now has a table-level object that names closest neighbors and the WarrantGuard discriminator. | Strongest empirical novelty still requires live paired contrast rows. |

## Current Most Dangerous Rejection Risk

The new closest-neighbor table is an L1 reviewed fixture artifact, not a live superiority result. A reviewer can still reject the main empirical claim if `reportable_influence_contrast_pair_table.*` remains empty after live sampling.

## Claim-to-Artifact Map

| Claim | Artifact / table / test | Status |
|---|---|---|
| Reportable closest-neighbor discriminator rows exist and are bounded. | `outputs/eair_warrant_reportable_export/reportable_closest_neighbor_discriminator_table.json`; `claim_boundary="reportable_discriminator_not_prior_work_failure"`. | L1 reviewed fixture claim. |
| The discriminator table is integrity-audited against the export payload. | `outputs/eair_warrant_reportable_export/integrity/reportable_export_integrity_audit.json`; `tests/test_mvp.py::test_eair_audit_reportable_export_detects_closest_neighbor_discriminator_table_row_mismatch`. | Tested and audited. |
| Closest-neighbor discriminator counts are claim-audited and reviewed. | `outputs/eair_warrant_reportable_export/paper_ready_claims.json`; `outputs/eair_warrant_reportable_export/paper_ready_claim_bundle_seal/verification/reportable_claim_bundle_seal_verification.json`. | 15/15 reviewed claims pass strict seal verification. |
| The live workflow requires this table before handoff. | `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.json`. | Protocol-supported; live workflow still blocked. |
| Main legitimate-vs-hijack empirical claim is not ready. | `outputs/eair_warrant_reportable_export/reportable_influence_contrast_pair_table.json`. | `total_rows=0`; no L4 claim. |

## Claims Not Yet Safe To Write

- Live closest-neighbor superiority over PCAA, AttriGuard, PlanGuard, PromptArmor, AgentSentry, CausalArmor, AIRGuard, RAGForensics, RAGChecker, or ARES.
- Generic proof-carrying action firstness.
- Live WarrantGuard reliability.
- Legitimate-vs-hijack main claim.
- Deployment safety.

## Next Killer Experiment

Run the locked 24-transcript live matrix and require the reportable export to produce both:

1. `reportable_closest_neighbor_discriminator_table.*` rows for PCAA, attribution, access control, RAG faithfulness, and PlanGuard-style objections.
2. Non-empty `reportable_influence_contrast_pair_table.*` rows for the same `model x prompt_variant`, proving WarrantGuard allows legitimate evidence influence while blocking hijack influence.

Without both, keep the main paper at L1/L2 and write only artifact-chain and pilot claims.

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

- Red export/audit test: `pytest tests\test_mvp.py -q -k "reportable_results_includes_warrant_taxonomy_columns or closest_neighbor_discriminator_table_row_mismatch or eair_prompt_protocol_live_template_reports_required_artifacts"` failed because `closest_neighbor_discriminator_rows` and the child audit spec did not exist.
- Green focused test: same command passed with `2 passed, 63 deselected`.
- Red claim-template test: `pytest tests\test_mvp.py::test_eair_write_reportable_claim_template_includes_protected_field_claims -q` failed because `closest_neighbor_discriminator_count_1` was missing.
- Green claim-template test: same command passed with `1 passed`.
- `pytest tests\test_mvp.py -q`: 65 passed.
- `pytest tests\test_eair_bench.py -q`: 45 passed.
- `python -m compileall formaltrust_platform`: passed.
- `pytest -q`: 122 passed.
- Regenerated reportable export, integrity audit, starter claim template, author-prepared claims, claim audit, reviewed claims, review verification, unreviewed bundle seal, paper-ready claim audit, paper-ready bundle seal, and strict seal verification.
- `outputs\eair_warrant_reportable_export\reportable_closest_neighbor_discriminator_table.json` has `total_rows=2`.
- `outputs\eair_warrant_reportable_export\paper_ready_claims.json` has `review_claim_count=15`.
- `outputs\eair_warrant_reportable_export\reportable_influence_contrast_pair_table.json` still has `total_rows=0`.
- `python -m formaltrust_platform eair-live-workflow-status ...` still reports `Live workflow blocked: live_preflight` because `OPENAI_API_KEY` is not set.
- Trailing-whitespace scan over touched code/docs/refreshed Markdown artifacts found no matches.
- `git diff --check` reported no whitespace errors; it repeated the existing LF-to-CRLF warning for `tests/test_mvp.py`.
