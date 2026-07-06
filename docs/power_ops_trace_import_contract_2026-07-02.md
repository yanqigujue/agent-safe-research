# Power-Ops Trace Import Contract

Date: 2026-07-02

## Purpose

This contract defines the current import boundary between a power-ops agent trace and the AFW runtime checker.

Plain version:

> A trace is not trusted because it came from the agent. The trace is only a transport format. AFW imports source events as candidate capabilities, imports action-field consumptions as Need(s,f), and then re-checks whether each action field is covered.

## Runtime Path

```text
agent trace
  -> custom.afw_trace_adapter
  -> metrics.afw_source_events
  -> metrics.afw_consumptions
  -> metrics.candidate_action
  -> guardrail.afw_capguard
  -> fieldwise final_action
  -> evaluate.afw_runtime
```

No new `FormalTrustState` top-level field is introduced. Imported objects stay under `metrics`.

## Canonical Event Mapping

| Raw trace event | Required fields | AFW runtime object | Notes |
|---|---|---|---|
| `source_event` | `source_id`, `source_type`, `authority_manifest` | `metrics.afw_source_events[]` | A source event is lifted into `Cap(x)` only if the manifest declares semantic role and scope fields. |
| `candidate_action` | `action.decision` | `metrics.candidate_action` | The action is still untrusted until field checks finish. |
| `authority_consumption` | `field`, `operation`, `need` | `metrics.afw_consumptions[]` | This is the imported `Need(s,f)`. |
| `counter_authority` | `field` | `metrics.afw_counter_authority[]` | Existing runtime handles this as abstain when it applies. |
| malformed or unknown event | none | `metrics.afw_trace_adapter_diagnostics` | The adapter records diagnostics instead of silently trusting it. |

## Span / OTLP Compatibility

The same adapter also supports `schema_preset: span_log_v1`. In that mode, spans with `span_kind` are normalized:

| Span kind | Normalized event |
|---|---|
| `retrieval`, `source`, `source_event`, `retrieval_chunk` | `source_event` |
| `agent_action`, `action`, `candidate_action` | `candidate_action` |
| `authority_use`, `authority_consumption`, `field_authority` | `authority_consumption` |
| `counter_authority`, `policy_hold` | `counter_authority` |

Current validation for this round uses canonical JSON events to isolate import-boundary behavior. Earlier artifacts cover span/OTLP replay.

## Boundary Behaviors Tested

| Boundary | Fixture case | Expected behavior |
|---|---|---|
| `malformed_trace` | `trace-import-malformed-keep-answer-block-dispatch` | Malformed events are counted in diagnostics; valid imported events still undergo field checks. |
| `missing_source` | `trace-import-missing-source-keep-answer-block-control` | A consumption that cites a source id absent from imported capabilities cannot authorize the field. |
| `duplicate_approval` | `trace-import-duplicate-approval-keep-work-order-block-switching` | Duplicate approval events are counted, but duplicated work-order authority does not become switching authority. |
| `expired_epoch` | `trace-import-expired-epoch-keep-answer-block-q4-publish` | Q3 publish approval does not cover Q4 publish need. |

## Result Readback

The fixture is runnable through:

```powershell
python -m formaltrust_platform.experiments.afw_runtime_suite `
  examples/power_ops_trace_import_validation.yaml `
  --suite-id power_ops_trace_import_runtime `
  --output-stem power_ops_trace_import_runtime_report_2026-07-02
```

Then summarize:

```powershell
python -m formaltrust_platform.experiments.power_ops_trace_import summarize `
  --run-dir runs/<trace-import-run-id> `
  --suite-id power_ops_trace_import `
  --out-md docs/power_ops_trace_import_results_2026-07-02.md `
  --out-json docs/power_ops_trace_import_results_2026-07-02.json
```

Current result:

| Metric | Value |
|---|---:|
| cases | 4 |
| passed | 4 |
| malformed trace cases | 1 |
| missing source cases | 1 |
| duplicate approval cases | 1 |
| expired epoch cases | 1 |
| authorized final-field preservation | 1.000 |
| unauthorized final-field removal | 1.000 |
| whole-action block rate | 0.000 |

## Claim Boundary

This is a realistic import-path fixture, not a production telemetry integration. It supports the claim that the current FormalTrust AFW interface can import and evaluate several trace-boundary failures without whole-action collapse. It does not yet prove coverage for real SCADA, OMS, EMS, or vendor-specific agent logs.
