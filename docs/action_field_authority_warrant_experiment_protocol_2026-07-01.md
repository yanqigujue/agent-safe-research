# AFW Experiment Protocol

Date: 2026-07-01

This file turns the AFW idea into an executable experiment plan aligned with current project interfaces and artifacts.

## Claim Ladder

The paper should climb claims in this order:

1. **Problem claim:** agents can launder a source's valid use into the wrong action-field semantic role.
2. **Representation claim:** `Cap(x)` and `Need(s,f)` express this problem across RAG, skill, tool metadata, memory, approval, and prior output sources.
3. **Algorithm claim:** CapGuard checks field-level authority coverage and returns minimal witnesses.
4. **Benchmark claim:** same-source paired rows and trace-derived mutations expose errors missed by permission, attribution, and scope-only baselines.
5. **Systems claim:** the method can be integrated into FormalTrust as a guardrail/evaluator using `metrics` and `artifacts`.

Do not claim:

- first authorization framework;
- first provenance-aware agent defense;
- official failure of named systems not actually run;
- deployment safety;
- live-model superiority before running live traces.

## Current Evidence

Current deterministic assets:

```text
40-row V2 rollup:
  same-source 10
  composite 8
  counter-authority 6
  attenuation 8
  boundary-role 8

mechanism slices:
  obligation 2
  temporal 2

trace seed:
  trace scenarios 22
  generated role-confusion rows 41

power-ops domain slice:
  paired rows 30
  trace scenarios 20
  generated power-ops role-confusion rows 40
```

Current validation:

```powershell
pytest tests\test_afw_bench.py -q
```

Expected:

```text
38 passed
```

## Experiment Blocks

### E0: Schema and Interface Sanity

Purpose:

```text
prove rows instantiate the AFW interface cleanly
```

Inputs:

- all `examples/afw_*.json` row files;
- `examples/afw_trace_scenarios.json`.

Checks:

- JSON parse;
- required row fields;
- `capability` or `capabilities`;
- legal and laundered consumption;
- expected labels;
- all `need` objects have `required_role` or `required_roles`.

Success:

```text
100% parse and no structural errors
```

### E1: Main Same-Source Contrast

Purpose:

```text
show same source can be valid in one field and invalid in another
```

Inputs:

```text
examples/afw_same_source_paired_rows.json
```

Baselines:

```text
capguard
permission_only
attribution_only
strict_block
```

Metrics:

- legal preservation rate;
- laundering block rate;
- false allow rate;
- false block rate;
- same-source contrast gap.

Success pattern:

| Baseline | Expected |
|---|---|
| CapGuard | legal preservation 1.0, laundering block 1.0 |
| permission-only | false allow 1.0 |
| attribution-only | false allow 1.0 |
| strict-block | false block 1.0 |

### E2: Strong Neighbor Discriminator

Purpose:

```text
show the contribution is not only boundary/scope checking
```

Inputs:

```text
examples/afw_boundary_role_rows.json
trace-generated role-confusion rows
```

Baselines:

```text
capguard
boundary_scope_only
field_attribution_only
skill_permission_style
```

Success pattern:

```text
boundary scopes pass
semantic role fails
CapGuard blocks
boundary_scope_only false-allows
```

This is the most important table after the main same-source contrast.

### E3: Source-Family Generalization

Purpose:

```text
show AFW is not only RAG evidence checking
```

Inputs:

- evidence rows;
- skill rows;
- tool metadata rows;
- memory rows;
- user approval rows;
- prior-step output rows.

Metrics:

- legal preservation by source family;
- laundering block/reject by source family;
- missing-role explanations by source family.

Success:

```text
same Cap/Need interface covers all families without per-family verifier rewrite
```

### E4: Composition and Attenuation

Purpose:

```text
show multiple sources can satisfy a field, but transformations/compositions do not create new roles
```

Inputs:

```text
examples/afw_composite_authority_rows.json
examples/afw_attenuation_rows.json
```

Metrics:

- legal preservation;
- laundering block;
- witness size;
- missing roles;
- witness compression.

Success:

```text
CapGuard allows narrow composite authority
CapGuard blocks external roles absent from all capabilities
minimal witness is smaller than full context where redundant sources exist
```

### E5: Counter-Authority, Obligation, and Temporal Mechanisms

Purpose:

```text
make AFW realistic without making these the headline novelty
```

Inputs:

```text
examples/afw_counter_authority_rows.json
examples/afw_obligation_rows.json
examples/afw_temporal_rows.json
```

Metrics:

- abstain rate;
- laundering reject rate;
- undischarged obligations;
- time-scope mismatch block rate.

Success:

```text
counter-authority routes to abstain
must_discharge obligations must be discharged
expired/stale authority is blocked
```

### E6: Trace-Derived Authority Confusion

Purpose:

```text
reduce the "hand-written synthetic benchmark" objection
```

Inputs:

```text
examples/afw_trace_scenarios.json
```

Procedure:

