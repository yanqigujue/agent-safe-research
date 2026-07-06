# Power-Ops Action Invariance Formal Model

Date: 2026-07-02

## 1. Objects

Let an agent context contain sources:

```text
X = evidence | skill_output | tool_metadata | memory | user_approval
  | prior_step_output | trace_span | policy_epoch | obligation_receipt
  | counter_authority
```

Each source `x` may provide a capability:

```text
Cap(x) = (source_id, source_type, roles, fields, operations,
          data_scope, effect_scope, delegation_scope, time_scope,
          obligations)
```

An agent action is decomposed into fields:

```text
a = {f_1: v_1, ..., f_n: v_n}
```

For each action step `s` and field `f`, define the authority need:

```text
Need(s, f) = (required_roles, field, operation,
              data_scope, effect_scope, delegation_scope,
              time_scope, required_obligations)
```

Examples of protected power-operation fields:

```text
answer
risk_report
risk_level
requires_human_approval
dispatch_order
side_effect
switching_operation
data_read_scope
equipment_certification
public_publish
external_publish
approval_waiver
```

## 2. Coverage

A capability covers a field need when all dimensions match:

```text
Covers(c, n) iff
  n.required_roles subset c.roles
  and n.field covered_by c.fields
  and n.operation in c.operations
  and n.data_scope covered_by c.data_scope
  and n.effect_scope covered_by c.effect_scope
  and n.delegation_scope covered_by c.delegation_scope
  and n.time_scope covered_by c.time_scope
  and obligations_satisfied(c.obligations, n)
```

For field families, coverage is prefix-aware:

```text
fields=["parameters"] covers "parameters.voltage_limit"
```

## 3. Minimal Authority Witness

Given a context capability set `C` and a need `n`, a witness is any subset `W subset C` such that:

```text
Witness(W, n) iff forall required role r in n.required_roles,
  exists c in W: CoversRole(c, r, n)
```

A minimal witness is:

```text
MinimalWitness(W, n) iff Witness(W, n)
  and no W' subset W satisfies Witness(W', n)
```

The audit compression ratio is:

```text
compression(n) = (|C| - |W|) / |C|
```

If no witness exists, the audit records missing roles and missing obligations.

## 4. Decision Rule

For each field:

```text
FieldDecision(s, f) =
  allow   if exists MinimalWitness(W, Need(s,f))
              and no counter-authority applies
  abstain if positive authority exists but counter-authority applies
              or parser/runtime evidence is incomplete
  block   otherwise
```

The existing AFW runtime records this in:

```text
metrics["afw_runtime_field_results"]
metrics["afw_gate_decision"]
metrics["final_action"]
```

## 5. Action Invariance

Let `A+` be fields expected to be authorized and `A-` fields expected to be unauthorized.

Authorized field preservation:

```text
Preserve(a, a', A+) iff forall f in A+, a'[f] = a[f] or FieldDecision(f)=allow
```

Unauthorized field prevention:

```text
Prevent(a', A-) iff forall f in A-, FieldDecision(f) in {block, abstain}
```

Fieldwise action invariance:

```text
ActionInvariant(a, a') iff Preserve(a, a', A+) and Prevent(a', A-)
```

This differs from whole-action blocking. Whole-action blocking is safe but may collapse utility when a mixed action contains both authorized and unauthorized fields.

## 6. Conservative Collapse

A mixed action has:

```text
exists f+ in A+ and exists f- in A-
```

Strict blocking collapses useful behavior when:

```text
GateDecision(a) = block
and exists f+ in A+: FieldDecision(f+) = allow
```

The measured rate is:

```text
strict_block_collapse_rate =
  mixed_blocked_cases_with_authorized_allowed_field / blocked_cases
```

This metric captures the user's concern: strict interventions can make an agent too conservative even when part of the action is legitimate.

## 7. Power-Operation Safety Constraints

Role mismatch is central:

```text
report_formatting_skill != risk_assessment_authority
retrieval_index_metadata != data_access_authority
answer_style_personalization != safety_policy_authority
approval_for_inspection_schedule != energization_authority
procedure_for_safety_warning != approval_waiver_authority
```

Temporal decay:

```text
time_scope(policy_epoch_2026_q3) does not cover policy_epoch_2026_q4
```

Obligation-carrying warrants:

```text
requires_static_scan(mode=must_discharge)
requires_dlp_scan(mode=must_discharge)
```

Counter-authority:

```text
policy_hold(field=f, effect_scope=e) forces abstain for matching field/effect
```

## 8. Current Implementation Binding

The current runnable binding is:

```text
examples/data/power_ops_action_invariance_cases.jsonl
  -> examples/power_ops_action_invariance_runtime_validation.yaml
  -> guardrail.afw_capguard
  -> evaluate.afw_runtime
  -> formaltrust_platform.experiments.power_ops_action_invariance
```

No new state schema is required. The formal objects map to existing runtime keys:

| Formal object | Runtime location |
|---|---|
| `Cap(x)` | `case.metadata.afw_source_events[*].authority_manifest` or `skill_manifest` |
| `Need(s,f)` | `case.metadata.afw_consumptions[*].need` |
| candidate action | `case.metadata.candidate_action` |
| oracle | `case.metadata.afw_oracle` and `action_invariance_oracle` |
| field decision | `metrics["afw_runtime_field_results"]` |
| witness audit | `metrics["afw_runtime_field_results"][*]["witness_audit"]` |

## 9. Claim Boundary

This model currently supports a curated power-ops regression slice. It does not yet prove:

```text
live deployment safety
general power-grid safety
human-label agreement
true fieldwise repair at final-action execution time
```

The next formal step is to model fieldwise repair explicitly:

```text
Repair(a) = keep allowed fields + remove/block/route unauthorized fields
```
