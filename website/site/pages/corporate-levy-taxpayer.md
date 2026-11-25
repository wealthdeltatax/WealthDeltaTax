---
title: "Your Corporate Tax Credits"
description: >
  How the corporate delta levy collects tax on your listed equity before
  you file anything — and how to make sure the credit reaches you.
toc: true
---

## The levy does the work. Your job is to claim it.

If you hold listed shares — directly, through a broker, through an ISA wrapper, through
any vehicle that can be attributed back to you — a portion of your annual WDT liability
is being collected before you file a single return. The company whose shares you hold
calculates how much its market capitalisation rose last year, pays a provisional amount
into a ring-fenced settlement account, and issues a statement to your broker showing your
share of that figure.

That statement is a credit. When you settle your individual WDT — annually, or
on a multi-year rolling basis — the credit is applied against what you owe. If the company
provisioned at the same rate you pay, you write no cheque for the equity portion. If it
provisioned at a lower rate, you top up the difference. If it provisioned more than your
marginal rate, you receive the excess back.

This page explains how that mechanism works, what your broker's role is, what you need
to do each year to protect the credit, and what happens if you do nothing.

---

## How the corporate delta levy is calculated

A listed company measures its market capitalisation on a fixed annual assessment date —
the change from the prior year's figure is the **corporate delta**.

The company then pays a **provisional levy** into a settlement account:

$$
\text{Provisional levy} = \tau_{\text{prov}} \times \Delta \text{MarketCap}
$$

where $\tau_{\text{prov}}$ is a rate the company sets itself, subject to a floor of $\tau_0$
(the WDT entry-level rate, currently 15%). The company is the one taking the risk of its
own rate choice. If it provisions too low, it pays any shortfall itself at window close.
If it provisions high, it gets the excess back when credits are claimed.

Within sixty days of the assessment date, the company issues **delta statements** to every
registered holder showing their proportional share of the corporate delta. This figure
flows into your WDT annual report automatically if your broker is set up for WDT
reporting — most are.

---

## Who gets the credit and who doesn't

The mechanism divides shareholders into three tranches. Which one you land in determines
what happens to the levy paid on your behalf.

**Tranche one — native WDT shareholders.** If you are a UK resident individual within
scope of individual WDT assessment, you are in tranche one. The provisional levy
provisioned against your share of the delta is held in the settlement account as your
credit. When you file your individual WDT return and confirm your settlement, the credit
is released against your liability. If the company provisioned at a lower rate than your
marginal WDT rate, you pay the difference through individual settlement. If it provisioned
at a higher rate, you receive the excess.

**Tranche two — identified intermediaries.** This is where your broker sits. If your
shares are held through a nominee, the broker — not you — appears on the company's
register. The company pays $\tau_0$ on the broker's registered tranche. Whether that
becomes a credit flowing to you depends on whether your broker can pass the attribution
test: can it identify you as the underlying beneficial owner and attribute your share of
the delta? If yes, the broker submits a reconciliation return and your credit flows through
normally. If no, $\tau_0$ is a final charge at the company level and you receive nothing
back.

**Tranche three — unidentified beneficial ownership.** Positions that cannot be attributed
to any identified human at any level of the chain bear $\tau_h$ — a higher final charge
set above $\tau_0$, with no downstream recovery. There is no individual credit to claim
because there is no individual to claim it.

The operative question for tranche two is simple: does a continuous chain exist from the
registered holder to you? For most retail brokerage accounts in a standard KYC framework,
the answer is yes. Your broker knows who you are. It can attribute the delta. The credit
reaches you.

---

## What your broker does on your behalf

Your broker receives a consolidated delta statement covering all the listed companies you
hold. It allocates each company's delta to your account proportionally, confirms your
above-threshold WDT status, and submits a reconciliation return to HMRC showing three
populations within its book:

- **Below-threshold registered clients.** The broker claims back the $\tau_0$ already
  paid at the company level on their shares. No WDT is owed; the provisional payment was
  a temporary collection pending that confirmation.

- **Above-threshold native WDT shareholders (you).** Your settlement through individual
  WDT triggers credit release. The broker's reconciliation return maps your corporate
  allocation to the relevant companies so the credit can be matched correctly.

- **Unattributable positions within the book.** Any shares the broker cannot trace to a
  named beneficial owner bear $\tau_h$ at the intermediary level. This is the broker's
  cost, not yours — which is why brokers have a direct financial incentive to maintain
  complete KYC.

The practical consequence: if your broker has your WDT registration on file and you hold
straightforward listed equity, your corporate credits appear as a pre-populated line item
in your annual WDT report. You confirm and claim. You do not calculate them yourself.

---

## The credit timeline: one deadline the rolling window doesn't move

Here is where most misunderstandings occur.

The WDT permits rolling multi-year assessment windows. You can elect to settle your total
accumulated liability every two, three, five years or longer. Nothing about that window
changes when your corporate credits expire.

**Each year's corporate credit must be claimed within twelve months of that year's
assessment date.**

The rolling window governs when you pay your total accumulated WDT. It does not extend
the deadline for registering individual credits. A taxpayer on a three-year window who
waits until year three to register all three years of credits will find that years one
and two have lapsed.

A lapsed credit is not forgiven liability. You still owe WDT on the full delta including
the corporate allocation — you have simply lost the offset for the portion that was
pre-collected on your behalf. The provisional amount provisioned against your lapsed
credit has returned to the company at the one-year window close. You pay twice for the
same liability.

**The practical rule:** file your annual WDT report every year, regardless of when your
rolling settlement falls due. The annual report is what triggers credit registration.
It takes the pre-populated broker data, confirms your allocation, and banks the credit
against your running balance.

---

## A worked example: equity portfolio at the 95th percentile

