# Computational architecture hypothesis: three routes to a faster WDT model

**Status:** hypothesis for investigation; no implementation choice authorised  
**Date:** 2026-11-23  
**Owner:** guru  
**Context:** model v3, especially the household arm and the two-level stochastic runner

## Question

Can the WDT model be made materially faster and easier to extend without compromising its accounting identities, numerical behaviour, reproducibility or research auditability? If so, which implementation route gives the best return for the least disruption?

## Current position

The active model is model v3, not the legacy v1 implementation. It is currently a Python/NumPy system with a deliberately separated computational kernel, household accounting functions, runner, scenario inputs and output layer.

The runner uses 10,000 Level 1 paths, 200 Level 2 parameter draws and 1,000 paths per Level 2 draw, processed in chunks. The kernel folds payer lines and paths into vectorised arrays. The household arm adds stateful annual household accounting and settlement.

The 23 November status board records an early cost measurement: one household evaluation took about 4.9 seconds at 20 paths; a complete run was estimated at hours to days. Brief 150c is already investigating run cost and parallel evaluation. Its measured results must be treated as the baseline when available. These early figures are a warning, not yet a complete profile or proof that a language rewrite is warranted.

The current code has useful boundaries:
- `model_v3/core/kernel.py` owns route settlement mechanics and is vectorised over a line axis.
- `model_v3/core/household.py` contains a pure household-step function.
- `model_v3/runner/arm.py` wires household state into the kernel and is already at its 330-line budget.
- `model_v3/runner/runner.py` owns orchestration, sampling, path generation and output collection.

The distinction matters: the best implementation may be a faster computational core with the Python research pipeline left intact.

## Central hypothesis

The dominant run cost is likely to arise from repeated per-year household and settlement work across payer lines and paths, together with Python-level orchestration and/or array allocation overhead. A targeted improvement to the hot path may deliver most of the available speed-up without a wholesale rewrite.

This is not yet established. The first task is to measure the actual runtime distribution, including allocation and memory costs, before choosing an implementation.

Three implementation scenarios are proposed. They are alternatives to compare, not sequential commitments.

---

## Scenario A — Minimal intrusion: optimise the existing Python/NumPy model

**Objective:** obtain useful speed-ups while changing as little architecture, code and tooling as possible.

### Proposed approach

1. Use the 150c baseline and add function-level profiling to a representative run.
2. Identify repeated calculations, avoidable array copies, temporary arrays, redundant dictionary construction and repeated invariant work.
3. Improve chunk sizing and memory reuse where measurements justify it.
4. Evaluate a narrowly scoped JIT compiler such as Numba only for functions shown to be Python-loop bound. Keep the public interfaces and surrounding runner in Python.
5. Evaluate path-level or draw-level parallelism only after checking memory bandwidth, deterministic seeding and the cost of process/thread coordination. Avoid nested parallelism.
6. Preserve NumPy as the reference implementation and keep any accelerated path optional until validated.

Potential targets include the household annual transition and selected loops in the runner. The NumPy-vectorised kernel should not be rewritten merely because it is central: first establish whether it is actually a bottleneck.

### Advantages

- Lowest migration and maintenance cost.
- Retains the current Python research ecosystem and familiar debugging workflow.
- Small, reviewable diffs; easy to compare old and new implementations.
- Numba can compile selected numerical functions without redesigning the whole model.

### Risks and limitations

- Numba has restrictions around Python objects, dictionaries and dynamic control flow. Some code may need a numerical-array interface before it can compile efficiently.
- Speed-ups may be limited if the bottleneck is already NumPy, memory bandwidth, or repeated work at a higher level.
- A JIT dependency introduces compilation behaviour and another supported execution path.

### Success condition

A material end-to-end reduction in wall-clock time on the official workload, with no material increase in memory use or operational complexity, and exact or explicitly tolerance-bounded agreement with the reference implementation.

**Working judgement:** preferred first route. It has the best expected ratio of benefit to disruption, and it produces the profiling evidence needed to assess the other routes.

---

## Scenario B — Performance-first: Rust computational engine, Python research shell

