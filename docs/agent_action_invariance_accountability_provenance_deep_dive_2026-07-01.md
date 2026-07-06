# Agent Action Invariance: Accountability, Provenance, And Threshold Authority Deep Dive

Date: 2026-07-01

Purpose: connect AFW / CapGuard to traditional accountability, cryptographic
audit, provenance, threshold authorization, and supply-chain integrity theory.

The working question is:

```text
If a guard preserves an authorized action field, can we later prove who granted
that authority, whether enough independent authority existed, and whether the
witness log was altered?
```

This line does not replace action invariance. It strengthens the audit object
behind it:

```text
Witness(s,f)
  from: minimal explanation for an allow/block/abstain field decision
  to: accountable, tamper-evident, source-provenance-aware authority record
```

## 1. Why This Direction Matters

Current CapGuard theory already says:

```text
Cap(x) covers Need(s,f) -> preserve field f
otherwise -> block / repair / abstain / route
```

But a reviewer can still ask:

1. Who issued the capability?
2. Was the manifest or approval signed?
3. Did enough independent parties approve a high-risk field?
4. Can the agent or tool later deny that a field consumed a source?
5. Can an attacker rewrite the witness log after execution?
6. Can a stale witness be replayed under a new policy epoch?
7. Can a skill package be trusted as the artifact it claims to be?

This creates a second layer:

```text
authority correctness:
  Does Cap(x) cover Need(s,f)?

authority accountability:
  Is the Cap(x) statement attributable, non-repudiable, fresh, logged,
  and verifiable against source provenance?
```

The paper should not claim new cryptography. The safe claim is narrower:

> We instantiate existing accountability and provenance machinery at the
> source-to-action-field witness boundary of LLM agents.

## 2. Byzantine Fault Tolerance And Quorum Authority

Byzantine fault tolerance starts from a harsh assumption:

```text
some participants may behave arbitrarily or maliciously
```

For agent traces, this maps to:

```text
some sources, tools, skills, memories, approvals, or subagents may be faulty,
compromised, stale, or adversarial
```

The useful transfer is not to run PBFT inside the agent. The useful transfer is
the quorum idea:

```text
High-risk fields may require k-of-n independent authority witnesses.
```

Example:

```text
Need(s, "publish_external_report") =
  role: external_publish_authority
  threshold: 2 of {legal_approval, policy_owner_approval, DLP_clearance}
  independence: issuers must be distinct and non-delegated
```

Candidate property:

```text
Quorum-Sound Composite Authority:
  If a high-risk protected field executes under a threshold requirement,
  then at least k independent valid authority issuers cover Need(s,f), and no
  active counter-authority defeats the quorum.
```

Candidate metrics:

```text
quorum_authority_coverage =
  # threshold-required fields with sufficient independent witnesses
  / # threshold-required fields

source_independence_violation_rate =
  # cases where nominal k-of-n support collapses to dependent issuers
  / # threshold-required cases

byzantine_source_resilience =
  max faulty/corrupted source count under which the guard still blocks
  unauthorized field execution in the scenario family
```

Closest source:

- Castro and Liskov, "Practical Byzantine Fault Tolerance", OSDI 1999.
  <https://www.usenix.org/conference/osdi-99/practical-byzantine-fault-tolerance>

Safe use in AFW:

```text
Use quorum/BFT as a lens for composite authority under faulty sources.
Do not claim a BFT protocol contribution.
```

## 3. Threshold Signatures, Multi-Approval, And No Single Source Of Authority

Threshold cryptography distributes authority:

```text
no single party can produce the protected operation alone;
some threshold of parties must cooperate.
```

For AFW, the analogue is not necessarily a cryptographic threshold signature at
runtime. It can be a policy-level threshold witness:

```text
Witness(s,f) =
  {approval_a, approval_b, scan_receipt_c}
  satisfying threshold policy T_f
```

This is useful for fields where false allow is expensive:

- external publish;
- code deployment;
- money movement;
- user-data export;
- destructive tool use;
- high-risk simulation parameter change;
- self-approval or delegation escalation.

Candidate property:

```text
Threshold Authority Witness:
  A field-level witness is valid for a threshold-protected field only if its
  issuers satisfy the threshold predicate and each issuer's capability covers
  the required role, scope, time, and obligation dimensions.
```

Important distinction:

