# Divergent Innovation Map for Agent Safety

Date: 2026-07-01

## Purpose

The current AFW direction is promising, but the project should not tunnel on one story too early. This map expands the search space around skill-driven, RAG-driven, memory-driven, and protocol-driven agents.

The goal is to identify pain points that can support a publishable innovation, not merely rename existing authorization, provenance, or permission systems.

## Current Landscape Pressure

Recent close neighbors already occupy many obvious claims:

| Neighbor family | What it already pressures | Safe lesson |
|---|---|---|
| Proof-carrying actions / PCAA | generic action certificates, approval, authority, receipts, replay | do not claim proof-carrying firstness |
| AuthGraph / provenance authorization | authorization graph aligned with execution provenance for tools and parameter sources | do not compete on ordinary parameter provenance |
| SkillGuard / proof-carrying skills | skill permissions, skill supply-chain safety, capability containment | do not claim first skill-security framework |
| Consent integrity / scope lattices | user consent, operation boundaries, exact effect scopes | scope correctness is not enough; semantic role remains a possible delta |
| ToolPrivBench / ToolSafe | tool privilege, unsafe invocations, least-privilege tool choice | tool permission is not field-authority validity |
| MCP/runtime invariants / protocol composition | runtime safety, content-to-authority flow, protocol isolation | avoid broad authority-flow claims |
| Memory authority / origin-bound memory | memory poisoning, origin-bound authority, laundering through memory | avoid generic authority-laundering firstness |
| Contextual security | task alignment, source authorization, action/data isolation | treat AFW as a concrete field-level proof object |

## Candidate Directions

### Direction 1: Action-Field Authority Warrants

Pain point:

Agents flatten heterogeneous sources into one context, then fill protected fields such as approval, risk, side effect, delegation, and data scope.

Innovation:

Field-authority validity: each protected field must prove that the consumed source covers the field's semantic role and scopes.

Why still alive:

The strongest discriminator is no longer permission-only. It is role-only laundering: boundary scopes are correct, but semantic role is wrong.

Minimum experiment:

Same-source and boundary-scope discriminator rows:

```text
same source -> legal field      allow
same source -> role-laundered field with same boundaries  block
```

Status:

Best current direction. Implemented minimum evaluator and 14 regression tests. The current version includes a 40-row V2 seed benchmark: 10 same-source rows, 8 boundary-role rows, 8 attenuation rows, 8 composite rows, and 6 counter-authority rows.

Risk:

If reviewers treat semantic role as just another authorization attribute, novelty drops.

### Direction 2: Authority Attenuation for Derived Agent Artifacts

Pain point:

Agent artifacts are repeatedly transformed: retrieved evidence becomes summaries, skill output becomes reports, reports become plans, plans become tool calls. Authority should weaken or specialize across transformations, but agents often treat derived artifacts as if they preserve full authority.

Innovation:

Define an attenuation calculus:

```text
Cap(transform(x)) <= Cap(x)
```

and learn or verify attenuation rules for common transformations:

- summarize,
- translate,
- reformat,
- extract,
- merge,
- rank,
- compress,
- delegate.

Minimum experiment:

Create chains where source `x` legally supports an intermediate artifact, but the transformed artifact is later used as approval/risk/delegation authority.

Closest pressure:

Memory authority and protocol composition already discuss authority propagation. The delta must be transformation-specific attenuation for agent artifacts.

Risk:

May collapse into existing authorization propagation unless the transformation taxonomy and empirical traces are strong.

### Direction 3: Counter-Authority and Negative Evidence Routing

Pain point:

Current agents often ask whether enough positive support exists, but do not route negative evidence, missing receipts, policy conflicts, stale approvals, DLP gates, or unresolved obligations into an explicit review decision.

Innovation:

Make safety a three-valued decision:

```text
allow | block | abstain
```

where `abstain` is triggered by counter-authority even when positive authority exists.

Minimum experiment:

Rows where approval and policy roles are present, but a missing DLP scan or conflict forces review.

Closest pressure:

Cordon, pre-action authorization, and PCAA already carry receipts and workflow checks. The delta must be field-local counter-authority routing, not generic approval workflow.

Risk:

Could look like ordinary policy enforcement unless tied to field-level source consumption.

### Direction 4: Skill Output Declassification

Pain point:

Skill-driven agents often treat skill output as safe because the skill itself is allowed. But a skill output may contain code, plans, commands, or summaries that should be declassified before entering higher-authority fields.

Innovation:

A declassification gate for skill outputs:

```text
skill_output_role <= allowed_downstream_roles
```

The gate checks whether a skill's output can be consumed by downstream fields such as delegation, data write, deployment, or side-effect release.

