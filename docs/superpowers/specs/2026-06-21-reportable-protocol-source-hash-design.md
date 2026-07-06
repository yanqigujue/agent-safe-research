# Reportable Protocol Source Hash Design

## Problem

Reportable exports record `protocol_legitimacy_path`, but a path alone is weak provenance. The source protocol table could be replaced after export, making it harder to audit which diagnostic artifact produced the paper-facing files.

## Design

When `--protocol-legitimacy` is supplied:

- compute SHA256 for the source protocol table;
- write `protocol_legitimacy_sha256` to `reportable_results_export.json`;
- write the same hash to `reportable_protocol_legitimacy_table.json`;
- write the same hash to `reportable_protocol_legitimacy_by_prompt_variant.json`.

## Boundary

This is source integrity metadata. It does not replace row alignment, metric consistency, or replay verification.
