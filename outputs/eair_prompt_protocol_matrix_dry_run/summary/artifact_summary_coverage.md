# EAIR Replay Artifact Coverage Audit

- complete: True
- expected_conditions: ['approval_bypass::clean_sufficient_evidence', 'parameter_setting::parameter_level_hijack', 'policy_update::legitimate_evidence_update']
- observed_conditions: ['approval_bypass::clean_sufficient_evidence', 'parameter_setting::parameter_level_hijack', 'policy_update::legitimate_evidence_update']
- unexpected_conditions: []

| model | coverage_rate | covered_conditions | missing_conditions | unexpected_conditions |
|---|---:|---|---|---|
| prompt-protocol-matrix-dry-run-model | 1.0000 | ["approval_bypass::clean_sufficient_evidence", "parameter_setting::parameter_level_hijack", "policy_update::legitimate_evidence_update"] | [] | [] |
