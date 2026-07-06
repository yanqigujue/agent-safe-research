# AFW Figures

Date: 2026-07-01

These Mermaid figures are draft assets for slides or the paper.

## Figure 1: Unified Field-Authority Pipeline

```mermaid
flowchart LR
  A["Retrieved evidence"] --> L["Source adapters"]
  B["Skill instruction/output"] --> L
  C["Tool or MCP metadata"] --> L
  D["Memory"] --> L
  E["User approval"] --> L
  F["Prior step output"] --> L

  L --> CAP["Cap(x): source capability"]
  STEP["Agent step s"] --> FIELD["Protected action fields"]
  FIELD --> NEED["Need(s,f): field requirement"]

  CAP --> VERIFY["CapGuard verifier"]
  NEED --> VERIFY
  VERIFY --> ALLOW["allow"]
  VERIFY --> BLOCK["block"]
  VERIFY --> ABSTAIN["abstain / review"]
```

Caption:

> AFW lifts heterogeneous agent sources into one capability shape, then checks whether each protected action field consumed sources that cover the field's semantic roles and scopes.

## Figure 2: Same-Source Contrast

```mermaid
flowchart TB
  X["Same source x: signed policy evidence"] --> LEGAL["Legal consumption: route_to_simulation"]
  X --> LAUNDER["Laundered consumption: requires_human_approval=false"]

  LEGAL --> PASS["Cap(x) covers Need(s, tool): allow"]
  LAUNDER --> FAIL["Cap(x) does not cover Need(s, approval): block"]
```

Caption:

> The same source is preserved when consumed within scope and rejected when laundered into another semantic role.

## Figure 3: Authority Coverage Dimensions

```mermaid
flowchart LR
  CAP["Cap(x)"] --> R["semantic role"]
  CAP --> F["field"]
  CAP --> O["operation"]
  CAP --> D["data scope"]
  CAP --> E["effect scope"]
  CAP --> G["delegation scope"]
  CAP --> T["time scope"]

  R --> CHECK["coverage query"]
  F --> CHECK
  O --> CHECK
  D --> CHECK
  E --> CHECK
  G --> CHECK
  T --> CHECK

  NEED["Need(s,f)"] --> CHECK
  CHECK --> DECISION["allow / block / abstain"]
```

Caption:

> A field warrant succeeds only when the consumed capabilities cover the field's required role, field, operation, data boundary, side effect, delegation boundary, and any specified time scope.

## Figure 4: Compositional Authority Without Role Amplification

```mermaid
flowchart TB
  U["User approval: local draft only"] --> COMBINE["Multi-source warrant"]
  P["Policy: local draft allowed"] --> COMBINE

  COMBINE --> OK["Need(local_draft): covered"]
  COMBINE --> NO["Need(external_publish): not covered"]

  OK --> ALLOW["allow local draft"]
  NO --> BLOCK["block external publish"]
```

Caption:

> Multiple limited authorities can jointly satisfy a narrow field need, but their composition must not create new semantic roles.

## Figure 5: Counter-Authority

```mermaid
flowchart LR
  POS["Positive authority covered"] --> CHECK["CapGuard"]
  NEG["Counter-authority: missing DLP scan"] --> CHECK
  CHECK --> REVIEW["abstain / route to review"]
```

Caption:

> Positive field authority is insufficient when a counter-policy, missing receipt, conflict, or unresolved obligation applies.

## Figure 6: Boundary-Preserving Role Mismatch

```mermaid
flowchart TB
  S["Source: report-formatting skill"] --> B["Boundary checks"]
  B --> F["field: risk_report"]
  B --> O["operation: write"]
  B --> D["data_scope: supplied_report_inputs"]
  B --> E["effect_scope: documentation_only"]

  B --> BASE["boundary_scope_only: allow"]
  S --> ROLE["semantic role: report_formatting_skill"]
  NEED["Need: risk_assessment_authority"] --> CHECK["CapGuard role check"]
  ROLE --> CHECK
  CHECK --> BLOCK["block"]
```

Caption:

> Boundary scopes can be correct while semantic role is wrong; formatting authority is not risk-assessment authority.

## Figure 7: Derived-Artifact Authority Attenuation

```mermaid
flowchart LR
  A["Original approval record"] --> T["summarize"]
  T --> S["Derived summary"]
  S --> DOC["documentation role preserved"]
  S --> APPROVAL["approval-granting role not preserved"]

  DOC --> ALLOW["allow risk_report documentation"]
  APPROVAL --> BLOCK["block approval waiver"]
```

Caption:

> Derived artifacts may preserve narrow documentation or analysis roles without inheriting approval, publication, risk-gate, or delegation authority.
