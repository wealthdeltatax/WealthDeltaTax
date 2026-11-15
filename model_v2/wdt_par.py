"""
wdt_par.py -- ordered process-pool map for the WDT cores
========================================================
Base layer, same level as wdt_core / wdt_kernel / wdt_jst. Imports the standard library only (numpy is touched only
through the optional threadpoolctl). It knows nothing about the TOML, the cores or the model: a core hands it a
top-level function and a list of tasks and gets the results back IN TASK ORDER.

WHY PROCESSES, NOT THREADS
  The per-window work is many small numpy calls on arrays of a few thousand elements. That is dominated by Python
  interpreter time and per-call numpy overhead, which hold the GIL, so threads would not scale. Processes do.

WHAT IT GUARANTEES
  * Results come back in submission order, whatever order the workers finish in. A core that is deterministic
    serially is therefore deterministic here: same rows, same order, bit-identical numbers.
  * workers == 1 never creates a process: WorkerPool.parallel is False and the core runs its own serial path.
  * Persistent: the pool is created once (the `with` block in the core's main) and reused for every scenario, so the
    cost of starting workers (several seconds under 'spawn', which is also what Windows does) is paid once.
  * 'spawn' is used on every platform, so Linux behaves like the Windows run. Functions handed to the pool must be
    top-level and importable; the entry script must guard its main() with `if __name__ == '__main__'`.
  * Each worker is limited to one BLAS / OpenMP thread, so N workers do not become N x cores threads.
  * A failed task re-raises in the parent with the worker's traceback; the remaining tasks are cancelled. A worker
    that dies (out of memory) raises with a hint instead of hanging.

WORKER COUNT
  resolve_workers(None) -> cores available to this process minus one (min 1).   resolve_workers(1) -> serial.
  The count is a RUN setting (CLI --workers), not a model input, so it is deliberately not in the TOML.

USAGE
  with WorkerPool(workers, initializer=init, initargs=(big, read_only, state), tag=...) as pool:
      if pool.parallel:
          rows = pool.map_chunks(task_fn, jobs, ctx)       # task_fn((ctx, chunk)) -> list; results flattened, in order
  `initializer(*initargs)` runs once per worker and is where the large read-only inputs go (pickled once per worker,
  not once per task). `tag` is any comparable value the caller can check to be sure a pool belongs to its inputs.

  python wdt_par.py     runs the self-test
"""

import math
import os
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures.process import BrokenProcessPool
import multiprocessing as mp

_THREAD_VARS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS',
                'VECLIB_MAXIMUM_THREADS')
MAX_CHUNK = 16          # windows are ~0.1 to 1 s each: a chunk of 16 is long enough to hide the pickling, short enough to balance


def available_cpus():
    """Cores this process may use (affinity-aware where the OS has it)."""
    try:
        return len(os.sched_getaffinity(0))
    except AttributeError:
        return os.cpu_count() or 1


def resolve_workers(n=None):
    """None or 0 -> available cores minus one (at least 1). A positive int is used as given. Negative raises."""
    if n is None or n == 0:
        return max(1, available_cpus() - 1)
    n = int(n)
    if n < 0:
        raise ValueError(f'workers must be >= 0 (0 = automatic), got {n}')
    return n


def chunk_size(n_tasks, workers, cap=MAX_CHUNK):
    """Items per task: about four tasks per worker so the last one does not leave the others idle, capped at `cap`."""
    return max(1, min(cap, math.ceil(n_tasks / (4 * max(1, workers)))))


def _bootstrap(init, initargs):
    """Runs once in each worker: one BLAS thread, then the caller's initializer."""
    try:
        from threadpoolctl import threadpool_limits
        threadpool_limits(1)
    except Exception:                        # threadpoolctl is optional; the env vars set by the parent do the same job
        pass
    if init is not None:
        init(*initargs)


