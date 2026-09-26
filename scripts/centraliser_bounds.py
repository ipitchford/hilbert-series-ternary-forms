"""Centraliser-refined pole-order bounds for H(C[S^d C^3]^SL3, t) (paper Remark 9, refining Lemma 7).

For a torus element t and a primitive r-th root zeta, the piece pi(V_{S(t)}) of the fixed locus X^zeta is the image of
V_S under the quotient map, which is invariant under the centraliser Z = Z_G(t) (Z preserves V_S). So pi|V_S factors
through V_S//Z, and
    dim pi(V_S) <= min( dim V_S//T , dim V_S//Z ) <= min( kappa(S), dim V_S - (generic Z-orbit dimension on V_S) ),
the last step by Rosenlicht (trdeg C(V_S)^Z = dim V_S - max orbit dim, and C[V_S]^Z lies in C(V_S)^Z).
Z = T when t has three distinct eigenvalues. When two eigenvalues coincide, Z ~ GL2 acting on the corresponding pair of
variables, and the third variable by det^{-1}. The generic orbit dimension is at least the rank, modulo a prime P, of
the four gl2 derivatives at one random point of V_S (a specialisation can only lower the rank), so the bound is rigorous.

Enumeration (exhaustive, as in pole_bounds.py). A level set S = W ∩ phi^{-1}(zeta) of rank(S - S) = 2 has
phi(x, y) = omega^(c x + e y) with omega a primitive N-th root, N <= Nmax. With (u, v) = (t1/t3, t2/t3) = (omega^c, omega^e):
t1 = t3 iff c = 0 mod N; t2 = t3 iff e = 0; t1 = t2 iff c = e. These are the singular ('wall') cases. For r >= 2, a level set of
rank <= 1 lies in a line class {k u0 : k = rho mod M}, which is realised by an element with three distinct eigenvalues (generic
transverse value). So the torus bound kappa is kept there.
b_r(refined) = max over all level sets of the bound above; b_1 is unchanged (the refinement is for r >= 2).
Usage: centraliser_bounds.py d [d ...]   writes centraliser_bounds_d{d}.json and prints the comparison with pole_bounds."""
import sys, json, random
from math import gcd
from fractions import Fraction
from itertools import combinations
from sympy import divisors
P = (1 << 61) - 1

def weights(d): return [(a, b, d - a - b) for a in range(d + 1) for b in range(d + 1 - a)]
def red(m): return (m[0] - m[2], m[1] - m[2])

def in_cone(v, S):
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

def gl2_rank(mons, i, j, rng):
    """Rank mod P of the gl2 (variables i, j; third variable k scaled by -trace) derivatives at a random f in span(mons)."""
    k = 3 - i - j
    coef = {m: rng.randrange(1, P) for m in mons}
    rows = []
    for (p, q) in [(i, i), (i, j), (j, i), (j, j)]:
        # E_pq acts on f by x_q * d/dx_p, and on x_k by -tr(E) (tr = 1 if p == q)
        out = {}
        for m, c in coef.items():
            if m[p] > 0:
                n = list(m); n[p] -= 1; n[q] += 1; n = tuple(n)
                out[n] = (out.get(n, 0) + c * m[p]) % P
            if p == q and m[k] > 0:
                out[m] = (out.get(m, 0) - c * m[k]) % P
        rows.append(out)
    cols = sorted({n for r in rows for n in r})
    M = [[r.get(n, 0) for n in cols] for r in rows]
    rk = 0
    for c in range(len(cols)):
        piv = next((x for x in range(rk, len(M)) if M[x][c]), None)
        if piv is None: continue
        M[rk], M[piv] = M[piv], M[rk]; inv = pow(M[rk][c], P - 2, P)
        M[rk] = [v * inv % P for v in M[rk]]
        for x in range(len(M)):
            if x != rk and M[x][c]:
                f = M[x][c]; M[x] = [(a - f * b) % P for a, b in zip(M[x], M[rk])]
        rk += 1
    return rk

