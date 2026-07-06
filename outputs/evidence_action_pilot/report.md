# Evidence-to-Action Pilot Experiment

This deterministic pilot evaluates retrieval-to-action pollution on synthetic power-grid RAG-agent tasks.

## Baseline Summary

| baseline | unsafe_decision_rate | unsupported_action_rate | wrong_tool_rate | evidence_trace_fidelity | clean_utility_retention | over_refusal_rate | mean_eair |
|---|---:|---:|---:|---:|---:|---:|---:|
| access_control | 0.3265 | 0.3265 | 0.0000 | 0.6735 | 1.0000 | 0.0000 | 0.4884 |
| conflict_aware | 0.1429 | 0.1429 | 0.0612 | 0.8571 | 1.0000 | 0.0000 | 0.1980 |
| eair_gate | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0808 |
| eair_robust | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0564 |
| output_guardrail | 0.5714 | 0.5714 | 0.3265 | 0.4286 | 1.0000 | 0.0000 | 0.6184 |
| source_filter | 0.1429 | 0.1429 | 0.0612 | 0.8571 | 1.0000 | 0.0000 | 0.1184 |
| vanilla_rag | 0.8571 | 0.8571 | 0.5306 | 0.1429 | 1.0000 | 0.0000 | 0.7263 |

## Interpretation

- EAIR gate reduces unsafe_decision_rate by 0.8571 absolute versus vanilla_rag in this pilot.
- Robust retrieval changes unsafe_decision_rate by 0.0000 absolute versus EAIR gate.
- The pilot is deterministic and synthetic; it is evidence for pipeline behavior, not a real-grid safety claim.
