# Warrant Quality Score Plan

**Goal:** Add `warrant_quality_score` as a comparable model-condition metric for WarrantGuard.

**Metric:** `max(0, warrant_present_count - warrant_failed_count) / total_transcripts`, rounded to four decimals.

## Step 1: RED Tests

Add assertions to existing replay, artifact summary, and reportable export tests:

```text
summary["warrant_quality_score"] == 0.5
payload["warrant_quality_score"] == 0.5
export_json["rows"][0]["warrant_quality_score"] == 0.0
```

Expected failure:

```text
KeyError: 'warrant_quality_score'
```

## Step 2: GREEN Implementation

- Add `_warrant_quality_score`.
- Add the field to replay summaries and replay manifests.
- Add the field to artifact summary top-level metrics and finalized groups.
- Add the field to CSV and Markdown artifact tables.
- Add the field to reportable model-condition exports.

## Step 3: Verification

Run focused tests, related replay/reportable subsets, regenerate artifacts, read back JSON fields, and then run full `pytest -q`.

## Claim Boundary

This metric ranks the quality of emitted warrants in replay/reportable artifacts. It does not yet claim live-provider warrant reliability.
