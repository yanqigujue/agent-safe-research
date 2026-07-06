# Iteration 023: Conservative Denial vs Executing Actions

Date: 2026-06-20

## Goal

Reduce EAIR-Full over-refusal without weakening evidence sufficiency for high-risk execution or authorization actions.

## Hypothesis

Not every oracle-shaped high-risk decision should require the same evidence threshold. A conservative denial such as `reject_bypass` with `tool="none"` is different from an execution-like action such as `route_to_simulation` or `set_parameter`.

## Implementation

- Added `is_conservative_denial_action`.
- `classify_influence` now classifies such actions as `conservative`.
- `requires_evidence_support` returns false for conservative denials.
- `is_unsupported` does not mark conservative denials unsupported merely because retrieved evidence is low-trust or single-cluster.
- Added `policy_update::near_duplicate_single_source_policy_support` so source-diverse support is still tested on an execution-like action.
- Added `over_refusal_rate` to the Markdown report table.

## TDD

Added or revised tests for:

- allowing low-trust / single-cluster `reject_bypass` conservative denials;
- still blocking single-cluster `route_to_simulation`;
- authority-control baselines missing evidence sufficiency on the execution-like near-duplicate policy case;
- report output exposing `over_refusal_rate`.

The targeted tests failed before implementation and passed after the conservative-denial rule and new case were added.

## Experiment

Reran deterministic EAIR-Bench pilot:

- conditions: 13
- baselines: 17
- results: 221
- outputs: `outputs/eair_bench_pilot/`

EAIR-Full:

- UDR: `0.0000`
- UAR: `0.0000`
- parameter violation: `0.0000`
- false positive: `0.0000`
- EATF: `1.0000`
- ORR: `0.2308`

The previous ORR was `0.3333`.

## Supported

- Separating conservative denial from execution/authorization actions reduces conservative refusal.
- The reduction did not increase unsafe decisions, unsupported final actions, parameter violations, or false positives in the deterministic pilot.
- Source-diverse evidence sufficiency remains necessary for execution-like policy actions.

## Not Yet Supported

- That every no-tool action is safe.
- That conservative denial taxonomy is complete.
- That ORR will remain lower under real LLM planners, realistic retrievers, or adversarial report/approval manipulation.

## Next Iteration

Add cases where no-tool decisions still have operational consequences:

- risk report downgrades;
- approval-flag manipulation;
- false-safe recommendation without tool execution;
- “do nothing” decisions that omit mandatory escalation.

These cases will test whether conservative denial must be narrower than `tool="none"`.
