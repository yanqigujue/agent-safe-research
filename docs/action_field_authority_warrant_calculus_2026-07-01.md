# Action-Field Authority Warrant Calculus

Date: 2026-07-01

## Goal

Define a unified field-authority calculus for agents whose action fields consume heterogeneous sources:

- retrieved evidence,
- skill instructions and skill outputs,
- tool or MCP metadata,
- memory,
- user approvals,
- prior step outputs,
- system/developer/user instructions.

The calculus is intentionally narrower than a general agent-security framework. It checks whether protected action fields consumed authority sources that are valid for the field's semantic role.

## Objects

### Capability

Each source is lifted into a scoped capability:

```text
Cap(x) = (
  source_id,
  source_type,
  semantic_roles,
  fields,
  operations,
  data_scope,
  effect_scope,
  delegation_scope,
  time_scope,
  provenance,
  obligations
)
```

`Cap(x)` is not a trust score. It is the set of roles and scopes in which the source may be consumed.

### Field Need

Each protected action field has an authority requirement:

```text
Need(s, f) = (
  required_roles,
  field,
  operation,
  data_scope,
  effect_scope,
  delegation_scope,
  time_scope,
  obligations
)
```

Protected fields include:

```text
decision
tool
parameters
data_read_scope
data_write_scope
side_effect
requires_human_approval
risk_level
risk_report
delegation
```

The current paper should emphasize non-parameter protected fields:

```text
approval, risk/report, side-effect release, delegation, data scope
```

### Consumption Edge

For a step `s`, define a source-to-field consumption edge:

```text
Consume(x -> f, s)
```

This edge says that source `x` was used to justify or fill field `f` in step `s`.

## Validity Rule

A field is valid when every required semantic role is covered by at least one consumed capability:

```text
ValidAuthority(s, f) =
  for every role r in Need(s, f).required_roles:
    exists source x:
      Consume(x -> f, s)
      and r in Cap(x).semantic_roles
      and FieldCover(Cap(x), Need(s, f))
      and OperationCover(Cap(x), Need(s, f))
      and DataCover(Cap(x), Need(s, f))
      and EffectCover(Cap(x), Need(s, f))
      and DelegationCover(Cap(x), Need(s, f))
      and TimeCover(Cap(x), Need(s, f))
```

The current implemented slice checks:

```text
semantic_roles
fields
operations
data_scope
effect_scope
delegation_scope
time_scope
multi-source required_roles
```

## Core Rules

### R1: Same-Source Validity

The same source may be valid for one field and invalid for another:

```text
Cap(x) covers Need(s, f1)  => valid x -> f1
Cap(x) not covers Need(s, f2)  => invalid x -> f2
```

This is the benchmark's main contrast.

### R2: No Role Amplification

A transformation or composition may attenuate authority but must not create a semantic role absent from all consumed capabilities:

```text
role r not in union_i Cap(x_i).semantic_roles
------------------------------------------------
{x_i} cannot satisfy Need(s, f).required_roles containing r
```

Example:

```text
approval_for_local_draft + policy_allows_local_draft
  cannot imply approval_for_external_publish
```

### R3: Conjunctive Multi-Authority

Some fields require multiple semantic roles:

```text
Need(s, f).required_roles = [r1, r2, ..., rk]
```

The field is valid only if every required role is covered:

```text
forall r_j, exists Cap(x_i) covering r_j under the field's scope.
```

This supports cases where user approval and policy evidence jointly authorize a field.

### R4: Scope Attenuation

Derived artifacts inherit at most the authority of their source chain unless a new authority source explicitly adds a role:

```text
Cap(transform(x)) <= Cap(x)
```

Skill output can summarize an artifact without becoming approval, risk-gate, publication, or delegation authority.

Current regression rows instantiate this as:

- an approval-record summary preserves documentation authority but not approval-granting authority;
- an analysis skill output preserves analysis context but not delegation authority.

### R5: Counter-Authority

If a consumed source covers the required role but another valid source denies the field, the verifier must not silently pass:

```text
CounterAuthority(s, f) = present
--------------------------------
Verify(s, f) = block or abstain
```

The current implemented slice supports field/effect-scoped counter-authority and returns `abstain` when it applies.

### R6: Obligation Preservation

If a capability is consumed, its obligations become obligations of the action field:

```text
Consume(x -> f, s) and o in Cap(x).obligations
----------------------------------------------
o in FieldObligations(s, f)
```

Example: `requires_separate_publish_approval` must survive when local-draft approval is used.

Current implemented slice:

```text
if row.enforce_obligations
and inherited obligation o is not satisfied under its mode
then Verify(s, f) = block
```

Supported modes:

```text
must_discharge:
  o must appear in discharged_obligations

may_carry_forward:
  o may appear in carried_obligations or discharged_obligations
```

