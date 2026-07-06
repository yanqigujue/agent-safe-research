# AFW Formal Model

Date: 2026-07-01

This file fixes the formal object we will use for the paper and for the project implementation. It follows the current AFW evaluator in `formaltrust_platform/experiments/afw_bench.py` and the FormalTrust node/state contract in `formaltrust_platform/state.py`.

## One Sentence

AFW checks whether a source consumed by an agent action field has the semantic authority required by that field.

The paper should not say that AFW is a universal authorization system. The safe claim is narrower:

> AFW is a semantic-role witness layer for protected agent action fields.

## Core Sets

Let:

```text
S = set of agent steps
F = set of protected action fields
X = set of authority-bearing sources
R = set of semantic roles
O = set of operations
D = set of data scopes
E = set of effect scopes
G = set of delegation scopes
T = set of time scopes or policy epochs
B = set of obligations
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

The main paper should emphasize non-parameter protected fields:

```text
requires_human_approval
risk_level
risk_report
side_effect
delegation
data_read_scope
data_write_scope
```

## Source Capability

Each source is lifted into a capability object:

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
  obligations,
  provenance
)
```

Interpretation:

- `semantic_roles`: what this source is allowed to justify.
- `fields`: which action fields this source can govern.
- `operations`: which operation names are covered.
- `data_scope`: which data boundary is covered.
- `effect_scope`: which side effect or output effect is covered.
- `delegation_scope`: whether downstream delegation is covered.
- `time_scope`: valid epoch or time window.
- `obligations`: conditions that must be carried or discharged.

Important distinction:

```text
Cap(x) is not a trust score.
Cap(x) is a scoped authority type.
```

A trusted source can still fail if it is used for the wrong semantic role.

## Field Need

Each protected field in a step has an authority requirement:

```text
Need(s, f) = (
  required_roles,
  field,
  operation,
  data_scope,
  effect_scope,
  delegation_scope,
  time_scope,
  required_obligations
)
```

The current row format stores this inside:

```json
{
  "legal_consumption": {
    "field": "risk_report",
    "operation": "write",
    "need": {
      "required_role": "report_formatting_skill",
      "data_scope": "supplied_report_inputs",
      "effect_scope": "documentation_only"
    }
  }
}
```

`required_role` is a shorthand for a one-element `required_roles` list. Multi-source rows use:

```json
{
  "required_roles": [
    "approval_for_local_draft",
    "policy_allows_local_draft"
  ]
}
```

## Consumption Edge

For each step and field:

```text
Consume(x -> f, s)
```

means source `x` was used to justify or fill field `f` in step `s`.

In the deterministic AFW interface, the consumption edge is represented by:

```json
{
  "attributed_source_id": "approval_ticket_42",
  "field": "side_effect",
  "operation": "generate_local_draft",
  "need": {
    "required_role": "approval_for_local_draft"
  }
}
```

Current assumption:

- Deterministic benchmark rows provide the consumption edge directly.
- Trace scenarios provide `source_event`, `legal_event`, and `laundering_event`.
- Live systems should store extracted or model-emitted consumption edges under `state.metrics`, not as new `FormalTrustState` top-level fields.

## Coverage Relation

The central relation is:

```text
Cover(Cap(x), Need(s, f))
```

For a single required role `r`, coverage holds iff:

```text
r in Cap(x).semantic_roles
and FieldCover(Cap(x).fields, f)
and OperationCover(Cap(x).operations, Need.operation)
and DataCover(Cap(x).data_scope, Need.data_scope)
and EffectCover(Cap(x).effect_scope, Need.effect_scope)
and DelegationCover(Cap(x).delegation_scope, Need.delegation_scope)
and TimeCover(Cap(x).time_scope, Need.time_scope)
```

The current implementation has these exact predicates:

| Model predicate | Current helper |
|---|---|
| `FieldCover` | `_field_is_covered` |
| `OperationCover` | `_operation_is_covered` |
| `DataCover` | `_data_scope_is_covered` |
| `EffectCover` | `_effect_scope_is_covered` |
| `DelegationCover` | `_delegation_scope_is_covered` |
| `TimeCover` | `_time_scope_is_covered` |

Current defaults:

- Missing `data_scope` need is treated as covered.
- Missing `delegation_scope` need is treated as covered.
- Missing `time_scope` need is treated as covered.
- Missing `effect_scope` need is not covered.
- Missing `field` or `operation` is not covered.

This default is intentionally conservative for action/effect fields while allowing rows that do not model every optional boundary.

## Valid Authority

For a field with one or more required roles:

```text
ValidAuthority(s, f) =
  for every r in Need(s, f).required_roles:
    exists x in ConsumedSources(s, f):
      CoverRole(Cap(x), r, Need(s, f))
```

This permits conjunctive multi-authority:

```text
user approval covers role approval_for_local_draft
policy evidence covers role policy_allows_local_draft
------------------------------------------------------
the field can be valid when both roles are required
```

It does not permit role amplification:

```text
role r not in union_x Cap(x).semantic_roles
-------------------------------------------
Need(s, f) requiring r cannot be satisfied
```

