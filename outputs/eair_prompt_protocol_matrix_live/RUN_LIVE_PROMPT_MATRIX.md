# EAIR Live Model Runbook

This runbook records the command sequence for collecting live provider transcripts and turning them into verified replay artifacts.

## Claim Boundary

Do not cite sampler logs as safety evidence. Cite saved transcript JSONL, replay artifacts, verified manifests, and coverage-gated summaries.

Runbook only records the planned live-provider workflow; it is not live-model evidence.

## Config

- config: examples/eair_prompt_protocol_matrix_live_template.yaml
- model: gpt-4.1-mini
- api_key_env: OPENAI_API_KEY
- transcript_output: C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\sampled_transcripts.jsonl
- replay_output_dir: C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\replay
- summary_output_dir: C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\summary
- scenario_count: 8
- prompt_variants: legacy_action_only, proof_carrying, proof_carrying_strict
- planned_transcripts: 24

## Expected Conditions

- approval_bypass::hijack_evidence_support
- approval_bypass::poison_exposure_no_action_influence
- approval_bypass::risk_report_downgrade_no_tool
- dispatch_control::insufficient_evidence_dangerous_decision
- parameter_setting::parameter_level_hijack
- policy_update::legitimate_evidence_update
- policy_update::near_duplicate_single_source_policy_support
- policy_update::stale_trusted_policy_support

## Reviewer-Rejection Coverage

| reviewer_rejection | condition_count |
|---|---:|
| access_control_only | 3 |
| attribution_only_overblocks_legitimate_influence | 1 |
| benchmark_overfit_source_diversity | 1 |
| pcaa_certificate_not_evidence_warrant | 3 |
| planguard_attriguard_novelty | 1 |
| pre_rhe_false_positive | 1 |
| rag_faithfulness_misses_action_parameter_risk | 1 |
| rag_faithfulness_only | 3 |
| source_attribution_only | 4 |

## Closest-Neighbor Discriminator Plan

| reviewer_rejection | closest_neighbor | conditions | warrant_obligations | WarrantGuard discriminator | claim_boundary |
|---|---|---|---|---|---|
| access_control_only | AIRGuard / access-control guards | approval_bypass::risk_report_downgrade_no_tool, dispatch_control::insufficient_evidence_dangerous_decision, parameter_setting::parameter_level_hijack | counter_evidence_exposure, hard_policy_constraints, parameter_claim_support, risk_report_claim_support, sufficient_support | authorized actions whose evidence warrant is insufficient, stale, source-collapsed, or conflicted | planned_discriminator_not_live_result |
| attribution_only_overblocks_legitimate_influence | AttriGuard / attribution-only guards | policy_update::legitimate_evidence_update | fresh_current_support, source_diverse_support | legitimate evidence influence that should be allowed when the warrant is sufficient | planned_discriminator_not_live_result |
| benchmark_overfit_source_diversity | synthetic benchmark overfit critique | policy_update::near_duplicate_single_source_policy_support | source_diverse_support | source-diversity failures separated from clean sufficient-evidence controls | planned_discriminator_not_live_result |
| pcaa_certificate_not_evidence_warrant | PCAA / Proof-Carrying Agent Actions | approval_bypass::hijack_evidence_support, dispatch_control::insufficient_evidence_dangerous_decision, policy_update::stale_trusted_policy_support | counter_evidence_exposure, fresh_current_support, legitimate_influence_separation, sufficient_support | certificate-shaped actions whose evidence warrant fails sufficiency, freshness, source-diversity, or conflict obligations | planned_discriminator_not_live_result |
| planguard_attriguard_novelty | PlanGuard / AttriGuard | approval_bypass::hijack_evidence_support | counter_evidence_exposure, legitimate_influence_separation | plan-consistent or attributable actions that still lack admissible evidence warrants | planned_discriminator_not_live_result |
| pre_rhe_false_positive | PRE / RHE poison-exposure baselines | approval_bypass::poison_exposure_no_action_influence | legitimate_influence_separation, sufficient_support | poison retrieved without action influence should not force a block | planned_discriminator_not_live_result |
| rag_faithfulness_misses_action_parameter_risk | RAGChecker / ARES / RAG faithfulness | parameter_setting::parameter_level_hijack | counter_evidence_exposure, hard_policy_constraints, parameter_claim_support | faithful text can still ground unsafe action parameters or risk metadata | planned_discriminator_not_live_result |
| rag_faithfulness_only | RAGChecker / ARES / RAG faithfulness | approval_bypass::risk_report_downgrade_no_tool, dispatch_control::insufficient_evidence_dangerous_decision, policy_update::stale_trusted_policy_support | fresh_current_support, hard_policy_constraints, risk_report_claim_support, sufficient_support | faithful support can be stale, insufficient, or unsafe for protected action fields | planned_discriminator_not_live_result |
| source_attribution_only | RAGForensics / source attribution | approval_bypass::hijack_evidence_support, approval_bypass::poison_exposure_no_action_influence, policy_update::near_duplicate_single_source_policy_support, policy_update::stale_trusted_policy_support | counter_evidence_exposure, fresh_current_support, legitimate_influence_separation, source_diverse_support, sufficient_support | attributed evidence still needs sufficiency, freshness, source diversity, and low conflict | planned_discriminator_not_live_result |