Take a taxpayer at the 95th wealth percentile — starting wealth £2.858m, half in listed
equities held through a broker (Route A), half in property (Route D). Growth at the
canonical "Good" tier rate of 11.4% per year. Three-year rolling assessment window.

At canonical parameters, the WDT rate at this wealth level sits on the near-flat entry
limb of the logistic curve at approximately $\tau_0 = 15\%$.

**Year 1.** Equity portfolio: £1.429m. Growth: 11.4%. Delta: £163k. Provisional levy
(companies, provisioning at $\tau_0 = 15\%$): £24.4k paid into settlement accounts.
Delta statements issued to broker. Broker reconciliation return filed. Credit earmarked
against taxpayer's individual WDT: £24.4k. Annual WDT report filed. Credit registered.
Twelve-month clock starts.

**Year 2.** Portfolio now £1.592m. Delta: £181k. Provisional levy: £27.2k. Same chain.
Year 2 credit registered: £27.2k. Approximately two months remain on the Year 1 credit
window — this is the moment to confirm Year 1 credit is fully registered before it lapses.

**Year 3 — settlement.** Portfolio £1.773m. Delta: £202k. Provisional levy: £30.3k.
Year 3 credit registered: £30.3k.

Three-year settlement triggered. Total equity delta: £546k. Total Route D (property)
delta: approximately £545k at matching growth. Combined three-year delta: ~£1.09m.
Gross WDT liability at ~15%: ~£164k.

Corporate credits applied: £24.4k + £27.2k + £30.3k = **£81.9k**.

Net out-of-pocket payment: **~£82k** — covering the Route D slice only. The equity-side
liability was pre-collected through the levy. Average annual cash outflow: ~£27k on
~£3m of wealth, equivalent to the RATES-canonical annual wealth burden of approximately
0.35% of net worth.

The taxpayer wrote no cheque for the equity portion. The mechanism collected it before
they filed anything.

---

## What happens to corporate credits in a loss year

If a company's market capitalisation falls, the corporate instrument is silent. No levy.
No refund. The company pays nothing into the settlement account.

Loss-year refund protection runs through individual WDT assessment, not through the
corporate mechanism. If your total net worth delta is negative — including the equity
component — you receive a refund proportional to your declared basis and marginal rate
through your personal return.

This is not a gap in the mechanism. Corporations do not experience losses in any humanly
meaningful sense. Your shares fell in value; *you* experienced a loss. The mechanism
recognises that through your individual assessment, not through the company. You still
need to have been reporting and registering credits in gain years for the lifetime
contribution envelope to have accumulated enough to support a meaningful refund.

A taxpayer who has been filing annual reports, banking credits, and building contribution
history arrives in a bad year with full refund entitlement proportional to accumulated
payments. A taxpayer who has not filed — or whose credits have lapsed — has a smaller
envelope and correspondingly less protection.

---

## Derivatives and synthetic exposure: what the levy doesn't reach

The corporate delta mechanism taxes beneficial ownership of shares. It does not reach
derivative or synthetic exposure to the same underlying company.

If you hold a call option on a stock, or a total return swap referencing its price, your
gain or loss from that position runs against your derivative counterparty, not against
the company. The company is the reference point for the contract, not a party to it.
There is no double-counting risk: your derivative position does not appear in the
company's reconciliation ledger, and the company's corporate levy does not appear in
your derivative settlement. The two instruments tax different legal claims arising from
the same price movement.

Your gain on the derivative enters your individual WDT assessment through your net worth
calculation in the ordinary way.

---

## The case for full attribution

Everything in this page assumes a straightforward fact: your broker can identify you.
That single condition is what separates tranche-one treatment — corporate credit released
against confirmed individual settlement at your own marginal rate — from tranche-three
treatment: $\tau_h$ as a final charge, no credit, no refund access on the relevant
tranche.

Under any tax system that existed before the WDT, opacity through intermediaries could
reduce tax liability. Nominee structures, offshore vehicles, and multi-layer holdings
created attribution gaps that the system depended on closing — gaps that required
enforcement effort to bridge and often weren't closed at all. Complexity was profitable.

Under the WDT, that relationship is reversed. The levy is collected at source regardless
of attribution. Attribution determines who receives the credit, not whether the state
collects. An opaque position doesn't escape the levy; it receives $\tau_h$ instead of
$\tau_0$, loses access to the refund mechanism in loss years, and forfeits the
progressive credit that individual settlement would have generated.

The mechanism requires no enforcement action to produce this outcome. It follows
mechanically from the attribution structure. A beneficial owner who has kept their
ownership opaque has cost themselves both the credit and the refund protection, while
paying a higher charge than a transparently attributed equivalent position. The optimal
strategy and the cooperative strategy are the same document.

---

## Summary: what you need to do

**Every year, regardless of your rolling settlement window:**
file your annual WDT report confirming your corporate allocations. This banks the credit.
The credit expires in twelve months. The rolling window does not extend it.

**Ensure your broker holds your WDT registration.** This is the condition for attribution
to flow. Without it, your broker cannot pass the reconciliation chain through to you.

**Hold nothing in structures that break the attribution chain.** Nominee arrangements
that your broker cannot look through seat you in the unattributed tranche. The cost is
$\tau_h$ rather than $\tau_0$, no loss-year refunds on that tranche, and no credit. The
mechanism has already collected the levy. You have just removed your ability to benefit
from it.

**In a loss year, file your individual WDT return as normal.** The company does nothing.
Your refund protection runs through personal assessment. You need contribution history in
the lifetime envelope for the refund to fire. Building that history means filing annually,
which is the same instruction as the first point.

The corporate levy is doing the heavy lifting. Your role is to show up and claim it.

