# Iteration 100: Add a Claim Readiness Ladder

## Goal

Compress the current WarrantGuard story into a defensible paper-claim boundary. The project already has dry-run contrast tables, reportable fixture exports, and reviewed claim seals, but those artifacts support different levels of claims. This iteration makes that separation explicit so the paper does not promote fixture or pilot evidence into the main empirical claim.

## Updated One-Sentence Thesis

High-risk RAG-agent actions should execute only with evidence warrants, and the strongest empirical claim that WarrantGuard distinguishes legitimate from hijack influence should be written only after paired live reportable rows pass audit, review, and seal gates.

## Current Strongest Contributions

1. **EAIR-Bench.** Benchmark contribution: evaluates whether evidence influence over protected high-risk action fields is admissible, not merely whether an answer cites retrieved text or a tool call is authorized.
2. **Evidence Warrant / Proof-Carrying Action.** Representation contribution: action fields, arguments, approval status, risk metadata, and supporting claims travel with a replayable warrant.
3. **WarrantGuard / EAIR-Gate.** System contribution: an external verifier checks hard action obligations and evidence sufficiency, then exports reportable tables and reviewed claim packets without treating every evidence influence as unsafe.

## What Changed

- Added a five-level claim readiness ladder to `PAPER_PLAN.md` and `refine-logs/FINAL_PROPOSAL.md`.
- Downgraded an older proposal sentence from "paper-ready" to "reportability-ready" and stated the remaining gates.
- Rewrote the next killer experiment so the main legitimate-vs-hijack claim requires populated `reportable_influence_contrast_pair_table.*` rows for the same `model x prompt_variant`.

## Claim Readiness Ladder

| Tier | Evidence level | Claims allowed |
|---|---|---|
| L0 | Method design, threat model, and proof-carrying action schema. | WarrantGuard is a proposed design pattern; no empirical model-behavior claim. |
| L1 | Fixture export, integrity audit, reviewed claim manifest, and strict seal. | Artifact-chain claims about reportability, auditability, and review boundaries. |
| L2 | Deterministic dry-run or pilot rows. | Pilot evidence that warrant checks expose protected-field failures and legitimate/hijack contrast. |
| L3 | Live-provider reportable rows that pass coverage, provenance, integrity, claim audit, and strict review seal. | Live model-condition claims for specific rows and protected fields. |
| L4 | Live paired legitimate-vs-hijack rows in `reportable_influence_contrast_pair_table.*` for the same `model x prompt_variant`. | Main claim that WarrantGuard distinguishes legitimate evidence influence from hijack influence. |

Current state: L1 is supported for reviewed fixture artifacts, L2 is supported for dry-run contrast, and L3/L4 are not yet supported because the live matrix is blocked and the current pair table has `total_rows=0`.

## Novelty Pressure Test

| Neighbor | Solves | Remaining difference |
|---|---|---|
| AttriGuard | Causal attribution for tool invocations under indirect prompt injection. | The paper object is not only whether context influenced a call, but whether protected action fields carry sufficient, fresh, source-diverse, low-conflict evidence warrants. |
| PlanGuard | Plan and parameter consistency for agent actions. | A consistent plan can still be evidence-insufficient, stale, source-collapsed, or conflict-heavy for a high-risk decision. |
| PromptArmor | Prompt-injection detection and sanitization. | Sanitization does not produce a replayable warrant for action arguments, approval status, or risk reports. |
| AgentSentry | Temporal causal tracing and context purification for agent takeover. | It does not define paired legitimate-vs-hijack evidence-warrant rows as the condition for a paper claim. |
| CausalArmor | Causal dominance and shielding around privileged actions. | WarrantGuard must preserve legitimate evidence influence while blocking hijack influence, rather than minimizing all untrusted influence. |
| AIRGuard | Runtime authority and execution control. | Permission to act is not proof that the action is sufficiently warranted by current, independent evidence. |
| RAGForensics | Poison-source traceback and forensic attribution. | Traceback does not decide whether evidence should be allowed to affect protected action fields. |
| RAGChecker / ARES | RAG context relevance, faithfulness, and answer-quality evaluation. | They do not evaluate action parameters, approval flags, risk reports, or proof-carrying execution gates. |