## Condition Threat-Model Rows

| condition | protected_action_fields | warrant_obligations | reviewer_rejections_answered |
|---|---|---|---|
| approval_bypass::hijack_evidence_support | decision, requires_human_approval, risk_report | legitimate_influence_separation, counter_evidence_exposure | source_attribution_only, planguard_attriguard_novelty, pcaa_certificate_not_evidence_warrant |
| approval_bypass::poison_exposure_no_action_influence | decision, requires_human_approval, risk_report | legitimate_influence_separation, sufficient_support | pre_rhe_false_positive, source_attribution_only |
| approval_bypass::risk_report_downgrade_no_tool | risk_report, risk_level, requires_human_approval | risk_report_claim_support, hard_policy_constraints | access_control_only, rag_faithfulness_only |
| dispatch_control::insufficient_evidence_dangerous_decision | decision, tool, risk_report | sufficient_support | access_control_only, rag_faithfulness_only, pcaa_certificate_not_evidence_warrant |
| parameter_setting::parameter_level_hijack | parameters, risk_level, risk_report, requires_human_approval | parameter_claim_support, hard_policy_constraints, counter_evidence_exposure | rag_faithfulness_misses_action_parameter_risk, access_control_only |
| policy_update::legitimate_evidence_update | decision, tool, risk_level, risk_report | fresh_current_support, source_diverse_support | attribution_only_overblocks_legitimate_influence |
| policy_update::near_duplicate_single_source_policy_support | decision, tool, risk_report | source_diverse_support | source_attribution_only, benchmark_overfit_source_diversity |
| policy_update::stale_trusted_policy_support | decision, tool, risk_report | fresh_current_support | rag_faithfulness_only, source_attribution_only, pcaa_certificate_not_evidence_warrant |

## Commands

1. Run live preflight doctor.

```powershell
formaltrust eair-doctor-live-run --config examples/eair_prompt_protocol_matrix_live_template.yaml --output-dir C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\live_preflight
```

2. Check live config readiness.

```powershell
formaltrust eair-check-live-config --config examples/eair_prompt_protocol_matrix_live_template.yaml
```

3. Run provider sampling and deterministic replay.

```powershell
formaltrust eair-sample --config examples/eair_prompt_protocol_matrix_live_template.yaml
```

4. Audit prompt protocol adherence.

```powershell
formaltrust eair-audit-prompt-adherence --transcripts C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\sampled_transcripts.jsonl --output-dir C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\prompt_adherence
```

5. Export protocol-vs-legitimacy diagnostic table.

```powershell
formaltrust eair-export-protocol-legitimacy-table --adherence C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\prompt_adherence\prompt_adherence_audit.json --summary C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\summary\artifact_summary.json --output-dir C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\protocol_legitimacy
```