```text
multi-source evidence support != threshold authority
```

Several sources may support the same factual claim, but only designated
authority issuers should count toward an approval threshold.

Closest sources:

- Shamir, "How to Share a Secret", Communications of the ACM, 1979.
  <https://dl.acm.org/doi/10.1145/359168.359176>
- NIST Multi-Party Threshold Cryptography project.
  <https://csrc.nist.gov/projects/threshold-cryptography>

Safe use in AFW:

```text
Threshold signatures and secret sharing are prior art.
AFW can borrow the threshold-authority pattern for action-field witnesses.
```

## 4. Tamper-Evident Witness Logs

Runtime witness outputs are only useful for audit if the log cannot be silently
rewritten.

Certificate Transparency gives a mature pattern:

```text
append-only log + Merkle tree + inclusion proof + consistency proof
```

AFW mapping:

```text
each field decision emits a witness event:
  step id
  field id
  Need(s,f)
  consumed source ids
  witness hash
  decision: allow/block/abstain/repair
  policy epoch
  obligation receipts
  counter-authority ids
```

These events can be chained or placed in an append-only transparency log.

Candidate properties:

```text
Witness Log Inclusion:
  every executed protected field has a corresponding logged witness event.

Witness Log Consistency:
  an auditor can detect if the sequence of witness events was forked,
  deleted, or rewritten after the fact.

Epoch-Replay Resistance:
  a witness event issued under policy epoch e cannot be reused as authority
  under epoch e' unless the policy explicitly allows it.
```

Candidate metrics:

```text
witness_log_completeness =
  # executed protected fields with logged witness events
  / # executed protected fields

witness_log_tamper_detection_rate =
  # injected log deletion/rewrite/fork attacks detected
  / # injected log tamper attacks

replay_epoch_mismatch_rate =
  # stale/replayed witness attempts detected
  / # stale/replayed witness attempts
```

Closest sources:

- RFC 6962, Certificate Transparency.
  <https://datatracker.ietf.org/doc/html/rfc6962>
- RFC 9162, Certificate Transparency Version 2.0.
  <https://www.rfc-editor.org/info/rfc9162/>

Safe use in AFW:

```text
Do not claim a new transparency-log design.
Claim that action-field authority witnesses can be logged in a CT-style
tamper-evident audit trail.
```

## 5. Provenance Semirings And Minimal Authority Witnesses

Database provenance asks why a result exists. Provenance semirings provide a
formal way to annotate outputs with the input facts used to derive them.

AFW already has a provenance-shaped relation:

```text
Consume(x -> f, s)
```

A field witness can be treated as a provenance expression:

```text
answer.body =
  manual_7 * retrieval_span_3

external_publish =
  legal_approval_2 * dlp_receipt_5
```

In this reading:

```text
* means jointly required authority
+ means alternative satisfying witness paths
```

Then the "minimal authority witness" is analogous to a minimal monomial or
minimal satisfying provenance path.

Why this is useful:

1. It gives a mathematical language for witness compression.
2. It separates alternative authority paths from jointly required roles.
3. It can explain why two sources are not independent.
4. It gives a clean way to audit "which inputs made this field legal."

Candidate property:

```text
Provenance-Minimal Authority Witness:
  Witness(s,f) is minimal if removing any consumed source from the selected
  provenance expression makes Need(s,f) uncovered.
```

Candidate metrics:

```text
provenance_witness_minimality =
  # witnesses where every source is necessary
  / # emitted witnesses

provenance_alternative_coverage =
  # fields with enumerated alternative satisfying witness paths
  / # fields with at least one satisfying path
```

Closest sources:

- Green, Karvounarakis, and Tannen, "Provenance Semirings", PODS 2007.
  <https://dl.acm.org/doi/10.1145/1265530.1265535>
- Green and Tannen, "The Semiring Framework for Database Provenance", PODS
  2017. <https://doi.org/10.1145/3034786.3056125>

Safe use in AFW:

```text
Do not claim new provenance theory.
Use semiring provenance as a compact model for minimal source-to-field
authority witnesses.
```

## 6. Verifiable Credentials For Capabilities

Verifiable Credentials provide an issuer-holder-verifier model for claims that
can be checked cryptographically.

AFW mapping:

