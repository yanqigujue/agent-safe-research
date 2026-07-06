# Reportable Claim Template Overwrite Guard Design

## Problem

`eair-write-reportable-claim-template` creates a starter `reportable_claims.json` from reportable artifacts. After an author reviews or edits that file, rerunning the template command can silently replace human-reviewed claim text and citation decisions.

## Design

The template writer treats an existing output file as protected by default. If `reportable_claims.json` already exists, the API raises a concise error and the CLI exits with code 2. A caller can explicitly pass `--force` to regenerate the starter template.

This keeps the boundary clear: the command is safe for first-pass initialization, while deliberate regeneration remains possible for fixture refreshes or early draft churn.

## Interfaces

- `write_reportable_claim_template(..., force: bool = False)`.
- `formaltrust eair-write-reportable-claim-template --force`.

## Testing

Add a CLI regression test that writes a human-reviewed placeholder file, runs the template command without `--force`, verifies the command fails and the file content is unchanged, then reruns with `--force` and verifies the template is written.