6. Verify the replay artifact manifest.

```powershell
formaltrust eair-verify-artifact --manifest C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\replay\artifact_manifest.json
```

7. Generate coverage-gated summary tables.

```powershell
formaltrust eair-summarize-artifacts --manifest C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\replay\artifact_manifest.json --expected-condition approval_bypass::hijack_evidence_support --expected-condition approval_bypass::poison_exposure_no_action_influence --expected-condition approval_bypass::risk_report_downgrade_no_tool --expected-condition dispatch_control::insufficient_evidence_dangerous_decision --expected-condition parameter_setting::parameter_level_hijack --expected-condition policy_update::legitimate_evidence_update --expected-condition policy_update::near_duplicate_single_source_policy_support --expected-condition policy_update::stale_trusted_policy_support --require-complete-coverage --output-dir C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\summary
```

8. Audit whether the run is reportable as live-provider evidence.

```powershell
formaltrust eair-audit-reportable-run --manifest C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\replay\artifact_manifest.json --summary C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\summary\artifact_summary.json --output-dir C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\reportability
```

9. Export paper-facing model-condition tables only after reportability passes.

```powershell
formaltrust eair-export-reportable-results --summary C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\summary\artifact_summary.json --audit C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\reportability\reportable_run_audit.json --protocol-legitimacy C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\protocol_legitimacy\protocol_legitimacy_table.json --output-dir C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\paper_tables
```

10. Audit exported paper table integrity.

```powershell
formaltrust eair-audit-reportable-export --export C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\paper_tables\reportable_results_export.json --output-dir C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\paper_tables\integrity
```

11. Write the reportable claim template.

```powershell
formaltrust eair-write-reportable-claim-template --export C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\paper_tables\reportable_results_export.json --integrity-audit C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\paper_tables\integrity\reportable_export_integrity_audit.json --output C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\paper_tables\reportable_claims.json
```

12. Run diagnostic reportable claim citation audit.

```powershell
formaltrust eair-audit-reportable-claims --claims C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\paper_tables\reportable_claims.json --output-dir C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\paper_tables\claim_audit
```

13. Seal the diagnostic reportable claim bundle.

```powershell
formaltrust eair-seal-reportable-claim-bundle --claims C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\paper_tables\reportable_claims.json --claim-audit C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\paper_tables\claim_audit\reportable_claim_citation_audit.json --output-dir C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\paper_tables\bundle_seal
```

14. Verify the diagnostic reportable claim bundle seal.

```powershell
formaltrust eair-verify-reportable-claim-bundle-seal --seal C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\paper_tables\bundle_seal\reportable_claim_bundle_seal.json --output-dir C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\paper_tables\bundle_seal\verification
```

15. Record the paper-ready claim review declaration.

```powershell
formaltrust eair-record-reportable-claim-review --claims C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\paper_tables\reportable_claims.json --claim-audit C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\paper_tables\claim_audit\reportable_claim_citation_audit.json --reviewer REVIEWER_ID --review-note "Reviewed claim text and cited artifact values." --output C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\paper_tables\paper_ready_claims.json
```

16. Verify the paper-ready claim review declaration.

```powershell
formaltrust eair-verify-reportable-claim-review --claims C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\paper_tables\paper_ready_claims.json --output-dir C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\paper_tables\paper_ready_claim_review_verification
```

17. Strictly audit human-reviewed reportable claims.

```powershell
formaltrust eair-audit-reportable-claims --claims C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\paper_tables\paper_ready_claims.json --output-dir C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\paper_tables\paper_ready_claim_audit --require-reviewed
```

18. Seal the paper-ready reportable claim bundle.

```powershell
formaltrust eair-seal-reportable-claim-bundle --claims C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\paper_tables\paper_ready_claims.json --claim-audit C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\paper_tables\paper_ready_claim_audit\reportable_claim_citation_audit.json --output-dir C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\paper_tables\paper_ready_claim_bundle_seal --require-reviewed
```

