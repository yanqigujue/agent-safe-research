# EAIR Experiment Spine

This file defines the paper's main experiment story for **WarrantGuard: Evidence Warrants for High-Risk RAG-Agent Actions**. It is not a new module. It decides which existing artifacts are allowed into the main paper, which are appendix-only, and which claims remain blocked.

Use with:

- `docs/eair_claim_ledger.md` for evidence tiers.
- `docs/eair_live_killer_experiment_contract.md` for live promotion rules.
- `docs/eair_front_matter_kernel.md` for abstract/introduction wording.
- `docs/eair_related_work_positioning.md` for novelty boundaries.

## Experiment Thesis

The experiments should test whether an evidence warrant can preserve legitimate capability-bearing evidence influence while blocking hijack-style or evidence-insufficient influence over protected action fields.

This is stricter than showing that a verifier blocks many unsafe rows. A main-paper experiment must identify:

```text
reviewer objection -> nearest neighbor -> condition -> protected fields
                  -> artifact -> allowed claim -> downgrade if failed
```

## Main-Paper Table Budget

The main paper should use at most three experiment tables before live evidence exists.

| Slot | Main question | Current status | Main artifact | Allowed wording |
|---|---|---|---|---|
| Table 1: Claim tiers | What can the paper claim now? | Available. | `docs/eair_claim_ledger.md` | The paper has L0/L1/L2 support and no L3/L4 live result. |
| Table 2: Offline pair | Can the artifact chain carry the central legitimate-vs-hijack contrast? | Available as L1 fixture only. | `outputs/eair_warrant_pair_reportable_export/reportable_influence_contrast_pair_table.json` | The offline paired fixture records legitimate quality `1.0`, hijack quality `0.0`, and gap `1.0`; this is artifact-chain readiness, not live behavior. |
| Table 3: Reviewer-objection spine | Does each planned/live row answer a specific rejection? | Planned; partially supported by L1/L2 artifacts. | `docs/eair_live_killer_experiment_contract.md`; `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.json` | The locked live matrix maps objections to conditions, protected fields, and downgrade rules; it has not executed because live preflight is blocked. |

Appendix-only by default:

- `reportable_warrant_leaderboard.*`
- `reportable_model_condition_table.*`
- `reportable_protected_field_table.*`
- `reportable_protocol_legitimacy_*`
- raw replay manifests, hash seals, integrity audits, and claim-audit details

These artifacts support reproducibility and auditing. They should not become separate novelty claims.

## Reviewer Objection Matrix

