"""Rigorous upper bounds b_r >= (pole order of H(C[S^d C^3]^SL3, t) at primitive r-th roots of unity).

Chain (paper Lemmas 5-7): pole order at zeta <= dim X^zeta (Lemma 5), X = V//G; X^zeta = union over torus elements t of
pi(V_S), S = {w in W : chi_w(t) = zeta} (Lemma 6); dim pi(V_S) <= dim V_S//T = kappa(S) (Lemma 7);
kappa(S) = |S0| - rank(S0), S0 = {w in S : -w in cone(S)}.
Level sets S = W ∩ phi^{-1}(zeta) for a homomorphism phi: Z^2 -> C^*. Cases:
 (i) rank(S - S) = 2: ker(phi) has finite index N <= max|det| of two weight differences, Z^2/ker cyclic, r = order of w0.
 (ii) rank(S - S) = 1: S lies on an affine line; kappa = 0 unless the line passes through 0, handled by enumeration.
 (iii) |S| = 1: kappa = 0.
Usage: pole_bounds.py d"""
import sys, json
from math import gcd
from fractions import Fraction
from itertools import combinations
from sympy import divisors
d = int(sys.argv[1]) if len(sys.argv) > 1 else 7
W = [(a - c, b - c) for a in range(d + 1) for b in range(d + 1 - a) for c in [d - a - b]]

def in_cone(v, S):
    """v in cone(S) (nonneg combination), exact, 2D (Caratheodory: <= 2 generators)."""
    if v == (0, 0): return True
    for s in S:
        if s[0] * v[1] - s[1] * v[0] == 0 and s[0] * v[0] + s[1] * v[1] > 0: return True
    for s, t in combinations(S, 2):
        det = s[0] * t[1] - s[1] * t[0]
        if det == 0: continue
        l1 = Fraction(v[0] * t[1] - v[1] * t[0], det); l2 = Fraction(s[0] * v[1] - s[1] * v[0], det)
        if l1 >= 0 and l2 >= 0: return True
    return False

def rank(S):
    nz = [s for s in S if s != (0, 0)]
    if not nz: return 0
    b = nz[0]
    return 2 if any(b[0] * s[1] - b[1] * s[0] for s in nz) else 1

def kappa(S):
    S0 = [w for w in S if in_cone((-w[0], -w[1]), S)]
    return len(S0) - rank(S0) if S0 else 0

best = {}
def rec(r, k, info):
    if k > best.get(r, (-1,))[0]: best[r] = (k,) + info

# (i) rank-2 level sets
diffs = {(p[0] - q[0], p[1] - q[1]) for p in W for q in W}
Nmax = max(abs(u[0] * v[1] - u[1] * v[0]) for u in diffs for v in diffs)
seen = set()
for N in range(1, Nmax + 1):
    for c in divisors(N):
        for e in range(N):
            if gcd(gcd(c, e), N) != 1: continue
            groups = {}
            for w in W: groups.setdefault((c * w[0] + e * w[1]) % N, []).append(w)
            sig = (N, tuple(sorted((tuple(sorted(S)), N // gcd(q, N)) for q, S in groups.items())))
            if sig in seen: continue
            seen.add(sig)
            for q, S in groups.items():
                if len(S) >= 2 and rank([(s[0] - S[0][0], s[1] - S[0][1]) for s in S]) == 2:
                    rec(N // gcd(q, N), kappa(S), ('rank2', N, c, e, len(S)))
# (ii) rank-1 level sets on lines through the origin (other lines give kappa = 0)
dirs = set()
for w in W:
    if w == (0, 0): continue
    g = gcd(abs(w[0]), abs(w[1])); u = (w[0] // g, w[1] // g)
    dirs.add(u if u > (0, 0) else (-u[0], -u[1]))
for u in dirs:
    pts = {(w[0] // u[0] if u[0] else w[1] // u[1]): w for w in W if w[0] * u[1] - w[1] * u[0] == 0}
    K = sorted(pts)
    for M in range(1, 2 * max(abs(k) for k in K) + 2):      # z = phi(u) of order M; points in S share k mod M
        for rho in range(M):
            S = [pts[k] for k in K if k % M == rho]
            if len(S) >= 2:
                rec(M // gcd(M, rho), kappa(S), ('line', u, M, rho, len(S)))
if (0, 0) in W: rec(1, kappa([(0, 0)]), ('zero',))
json.dump({str(r): list(v) for r, v in sorted(best.items())}, open(f'pole_bounds_d{d}.json', 'w'), default=str)
print(f"d = {d}: |W| = {len(W)}, Nmax = {Nmax}, rank-2 lattices examined = {len(seen)}")
print({r: best[r][0] for r in sorted(best) if best[r][0] > 0})
