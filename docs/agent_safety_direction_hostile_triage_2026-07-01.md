# Hostile Triage for Agent-Safety Directions

Date: 2026-07-01

Review mode: local adversarial triage. This is not a cross-model `kill-argument` result because no `mcp__codex__codex` reviewer tool is available in this environment.

## Direction 1: Semantic-Role Warrants for Agent Action Fields

### Strongest Rejection Memo

This paper appears to repackage authorization, provenance, and consent-scope checking under new terminology. PCAA already gives proof-carrying agent actions; AuthGraph aligns provenance and authorization; contextual-security work formalizes source authorization; SkillGuard and formal skill verification cover skill permissions; Cordon and consent-integrity style work handle effect scopes and approval boundaries. Saying that each field must consume an authorized source is not a new mechanism. The proposed examples are hand-written, and CapGuard wins because it encodes the labels while weak baselines ignore obvious fields. Unless the paper demonstrates failures that survive a strong boundary/scope checker, the contribution is vocabulary plus synthetic benchmark design.

### Defense

The V2 story directly targets this: `boundary_scope_only` checks field, operation, data scope, effect scope, delegation scope, and specified time scope, but still misses pure semantic-role laundering. The differentiator is not "source authorized" but "boundary-preserving role mismatch."

### Still-Unresolved Risk

Need more rows where boundary checks really are satisfied. One inline regression is not enough for a paper.

### Required Fix

Expand boundary-preserving role mismatch rows to 8-10 cases across approval, risk/report, side-effect, delegation, and data-scope fields.

## Direction 2: Authority Attenuation for Derived Agent Artifacts

### Strongest Rejection Memo

Authority attenuation is a known principle in information-flow security and authorization propagation. Recent memory-authority and protocol-composition work already discuss laundering, transformation, and origin-bound authority. Claiming that summaries or skill outputs should not inherit full authority is intuitive and may not need a new paper. Without a crisp transformation algebra or empirical evidence from real agent traces, this direction risks being a small rule inside a broader authorization framework.

### Defense

The direction becomes stronger when framed as part of AFW: transformations produce derived artifacts whose `Cap(transform(x))` is checked by the same field-warrant verifier. It is not a separate broad theory claim; it is an operational mechanism for preventing derived summaries and skill outputs from becoming approval/delegation authority.

### Still-Unresolved Risk

Only two rows currently exist. No taxonomy of transformations is implemented.

### Required Fix

Add rows for summarize, extract, translate, merge, compress, and rank. Each should preserve one narrow role and block one higher-authority role.

## Direction 3: Counter-Authority Routing

### Strongest Rejection Memo

Routing conflicts to review is standard policy enforcement. PCAA, Cordon, pre-action authorization, and many workflow systems already carry receipts, approvals, and policy gates. A three-valued `allow/block/abstain` decision is sensible but not novel. The DLP example is too obvious.

### Defense

Counter-authority is not the main contribution. It is a necessary field-warrant outcome when positive authority exists but a field-local counter-source applies. It makes AFW realistic without claiming review routing as novel.

### Still-Unresolved Risk

If presented as a contribution, it will be killed. Keep it as a subsystem.

### Required Fix

Move counter-authority to supporting mechanism; add varied cases but do not headline it.

## Direction 4: Skill Output Declassification

### Strongest Rejection Memo

This is likely too close to SkillGuard, proof-carrying skills, and skill supply-chain security. If the paper says skill outputs need declassification, reviewers will ask how this differs from skill permissions, capability containment, or taint tracking. The current examples are simple and may look like obvious policy rules.

### Defense

Use it as a source-family slice inside AFW. The key is downstream action-field consumption: the skill can be benign and allowed, but its output is later consumed as delegation, risk, or side-effect authority.

### Still-Unresolved Risk

Standalone skill paper is weak unless we collect real skill traces.

### Required Fix

Do not make it standalone. Fold into attenuation and downstream consumption rows.

## Direction 5: Consent Delta Tracking

### Strongest Rejection Memo

Consent drift is already a known problem, and consent-integrity work is a direct neighbor. If the method tracks deltas between approved and executed actions, that is exactly what a consent-integrity system should do. The novelty over existing consent systems is not clear.

### Defense

