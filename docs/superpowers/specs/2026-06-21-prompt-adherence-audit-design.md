# Prompt Adherence Audit Design

Date: 2026-06-21

## Problem

The live matrix runbook can tell us what prompt protocols should be run, and replay can tell us whether actions and warrants are safe. A missing layer remains: after transcripts exist, we need to check whether each prompt variant followed its requested output protocol.

## Design

Add `eair-audit-prompt-adherence`.

The audit reads transcript JSONL/JSON and checks:

- action-only prompts parse as actions and do not include top-level warrants;
- proof-carrying prompts include top-level `action` and `warrant`;
- strict proof-carrying prompts include non-empty warrant fields for decision, approval, risk level, risk report, and any action parameters.

The audit writes:

- `prompt_adherence_audit.json`
- `prompt_adherence_audit.csv`
- `prompt_adherence_audit.md`

## Boundary

This audit checks response protocol adherence only. It does not verify evidence legitimacy, source diversity, policy legality, parameter safety, or action safety. Those remain WarrantGuard/replay responsibilities.

