#!/usr/bin/env python3
"""c1_noise.py -- measure the seed noise of the level 1 outputs and derive the C1 limits (brief 187c). Method fixed in the brief before any number was seen.

    python model/tools/c1_noise.py run [--out DIR] [--workers N] [--n 10000] [--seeds 10]    measure (resumable), then analyse
    python model/tools/c1_noise.py analyse [--out DIR] [--write-limits FILE] [--ceiling X]     analyse the saved paths only

`run`: `level1` on the legacy arm, S_central (the test's own setup), for 10 seeds (the five C1 seeds and five more) at n = N1 paths; the per-path arrays of O1, O2 (overall), O3 and O4a (overall) are saved per seed
(DIR/paths/seed-<seed>.npz) before anything is summarised. `analyse`: from the first n/8, n/4, n/2 and n paths of each seed (paths are independent, so the first k paths are a run of k paths), and from pairs of disjoint seeds
pooled (2n paths, five pairs), the mean, P10 and P90; the standard deviation across seeds sd(N); the Monte Carlo law (sd(N) * sqrt(N) constant within 20%); the limit rule limit = q * sd(N1), q the 99th percentile
of the range of 5 draws in units of sd (simulated here, 10^6 draws, fixed seed); the limit against the output's own spread and mean; and the N that brings O3's limit to 0.15. Writes DIR/c1-noise.csv and DIR/c1-noise.md;
`--write-limits` also writes the limits file the C1 test reads. `--ceiling` caps each limit (default: none)."""
from __future__ import annotations

import argparse, csv, json, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'model'))
from model_v3 import numerics  # noqa: F401,E402  (before any numpy import)
import numpy as np  # noqa: E402

OUTS, STATS = ('O1', 'O2', 'O3', 'O4a'), ('mean', 'p10', 'p90')
SEEDS = (20261118, 20261119, 20261120, 20261121, 20261122, 20261123, 20261124, 20261125, 20261126, 20261127)   # the five C1 seeds (run.SEED first), then five more
FLOOR = 1e-9   # author, 2026-11-28: a limit is never below the 171c zero tolerance (O4a P10 and P90 are constant, sd 0)
RATE, LAW, TARGET = 0.01, 0.20, 0.15                                       # false-failure rate, the law's tolerance, O3's limit to reach


def summary(v):
    return np.array([np.nanmean(v), *np.nanpercentile(v, (10, 90))])


def q_factor(rate=RATE, draws=1_000_000, k=5):
    """The (1 - rate) percentile of the range of k standard normal draws, in units of sd (simulated, fixed seed)."""
    x = np.random.default_rng(20261127).standard_normal((draws, k))
    return float(np.quantile(x.max(1) - x.min(1), 1 - rate))


