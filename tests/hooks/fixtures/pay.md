---
spoke: PAY
question: ""
defaults: {schedule: S_central, horizon: short}
outputs: [O2, O2d, O3, O4a, O4b, O5, O6, O2b, O2c, DH1c, OL1]
---
**Short answer.** The taxpayer burden is {{o:O2.mean}} of wealth, and {{o:O2.range#wealth_band:D10}} in the top band, or {{o:O2d.mean}} with the settlement at death. Non-payers keep {{o:O4a.mean#income_decile:D1}} of the tax bill, and {{o:O3}} over a lifetime.

## Evidence

The threshold is set at {{i:I-D4b}} of adults. A `{{o:ZZ9}}` in a code span is left alone.

```
{{o:ZZ9}} in a fence is left alone
```

::: {#fig-PAY-1}
output: [O2, O2d, O3, O4a, O4b, O5, O6, O2b, O2c, DH1c, OL1]
kind: bar
caption: "Burden by band. Data: Table F-PAY-1."
:::

The burden is {{o:O2.mean#wealth_band:D4_5}} in the lowest taxed band, as {{ref:fig-PAY-1}} draws.
