# EAIR Replay Artifact Coverage Audit

- complete: True
- expected_conditions: ['approval_bypass::clean_sufficient_evidence', 'approval_bypass::risk_report_downgrade_no_tool', 'parameter_setting::parameter_level_hijack', 'policy_update::legitimate_evidence_update']
- observed_conditions: ['approval_bypass::clean_sufficient_evidence', 'approval_bypass::risk_report_downgrade_no_tool', 'parameter_setting::parameter_level_hijack', 'policy_update::legitimate_evidence_update']
- unexpected_conditions: []

| model | coverage_rate | covered_conditions | missing_conditions | unexpected_conditions |
|---|---:|---|---|---|
| complete-dry-run-openai-compatible | 1.0000 | ["approval_bypass::clean_sufficient_evidence", "approval_bypass::risk_report_downgrade_no_tool", "parameter_setting::parameter_level_hijack", "policy_update::legitimate_evidence_update"] | [] | [] |
