# Agent Search Cases Package

Created: 2026-07-07T17:01:38

## Contents

- `agent_search_cases.jsonl`: 660 append-only agent scenario cases.
- `test_results.json`: local JSON/schema/dedup validation and distributions.
- `qwen3_8b_check.json`: Ollama qwen3:8b review output.
- `source_refs.json`: deduplicated public source references from the cases.

## Validation Summary

- Rows: 660
- Latest id: `agent-search-20260707-r30-660`
- Dataset SHA256: `c2470844ff142c6956346c4f46e8bc930695c52b63b3cf29a455284e29c4b891`
- JSON errors: 0
- Schema errors: 0
- Duplicate ids: 0
- Duplicate fingerprints: 0
- Validation pass: True

## Oracle Decision Distribution

```json
{
  "block": 387,
  "require_human_approval": 81,
  "abstain": 16,
  "allow": 176
}
```

## Domain Group Distribution

```json
{
  "power_grid": 191,
  "non_power": 469
}
```

## qwen3:8b Check

Status: `ok`

```json
{
  "schema_ok": true,
  "oracle_clear": true,
  "allow_controls_reasonable": true,
  "duplicate_risk": false,
  "issues": [
    "The 'no_error_authorized_action' failure mode is the most common, which may indicate a systemic issue with the authorization logic.",
    "The 'rag_evidence_insufficient' and 'rag_evidence_pollution' failure modes are not fully addressed in the expected decision distribution, which may lead to under-blocking.",
    "The 'tool_wrong_tool' and 'tool_wrong_parameter' failure modes are relatively high in the top failure modes but have lower expected decision blocks, which may indicate a misalignment between failure modes and control measures."
  ]
}
```