## Rejection Simulation

| Rejection | Current answer |
|---|---|
| This is just source attribution. | The readiness ladder reserves the main claim for paired warrant-quality evidence over action fields, not source responsibility alone. |
| This is just access control. | L4 requires evidence sufficiency contrast under the same model and prompt; allowed-tool actions can still fail. |
| This is just RAG faithfulness. | The object is action-field admissibility and risk metadata, not answer faithfulness. |
| This benchmark is synthetic and overfitted. | Fixture and dry-run claims are explicitly capped at L1/L2; live-provider claims require L3/L4 gates. |
| The method has too many hand-designed rules. | The rules are verifier obligations inside a proof-carrying action pattern, not separate novelty claims. |
| Novelty over PlanGuard/AttriGuard is unclear. | The named object is the evidence warrant and the paired legitimate-vs-hijack claim artifact. |

## Current Most Dangerous Rejection Risk

The main WarrantGuard empirical claim is still not paper-safe. The current fixture proves the artifact pipeline can prevent overclaiming, but it does not yet provide live paired legitimate-vs-hijack evidence.

## Claim-to-Artifact Map

| Claim | Artifact / table / test | Status |
|---|---|---|
| The paper has an explicit claim-readiness boundary. | `PAPER_PLAN.md`; `refine-logs/FINAL_PROPOSAL.md`. | Updated this iteration. |
| Current reviewed fixture claims are artifact-chain claims, not main live-model claims. | `outputs/eair_warrant_reportable_export/paper_ready_claims.json`; strict seal verification artifact. | L1 supported. |
| Dry-run contrast suggests WarrantGuard can allow legitimate evidence updates and block hijack influence. | `outputs/eair_prompt_protocol_matrix_dry_run/summary/artifact_summary_influence_contrast_table.*`. | L2 only. |
| Main legitimate-vs-hijack claims require paired rows. | `outputs/eair_warrant_reportable_export/reportable_influence_contrast_pair_table.json`; pair-table tests from Iteration 099. | Gate exists; current `total_rows=0`. |

## Claims Not Yet Safe To Write

- Live-model legitimate-vs-hijack separation.
- Superiority over official AttriGuard, PlanGuard, PromptArmor, AgentSentry, CausalArmor, AIRGuard, RAGForensics, RAGChecker, or ARES.
- First benchmark or first proof-carrying action system.
- Deployment safety for real high-risk agents.
- Any L3/L4 empirical claim before the live provider matrix passes coverage, reportability, export-integrity, claim-audit, human-review, and strict-seal gates.

## Next Killer Experiment

Unblock the locked 24-transcript live matrix and require `reportable_influence_contrast_pair_table.*` to contain paired legitimate-vs-hijack rows for each target `model x prompt_variant` before writing the main WarrantGuard distinction claim. The decisive table should report legitimate condition, hijack condition, protected fields, warrant quality gap, gate outcomes, and reviewer-rejection labels.

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

## Verification

- `rg` found no remaining `This makes the next model-backed experiment paper-ready` sentence in the active plan/proposal/log files.
- `rg` confirmed the new claim-readiness ladder appears in both `PAPER_PLAN.md` and `refine-logs/FINAL_PROPOSAL.md`.
- Direct whitespace scan over the touched Markdown files found no trailing whitespace.
- `outputs/eair_warrant_reportable_export/reportable_influence_contrast_pair_table.json` still has `total_rows=0`, so no L4 legitimate-vs-hijack claim is supported yet.
- `outputs/eair_prompt_protocol_matrix_live/workflow_status/live_workflow_status.json` still reports `overall_status="blocked"` at `live_preflight` because `OPENAI_API_KEY` is not set.
- No code or generated artifacts were changed in this iteration, so the prior test results from Iteration 099 remain the latest code-verification run.
