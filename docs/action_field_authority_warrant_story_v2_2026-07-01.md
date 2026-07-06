# AFW Story V2: Semantic Role After Boundaries

Date: 2026-07-01

## Why V2 Is Needed

The original AFW story was:

> each protected field must consume a valid authority source.

That is directionally right but too close to authorization, provenance, proof-carrying action, consent, and skill-permission work.

The stronger V2 story is:

> Even after provenance, permission, consent scope, and boundary checks are satisfied, agents can still launder a source into a semantic role it does not carry.

This is sharper because it does not rely on weak baselines.

## Working Title

**Semantic-Role Warrants for Agent Action Fields**

Alternative:

**Beyond Scope Checks: Detecting Semantic-Role Laundering in Agent Actions**

## Core Thesis

Protected agent action fields require semantic-role warrants, not only provenance, permission, or boundary-scope validity.

AFW verifies:

```text
Cap(x) covers Need(s, f)
```

where coverage includes:

- semantic role,
- field,
- operation,
- data scope,
- effect scope,
- delegation scope,
- time scope,
- counter-authority.

## Three Differentiators

### D1: Boundary-Preserving Role Mismatch

Pain:

A source may satisfy field, operation, data, effect, delegation, and any specified time boundaries while still lacking the semantic role required by the field.

Example:

```text
report_formatting_skill
  field = risk_report
  operation = write
  data_scope = supplied_report_inputs
  effect_scope = documentation_only

Legal:
  required_role = report_formatting_skill

Laundered:
  required_role = risk_assessment_authority
```

Why it matters:

This beats a stronger baseline than permission-only:

```text
boundary_scope_only: allow
CapGuard: block
```

### D2: Derived-Artifact Authority Attenuation

Pain:

Agent artifacts are transformed across steps. A summary, skill output, extracted table, or compressed trace should not inherit all authority from its original source.

Rule:

```text
Cap(transform(x)) <= Cap(x)
```

Examples:

- approval-record summary supports documentation but not approval waiver;
- skill output supports analysis context but not delegation;
- retrieved evidence summary supports reporting but not publication.

### D3: Compositional Authority Without Role Amplification

Pain:

Real fields often require several authorities, e.g. user approval plus policy. But combining limited authorities must not synthesize new roles.

Rule:

```text
Need(s,f).required_roles = [r1, r2, ...]

valid iff every required role is covered
and no uncovered role is created by composition
```

Example:

```text
approval_for_local_draft + policy_allows_local_draft
  => local_draft allowed
  != external_publish allowed
```

## Paper Claims

| Claim | Evidence now | Evidence needed |
|---|---|---|
| C1: Semantic-role laundering survives boundary checks. | `boundary_scope_only` role-only discriminator passes tests on 8 boundary-preserving role-mismatch rows. | Expand beyond 8 rows only after adding real traces or harder mixed cases. |
| C2: Derived artifacts must attenuate authority. | 8 attenuation rows pass tests across summary, skill output, translation, extraction, compression, merge, ranking, and code preview. | Add real traces or harder mixed transformation chains. |
| C3: Multi-source authority must be conjunctive and non-amplifying. | 8 composite rows pass tests. | Add partial-coverage and real trace rows. |
| C4: Counter-authority needs abstain/review, not only allow/block. | 6 counter-authority rows pass tests. | Add richer obligation propagation beyond field/effect matching. |

## Main Tables

### Table 1: Baseline Contrast

| Baseline | Checks | Expected failure |
|---|---|---|
| permission-only | whether source/tool is allowed | misses all role laundering |
| attribution-only | whether source influenced field | misses authority validity |
| boundary-scope-only | field/operation/data/effect/delegation boundaries | misses pure semantic-role mismatch |
| strict-block | blocks protected fields | loses legal utility |
| CapGuard | semantic role plus boundaries plus counter-authority | preserves legal use and blocks laundering |

### Table 2: Discriminator Families

| Family | Example | Closest neighbor pressure |
|---|---|---|
| Same-source cross-field | policy evidence routes simulation but cannot waive approval | RAG attribution, AuthGraph |
| Boundary-preserving role mismatch | report formatter is not risk assessor | consent/scope guards |
| Derived-artifact attenuation | summary is not approval authority | memory authority, authorization propagation |
| Composite non-amplification | local draft approval does not imply publish approval | consent integrity, protocol composition |
| Counter-authority | positive approval plus missing DLP scan -> abstain | Cordon, PCAA, pre-action authorization |

### Table 3: Coverage Dimensions

| Dimension | Implemented | Why it matters |
|---|---|---|
| semantic role | yes | core novelty |
| field | yes | prevents cross-field laundering |
| operation | yes | prevents action operation drift |
| data scope | yes | prevents data boundary drift |
| effect scope | yes | prevents side-effect drift |
| delegation scope | yes | prevents authority delegation drift |
| counter-authority | basic | routes conflicts to review |
| time scope | yes | blocks stale approval or memory reuse across policy/preference epochs |
| obligations | basic | carries or discharges inherited constraints |

## What To Cut

Cut these from the main paper:

- generic proof-carrying action claims;
- generic skill security claims;
- broad MCP protocol verification;
- full policy language or complete authorization graph;
- live-model superiority claims before official/faithful baselines exist.

## What To Keep

Keep one dominant contribution:

> semantic-role warrant checking for protected action fields.

Keep two supporting mechanisms:

1. derived-artifact authority attenuation;
2. compositional non-amplification with counter-authority abstain.

## Minimal Next Experiment

V2 seed benchmark now has 40 deterministic rows:

- 10 same-source cross-field rows; current: 10;
- 8 boundary-preserving role mismatch rows; current: 8;
- 8 derived-artifact attenuation rows; current: 8;
- 8 composite authority rows; current: 8;
- 6 counter-authority rows; current: 6.

Run:

```text
CapGuard
permission-only
attribution-only
boundary-scope-only
strict-block
```

Metrics:

- legal preservation,
- laundering block,
- laundering reject including abstain,
- false allow,
- false block,
- abstain rate,
- same-source contrast gap,
- boundary-preserving role gap.

## Final V2 Pitch

> Existing agent defenses can verify that a source is present, a tool is permitted, a user consent boundary is respected, or an action carries a certificate. We show that protected action fields still suffer semantic-role laundering: a source can satisfy all boundary scopes while lacking the role required by the field that consumes it. Semantic-role warrants check field-level authority over role, operation, data, effect, and delegation scopes, including attenuation across derived artifacts and non-amplifying composition across multiple authorities.