**Objective:** move the computationally intensive model core into a compiled, parallel, strongly typed implementation while retaining Python for research orchestration and analysis.

### Proposed approach

1. Keep Python responsible for input loading, register and pack handling, scenario construction, sampling, output schemas, diagnostics and plotting.
2. Define a narrow, stable boundary between Python and the computational engine. Pass contiguous numeric arrays and explicit configuration structures rather than Python dictionaries or arbitrary objects.
3. Prototype the most expensive measured function or loop in Rust. Candidate areas are the household annual transition, the repeated path/line settlement loop, or a combined kernel if profiling shows that boundary crossings would otherwise dominate.
4. Expose the Rust implementation to Python through PyO3/maturin or an equivalent maintained binding.
5. Parallelise independent paths or parameter draws in Rust, with deterministic random inputs generated or assigned at a clearly defined boundary.
6. Keep the Python implementation as the reference oracle until the Rust implementation has passed equivalence tests and representative full-run comparisons.

Do not assume that porting `household_step` alone will help: it is currently a pure NumPy-oriented function, and conversion overhead could erase the gain. The prototype must measure the complete call boundary, not just the Rust function in isolation.

### Advantages

- High potential throughput for repeated scalar/state-transition work.
- Strong control over memory layout, allocations and parallel execution.
- Type system can make accounting states and route-specific rules more explicit.
- Python remains available for the parts of the project where it is strongest.

### Risks and limitations

- Highest engineering cost of the three scenarios.
- Two implementations of important mechanics create a continuing parity burden.
- Binding and data-conversion overhead can undermine small-grained calls.
- Rust's type safety does not establish the correctness of the economic model; it only helps enforce the rules encoded in the implementation.
- Parallel execution must not change random-number assignment, path comparability or reduction behaviour silently.

### Success condition

A substantial, repeatable end-to-end speed-up on the official workload, including data transfer and orchestration overhead, with bounded memory use, deterministic replay and full parity against the Python reference on the validation suite.

**Working judgement:** strongest candidate if Scenario A shows that the workload is genuinely compute-bound and the expected long-run scale justifies the extra engineering burden.

---

## Scenario C — More exotic: Julia-native scientific model

**Objective:** investigate whether the model would be better expressed as a single high-performance scientific-computing system rather than a Python orchestration layer plus a compiled extension.

### Proposed approach

1. Build a small Julia proof of concept for one complete, representative model path, including household state transitions and settlement.
2. Use Julia's native numerical arrays, multiple dispatch and compilation model to express the computational model directly.
3. Compare ordinary CPU execution and Julia's supported parallel/distributed options before considering accelerators.
4. Keep data interchange with the existing Python research pipeline simple and explicit, for example through stable CSV/Arrow/Parquet outputs or a narrow Python-Julia interface.
5. Do not port the whole model unless the proof of concept demonstrates a meaningful advantage in both performance and model clarity.

This scenario is deliberately more than a language swap. It tests whether a coherent scientific-computing environment would make future model development easier, especially if the WDT grows into more detailed household-level or agent-based simulations.

### Advantages

- Designed for numerical and scientific computing, with high-performance native execution.
- One language could own more of the computational model, avoiding a growing collection of Python/Rust boundaries.
- Expressive tools for numerical methods, simulation and statistical analysis.
- Potentially attractive if the model becomes more exploratory and mathematically complex.

### Risks and limitations

- A larger rewrite and a new language ecosystem for contributors and agents.
- Less direct reuse of the existing Python code, tests and tooling.
- Interoperability and reproducible environments become additional maintenance concerns.
- Julia's performance advantage is not automatic; compilation latency, allocations and code design still matter.
- A successful microbenchmark would not justify migration unless a representative end-to-end model path also improves.

### Success condition

A Julia prototype that is materially faster or substantially clearer to extend than the Python baseline, on a representative end-to-end workload, without creating an unacceptable second research-tooling ecosystem.

**Working judgement:** strategically interesting but not the default recommendation. Treat it as a bounded feasibility experiment, not a migration plan.

---

## Comparison

