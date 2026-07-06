# Iteration 098: Promote Influence Contrast Into the Reportable Handoff

## Goal

Close the gap left by Iteration 097: the dry-run summary could show influence contrast, but the reportable export and reviewed claim packet could not yet carry influence-type rows. This iteration promotes influence contrast into the same reportability, integrity-audit, claim-template, review, and seal path used for protected fields.

## Updated One-Sentence Thesis

High-risk RAG-agent actions should carry evidence warrants whose influence type can be audited end to end, so a paper claim can distinguish insufficient, legitimate, and hijack evidence influence without relying on an informal table.

## Current Strongest Contributions

1. **EAIR-Bench.** Benchmark contribution: conditions encode evidence-to-action admissibility and reviewer objections, including influence type over protected action fields.
2. **Evidence Warrant / Proof-Carrying Action.** Representation contribution: action claims are not paper-citeable until the warrant row, artifact hash, and expected value survive citation audit.
3. **WarrantGuard / EAIR-Gate.** System contribution: WarrantGuard exports verifier outcomes into a paper-facing evidence factory with child-table integrity checks, reviewed claim declarations, and strict seal verification.

## What Changed

- `eair-export-reportable-results` now derives `influence_contrast_rows` from `by_model_prompt_condition` and writes `reportable_influence_contrast_table.json/csv/md`.
- `eair-audit-reportable-export` now checks `reportable_influence_contrast_table.json` rows against `reportable_results_export.json`.
- `eair-write-reportable-claim-template` now emits `influence_contrast_warrant_quality_*` starter claims.
- The live runbook now lists `reportable_influence_contrast_table.json/csv/md` as required handoff artifacts.
- Regenerated `outputs/eair_warrant_reportable_export/*`, including `reportable_influence_contrast_table.*`, diagnostic claim audit/seal, reviewed `paper_ready_claims.json`, strict claim audit, strict seal, and strict seal verification.
- Updated `PAPER_PLAN.md` and `refine-logs/FINAL_PROPOSAL.md` to keep the distinction honest: this is an artifact-chain claim, not yet live legitimate-vs-hijack evidence.

## Novelty Pressure Test

| Neighbor | Solves | Remaining difference |
|---|---|---|
| AttriGuard | Causal attribution of tool invocations under indirect prompt injection. | Our new paper object is a reportable influence-type warrant row, not only a context-to-tool causal edge. |
| CausalArmor | Causal dominance and sanitization at privileged decision points. | WarrantGuard must preserve admissible influence and reject inadmissible influence; the reportable row records warrant quality and gate outcome. |
| AgentSentry | Temporal takeover localization and context purification. | Takeover tracing does not produce a reviewed claim packet for action-field evidence sufficiency. |
| PlanGuard / PromptArmor | Plan/prompt consistency, constraints, and prompt-injection mitigation. | A sanitized or consistent plan can still be evidence-insufficient for a parameter, approval flag, or risk report. |
| AIRGuard | Action-time authority and least-privilege control. | Authorization does not prove source diversity, freshness, low conflict, or warrant validity for a high-risk action. |
| RAGForensics | Identifying poisoned texts behind RAG attacks. | Traceback is not the same as deciding whether evidence influence over an action field is admissible. |
| RAGChecker / ARES | RAG context and answer-quality diagnostics. | They do not make tool arguments, approval status, risk report, and influence type into reviewed paper-claim objects. |

## Rejection Simulation

| Rejection | Current answer |
|---|---|
| This is just source attribution. | The new reportable row is keyed by influence type, condition, gate outcome, warrant quality, reviewer objection, and protected fields. |
| This is just access control. | Reportability requires WarrantGuard evidence metrics and child-table integrity, not only permission to call a tool. |
| This is just RAG faithfulness. | The row describes evidence influence on action execution fields, not answer faithfulness. |
| The benchmark is synthetic and overfitted. | The current reviewed row is explicitly fixture-backed; the value of this iteration is the live-ready handoff path, not a model-performance claim. |
| The method has too many hand-designed rules. | No new verifier rule was added. The change only makes existing influence metrics reportable and auditable. |
| The novelty over PlanGuard/AttriGuard is unclear. | The closest-neighbor distinction is now artifact-level: a paper claim cites an influence-type warrant row, not a plan check or attribution-only score. |

