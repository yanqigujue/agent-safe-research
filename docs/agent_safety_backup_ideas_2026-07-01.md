# Backup Ideas Beyond AFW V2

Date: 2026-07-01

## Purpose

AFW V2 is the current main line, but a publishable project should keep backup paths. These ideas are adjacent enough to reuse current assets, but distinct enough that the project can pivot if reviewers decide semantic-role warrants are too close to authorization/provenance work.

## Backup Idea 1: Authority Type Inference From Agent Traces

### Pain Point

AFW assumes source capabilities are known. In real agents, source authority is implicit: skill outputs, tool descriptions, memory entries, approval dialogs, and retrieved snippets rarely come with clean `Cap(x)` annotations.

### Innovation

Infer authority types from traces:

```text
trace event -> candidate Cap(x)
```

Use a small authority ontology:

- documentation source,
- parameter evidence,
- approval authority,
- risk-gate authority,
- side-effect release authority,
- delegation authority,
- data-access authority.

Then verify whether inferred capabilities match downstream field consumption.

### Minimum Experiment

Collect or synthesize 50 structured traces. Compare:

- human-labeled `Cap(x)`;
- LLM-inferred `Cap(x)`;
- rule-based source-type heuristic.

Metric:

- role inference accuracy;
- downstream verification accuracy;
- false authority amplification.

### Strongest Rejection

This becomes an extraction/annotation paper rather than a safety mechanism paper. Reviewers may say the core verifier is assumed and the inference task is just classification.

### Survival Condition

It survives only if inferred authority types expose failures that raw source type or attribution cannot.

### Current Seed Status

A conservative manifest-lift seed is implemented as `infer_capability_from_trace_scenario`.

Current behavior:

- a skill manifest with explicit `output_semantic_roles` and allowed scopes is lifted into `Cap(skill_output)`;
- a generic `authority_manifest` can lift non-skill sources such as user approvals into `Cap(source)`;
- the trace adapter can use the inferred capability when a scenario lacks a hand-authored `capability`;
- the generated `Cap(x)` still blocks downstream role laundering because it carries only the declared roles.

This is not a full inference system yet. It is the first practical adapter showing where `Cap(x)` can come from in skill-driven and approval-driven agent traces.

## Backup Idea 2: Authority-Confusion Fuzzing From Real Traces

### Pain Point

Hand-authored safety rows are vulnerable to the critique that the verifier encodes the labels. We need a generator that mutates real traces into boundary-preserving authority confusions.

### Innovation

Given a valid trace, mutate one dimension while holding others fixed:

```text
role mutation
operation mutation
data-scope mutation
effect-scope mutation
delegation-scope mutation
time-scope mutation
counter-authority insertion
```

The key generator is role mutation with boundary preservation:

```text
field/operation/data/effect/delegation unchanged
required_role changed
```

### Minimum Experiment

Start from 20 trace-derived legal actions and generate 5 mutations each. Evaluate:

- CapGuard,
- boundary-scope-only,
- field-attribution-only,
- skill-permission-style.

Metric:

- mutation validity rate;
- nontrivial false-allow rate;
- human audit agreement.

### Strongest Rejection

Generated attacks may be artificial and circular: the generator creates exactly what CapGuard detects.

### Survival Condition

Use real traces as seeds and human audit to show mutations are plausible agent errors, not arbitrary label flips.

### Current Seed Status

A minimal seed is implemented in `examples/afw_trace_scenarios.json` and `generate_authority_confusion_rows`.

Current generated row:

```text
TRACE-SKILL-REPORT-RISK-LAUNDER::risk_assessment_from_formatting
```

It preserves field, operation, attributed source, data scope, and effect scope from the legal trace event, while mutating only:

```text
required_role: report_formatting_skill -> risk_assessment_authority
```

This is still far from the 20-trace target, but it proves the route from structured trace to adversarial authority-confusion row.

## Backup Idea 3: Obligation-Carrying Skill Outputs

### Pain Point

Skill outputs often carry implicit obligations: cite source, do not publish, require scan, do not delegate. Existing skill permission frameworks focus on what a skill can do, not what obligations its outputs impose downstream.

### Innovation

Attach obligations to skill-derived artifacts and propagate them to downstream fields:

```text
Consume(skill_output -> field)
  => obligations(skill_output) subset obligations(field)
```

Violation occurs when a downstream field consumes the artifact but drops required obligations.

### Minimum Experiment

Construct skill traces where outputs include obligations:

- `do_not_publish`,
- `requires_scan`,
- `cite_source`,
- `do_not_delegate`,
- `human_review_required`.

