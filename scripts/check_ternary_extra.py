"""Out-of-sample and independent checks of a determined H_d (d{d}_rational.json):
 (1) prediction modulo a 31-bit prime beyond the data used (grid file from run32.py, key 'residues');
 (2) agreement modulo 16-bit primes with an independent weight-counting program (methodAd.c; no roots of unity).
Usage: check_ternary_extra.py d rational.json grid31.json wc_file1.txt [wc_file2.txt ...]"""
import json, sys
from sympy import isprime
d = int(sys.argv[1]); R = json.load(open(sys.argv[2])); g = json.load(open(sys.argv[3])); wcs = sys.argv[4:]
D = [int(x) for x in R['D']]; N = [int(x) for x in R['N']]
Lmax = max(g['L'], *(sum(1 for _ in open(f)) - 1 for f in wcs))
a = [0] * (Lmax + 1)
for n in range(Lmax + 1):
    v = N[n] if n < len(N) else 0
    for j in range(1, min(n, len(D) - 1) + 1): v -= D[j] * a[n - j]
    q, r = divmod(v, D[0]);
    if r: sys.exit('non-integral')
    a[n] = q
ok = True
p = g['primes'][0]; res = [int(x) for x in g['residues'][0]]; L = g['L']
meta = isprime(p) and (p - 1) % g['M'] == 0 and g['M'] > d * L + 4
pred = all(a[n] % p == res[n] for n in range(L + 1))
print(f"(1) 31-bit prime {p}, M = {g['M']}: metadata {meta}; H_{d} agrees for all n <= {L}: {pred}")
ok &= meta and pred
for f in wcs:
    rows = [l.split() for l in open(f) if l.strip()]; q = int(f.split('_p')[-1].split('.')[0])
    good = isprime(q) and all(a[int(n)] % q == int(v) for n, v in rows)
    print(f"(2) weight counting mod {q}, n <= {len(rows)-1}: agrees {good}"); ok &= good
print(f"d = {d} EXTRA CHECKS PASS:", ok); sys.exit(0 if ok else 1)
