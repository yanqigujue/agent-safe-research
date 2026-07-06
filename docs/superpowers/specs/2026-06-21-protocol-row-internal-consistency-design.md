# Protocol Row Internal Consistency Design

## Problem

Reportable protocol export now checks row membership and selected summary metrics, but protocol-specific fields can still be internally inconsistent. For example, a row may claim `prompt_adherence_rate=0.5` while also claiming one compliant transcript out of one total transcript.

## Design

Before exporting reportable protocol artifacts, validate each protocol row:

- `prompt_adherence_total == total_transcripts`
- `prompt_adherence_compliant_count + prompt_adherence_noncompliant_count == prompt_adherence_total`
- `prompt_adherence_rate == compliant / prompt_adherence_total`
- `adherence_legitimacy_gap == prompt_adherence_rate - warrant_quality_score`

Any violation blocks reportable export.

## Boundary

This gate validates arithmetic consistency inside protocol rows. It does not validate the semantic truth of prompt adherence labels.
