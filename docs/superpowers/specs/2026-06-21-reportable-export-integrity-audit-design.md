# Reportable Export Integrity Audit Design

## Problem

Iteration 067 records `protocol_legitimacy_sha256` inside reportable exports, but the recorded hash needs a post-export verifier. Without one, a paper table can say which source file it came from, yet the pipeline cannot later prove that the source file still matches the recorded digest.

## Design

Add `eair-audit-reportable-export`.

The command reads `reportable_results_export.json` and writes:

- `reportable_export_integrity_audit.json`
- `reportable_export_integrity_audit.md`

The audit checks:

- the export artifact type is `eair_reportable_results_export`;
- the export is marked `reportable=true`;
- `protocol_legitimacy_path` and `protocol_legitimacy_sha256` are both present or both absent;
- when present, the current SHA256 of the source protocol table matches the export;
- reportable protocol child artifacts carry the same protocol source hash.

On failure, the audit writes the diagnostic files and exits with a blocking error.

## Boundary

This is an artifact-integrity audit. It does not prove live-model behavior, replace manifest verification, or determine whether WarrantGuard decisions are correct. It makes the reportable paper-table chain reproducible after export.