Compare:

- skill permission,
- attribution,
- obligation-carrying verifier.

### Strongest Rejection

This may be seen as ordinary policy propagation or proof-carrying action payload design.

### Survival Condition

Needs concrete skill-output traces and evidence that obligations are lost in common agent workflows.

### Current Seed Status

A minimal obligation-discharge slice is implemented in `examples/afw_obligation_rows.json`.

Current behavior:

- a capability can carry inherited obligations such as `requires_static_scan` or `requires_dlp_scan`;
- if `enforce_obligations` is enabled, CapGuard blocks a field whose role and scope are valid but whose inherited obligations are not satisfied under their mode;
- `must_discharge` obligations require local discharge, while `may_carry_forward` obligations may be carried forward;
- row results expose `undischarged_obligations` through the authority witness.

This keeps obligation-carrying skill outputs as a supporting mechanism inside AFW rather than a standalone skill-security paper.

## Backup Idea 4: Authority Decay and Revocation for Agent Memory

### Pain Point

Agent memory persists authority-like facts after their valid time, policy epoch, or user intent expires. Memory may be correct historically but invalid currently.

### Innovation

Represent capability as time- and epoch-scoped:

```text
Cap_t(x) = Cap(x) under time_scope, policy_epoch, revocation_log
```

Detect when memory is reused after decay or revocation.

### Minimum Experiment

Rows/traces where memory is valid at `t0` and invalid at `t1`:

- approval expired;
- policy version changed;
- user preference revoked;
- file access ticket revoked;
- environment observation stale.

### Strongest Rejection

EnvTrustBench, memory authority, and contextual security already cover stale or poisoned memory.

### Survival Condition

Frame as an AFW dimension or trace adapter extension, not standalone unless memory traces are strong.

### Current Seed Status

A minimal temporal slice is implemented in `examples/afw_temporal_rows.json`.

Current behavior:

- explicit capability `time_scope` must cover the field need's `time_scope`;
- expired approval is blocked when a Q3 publish approval is reused for Q4 publication;
- stale memory is blocked when an epoch-7 preference is reused for an epoch-8 rewrite;
- this remains a supporting AFW coverage dimension, not a standalone memory-security claim.

## Backup Idea 5: Minimal Authority Witness Extraction

### Pain Point

Agent traces can contain many sources. Auditors need the smallest witness set that justifies each field, not a full context dump.

### Innovation

Compute:

```text
min X_f such that X_f covers Need(s,f)
```

and mark surplus sources or missing minimal witnesses.

### Minimum Experiment

Given 100 multi-source traces, compare:

- full attribution context,
- top-k attribution,
- minimal authority witness.

Metric:

- audit token reduction;
- preserved verification accuracy;
- missing-authority detection.

### Strongest Rejection

This could be provenance summarization, not safety.

### Survival Condition

Needs a measured audit-cost reduction and a case where minimal witnesses change accept/reject decisions.

### Current Seed Status

A minimal witness extractor is implemented as `find_minimal_authority_witness`.

Current behavior:

- legal composite fields return the smallest capability indexes that cover all required roles;
- laundered fields return missing roles rather than a generic block;
- witness obligations are surfaced for audit.
- witness audit summaries report full capability count, witness count, irrelevant capability count, and compression ratio.

This does not yet prove human audit-time reduction, but it turns AFW decisions into inspectable proof objects with a measurable context-compression proxy.

## Backup Ranking

| Rank | Idea | Why |
|---:|---|---|
| 1 | Authority-confusion fuzzing from real traces | Best complement to AFW; attacks the synthetic-row critique. |
| 2 | Authority type inference from traces | Solves AFW's biggest deployment assumption: where `Cap(x)` comes from. |
| 3 | Obligation-carrying skill outputs | Strong skill-specific pivot; reuses attenuation/counter-authority logic. |
| 4 | Minimal authority witnesses | Useful if audit-cost result is strong. |
| 5 | Authority decay and revocation | Implemented as a small AFW dimension; still crowded as a standalone paper. |

## Current Recommendation

Do not pivot away from AFW V2 yet.

Instead, attach two backup ideas as future-proofing:

1. **Trace-derived authority-confusion fuzzing** as the benchmark generator.
2. **Authority type inference** as the practical extraction layer.

This makes the full project story:

```text
AFW = verifier / safety object
Trace adapter = how rows come from agent behavior
Authority fuzzing = how to scale evaluation
Authority inference = how to get Cap(x) in practice
```

That is a stronger research program than any one piece alone, while the first paper can still stay focused on AFW V2.
