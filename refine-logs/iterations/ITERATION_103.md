# Iteration 103: Make PCAA Pressure Test a Live-Plan Artifact

## Goal

Move the PCAA boundary from prose into the live experiment plan. Iteration 102 established that generic proof-carrying action novelty is unsafe. This iteration makes the live runbook explicitly test the rejection: "a certificate-shaped action is not enough when the evidence warrant is insufficient, stale, or hijack-driven."

## Updated One-Sentence Thesis

High-risk RAG-agent actions need evidence warrants, and the live experiment should test cases where a generic certificate or permission shape can be present while the evidence warrant fails sufficiency, freshness, source-diversity, or conflict obligations.

## Current Strongest Contributions

1. **EAIR-Bench.** Benchmark contribution: the live plan now includes PCAA-aware discriminator coverage alongside source-attribution, access-control, RAG-faithfulness, and PlanGuard/AttriGuard objections.
2. **Evidence Warrant / Proof-Carrying Action.** Representation contribution: the paper object remains `W_a = (F_a, C_a, S_a, T_a, X_a, H_a)`, not generic action certificates.
3. **WarrantGuard / EAIR-Gate.** System contribution: the verifier turns certificate-shaped actions into executable actions only when their evidence warrant is valid.

## What Changed

- Added the reviewer rejection label `pcaa_certificate_not_evidence_warrant` to three existing threat-model rows:
  - `approval_bypass::hijack_evidence_support`
  - `dispatch_control::insufficient_evidence_dangerous_decision`
  - `policy_update::stale_trusted_policy_support`
- Updated tests so the live runbook must expose `pcaa_certificate_not_evidence_warrant=3`.
- Regenerated:
  - `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.md/json`
  - `outputs/eair_prompt_protocol_matrix_live/live_preflight/live_run_doctor.md/json`
  - `outputs/eair_prompt_protocol_matrix_live/workflow_status/live_workflow_status.md/json`
- Updated `PAPER_PLAN.md` and `refine-logs/FINAL_PROPOSAL.md` to state that PCAA-aware coverage is protocol evidence only.

## Novelty Pressure Test

| Neighbor | Solves | Remaining gap tested here |
|---|---|---|
| PCAA | Generic proof-carrying action certificates and runtime governance. | A certificate-shaped action can still fail because its RAG evidence warrant lacks sufficiency, freshness, source diversity, or low-conflict support. |
| AttriGuard | Causal attribution for context influence. | `hijack_evidence_support` asks whether influence is admissible, not only attributable. |
| PlanGuard | Plan/parameter consistency. | `stale_trusted_policy_support` can be plan-consistent yet evidence-invalid. |
| PromptArmor | Prompt-injection defense. | `hijack_evidence_support` tests warrant validity after attack-shaped evidence influence. |
| AgentSentry / CausalArmor / AIRGuard | Runtime provenance, causal shielding, and authority control. | `insufficient_evidence_dangerous_decision` can remain authorized but unwarranted. |
| RAGForensics / RAGChecker / ARES | Traceback, context relevance, and faithfulness. | Action-field warrant obligations test what answer faithfulness cannot see. |

## Rejection Simulation

| Rejection | Current answer |
|---|---|
| This is just source attribution. | PCAA-aware rows require warrant obligations, not just source responsibility. |
| This is just access control. | `insufficient_evidence_dangerous_decision` is explicitly an allowed-action but evidence-insufficient case. |
| This is just RAG faithfulness. | `stale_trusted_policy_support` can be text-faithful to stale evidence while failing `T_a`. |
| This benchmark is synthetic and overfitted. | The live plan now pins the objection to named rows and keeps them behind reportability and claim-readiness gates. |
| The method has too many hand-designed rules. | The rules are reported as warrant obligations under `W_a`, not as independent method claims. |
| Novelty over PlanGuard/AttriGuard is unclear. | The runbook now carries a separate PCAA axis plus existing PlanGuard/AttriGuard discriminator labels. |

