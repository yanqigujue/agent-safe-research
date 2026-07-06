# Prompt Protocol Adherence Audit

Checks response protocol adherence only; it does not verify evidence legitimacy or action safety.

| metric | value |
|---|---:|
| total_transcripts | 1 |
| compliant_count | 1 |
| noncompliant_count | 0 |
| compliance_rate | 1.0000 |

## By Prompt Variant

| prompt_variant | total | compliant | noncompliant | compliance_rate |
|---|---:|---:|---:|---:|
| default | 1 | 1 | 0 | 1.0000 |

## Rows

| transcript_id | prompt_variant | expected_protocol | compliant | errors |
|---|---|---|---|---|
| live_warrant_duplicate_fail | default | action_only_allowed | true | none |
