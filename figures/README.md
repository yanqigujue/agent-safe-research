# WarrantGuard Figure Artifacts

This directory contains deterministic, editable SVG figures for the current WarrantGuard / EAIR-Bench paper direction.

## Figure 1: Proof-Carrying Action Chain

- SVG: `fig1_eair_main_chain.svg`
- Spec: `specs/fig1_eair_main_chain.json`
- Preview: `fig1_preview.png`
- Purpose: introduces WarrantGuard as a proof-carrying action pattern.
- Suggested caption: "WarrantGuard requires high-risk RAG-agent actions to carry evidence warrants that can be verified before execution."

## Figure 2: Legitimate Influence vs Hijack Influence

- SVG: `fig2_legitimate_vs_hijack_influence.svg`
- Spec: `specs/fig2_legitimate_vs_hijack_influence.json`
- Preview: `fig2_preview.png`
- Purpose: main conceptual figure for the paper's core novelty.
- Suggested caption: "EAIR does not try to stop evidence from influencing actions; it distinguishes legitimate evidence influence from hijack-style influence caused by poisoned, stale, or conflicting evidence."

## Figure 3: Three-Layer WarrantGuard Verifier

- SVG: `fig3_three_layer_gate.svg`
- Spec: `specs/fig3_three_layer_gate.json`
- Preview: `fig3_preview.png`
- Purpose: explains how the method is implemented as an external verifier.
- Suggested caption: "WarrantGuard verifies hard action obligations, evidence sufficiency, and counter-warrant signals before allowing, blocking, or routing a high-risk action to human approval."

## Power-Ops Action Invariance Figure 1: Architecture

- SVG: `power_ops_action_invariance_architecture.svg`
- Spec: `specs/power_ops_action_invariance_architecture.json`
- Purpose: shows how authority-bearing sources are lifted into `Cap(x)`, how action fields become `Need(s,f)`, and how CapGuard feeds fieldwise repair.
- Suggested caption: "Field-level action-invariance architecture. CapGuard checks whether each action field is covered by a valid capability and repairs only invalid fields."

## Power-Ops Action Invariance Figure 2: Repair Frame

- SVG: `power_ops_action_invariance_repair_frame.svg`
- Spec: `specs/power_ops_action_invariance_repair_frame.json`
- Purpose: explains the core invariant: authorized fields remain executable while unauthorized fields are removed or routed to partial review.
- Suggested caption: "Repair-frame action invariance preserves authorized fields in a mixed action while routing unauthorized fields to partial human review."

## Power-Ops Action Invariance Figure 3: Evidence Ladder

- SVG: `power_ops_action_invariance_result_ladder.svg`
- Spec: `specs/power_ops_action_invariance_result_ladder.json`
- Purpose: makes the claim boundary explicit: current evidence reaches curated, trace, and bridge fixtures, but not production evidence.
- Suggested caption: "Evidence and claim boundary ladder for the current power-ops action-invariance artifact."

## Editing Workflow

Edit the JSON specs under `figures/specs/`, then re-render with:

```powershell
$env:PYTHONIOENCODING='utf-8'
python C:\Users\wang\.codex\skills\figure-spec\scripts\figure_renderer.py render figures\specs\<spec>.json --output figures\<figure>.svg
```

Power-ops action-invariance figures:

```powershell
$env:PYTHONIOENCODING='utf-8'
python C:\Users\wang\.codex\skills\figure-spec\scripts\figure_renderer.py render figures\specs\power_ops_action_invariance_architecture.json --output figures\power_ops_action_invariance_architecture.svg
python C:\Users\wang\.codex\skills\figure-spec\scripts\figure_renderer.py render figures\specs\power_ops_action_invariance_repair_frame.json --output figures\power_ops_action_invariance_repair_frame.svg
python C:\Users\wang\.codex\skills\figure-spec\scripts\figure_renderer.py render figures\specs\power_ops_action_invariance_result_ladder.json --output figures\power_ops_action_invariance_result_ladder.svg
```
