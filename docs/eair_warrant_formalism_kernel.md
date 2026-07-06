# EAIR Evidence-Warrant Formalism Kernel

This file is the paper-facing formalism for **WarrantGuard: Evidence Warrants for High-Risk RAG-Agent Actions**. It compresses HardGate, VerifyWarrant, CounterWarrant, and warrant-quality metrics into one claim-safe object: a field-scoped evidence capability relation over protected action fields.

## One-Sentence Formal Claim

A high-risk action may execute only if every protected action field consumes evidence capabilities that are valid for that field. Sufficiency, freshness/currentness, source diversity, conflict, counter-evidence exposure, and hard obligations are capability-boundary predicates, not standalone novelty claims.

## Objects

| Symbol | Meaning | Paper role |
|---|---|---|
| `q` | User/task query. | Context for retrieval and action generation. |
| `K_q` | Retrieved evidence set. | May include legitimate, stale, conflicting, source-collapsed, or hijack-style evidence. |
| `a` | Structured high-risk action. | Contains `decision`, `tool`, `parameters`, `requires_human_approval`, `risk_level`, and `risk_report`. |
| `F_a` | Protected fields of `a`. | The fields that must be warranted before execution. |
| `C_a` | Required support claims. | Claims that must be supported for protected fields. |
| `S_a` | Source clusters and support paths. | Evidence paths and source-diversity information. |
| `T_a` | Freshness/currentness records. | Detects stale or superseded support. |
| `X_a` | Conflict and counter-evidence records. | Exposes disagreement, counter-support, and unresolved conflicts. |
| `H_a` | Hard action obligations. | Domain/tool/parameter/approval/risk-report constraints. |
| `W_a` | Evidence warrant / jurisdiction record. | `W_a = (F_a, C_a, S_a, T_a, X_a, H_a)`. |

The paper contribution is not that each checker is new. The contribution is the proof-carrying action object `(a, W_a)` and the semantics that decide whether retrieved evidence carries a bounded capability to govern each protected field.

## Evidence Field Capabilities

The sharper interpretation of `W_a` is a field-capability ledger. For each retrieved evidence item or support path `e`, define an evidence capability:

```text
ECap(e) = (F_e, O_e, B_e, T_e, P_e, X_e, H_e)
```

where:

| Component | Meaning |
|---|---|
| `F_e` | Protected fields the evidence may govern. |
| `O_e` | Permitted field operations such as set, raise, lower, select, approve, block, or report. |
| `B_e` | Evidence-force bound: relation, modality, scope, temporal validity, and numeric specificity the evidence can support. |
| `T_e` | Currentness interval or supersession status. |
| `P_e` | Provenance and source-cluster scope. |
| `X_e` | Known conflicts and counter-evidence obligations. |
| `H_e` | Hard action obligations the evidence can satisfy or trigger. |

An action field does not merely cite evidence. It **consumes** an evidence capability:

```text
Consume(f, op, a, e) is valid
  iff f in F_e
  and op in O_e
  and the field claim in a stays within B_e, T_e, P_e, X_e, and H_e.
```

This is why the method is not a checklist. A stale source, duplicate cluster, unresolved conflict, weak modality, or missing hard obligation is a way for the action to consume an evidence capability outside its scope.

## Evidence Jurisdiction

For each protected field `f in F_a`, define the field-scoped jurisdiction predicate:

```text
Jurisdiction(f, a, W_a, K_q) =
  HardOK(f, a, H_a)
  and SupportOK(f, C_a, S_a, K_q)
  and FreshOK(f, T_a, K_q)
  and DiversityOK(f, S_a)
  and ConflictOK(f, X_a)
  and CounterEvidenceExposed(f, X_a).
```

Interpretation:

```text
Evidence in K_q may govern field f of action a
iff Jurisdiction(f, a, W_a, K_q) = TRUE.
```

This is the operational predicate for evidence field capabilities. The component checks establish whether the action consumes an in-scope capability for a specific field.

## Field-Level Validity

For each protected field `f in F_a`, define:

```text
ValidField(f, a, W_a, K_q) =
  Jurisdiction(f, a, W_a, K_q).
```

The exact implementation may use domain-specific thresholds or rule checks, but the paper should describe them as capability-boundary predicates attached to protected fields, not as standalone algorithmic contributions.

## Warrant Validity

```text
VerifyWarrant(a, W_a, K_q) = PASS
  iff for every f in F_a:
        ValidField(f, a, W_a, K_q) = TRUE.
```

```text
CounterWarrant(a, W_a, K_q) = CLEAR
  iff no unresolved counter-evidence in X_a invalidates a protected field.
```

```text
HardGate(a, H_a) = PASS
  iff no hard action obligation in H_a is violated.
```

## Execution Semantics

```text
Execute(a) iff
  HardGate(a, H_a) = PASS
  and VerifyWarrant(a, W_a, K_q) = PASS
  and CounterWarrant(a, W_a, K_q) = CLEAR.
```

