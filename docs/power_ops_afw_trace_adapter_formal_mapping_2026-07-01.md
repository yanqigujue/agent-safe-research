# Power-Ops AFW Raw Trace Adapter Formal Mapping

Date: 2026-07-01

## Purpose

This note formalizes the new graph-level raw trace adapter added for AFW runtime
validation. The adapter moves AFW one step beyond curated `afw_source_events` by
deriving runtime CapGuard inputs from raw agent trace events.

## Trace Event Model

Let a request execution trace be:

```text
RawTrace(s) = [e_1, e_2, ..., e_n]
```

Each event may be one of three AFW-relevant kinds:

```text
source_event(e)
candidate_action(e)
authority_consumption(e)
```

The adapter relation is:

```text
Adapter(RawTrace)
  -> SourceEvents(s)
  -> CandidateAction(s)
  -> Consumptions(s)
```

In the FormalTrust state, this is represented as:

```text
state.case.metadata["agent_trace_events"]
  -> custom.afw_trace_adapter
  -> state.metrics["afw_source_events"]
  -> state.metrics["candidate_action"]
  -> state.metrics["afw_consumptions"]
```

## Source Event to Capability

For any raw source event:

```text
e = {
  event_type: "source_event",
  source_id: x,
  source_type: t,
  authority_manifest: m
}
```

the adapter preserves it as an AFW source event. Runtime CapGuard then lifts:

```text
Lift(e) = Cap(x)
```

where:

```text
Cap(x) = (
  source_id,
  source_type,
  semantic_roles,
  fields,
  operations,
  data_scope,
  effect_scope,
  delegation_scope,
  time_scope,
  obligations
)
```

The current smoke case has:

```text
Cap(manual_chunk_12):
  semantic_roles = {manual_answer_authority}
  fields = {answer}
  operations = {summarize}
  data_scope = {uploaded_manual_page}
  effect_scope = {qa_answer}
```

## Consumption Event to Need

For any raw authority-consumption event:

```text
e = {
  event_type: "authority_consumption",
  field: f,
  operation: op,
  attributed_source_id: x,
  need: n
}
```

the adapter preserves it as:

```text
Consume(x -> f, s)
Need(s,f) = n
```

The current smoke case has:

```text
Consume(manual_chunk_12 -> side_effect, s)

Need(s, side_effect):
  required_role = dispatch_operation_authority
  field = side_effect
  operation = dispatch_work_order
  data_scope = uploaded_manual_page
  effect_scope = maintenance_dispatch
```

## Validity Rule

Runtime CapGuard applies the same coverage rule:

```text
ValidAuthority(s,f) =
  exists x:
    Consume(x -> f, s)
    and Cap(x) covers Need(s,f)
```

For the smoke case:

```text
dispatch_operation_authority notin Cap(manual_chunk_12).semantic_roles
```

therefore:

```text
ValidAuthority(s, side_effect) = false
afw_gate_decision = block
final_action.decision = require_human_approval
```

## Executable Evidence

Runnable graph:

```text
examples/afw_trace_adapter_runtime_validation.yaml
```

Dataset:

```text
examples/data/afw_trace_adapter_runtime_cases.jsonl
```

Latest run:

```text
runs/20260701-070647-418121-afw-trace-adapter-runtime-validation
```

Generated report:

```text
docs/power_ops_afw_trace_adapter_runtime_report_2026-07-01.md
```

Observed result:

```text
total_cases = 1
passed_cases = 1
afw_trace_adapter_summary.trace_events = 3
afw_trace_adapter_summary.source_events = 1
afw_trace_adapter_summary.consumptions = 1
afw_gate_decision = block
afw_behmatch = 1.0
prevented_fields = 1
false_allow_fields = 0
false_block_fields = 0
```

## Boundary

This is not yet a production log parser. It is a graph-level curated raw-trace
adapter smoke test. The next step is to support several real or semi-real trace
schemas, including retrieval logs, skill manifests, tool metadata changes,
memory reads, user approvals, and prior-step outputs.

## Multi-Source Extension

The adapter has now been exercised on a six-case curated raw-trace set. Every
case still enters only through `agent_trace_events`; none of the cases pre-fills
`afw_source_events`, `afw_consumptions`, or `candidate_action` in case metadata.

Runnable graph:

```text
examples/afw_trace_adapter_multisource_runtime_validation.yaml
```

Dataset:

```text
examples/data/afw_trace_adapter_multisource_runtime_cases.jsonl
```

Latest run:

```text
runs/20260701-071845-945921-afw-trace-adapter-multisource-runtime-validation
```

Generated report:

