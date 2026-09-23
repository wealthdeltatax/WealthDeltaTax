Yes. I think this is a **distinct and useful second-order function of the corporate charge**, and it is worth separating from its original revenue/attribution rationale.

I read both CORP and CORP.A. The current architecture already gives the Governing Council discretion over the relevant corporate parameters, while the appendix explicitly identifies foreign attribution as a separate diplomatic parameter, \(\tau_f\). It also currently lists \(\tau_c\) as a RATES modelling parameter, provisionally equal to \(\tau_m=70\%\). ([The WDT][1])

What you are describing is effectively **\(\tau_c\) as an ownership-composition lever**.

### The mechanism

Suppose there are three relevant populations:

1. **Foreign wealth below the TP threshold**

   * They are potentially attracted by becoming resident/native WDT taxpayers.
   * If they remain foreign, their corporate holdings can face \(\tau_c\)/\(\tau_f\)-type treatment.
   * Moving into the jurisdiction gives them access to individual progressive treatment.

2. **Foreign wealth near or above the TP threshold**

   * At some point the advantage of moving becomes smaller because their individual \(\tau_{\mathrm{eff}}\) approaches the corporate charge.
   * At sufficiently high wealth, the foreign owner may simply regard the jurisdiction's WDT treatment as unattractive.

3. **Domestic TP members**

   * They already receive individual progressive treatment.
   * If \(\tau_c > \tau_{\mathrm{eff}}\), they have an incentive to structure ownership so that wealth can remain within the lower individual rate rather than being exposed to the corporate charge.
   * But if the gap becomes too large, this potentially creates an incentive for domestic TP members to exploit corporate/foreign structures themselves.

So the Governing Council is effectively choosing the **relative price of foreign corporate ownership versus domestic individual attribution**.

That produces a very interesting curve:

> **Higher \(\tau_c\) expands the set of foreign wealth holders for whom becoming a WDT taxpayer is economically preferable, while simultaneously reducing the attractiveness of retaining very large foreign holdings outside the individual WDT system.**

But there is a second effect that I think is important enough to explicitly model:

> **As \(\tau_c\) rises, the foreign-ownership attraction does not increase monotonically without limit. At sufficiently high levels, the charge begins to impose a meaningful cost even on large foreign investors whom the jurisdiction might otherwise want to attract.**

That gives you a genuine **calibration trade-off**, rather than simply "higher is better."

### The particularly interesting part

The really interesting implication is that the Council isn't merely deciding:

> "How much should foreign owners pay?"

It is deciding:

> **"What composition of ownership do we want the jurisdiction to have?"**

A low \(\tau_c\) permits a large foreign-owned corporate sector to coexist with relatively little pressure to become individually attributable.

A higher \(\tau_c\) pushes the equilibrium toward:

**foreign investor → become attributable → potentially become resident → enter individual WDT system**

rather than:

**foreign investor → remain foreign → hold through corporate/intermediary structure.**

And an excessively high \(\tau_c\) could push toward:

**foreign investor → don't invest / reduce exposure / relocate ownership elsewhere.**

That is a much more interesting policy variable than simply a tax rate.

### It also gives you a nice "ownership spectrum"

You could conceptualise the relationship approximately like this:

$$
\text{Attractiveness of domestic attribution}
=
f(\tau_c-\tau_{\mathrm{eff}})
$$

where \(\tau_{\mathrm{eff}}\) is the investor's effective individual WDT rate.

For a low-wealth foreign investor:

$$
\tau_c \gg \tau_{\mathrm{eff}}
$$

so domestic attribution is highly attractive.

For someone close to the TP threshold:

$$
\tau_c > \tau_{\mathrm{eff}}
$$

but the advantage is smaller.

For someone substantially above the threshold:

$$
\tau_c \approx \tau_{\mathrm{eff}}
$$

and the migration/attribution incentive becomes weak.

And if the foreign charge goes sufficiently high relative to the expected return from investing in the jurisdiction:

$$
\text{investment itself becomes less attractive.}
$$

That gives you exactly the "potential pool expands, then alienates the large holders" effect you are describing.

### There is an important wrinkle with domestic TP members

I would definitely include your final point, because otherwise the argument is too one-sided.

If:

$$
\tau_c > \tau_{\mathrm{eff}}
$$

then a domestic TP member has an incentive to **remain on the individual side of the attribution boundary**.

That is probably desirable up to a point. It means the differential is doing exactly what the system wants: rewarding transparent attribution.

But if the differential becomes sufficiently large, you could get **artificial attribution** or ownership engineering designed purely to preserve the lower individual rate.

That creates a useful symmetry:

