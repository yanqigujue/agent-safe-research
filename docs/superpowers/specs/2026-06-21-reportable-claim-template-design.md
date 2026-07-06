# Reportable Claim Template Design

## Problem

The live runbook requires `reportable_claims.json`, but writing a claim manifest fully by hand makes the evidence factory easier to skip or mis-pin.

## Design

Add `eair-write-reportable-claim-template`.

Inputs:

- `reportable_results_export.json`
- `reportable_export_integrity_audit.json`

Output:

- `reportable_claims.json`

The generated starter manifest includes SHA-pinned claims for:

- WarrantGuard leaderboard quality scores;
- protocol-legitimacy aggregate gaps;
- reportable export integrity pass status.

## Boundary

This is a starter manifest. Authors should review and edit claim text before using it in paper prose. The generator does not infer every possible paper claim.