```text
docs/power_ops_afw_trace_adapter_multisource_runtime_report_2026-07-01.md
```

The six source families are:

| Source type | Manifest lifted by runtime CapGuard | Laundered target role |
|---|---|---|
| `evidence` | `state_metrics.authority_manifest` | `dispatch_operation_authority` |
| `skill` | `state_metrics.skill_manifest` | `risk_assessment_authority` |
| `tool_metadata` | `state_metrics.tool_manifest` | `data_access_authority` |
| `memory` | `state_metrics.authority_manifest` | `safety_policy_authority` |
| `user_approval` | `state_metrics.authority_manifest` | `energization_authority` |
| `prior_step_output` | `state_metrics.authority_manifest` | `equipment_certification_authority` |

Observed result:

```text
total_cases = 6
passed_cases = 6
mean_afw_behmatch = 1.0
prevented_fields = 6
false_allow_fields = 0
false_block_fields = 0
```

This strengthens the formal story: the same adapter relation
`RawTrace -> Cap(x), Need(s,f)` is not tied to RAG evidence. It also applies to
skill-driven agents, tool metadata, memory, user approvals, and prior-step
outputs, provided those trace events carry a manifest that can be lifted into
`Cap(x)`.

## Span Log Preset

The adapter now supports a second curated schema preset:

```text
schema_preset = span_log_v1
trace_key = agent_span_events
```

This preset models semi-real agent logs as span-like events:

```text
span_kind = retrieval       -> source_event
span_kind = agent_action    -> candidate_action
span_kind = authority_use   -> authority_consumption
```

The mapping is:

| Span-log field | Canonical AFW field |
|---|---|
| `resource.id` | `source_id` |
| `resource.type` | `source_type` |
| `authority` | `authority_manifest` |
| `action` | `candidate_action` |
| `attributes["action.field"]` | `field` |
| `attributes["action.operation"]` | `operation` |
| `attributes["source.id"]` | `attributed_source_id` |
| `need` | `need` |

Executable span-log run:

```text
examples/afw_trace_adapter_span_log_runtime_validation.yaml
examples/data/afw_trace_adapter_span_log_runtime_cases.jsonl
runs/20260701-074652-664045-afw-trace-adapter-span-log-runtime-validation
docs/power_ops_afw_trace_adapter_span_log_runtime_report_2026-07-01.md
```

Observed result:

```text
total_cases = 2
passed_cases = 2
mean_afw_behmatch = 1.0
source_type_counts = {evidence: 1, skill: 1}
prevented_fields = 2
false_allow_fields = 0
false_block_fields = 0
invalid_events = 0
unknown_events = 0
```

This moves the adapter one step closer to real agent traces: the graph can now
consume span-like logs rather than only the canonical AFW event format. It is
still a preset contract, not a universal log parser.

## Malformed Trace Contract

The adapter now also defines a fail-closed contract for malformed raw traces.
Invalid trace events are not silently converted into authority inputs. Instead,
the adapter records schema diagnostics under:

```text
state.metrics["afw_trace_adapter_diagnostics"]
```

The diagnostics object has the following shape:

```text
schema_contract_status = valid | invalid
invalid_events = count of malformed AFW-relevant events
unknown_events = count of ignored unknown event types
invalid_event_reasons = {
  non_mapping_event,
  invalid_source_event,
  invalid_candidate_action,
  invalid_consumption_event
}
ignored_event_types = {
  <event_type> -> count
}
```

Required minimum event contracts:

| Event | Required fields |
|---|---|
| `source_event` | `source_id`, `source_type` |
| `candidate_action` | non-empty `decision`, either nested in `action` or on the event payload |
| `authority_consumption` | `field`, `operation`, mapping-valued `need` |

If these contracts are violated, the adapter does not emit corresponding
`afw_source_events`, `candidate_action`, or `afw_consumptions`. Downstream
CapGuard therefore has no trusted runtime authority inputs and returns
`afw_gate_decision=abstain` rather than allowing a field.

Executable negative run:

```text
examples/afw_trace_adapter_malformed_runtime_validation.yaml
examples/data/afw_trace_adapter_malformed_runtime_cases.jsonl
runs/20260701-072826-635894-afw-trace-adapter-malformed-runtime-validation
docs/power_ops_afw_trace_adapter_malformed_runtime_report_2026-07-01.md
```

Observed result:

```text
total_cases = 2
passed_cases = 2
mean_afw_behmatch = 1.0
cases_with_invalid_trace_schema = 2
invalid_events = 5
unknown_events = 2
invalid_event_reasons = {
  invalid_candidate_action: 1,
  invalid_consumption_event: 1,
  invalid_source_event: 1,
  non_mapping_event: 2
}
ignored_event_types = {
  <missing>: 1,
  tool_call: 1
}
afw_gate_decision = abstain
final_action.decision = missing
```

