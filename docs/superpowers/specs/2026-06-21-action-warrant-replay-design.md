# Action-Warrant Transcript Replay Design

## Goal

Allow structured transcript replay to evaluate model-supplied proof-carrying actions, not only bare action JSON.

## Scope

Replay accepts both formats:

```json
{
  "decision": "route_to_simulation",
  "tool": "power_flow",
  "risk_level": "high",
  "risk_report": "human_review_required",
  "requires_human_approval": true,
  "supporting_claims": ["new_policy_requires_simulation"]
}
```

and:

```json
{
  "action": {
    "decision": "route_to_simulation",
    "tool": "power_flow",
    "risk_level": "high",
    "risk_report": "human_review_required",
    "requires_human_approval": true,
    "supporting_claims": ["new_policy_requires_simulation"]
  },
  "warrant": {
    "decision_claims": ["new_policy_requires_simulation"],
    "parameter_claims": {},
    "approval_claims": ["new_policy_requires_simulation"],
    "risk_level_claims": ["new_policy_requires_simulation"],
    "risk_report_claims": ["new_policy_requires_simulation"],
    "counter_claims": []
  }
}
```

Bare action JSON remains supported for backward compatibility. When a model-supplied warrant exists, replay verifies it with `verify_action_warrant` before applying the normal EAIR full gate.

## Result Contract

Transcript rows expose:

- `warrant_present`
- `warrant_passed`
- `warrant_error_count`
- `warrant_warning_count`
- `warrant_errors`
- `warrant_warnings`

Replay summaries expose:

- `warrant_present_count`
- `warrant_failed_count`

## Prompt Contract

The sampler prompt now asks models to return top-level `action` and `warrant` objects. Old bare-action dry-run responses are still replayable.

