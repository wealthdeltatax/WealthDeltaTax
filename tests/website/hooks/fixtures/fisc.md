---
spoke: FISC
question: ""
defaults: {schedule: S_central, horizon: short}
outputs: [O1, O1a, O1b, O1c, O1d, O1e, O1f, O2, O2d, O3, O5, O6, O7, OP1, OP4, O8, OB1, OR1, OF1, OT1]
---
**Short answer.** Net revenue is {{o:O1:M1.mean}} and {{o:O1a.range}}; the reserve fills in {{o:OP1.mean}}. At the long horizon it is {{o:O1:M1.mean/long}}.

## Evidence

::: {#fig-FISC-1}
output: [O1, O1a, O1b, O1c, O1d, O1e, O1f, O2, O2d, O3, O5, O6, O7, OP1, OP4, O8, OB1, OR1, OF1, OT1]
kind: line
caption: "Net revenue by schedule. Data: Table F-FISC-1."
:::

Revenue is {{o:O1:M1.mean@S_high}} in the high schedule, as {{ref:fig-FISC-1}} draws. The inflow is {{lit:ONS2025ETB:council-tax-top-decile-gbp}}.
