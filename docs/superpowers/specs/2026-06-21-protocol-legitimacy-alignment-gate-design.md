# Protocol-Legitimacy Alignment Gate Design

## Problem

Iteration 063 let `eair-export-reportable-results` carry protocol-legitimacy tables into paper-facing artifacts. The remaining risk was artifact mixing: a valid `protocol_legitimacy_table.json` from another model, prompt variant, or condition could be supplied alongside a reportable summary from a different run.

## Design

Before writing reportable protocol artifacts, validate every protocol row against the summary:

- If `by_model_prompt_condition` exists, require exact `(model, prompt_variant, condition)` membership.
- Otherwise require `(model, condition)` membership in `by_model_condition`.
- On mismatch, write the normal blocked export artifact and exit with an error.

## Boundary

This gate checks row membership, not semantic correctness of the warrant. Warrant correctness is still evaluated by replay and WarrantGuard metrics.