class WorkerPool:
    """Persistent ordered pool; see the module docstring. Use as a context manager."""

    def __init__(self, workers=None, initializer=None, initargs=(), tag=None):
        self.workers = resolve_workers(workers)
        self.tag = tag
        self._init, self._initargs = initializer, tuple(initargs)
        self._ex = None

    @property
    def parallel(self):
        return self.workers > 1

    def __enter__(self):
        if self.parallel and self._ex is None:
            for v in _THREAD_VARS:           # inherited by the spawned workers, before they import numpy
                os.environ[v] = '1'
            self._ex = ProcessPoolExecutor(max_workers=self.workers, mp_context=mp.get_context('spawn'),
                                           initializer=_bootstrap, initargs=(self._init, self._initargs))
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close(abort=exc_type is not None)
        return False

    def close(self, abort=False):
        if self._ex is not None:
            self._ex.shutdown(wait=not abort, cancel_futures=True)
            self._ex = None

    def map(self, fn, tasks):
        """[fn(t) for t in tasks], run in the workers, results in task order."""
        if self._ex is None:
            raise RuntimeError('WorkerPool.map: no live pool (workers == 1, or used outside its with-block)')
        futs = [self._ex.submit(fn, t) for t in tasks]
        out = []
        try:
            for f in futs:
                out.append(f.result())
        except BrokenProcessPool as e:
            for f in futs:
                f.cancel()
            raise RuntimeError('a worker process died (usually out of memory). Re-run with fewer workers, '
                               'e.g. --workers 2, or --workers 1 for the serial path') from e
        except BaseException:
            for f in futs:
                f.cancel()
            raise
        return out

    def map_chunks(self, fn, items, ctx=None, chunk=None):
        """
        Split `items` into consecutive chunks, call fn((ctx, chunk)) on each in the workers, and return the
        per-chunk lists joined back into one list in the original order. fn must return a list with one entry
        per item of its chunk. ctx is pickled once per chunk, so keep it small (large read-only inputs go in
        the initializer).
        """
        items = list(items)
        size = chunk or chunk_size(len(items), self.workers)
        parts = self.map(fn, [(ctx, items[i:i + size]) for i in range(0, len(items), size)])
        out = [r for part in parts for r in part]
        if len(out) != len(items):
            raise RuntimeError(f'map_chunks: {len(items)} items in, {len(out)} results out')
        return out


# ─────────────────────────────────────────────────────────────
# SELF-TEST (python wdt_par.py)
# ─────────────────────────────────────────────────────────────
_STATE = {}


def _t_init(base):
    _STATE['base'] = base


def _t_run(task):
    ctx, chunk = task
    import time
    time.sleep(0.02 * (len(chunk) % 3))      # make the chunks finish out of order
    if ctx == 'boom' and 7 in chunk:
        raise ValueError('boom at 7')
    return [(_STATE['base'] + x) * ctx if ctx != 'boom' else x for x in chunk]


def _self_test():
    assert resolve_workers(1) == 1 and resolve_workers(3) == 3 and resolve_workers(None) >= 1
    for bad in (-1,):
        try:
            resolve_workers(bad)
            raise AssertionError('negative workers must raise')
        except ValueError:
            pass
    assert chunk_size(1, 8) == 1 and chunk_size(10 ** 6, 8) == MAX_CHUNK and chunk_size(64, 4) == 4
    with WorkerPool(1) as p1:
        assert not p1.parallel and p1._ex is None
    items = list(range(53))
    with WorkerPool(3, initializer=_t_init, initargs=(100,), tag='t') as pool:
        assert pool.parallel and pool.tag == 't'
        got = pool.map_chunks(_t_run, items, ctx=2, chunk=5)
        assert got == [(100 + x) * 2 for x in items], 'order or value mismatch'
        got2 = pool.map_chunks(_t_run, items, ctx=3)                    # same pool, second sweep, automatic chunking
        assert got2 == [(100 + x) * 3 for x in items]
        try:
            pool.map_chunks(_t_run, items, ctx='boom', chunk=4)
            raise AssertionError('worker exception must reach the parent')
        except ValueError as e:
            assert 'boom at 7' in str(e)
        assert pool.map_chunks(_t_run, items, ctx=1, chunk=9) == [100 + x for x in items]   # still usable after a task error
    print('wdt_par self-test ok')


if __name__ == '__main__':
    _self_test()