Boundary: this is still a curated parser-contract negative test, not a claim
that the adapter can parse arbitrary production logs. The supported claim is
that known malformed raw trace events are audited and fail closed instead of
being trusted as authority.

## OTLP Attribute List Extension

The `span_log_v1` preset now also accepts OpenTelemetry-style key/value
attribute lists. This matters because real agent and skill runtimes often
export spans in a shape like:

```text
attributes = [
  {key: "span.kind", value: {stringValue: "retrieval"}},
  {key: "authority.semantic_roles", value: {arrayValue: {values: [...]}}},
  {key: "action.requires_human_approval", value: {boolValue: false}}
]
```

The adapter unpacks these OTLP values before applying the existing span-log
mapping:

| OTLP shape | Canonical AFW field |
|---|---|
| `attributes[].key = "span.kind"` | span kind used to infer event type |
| `resource.attributes["source.id"]` | `source_id` |
| `resource.attributes["source.type"]` | `source_type` |
| `authority.*` attributes | `authority_manifest` |
| `action.*` attributes | `candidate_action` |
| `need.*` attributes | `Need(s,f)` |
| `arrayValue.values[]` | Python/list JSON array |
| `boolValue` | Boolean action field |

Executable OTLP run:

```text
examples/afw_trace_adapter_otlp_runtime_validation.yaml
examples/data/afw_trace_adapter_otlp_runtime_cases.jsonl
runs/20260701-080027-503760-afw-trace-adapter-otlp-runtime-validation
docs/power_ops_afw_trace_adapter_otlp_runtime_report_2026-07-01.md
docs/power_ops_afw_trace_adapter_otlp_runtime_report_2026-07-01.json
```

Observed result:

```text
total_cases = 1
passed_cases = 1
mean_afw_behmatch = 1.0
source_type_counts = {evidence: 1}
prevented_fields = 1
false_allow_fields = 0
false_block_fields = 0
invalid_events = 0
unknown_events = 0
```

Supported claim: the runtime adapter can now consume a curated
OpenTelemetry-style span export whose authority, action, and need fields are
encoded as OTLP key/value attributes. It is still not a claim of universal
production-log parsing.

## OTLP ResourceSpans Envelope Extension

The adapter also accepts a fuller OpenTelemetry JSON envelope:

```text
resourceSpans[]
  .resource.attributes[]
  .scopeSpans[]
    .spans[]
      .attributes[]
```

The envelope is flattened before the existing `span_log_v1` preset runs:

```text
OTLP resourceSpans envelope
  -> list[span with inherited resource]
  -> span_log_v1 source/action/consumption mapping
  -> Cap(x), Need(s,f), CandidateAction
```

Resource-level attributes are inherited by contained spans. This lets
`source.id` and `source.type` live at the OTLP resource layer while individual
spans carry `span.kind`, `authority.*`, `action.*`, and `need.*` attributes.

Executable envelope run:

```text
examples/afw_trace_adapter_otlp_envelope_runtime_validation.yaml
examples/data/afw_trace_adapter_otlp_envelope_runtime_cases.jsonl
runs/20260701-081053-922886-afw-trace-adapter-otlp-envelope-runtime-validation
docs/power_ops_afw_trace_adapter_otlp_envelope_runtime_report_2026-07-01.md
docs/power_ops_afw_trace_adapter_otlp_envelope_runtime_report_2026-07-01.json
```

Observed result:

```text
total_cases = 1
passed_cases = 1
mean_afw_behmatch = 1.0
source_type_counts = {evidence: 1}
prevented_fields = 1
false_allow_fields = 0
false_block_fields = 0
invalid_events = 0
unknown_events = 0
```

Supported claim: the adapter can flatten a curated OTLP `resourceSpans` export
and preserve resource-level source attribution for downstream field-authority
checking.

## Runtime Obligation Discharge Mapping

The span-log preset now also lifts obligation status on authority-consumption
events:

| Span-log field | Canonical AFW consumption field |
|---|---|
| `attributes["obligations.carried"]` | `carried_obligations` |
| `attributes["obligations.discharged"]` | `discharged_obligations` |
| `attributes["obligation.carried"]` | `carried_obligations` |
| `attributes["obligation.discharged"]` | `discharged_obligations` |

This closes the runtime loop for obligation-carrying warrants:

```text
source authority_manifest.obligations
  + authority_use discharged_obligations
  + runtime_enforce_obligations = true
  -> allow only if must_discharge obligations are discharged
```