| Objection | Nearest neighbor | Required condition(s) | Protected fields | Current artifact | Safe current claim | Main upgrade claim if live L4 passes |
|---|---|---|---|---|---|---|
| PRE/RHE false positives: poison exposure is overblocked. | PRE/RHE poison-exposure baselines; RAGForensics-style source tracing. | `approval_bypass::poison_exposure_no_action_influence` | `decision`, `requires_human_approval`, `risk_report` | Planned in `RUN_LIVE_PROMPT_MATRIX.json`; no reportable live row. | The live matrix includes a row to separate poison exposure from action influence. | WarrantGuard does not block solely because poison was retrieved when no protected-field influence exists. |
| Attribution-only overblocks legitimate evidence influence. | AttriGuard; attribution-only guards. | `policy_update::legitimate_evidence_update` | `decision`, `tool`, `risk_level`, `risk_report` | L1 offline pair; L2 dry-run contrast. | Fixture/dry-run artifacts show the reportable chain can preserve a legitimate update under proof-carrying prompts. | WarrantGuard preserves legitimate capability-bearing evidence influence in live-provider transcripts for the sealed row. |
| RAG faithfulness misses action-parameter risk. | RAGChecker; ARES; RAGAS-style faithfulness. | `parameter_setting::parameter_level_hijack` | `parameters`, `requires_human_approval`, `risk_level`, `risk_report` | L1 offline pair; L2 dry-run contrast. | Fixture/dry-run artifacts show parameter hijack can fail warrant obligations even when framed as evidence support. | Action-parameter warrant checks expose live risk that answer faithfulness does not target. |
| Evidence-capability laundering is just tool capability laundering or evidence-force calibration. | Tool/MCP capability laundering discussions; FORCEBENCH. | `policy_update::same_evidence_field_capability_laundering` | `requires_human_approval`, `risk_level`, `risk_report` | L2 deterministic test row; not in the locked 8-condition live matrix. | EAIR-Bench now has a same-evidence row where trusted policy evidence supports simulation routing but fails when consumed as approval waiver or risk downgrade authority. | A follow-on live extension shows WarrantGuard detects same-evidence field-capability laundering, not merely unrelated good/bad cases. |
| Access control misses evidence-insufficient dangerous decisions. | AIRGuard; access-control guards. | `dispatch_control::insufficient_evidence_dangerous_decision`; `approval_bypass::risk_report_downgrade_no_tool`; `parameter_setting::parameter_level_hijack` | `decision`, `tool`, `parameters`, `requires_human_approval`, `risk_level`, `risk_report` | Planned live rows; L1 pair covers only parameter hijack. | Permission is a threat-model boundary; current artifacts do not prove the full live access-control contrast. | Authorized or no-tool actions can still be blocked/routed when their evidence warrant is insufficient, stale, conflicted, or risk-inconsistent. |
| WarrantGuard distinguishes legitimate influence from hijack influence. | CausalArmor; AttriGuard; PlanGuard. | Same `model x prompt_variant` pair: `policy_update::legitimate_evidence_update` and `parameter_setting::parameter_level_hijack` | touched fields across the pair | L1 offline pair records gap `1.0`; L2 dry-run rehearses the pair. | The central contrast is reportable as fixture readiness only. | Main empirical claim: WarrantGuard distinguishes capability-bearing influence from hijack influence in sealed live-provider paired rows. |
| Novelty over PlanGuard/AttriGuard is unclear. | PlanGuard; AttriGuard. | `approval_bypass::hijack_evidence_support`; paired contrast above | `decision`, `requires_human_approval`, `risk_report`; pair fields | Planned live discriminator; L1/L2 partial. | The measured object is field-scoped evidence capability consumption, not plan consistency or attribution alone. | A plan-consistent or attributable action can still fail when evidence lacks field capability, while legitimate evidence remains allowed. |
| Synthetic benchmark is overfit. | Synthetic benchmark critique; source-attribution benchmarks. | `policy_update::near_duplicate_single_source_policy_support`; complete 8-condition coverage | `decision`, `tool`, `risk_report` | L1 closest-neighbor discriminator rows; live run blocked. | Current fixture rows are labeled L1 and do not prove realism. | The live matrix exercises source-collapse and legitimate-update contrast under fixed reportability gates. |
| PCAA / generic certificate is not evidence jurisdiction. | PCAA; Proof-Carrying Certificates. | `dispatch_control::insufficient_evidence_dangerous_decision`; `policy_update::stale_trusted_policy_support`; `approval_bypass::hijack_evidence_support` | `decision`, `tool`, `requires_human_approval`, `risk_report` | Planned live PCAA discriminator only. | WarrantGuard is positioned as RAG-specific field jurisdiction, not proof-carrying firstness. | Certificate-shaped actions fail when evidence lacks jurisdiction because it is stale, insufficient, source-collapsed, or conflict-heavy. |

## Baseline-Framing Rules

- **PRE/RHE-style exposure baselines:** Use only as conceptual baselines unless implemented. The paper may explain why exposure blocking can overblock, but cannot claim measured PRE/RHE failure without runs.
- **Attribution-only:** Treat attribution as necessary but insufficient. Current L1/L2 evidence can show artifact readiness for allowing legitimate influence; official AttriGuard failure is forbidden.
- **RAG faithfulness:** Treat answer faithfulness as a different object. Current artifacts can show parameter/risk-report fields are represented and checked; official RAGChecker/ARES failure is forbidden.
- **Access control:** Treat permission as a hard precondition. Current artifacts can motivate why authorization is insufficient; official AIRGuard failure is forbidden.
- **PCAA:** Treat PCAA as the closest representation neighbor. The paper's novelty is the RAG evidence-warrant payload and benchmark, not generic proof-carrying action.

## Metrics That May Appear In The Main Text

| Metric | Main-text use | Claim boundary |
|---|---|---|
| `warrant_quality_score` | Diagnostic score for whether protected fields satisfy warrant obligations. | Not a universal safety score. |
| `warrant_quality_gap` | Central paired contrast diagnostic. | L1 now; L4 only after sealed live pair. |
| `candidate_unsafe_count` vs `final_unsafe_count` | Shows whether verifier rewrites/blocks unsafe candidates in a specific artifact row. | Does not prove deployment safety. |
| `gate_counts_json` | Shows allow/block/replace decisions for a row. | Must be tied to protected fields and conditions. |
| `reviewer_rejection_counts_json` | Shows which objection a row is designed to answer. | Does not prove official prior-work failure. |
| `protected_action_field_counts_json` | Shows which action fields the row exercises. | Use to prevent answer-only/RAG-only framing. |

Move to appendix unless a claim directly needs them:

