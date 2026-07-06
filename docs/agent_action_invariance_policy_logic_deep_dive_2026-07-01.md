# Agent Action Invariance: Policy-Logic Deep Dive

Date: 2026-07-01

This note continues the search for traditional formal theories that can support AFW / CapGuard. The focus here is not control, but policy logic:

- deontic logic,
- XACML-style multi-valued access decisions,
- Belnap four-valued policy composition,
- obligation/advice semantics,
- conflict and incompleteness.

Bottom line:

> These theories are useful for formalizing `allow / block / abstain`, obligations, and counter-authority. They are not the main novelty. The main novelty should remain field-level authority witnesses and fieldwise action invariance.

## 1. Why Policy Logic Matters

CapGuard already outputs:

```text
allow
block
abstain
```

The current interpretation is:

```text
allow:
  valid authority witness exists and no blocking obligation/counter-authority applies

block:
  authority coverage is missing or a must-discharge obligation is unsatisfied

abstain:
  positive authority may exist, but conflict/counter-authority/missing receipt means the system should not silently proceed
```

This resembles mature access-control decision models:

```text
Permit
Deny
NotApplicable
Indeterminate
```

However, AFW should not collapse into XACML-style access control because AFW's object is different:

```text
XACML:
  Does this subject/action/resource request satisfy a policy?

AFW:
  Did this concrete action field consume a source that has the semantic role needed by that field?
```

## 2. Deontic Logic

Deontic logic models normative concepts:

```text
P(phi): phi is permitted
F(phi): phi is forbidden
O(phi): phi is obligatory
```

AFW mapping:

```text
P(execute field f):
  ValidAuthority(s,f) and no counter-authority

F(execute field f):
  missing role/scope/time/obligation or explicit counter-authority

O(review field f):
  abstain or must_discharge obligation is unresolved
```

Useful source:

- Stanford Encyclopedia of Philosophy, "Deontic Logic". <https://plato.stanford.edu/archives/spr2021/entries/logic-deontic/>
- Deontic logic for access/security policy consistency. <https://www.cs.columbia.edu/~locasto/projects/spcl/docs/research/laurence97analyzing.pdf>

How to use it:

```text
Use deontic logic as background vocabulary for permission, prohibition, and obligation.
Do not present AFW as a new deontic logic.
```

## 3. XACML-Style Multi-Valued Decisions

XACML standardizes access-control decisions such as:

```text
Permit
Deny
NotApplicable
Indeterminate
```

Useful sources:

- OASIS XACML 3.0 core specification. <https://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-cs-01-en.html>
- "The Logic of XACML - Extended". <https://arxiv.org/abs/1110.3706>

AFW mapping:

| XACML-like decision | AFW analogue | Meaning |
|---|---|---|
| Permit | `allow` | field has valid witness |
| Deny | `block` | witness missing or hard obligation failed |
| NotApplicable | `no protected field / no relevant need` | outside AFW's field object |
| Indeterminate | `abstain` | uncertainty, conflict, counter-authority, missing receipt |

But keep the distinction:

```text
XACML combines policies over access requests.
AFW checks authority consumption over action fields.
```

## 4. Belnap Four-Valued Logic

Belnap-style policy semantics often use four values:

```text
grant
deny
conflict
unspecified
```

Useful sources:

- "Access control via Belnap logic: Intuitive, expressive, and analyzable policy composition". <https://dl.acm.org/doi/10.1145/1952982.1952991>
- Technical report version. <https://www.doc.ic.ac.uk/research/technicalreports/2011/DTR11-6.pdf>

AFW mapping:

```text
grant:
  positive authority witness covers Need(s,f)

deny:
  capability explicitly excludes or counter-authority denies field/effect

conflict:
  positive authority and counter-authority both apply

unspecified:
  no source covers the required role/scope
```

AFW current decision collapse:

```text
grant       -> allow
deny        -> block or abstain depending on policy mode
conflict    -> abstain
unspecified -> block
```

