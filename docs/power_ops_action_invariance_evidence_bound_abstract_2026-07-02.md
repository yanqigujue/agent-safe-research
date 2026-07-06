# Power-Ops Evidence-Bound Abstract

**Status:** ready
**Word count:** 80
**Forbidden claim hits:** 0

## Abstract

High-risk power-operation LLM agents need supervision that preserves authorized action fields while removing fields without valid authority. The current artifact implements fieldwise repair as an auditable final-action mode. Paper-ready evidence covers curated and expanded power-operation cases, metamorphic authority-confusion tests, skill-driven multi-source authority, baselines, and safety-preserving normal-behavior profiles. Trace evidence covers trace/span/OTLP replay, trace-import boundaries, planner-skill-tool-memory source chains, and bridge fixtures. We keep the boundary explicit: no production telemetry, no real operator workload reduction claim, and no official neighboring-system superiority claim.

## Sentence Evidence

| Sentence | Source slot | Source claims |
|---|---|---|
| High-risk power-operation LLM agents need supervision that preserves authorized action fields while removing fields without valid authority. | problem | L1:fieldwise repair final-action mode exists |
| The current artifact implements fieldwise repair as an auditable final-action mode. | method | L1:fieldwise repair final-action mode exists |
| Paper-ready evidence covers curated and expanded power-operation cases, metamorphic authority-confusion tests, skill-driven multi-source authority, baselines, and safety-preserving normal-behavior profiles. | results | L2:curated power-ops fieldwise repair preserves authorized fields and removes unauthorized fields; L2:expanded 18-case power-ops fieldwise repair preserves authorized fields and removes unauthorized fields; L2:metamorphic authority-confusion tests preserve authorized fields while removing or reviewing mutated unsafe fields; L2:no-RAG skill-driven fixture lifts skill, tool metadata, approval, memory, and prior-step outputs into field-level capabilities; L2:current artifact reports a safety-preserving normal-behavior performance profile; L2:baseline grid shows strict-block collapse and provenance-only false allow on curated cases |
| Trace evidence covers trace/span/OTLP replay, trace-import boundaries, planner-skill-tool-memory source chains, and bridge fixtures. | trace coverage | L3:trace/span/OTLP replay feeds fieldwise repair; L3:trace import fixture covers malformed trace, missing source, duplicate approval, and expired epoch boundaries; L3:multi-step trace import covers planner, skill, tool metadata, memory, prior-step output, and user approval source chains; L4:AgentDojo-style and semi-real power trace bridge fixtures are expressible |
| We keep the boundary explicit: no production telemetry, no real operator workload reduction claim, and no official neighboring-system superiority claim. | limitations | L1:fieldwise repair final-action mode exists |