| Criterion | A: Python/NumPy + selective JIT | B: Python + Rust core | C: Julia-native model |
|---|---|---|---|
| Intrusion | Low | Medium to high | Very high |
| Potential speed | Moderate to high, workload-dependent | High | High |
| Reuse of current code | Very high | High outside the core | Low to medium |
| Parallelism | Existing Python/NumPy options; selective JIT | Fine-grained native parallelism | Native parallel/distributed options |
| Ongoing parity burden | Low | Medium to high | High during migration |
| Contributor/tooling disruption | Low | Medium | High |
| Best reason to choose | Fastest low-risk improvement | Sustained compute-bound workload | A genuine need for a new scientific-computing architecture |

## Common requirements for all three scenarios

No scenario is acceptable unless it preserves the model's substantive behaviour.

1. **Reference implementation:** retain a trusted Python path for comparison until the alternative is proven.
2. **Deterministic inputs:** compare implementations on identical pre-generated random innovations and parameter draws. Do not let each implementation generate unrelated random samples and call the results equivalent.
3. **Accounting identities:** test household account closure, route settlement, tax/refund conservation, pension and lien balances, death/horizon reconciliation, and the existing model invariants.
4. **Numerical tolerances:** define tolerances before comparing results. Distinguish floating-point summation-order differences from genuine behavioural differences. No tolerance may conceal a systematic bias.
5. **Statistical equivalence:** compare path-level outputs where possible, plus distributions and headline metrics across representative runs. Matching only the final mean is insufficient.
6. **Reproducibility:** record code version, inputs, parameters, seeds/random innovations, runtime environment and output hashes.
7. **Memory:** record peak resident memory and allocation behaviour as well as wall-clock time.
8. **End-to-end timing:** include setup, data conversion, execution, aggregation and output writing. Do not report kernel-only speed as the project's speed-up.
9. **No silent model changes:** performance work must not alter assumptions, scenario definitions, path construction, output meanings or the manifest. Any proposed model change is a separate decision.

## Proposed investigation and decision gate

### Stage 1 — Establish the baseline

Use brief 150c's results as the starting point. If it does not provide them, measure:

- wall-clock time by major phase and function;
- household arm versus legacy arm;
- cost by number of paths, payer lines and years;
- chunk-size sensitivity;
- peak memory and allocation volume;
- serial versus parallel scaling;
- repeatability across identical seeds.

Use a representative official workload, not only a tiny smoke run. Keep a small benchmark for iteration and a larger benchmark for decision-making.

### Stage 2 — Test Scenario A first

Apply low-risk improvements and, only where indicated by profiling, prototype selective Numba compilation. Record each change separately so the source of any gain is clear.

### Stage 3 — Compare a bounded Scenario B prototype

If the measured hot path remains a material bottleneck, port one representative unit of work to Rust. Benchmark through the Python interface and compare against the optimised Python baseline, not against an intentionally unoptimised version.

### Stage 4 — Decide whether Scenario C merits a proof of concept

Only investigate Julia if the first two routes reveal a structural limitation or if the expected future model makes a unified scientific-computing environment valuable independently of speed.

### Decision rule

Choose the least intrusive scenario that meets the project's measured runtime and memory needs with adequate headroom for the next planned model stages.

Do not select a language based on theoretical benchmark rankings. The WDT's actual workload, state structure, data movement and validation burden determine the answer.

## Falsification

The central hypothesis is weakened or falsified if profiling shows that the apparent runtime problem is mainly caused by an avoidable runner configuration, excessive workload size, repeated input preparation, output writing, or another issue that can be fixed without changing the computational implementation.

The Rust case is weakened if a representative end-to-end prototype produces little improvement after conversion and orchestration costs. The Julia case is weakened if it offers no meaningful advantage over the optimised Python/Rust alternatives in a representative model path.

A rewrite is not itself a success criterion.

## Recommendation

Proceed with Scenario A as the default investigation, using 150c's measurements as the baseline. Keep Scenario B as the performance ceiling to test if the profile justifies it. Retain Scenario C as an explicitly optional architectural experiment.

No wholesale rewrite is authorised by this hypothesis. The next deliverable should be evidence: a reproducible benchmark, a measured bottleneck map and, if justified, one bounded prototype.