```text
issuer:
  policy owner, skill publisher, tool owner, user approver, organization

holder:
  agent runtime, skill registry, memory store, tool registry

verifier:
  CapGuard

credential claim:
  source x has capability Cap(x) for role/scope/time/obligation dimensions
```

This is especially useful for skill-driven agents:

```text
skill manifest says:
  role: report_formatting_authority
  field_scope: report.format
  not: risk_assessment_authority
  issuer: skill_registry
  signature: ...
```

Candidate metric:

```text
signed_manifest_verification_rate =
  # capability manifests with valid issuer signatures
  / # capability manifests consumed by CapGuard
```

Closest source:

- W3C Verifiable Credentials Data Model 2.0.
  <https://www.w3.org/TR/vc-data-model-2.0/>

Safe use in AFW:

```text
VCs are not the contribution.
The contribution is using signed capability claims as inputs to
source-to-field authority checking.
```

## 7. Supply-Chain Provenance For Skills And Tools

Skill-driven agents bring a supply-chain problem:

```text
Which skill artifact produced this output?
Was it the reviewed skill version?
Who signed it?
Was the tool metadata generated by the expected build/deploy chain?
```

Software supply-chain integrity frameworks are a natural fit:

```text
in-toto:
  signed metadata for steps and functionaries

SLSA:
  provenance and attestation for where, when, and how an artifact was produced

Sigstore/Rekor:
  signatures and transparency-log backed signing events
```

AFW mapping:

```text
source x = skill output
Cap(x) depends on:
  skill manifest
  artifact digest
  signer identity
  build provenance
  policy epoch
  runtime invocation context
```

Candidate property:

```text
Supply-Chain-Bound Skill Authority:
  A skill output can contribute to Witness(s,f) only if the skill artifact,
  manifest, signer, and build provenance satisfy the field's required trust
  policy.
```

Candidate metrics:

```text
skill_provenance_verification_rate =
  # skill outputs with verified artifact provenance
  / # skill outputs consumed by protected fields

unreviewed_skill_authority_rejection_rate =
  # protected field consumptions from unsigned/unreviewed skill outputs blocked
  / # such consumptions
```

Closest sources:

- in-toto. <https://in-toto.io/>
- SLSA specification. <https://slsa.dev/spec/v1.2/>
- Sigstore Rekor. <https://docs.sigstore.dev/logging/overview/>

Safe use in AFW:

```text
Do not claim a new supply-chain security framework.
Claim that supply-chain provenance can be lifted into Cap(x) for skill and
tool-metadata sources.
```

## 8. Non-Repudiation And Accountability

Non-repudiation means an actor cannot plausibly deny a prior statement or
action when cryptographic evidence exists.

AFW needs two accountability edges:

```text
issuer accountability:
  source issuer cannot deny granting a capability

consumer accountability:
  agent/tool cannot deny consuming that source for field f
```

This suggests an accountable witness schema:

```json
{
  "field": "risk_report",
  "need": "risk_assessment_authority",
  "consumed_sources": ["risk_team_approval_17"],
  "issuer_signature": "...",
  "agent_consumption_signature": "...",
  "policy_epoch": "2026-Q3",
  "decision": "allow",
  "witness_hash": "..."
}
```

The key is that accountability does not grant authority. It only makes the
authority decision auditable.

Important warning:

```text
Signed wrong authority is still wrong authority.
```

Example:

```text
A signed report-formatting skill manifest does not authorize risk assessment.
The signature proves who issued the limited capability; it does not expand the
capability.
```

## 9. How This Changes The Main AFW Framework

Original AFW:

```text
Cap(x) covers Need(s,f)
```

Accountable AFW:

```text
VerifiedCap(x) =
  Cap(x)
  + issuer identity
  + signature / attestation
  + policy epoch
  + artifact provenance
  + revocation state
  + log inclusion proof

VerifiedCap(x) covers Need(s,f)
```

Original witness:

```text
minimal set of sources covering Need(s,f)
```

Accountable witness:

```text
minimal set of verified, logged, non-revoked, provenance-valid sources covering
Need(s,f), plus the obligations and counter-authority state relevant to f
```

## 10. Best Research Directions From This Pass

### Direction A: Tamper-Evident Authority Witness Logs

Method:

1. Every CapGuard field decision emits a witness event.
2. Events are hash-chained or placed into a Merkle append-only log.
3. Evaluation injects deletion, rewrite, fork, stale-epoch replay, and missing
   witness attacks.

