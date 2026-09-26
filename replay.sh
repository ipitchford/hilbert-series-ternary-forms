#!/usr/bin/env bash
# Replay for v0.2.0-candidate (ternary septics, octics, nonics). Quick mode about 3 min; FULL=1 also regenerates the
# exact septic integers to t^760 (about 3 min, 4.8 GB RAM). Recomputing the octic/nonic grid residues is documented in README.
# Usage: PY=/path/to/python ./replay.sh     (python-flint, sympy; a C compiler with OpenMP)
set -euo pipefail
PY="${PY:-python3}"
if [[ "$PY" == */* ]]; then PY="$(cd "$(dirname "$PY")" && pwd)/$(basename "$PY")"; else PY="$(command -v "$PY")"; fi
if [ -z "${CC:-}" ]; then
  for c in gcc-16 gcc-15 gcc-14 gcc-13 gcc clang; do
    if command -v "$c" >/dev/null && echo 'int main(){return 0;}' | "$c" -fopenmp -x c - -o /dev/null 2>/dev/null; then CC="$c"; break; fi
  done
fi
[ -n "${CC:-}" ] || { echo "no C compiler with OpenMP found; set CC"; exit 1; }
cd "$(dirname "$0")"
[ -w scripts ] || { echo "run on a writable copy"; exit 1; }
check_manifest() { (command -v sha256sum >/dev/null && sha256sum -c MANIFEST.sha256 --quiet || shasum -a 256 -c MANIFEST.sha256 --quiet); }
echo "== environment"; "$PY" -c "import sys,flint,sympy; print(sys.version.split()[0],'python-flint',flint.__version__,'sympy',sympy.__version__)"; "$CC" --version | head -1
if [ -f MANIFEST.sha256 ]; then echo "== manifest"; check_manifest; echo "MANIFEST OK"; fi
echo "== build"
( cd scripts && "$CC" -O3 -fopenmp mw5.c -o mw5 && "$CC" -O3 -fopenmp mw6.c -o mw6 && "$CC" -O3 -fopenmp methodAd.c -o methodAd && echo built )
( cd data/septic && "$CC" -O3 -fopenmp methodA16.c -o methodA16 && echo built-septic )
echo "== torus bounds (Derksen Thm 3.4 + 5.1), our enumeration vs the blind program, d = 5..9"
( cd scripts && for d in 5 6 7 8 9; do "$PY" pole_bounds.py $d > /dev/null; done
  "$PY" - <<'PYEOF'
import json, sys
ok = True
for d in (5, 6, 7, 8, 9):
    a = {int(k): v[0] for k, v in json.load(open(f'pole_bounds_d{d}.json')).items() if v[0] > 0}
    t = json.load(open(f'../independent/blind_torus_bounds/results_d{d}.json')); t = t.get('b_r', t)
    b = {int(k): int(v) for k, v in t.items() if int(v) > 0}
    print(f"  d = {d}: identical {a == b}"); ok &= a == b
print("TORUS BOUNDS AGREE:", ok); sys.exit(0 if ok else 1)
PYEOF
)
echo "== validation: the method re-derives Bedratyuk-Xin's d = 5, 6";      (cd scripts && "$PY" check_validation.py | tail -1)
echo "== septic exact integers"
( cd data/septic
  if [ "${FULL:-0}" = 1 ]; then "$PY" regenerate_exact.py fresh 760 | tail -2; fi
  "$PY" regenerate_exact.py fresh 120 | tail -2
  "$PY" regenerate_exact.py lift 760 | tail -1 )
echo "== Theorem 1 (septics, unconditional)";                                (cd scripts && "$PY" certify_septic_unconditional.py | tail -1)
echo "== Theorem 2 (octics)";   (cd scripts && "$PY" certify_ternary.py 8 ../data/octic/d8_L1194_p6.json | tail -1 && "$PY" check_ternary_extra.py 8 ../data/octic/d8_rational.json ../data/octic/d8_L1600_p31.json ../data/octic/wc_d8_N450_p65521.txt ../data/octic/wc_d8_N450_p65519.txt | tail -1)
echo "== Theorem 2 (nonics)";   (cd scripts && "$PY" certify_ternary.py 9 ../data/nonic/d9_L690_p6.json | tail -1 && "$PY" check_ternary_extra.py 9 ../data/nonic/d9_rational.json ../data/nonic/d9_L1000_p31.json ../data/nonic/wc_d9_N400_p65521.txt ../data/nonic/wc_d9_N400_p65519.txt | tail -1)
echo "== fresh spot recomputation: grid engine, d = 8, one 62-bit prime to t^200, and weight counting to t^60"
( cd scripts && "$PY" - <<'PYEOF'
import json, subprocess, sys
from sympy import isprime
R = json.load(open('../data/octic/d8_rational.json')); D = [int(x) for x in R['D']]; N = [int(x) for x in R['N']]
L = 200; a = [0] * (L + 1)
for n in range(L + 1):
    v = N[n] if n < len(N) else 0
    for j in range(1, min(n, len(D) - 1) + 1): v -= D[j] * a[n - j]
    a[n] = v // D[0]
M = 2 * (8 * L + 2) + 1; q = (2**62 - 12345) // M
while not isprime(q * M + 1): q -= 1
p = q * M + 1
out = subprocess.run(['./mw5', '8', str(L), str(p), str(M)], capture_output=True, text=True, check=True).stdout.split()
g = all(a[n] % p == int(out[n]) for n in range(L + 1))
wc = subprocess.run(['./methodAd', '8', '60', '65497'], capture_output=True, text=True, check=True).stdout.split('\n')
w = all(a[int(l.split()[0])] % 65497 == int(l.split()[1]) for l in wc if l.strip())
print(f"  fresh grid prime {p}: agrees {g}; fresh weight counting mod 65497: agrees {w}")
print("SPOT RECOMPUTATION PASSES:", g and w); sys.exit(0 if g and w else 1)
PYEOF
)
echo "== research gates";  "$PY" scripts/check_research_gates.py . | "$PY" -c "import json,sys; d=json.load(sys.stdin); print('RESEARCH GATES:', d['status']); sys.exit(0 if d['status']=='passed' else 1)"
( cd scripts && rm -f pole_bounds_d*.json )
if [ -f MANIFEST.sha256 ]; then echo "== manifest again (no shipped file modified)"; check_manifest; echo "MANIFEST STILL OK"; fi
echo "REPLAY COMPLETED"
