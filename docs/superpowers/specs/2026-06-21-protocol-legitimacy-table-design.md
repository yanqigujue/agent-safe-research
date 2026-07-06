# Protocol-Legitimacy Table Design

Date: 2026-06-21

## Problem

Prompt adherence and WarrantGuard quality currently live in separate artifacts. The paper needs one table that shows whether a model followed the response protocol and whether the resulting warrant was legitimate.

## Design

Add `eair-export-protocol-legitimacy-table`.

Inputs:

- `prompt_adherence_audit.json`
- `artifact_summary.json`

Join key:

```text
model x prompt_variant x case_id::condition
```

Outputs:

- `protocol_legitimacy_table.json`
- `protocol_legitimacy_table.csv`
- `protocol_legitimacy_table.md`

Primary columns:

- prompt adherence rate;
- WarrantGuard quality score;
- adherence-legitimacy gap;
- warrant error categories;
- gate and influence counts.

## Interpretation

A large positive gap means the transcript followed the prompt protocol, but the warrant or action still failed WarrantGuard. This directly supports the distinction between protocol adherence and evidence/action legitimacy.

