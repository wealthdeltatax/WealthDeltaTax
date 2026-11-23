#!/usr/bin/env bash
# Model v3 acceptance (acceptance.md section 1): exits 0 only if every step does; never passes --final (the author's act).  --check FILE runs step 5 only, --compare A B step 6 only (seeded-breakage tests).  The two runs are `--size quick` (author, 2026-11-23: the full-size run is not part of acceptance).
set -euo pipefail
cd "$(dirname "$0")/../.."
step5() { python -I - "$1" <<'PY'
import json, sys, yaml
d, m = json.load(open(sys.argv[1])), yaml.safe_load(open('docs/model-v3/outputs.yml'))
r = d['run']
nul = lambda x: x is None or (isinstance(x, dict) and any(map(nul, x.values()))) or (isinstance(x, list) and any(map(nul, x)))
bad = [f'no entry for {e["id"]}' for k in ('outputs', 'checks') for e in m[k] if e['id'] not in d['outputs']]
bad += ['a null cell'] * nul(d['outputs'])
bad += [f'run.{k} is {r.get(k)!r}' for k, ok in (('fixture', r.get('fixture') is False), ('seed', r.get('seed') == 20261118), ('paths', r['paths'] >= 1000), ('level2_paths', r.get('level2_paths', 0) >= 50),
        ('unfilled_paths', r.get('unfilled_paths', 0) <= 0.05 * r['paths']), ('status', r['status'] == 'provisional')) if not ok]
print('\n'.join(bad) or 'step 5: ok'); sys.exit(1 if bad else 0)
PY
}
step7() { for p in 'arithmetic' 'refund.{0,40}tau|tau.{0,12}loss' 'envelope.{0,60}reset|reset.{0,30}death'; do   # R6: each convention in a module docstring and in decisions.md
  { grep -q -i -E "$p" model_v3/core/returns.py model_v3/core/kernel.py && grep -q -i -E "$p" docs/decisions.md; } || { echo "R6: convention /$p/ missing"; return 1; }; done; }
case "${1:-}" in --check) step5 "$2"; exit;; --compare) cmp "$2" "$3"; exit;; esac
TMP=$(mktemp -d); TMP2=$(mktemp -d); trap 'rm -rf "$TMP" "$TMP2"' EXIT
RUN="import sys; sys.path.insert(0, '.'); from model_v3 import run; run.main(['--size', 'quick', '--out', sys.argv[1]])"   # python -I ignores the current directory, so -m model_v3.run cannot be found
python -I -m pytest tests/model_v3 -q -x -m "not converge"                          # 1
python -I -m pytest tests/model_v3/test_converge.py -q -m converge                  # 2
python -I -c "$RUN" "$TMP"                                                          # 3
python -I pipeline/validate_outputs.py "$TMP/outputs.json"                          # 4
step5 "$TMP/outputs.json"                                                           # 5
python -I -c "$RUN" "$TMP2"                                                         # 6
cmp "$TMP/outputs.json" "$TMP2/outputs.json"
step7                                                                               # 7
echo "accept.sh: all steps passed (provisional run)"