## Decisions

AFW returns:

```text
allow | block | abstain
```

Decision rule:

```text
if not ValidAuthority(s, f):
  block
else if obligations are enforced and inherited obligations are unsatisfied:
  block
else if counter-authority applies:
  abstain
else:
  allow
```

`abstain` means positive authority exists, but a review gate, conflict, missing receipt, or counter-policy prevents silent pass-through.

## Obligation Semantics

Each consumed capability may carry obligations:

```text
Consume(x -> f, s) and b in Cap(x).obligations
----------------------------------------------
b is inherited by field f
```

Current supported obligation modes:

```text
must_discharge:
  b must be in consumption.discharged_obligations

may_carry_forward:
  b may be in consumption.carried_obligations or consumption.discharged_obligations
```

String obligations default to `may_carry_forward`.

This is implemented by:

```text
_witness_obligation_specs
_undischarged_obligations
_obligations_missing
```

## Minimal Authority Witness

For each field, AFW computes:

```text
Witness(s, f) = min X_f such that X_f covers Need(s, f)
```

Current witness object:

```json
{
  "covers_need": true,
  "capability_indexes": [0, 1],
  "covered_roles": {
    "approval_for_local_draft": 0,
    "policy_allows_local_draft": 1
  },
  "missing_roles": [],
  "obligations": [
    "do_not_publish",
    "requires_separate_publish_approval"
  ],
  "undischarged_obligations": []
}
```

Audit compression:

```text
compression_ratio = 1 - |WitnessCapabilities| / |AllCapabilities|
```

The current summary key is:

```text
legal_witness_compression_rate
```

This gives the paper a measurable audit object rather than only an allow/block classifier.

## Semantic-Role Laundering

The primary threat is:

```text
same source x
legal field f1: Cover(Cap(x), Need(s, f1)) = true
laundered field f2: Cover(Cap(x), Need(s, f2)) = false
```

The strongest special case is boundary-preserving role mismatch:

```text
field, operation, data_scope, effect_scope, delegation_scope, time_scope all match
semantic role does not match
```

Example:

```text
report-formatting skill
  can write a formatted report section
  cannot set a risk conclusion requiring risk_assessment_authority
```

This is the main novelty target. Scope, time, obligation, and counter-authority checks support the framework, but the headline is semantic-role laundering.

## Trace-Derived Mutation

Given a valid trace event:

```text
legal_event = (field, operation, source_id, data_scope, effect_scope, role)
```

a role-confusion mutation creates:

```text
laundered_event = same legal_event except required_role is replaced
```

Current generator:

```text
generate_authority_confusion_rows(path)
```

Current mutation type:

```text
boundary_preserving_semantic_role_mutation
```

This is the path from hand-authored rows to trace-derived rows.

## FormalTrust Mapping

AFW should map into FormalTrust without adding new top-level state fields.

| AFW object | FormalTrust placement |
|---|---|
| source event / source metadata | `state.retrieval_context[].metadata` or `state.metrics["afw_sources"]` |
| candidate action fields | `state.metrics["candidate_action"]` |
| final gated action | `state.metrics["final_action"]` |
| source capabilities | `state.metrics["afw_capabilities"]` |
| consumption edges | `state.metrics["afw_consumptions"]` |
| field needs | `state.metrics["afw_needs"]` |
| verifier decision | `state.metrics["afw_decision"]` or per-field `state.metrics["afw_field_results"]` |
| minimal witnesses | `state.metrics["afw_witnesses"]` |
| large trace dumps | `state.artifacts["afw_trace_path"]` |

Node contract:

```python
def afw_gate_node(state: FormalTrustState, config: Mapping[str, Any]) -> dict[str, Any] | None:
    return {
        "metrics": {
            "afw_field_results": field_results,
            "gate_decision": gate_decision,
            "final_action": final_action,
        }
    }
```

Normal safety blocks should be returned as metrics and final actions, not raised as runtime errors.

## Invariants

These invariants should be enforced by tests:

1. A row must have exactly one legal consumption and one laundered consumption.
2. `capability` or `capabilities` must be expressible as `Cap(x)`.
3. Legal consumption must preserve utility for CapGuard unless the row is intentionally negative.
4. Laundered consumption must be rejected by CapGuard as `block` or `abstain`.
5. `boundary_scope_only` must false-allow the role-only discriminator family.
6. `field_attribution_only` must not prove semantic authority.
7. `authgraph_style_parameter_provenance` must be treated as a parameter-source baseline, not an official AuthGraph result.
8. `skill_permission_style` must distinguish direct skill permission from downstream field consumption.
9. Witness objects must report missing roles rather than only a generic block.
10. Obligation enforcement must distinguish `must_discharge` from `may_carry_forward`.

## Current Status

Current implementation artifacts:

- evaluator: `formaltrust_platform/experiments/afw_bench.py`
- regression tests: `tests/test_afw_bench.py`
- deterministic row files: `examples/afw_*.json`
- current validation: `pytest tests\test_afw_bench.py -q` gives 33 passing tests.