def run(d):
    rng = random.Random(20260926 + d)
    Wm = weights(d); W = [red(m) for m in Wm]; mon = dict(zip(W, Wm))
    torus, refined, witness = {}, {}, {}
    def rec(tab, r, k, info):
        if k > tab.get(r, -1):
            tab[r] = k
            if tab is refined: witness[r] = info
    diffs = {(p[0] - q[0], p[1] - q[1]) for p in W for q in W}
    Nmax = max(abs(u[0] * v[1] - u[1] * v[0]) for u in diffs for v in diffs)
    zcache = {}
    for N in range(1, Nmax + 1):
        for c in divisors(N):
            for e in range(N):
                if gcd(gcd(c, e), N) != 1: continue
                wall = [(0, 2)] if c % N == 0 else []
                if e % N == 0: wall.append((1, 2))
                if (c - e) % N == 0: wall.append((0, 1))
                groups = {}
                for w in W: groups.setdefault((c * w[0] + e * w[1]) % N, []).append(w)
                for q, S in groups.items():
                    if len(S) < 2 or rank([(s[0] - S[0][0], s[1] - S[0][1]) for s in S]) != 2: continue
                    r = N // gcd(q, N); kp = kappa(S)
                    rec(torus, r, kp, None)
                    b = kp
                    if wall and r >= 2 and kp > 0:
                        key = (tuple(sorted(S)), tuple(wall))
                        if key not in zcache:
                            zcache[key] = min(len(S) - gl2_rank([mon[s] for s in S], i, j, rng) for (i, j) in wall)
                        b = min(kp, zcache[key])
                    rec(refined, r, b, ('rank2', N, c, e, 'wall' if wall else 'regular', len(S), kp))
    dirs = set()
    for w in W:
        if w == (0, 0): continue
        g = gcd(abs(w[0]), abs(w[1])); u = (w[0] // g, w[1] // g)
        dirs.add(u if u > (0, 0) else (-u[0], -u[1]))
    for u in dirs:
        pts = {(w[0] // u[0] if u[0] else w[1] // u[1]): w for w in W if w[0] * u[1] - w[1] * u[0] == 0}
        K = sorted(pts)
        for M in range(1, 2 * max(abs(k) for k in K) + 2):
            for rho in range(M):
                S = [pts[k] for k in K if k % M == rho]
                if len(S) >= 2:
                    r = M // gcd(M, rho); kp = kappa(S)
                    rec(torus, r, kp, None); rec(refined, r, kp, ('line', u, M, rho, len(S)))
    if (0, 0) in W:
        rec(torus, 1, kappa([(0, 0)]), None); rec(refined, 1, kappa([(0, 0)]), ('zero',))
    refined[1] = torus[1]
    out = {'d': d, 'Nmax': Nmax, 'torus': {str(r): torus[r] for r in sorted(torus) if torus[r] > 0},
           'refined': {str(r): refined[r] for r in sorted(refined) if refined[r] > 0},
           'witness': {str(r): witness.get(r) for r in sorted(refined) if refined[r] > 0}}
    json.dump(out, open(f'centraliser_bounds_d{d}.json', 'w'), indent=1, default=str)
    return out

def true_multiplicities(d):
    """Multiplicity of Phi_r in the least denominator: Bedratyuk-Xin (d = 5, 6), determined series (d = 7, 8, 9)."""
    import os
    from flint import fmpz_poly
    data = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
    if d in (7, 8, 9):
        f = {7: 'septic/d7_denominator.json', 8: 'octic/d8_rational.json', 9: 'nonic/d9_rational.json'}[d]
        return {int(r): m for r, m in json.load(open(os.path.join(data, f)))['cyclotomic'].items() if m > 0}
    DEN = {5: [6, 9, 12, 15, 18, 18, 21, 24, 27, 30, 33, 36, 48],
           6: [3, 4, 6, 6, 7, 7, 8, 9, 9, 10, 11, 12, 13, 15, 15, 16, 17, 19, 20, 25]}[d]
    nb = json.load(open(os.path.join(data, 'validation', 'bx_numerators.json')))['b%d' % d]
    N = fmpz_poly([int(nb.get(str(i), 0)) for i in range(max(int(k) for k in nb) + 1)])
    out = {}
    for r in range(1, max(DEN) + 1):
        m = sum(1 for k in DEN if k % r == 0)
        if not m: continue
        c, Nq = 0, N
        while Nq % fmpz_poly.cyclotomic(r) == 0: Nq = Nq // fmpz_poly.cyclotomic(r); c += 1
        if m - c > 0: out[r] = m - c
    return out

if __name__ == '__main__':
    allok = True
    for d in [int(x) for x in sys.argv[1:]] or [5, 6, 7, 8, 9]:
        o = run(d); delta = (d + 1) * (d + 2) // 2 - 8
        tor = {int(r): min(delta, v) for r, v in o['torus'].items()}; ref = {int(r): min(delta, v) for r, v in o['refined'].items()}
        true = true_multiplicities(d)
        ok = all(ref.get(r, 0) >= m for r, m in true.items()) and all(ref[r] <= tor.get(r, 0) for r in ref)
        allok &= ok
        ex_t = sorted(r for r in tor if tor[r] > true.get(r, 0)); ex_r = sorted(r for r in ref if ref[r] > true.get(r, 0))
        print(f'd = {d}: refined >= true multiplicity everywhere and <= torus bound: {ok}; '
              f'orders with excess: torus {ex_t}, refined {ex_r}')
    print('CENTRALISER BOUNDS CONSISTENT:', allok); sys.exit(0 if allok else 1)
