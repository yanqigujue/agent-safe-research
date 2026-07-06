# WarrantGuard Full Baseline Design

## Goal

Promote WarrantGuard from a standalone verifier into an EAIR-Bench baseline that evaluates proof-carrying high-risk actions.

## Approved Direction

The current research direction is WarrantGuard: high-risk RAG-agent actions must be emitted as an action plus an evidence warrant. The verifier should check the warrant before execution rather than treating evidence influence as automatically suspicious.

## Scope

This iteration adds one deterministic benchmark baseline: `warrantguard_full`.

The baseline should:

- build an `ActionWarrant` for the candidate action;
- verify it with `verify_action_warrant`;
- block or replace the action when the warrant fails;
- preserve legitimate evidence-backed actions when the warrant passes;
- expose warrant pass/error diagnostics in `CaseResult`, summary JSON/CSV, and report Markdown.

This iteration does not require live model warrant generation. It uses the existing synthetic action proposer and deterministic warrant builder so the benchmark has a stable reference verifier.

## Architecture

`formaltrust_platform.experiments.eair_bench` remains the owner of the benchmark data model and deterministic pilots. `ActionWarrant` and `WarrantVerification` stay beside `AgentAction`, while `apply_warrantguard_full` becomes the method-level baseline wrapper that calls the verifier and then reuses the existing oracle/fallback actions.

`CaseResult` gains warrant diagnostics so downstream reports can distinguish normal EAIR safety outcomes from proof-carrying-action failures.

## Data Flow

1. EAIR-Bench retrieves synthetic evidence.
2. The candidate agent proposes an `AgentAction`.
3. `warrantguard_full` builds an `ActionWarrant` from the candidate action.
4. `verify_action_warrant` checks decision, parameter, approval, risk-level, risk-report, hard-gate, freshness, source-diversity, and counter-warrant constraints.
5. The baseline allows the candidate only when the warrant passes and the action also clears the existing EAIR full gate.
6. Results store warrant status and error counts.

## Testing

Tests must show that `warrantguard_full` is present in `BASELINES`, appears in summary output, produces warrant diagnostics, allows clean sufficient evidence, and rejects missing/insufficient proof-carrying action support.

The test must fail before implementation because `warrantguard_full` is not currently registered.