## Current Most Dangerous Rejection Risk

This is still only a planned live-matrix artifact. The project can say the experiment is ready to test PCAA-aware evidence-warrant novelty, but it cannot claim live-model behavior until provider transcripts pass coverage, reportability, review, and seal gates.

## Claim-to-Artifact Map

| Claim | Artifact / table / test | Status |
|---|---|---|
| The live runbook includes PCAA-aware rejection coverage. | `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.json`; `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.md`. | Protocol-supported; coverage value is `3`. |
| The live preflight and workflow status preserve PCAA-aware coverage while staying blocked without secrets. | `outputs/eair_prompt_protocol_matrix_live/live_preflight/live_run_doctor.json`; `outputs/eair_prompt_protocol_matrix_live/workflow_status/live_workflow_status.json`. | Protocol-supported; blocked at `live_preflight`. |
| Tests enforce PCAA-aware coverage. | `tests/test_mvp.py::test_eair_prompt_protocol_live_template_reports_reviewer_rejection_coverage`; `tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar`. | Red-green verified this iteration. |
| Main legitimate-vs-hijack empirical claim still requires paired reportable rows. | `outputs/eair_warrant_reportable_export/reportable_influence_contrast_pair_table.json`. | Current `total_rows=0`; not yet supported. |

## Claims Not Yet Safe To Write

- Live-model PCAA-aware failure rates.
- Superiority over official PCAA or any close neighbor.
- Generic proof-carrying action or action-certificate novelty.
- Main legitimate-vs-hijack distinction on live-provider outputs.
- Deployment safety.

## Next Killer Experiment

Run the live matrix and produce a closest-neighbor discriminator table with columns for certificate-shape/PCAA-style admissibility, access control, attribution, RAG faithfulness, plan consistency, and WarrantGuard. The killer result is not that WarrantGuard blocks more; it is that only WarrantGuard allows legitimate evidence influence while rejecting certificate-shaped actions whose `C_a`, `S_a`, `T_a`, or `X_a` obligations fail.

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

- Red test first: `pytest tests\test_mvp.py -q -k "prompt_protocol_live_template_reports_reviewer_rejection_coverage or live_runbook_command_writes_prompt_matrix_json_sidecar"` failed because `pcaa_certificate_not_evidence_warrant` was missing from runbook coverage.
- Green focused test: the same command passed with `2 passed, 62 deselected`.
- Live runbook/status focused tests: `pytest tests\test_mvp.py -q -k "prompt_protocol_live_template_targets_reviewer_rejection_slice or prompt_protocol_live_template_reports_reviewer_rejection_coverage or live_runbook_command_writes_prompt_matrix_json_sidecar or live_workflow_status_reports_preflight_blocker"` passed with `4 passed, 60 deselected`.
- `pytest tests\test_mvp.py -q`: 64 passed.
- `pytest tests\test_eair_bench.py -q`: 45 passed.
- `pytest -q`: 121 passed.
- `python -m compileall formaltrust_platform`: passed.
- Regenerated live runbook/preflight/status artifacts. `rg` confirms `pcaa_certificate_not_evidence_warrant=3` appears in `RUN_LIVE_PROMPT_MATRIX.json/md`, `live_run_doctor.json`, and `live_workflow_status.json`.
- `outputs/eair_warrant_reportable_export/reportable_influence_contrast_pair_table.json` still has `total_rows=0`, so no L4 legitimate-vs-hijack claim was added.
- `outputs/eair_prompt_protocol_matrix_live/workflow_status/live_workflow_status.json` still reports `overall_status="blocked"` at `live_preflight` because `OPENAI_API_KEY` is not set.
- Direct trailing-whitespace scan over touched code, docs, and refreshed Markdown artifacts found no matches.
- `git diff --check` over touched tracked files and refreshed live-output directory reported no whitespace errors; it repeated the existing LF-to-CRLF warning for `tests/test_mvp.py`.