This is useful because it explains why `abstain` is not just "weak block":

> `abstain` is the runtime analogue of a conflict/indeterminate decision that should be routed to a higher-authority reviewer.

## 5. Obligation Semantics

XACML policies can carry obligations and advice. AFW also carries obligations in `Cap(x)` and witness objects.

AFW modes:

```text
must_discharge:
  obligation must be locally discharged before field executes

may_carry_forward:
  obligation may be carried or discharged
```

Policy-logic interpretation:

```text
P(execute f) is conditional on O(discharge b) being satisfied.
If O(discharge b) is unsatisfied, P(execute f) is suspended or denied.
```

Why it helps:

- Makes obligation-carrying warrants look less ad hoc.
- Supports a clean distinction between missing authority and missing obligation discharge.
- Explains why an otherwise valid authority witness can still block.

## 6. Counter-Authority

Counter-authority can be modeled as explicit negative evidence or a conflicting policy fact:

```text
PositiveAuthority(s,f)
CounterAuthority(s,f)
--------------------------------
decision = abstain or block
```

Policy-logic view:

```text
grant + conflict -> indeterminate/abstain
grant + explicit deny -> deny/block under deny-overrides
```

AFW should expose which policy mode is used:

```text
conflict_route_to_review:
  conflict -> abstain

deny_overrides:
  counter-authority -> block

permit_overrides:
  only valid for low-risk informational fields, if ever
```

This could become a future configuration dimension, but not a main current claim.

## 7. Relation To Action Invariance

Policy logic helps define exact categories for fieldwise invariance:

```text
Preserve field:
  grant / allow

Suppress field:
  unspecified / missing authority

Route field:
  conflict / indeterminate

Repair field:
  deny or missing hard obligation with safe fallback
```

Thus:

```text
Fieldwise maximal permissiveness
  = preserve all grant fields
    suppress or route all non-grant fields
```

This makes the action-invariance story more rigorous:

> The guard is not merely conservative. It is a decision-preserving transformer over fields with explicit grant/conflict/unspecified semantics.

## 8. Possible Extension: Decision Lattice

Define an AFW decision lattice:

```text
bottom: no_applicable_need
grant: allow
missing: block_missing_authority
conflict: abstain_counter_authority
obligation_gap: block_or_abstain_obligation
top: inconsistent_policy_state
```

Potential orderings:

```text
truth / safety order:
  block <= abstain <= allow

information order:
  no_applicable_need <= missing/conflict/obligation_gap <= explicit allow/deny
```

This is inspired by Belnap logic, but should be presented as an engineering diagnostic lattice, not a new logic.

## 9. Candidate Paper Use

Use this material in:

```text
Method appendix:
  explain allow/block/abstain and obligations

Threat model:
  distinguish missing authority from conflicting authority

Experiment:
  count block vs abstain separately

Related work:
  acknowledge XACML, deontic logic, Belnap policy composition
```

Do not use it as:

```text
main novelty claim
```

## 10. Claim Firewall

Do not claim:

- first multi-valued access-control decision;
- first use of deontic logic for security policy;
- first obligation-carrying authorization model;
- first policy-composition semantics;
- first conflict-aware access-control logic.

Safe claim:

> AFW reuses mature policy-logic ideas to make field-level authority decisions auditable, but its contribution is the action-field authority witness and the preservation of witness-backed fields under supervision.

## 11. Updated Direction Ranking Impact

This deep dive does not change the main ranking.

| Direction | Effect of policy-logic deep dive |
|---|---|
| Fieldwise maximally permissive CapGuard | strengthened by clearer decision categories |
| Fieldwise Simplex | strengthened by route/repair/suppress taxonomy |
| Obligation-carrying warrants | strengthened by deontic obligation framing |
| Counter-authority abstain | strengthened by Belnap/XACML conflict semantics |
| Policy-logic contribution | keep as appendix/background only |

