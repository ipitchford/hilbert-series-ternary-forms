"""Unconditional certificate for H(I_{3,7}, t) = R(t).
Inputs: pole-order bounds b_r (pole_bounds.py, fixed-locus argument), Krull dimension 28, functional equation
H(1/t) = t^36 H(t) (paper Section 3.1), exact a_n for n <= 760 (independent weight counting), candidate R.
B' = prod_r Phi_r^{p_r}, p_r = min(28, b_r). Then H*B' is a polynomial P' with P'(t) = eps t^K P'(1/t), K = deg B' - 36,
determined by a_0..a_{floor(K/2)}. If D_R | B', P_R = R*B' has the same shape, and R agrees with the exact a_n up to
floor(K/2), then H = R."""
import json, os, sys
from flint import fmpz_poly
here = os.path.dirname(os.path.abspath(__file__)); up = os.path.join(here, '..', 'data', 'septic')
import subprocess
# regenerate the pole bounds from the enumeration script rather than trusting a stored file
subprocess.run([sys.executable, os.path.join(here, 'pole_bounds.py'), '7'], cwd=here, check=True, capture_output=True)
b = {int(k): v[0] for k, v in json.load(open(os.path.join(here, 'pole_bounds_d7.json'))).items()}
p = {r: min(28, k) for r, k in b.items() if k > 0}
B = fmpz_poly([1])
for r, e in p.items():
    for _ in range(e): B *= fmpz_poly.cyclotomic(r)
Rj = json.load(open(os.path.join(up, 'd7_rational.json')))
D = fmpz_poly([int(x) for x in Rj['D']]); N = fmpz_poly([int(x) for x in Rj['N']])
q, rem = divmod(B, D)
P = N * q; K = B.degree() - 36
c = [int(P[i]) for i in range(P.degree() + 1)]
sB = 1 if int(B[B.degree()]) == int(B[0]) else -1
eps = sB                                     # H(1/t) = +t^36 H(t)
shape = rem == 0 and P.degree() <= K and all((c[i] if i < len(c) else 0) == eps * (c[K - i] if K - i < len(c) else 0) for i in range(K + 1))
half = K // 2
ind = [int(x) for x in json.load(open(os.path.join(up, 'methodA_exact_760.json')))['coeffs']]
a = [0] * (half + 1); Dl = [int(D[i]) for i in range(D.degree() + 1)]; Nl = [int(x) for x in Rj['N']]
for n in range(half + 1):
    s = Nl[n] if n < len(Nl) else 0
    for j in range(1, min(n, len(Dl) - 1) + 1): s -= Dl[j] * a[n - j]
    q_, r_ = divmod(s, Dl[0])
    if r_: sys.exit('non-integral series coefficient')
    a[n] = q_
agree = half <= len(ind) - 1 and a == ind[:half + 1]
print(f"B' = prod Phi_r^p_r over {len(p)} orders; deg B' = {B.degree()}; K = {K}; coefficients needed: 0..{half} (exact data to {len(ind)-1})")
print(f"D_R divides B': {rem == 0}; R*B' polynomial of degree <= K with P(t) = {eps:+d} t^K P(1/t): {shape}")
print(f"R agrees with the exact a_n for n <= {half}: {agree}")
ok = shape and agree
print("UNCONDITIONAL SEPTIC CERTIFICATE PASSES:", ok); sys.exit(0 if ok else 1)