Minimum experiment:

Benign report skill produces text that is later consumed as deployment/risk/delegation authority.

Closest pressure:

SkillGuard and proof-carrying skill artifacts are close. The safe delta is downstream output consumption, not skill artifact scanning.

Risk:

If phrased as skill permission, it is not novel.

### Direction 5: Consent Delta Tracking Across Multi-Step Agent Plans

Pain point:

Users approve one action, but agent plans drift. The dangerous part is often the delta between approved action and executed action, not the action itself.

Innovation:

Track consent deltas:

```text
Delta(approved_effect, executed_effect)
```

and reject or abstain when the delta crosses data, operation, audience, or persistence boundaries.

Minimum experiment:

User approves local draft; agent sends email, uploads file, or shares link after intermediate steps.

Closest pressure:

Consent integrity is extremely close. The delta must focus on multi-step plan drift and source-to-field consumption, not just final approval matching.

Risk:

May be too close to Consent Integrity unless the plan-delta benchmark is strong.

### Direction 6: Agent Capability Decay Over Time

Pain point:

Permissions, policies, approvals, memories, and environment observations become stale, but agents often reuse them indefinitely.

Innovation:

Define time-scoped authority decay:

```text
Cap_t(x) = decay(Cap(x), elapsed_time, revocation_events, policy_epoch)
```

Minimum experiment:

Same source passes before a policy update but must fail after revocation or epoch change.

Closest pressure:

EnvTrustBench and contextual security already discuss stale environmental evidence. The delta must be a general capability-decay interface across evidence, memory, approval, and skill outputs.

Risk:

Could become a simple timestamp check unless revocation and transformation are handled elegantly.

### Direction 7: Minimal Authority Witnesses for Agent Actions

Pain point:

Agent traces are huge. Auditors need the smallest set of sources that actually justify each protected field.

Innovation:

Compute a minimal authority witness:

```text
min X_f such that X_f covers Need(s,f)
```

and flag surplus or irrelevant sources as audit risk.

Minimum experiment:

Given many sources in context, identify the minimal subset needed for approval/risk/delegation fields and compare to attribution methods.

Closest pressure:

AuthGraph and provenance systems already track source-use. The delta must be minimality and field-level witness compression.

Risk:

Could look like provenance summarization unless it changes decisions or audit cost.

### Direction 8: Authority-Confusion Fuzzing for Agents

Pain point:

Security benchmarks are often manually authored. We need systematic generation of cases where sources are valid in one role but invalid in another.

Innovation:

A fuzzing generator that mutates:

- source role,
- field,
- operation,
- data scope,
- effect scope,
- delegation scope,
- time epoch,
- counter-authority.

Minimum experiment:

Generate same-source and role-only laundering cases automatically, then test agents and guards.

Closest pressure:

Agent security benchmarks are crowded. The delta is grammar-guided generation over authority dimensions, not another static benchmark.

Risk:

May be viewed as benchmark engineering unless paired with a strong method.

## Ranking

| Rank | Direction | Novelty | Pain strength | Feasibility | Paper story | Recommendation |
|---:|---|---:|---:|---:|---:|---|
| 1 | Action-Field Authority Warrants | 7 | 8 | 9 | 8 | Main line |
| 2 | Authority attenuation for derived artifacts | 7 | 8 | 9 | 8 | Folded into AFW as second mechanism layer |
| 3 | Counter-authority routing | 6 | 8 | 8 | 7 | Useful as AFW subsystem |
| 4 | Skill output declassification | 6 | 7 | 8 | 7 | Skill-focused paper possible |
| 5 | Authority-confusion fuzzing | 6 | 7 | 8 | 6 | Good benchmark companion |
| 6 | Minimal authority witnesses | 6 | 6 | 7 | 6 | Needs sharper audit-cost result |
| 7 | Consent delta tracking | 5 | 8 | 7 | 6 | Too close unless plan-drift angle is strong |
| 8 | Capability decay over time | 5 | 7 | 8 | 5 | Likely an AFW dimension, not standalone |

## Immediate Recommendation

Keep AFW as the main story, but add two innovations to prevent it from looking like a renamed authorization checker:

1. **Boundary-scope discriminator:** show that field, operation, data, effect, and delegation scopes can all match while semantic role still fails.
2. **Authority attenuation:** add derived-artifact chains where authority must not amplify across summary/format/skill-output transformations.

This gives a cleaner paper sentence:

> Existing systems can verify provenance, permission, consent scope, or action certificates, but they do not directly test whether the semantic role carried by a source is valid for the action field that consumes it, especially after sources are transformed, combined, or routed through skills.
