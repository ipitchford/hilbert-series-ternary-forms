"""Determine and certify H_d(t), the Hilbert series of C[S^d C^3]^SL3. Usage: certify_ternary.py d grid.json
Inputs: torus bounds b_r (pole_bounds.py d; Derksen Thm 3.4 + 5.1); exact a_n for n <= floor(K/2) from grid residues
modulo several primes (CRT); functional equation H(1/t) = (-1)^delta t^dimV H(t), delta = dimV - 8.
Steps: B = prod Phi_r^{min(delta,b_r)}; P_n = sum_j B_j a_{n-j} for n <= K/2; P_{K-n} = eps P_n; H = P/B in lowest terms.
Checks: primes distinct and prime, p = 1 mod M, M > dL+4; modulus > 2*C(K/2+dimV-1, dimV-1); lifted a_n in range;
pole order at 1 equals delta; the series is nonnegative. Writes d{d}_rational.json. Exit 0 only if all checks pass."""
import json, os, sys, subprocess
from math import comb, prod
from sympy import isprime
from flint import fmpz_poly
here = os.path.dirname(os.path.abspath(__file__))
PB = os.path.join(here, 'pole_bounds.py')
d = int(sys.argv[1]); gridfile = sys.argv[2]
subprocess.run([sys.executable, PB, str(d)], cwd=here, check=True, capture_output=True)
b = {int(k): v[0] for k, v in json.load(open(os.path.join(here, f'pole_bounds_d{d}.json'))).items()}
dimV = (d + 1) * (d + 2) // 2; delta = dimV - 8
p = {r: min(delta, k) for r, k in b.items() if k > 0}
B = fmpz_poly([1])
for r, e in p.items():
    for _ in range(e): B *= fmpz_poly.cyclotomic(r)
if B[0] < 0: B = -B
K = B.degree() - dimV; half = K // 2
sB = 1 if int(B[B.degree()]) == int(B[0]) else -1
eps = (-1) ** delta * sB
gridfile = os.path.abspath(gridfile); outdir = os.path.dirname(gridfile)
g = json.load(open(gridfile))
primes, M, L = g['primes'], g['M'], g['L']
meta = len(set(primes)) == len(primes) and all(isprime(q) and (q - 1) % M == 0 for q in primes) and M > d * L + 4 and L >= half
a = [int(x) for x in g['coeffs']]
mod = prod(primes)
bounds_ok = all(0 <= a[n] <= comb(n + dimV - 1, dimV - 1) for n in range(half + 1)) and mod > 2 * comb(half + dimV - 1, dimV - 1)
Bl = [int(B[i]) for i in range(B.degree() + 1)]
P = [0] * (K + 1)
for n in range(half + 1):
    P[n] = sum(Bl[j] * a[n - j] for j in range(0, min(n, len(Bl) - 1) + 1))
for n in range(half + 1, K + 1): P[n] = eps * P[K - n]
if K % 2 == 0 and eps == -1 and P[half] != 0: sys.exit('antisymmetric middle coefficient must vanish')
Pp = fmpz_poly(P); gcd = Pp.gcd(B)
N, D = Pp // gcd, B // gcd
if D[0] < 0: N, D = -N, -D
# pole order at t = 1 must equal the Krull dimension
m1, Dq = 0, D
while Dq(1) == 0: Dq = Dq // fmpz_poly([-1, 1]); m1 += 1
# series of N/D reproduces the input a_n (sanity of the division)
Dl = [int(D[i]) for i in range(D.degree() + 1)]; Nl = [int(N[i]) for i in range(N.degree() + 1)]
s = [0] * (L + 1)
for n in range(L + 1):
    v = Nl[n] if n < len(Nl) else 0
    for j in range(1, min(n, len(Dl) - 1) + 1): v -= Dl[j] * s[n - j]
    q, rem = divmod(v, Dl[0]); s[n] = q
    if rem: sys.exit('non-integral series')
reproduces = s[:half + 1] == a[:half + 1]
nonneg = all(x >= 0 for x in s)
cyc = {}
Dr = D
for r in sorted(p):
    c = 0
    while Dr.degree() > 0 and (Dr % fmpz_poly.cyclotomic(r)) == 0: Dr = Dr // fmpz_poly.cyclotomic(r); c += 1
    if c: cyc[r] = c
json.dump({"d": d, "D": [int(D[i]) for i in range(D.degree() + 1)], "N": [str(int(N[i])) for i in range(N.degree() + 1)],
           "cyclotomic": {str(r): c for r, c in cyc.items()}, "bound_degree": B.degree(), "K": K, "eps": eps},
          open(os.path.join(outdir, f'd{d}_rational.json'), 'w'))
print(f"B: {len(p)} orders, deg {B.degree()}; K = {K}; eps = {eps:+d}; coefficients used 0..{half} (have {L})")
print(f"grid metadata valid: {meta}; lifted a_n in range and modulus {mod.bit_length()} bits > 2*C(K/2+dimV-1,dimV-1): {bounds_ok}")
print(f"least denominator degree {D.degree()}, numerator degree {N.degree()}; pole order at 1 = {m1} (Krull dim {delta})")
print(f"series of N/D reproduces a_0..a_{half}: {reproduces}; coefficients nonnegative to t^{L}: {nonneg}")
print("cyclotomic multiplicities:", cyc)
ok = meta and bounds_ok and reproduces and m1 == delta and nonneg
print(f"d = {d} DETERMINATION PASSES:", ok); sys.exit(0 if ok else 1)
