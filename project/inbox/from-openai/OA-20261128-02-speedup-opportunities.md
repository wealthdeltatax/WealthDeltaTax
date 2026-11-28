---
id: OA-20261128-02
type: performance-review
question: What additional optimisation opportunities and sequencing improvements are supported by the current speed-up evidence?
in-reply-to: none
supersedes: none
repo-commit: b71eacd5fbd6115adf3427cdf8f36438e1419e1c
sources: project/STATUS.md; project/briefs/open/152c-shared-year-loop-for-burden-and-ledger.md; project/briefs/open/153c-fewer-evaluations-per-o1e-root.md; project/briefs/open/187c-c1-limits-from-measured-noise.md; project/briefs/open/189c-fewer-array-passes-in-level-1.md; project/briefs/open/190c-rough-size-for-fast-refinement.md; project/agents/reference/code/speedup.md; results/speedup/profile-after-154c.md; results/speedup/kernel-spike.md; results/speedup/ledger.md; model/model_v3/core/burden.py; model/model_v3/core/revenue.py; model/model_v3/runner/runner.py
verified: read-only source review; no benchmark executed
confidence: medium-high
status: new
---

## Executive assessment

The current programme is pointed in the right direction. The next gains should come from (1) eliminating duplicated simulation work, (2) reducing repeated array operations in the household loop, and (3) making refinement runs smaller without confusing them with acceptance runs.

The strongest additional opportunity is to revisit 152c, the shared household year loop. The code and the compiled-kernel report both show that the burden and revenue/ledger paths independently walk the household year mechanics. This appears to duplicate a material part of the main workload, not just the small diagnostic workload. It should be quantified before being parked or dropped.

Do not start a broad rewrite in Rust, Julia or Numba based on the current evidence. The Numba spike achieved only 1.1–1.16x for two small functions, and a useful compiled implementation would require moving the complete household state transition and its hook into a different representation.

## What is already well targeted

### 1. 189c: fewer array passes

The profile identifies concrete targets:
- `builtins.sum`: 536,000 calls and 13.8 seconds own time in a 1,000-path evaluation (12% of profiled own time).
- `asarray`: about 1.03 million calls, mostly on small arrays.
- `where`: about 1.44 million calls.
- `burden.m2` and `burden._cash`: 5.7 and 5.1 seconds respectively at 1,000 paths.

189c has a sensible order, byte-identity requirement and stop rule. Keep it narrow. In particular, do not turn it into a general vectorisation or dtype/layout rewrite. The latter changes numerical behaviour and should be separately measured against an author-approved tolerance.

### 2. 153c: fewer O1e root evaluations

The root work is a good independent target. Preserve the sign-changing bracket and fall back to bisection whenever the accelerated method cannot establish a safe bracket. The new author-signed tolerance is a meaningful constraint, not permission to find a different root. Check the non-monotone death-phase cases explicitly.

### 3. 190c: a refinement size

This is important for the human development loop. A five-minute rough run could make model iteration much more productive even if it does not make the official run faster. It must remain visibly non-acceptance output and be rejected by the final validator, gate and acceptance script. Choose its path count from measured seed noise, not convenience.

### 4. 183c and 181c: split final run and baseline

Keep these as infrastructure work. The split final run should improve operational reliability and recoverability, but do not count sharding as an algorithmic speed-up unless the wall-clock comparison demonstrates it. The first full run should retain a reproducible baseline and machine/runtime record.

## Additional opportunity A: quantify and potentially share the household year loop

**Evidence in source**

- `burden.line_flows()` in `model/model_v3/core/burden.py` loops over death phases and years, calling `K.step_year(..., hook, t)`, and stores the burden-side flows and wealth.
- `revenue.run_lines()` in `model/model_v3/core/revenue.py` separately loops over the same phases and years and calls `K.step_year(..., hook, t)`, while collecting tax, death, payer and ledger outputs.
- Both paths use the household hook for the household arm.
- `results/speedup/kernel-spike.md` states that each `core_run` walks the year loop twice, once in burden and again in revenue.
- The 152c brief already proposes sharing one year loop, but its state is parked pending measurement.

**Why it matters**

This is duplicated simulation, not just duplicated post-processing. If both paths can consume one common year-transition result, the saving could apply to the large level-one evaluations as well as the smaller tornado/map/root evaluations.

The 179c report says level 1 is 75% of quick and array-bound. That does not make shared simulation irrelevant: eliminating a second pass over the same household state is a different lever from compiling the remaining array operations. The 152c brief should not be judged solely as a small-array call-overhead optimisation.

**Recommended investigation before implementation**

Instrument one representative 1,000-path household evaluation and separately time:
1. burden-side `line_flows`;
2. revenue-side `run_lines`;
3. the household year transition within each;
4. death, terminal settlement and ledger-only work;
5. burden-only and revenue-only aggregation.