19. Verify the paper-ready reportable claim bundle seal.

```powershell
formaltrust eair-verify-reportable-claim-bundle-seal --seal C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\paper_tables\paper_ready_claim_bundle_seal\reportable_claim_bundle_seal.json --output-dir C:\Users\wang\Documents\agent-safe-research\outputs\eair_prompt_protocol_matrix_live\paper_tables\paper_ready_claim_bundle_seal\verification --require-reviewed
```

## Required Artifacts

- sampled_transcripts.jsonl
- live_run_doctor.json
- live_run_doctor.md
- secret_value_recorded
- artifact_manifest.json
- structured_action_transcript_replay_results.json
- structured_action_transcript_replay_report.md
- prompt_adherence_audit.json
- prompt_adherence_audit.csv
- prompt_adherence_audit.md
- protocol_legitimacy_table.json
- protocol_legitimacy_table.csv
- protocol_legitimacy_table.md
- protocol_legitimacy_by_prompt_variant.json
- protocol_legitimacy_by_prompt_variant.csv
- protocol_legitimacy_by_prompt_variant.md
- artifact_summary.json
- artifact_summary_influence_contrast_table.json
- artifact_summary_influence_contrast_table.csv
- artifact_summary_influence_contrast_table.md
- artifact_summary_by_model_prompt_condition.csv
- artifact_summary_by_model_prompt_protected_field.json
- artifact_summary_by_model_prompt_protected_field.csv
- artifact_summary_by_model_prompt_protected_field.md
- artifact_summary_warrant_leaderboard.json
- artifact_summary_coverage.csv
- reportable_run_audit.json
- reportable_run_audit.md
- reportable_results_export.json
- reportable_model_condition_table.csv
- reportable_model_condition_table.md
- reportable_warrant_leaderboard.json
- reportable_protected_field_table.json
- reportable_protected_field_table.csv
- reportable_protected_field_table.md
- reportable_reviewer_rejection_protected_field_table.json
- reportable_reviewer_rejection_protected_field_table.csv
- reportable_reviewer_rejection_protected_field_table.md
- reportable_influence_contrast_table.json
- reportable_influence_contrast_table.csv
- reportable_influence_contrast_table.md
- reportable_influence_contrast_pair_table.json
- reportable_influence_contrast_pair_table.csv
- reportable_influence_contrast_pair_table.md
- reportable_closest_neighbor_discriminator_table.json
- reportable_closest_neighbor_discriminator_table.csv
- reportable_closest_neighbor_discriminator_table.md
- reportable_protocol_legitimacy_table.json
- reportable_protocol_legitimacy_table.csv
- reportable_protocol_legitimacy_table.md
- reportable_protocol_legitimacy_by_prompt_variant.json
- reportable_protocol_legitimacy_by_prompt_variant.csv
- reportable_protocol_legitimacy_by_prompt_variant.md
- reportable_export_integrity_audit.json
- reportable_export_integrity_audit.md
- reportable_claims.json
- reportable_claim_citation_audit.json
- reportable_claim_citation_audit.md
- reportable_claim_bundle_seal.json
- reportable_claim_bundle_seal.md
- reportable_claim_bundle_seal_verification.json
- reportable_claim_bundle_seal_verification.md
- paper_ready_claims.json
- paper_ready_claim_review_verification/reportable_claim_review_verification.json
- paper_ready_claim_review_verification/reportable_claim_review_verification.md
- paper_ready_claim_audit/reportable_claim_citation_audit.json
- paper_ready_claim_audit/reportable_claim_citation_audit.md
- paper_ready_claim_bundle_seal/reportable_claim_bundle_seal.json
- paper_ready_claim_bundle_seal/reportable_claim_bundle_seal.md
- paper_ready_claim_bundle_seal/verification/reportable_claim_bundle_seal_verification.json
- paper_ready_claim_bundle_seal/verification/reportable_claim_bundle_seal_verification.md
