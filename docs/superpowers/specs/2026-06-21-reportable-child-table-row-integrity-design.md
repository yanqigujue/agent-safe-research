# Reportable Child Table Row Integrity Design

## Problem

`eair-audit-reportable-export` checked the protocol source hash and child artifact hashes, but a reportable protocol child table could still have its `rows` edited after export while retaining the same recorded source hash. That weakens the paper-table artifact chain.

## Design

Extend the export integrity audit to compare child artifact rows with the main `reportable_results_export.json` payload.

The audit checks:

- `reportable_protocol_legitimacy_table.json.rows` equals `reportable_results_export.json.protocol_legitimacy_rows`;
- `reportable_protocol_legitimacy_by_prompt_variant.json.rows` equals `reportable_results_export.json.protocol_legitimacy_by_prompt_variant`;
- row counts are recorded in `checked_child_artifacts`;
- each child artifact records `rows_match_export`.

On mismatch, the audit writes its JSON/Markdown diagnostics and blocks with a `rows mismatch` error.

## Boundary

This protects post-export reportable artifacts from local row edits. It does not replace source hash verification, reportability audit, or WarrantGuard verification.