## Current Most Dangerous Rejection Risk

The reportable influence handoff is now stronger, but the actual legitimate-vs-hijack model claim is still not paper-safe. The reviewed reportable influence row currently says `insufficient`, while the legitimate/hijack contrast remains dry-run/pilot evidence.

## Claim-to-Artifact Map

| Claim | Artifact / table / test | Status |
|---|---|---|
| Influence-contrast rows are exported after reportability and coverage gates pass. | `outputs/eair_warrant_reportable_export/reportable_influence_contrast_table.md`; `tests/test_mvp.py::test_eair_export_reportable_results_includes_influence_contrast_table`. | Tested; current output is fixture-backed. |
| Reportable influence rows are protected by the export integrity audit. | `outputs/eair_warrant_reportable_export/integrity/reportable_export_integrity_audit.json`; `tests/test_mvp.py::test_eair_audit_reportable_export_detects_influence_contrast_table_row_mismatch`. | Tested and regenerated. |
| Influence-contrast rows can become reviewed, hash-pinned starter claims. | `outputs/eair_warrant_reportable_export/paper_ready_claims.json`; `tests/test_mvp.py::test_eair_write_reportable_claim_template_includes_influence_contrast_claims`. | Reviewed fixture claim packet: 13/13 strict audit pass. |
| The live workflow now requires the reportable influence contrast handoff. | `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.json`; `tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar`. | Runbook/handoff-supported. |

## Claims Not Yet Safe To Write

- Live-model warrant reliability.
- Paper-ready live legitimate-vs-hijack contrast.
- Superiority over official AttriGuard, PlanGuard, PromptArmor, AgentSentry, CausalArmor, AIRGuard, RAGForensics, RAGChecker, or ARES.
- Real deployment safety for power-grid or other operational agents.
- Firstness claims without a final citation and novelty audit.

## Next Killer Experiment

Run the locked 24-transcript live matrix and require that `reportable_influence_contrast_table.*` contains both `legitimate` and `hijack` rows before authoring the main claim. Then promote only those live rows through reportable export, integrity audit, claim review, strict audit, and strict seal verification.

## Verification

- Red test observed: `test_eair_export_reportable_results_includes_influence_contrast_table` failed with missing `influence_contrast_rows`.
- Red tests observed for runbook required artifacts, export child-table audit, and influence-contrast claim-template entries.
- Focused post-fix test group: `4 passed, 58 deselected`.
- Regenerated reportable fixture export, integrity audit, claim template, author-prepared claims, diagnostic claim audit/seal, reviewed `paper_ready_claims.json`, strict claim audit, strict seal, strict seal verification, and live runbook.
- `pytest tests\test_mvp.py -q`: 62 passed.
- `pytest tests\test_eair_bench.py -q`: 45 passed.
- `pytest -q`: 119 passed.
- `python -m compileall formaltrust_platform`: passed.
- `git diff --check -- formaltrust_platform\experiments\eair_bench.py tests\test_mvp.py PAPER_PLAN.md refine-logs\FINAL_PROPOSAL.md refine-logs\iterations\ITERATION_098.md outputs\eair_warrant_reportable_export outputs\eair_prompt_protocol_matrix_live`: no whitespace errors; PowerShell reported the existing LF-to-CRLF warning for `tests/test_mvp.py`.
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

This iteration strengthens the evidence factory, not the empirical result. It does not add a new safety module, does not add a new score, and does not claim that live models already distinguish legitimate from hijack influence.
