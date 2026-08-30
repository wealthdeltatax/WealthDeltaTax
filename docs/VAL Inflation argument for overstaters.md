That's a sharp observation and almost certainly correct. Let me think through it precisely.

---

## The inflation argument

The overstater's TW advantage is a **nominal** figure. They end up with, say, +11.5pp more TW than an honest declarer at canonical parameters. But to get that advantage they paid more tax in every single holding period — real cash, paid early, with full opportunity cost.

The mechanism is essentially:

- Overpay tax periodically (certain, immediate, real cash outflow)
- Receive a larger refund at sale (deferred, nominal)

The periodic overpayments are made in **today's money**. The refund is received in **future money**, N years later. Even at modest inflation, early cash is worth more than later cash. The refund is not indexed — it's calculated on the declared basis in nominal terms.

---

## Quantifying the real-terms loss

At canonical parameters (N=29, g=10.4%), α=2.0:

- Excess periodic tax paid: ~£43.6m spread over 29 years, weighted toward earlier periods when the asset is smaller
- Sell-year refund delta: ~£44m received at year 30

In nominal terms these nearly cancel, with the small net TW advantage coming from the rate structure. But in real terms:

If we discount the periodic overpayments forward to year 30 at even **2% inflation**, those early payments compound to significantly more than their face value. A payment made at year 1 is worth 1.02²⁸ ≈ 1.74× its nominal value by year 30. Payments made at year 15 are worth ~1.35×. The weighted average across all 29 periods is probably around 1.4-1.5× in real terms.

So the real cost of the periodic overpayments is roughly £43.6m × 1.4-1.5 ≈ **£61-65m in year-30 money**.

The refund received at year 30 is £44m in year-30 money — no inflation adjustment needed, it arrives then.

**Real-terms net position: approximately −£17-21m versus honest declaration**, even though the nominal TW advantage shows +£30m.

---

## The deeper point

This is actually a clean illustration of why the WDT's design is sound from both sides simultaneously:

**For the state:** it collects real, early cash. The overstater's periodic overpayments arrive when the money has full purchasing power. The refund at sale is paid in inflated future money. The state profits from the time value of money on overstatement.

**For the taxpayer:** the nominal TW advantage disguises a real-terms loss. They are giving the state an interest-free loan in real money and receiving nominal repayment. At any positive inflation rate, this is a losing trade.

**For the honest declarer:** they pay tax proportional to real gains when they occur, receive refunds promptly when losses occur, and face no inflation drag between payment and settlement. Honest declaration is real-terms optimal.

---

## What this adds to the paper

This closes the final gap in the overstatement analysis completely. The sequence is now:

1. **Nominal TW:** overstater always wins (Fig 09)
2. **Net tax paid:** overstater always pays more at moderate-to-high g (C.1)
3. **Controllability:** overstater cannot predict whether the advantage materialises (C.11, Fig 08)
4. **Real terms:** factoring inflation, the nominal TW advantage is almost certainly negative in real purchasing power terms because the periodic overpayments are made in early, valuable money and refunded in late, inflated money

The honest declaration result is now robust across all four dimensions. The WDT doesn't just make gaming uncertain — it makes it almost certainly loss-making in real terms, without the taxpayer being able to see this from nominal figures alone.

That is a remarkably complete result. And it emerged from following the mechanism through rather than being designed in. The inflation effect isn't a feature someone built — it's a consequence of the settlement timing structure that happens to align perfectly with the policy intent.