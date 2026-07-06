# Iteration 104: Add a Closest-Neighbor Discriminator Plan

## Goal

Make the next killer experiment reviewer-facing before any live API call. Iteration 103 added PCAA-aware coverage, but the runbook still required a reader to infer which closest neighbor each reviewer objection targeted. This iteration derives an explicit `closest_neighbor_discriminator_plan` from existing threat-model rows, without adding new benchmark conditions or verifier rules.

## Updated One-Sentence Thesis

High-risk RAG-agent actions need evidence warrants, and the live experiment should report a closest-neighbor discriminator plan showing where attribution, access control, RAG faithfulness, plan consistency, or generic action certificates can pass while evidence-warrant admissibility fails.

## Current Strongest Contributions

1. **EAIR-Bench.** Benchmark contribution: each decisive live condition is mapped to reviewer objections and closest-neighbor discriminator axes.
2. **Evidence Warrant / Proof-Carrying Action.** Representation contribution: `W_a = (F_a, C_a, S_a, T_a, X_a, H_a)` remains the paper object; generic certificate shape is insufficient.
3. **WarrantGuard / EAIR-Gate.** System contribution: WarrantGuard is the verifier that separates protocol/certificate shape from evidence-warrant legitimacy.

## What Changed

- Added `closest_neighbor_discriminator_plan` to the live runbook JSON sidecar.
- Added a `## Closest-Neighbor Discriminator Plan` Markdown table to the live runbook.
- The table is derived from existing `condition_threat_model_rows`; no new benchmark condition or runtime verifier was added.
- The PCAA row now explicitly links `pcaa_certificate_not_evidence_warrant` to:
  - `approval_bypass::hijack_evidence_support`
  - `dispatch_control::insufficient_evidence_dangerous_decision`
  - `policy_update::stale_trusted_policy_support`
- Updated `PAPER_PLAN.md` and `refine-logs/FINAL_PROPOSAL.md` to cite the discriminator plan as protocol evidence only.
- Regenerated the live runbook, live preflight, and workflow status artifacts.

## Novelty Pressure Test

| Neighbor | Solves | Planned discriminator |
|---|---|---|
| PCAA | Generic proof-carrying action certificates and runtime governance. | Certificate-shaped actions whose evidence warrant fails sufficiency, freshness, source-diversity, or conflict obligations. |
| AttriGuard / RAGForensics | Attribution and source traceback. | Attributed evidence still needs admissible action-field support. |
| PlanGuard | Plan and parameter consistency. | Plan-consistent actions can fail freshness or source-diversity obligations. |
| AIRGuard | Runtime authority and access control. | Authorized actions can fail sufficient evidence support. |
| RAGChecker / ARES | RAG context relevance and faithfulness. | Faithful text can still support unsafe parameters, approvals, or risk reports. |
| PromptArmor / AgentSentry / CausalArmor | Injection defense, takeover tracing, and causal shielding. | The table separates attack/provenance defenses from evidence admissibility. |

## Rejection Simulation

| Rejection | Current answer |
|---|---|
| This is just source attribution. | The runbook table includes attribution neighbors but ties them to warrant obligations, not only source identity. |
| This is just access control. | The discriminator plan has access-control rows whose WarrantGuard distinction is evidence sufficiency. |
| This is just RAG faithfulness. | RAG faithfulness rows are mapped to protected action fields and warrant obligations. |
| This benchmark is synthetic and overfitted. | The plan states exactly which reviewer objection each row tests before live sampling; claims still require reportability gates. |
| The method has too many hand-designed rules. | Rules are summarized as warrant obligations in a single table. |
| Novelty over PlanGuard/AttriGuard is unclear. | The plan explicitly names the closest neighbor for each objection and the WarrantGuard discriminator. |

## Current Most Dangerous Rejection Risk

The closest-neighbor plan is still protocol evidence. It proves the live experiment is claim-driven, but it does not prove model behavior until live transcripts pass coverage, reportability, claim audit, human review, and strict seal gates.

## Claim-to-Artifact Map

| Claim | Artifact / table / test | Status |
|---|---|---|
| Live runbook exposes a closest-neighbor discriminator plan. | `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.json`; `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.md`. | Protocol-supported. |
| PCAA discriminator row is represented explicitly. | `closest_neighbor_discriminator_plan` row with `reviewer_rejection="pcaa_certificate_not_evidence_warrant"`; `tests/test_mvp.py::test_eair_prompt_protocol_live_template_reports_reviewer_rejection_coverage`. | Protocol-supported. |
| The plan remains non-live evidence. | `claim_boundary="planned_discriminator_not_live_result"` in each discriminator row. | Boundary enforced in JSON. |
| Main legitimate-vs-hijack empirical claim still requires paired reportable rows. | `outputs/eair_warrant_reportable_export/reportable_influence_contrast_pair_table.json`. | Current `total_rows=0`. |

## Claims Not Yet Safe To Write

- Live closest-neighbor superiority.
- Live model behavior for the discriminator table.
- Generic proof-carrying action or action-certificate novelty over PCAA.
- Official failure claims about PCAA, AttriGuard, PlanGuard, PromptArmor, AgentSentry, CausalArmor, AIRGuard, RAGForensics, RAGChecker, or ARES.
- Deployment safety.

## Next Killer Experiment

Run the live matrix and populate a reportable closest-neighbor discriminator result table. The killer claim requires live paired rows showing that WarrantGuard allows legitimate evidence influence while rejecting authorized/certificate-shaped/faithful/attributed actions when their `C_a`, `S_a`, `T_a`, or `X_a` obligations fail.

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

- Red test first: `pytest tests\test_mvp.py -q -k "prompt_protocol_live_template_reports_reviewer_rejection_coverage or live_runbook_command_writes_prompt_matrix_json_sidecar"` failed because `closest_neighbor_discriminator_plan` and the Markdown `## Closest-Neighbor Discriminator Plan` table did not exist.
- Green focused test: the same command passed with `2 passed, 62 deselected`.
- `python -m compileall formaltrust_platform`: passed.
- `pytest tests\test_mvp.py -q`: 64 passed.
- `pytest tests\test_eair_bench.py -q`: 45 passed.
- `pytest -q`: 121 passed.
- Regenerated `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.md/json`, live preflight, and workflow status artifacts.
- `rg` confirms `closest_neighbor_discriminator_plan`, `## Closest-Neighbor Discriminator Plan`, `planned_discriminator_not_live_result`, and `pcaa_certificate_not_evidence_warrant` appear in the live runbook artifacts.
- `outputs\eair_warrant_reportable_export\reportable_influence_contrast_pair_table.json` still has `total_rows=0`, so no L4 empirical claim was added.
- `outputs\eair_prompt_protocol_matrix_live\workflow_status\live_workflow_status.json` still reports `overall_status="blocked"` because `OPENAI_API_KEY` is not set.
- Direct trailing-whitespace scan over touched code, docs, and refreshed Markdown artifacts found no matches.
- `git diff --check` over touched tracked files and refreshed live-output directory reported no whitespace errors; it repeated the existing LF-to-CRLF warning for `tests/test_mvp.py`.