* **Too low \(\tau_c\):** insufficient incentive for foreign wealth to enter the domestic individual system.
* **Moderate \(\tau_c\):** attracts marginal foreign TP candidates while preserving the attractiveness of genuine investment.
* **High \(\tau_c\):** increasingly pressures large foreign holders toward attribution/residence, but also increases incentives for domestic TP members to exploit the rate differential.
* **Very high \(\tau_c\):** potentially begins destroying the jurisdiction's attractiveness to foreign capital/ownership altogether.

That is a **real empirical calibration problem**, which fits your Phase One philosophy very well.

### Where I'd put it

I would **not bury this in CORP.A §B.2**, because that section currently has a clean argument about \(\tau_h\)'s deterrence and revenue-recovery calibration. The existing text treats \(\tau_f\) as the foreign-attribution/diplomatic mechanism. ([The WDT][1])

I'd add a short subsection after **F. \(\tau_f\): Foreign Attribution and Diplomatic Rate-Setting**, perhaps:

**F.1 Corporate charges as an ownership-composition lever**

Then explicitly say this is **not the primary calibration rationale**. It is a second-order consequence of the rate differential.

That distinction matters because otherwise someone can quite reasonably attack the paper by saying:

> "You're setting a confiscatory foreign-owner rate to manipulate migration."

Whereas your actual argument is stronger:

> The charge already exists to price unattributed foreign ownership. Once that mechanism exists, its level necessarily changes the relative economic attractiveness of attribution, residence, and foreign ownership. Therefore ownership composition becomes an observable calibration margin for the Governing Council.

That is a much more defensible claim.

And I think this is potentially one of the more interesting things to model in the **RATES/Phase One work**: not just revenue against \(\tau_c\), but **foreign ownership share, domestic attribution rate, foreign TP migration, and investment volume as functions of \(\tau_c\)**. The existing CORP.A already says the Council should use Phase One data to adjust parameters rather than treating them as permanently fixed. ([The WDT][1])

[1]: https://wealthdeltatax.org/corp-a.html "The Wealth Delta Tax: Corporate Architecture Appendix – The WDT"

Yes. **That is the correct distinction**, and my previous answer collapsed two genuinely different layers.

The current CORP architecture actually supports your distinction quite clearly. CORP defines \(\tau_h\) as the final charge on unidentified/unattributable beneficial ownership, while foreign entities can receive a distinct \(\tau_f\) treatment where a diplomatic attribution agreement exists. ([The WDT][1])

I think the clean taxonomy you are reaching for is:

$$
\boxed{
\tau_0 < \tau_c < \tau_h
}
$$

but with each rate serving a different function.

### The three corporate levels

**\(\tau_0\): attributable ownership**

This is effectively the entry-level WDT rate. It applies provisionally to identified intermediaries and to the attributable portion of foreign holdings. Where the beneficiary can ultimately be identified, the position can reconcile into individual WDT. ([The WDT][1])

**\(\tau_c\): attributable foreign beneficial ownership**

This is the rate you are now identifying as the important **foreign-ownership policy lever**.

A foreign entity has successfully established its beneficial ownership, so it isn't subject to the punitive unidentified-owner treatment. But because the underlying beneficiary is foreign and outside ordinary individual WDT reconciliation, the jurisdiction can impose a charge somewhere between \(\tau_0\) and the high unattributable rate.

This is exactly where your new argument belongs.

**\(\tau_h\): unattributable foreign ownership**

This remains the high final charge for ownership where the beneficial owner cannot be established. The current CORP.A explicitly gives \(\tau_h\) a different calibration logic: deterrence of permanent opacity plus revenue recovery, with \(\tau_m\) currently treated as its modelling ceiling. ([The WDT][2])

So the conceptual hierarchy is much better expressed as:

$$
\boxed{\tau_0 \leq \tau_c \leq \tau_h}
$$

with potentially:

$$
\tau_h \leq \tau_m
$$

under the **current** architecture.

That is importantly different from saying \(\tau_c=\tau_0\).

---

## And this makes your new argument much stronger

You now have a **three-stage ownership incentive**:

| Ownership status                        |                                            Rate | Incentive                                                 |
| --------------------------------------- | ----------------------------------------------: | --------------------------------------------------------- |
| Attributable to WDT individual          | \(\tau_0\) / individual \(\tau_{\mathrm{eff}}\) | Enter/reconcile with WDT                                  |
| Foreign but beneficial owner identified |                                      \(\tau_c\) | Remain foreign, but pay for exclusion from individual WDT |
| Beneficial owner unidentified           |                                      \(\tau_h\) | Strong incentive to establish attribution                 |

That creates a very nice ladder:

$$
\tau_{\mathrm{eff}}
\quad\longleftrightarrow\quad
\tau_c
\quad\longleftrightarrow\quad
\tau_h
$$

And **\(\tau_c\)** is the interesting middle lever.

