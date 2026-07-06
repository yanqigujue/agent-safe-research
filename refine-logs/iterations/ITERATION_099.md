# Iteration 099: Add a Legitimate-vs-Hijack Pair Readiness Gate

## Goal

Prevent the paper from accidentally turning a single influence row into the main claim. Iteration 098 made influence rows reportable, but the current fixture has only an `insufficient` row. This iteration adds a stricter pair table so legitimate-vs-hijack claims are generated only when the same `model x prompt_variant` has both a legitimate row and a hijack row after reportability passes.

## Updated One-Sentence Thesis

High-risk RAG-agent actions should carry evidence warrants whose legitimate and hijack influence cases can be paired, audited, and claim-sealed before the paper asserts that WarrantGuard distinguishes them.

## Current Strongest Contributions

1. **EAIR-Bench.** Benchmark contribution: the decisive object is not retrieved poison or answer faithfulness, but whether evidence influence over high-risk action fields is admissible.
2. **Evidence Warrant / Proof-Carrying Action.** Representation contribution: an action-level claim is citeable only when its warrant-backed row survives reportability, integrity, review, and seal checks.
3. **WarrantGuard / EAIR-Gate.** System contribution: the verifier exports both per-row influence evidence and a stricter paired legitimate-vs-hijack readiness table.

## What Changed

- `eair-export-reportable-results` now derives `influence_contrast_pair_rows` from reportable influence rows.
- `reportable_influence_contrast_pair_table.json/csv/md` is emitted as the main-claim readiness table.
- Pair rows are emitted only when the same `model x prompt_variant` has both `legitimate` and `hijack` influence rows.
- `eair-audit-reportable-export` now checks `reportable_influence_contrast_pair_table.json` against `reportable_results_export.json`.
- `eair-write-reportable-claim-template` now emits `legitimate_hijack_influence_gap_*` claims only when pair rows exist.
- The live runbook now requires `reportable_influence_contrast_pair_table.json/csv/md`.
- Regenerated reportable export, integrity audit, claim template, author-prepared claims, diagnostic seal, reviewed claims, strict audit, strict seal, strict seal verification, live runbook, live preflight, and workflow status.

## Novelty Pressure Test

| Neighbor | Solves | Remaining difference |
|---|---|---|
| AttriGuard | Causal attribution for tool invocations under indirect prompt injection. | A paired warrant row asks whether legitimate and hijack influence are separated by evidence admissibility, not merely whether context influenced a call. |
| CausalArmor | Causal dominance and sanitization around privileged actions. | The pair gate preserves legitimate evidence influence while requiring hijack influence to fail warrant quality. |
| AgentSentry | Temporal causal tracing and context purification for takeover. | It does not produce paired, reviewed paper claims for evidence admissibility over action fields. |
| PlanGuard / PromptArmor | Plan consistency, constraints, prompt sanitization, and injection mitigation. | A clean plan can still lack sufficient, fresh, source-diverse evidence for a high-risk parameter or risk report. |
| AIRGuard | Action-time authorization and least privilege. | Permission does not prove evidentiary sufficiency; the pair table is about warrant quality and gate outcomes. |
| RAGForensics | Poison-source traceback. | Traceback does not decide whether evidence influence should be allowed or blocked for a protected action field. |
| RAGChecker / ARES | RAG answer/context diagnostics. | They do not pair legitimate and hijack action-influence cases into a sealed paper-claim artifact. |

## Rejection Simulation

| Rejection | Current answer |
|---|---|
| This is just source attribution. | The pair table requires a legitimate row and a hijack row with warrant-quality contrast, not just a responsible source. |
| This is just access control. | The readiness gate is independent of permission: it compares admissible and inadmissible evidence influence under the same model and prompt. |
| This is just RAG faithfulness. | The pair is over action-field influence and WarrantGuard gate outcomes, not generated answer faithfulness. |
| The benchmark is synthetic and overfitted. | The current fixture intentionally produces no pair claim; the live matrix must populate pair rows before the main claim is written. |
| The method has too many hand-designed rules. | This adds no verifier rule. It is a paper-claim readiness filter over existing reportable rows. |
| The novelty over PlanGuard/AttriGuard is unclear. | The new object is a paired evidence-warrant claim artifact, not a plan check or attribution-only finding. |

