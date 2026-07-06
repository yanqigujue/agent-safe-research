# Power-Ops Evidence-Bound Limitations Outline

**Status:** ready
**Paper section:** §6 Limitations and Next Experiments
**Forbidden claim count:** 7
**Paper readiness passed:** True
**Forbidden claim hits:** 0

## Limitations Outline

| Slot | Paragraph goal | Excluded claims | Future work | Source refs |
|---|---|---|---|---|
| production_trace_gap | State that current trace evidence is fixture, bridge, span, OTLP, and import evidence, not production telemetry or live deployment evidence. | proves production safety | Collect reviewed real or semi-real multi-step power-agent traces before any production-safety claim. | docs/power_ops_action_invariance_paper_outline_2026-07-02.json#§6 Limitations and Next Experiments; docs/power_ops_action_invariance_claim_ledger_readiness_2026-07-02.json#forbidden_claims |
| latency_gap | State that the performance profile uses a field-check latency proxy and does not measure wall-clock latency. |  | Measure wall-clock latency with runtime instrumentation before reporting speed claims. | docs/power_ops_action_invariance_paper_outline_2026-07-02.json#§6 Limitations and Next Experiments; docs/power_ops_action_invariance_performance_2026-07-02.json#latency_proxy_units |
| operator_workload_gap | State that the current artifact does not support real operator workload reduction because there is no operator-time or human-study evidence. | reduces real human workload without operator-time evidence | Run operator-time or reviewer-burden studies before any real workload-reduction claim. | docs/power_ops_action_invariance_paper_outline_2026-07-02.json#§6 Limitations and Next Experiments; docs/power_ops_action_invariance_claim_ledger_readiness_2026-07-02.json#forbidden_claims |
| official_benchmark_gap | State that AgentDojo-style and semi-real bridge fixtures are expressibility evidence, not official benchmark superiority. | outperforms official neighboring systems | Run official external benchmarks and pre-register comparison rules before any superiority claim. | docs/power_ops_action_invariance_paper_outline_2026-07-02.json#§6 Limitations and Next Experiments; docs/power_ops_action_invariance_claim_ledger_readiness_2026-07-02.json#forbidden_claims |
| forbidden_firstness_security_claims | List firstness, generic runtime-enforcement, least-privilege, and prompt-injection claims as excluded from the current paper. | first LLM-agent guardrail; first runtime enforcement framework; first least-privilege LLM-agent security framework; solves prompt injection | Keep novelty phrased as field-level action invariance with authority witnesses and repair validity. | docs/power_ops_action_invariance_claim_ledger_readiness_2026-07-02.json#forbidden_claims; docs/power_ops_action_invariance_novelty_firewall_2026-07-02.md#Forbidden |
| next_experiments | Convert the limitations into next experiments: real or semi-real traces, wall-clock timing, operator workload, and official benchmark comparison. |  | Collect reviewed traces.; Measure wall-clock latency.; Run operator workload studies.; Run official benchmark comparisons. | docs/power_ops_action_invariance_paper_outline_2026-07-02.json#§6 Limitations and Next Experiments; docs/power_ops_action_invariance_paper_claim_readiness_2026-07-02.json#checks |