Then build a small design table identifying which outputs can be emitted by a shared transition and which operations genuinely remain separate. Check whether the two hooks begin from identical state and whether their event ordering is identical at death and terminal settlement. The burden-side code currently performs terminal settlement and reconciliation in its own loop; this must not be silently conflated with the revenue ledger's settlement sequence.

**Recommendation:** revive 152c as a measurement/design investigation. Do not yet assume the implementation is safe or that the gain is 2x. If the shared loop is viable, it may be a higher-value level-one optimisation than further local substitutions.

## Additional opportunity B: distinguish repeated computation from repeated allocation

189c targets repeated `asarray`, `where` and `sum` calls. A useful follow-on, only if its profile shows a material residual, is to measure allocation and construction overhead separately from arithmetic.

Potential candidates visible in the source include:
- per-year `np.repeat` construction of the GDP index and growth arrays in the burden and revenue loops;
- repeated construction of masks, route dictionaries and temporary arrays;
- repeated group/band masks and weights in burden aggregation;
- repeated conversion of arrays already known to be float arrays.

Do not pre-emptively cache all of these. Some arrays depend on path, phase, year or mutable state. First establish whether each object is invariant over the relevant scope and whether its construction is at least 5% of the measured case, per the speed-up rules. Cache only at the narrowest safe scope (for example, once per evaluation rather than globally) and test that no mutable state is shared across worker jobs.

A useful profiling addition would be peak memory and allocation counts alongside wall time. This matters because the 1,000-path profile used substantial memory, and reducing temporary arrays may improve both runtime and the number of concurrent jobs that fit in memory.

## Additional opportunity C: benchmark the worker/chunk trade-off, not just worker count

The current level-one scheduler creates jobs by (path chunk, schedule), and the comment says there are three units per chunk at quick and 30 at final size. The existing timing shows that worker count helps, but the workload is not necessarily optimally balanced for every runner.

A bounded experiment could compare:
- current chunk size and worker count;
- smaller and larger chunks at fixed worker count;
- worker count capped by available memory as well as CPU;
- the slowest-unit time and total wall time, not only aggregate throughput.

This should be a measurement-only study unless it finds a material improvement. Avoid adding adaptive scheduling complexity unless the measured imbalance is meaningful. Preserve deterministic random path generation and merge order.

## Additional opportunity D: avoid recomputing shared inputs across diagnostic groups

The runner's `evaluate()` caches `core_run` results for repeated specs in its local `seen` dictionary, and `only` allows selected output groups. That is good. The next check is whether each output group independently reconstructs expensive but identical masks, weights, discount factors or transformations from the same raw arrays.

The profile already identifies `m2` and `_cash` as per-year loops of their own. 189c is the correct first pass. After it, profile group post-processing separately. A common immutable evaluation context for derived masks/weights could help, but only if multiple groups actually request the same calculation. Do not create a large caching framework for one or two arrays.

## Sequencing recommendation

1. Let 187c establish noise limits. This informs 190c and avoids choosing a refinement size blind.
2. Continue 189c as briefed; it is concrete, measurable and already assigned.
3. Run a focused 152c measurement/design review in parallel only if it does not conflict with the current code ownership. Otherwise queue it immediately after 189c. It should quantify the duplicated household simulation before a decision to drop it.
4. Continue 153c with its bracket-preserving fallback and cell-level reporting.
5. Complete 190c once 187c's noise data is available. Treat it as a development workflow improvement, not a model-performance claim.
6. Complete 183c and then 181c to establish a reliable full-run route and first full baseline.
7. Only after those measurements, decide whether memory/layout work, chunk tuning or a whole-loop compiled implementation deserves a separate brief.

## Things I would not pursue yet

- A general Rust or Julia rewrite: no evidence that language choice alone fixes the object/state-transition overhead.
- A broader Numba rewrite: the small spike did not clear its bar; a full-loop port is a different, expensive project.
- float32: it changes numerical results and memory behaviour; first establish whether memory bandwidth is the bottleneck and obtain a tolerance ruling.
- GPU: the current Python object graph, small per-year operations and stateful settlement logic are poor evidence for a GPU case. Reconsider only after the model is expressed as large, regular array kernels.
- More parallelism without a memory/throughput study: the current scheduler already parallelises chunk/schedule jobs, and additional workers may increase memory pressure rather than reduce wall time.

## Proposed follow-up brief

A short guru-owned brief could be titled **"Measure duplicated household simulation before deciding 152c"**. Deliverables:
- one 1,000-path profile separating burden and revenue year-loop time;
- a map of shared versus distinct state transitions and outputs;
- a byte-identity feasibility assessment for a shared loop;
- a conservative upper bound on expected level-one wall-time saving;
- a go/no-go recommendation for implementation.

This should not change model code or pins. The result should either release 152c with a better specification or close it with evidence.

## Limitations

This is a read-only source and results review. I did not execute the model, reproduce timings, inspect Actions logs, or test a shared-loop prototype. The reported timings are taken from the repository's existing measurements, not new experiments.
