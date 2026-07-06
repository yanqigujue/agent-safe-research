# Reportable Live Matrix Runbook Design

Date: 2026-06-21

## Problem

The live prompt-matrix template and readiness checker specify the planned experiment, but the handoff from preflight to reportable paper artifacts was only a Markdown checklist. For autonomous iteration and auditability, the runbook should also be machine-readable.

## Design

Upgrade `eair-write-live-runbook` to write two artifacts:

- Markdown runbook for humans.
- JSON sidecar for automation and audit.

The JSON sidecar records:

- config, model, output directories;
- expected conditions;
- scenario count, prompt variants, planned transcript count;
- nine named commands:
  - live preflight doctor;
  - live config check;
  - provider sampling and replay;
  - prompt adherence audit;
  - protocol-legitimacy table and prompt aggregate export;
  - replay manifest verification;
  - coverage-gated summary;
  - reportability audit;
  - paper-table export;
- required artifacts, including the reportable WarrantGuard leaderboard.

## Boundary

The runbook is not live-model evidence. It is the reproducible handoff contract that must be executed before any live-model claim.