def analyse(paths, seeds, n, c1_seeds=5, rate=RATE, ceiling=None):
    """paths: {seed: {output: (n,) array}}. Returns (rows, limits, extra): rows one per output, statistic, N (see the csv); limits {output: {stat: limit}}; extra the per-output detail the report prints."""
    sizes = [n // 8, n // 4, n // 2, n]
    rows, sd1, q = [], {}, q_factor(rate)
    for o in OUTS:
        for N in sizes + [2 * n]:
            if N == 2 * n:
                a = np.array([summary(np.concatenate([paths[seeds[2 * i]][o], paths[seeds[2 * i + 1]][o]])) for i in range(len(seeds) // 2)])
            else:
                a = np.array([summary(paths[s][o][:N]) for s in seeds])
            for j, st in enumerate(STATS):
                sd = float(a[:, j].std(ddof=1))
                rows.append(dict(output=o, statistic=st, N=N, n_draws=len(a), sd=sd, range=float(np.ptp(a[:, j])), sd_sqrtN=sd * np.sqrt(N)))
                if N == n:
                    sd1[o, st] = sd
    for r in rows:
        r['ratio'] = r['sd_sqrtN'] / (sd1[r['output'], r['statistic']] * np.sqrt(n)) if sd1[r['output'], r['statistic']] > 0 else float('nan')
    limits = {o: {st: max(FLOOR, min(q * sd1[o, st], ceiling) if ceiling else q * sd1[o, st]) for st in STATS} for o in OUTS}
    extra = {'q': q, 'sd1': sd1}
    extra['slope'] = {}
    for o in OUTS:
        for st in STATS:
            r = [x for x in rows if x['output'] == o and x['statistic'] == st and x['N'] <= n]
            extra['slope'][o, st] = float(np.polyfit(np.log([x['N'] for x in r]), np.log([x['sd'] for x in r]), 1)[0]) if min(x['sd'] for x in r) > 0 else float('nan')
    for o in OUTS:
        top = np.array([summary(paths[s][o]) for s in seeds])
        c1 = top[:c1_seeds]
        extra[o] = dict(spread10=np.ptp(top, 0), spreadC1=np.ptp(c1, 0), mean_of_seeds=top.mean(0), path_sd=float(np.mean([np.nanstd(paths[s][o], ddof=1) for s in seeds])))
    return rows, limits, extra


def report(rows, limits, extra, n, head, ceiling):
    o3 = limits['O3']
    ok = lambda r: 'sd 0' if r['ratio'] != r['ratio'] else ('ok' if abs(r['ratio'] - 1) <= LAW else 'OUT')
    L = [f'# C1 seed noise and limits (brief 187c)', '', f'Machine and run: {head}', '', f'Rule (fixed in the brief before measuring): limit = q x sd(N1), q = {extra["q"]:.3f} (99th percentile of the range of 5 standard normal draws, 10^6 draws, seed 20261127; the brief recalled about 4.6), sd the standard deviation across {len(SEEDS)} seeds at N1 = {n:,} paths'
         + (f'; each limit capped at {ceiling}' if ceiling else '; no absolute ceiling') + f'; a floor of {FLOOR:g} (the 171c zero tolerance, author 2026-11-28)' + '.', '',
         '## 1. Monte Carlo law: sd(N) x sqrt(N) against its value at N1 (ratio; ok = within 20%)', '', '| output | statistic | ' + ' | '.join(f'N={N:,}' for N in sorted({r["N"] for r in rows})) + ' |', '|---|---|' + '---|' * len({r['N'] for r in rows})]
    for o in OUTS:
        for st in STATS:
            rr = sorted((r for r in rows if r['output'] == o and r['statistic'] == st), key=lambda r: r['N'])
            L.append(f'| {o} | {st} | ' + ' | '.join(f'{r["ratio"]:.2f} {ok(r)}' for r in rr) + ' |')
    L += ['', f'sd from {len(SEEDS)} seeds is itself uncertain by about 22% (35% for the five pairs at 2 x N1), so single `OUT` cells at the extremes are not evidence against the law; a row that is OUT at every N is.', '',
          'The ratio is to a single reference (sd at N1, from 10 seeds), and the nested subsamples of one seed share their paths, so a low or high reference moves a whole row together (O2 and O3 means: 1.5 to 1.9 below N1). A reference-free check, added to the brief\'s method: the slope of log sd on log N over N1/8 to N1 (the law says -0.5):', '',
          '| output | ' + ' | '.join(STATS) + ' |', '|---|---|---|---|'] + [f'| {o} | ' + ' | '.join(f'{extra["slope"][o, st]:.2f}' for st in STATS) + ' |' for o in OUTS] + ['',
          '## 2. Limits and the measured spread', '', '| output | statistic | sd(N1) | limit | spread of the 5 C1 seeds | range of all 10 seeds | limit / path sd | limit / abs mean | N for O3 limit 0.15 |', '|---|---|---|---|---|---|---|---|---|']
    for o in OUTS:
        e = extra[o]
        for j, st in enumerate(STATS):
            lim, sd = limits[o][st], extra['sd1'][o, st]
            need = f'{n * (lim / TARGET) ** 2:,.0f}' if o == 'O3' else ''
            L.append(f'| {o} | {st} | {sd:.4f} | {lim:.4f} | {e["spreadC1"][j]:.4f} | {e["spread10"][j]:.4f} | {lim / e["path_sd"]:.3f} | {abs(lim / e["mean_of_seeds"][0]) if e["mean_of_seeds"][0] else float("nan"):.3f} | {need} |')
    bad5 = [f'{o} {st}' for o in OUTS for j, st in enumerate(STATS) if not extra[o]['spreadC1'][j] <= limits[o][st]]
    bad10 = [f'{o} {st}' for o in OUTS for j, st in enumerate(STATS) if not extra[o]['spread10'][j] <= limits[o][st]]
    L += ['', f'Rows where the five C1 seeds spread more than the limit: {", ".join(bad5) or "none"}.',
          f'Rows where the range of all ten seeds exceeds the limit: {", ".join(bad10) or "none"}. (The limit is built for the range of 5 draws, which is the one the test uses; the range of 10 draws is larger on average, about 3.08 sd against 2.33, so the ten-seed list is the stricter check and a row on it is a warning, not a failure of the rule.)', '',
          '"Limit / path sd" is the limit in units of the output\'s own cross-path standard deviation (mean over seeds at N1); "limit / abs mean" in units of the mean over seeds. The last column is information, not a proposal: it assumes sd falls as 1/sqrt(N).']
    return '\n'.join(L) + '\n'


def setup():
    """The converge test's own legacy-arm setup (test_converge.py `base`, `named`): context, the stand-in schedule."""
    import yaml
    from model_v3 import run
    from model_v3.core import pack as pk, returns as rt
    from model_v3.out import assemble as asm
    from model_v3.runner import runner as R, sweeps as S
    man, lv = yaml.safe_load(run.MANIFEST.read_text()), json.loads(run.LEVERS.read_text())
    tier1 = next(o for o in man['outputs'] if o['id'] == 'OT1')['by']['input']
    ctx = R.context(pk.load_pack(next(d for d in sorted(run.PACKS.iterdir()) if (d / 'manifest.json').is_file())), pk.load_register(run.INPUTS), lv, tier1, list(asm.entries(man)),
                    [e['id'] for e in asm.entries(man).values() if e.get('once_not_per_schedule')])
    fmap, _ = S.feasibility(R.make_ev(ctx, rt.streams(run.SEED)['tornado_crn'].standard_normal((R.T, 20))), S.grid(lv))
    named = S.choose(fmap, man['feasibility'])
    spec = named['S_central'] if named else max(fmap, key=lambda p: (p['F1']['short'], -p['M2']['short']))['spec']
    return R, rt, ctx, {'S_central': spec}


KEY = {'O1': ('S_central', 'short', (), 'M1'), 'O2': ('S_central', 'short', (('wealth_band', 'overall'),), None), 'O3': ('S_central', 'single', (), None), 'O4a': ('S_central', 'short', (('income_decile', 'overall'),), None)}


def measure(out, n, workers, seeds):
    d = out / 'paths'
    d.mkdir(parents=True, exist_ok=True)
    todo = [s for s in seeds if not (d / f'seed-{s}.npz').is_file()]
    if not todo:
        return
    R, rt, ctx, spec = setup()
    for s in todo:
        t = time.perf_counter()
        smp, _ = R.level1(ctx, spec, rt.streams(s)['level1_paths'], n=n, workers=workers)
        np.savez_compressed(d / f'seed-{s}.npz', **{o: np.asarray(smp[o][k], float) for o, k in KEY.items()})
        print(f'seed {s}: {time.perf_counter() - t:.0f} s', flush=True)


def load(out, seeds):
    return {s: dict(np.load(out / 'paths' / f'seed-{s}.npz')) for s in seeds}


def header(workers, n):
    cpu = next((l.split(':', 1)[1].strip() for l in open('/proc/cpuinfo') if l.startswith('model name')), 'unknown')
    sha = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    return f'{cpu}, {__import__("os").cpu_count()} cores, numpy {np.__version__}, NPY_DISABLE_CPU_FEATURES={__import__("os").environ.get("NPY_DISABLE_CPU_FEATURES")}, workers {workers}, N1 {n:,}, commit {sha[:12]}'


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    p.add_argument('cmd', choices=('run', 'analyse'))
    p.add_argument('--out', default=str(ROOT / 'results/converge'))
    p.add_argument('--workers', type=int, default=1)
    p.add_argument('--n', type=int, default=10_000)
    p.add_argument('--seeds', type=int, default=len(SEEDS))
    p.add_argument('--write-limits')
    p.add_argument('--ceiling', type=float)
    p.add_argument('--run-url', default='')
    a = p.parse_args(argv)
    out, seeds = Path(a.out), SEEDS[:a.seeds]
    t0 = time.perf_counter()
    if a.cmd == 'run':
        measure(out, a.n, a.workers, seeds)
    rows, limits, extra = analyse(load(out, seeds), seeds, a.n, min(5, len(seeds)), ceiling=a.ceiling)
    with (out / 'c1-noise.csv').open('w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, ['output', 'statistic', 'N', 'n_draws', 'sd', 'range', 'sd_sqrtN', 'ratio'], lineterminator='\n')
        w.writeheader(); w.writerows({k: (f'{v:.6g}' if isinstance(v, float) else v) for k, v in r.items()} for r in rows)
    head = header(a.workers, a.n) + (f', run {a.run_url}' if a.run_url else '') + (f', measured and analysed in {time.perf_counter() - t0:.0f} s' if a.cmd == 'run' else '')
    (out / 'c1-noise.md').write_text(report(rows, limits, extra, a.n, head, a.ceiling), encoding='utf-8')
    if a.write_limits:
        sha = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
        Path(a.write_limits).write_text(json.dumps({'rule': f'limit = q * sd(N1): q = {extra["q"]:.3f}, the 99th percentile of the range of 5 draws in sd units (false-failure rate {RATE}); sd across {len(seeds)} seeds at N1 = {a.n}; legacy arm, S_central, short horizon',
                                                   'date': time.strftime('%Y-%m-%d'), 'q': round(extra['q'], 4), 'false_failure_rate': RATE, 'ceiling': a.ceiling, 'seeds': list(seeds), 'n': a.n, 'commit': sha,
                                                   'limits': {o: {s: float(f'{v:.4g}') for s, v in d.items()} for o, d in limits.items()}}, indent=1) + '\n', encoding='utf-8')
    print(f'wrote {out / "c1-noise.csv"} and {out / "c1-noise.md"}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
