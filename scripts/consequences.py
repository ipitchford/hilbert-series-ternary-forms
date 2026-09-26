"""Structural consequences of H_d (d = 7, 8, 9) that follow from the series alone.
(1) Minimal generators in low degree: g_n = a_n - dim(A_+^2)_n, where (A_+^2)_n is spanned by the monomials of degree n
    (at least two factors) in generators of lower degree. Degrees are processed in order while every lower g_m is exact.
    - Common factor (exact): if every such monomial contains one generator f of degree e, then (A_+^2)_n = f A_{n-e}
      (both inclusions are immediate), and multiplication by f is injective in the domain A, so dim = a_{n-e}.
    - Otherwise: max over 1 <= m < n of (a_m + a_{n-m} - 1) <= dim(A_+^2)_n <= min(a_n, number of monomials). The lower
      bound is Hopf's: a bilinear map C^p x C^q -> C^s without zero divisors has rank >= p + q - 1 (the kernel, as a linear
      subspace of P(C^p (x) C^q), must miss the Segre variety of dimension p + q - 2).
(2) Homogeneous systems of parameters: if A is finite over C[f_1..f_delta] with deg f_i = k_i, then H = Q/prod(1-t^{k_i}) with
    Q a polynomial, so the least denominator divides prod(1-t^{k_i}): #{i : r | k_i} >= m_r for every r (the method used by
    Dixmier and by Brouwer-Popoviciu for binary forms). We minimise sum k_i over multisets satisfying these constraints with each
    k_i a degree in which invariants exist (MILP, HiGHS). Candidate degrees are capped at S - (delta - 1) k_min, where S is the
    sum of a feasible multiset: no optimal multiset can contain a larger degree. The optimum is solver-computed (HiGHS reports
    optimality); it is not independently certified.
(3) The leading constant c = lim (1-t)^delta H. A is Cohen-Macaulay, hence free over any hsop; the number of secondary
    invariants over an hsop with degrees k_i is c * prod k_i."""
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
    for n in range(1, 31):
        if a[n] == 0: continue
        # monomials of degree n (>= 2 factors) in generators of degree < n, by generator degree multiset
        poly = [1] + [0] * n
        for m, g in gens.items():
            for _ in range(g):
                for k in range(m, n + 1): poly[k] += poly[k - m]
        Mn = poly[n] - gens.get(n, 0)
        # common factor: a single generator f (degree e, g_e = 1) dividing every monomial of degree n
        common = None
        for e, ge in gens.items():
            if ge != 1: continue
            q = [1] + [0] * n                      # monomials avoiding f
            for m, g in gens.items():
                for j in range(g - (1 if m == e else 0)):
                    for k in range(m, n + 1): q[k] += q[k - m]
            if q[n] == 0 and Mn > 0: common = e; break
        if Mn == 0: lo = hi = 0; rule = 'none'
        elif common is not None: lo = hi = a[n - common]; rule = f'common factor of degree {common}'
        else:
            lo = max(a[m] + a[n - m] - 1 for m in range(1, n) if a[m] > 0 and a[n - m] > 0); hi = min(a[n], Mn); rule = 'Hopf / monomial count'
        rows.append((n, a[n], lo, hi, a[n] - hi, a[n] - lo, rule))
        if lo != hi: break
        gens[n] = a[n] - lo
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
    rs = sorted(J2)
    def solve(cap):
        degs = [k for k in range(1, cap + 1) if A[k] > 0]
        cons = [LinearConstraint(np.ones((1, len(degs))), delta, delta),
                LinearConstraint(np.array([[1.0 if k % r == 0 else 0.0 for k in degs] for r in rs]), np.array([J2[r] for r in rs], dtype=float), np.inf)]
        res = milp(np.array(degs, dtype=float), constraints=cons, integrality=np.ones(len(degs)), bounds=Bounds(0, delta))
        return res, {degs[i]: int(round(v)) for i, v in enumerate(res.x) if round(v) > 0}
    res0, xs0 = solve(400)                                  # any feasible multiset gives S
    S0 = sum(k * m for k, m in xs0.items()); kmin = min(k for k in range(1, 401) if A[k] > 0)
    cap = S0 - (delta - 1) * kmin
    if len(A) <= cap:
        A = A + [0] * (cap + 1 - len(A))
        for n in range(1001, cap + 1):
            v = N[n] if n < len(N) else 0
            for j in range(1, min(n, len(D) - 1) + 1): v -= D[j] * A[n - j]
            A[n] = v // D[0]
    res, xs = solve(cap)
    feasible = sum(xs.values()) == delta and all(sum(m for k, m in xs.items() if k % r == 0) >= J2[r] for r in rs)
    # (3) leading constant: c = lim (1-t)^delta H = N(1) / (D/(1-t)^delta)(1)
    Dp = fmpz_poly(D)
    for _ in range(delta): Dp = Dp // fmpz_poly([1, -1])
    cconst = Fraction(sum(N), int(Dp(1)))
    msum = sum(k * m for k, m in xs.items())
    secondaries = cconst * prod(k ** m for k, m in xs.items())
    out[d] = {"generators_low_degree": [{"degree": n, "a_n": an, "decomposables_dim_lower": lo, "decomposables_dim_upper": hi,
                                         "g_n_lower": glo, "g_n_upper": ghi, "rule": rule} for n, an, lo, hi, glo, ghi, rule in rows],
              "hsop_min_sum": msum, "hsop_min_sum_degrees": {str(k): m for k, m in sorted(xs.items())},
              "hsop_degree_cap": cap, "hsop_solution_feasible_exact": feasible, "milp_status": res.message,
              "hsop_min_sum_status": "solver-computed (HiGHS MILP reports optimal); not independently certified",
              "hsop_max_degree_lower_bound": max(J2), "leading_constant": str(cconst), "secondaries_if_min_sum_hsop_exists": str(secondaries)}
    print(f"d = {d}: generators (n, a_n, g_n range, rule): {[(n, an, glo, ghi, rule) for n, an, lo, hi, glo, ghi, rule in rows]}")
    print(f"   hsop: degree cap {cap}; exact feasibility of the solution {feasible}; min sum of degrees {msum}; some hsop degree divisible by {max(J2)}; c = {float(cconst):.6e}; secondaries at min-sum degrees = {secondaries}")
dest = os.path.join(R, 'consequences.json')
if '--check' in sys.argv:
    same = json.load(open(dest)) == json.loads(json.dumps(out))
    print("consequences match data/consequences.json:", same); sys.exit(0 if same else 1)
json.dump(out, open(dest, 'w'), indent=1)