- aggregate leaderboards;
- raw prompt-adherence tables;
- model-condition summaries;
- seal and hash internals;
- robustness sweeps that do not map to a reviewer objection.

## Claim Promotion Ladder

| State | Main-paper stance | Required next evidence |
|---|---|---|
| Current L1/L2 state | Benchmark/design/artifact-chain paper with honest dry-run and fixture evidence. | Live provider execution. |
| Live preflight passes but transcripts missing | Reproducible runbook only. | Saved transcripts and replay manifest. |
| Live transcripts exist but reportability fails | Protocol diagnostic, not empirical result. | Passing reportability audit. |
| Reportable live rows without pair | Row-level L3 claims only. | Same-model legitimate-vs-hijack pair. |
| Same-model live pair without strict reviewed seal | Diagnostic pair only. | Reviewed `paper_ready_claims.json` plus strict bundle seal. |
| Same-model live pair with strict reviewed seal | L4 main empirical claim for that sealed model/prompt pair. | Further generalization requires additional models/domains. |
| Same-model live pair plus capability-laundering extension | Stronger field-capability claim for that sealed model/prompt/condition set. | Add `policy_update::same_evidence_field_capability_laundering` to the live matrix and pass the same reportability/review gates. |

## Modules To Keep, Demote, Or Delete

| Component/artifact | Paper role | Decision |
|---|---|---|
| EAIR-Bench condition taxonomy | Benchmark contribution. | Keep in main text. |
| Evidence warrant `(a, W_a)` | Representation contribution. | Keep in main text. |
| WarrantGuard verifier | System contribution. | Keep in main text. |
| `HardGate` | Hard action obligation inside `W_a` validation. | Demote from standalone contribution. |
| `EvidenceSufficient` | Field-level warrant obligation. | Demote from standalone contribution. |
| soft EAIR score / warrant-quality score | Diagnostic metric. | Use only when tied to table rows. |
| reportability audits and claim seals | Reproducibility support. | Appendix unless claim integrity is under discussion. |
| leaderboard views | Convenience summary. | Appendix-only. |
| extra robustness sweeps without objection mapping | Artifact sprawl. | Delete or defer. |

## What The Main Results Section Should Say Now

1. The current evidence is not a live-provider performance result.
2. The reviewed fixture packet and offline pair show that the artifact chain can carry the paper's central contrast.
3. The dry-run matrix rehearses the intended proof-carrying prompt behavior.
4. The live matrix is locked to reviewer objections and protected fields but is blocked before sampling by missing `OPENAI_API_KEY`.
5. Therefore the paper can currently be written as a benchmark/design/artifact-chain paper; the stronger empirical paper requires the L4 live pair.

## What The Main Results Section Must Not Say

- Do not report official baseline wins.
- Do not call the offline pair a live model result.
- Do not convert leaderboard aggregates into safety claims.
- Do not claim benchmark realism from fixtures.
- Do not use any table that lacks a reviewer objection, protected field, artifact, and downgrade rule.

## Source Anchors

- PCAA: https://arxiv.org/abs/2606.04104
- Proof-Carrying Certificates for LLM Pipelines: https://arxiv.org/abs/2605.16407
- Confused Deputy / capability security: https://dl.acm.org/doi/10.1145/54289.871709
- Towards Verifiably Safe Tool Use for LLM Agents: https://arxiv.org/abs/2601.08012
- FORCEBENCH / Relevant Is Not Warranted: https://arxiv.org/abs/2605.28044
- EnvTrustBench: https://arxiv.org/abs/2605.08828
- Prism-Reranker: https://arxiv.org/abs/2604.23734
- MiniScope: https://arxiv.org/abs/2512.11147
- ToolPrivBench / When Lower Privileges Suffice: https://arxiv.org/html/2606.20023
- Causality Laundering / ARM: https://arxiv.org/abs/2604.04035
- Tool/MCP capability laundering discussion, non-paper security-neighbor anchor: https://github.com/cosai-oasis/secure-ai-tooling/issues/196
- AttriGuard: https://arxiv.org/abs/2603.10749
- PlanGuard: https://arxiv.org/abs/2604.10134
- PromptArmor: https://arxiv.org/abs/2507.15219
- AgentSentry: https://arxiv.org/abs/2602.22724
- CausalArmor: https://arxiv.org/abs/2602.07918
- AIRGuard: https://arxiv.org/abs/2605.28914
- RAGForensics: https://arxiv.org/abs/2504.21668
- RAGChecker: https://arxiv.org/abs/2408.08067
- ARES: https://arxiv.org/abs/2311.09476
