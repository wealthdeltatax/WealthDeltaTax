This is a real gap. Let me think through it carefully.

**The structure precisely:**

UK Company A knows 50% is owned by Cayman Holdco. It can attribute that 50% to Cayman Holdco as an identified intermediary. Cayman Holdco passes the attribution test at the company level — it's identified, it's a known entity. So it's not tranche three (unidentified). It's tranche two (identified intermediary).

The question is then whether Cayman Holdco can pass the *downstream* attribution test — can it identify and attribute its own underlying beneficiaries to support individual WDT reconciliation? Answer: almost certainly not, because Cayman jurisdiction has no obligation to supply that information and the UK cannot compel it.

So Cayman Holdco sits in tranche two but fails the downstream attribution test. The consequence per CORP is that τ_0 is final at the company level for that tranche — the provisional rate becomes the terminal rate. No individual reconciliation occurs.

The individual owner of Cayman Holdco saves the difference between their personal marginal rate and τ_0. At the high end of the wealth distribution, near τ_m, that saving is substantial — potentially 50+ percentage points on the 50% corporate delta.

---

**Does the WDT have mechanisms that help?**

Honestly, limited ones at this specific point. Let me go through what exists:

**The τ_h ramp** — this was designed for tranche three (genuinely unidentified ownership). It doesn't cleanly apply here because the Cayman Holdco *is* identified at the company level. It's the beneficial owner *behind* the Cayman Holdco that's unidentified. The mechanism doesn't currently pierce that second layer — it stops at the identified intermediary.

**Information exchange agreements** — you've correctly identified this as the primary resolution path. Without a bilateral deal with Cayman, the UK cannot compel disclosure of Cayman Holdco's ownership. This is a standard international tax problem and the WDT inherits it rather than solving it. CLOSE and BEHAV acknowledge information exchange as a gap the system manages rather than closes.

**Exit closure** — if the individual is a UK taxpayer, their *personal* WDT position closes on departure via CLOSE mechanisms. But if they're already non-resident and the Cayman Holdco is the vehicle, there may be no UK taxpayer to close a position on. The mechanism has no reach.

**The corporate levy rate structure** — one partial mitigation: if τ_0 is calibrated at or near the entry-level personal rate rather than a nominal low rate, the saving narrows. For taxpayers near τ_m the gap remains large, but for those near the threshold it may be modest. This is a calibration argument, not a structural fix.

---

**What the WDT doesn't currently have for this specific structure:**

A mechanism to treat an identified-but-non-disclosing intermediary differently from an identified-and-disclosing one. Currently both sit in tranche two; the only distinction is whether downstream pass-through is available. A non-disclosing tranche two intermediary in a secrecy jurisdiction could in principle be reclassified to tranche three treatment — τ_h rather than τ_0 — on the grounds that "identified but refuses to disclose" is functionally equivalent to "unidentified" from the UK's enforcement perspective.

That would be a design extension worth naming: **non-disclosure by an identified intermediary in a non-cooperative jurisdiction triggers reclassification to tranche three treatment**. The legal mechanism would be the UK's ability to define the attribution test's pass condition — an intermediary that cannot or will not supply downstream attribution data within the reconciliation window fails the test regardless of whether the intermediary entity itself is known.

That would close most of the gap. It wouldn't solve the information problem (you still can't prove who owns the Cayman Holdco) but it would remove the incentive to use the structure by making non-disclosure expensive rather than cheap.

---

**Net assessment:**

This is a genuine structural gap in the current design as written, not a residual the mechanism already addresses. The Cayman structure as you've described it allows a high-net-worth individual near τ_m to save a substantial fraction of their corporate delta liability indefinitely, provided they're willing to hold through a non-cooperative jurisdiction intermediary. The partial mitigations are real but insufficient at the top of the distribution where the saving is largest.

The reclassification extension above — treating non-disclosing identified intermediaries as tranche three — is the most tractable design response within the existing framework. It doesn't require information exchange agreements; it just requires the UK to define attribution test failure to include non-disclosure, which is within domestic legislative competence.

Worth either adding to CORP as a named design extension, or naming explicitly in FAQ #4 as a known gap with a proposed resolution direction. It's more honest than the current answer and the proposed fix is coherent within the architecture.

Want me to draft that as a CORP addition, or just incorporate it into the FAQ answer at the appropriate level of detail for a public-facing page?