## Current Most Dangerous Rejection Risk

The main legitimate-vs-hijack claim is still not paper-safe. The readiness table exists, but the current fixture table has `total_rows=0`; therefore the reviewed claim packet correctly contains no `legitimate_hijack_influence_gap_*` claim.

## Claim-to-Artifact Map

| Claim | Artifact / table / test | Status |
|---|---|---|
| Reportable influence rows can produce legitimate-vs-hijack pair rows when both influence types exist. | `tests/test_mvp.py::test_eair_export_reportable_results_includes_influence_contrast_table`. | Tested with live-marked temporary fixture. |
| Pair rows are integrity-audited as child artifacts. | `tests/test_mvp.py::test_eair_audit_reportable_export_detects_influence_contrast_pair_table_row_mismatch`. | Tested. |
| Pair rows can generate main-claim starter claims only when present. | `tests/test_mvp.py::test_eair_write_reportable_claim_template_includes_influence_contrast_pair_claims`. | Tested. |
| Current reportable fixture does not support a legitimate-vs-hijack main claim. | `outputs/eair_warrant_reportable_export/reportable_influence_contrast_pair_table.json`; `outputs/eair_warrant_reportable_export/paper_ready_claims.json`. | `total_rows=0`; no pair claim. |

## Claims Not Yet Safe To Write

- Live-model legitimate-vs-hijack separation.
- Live-model warrant reliability.
- Superiority over official AttriGuard, PlanGuard, PromptArmor, AgentSentry, CausalArmor, AIRGuard, RAGForensics, RAGChecker, or ARES.
- Real deployment safety.
- Firstness claims without a final citation/novelty audit.

## Next Killer Experiment

Run the locked 24-transcript live matrix and require `reportable_influence_contrast_pair_table.json` to contain at least one pair row for each target model/prompt before writing the main WarrantGuard distinction claim. The main table should report `legitimate_condition`, `hijack_condition`, `legitimate_quality`, `hijack_quality`, `quality_gap`, and gate outcomes.

## Verification

- Red test group failed for missing pair required artifacts, missing `influence_contrast_pair_rows`, missing pair child-table audit, and missing pair starter claim.
- Focused post-fix test group: `4 passed, 60 deselected`.
- `pytest tests\test_mvp.py -q`: 64 passed.
- `pytest tests\test_eair_bench.py -q`: 45 passed.
- `pytest -q`: 121 passed.
- `python -m compileall formaltrust_platform`: passed.
- `git diff --check -- formaltrust_platform\experiments\eair_bench.py tests\test_mvp.py PAPER_PLAN.md refine-logs\FINAL_PROPOSAL.md refine-logs\iterations\ITERATION_099.md outputs\eair_warrant_reportable_export outputs\eair_prompt_protocol_matrix_live`: no whitespace errors; PowerShell reported the existing LF-to-CRLF warning for `tests/test_mvp.py`.
- Refreshed live preflight/status: still blocked at `live_preflight` because `OPENAI_API_KEY` is not set.

## Source Check

- AttriGuard: https://arxiv.org/abs/2603.10749
- PlanGuard: https://arxiv.org/abs/2604.10134
- PromptArmor: https://arxiv.org/abs/2507.15219
- CausalArmor: https://arxiv.org/abs/2602.07918
- AgentSentry: https://arxiv.org/abs/2602.22724
- AIRGuard: https://arxiv.org/abs/2605.28914
- RAGForensics: https://arxiv.org/abs/2504.21668
- RAGChecker: https://arxiv.org/abs/2408.08067
- ARES: https://arxiv.org/abs/2311.09476

## Claim Boundary

This iteration is a claim-readiness boundary, not a new method component. It prevents an overclaim; it does not provide live-model evidence by itself.
