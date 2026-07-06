# EAIR-Bench Pilot Experiment

This deterministic pilot targets context-dependent high-risk action grounding.

## Baseline Summary

| baseline | unsafe_decision_rate | unsupported_action_rate | false_positive_rate | over_refusal_rate | poison_warning_rate | warrant_failure_rate | mean_warrant_error_count | parameter_violation_rate | clean_utility_retention | mean_support_clusters | mean_support_freshness | support_current_rate | mean_superseded_support | mean_eair | mean_raw_path_poison |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| access_control | 0.4000 | 0.4000 | 0.0000 | 0.0000 | 0.0667 | 0.6000 | 0.8667 | 0.1333 | 1.0000 | 1.0000 | 0.7727 | 0.6000 | 0.1333 | 0.3920 | 0.3100 |
| agent_sentry_provenance | 0.0000 | 0.0667 | 0.0000 | 0.1333 | 0.0667 | 0.6000 | 0.8667 | 0.0000 | 1.0000 | 1.0000 | 0.7727 | 0.6000 | 0.1333 | 0.0778 | 0.0620 |
| airguard_authority | 0.0000 | 0.2000 | 0.0000 | 0.0000 | 0.0667 | 0.6000 | 0.8667 | 0.0000 | 1.0000 | 1.0000 | 0.7727 | 0.6000 | 0.1333 | 0.1110 | 0.0620 |
| attriguard_attribution | 0.0000 | 0.0000 | 0.4000 | 0.6000 | 0.0000 | 0.6000 | 0.8667 | 0.0000 | 0.0000 | 1.0000 | 0.7727 | 0.6000 | 0.1333 | 0.0245 | 0.0000 |
| attriguard_selective | 0.0667 | 0.1333 | 0.0000 | 0.0667 | 0.0667 | 0.6000 | 0.8667 | 0.0667 | 1.0000 | 1.0000 | 0.7727 | 0.6000 | 0.1333 | 0.1101 | 0.0620 |
| causalarmor_dominance | 0.0667 | 0.2000 | 0.0000 | 0.0000 | 0.0667 | 0.6000 | 0.8667 | 0.0667 | 1.0000 | 1.0000 | 0.7727 | 0.6000 | 0.1333 | 0.1299 | 0.0620 |
| conflict_aware | 0.0667 | 0.2667 | 0.1333 | 0.0000 | 0.0667 | 0.6000 | 0.8667 | 0.0000 | 1.0000 | 1.0000 | 0.7727 | 0.6000 | 0.1333 | 0.1510 | 0.0620 |
| eair_evidence_sufficiency_only | 0.2000 | 0.0000 | 0.0000 | 0.2000 | 0.0667 | 0.6000 | 0.8667 | 0.0667 | 1.0000 | 1.0000 | 0.7727 | 0.6000 | 0.1333 | 0.1796 | 0.1860 |
| eair_full | 0.0000 | 0.0000 | 0.0000 | 0.2000 | 0.0667 | 0.6000 | 0.8667 | 0.0000 | 1.0000 | 1.0000 | 0.7727 | 0.6000 | 0.1333 | 0.0630 | 0.0620 |
| eair_gate | 0.0000 | 0.2000 | 0.0000 | 0.0000 | 0.0667 | 0.6000 | 0.8667 | 0.0000 | 1.0000 | 1.0000 | 0.7727 | 0.6000 | 0.1333 | 0.1110 | 0.0620 |
| eair_hard_gate_only | 0.0000 | 0.2000 | 0.0000 | 0.0000 | 0.0667 | 0.6000 | 0.8667 | 0.0000 | 1.0000 | 1.0000 | 0.7727 | 0.6000 | 0.1333 | 0.1110 | 0.0620 |
| eair_soft_score_only | 0.0667 | 0.2000 | 0.0000 | 0.0000 | 0.0667 | 0.6000 | 0.8667 | 0.0667 | 1.0000 | 1.0000 | 0.7727 | 0.6000 | 0.1333 | 0.1299 | 0.0620 |
| planguard_intent | 0.1333 | 0.2000 | 0.0000 | 0.0000 | 0.0667 | 0.6000 | 0.8667 | 0.0000 | 1.0000 | 1.0000 | 0.7727 | 0.6000 | 0.1333 | 0.2087 | 0.1860 |
| pre_rhe | 0.1333 | 0.2667 | 0.1333 | 0.1333 | 0.0000 | 0.6000 | 0.8667 | 0.0667 | 0.6667 | 1.0000 | 0.7727 | 0.6000 | 0.1333 | 0.1699 | 0.0000 |
| ragas_claim_support | 0.4000 | 0.0000 | 0.0000 | 0.0000 | 0.0667 | 0.6000 | 0.8667 | 0.1333 | 1.0000 | 1.0000 | 0.7727 | 0.6000 | 0.1333 | 0.3920 | 0.3100 |
| source_filter | 0.0667 | 0.2000 | 0.0000 | 0.0000 | 0.0000 | 0.4000 | 0.7333 | 0.0667 | 1.0000 | 1.2667 | 0.9220 | 0.8667 | 0.1333 | 0.0852 | 0.0000 |
| vanilla_rag | 0.4000 | 0.4000 | 0.0000 | 0.0000 | 0.0667 | 0.6000 | 0.8667 | 0.1333 | 1.0000 | 1.0000 | 0.7727 | 0.6000 | 0.1333 | 0.3920 | 0.3100 |
| warrantguard_full | 0.0000 | 0.0000 | 0.0000 | 0.2000 | 0.0667 | 0.6000 | 0.8667 | 0.0000 | 1.0000 | 1.0000 | 0.7727 | 0.6000 | 0.1333 | 0.0630 | 0.0620 |

## Key Findings

- EAIR-Full reduces unsafe_decision_rate by 0.4000 absolute versus vanilla_rag.
- PRE/RHE false_positive_rate is 0.1333 in this pilot.
- AttriGuard-style attribution blocks legitimate evidence influence that EAIR-Full allows when evidence is sufficient.
- Selective AttriGuard-style preserves clean utility but still leaves unsafe_decision_rate=0.0667 and unsupported_action_rate=0.1333.
- CausalArmor-style dominance catches untrusted-control cases but misses trusted-looking policy gaps (parameter_violation_rate=0.0667).
- AIRGuard-style authority control removes hard policy violations but leaves evidence insufficiency (unsupported_action_rate=0.2000).
- Agent-Sentry-style provenance bounds reduce stale-version failures but still miss source-diversity insufficiency (unsupported_action_rate=0.0667).
- WarrantGuard exposes proof-carrying action failures directly (warrant_failure_rate=0.6000, mean_warrant_error_count=0.8667).
- The pilot is deterministic and synthetic; it supports system behavior claims, not deployment safety claims.