If any condition fails, WarrantGuard blocks, replaces, or routes the action to review. This is the design pattern shown in `figures/fig1_eair_main_chain.svg`.

## Evidence Influence Semantics

The benchmark does not treat all evidence influence as unsafe. It asks whether the influencing evidence has jurisdiction over the field it changes.

| Influence type | Formal meaning | Expected verifier behavior |
|---|---|---|
| Legitimate influence | Evidence changes a protected field and the action consumes an in-scope evidence capability. | Allow or preserve the action. |
| Capability laundering | Evidence is trusted/current/sufficient for one field or operation, but the action consumes it to change another field, operation, or force level. | Block, replace, or route to review while preserving any valid oracle-supported field updates. |
| Hijack influence | Evidence changes a protected field by laundering a capability across field, operation, force, time, provenance, or conflict scope. | Block, replace, or route to review. |
| Insufficient influence | Evidence is present but lacks the capability needed by the protected field. | Block or route to review. |
| No action influence | Evidence is retrieved but does not affect protected fields. | Do not block solely because exposure occurred. |

This semantics directly addresses PRE/RHE false positives, attribution-only overblocking, access-control gaps, and RAG-faithfulness gaps.

## Report Metrics Are Diagnostics

`warrant_quality_score` is a report metric, not the definition of WarrantGuard:

```text
warrant_quality_score =
  max(0, warrant_present_count - warrant_failed_count) / total_transcripts.
```

The legitimate-vs-hijack pair gap is also diagnostic:

```text
warrant_quality_gap =
  legitimate_warrant_quality_score - hijack_warrant_quality_score
```

The pair gap supports the main empirical claim only when it is computed for the same `model x prompt_variant`, appears in `reportable_influence_contrast_pair_table.*`, and passes strict reviewed claim sealing.

## Rejection-Response Mapping

| Rejection | Formal response |
|---|---|
| This is just source attribution. | Attribution identifies influence; `Jurisdiction` decides whether the influence has authority over a protected field. |
| This is just access control. | `HardGate` is necessary but insufficient; `VerifyWarrant` and `CounterWarrant` still govern evidence authority. |
| This is just RAG faithfulness. | Textual grounding does not imply `ValidField` for parameters, approval, risk level, or risk report. |
| This is just evidence-force calibration. | Force calibration is one dimension of `B_e`; WarrantGuard additionally asks whether calibrated force may be consumed by an action field. |
| This is just environmental grounding. | Environmental grounding detects false paths; WarrantGuard localizes the invalid transfer to field-capability consumption. |
| The benchmark is synthetic and overfitted. | Rows instantiate specific violations of `ValidField`; current evidence tier still limits claims to fixture/dry-run/planned-live boundaries. |
| The method has too many hand-designed rules. | Rules are capability-boundary predicates inside `W_a`; the paper object is field-scoped evidence capability. |
| Novelty over PlanGuard/AttriGuard is unclear. | Plan consistency or attribution can hold while `Jurisdiction` fails, and legitimate evidence influence can pass when `Jurisdiction` holds. |

## Artifact Map

| Formal object or metric | Artifact / test | Claim boundary |
|---|---|---|
| Evidence field capability `ECap(e)` | `docs/eair_innovation_pressure_test.md`; `docs/eair_design_pattern_spine.md` | L0 sharpened design object. |
| `Jurisdiction(f, a, W_a, K_q)` | `docs/eair_design_pattern_spine.md`; `PAPER_PLAN.md` | L0 operational predicate for capability consumption. |
| `W_a = (F_a, C_a, S_a, T_a, X_a, H_a)` | `docs/eair_threat_model_kernel.md`; `PAPER_PLAN.md` | L0 jurisdiction record. |
| Protected fields and obligations | `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.json` | Planned live protocol only. |
| `warrant_quality_score` formula | `formaltrust_platform/experiments/eair_bench.py::_warrant_quality_score`; `tests/test_eair_bench.py`; `tests/test_mvp.py` | Metric implementation evidence. |
| Same-evidence capability laundering | `policy_update::same_evidence_field_capability_laundering`; `tests/test_eair_bench.py::test_warrantguard_blocks_same_evidence_field_capability_laundering` | L2 deterministic/pilot evidence, not live-provider evidence. |
| Legitimate-vs-hijack pair gap | `outputs/eair_warrant_pair_reportable_export/reportable_influence_contrast_pair_table.json` | L1 offline paired fixture only. |
| Live main-claim promotion | `docs/eair_live_killer_experiment_contract.md` | Requires L4 live pair and strict reviewed seal. |

## Claims To Avoid

- Do not claim `HardGate`, `VerifyWarrant`, or `CounterWarrant` are separate novelty contributions.
- Do not claim `warrant_quality_score` is a safety proof.
- Do not claim a positive pair gap proves deployment safety or official prior-work superiority.
- Do not claim generic proof-carrying action firstness.
- Do not describe sufficiency, freshness, diversity, or conflict as the innovation by themselves; they are predicates for field-scoped evidence capabilities.
