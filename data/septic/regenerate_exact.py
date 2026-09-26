"""Regenerate the exact septic coefficients a_0..a_N from methodA16 (weight counting, no roots of unity).

Usage:
  python regenerate_exact.py run N [prime ...]   run ./methodA16 N p for each prime, store runs/methodA16_N{N}_p{p}.txt
  python regenerate_exact.py fresh N             run into a temporary directory, then require byte-identical outputs to
                                                 the archived runs/ files (if present) and lift the fresh outputs
  python regenerate_exact.py lift N [RUNS_DIR]   CRT-lift the stored per-prime outputs for N; check and compare

The lift step checks: every modulus is prime and they are pairwise distinct; each output file covers n = 0..N;
the product of the moduli exceeds 2*C(N+35,35), an upper bound for a_n (dim Sym^n of a 36-dim space);
the lifted integers lie in [0, C(n+35,35)]; the result equals methodA_exact_760.json on the common range.
Exit status 0 only if every check passes.
"""
import json, os, subprocess, sys
from math import comb, prod
from sympy import isprime
from sympy.ntheory.modular import crt

HERE = os.path.dirname(os.path.abspath(__file__))
PRIMES = [65521, 65519, 65497, 65479, 65449, 65447, 65437, 65423, 65419, 65413, 65407, 65393, 65381, 65371, 65357]

RUNS = os.path.join(HERE, "runs")
def path(N, p): return os.path.join(RUNS, f"methodA16_N{N}_p{p}.txt")

def run(N, primes):
    exe = os.path.join(HERE, "methodA16")
    for p in primes:
        if not (isprime(p) and p < 65536): sys.exit(f"refusing p = {p}: methodA16 needs a prime below 65536")
        out = subprocess.run([exe, str(N), str(p)], check=True, capture_output=True, text=True).stdout
        with open(path(N, p), "w") as f: f.write(out)
        print(f"N={N} p={p}: stored", flush=True)

def lift(N):
    primes = [p for p in PRIMES if os.path.exists(path(N, p))]
    ok = len(primes) == len(set(primes)) and all(isprime(p) for p in primes)
    res = {}
    for p in primes:
        rows = [l.split() for l in open(path(N, p)) if l.strip()]
        vals = {int(a): int(b) for a, b in rows}
        ok &= sorted(vals) == list(range(N + 1)) and all(0 <= v < p for v in vals.values())
        res[p] = vals
    M = prod(primes); bound = comb(N + 35, 35)
    ok_mod = M > 2 * bound
    print(f"primes used: {len(primes)} distinct primes, all prime: {ok}")
    print(f"modulus {M.bit_length()} bits > 2*C(N+35,35) ({(2*bound).bit_length()} bits): {ok_mod}")
    a = []
    for n in range(N + 1):
        x, _ = crt(primes, [res[p][n] for p in primes]); x = int(x)
        ok &= 0 <= x <= comb(n + 35, 35)
        a.append(x)
    stored = [int(c) for c in json.load(open(os.path.join(HERE, "methodA_exact_760.json")))["coeffs"]]
    m = min(len(stored), N + 1)
    same = a[:m] == stored[:m]
    print(f"lifted a_0..a_{N}; in range [0, C(n+35,35)]: {ok}; equals methodA_exact_760.json on n <= {m-1}: {same}")
    allok = ok and ok_mod and same
    print("EXACT REGENERATION CHECK PASSES:", allok)
    return allok

if __name__ == "__main__":
    cmd, N = sys.argv[1], int(sys.argv[2])
    if cmd == "run": run(N, [int(x) for x in sys.argv[3:]] or PRIMES)
    elif cmd == "fresh":
        import tempfile, filecmp
        archived = RUNS; RUNS = tempfile.mkdtemp(); run(N, PRIMES)
        same = all(filecmp.cmp(path(N, p), os.path.join(archived, os.path.basename(path(N, p))), shallow=False)
                   for p in PRIMES if os.path.exists(os.path.join(archived, os.path.basename(path(N, p)))))
        print(f"fresh outputs byte-identical to archived runs/ files: {same}")
        ok = lift(N); sys.exit(0 if (ok and same) else 1)
    elif cmd == "lift":
        if len(sys.argv) > 3: RUNS = sys.argv[3]
        sys.exit(0 if lift(N) else 1)
    else: sys.exit("usage: regenerate_exact.py run|lift N [primes]")
