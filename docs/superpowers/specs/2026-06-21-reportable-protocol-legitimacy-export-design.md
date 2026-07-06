# Reportable Protocol-Legitimacy Export Design

## Problem

Protocol-legitimacy tables exist as intermediate artifacts, but paper-facing export only carried model-condition and WarrantGuard leaderboard tables. A user could still cite a protocol-legitimacy table without proving that the underlying run passed reportability gates.

## Design

Extend `eair-export-reportable-results` with an optional input:

```text
--protocol-legitimacy protocol_legitimacy_table.json
```

When the reportability audit and coverage gate pass, the export writes:

```text
reportable_protocol_legitimacy_table.json
reportable_protocol_legitimacy_table.csv
reportable_protocol_legitimacy_table.md
reportable_protocol_legitimacy_by_prompt_variant.json
reportable_protocol_legitimacy_by_prompt_variant.csv
reportable_protocol_legitimacy_by_prompt_variant.md
```

The main export JSON records `protocol_legitimacy_path` and `protocol_legitimacy_row_count`.

## Boundary

This does not make intermediate dry-run protocol tables reportable. It only carries protocol-legitimacy rows forward after the existing live-reportability gate has passed.
