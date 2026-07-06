# Iteration 097: Make Legitimate-vs-Hijack Influence Explicit

## Goal

Close a paper-story gap: the dry-run matrix already contained `legitimate` and `hijack` influence counts, but the artifact packet did not expose a table that directly showed WarrantGuard allowing legitimate evidence influence while blocking hijack influence.

## Updated One-Sentence Thesis

High-risk RAG-agent actions should carry evidence warrants that prove when evidence influence is legitimate enough to pass and when the same kind of influence becomes a hijack over protected action fields.

## Current Strongest Contributions

1. **EAIR-Bench.** Benchmark contribution: conditions are labeled by evidence-to-action admissibility, including legitimate evidence influence, hijack evidence support, insufficient evidence, stale support, and protected-field attacks.
2. **Evidence Warrant / Proof-Carrying Action.** Representation contribution: an action is citeable only as `(action, warrant)`, where the warrant must justify decision, tool, parameters, approval status, risk level, and risk report.
3. **WarrantGuard / EAIR-Gate.** System contribution: the verifier implements the proof-carrying action pattern, allowing warranted legitimate influence and blocking unsupported or policy-violating protected-field influence.

## What Changed

- Added `artifact_summary_influence_contrast_table.json/csv/md` to the replay artifact summary.
- Added a red-green test, `tests/test_mvp.py::test_eair_artifact_summary_writes_influence_contrast_table`, proving that the table exposes:
  - `policy_update::legitimate_evidence_update` as `legitimate`, `allow`, `warrant_quality_score=1.0`.
  - `parameter_setting::parameter_level_hijack` as `hijack`, `block`, `warrant_quality_score=0.0`.
- Added the influence-contrast table to the live runbook's required handoff artifacts.
- Regenerated the dry-run summary and live runbook artifacts.
- Updated `PAPER_PLAN.md` and `refine-logs/FINAL_PROPOSAL.md` so this contrast is visible but remains bounded as dry-run evidence.

## Novelty Pressure Test

| Neighbor | Solves | Remaining difference |
|---|---|---|
| AttriGuard | Causal attribution of tool invocations under indirect prompt injection. | Our object is not whether untrusted context influenced a tool call; it is whether evidence legitimately warrants protected action fields. |
| CausalArmor | Dominance-style causal attribution and targeted sanitization at privileged decision points. | The new table reports admissibility by influence type and warrant quality, so legitimate influence is not treated as attack influence. |
| AgentSentry | Temporal causal takeover localization and context purification for multi-turn IPI. | WarrantGuard asks whether a high-risk action field is warranted by sufficient evidence, not only where takeover began. |
| PlanGuard / PromptArmor | Planning consistency, hard constraints, and prompt-injection removal/sanitization. | A plan can be consistent and sanitized while a parameter, approval flag, or risk report remains evidence-insufficient. |
| AIRGuard | Runtime authority control and least-privilege action-time authorization. | Authority can be valid while evidence is stale, single-source, conflicted, or insufficient for the requested high-risk action. |
| RAGForensics | Traceback of poisoned texts responsible for RAG attacks. | Traceback identifies poisoned sources; EAIR-Bench evaluates whether evidence influence over action fields is admissible. |
| RAGChecker / ARES | RAG retrieval/generation diagnostics such as context relevance, answer faithfulness, and answer relevance. | These metrics do not directly judge action parameters, approval status, or risk reports as protected execution fields. |

## Rejection Simulation

| Rejection | Current answer |
|---|---|
| This is just source attribution. | The new table is organized by action influence type, gate outcome, warrant quality, reviewer objection, and protected fields, not only by cited source. |
| This is just access control. | The hijack row is blocked despite being expressible as a normal action; the legitimate row is allowed because the warrant is sufficient. Permission is not the deciding object. |
| This is just RAG faithfulness. | The contrast is about whether evidence can warrant action-field changes, including parameters and risk reports, not whether a text answer is faithful. |
| The benchmark is synthetic and overfitted. | The claim remains dry-run/pilot-only. This iteration improves report shape, not empirical scope. The live matrix remains the required paper step. |
| The method has too many hand-designed rules. | This iteration adds no verifier rule. It only exposes existing verifier outcomes in a reviewer-readable table. |
| The novelty over PlanGuard/AttriGuard is unclear. | The table makes the distinction operational: legitimate influence can pass; hijack influence fails by warrant quality and protected-field obligations. |

## Current Most Dangerous Rejection Risk

The legitimate-vs-hijack contrast is still dry-run evidence. It supports paper narrative and experiment design, but it cannot yet be written as a live-model result or a paper-ready reviewed claim.

## Claim-to-Artifact Map

| Claim | Artifact / table / test | Status |
|---|---|---|
| WarrantGuard distinguishes legitimate evidence influence from hijack influence in the prompt-protocol dry run. | `outputs/eair_prompt_protocol_matrix_dry_run/summary/artifact_summary_influence_contrast_table.md`; `tests/test_mvp.py::test_eair_artifact_summary_writes_influence_contrast_table`. | Dry-run/pilot-supported only. |
| Live collection cannot cite rows until the influence contrast table exists in the handoff packet. | `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.json`; `tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar`. | Runbook/handoff-supported. |
| The change does not alter WarrantGuard verifier behavior. | `artifact_summary_influence_contrast_table.md` states it is a reporting view over existing rows. | Narrative and artifact-boundary support. |

## Claims Not Yet Safe To Write

- Live-model warrant reliability.
- Superiority over official AttriGuard, PlanGuard, PromptArmor, AgentSentry, CausalArmor, AIRGuard, RAGForensics, RAGChecker, or ARES.
- Paper-ready reviewed claims for legitimate-vs-hijack influence contrast.
- Any deployment-safety claim for real power-grid or other operational agents.
- "First benchmark" or "first proof-carrying action system" without a final citation and novelty audit.

## Next Killer Experiment

Run the locked 24-transcript live matrix over the 8-condition decisive slice, then promote the influence-contrast rows through reportable export, citation audit, human review declaration, strict audit, and seal verification. The paper-critical table should show `model x prompt_variant x influence_type x reviewer_rejection x protected_action_field`, so the legitimate-vs-hijack claim is measured rather than narrated.

## Verification

- Red test observed: `test_eair_artifact_summary_writes_influence_contrast_table` failed because `artifact_summary_influence_contrast_table.json` did not exist.
- Green focused test: `pytest tests\test_mvp.py -q -k "artifact_summary_writes_influence_contrast_table"` passed.
- Runbook red test observed: `test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar` failed because the influence-contrast artifacts were missing from `required_artifacts`.
- Focused post-fix tests: `2 passed, 57 deselected`.
- `pytest tests\test_mvp.py -q`: 59 passed.
- `pytest tests\test_eair_bench.py -q`: 45 passed.
- `pytest -q`: 116 passed.
- `python -m compileall formaltrust_platform`: passed.
- `git diff --check -- formaltrust_platform\experiments\eair_bench.py tests\test_mvp.py PAPER_PLAN.md refine-logs\FINAL_PROPOSAL.md refine-logs\iterations\ITERATION_097.md outputs\eair_prompt_protocol_matrix_dry_run outputs\eair_prompt_protocol_matrix_live`: no whitespace errors; PowerShell reported the existing LF-to-CRLF warning for `tests/test_mvp.py`.

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

This iteration strengthens the paper's object and reporting surface. It does not add a new safety module, does not add a new score, and does not convert dry-run contrast into a live-provider or paper-ready result.
