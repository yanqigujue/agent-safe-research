# Power-Ops Evidence-Bound Limitations Prose

**Status:** ready
**Paper section:** §6 Limitations and Next Experiments
**Paragraph count:** 6
**Forbidden claim hits:** 0

## Limitations Prose

The current trace evidence remains fixture, bridge, span, OTLP, and import evidence. It supports local replay and import behavior, but production telemetry and live deployment safety remain outside the supported claim set.

The current performance profile is a safety-preserving normal-behavior profile with a field-check proxy. It is not a wall-clock latency measurement and should not be read as a speed result.

The artifact has no operator-time study or human-subject workload measurement. Any real workload-reduction statement remains an excluded claim until reviewer-burden or operator-time evidence exists.

The AgentDojo-style and semi-real bridge fixtures show that the interface can express neighboring benchmark shapes. They do not establish official benchmark superiority.

The paper should not frame the artifact as a generic firstness, general runtime enforcement, least-privilege, or prompt-injection solution. The defensible scope is field-level action invariance with authority witnesses and repair validity.

The next experiments follow directly from the excluded-claim binding: collect reviewed traces, measure wall-clock timing, run operator workload studies, and run official benchmark comparisons under pre-registered rules.

## Paragraph Evidence

| Slot | Paragraph | Excluded claim binding | Future work | Source refs |
|---|---|---|---|---|
| production_trace_gap | The current trace evidence remains fixture, bridge, span, OTLP, and import evidence. It supports local replay and import behavior, but production telemetry and live deployment safety remain outside the supported claim set. | 1 excluded claim binding | Collect reviewed real or semi-real multi-step power-agent traces before any production-safety claim. | docs/power_ops_action_invariance_paper_outline_2026-07-02.json#§6 Limitations and Next Experiments; docs/power_ops_action_invariance_claim_ledger_readiness_2026-07-02.json#forbidden_claims |
| latency_gap | The current performance profile is a safety-preserving normal-behavior profile with a field-check proxy. It is not a wall-clock latency measurement and should not be read as a speed result. | none | Measure wall-clock latency with runtime instrumentation before reporting speed claims. | docs/power_ops_action_invariance_paper_outline_2026-07-02.json#§6 Limitations and Next Experiments; docs/power_ops_action_invariance_performance_2026-07-02.json#latency_proxy_units |
| operator_workload_gap | The artifact has no operator-time study or human-subject workload measurement. Any real workload-reduction statement remains an excluded claim until reviewer-burden or operator-time evidence exists. | 1 excluded claim binding | Run operator-time or reviewer-burden studies before any real workload-reduction claim. | docs/power_ops_action_invariance_paper_outline_2026-07-02.json#§6 Limitations and Next Experiments; docs/power_ops_action_invariance_claim_ledger_readiness_2026-07-02.json#forbidden_claims |
| official_benchmark_gap | The AgentDojo-style and semi-real bridge fixtures show that the interface can express neighboring benchmark shapes. They do not establish official benchmark superiority. | 1 excluded claim binding | Run official external benchmarks and pre-register comparison rules before any superiority claim. | docs/power_ops_action_invariance_paper_outline_2026-07-02.json#§6 Limitations and Next Experiments; docs/power_ops_action_invariance_claim_ledger_readiness_2026-07-02.json#forbidden_claims |
| forbidden_firstness_security_claims | The paper should not frame the artifact as a generic firstness, general runtime enforcement, least-privilege, or prompt-injection solution. The defensible scope is field-level action invariance with authority witnesses and repair validity. | 4 excluded claim binding | Keep novelty phrased as field-level action invariance with authority witnesses and repair validity. | docs/power_ops_action_invariance_claim_ledger_readiness_2026-07-02.json#forbidden_claims; docs/power_ops_action_invariance_novelty_firewall_2026-07-02.md#Forbidden |
| next_experiments | The next experiments follow directly from the excluded-claim binding: collect reviewed traces, measure wall-clock timing, run operator workload studies, and run official benchmark comparisons under pre-registered rules. | none | Collect reviewed traces.; Measure wall-clock latency.; Run operator workload studies.; Run official benchmark comparisons. | docs/power_ops_action_invariance_paper_outline_2026-07-02.json#§6 Limitations and Next Experiments; docs/power_ops_action_invariance_paper_claim_readiness_2026-07-02.json#checks |
