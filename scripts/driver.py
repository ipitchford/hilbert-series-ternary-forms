"""Run mw5 (62-bit Montgomery engine) for ternary d-ics modulo several primes p = 1 (mod M) and combine by CRT.
Usage: driver.py d L nprimes [outfile]"""
import sys, subprocess, time, json
from sympy import isprime
from sympy.ntheory.modular import crt
d, L, k = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
out = sys.argv[4] if len(sys.argv) > 4 else None
M = 2 * (d * L + 2) + 1
primes = []; q = (2**62) // M
while len(primes) < k:
    p = q * M + 1
    if isprime(p): primes.append(p)
    q -= 1
res = []
for p in primes:
    t0 = time.time()
    r = subprocess.run(['./mw5', str(d), str(L), str(p), str(M)], capture_output=True, text=True, check=True)
    res.append([int(x) for x in r.stdout.split()])
    print(f"prime {p}: {time.time()-t0:.1f} s", file=sys.stderr)
coef = []
for n in range(L + 1):
    v, mod = crt(primes, [r[n] for r in res])
    coef.append(int(v))
modulus = 1
for p in primes: modulus *= p
if out:
    json.dump({"d": d, "L": L, "M": M, "primes": primes, "coeffs": [str(c) for c in coef]}, open(out, 'w'))
print("max coefficient bits:", max(c.bit_length() for c in coef), "modulus bits:", modulus.bit_length(), file=sys.stderr)
print(coef[:40])