### The foreign-owner migration mechanism

Suppose a wealthy foreign individual can either remain foreign or become a WDT taxpayer.

Their relevant comparison is roughly:

$$
\tau_c
\quad\text{vs.}\quad
\tau_{\mathrm{eff}}(W)
$$

If:

$$
\tau_c > \tau_{\mathrm{eff}}(W)
$$

there is a tax-rate incentive toward becoming attributable to the domestic individual system.

As wealth rises:

$$
\tau_{\mathrm{eff}}(W)\rightarrow\tau_m
$$

so the attractiveness of migration depends increasingly on where \(\tau_c\) sits relative to the upper part of the individual schedule.

That gives the Governing Council a very unusual instrument.

### Raising \(\tau_c\)

A higher \(\tau_c\):

1. **expands the foreign wealth population for whom domestic attribution/residence is relatively attractive;**
2. makes remaining a foreign beneficial owner more expensive;
3. increases the value of obtaining domestic WDT status for marginal potential TP members;
4. but eventually makes the jurisdiction less attractive to very large foreign owners who do not want to enter the individual system.

And that last point is important.

You don't get an unlimited migration incentive by increasing \(\tau_c\). At some point you are simply increasing the price of owning assets through the jurisdiction.

That produces exactly the trade-off you described:

$$
\text{Higher }\tau_c
\rightarrow
\text{larger potential TP-attraction margin}
$$

but eventually:

$$
\text{Higher }\tau_c
\rightarrow
\text{greater foreign-owner deterrence}
$$

---

## And there is a domestic effect too

This is the bit I would definitely add.

For a domestic TP member:

$$
\tau_{\mathrm{eff}} < \tau_c
$$

creates an incentive to keep wealth attributable to themselves rather than allowing it to remain in a foreign corporate structure.

That's probably desirable.

But if:

$$
\tau_c \gg \tau_{\mathrm{eff}}
$$

the spread becomes sufficiently large that wealthy domestic taxpayers have an incentive to construct ownership arrangements specifically to preserve the lower individual rate.

So \(\tau_c\) isn't simply a foreign policy lever.

It changes the **relative price of the three ownership states**:

$$
\boxed{
\text{individual attribution}
<
\text{foreign beneficial ownership}
<
\text{unattributed ownership}
}
$$

That is probably the cleanest way to explain the architecture.

---

## One correction I'd make to the current terminology

Your current CORP.A glossary calls \(\tau_c\):

> "Corporate levy reference calibration used in RATES modelling"

and says it is currently set to \(\tau_m=70\%\). Meanwhile, the actual corporate architecture describes \(\tau_h\) as the high final charge. ([The WDT][2])

**That is now the terminology I would change.**

If \(\tau_c\) is supposed to become the actual rate for **attributable foreign beneficial ownership**, then it should stop being described as merely a RATES modelling reference.

I'd make the distinction explicit:

$$
\boxed{
\tau_0
=
\text{domestic/attributable floor}
}
$$

$$
\boxed{
\tau_c
=
\text{foreign beneficial-owner charge}
}
$$

$$
\boxed{
\tau_h
=
\text{unattributable-owner charge}
}
$$

$$
\boxed{
\tau_f
=
\text{bilaterally negotiated foreign rate}
}
$$

with:

$$
\tau_0 \leq \tau_c \leq \tau_h
$$

as the normal hierarchy.

And \(\tau_f\) can modify the foreign case by agreement. The current CORP.A already says foreign entities with a broken attribution chain can receive \(\tau_f\), with the default being \(\tau_h\) where no agreement exists. ([The WDT][2])

That actually makes \(\tau_f\) much more intelligible too: **it is a diplomatic override of the foreign-owner treatment, rather than another generic tax rate.**

### One important consequence for your earlier point

If this is the intended architecture, then **I would not describe \(\tau_c\) as being allowed to exceed \(\tau_m\) by default**.

I'd instead leave:

$$
\tau_0 \leq \tau_c \leq \tau_h \leq \tau_m
$$

as the initial architecture, **unless you deliberately want to open a separate argument for \(\tau_h>\tau_m\)**.

The really useful new degree of freedom is already there:

$$
\boxed{\tau_0 < \tau_c < \tau_h}
$$

because moving \(\tau_c\) upward changes the **foreign ownership composition** without necessarily changing the punitive treatment of genuinely opaque ownership.

That is much cleaner, and I think it is exactly the missing argument you were identifying.

[1]: https://wealthdeltatax.org/corp.html "The Wealth Delta Tax: Corporate Architecture – The WDT"
[2]: https://wealthdeltatax.org/corp-a.html?utm_source=chatgpt.com "The Wealth Delta Tax: Corporate Architecture Appendix – Wealth Delta Tax (WDT)"