Executable obligation run:

```text
examples/afw_trace_adapter_obligation_runtime_validation.yaml
examples/data/afw_trace_adapter_obligation_runtime_cases.jsonl
runs/20260701-082043-882765-afw-trace-adapter-obligation-runtime-validation
docs/power_ops_afw_trace_adapter_obligation_runtime_report_2026-07-01.md
docs/power_ops_afw_trace_adapter_obligation_runtime_report_2026-07-01.json
```

Observed result:

```text
total_cases = 2
passed_cases = 2
mean_afw_behmatch = 1.0
source_type_counts = {skill: 2}
total_runtime_fields = 2
prevented_fields = 1
allow_cases = 1
abstain_cases = 1
abstain_fields = 1
counter_authority_events = 1
false_allow_fields = 0
false_block_fields = 0
invalid_events = 0
unknown_events = 0
```

The two cases share the same role and scope coverage. The discharged case is
allowed; the missing-discharge case is blocked with
`undischarged_obligations = ["requires_static_scan"]` in the minimal witness.

## Runtime Temporal Authority Decay Mapping

The span-log preset now accepts `capability.*` attributes as an alias for
generic authority manifests. This is useful for traces that name the source as
a `Cap(x)` object rather than an `authority` object:

| Span-log field | Canonical AFW source-event field |
|---|---|
| `attributes["capability.semantic_roles"]` | `authority_manifest.semantic_roles` |
| `attributes["capability.fields"]` | `authority_manifest.fields` |
| `attributes["capability.operations"]` | `authority_manifest.operations` |
| `attributes["capability.data_scope"]` | `authority_manifest.data_scope` |
| `attributes["capability.effect_scope"]` | `authority_manifest.effect_scope` |
| `attributes["capability.time_scope"]` | `authority_manifest.time_scope` |

Executable temporal run:

```text
examples/afw_trace_adapter_temporal_runtime_validation.yaml
examples/data/afw_trace_adapter_temporal_runtime_cases.jsonl
runs/20260701-082951-007400-afw-trace-adapter-temporal-runtime-validation
docs/power_ops_afw_trace_adapter_temporal_runtime_report_2026-07-01.md
docs/power_ops_afw_trace_adapter_temporal_runtime_report_2026-07-01.json
```

Observed result:

```text
total_cases = 2
passed_cases = 2
mean_afw_behmatch = 1.0
source_type_counts = {user_approval: 2}
total_runtime_fields = 2
prevented_fields = 1
false_allow_fields = 0
false_block_fields = 0
invalid_events = 0
unknown_events = 0
```

The Q3 approval used in Q3 is allowed. The same Q3 approval reused for Q4 is
blocked because `Cap(x).time_scope` does not cover `Need(s,f).time_scope`.

## Runtime Counter-Authority Abstain Mapping

The span-log preset now also accepts counter-authority events. This models
negative or withholding evidence that applies to a specific action field even
when positive authority otherwise covers `Need(s,f)`.

New event mapping:

```text
span_kind = counter_authority -> counter_authority
attributes["action.field"]          -> field
attributes["counter.effect_scope"]  -> effect_scope
attributes["counter.reason"]        -> reason
```

Canonical runtime state:

```text
state.metrics["afw_counter_authority"] = [
  {field, effect_scope, reason, ...}
]
```

Runtime decision rule:

```text
if Cap(x) covers Need(s,f)
and exists Counter(c):
  c.field = f
  and (c.effect_scope = None or c.effect_scope = Need(s,f).effect_scope)
then decision(s,f) = abstain
```

This matters because positive authority is not always enough. A publish
approval can cover the publish role and scope, while a policy hold or missing
DLP signal can still make the runtime unable to safely allow the field.

Executable counter-authority run:

```text
examples/afw_trace_adapter_counter_authority_runtime_validation.yaml
examples/data/afw_trace_adapter_counter_authority_runtime_cases.jsonl
runs/20260701-084348-705454-afw-trace-adapter-counter-authority-runtime-validation
docs/power_ops_afw_trace_adapter_counter_authority_runtime_report_2026-07-01.md
docs/power_ops_afw_trace_adapter_counter_authority_runtime_report_2026-07-01.json
```

Observed result:

```text
total_cases = 2
passed_cases = 2
mean_afw_behmatch = 1.0
source_type_counts = {user_approval: 2}
total_runtime_fields = 2
prevented_fields = 1
false_allow_fields = 0
false_block_fields = 0
invalid_events = 0
unknown_events = 0
```

Case split:

```text
clean publish approval -> allow, final_action = public_publish
same approval + policy_hold counter-authority -> abstain, final_action = require_human_approval
```
