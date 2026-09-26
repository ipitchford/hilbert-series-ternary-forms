"""Structural consequences of H_d (d = 7, 8, 9) that follow from the series alone.
(1) Minimal generators in low degree: g_n = a_n - dim(A_+^2)_n. dim(A_+^2)_n <= M_n = number of monomials of degree n in
    generators of lower degree (computed recursively from lower bounds on g_m is NOT valid; we use the exact g_m where known
    and stop at the first degree where g_m is not exact). A single nonzero product is nonzero in a domain, so M_n <= 1 gives
    g_n exactly. Otherwise report a_n - M_n <= g_n <= a_n - (1 if M_n >= 1 else 0).
(2) Homogeneous systems of parameters: if A is finite over C[f_1..f_delta] with deg f_i = k_i, then H = Q/prod(1-t^{k_i}) with
    Q a polynomial, so the least denominator divides prod(1-t^{k_i}): #{i : r | k_i} >= m_r for every r. We minimise
    sum k_i and max k_i over multisets satisfying these constraints with each k_i a degree in which invariants exist (MILP).
(3) The leading constant c = lim (1-t)^delta H; for any hsop over which A is free (A is Cohen-Macaulay), the number of
    secondary invariants is c * prod k_i."""
import json, sys
from fractions import Fraction
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from flint import fmpz_poly
from math import prod
import os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
SRC = {7: R + '/septic/d7_rational.json', 8: R + '/octic/d8_rational.json', 9: R + '/nonic/d9_rational.json'}
out = {}
for d, f in SRC.items():
    J = json.load(open(f)); D = [int(x) for x in J['D']]; N = [int(x) for x in J['N']]
    dimV = (d + 1) * (d + 2) // 2; delta = dimV - 8
    Lmax = 400
    a = [0] * (Lmax + 1)
    for n in range(Lmax + 1):
        v = N[n] if n < len(N) else 0
        for j in range(1, min(n, len(D) - 1) + 1): v -= D[j] * a[n - j]
        a[n] = v // D[0]
    # (1) generators
    gens = {}; rows = []
    exact_so_far = True
    for n in range(1, 31):
        if a[n] == 0: continue
        # monomials of degree n in generators of degree < n (counted with multiplicity g_m); requires exact g_m
        if not exact_so_far: break
        poly = [1] + [0] * n
        for m, g in gens.items():
            for _ in range(g):
                for k in range(m, n + 1): poly[k] += poly[k - m]
        Mn = poly[n]
        if Mn <= 1:
            g = a[n] - Mn; gens[n] = g; rows.append((n, a[n], Mn, g, g)); 
        else:
            rows.append((n, a[n], Mn, a[n] - Mn, a[n] - 1)); exact_so_far = False
    # (2) hsop constraints via MILP
    J2 = {int(k): int(v) for k, v in (J.get('cyclotomic') or json.load(open(R + '/septic/d7_denominator.json'))['cyclotomic']).items()}
    degs = [k for k in range(1, 600) if a[k] > 0] if Lmax >= 600 else None
    a2 = a + [0] * 1000
    # extend series to 1000 for degree availability
    A = [0] * 1001
    for n in range(1001):
        v = N[n] if n < len(N) else 0
        for j in range(1, min(n, len(D) - 1) + 1): v -= D[j] * A[n - j]
        A[n] = v // D[0]
    degs = [k for k in range(1, 1001) if A[k] > 0]
    rs = sorted(J2)
    c = np.array(degs, dtype=float)
    cons = [LinearConstraint(np.ones((1, len(degs))), delta, delta)]
    Amat = np.array([[1.0 if k % r == 0 else 0.0 for k in degs] for r in rs]); lb = np.array([J2[r] for r in rs], dtype=float)
    cons.append(LinearConstraint(Amat, lb, np.inf))
    res = milp(c, constraints=cons, integrality=np.ones(len(degs)), bounds=Bounds(0, delta))
    xs = {degs[i]: int(round(v)) for i, v in enumerate(res.x) if round(v) > 0}
    # (3) leading constant: c = lim (1-t)^delta H = N(1) / (D/(1-t)^delta)(1)
    Dp = fmpz_poly(D)
    for _ in range(delta): Dp = Dp // fmpz_poly([1, -1])
    cconst = Fraction(sum(N), int(Dp(1)))
    msum = sum(k * m for k, m in xs.items())
    secondaries = cconst * prod(k ** m for k, m in xs.items())
    out[d] = {"generators_low_degree": [{"degree": n, "a_n": an, "decomposable_monomials_upper": Mn, "g_n_lower": lo, "g_n_upper": hi} for n, an, Mn, lo, hi in rows],
              "hsop_min_sum": msum, "hsop_min_sum_degrees": {str(k): m for k, m in sorted(xs.items())}, "milp_status": res.message,
              "hsop_max_degree_lower_bound": max(J2), "leading_constant": str(cconst), "secondaries_for_min_sum_hsop_if_free": str(secondaries)}
    print(f"d = {d}: generators (n, a_n, M_n, g_n range): {rows}")
    print(f"   hsop: min sum of degrees {msum} with {xs}; some hsop degree divisible by {max(J2)}; c = {float(cconst):.6e}; secondaries at min-sum degrees = {secondaries}")
dest = os.path.join(R, 'consequences.json')
if '--check' in sys.argv:
    same = json.load(open(dest)) == json.loads(json.dumps(out))
    print("consequences match data/consequences.json:", same); sys.exit(0 if same else 1)
json.dump(out, open(dest, 'w'), indent=1)