String obligations default to `may_carry_forward`.

### R7: Minimal Authority Witness

For each field, AFW can return a minimal witness set:

```text
min X_f such that X_f covers Need(s, f)
```

The witness reports:

- which capability indexes are necessary;
- which required roles they cover;
- which roles remain missing;
- which obligations are inherited from the witness capabilities.
- how much capability context is irrelevant to the minimal witness.

This makes the verifier auditable. A reviewer does not need the full trace to see why a field passed or failed; they can inspect the smallest authority subset that justifies the field.

Audit compression:

```text
compression_ratio = 1 - |WitnessCapabilities| / |AllCapabilities|
```

This is currently reported as `legal_witness_compression_rate` in evaluator summaries.

## Verifier Algorithm

```text
Input:
  step s
  protected fields F_s
  source set X_s
  consumption edges Consume(x -> f, s)
  capability adapters Lift(source) -> Cap(x)
  field policy Need(s, f)

For each protected field f in F_s:
  1. collect consumed sources X_f = {x | Consume(x -> f, s)}
  2. lift each source x to Cap(x)
  3. instantiate Need(s, f)
  4. solve the coverage query for every required role and scope dimension
  5. compute the minimal authority witness for the field
  6. attach inherited obligations from the witness
  7. check counter-authority
  8. return allow, block, or abstain with witness and missing dimensions

Step passes iff all protected fields pass or all unresolved fields are explicitly routed to review.
```

## Source Adapters

The unification comes from adapters that lift heterogeneous sources into the same `Cap(x)` shape:

| Source family | Typical roles | Role limits |
|---|---|---|
| Evidence | evidence_for_decision, evidence_for_parameter_bound, evidence_for_simulation_routing | not approval, not risk-gate authority by default |
| Skill | report_formatting_skill, data_cleaning_skill, task_folder_reader | not external side-effect authority unless explicitly granted |
| Tool metadata | schema_argument_source, enum_value_source, usage_description | not policy approval or human consent |
| Memory | preference_source, personalization_source | not safety-policy authority by default |
| User approval | approval_for_exact_effect | effect-scope and time-scope limited |
| Prior output | artifact_content_source | not new filesystem/network/delegation authority |
| System/developer instruction | policy_source, hard_constraint_source | can override lower-priority sources depending on policy |

Current implemented adapter seeds:

```text
skill_manifest -> Cap(skill_output)
authority_manifest -> Cap(source)
```

The adapter uses explicit manifest fields only:

```text
output_semantic_roles -> semantic_roles
allowed_fields -> fields
allowed_operations -> operations
allowed_data_scope -> data_scope
allowed_effect_scope -> effect_scope
allowed_delegation_scope -> delegation_scope
output_obligations -> obligations
```

The generic adapter uses the same target shape:

```text
semantic_roles -> semantic_roles
fields -> fields
operations -> operations
data_scope -> data_scope
effect_scope -> effect_scope
delegation_scope -> delegation_scope
obligations -> obligations
```

These are conservative source adapters. They do not infer authority from free-text descriptions unless a manifest has already declared the role and scope.

## Current Implementation Slice

Implemented in:

- `formaltrust_platform/experiments/afw_bench.py`
- `tests/test_afw_bench.py`

Supported today:

- single-source same-source contrast,
- permission-only baseline,
- attribution-only baseline,
- strict-block baseline,
- field-family breakdown,
- multi-capability rows,
- conjunctive `required_roles`,
- no role amplification under role/field/operation/data/effect/delegation coverage.
- time-scope coverage for explicit capabilities and field needs.
- field/effect-scoped counter-authority with `abstain`.
- derived-artifact authority attenuation through role/scope coverage.
- trace-derived authority-confusion generation.
- minimal authority witness extraction with covered roles, missing roles, and inherited obligations.
- skill-manifest and generic authority-manifest capability inference when explicit `capability` annotations are absent.
- obligation discharge enforcement for rows with `enforce_obligations`.

Not implemented yet:

- richer obligation policies beyond `must_discharge` and `may_carry_forward`,
- concrete source adapters for tool metadata, memory, prior-step outputs, system/developer instructions, and time-scoped manifests,
- richer counter-authority reasoning,
- extracted consumption edges from live traces.

## Why This Is an Algorithmic Contribution

The algorithmic object is not a new prompt, policy checklist, or generic access-control rule.

It is a field-level authority type check:

```text
source capability type <= field requirement type
```

with:

- same-source contrast,
- source-family adapters,
- conjunctive multi-authority,
- no role amplification,
- obligation propagation,
- counter-authority handling.
- minimal authority witnesses.
- witness audit-compression metrics.
- source adapters that lift trace metadata into `Cap(x)`.

This is the right level of abstraction for a unified RAG/skill/tool/memory/approval safety story while still staying narrower than broad agent authorization.