The only safe angle is field-level consumption of the approval source: user approval for one effect is a source capability with a narrow `effect_scope`, and AFW prevents it from being consumed by another field/effect.

### Still-Unresolved Risk

Too close as a standalone direction.

### Required Fix

Use consent rows as AFW examples, not as the paper title.

## Direction 6: Minimal Authority Witnesses

### Strongest Rejection Memo

Minimal witness extraction sounds like provenance summarization. AuthGraph and other provenance systems already reason over source graphs. Unless minimality changes a decision, reduces audit cost with measured evidence, or exposes failures missed by provenance, it is a nice UX feature rather than a research contribution.

### Defense

Useful when paired with AFW: for each protected field, find the minimal set of source capabilities covering `Need(s,f)`, then expose missing roles and inherited obligations.

### Still-Unresolved Risk

No audit-cost metric yet. The minimum implementation now exists, but it has not shown measured value over full provenance.

### Required Fix

Keep as a supporting audit object. Do not promote to a standalone contribution unless it reduces audit cost or changes decisions on multi-source traces.

## Direction 7: Authority-Confusion Fuzzing

### Strongest Rejection Memo

Another synthetic benchmark generator is unlikely to be accepted unless it exposes real failures or generates non-obvious cases. Grammar-guided mutation over fields/scopes may simply reproduce the verifier's own rules.

### Defense

This can be a useful evaluation engine for AFW if it starts from structured agent traces and generates adversarial rows across semantic role, boundary scope, transformation, and counter-authority axes.

### Still-Unresolved Risk

Generator-validity circularity.

### Required Fix

Keep fuzzing as an evaluation engine, not the main contribution. The first acceptable version should preserve trace boundaries and mutate only one authority dimension at a time.

## Current Verdict

| Direction | Verdict | Reason |
|---|---|---|
| AFW V2 | KEEP | Strongest after adding boundary-scope baseline and attenuation. |
| Authority attenuation | KEEP AS MECHANISM | Strong as AFW mechanism, weak as standalone. |
| Counter-authority | SUPPORTING ONLY | Necessary but not headline-novel. |
| Skill output declassification | FOLD IN | Good source-family slice, weak standalone. |
| Consent delta | FOLD IN | Too close to consent integrity. |
| Minimal witnesses | SUPPORTING ONLY | Implemented as an audit object, but still needs audit-cost metric. |
| Authority fuzzing | SUPPORTING ENGINE | Seeded trace-derived generator reduces, but does not eliminate, circular synthetic-benchmark risk. |

## Hard Next Requirement

The 40-row V2 benchmark seed is now in place:

- 8 boundary-preserving role mismatch rows;
- 8 derived-artifact attenuation rows;
- 8 composite non-amplification rows;
- 6 counter-authority rows;
- 10 same-source cross-field rows.

The next hard requirement is no longer more prose or more hand-authored rows. It is one of:

1. faithful implementations of close-neighbor baselines, especially AuthGraph-style parameter provenance and consent/scope guards;
2. real or semi-real agent traces showing source transformation and role laundering;
3. a row-generation protocol that produces boundary-preserving role mismatch cases without simply encoding CapGuard labels.

Current progress:

- faithful-style baselines now exist for field attribution, AuthGraph-style parameter provenance, and skill permission;
- a structured trace-to-row adapter seed exists, but it is not yet real log evidence;
- a trace-derived authority-confusion generator now produces a boundary-preserving role mutation from that seed. On the generated row, CapGuard blocks laundering while boundary-scope, field-attribution, and skill-permission baselines false-allow it.
- minimal authority witness extraction now surfaces the smallest capability set, covered roles, missing roles, and inherited obligations for each field decision.
- conservative skill-manifest and generic authority-manifest adapters now lift explicit roles and scopes into `Cap(x)`, reducing the hand-authored capability objection for skill-driven and approval-driven traces.
- obligation discharge rows now show that role and scope coverage can still be insufficient when inherited obligations are dropped.
- temporal rows now show that a source with the right role and scope can still fail when reused outside its policy or preference epoch.

If AFW still wins under `boundary_scope_only` plus a faithful AuthGraph-style baseline on trace-derived rows, the innovation story becomes much more defensible.
