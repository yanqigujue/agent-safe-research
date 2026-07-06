# Action-Warrant Transcript Replay Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend structured transcript replay and sampler prompts from bare action JSON to optional `(action, warrant)` JSON.

**Architecture:** Keep existing bare-action parsing as the compatibility path. Add warrant parsing and verification only when top-level `warrant` is present, then report warrant diagnostics in replay results.

**Tech Stack:** Python dataclasses, JSONL replay fixtures, pytest, existing EAIR-Bench replay writers.

---

### Task 1: Parse Model-Supplied Warrants

**Files:**
- Modify: `tests/test_eair_bench.py`
- Modify: `formaltrust_platform/experiments/eair_bench.py`

- [ ] **Step 1: Write failing replay test**

Add a test with two JSONL transcript rows. The first contains a valid `action` and `warrant`; the second contains an action with a warrant that lacks independent source-diverse support.

- [ ] **Step 2: Run red test**

Run:

```powershell
pytest tests/test_eair_bench.py::test_structured_action_transcript_replay_verifies_model_supplied_warrants -q
```

Expected: FAIL because replay summary does not expose warrant counts.

- [ ] **Step 3: Implement parser and replay verification**

Add `warrant_from_mapping`, `warrant_to_dict`, `action_warrant_from_mapping`, and `action_warrant_from_model_output`. Update replay to preserve mapping outputs and verify warrants when present.

- [ ] **Step 4: Run green test**

Run:

```powershell
pytest tests/test_eair_bench.py::test_structured_action_transcript_replay_verifies_model_supplied_warrants -q
```

Expected: PASS.

### Task 2: Upgrade Sampler Prompt

**Files:**
- Modify: `tests/test_eair_bench.py`
- Modify: `formaltrust_platform/experiments/eair_bench.py`

- [ ] **Step 1: Write failing prompt assertion**

Assert the sampler request prompt contains `"warrant"` and `decision_claims`.

- [ ] **Step 2: Run red test**

Run:

```powershell
pytest tests/test_eair_bench.py::test_openai_compatible_sampler_writes_replayable_transcript_jsonl -q
```

Expected: FAIL because the old prompt requests bare action fields only.

- [ ] **Step 3: Update prompt text**

Ask for one JSON object with top-level `action` and `warrant` objects.

- [ ] **Step 4: Run green test**

Run:

```powershell
pytest tests/test_eair_bench.py::test_openai_compatible_sampler_writes_replayable_transcript_jsonl -q
```

Expected: PASS.

### Task 3: Refresh Replay Fixture

**Files:**
- Modify: `examples/data/eair_structured_action_transcripts.jsonl`
- Generated: `outputs/eair_transcript_replay_pilot/structured_action_transcript_replay_results.json`
- Generated: `outputs/eair_transcript_replay_pilot/structured_action_transcript_replay_report.md`

- [ ] **Step 1: Add warrant fixture rows**

Append one passing and one failing `(action, warrant)` transcript row.

- [ ] **Step 2: Regenerate replay artifacts**

Run:

```powershell
@'
from pathlib import Path
from formaltrust_platform.experiments.eair_bench import run_structured_action_transcript_replay

run_structured_action_transcript_replay(
    Path("examples/data/eair_structured_action_transcripts.jsonl"),
    output_dir=Path("outputs/eair_transcript_replay_pilot"),
)
'@ | python -
```

Expected: replay results report `total_transcripts=6`, `warrant_present_count=2`, and `warrant_failed_count=1`.