Why strong:

- Easy to explain.
- Directly useful for audit.
- Adds a systems contribution without claiming new cryptography.

Risk:

- Could look like engineering unless tied back to field invariance.

Verdict:

```text
Strong appendix/system extension, especially if we show witness-log
completeness and tamper-detection metrics.
```

### Direction B: Threshold Authority Witnesses

Method:

1. Add `threshold` and `independence` dimensions to `Need(s,f)`.
2. Define a witness valid only if it satisfies k-of-n issuer constraints.
3. Add attack rows where the agent has multiple documents but only one actual
   authority issuer, or where one issuer self-delegates into two roles.

Why strong:

- Good for high-risk domains.
- Extends composite authority rows naturally.
- Gives a clean difference between evidence support and authority approval.

Risk:

- Need avoid turning the paper into access-control policy language.

Verdict:

```text
Very good benchmark and formal extension.
```

### Direction C: Provenance-Semiring Witness Compression

Method:

1. Model source-to-field consumptions as provenance expressions.
2. Report minimal witness monomials for each protected field.
3. Measure witness compression and alternative witness paths.

Why strong:

- Best mathematical modeling hook in this pass.
- Explains minimality better than prose.

Risk:

- Theory overhead may distract if put in main method.

Verdict:

```text
Use as theory subsection or appendix; do not make the whole paper about
semirings unless experiments support it.
```

### Direction D: Verifiable Credential Capability Manifests

Method:

1. Represent skill/tool/approval capabilities as signed claims.
2. CapGuard verifies issuer and revocation before checking coverage.
3. Add rows where unsigned, wrong-issuer, revoked, or stale credentials fail.

Why strong:

- Fits skill-driven agents.
- Makes "Cap(x) comes from where?" much cleaner.

Risk:

- VC ecosystem is broad; keep it as an instantiation.

Verdict:

```text
Good deployment story.
```

### Direction E: Supply-Chain Skill Authority

Method:

1. Bind skill output authority to skill artifact digest, manifest, signer, and
   build provenance.
2. Reject protected-field consumptions from unsigned or unreviewed skill builds.
3. Evaluate skill-output laundering under compromised skill registry or stale
   manifest.

Why strong:

- Moves beyond RAG into skill-driven agents.
- Connects agent safety to software supply-chain security.

Risk:

- Needs implementation evidence to be more than a concept.

Verdict:

```text
Best long-term skill-security expansion.
```

## 11. Ranking

| Rank | Direction | Novelty fit | Implementation cost | Main use |
|---:|---|---:|---:|---|
| 1 | Threshold Authority Witnesses | high | low-medium | formalism + benchmark |
| 2 | Tamper-Evident Witness Logs | medium-high | medium | audit/system extension |
| 3 | Provenance-Semiring Witness Compression | medium-high | low-medium | theory/appendix |
| 4 | Verifiable Credential Capability Manifests | medium | medium | deployment/skill manifests |
| 5 | Supply-Chain Skill Authority | high | high | future skill-driven agent paper |

## 12. Claim Firewall

Do not claim:

- first Byzantine/quorum model;
- first threshold authorization or threshold-signature use;
- first multi-approval workflow;
- first non-repudiation or signed audit log;
- first tamper-evident log, Merkle log, or transparency-log design;
- first provenance, secure provenance, or provenance-semiring model;
- first verifiable credential capability system;
- first software supply-chain provenance, SLSA, in-toto, or Sigstore/Rekor use;
- first accountable AI or agent audit log.

Safe claim:

> AFW lifts these existing mechanisms into a source-to-action-field authority
> witness: a protected field is preserved only when the consumed, verified,
> non-revoked, provenance-valid capabilities cover its Need(s,f), and the
> resulting decision is logged for later audit.

## 13. Plain Version

This direction says:

```text
The guard should not only say "allowed" or "blocked."
It should leave a receipt.

That receipt should answer:
  who authorized this field,
  whether enough independent authorizers agreed,
  whether the source artifact was the reviewed one,
  whether the approval was fresh,
  whether the log was later changed,
  and exactly which field the authority applied to.
```

The strongest insight:

```text
Accountability does not broaden authority.
A signed source can still be the wrong source for a field.
```

