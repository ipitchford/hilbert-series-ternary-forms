"""Run mw6 (32-bit engine) for ternary d-ics at one or more 31-bit primes p = 1 (mod M). Usage: run32.py d L k out.json [skip]"""
import sys, subprocess, time, json
from sympy import isprime
d, L, k, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
skip = int(sys.argv[5]) if len(sys.argv) > 5 else 0
M = 2 * (d * L + 2) + 1; q = (2**31 - 1) // M; primes = []
while len(primes) < k + skip:
    if isprime(q * M + 1): primes.append(q * M + 1)
    q -= 1
primes = primes[skip:]; res = []
for p in primes:
    t0 = time.time()
    r = subprocess.run(['./mw6', str(d), str(L), str(p), str(M)], capture_output=True, text=True, check=True)
    res.append(r.stdout.split()); print(f"prime {p}: {time.time()-t0:.1f} s", flush=True)
json.dump({"d": d, "L": L, "M": M, "primes": primes, "residues": res}, open(out, 'w'))
