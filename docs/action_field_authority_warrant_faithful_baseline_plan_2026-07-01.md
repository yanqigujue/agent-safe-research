# Faithful Baseline Plan for AFW V2

Date: 2026-07-01

## Purpose

The current deterministic results compare against useful but partly synthetic baselines. The next credibility step is to avoid strawmen. This plan defines faithful or faithful-style baselines and what each can and cannot prove.

## Baseline Principles

1. Do not claim official prior-work failure unless we run official code or reproduce the published algorithm faithfully.
2. If a baseline asks a different question, label it as a discriminator, not a failed system.
3. Prefer baselines that are stronger than permission-only and attribution-only.
4. Report both what the baseline checks and what AFW additionally checks.

## Baseline B1: Boundary-Scope-Only

Status: implemented.

What it checks:

- field,
- operation,
- data scope,
- effect scope,
- delegation scope.

What it ignores:

- semantic role.

Why it matters:

This is the strongest current baseline because it approximates consent/scope/boundary guards. The 8-row boundary-role family is designed so this baseline has all boundary information it needs, yet still false-allows role laundering.

Current result on 40-row seed:

```text
legal_preservation = 1.0
laundering_reject = 0.65
false_allow = 0.35
```

Interpretation:

> Boundary correctness is not semantic-role validity.

## Baseline B2: AuthGraph-Style Parameter Provenance

Status: implemented faithful-style discriminator.

What to implement:

Represent a dual graph:

```text
authorization graph:
  source -> allowed tool/parameter/data path

execution graph:
  source -> actual tool/parameter/data path
```

Decision:

```text
allow iff every parameter-source edge in execution graph is authorized
```

Scope:

- parameters,
- tool arguments,
- ordinary data-source provenance.

Out of scope:

- whether a source has semantic authority over approval, risk/report, side-effect release, delegation, or data-scope fields unless those are encoded as authorization nodes.

How to report:

Do not say "AuthGraph fails." Say:

> AuthGraph-style parameter provenance answers a different question. AFW adds field-role validity for non-parameter protected fields.

Needed rows:

- parameter provenance valid, but same source laundered into risk/approval;
- tool argument provenance valid, but side-effect release field lacks semantic role;
- data-source provenance valid, but delegation field lacks delegation authority.

Current implemented tests:

- authorized parameter source is allowed for a parameter field;
- unauthorized parameter source is blocked;
- valid parameter provenance does not answer a laundered non-parameter risk field.

## Baseline B3: Certificate-Shape / PCAA-Style

Status: planned discriminator, not official baseline.

What to implement:

Check whether an action contains a structured certificate with:

- actor,
- action,
- authority reference,
- approval/receipt fields,
- replay metadata.

Decision:

```text
allow iff certificate shape is complete and required receipt fields are present
```

What it ignores:

- whether the certificate payload proves the semantic role required by each protected action field.

How to report:

Do not say "PCAA fails." Say:

> AFW can be a payload semantics inside certificate-shaped actions; certificate presence alone is not a field-role proof.

Needed rows:

- certificate-shaped action with valid receipt but evidence/summary source used as approval authority;
- certificate-shaped action with valid actor/tool but risk-report source lacks risk-assessment role.

## Baseline B4: Skill Permission / SkillGuard-Style

Status: implemented faithful-style discriminator.

What to implement:

Represent a skill manifest:

```text
skill -> allowed tools
skill -> allowed reads/writes
skill -> allowed context injection
skill -> allowed side effects
```

Decision:

```text
allow iff the skill's direct effect is within manifest
```

What it ignores:

- later action fields consuming the skill output as approval, risk, delegation, or side-effect authority.

How to report:

Do not claim official SkillGuard failure. Say:

> Skill permission controls what the skill can do; AFW controls how downstream fields consume skill-derived sources.

Needed rows:

- benign report skill allowed to format, output later consumed as risk authority;
- allowed data-cleaning skill output later consumed as delegation authority.

Current implemented tests:

- direct skill effect outside the manifest is blocked;
- direct skill effect inside the manifest is allowed even when the downstream semantic role is wrong, showing the remaining AFW delta.

## Baseline B5: Attribution-Only with Field Influence

Status: strengthened as `field_attribution_only`.

The original `attribution_only` is intentionally loose. The stronger `field_attribution_only`:

1. require every protected field to name a source;
2. reject fields with missing attribution;
3. allow fields with any attributed source.

Current implemented tests:

- missing field attribution is blocked;
- present field attribution still false-allows semantic-role laundering because source presence is not source authority.

## Baseline B6: Strict Review Gate

Status: implemented as `strict_block`.

Purpose:

Shows that blocking everything is safe but useless.

Expected result:

```text
laundering_reject = 1.0
false_block = 1.0
```

## Execution Order

1. Keep `boundary_scope_only` as the strongest implemented baseline.
2. `field_attribution_only` is implemented.
3. `authgraph_style_parameter_provenance` is implemented as a faithful-style parameter/source graph check.
4. `skill_permission_style` is implemented as a faithful-style skill manifest check.
5. Add certificate-shape discriminator only as narrative/PCAA positioning unless we can implement it faithfully.

## Reporting Table

| Baseline | Official? | Implemented? | Main question | AFW delta |
|---|---|---|---|---|
| Permission-only | no | yes | Is the source/tool allowed? | field-role validity |
| Attribution-only | no | yes | Is there source influence? | authority of the source |
| Boundary-scope-only | no | yes | Are boundaries correct? | semantic role |
| Field-attribution-only | no | yes | Does each field name a source? | source authority for that field |
| AuthGraph-style parameter provenance | faithful-style | yes | Do tool/parameter provenance edges match authorization? | non-parameter field roles |
| Skill permission-style | faithful-style | yes | Is the skill's direct effect permitted? | downstream field consumption |
| Certificate-shape / PCAA-style | discriminator only | planned | Is there a complete action certificate? | certificate payload proves field role |
| Strict-block | no | yes | Reject all protected fields | preserve legal utility |

## Success Criterion

AFW V2 becomes credible if:

1. it preserves legal use on all deterministic row families;
2. it rejects or abstains on all laundered/review rows;
3. `boundary_scope_only` still false-allows role laundering;
4. AuthGraph-style parameter provenance passes parameter rows but does not answer non-parameter role rows;
5. skill permission-style passes benign skills but does not answer downstream skill-output authority.