1. Load scenarios with `load_trace_scenarios_as_rows`.
2. Generate role-confusion rows with `generate_authority_confusion_rows`.
3. Verify held-fixed dimensions.
4. Run baselines.
5. Human-audit plausibility.

Metrics:

- generated row count;
- mutation validity rate;
- CapGuard laundering block rate;
- boundary-scope false allow rate;
- human plausibility agreement.

Current seed:

```text
2 scenarios
1 general generated role-confusion row
40 power-ops generated role-confusion rows
```

Current power-ops scale:

```text
20 semi-real scenarios
40 generated rows
```

Target before paper:

```text
40 generated rows with generated audit sheet; human labels pending
```

### E7: FormalTrust Integration Smoke Test

Purpose:

```text
show AFW can run as a platform guardrail/evaluator
```

The row/trace guardrail smoke test is now implemented. The live candidate-action YAML graph is still future implementation work.

Minimum requirements:

- `guardrail.afw_capguard` node uses `@node`.
- It reads AFW inputs from config paths or `metrics["afw_rows"]`.
- It returns `metrics["afw_gate_decision"]`, `metrics["afw_capguard_summary"]`, `metrics["afw_baseline_summaries"]`, and `metrics["afw_sources"]`.
- It never returns unknown top-level state fields.
- It routes normal safety blocks through metrics, not exceptions.
- Future runtime extension returns `metrics["afw_field_results"]` and `metrics["final_action"]` for candidate-action cases.
- A YAML graph can run one mock case.

Acceptance commands after implementation:

```powershell
pytest tests/test_interfaces.py tests/test_afw_bench.py
pytest tests/test_mvp.py
formaltrust run --config examples/afw_validation.yaml
```

## Baseline Interpretation

| Baseline | What it means | What it cannot prove |
|---|---|---|
| `permission_only` | source/tool is allowed | field semantic authority |
| `attribution_only` | field names or uses a source | source may govern that field |
| `strict_block` | blocks all questionable use | legal utility |
| `boundary_scope_only` | checks field/operation/data/effect/delegation/time | semantic-role validity |
| `field_attribution_only` | field has a named source | source has correct role |
| `authgraph_style_parameter_provenance` | parameter source edge is authorized | non-parameter approval/risk/delegation authority |
| `skill_permission_style` | direct skill effect fits manifest | downstream consumption of skill output |

These are faithful-style discriminators, not official prior-work reproductions.

## Tables to Produce

### Main Table 1: Same-Source Contrast

Rows:

- baseline;
- legal preservation;
- laundering block;
- false allow;
- false block;
- same-source contrast gap.

### Main Table 2: Boundary-Preserving Role Mismatch

Rows:

- CapGuard;
- boundary-scope-only;
- field-attribution-only;
- skill-permission-style.

Columns:

- legal preservation;
- laundering block;
- false allow;
- representative failure.

### Main Table 3: Source-Family Results

Rows:

- evidence;
- skill;
- tool metadata;
- memory;
- user approval;
- prior-step output.

Columns:

- legal preservation;
- laundering reject;
- representative missing role.

### Appendix Table A1: Mechanism Slices

Rows:

- composite;
- attenuation;
- counter-authority;
- obligation;
- temporal.

Columns:

- rows;
- expected decision pattern;
- metric;
- interpretation.

### Appendix Table A2: Witness Audit

Rows:

- representative multi-source rows.

Columns:

- full capability count;
- witness capability count;
- missing roles;
- obligations;
- compression ratio.

## Run Order

1. E0 schema sanity.
2. E1 main same-source contrast.
3. E2 boundary-role discriminator.
4. E3 source-family generalization.
5. E4 composition and attenuation.
6. E5 mechanism slices.
7. E6 trace-derived generation.
8. E7 FormalTrust integration.

Stop condition for this phase:

```text
E0-E6 pass deterministically and produce paper-ready tables
```

Do not run live models until:

- deterministic rows are locked;
- generated trace rows pass human plausibility audit;
- claim firewall is updated to avoid official prior-work overclaims.

## Paper-Ready Success Criteria

Minimum:

```text
CapGuard legal_preservation_rate = 1.0
CapGuard laundering_reject_rate = 1.0
Boundary-role family: boundary_scope_only false_allow_rate = 1.0
Trace-derived generated rows: 40 power-ops rows pending human plausibility audit
```

Better:

```text
40-100 trace-derived generated rows with plausibility audit
at least 3 source families represented in trace-derived rows
minimal witness compression measured on multi-source rows
obligation and temporal slices reported as mechanism support
```

## Risks

| Risk | Mitigation |
|---|---|
| Looks like access control | Lead with boundary-preserving semantic-role mismatch. |
| Looks hand-written | Expand trace-derived rows and human plausibility audit. |
| Looks like AuthGraph | Avoid ordinary parameter provenance as main claim. |
| Looks like SkillGuard | Make skill direct effect legal; test downstream consumption. |
| Looks like consent/scope | Use rows where all boundaries match but role differs. |
| Looks too broad | Keep obligation/time/counter-authority as extensions. |
