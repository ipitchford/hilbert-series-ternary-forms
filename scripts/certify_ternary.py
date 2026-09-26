"""Determine and certify H_d(t), the Hilbert series of C[S^d C^3]^SL3.
Usage: certify_ternary.py d grid.json --predict grid31.json [--predict ...] [--reference rational.json] [--write out.json]
       certify_ternary.py d grid.json --no-predict ...     (validation on known cases only: d = 5, 6)
The grid file must contain the raw per-prime residue arrays ('residues'); the script CRT-lifts them itself, checks every
congruence, array length, prime, M and the coefficient bound, and (with --reference) compares the determined rational
function with an immutable reference file. Nothing is written unless --write is given, and only after all checks pass.
The out-of-sample prediction is part of the pass/fail: the internal checks cannot detect an undersized denominator
bound B (any B yields a function reproducing a_0..a_{K/2}), so the determined function must also predict the residues of
at least one further prime file (run32.py; a different prime and grid size) beyond the data used.
--drop-factor r (negative controls only) lowers the exponent of Phi_r in B by one; the run must then FAIL.
Inputs: pole-order bounds b_r (pole_bounds.py d; Lemmas 5-8 of the paper); exact a_n for n <= floor(K/2) from grid residues
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
args = sys.argv[1:]
def opt(name):
    if name in args: i = args.index(name); v = args[i + 1]; del args[i:i + 2]; return v
    return None
reference = opt('--reference'); writeto = opt('--write'); drop = opt('--drop-factor')
predicts = []
while '--predict' in args: predicts.append(opt('--predict'))
no_predict = '--no-predict' in args
if no_predict: args.remove('--no-predict')
d = int(args[0]); gridfile = args[1]
subprocess.run([sys.executable, PB, str(d)], cwd=here, check=True, capture_output=True)
b = {int(k): v[0] for k, v in json.load(open(os.path.join(here, f'pole_bounds_d{d}.json'))).items()}
dimV = (d + 1) * (d + 2) // 2; delta = dimV - 8
p = {r: min(delta, k) for r, k in b.items() if k > 0}
if drop is not None:
    p[int(drop)] -= 1; print(f"NEGATIVE CONTROL: exponent of Phi_{drop} in B lowered to {p[int(drop)]}")
B = fmpz_poly([1])
for r, e in p.items():
    for _ in range(e): B *= fmpz_poly.cyclotomic(r)
if B[0] < 0: B = -B
K = B.degree() - dimV; half = K // 2
sB = 1 if int(B[B.degree()]) == int(B[0]) else -1
eps = (-1) ** delta * sB
g = json.load(open(gridfile))
primes, M, L = g['primes'], g['M'], g['L']
meta = (int(g['d']) == d and len(set(primes)) == len(primes) and all(isprime(q) and (q - 1) % M == 0 for q in primes)
        and M > d * L + 4 and L >= half and 'residues' in g and len(g['residues']) == len(primes)
        and all(len(r) == L + 1 for r in g['residues']))
if not meta: sys.exit(f"grid file metadata invalid (degree label, primes, M, residue arrays): {gridfile}")
from sympy.ntheory.modular import crt
res = [[int(x) for x in r] for r in g['residues']]
a = [int(crt(primes, [r[n] for r in res])[0]) for n in range(L + 1)]
congruent = all(a[n] % q == res[k][n] % q for k, q in enumerate(primes) for n in range(L + 1))
matches_stored = 'coeffs' not in g or [int(x) for x in g['coeffs']] == a
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
result = {"d": d, "D": [int(D[i]) for i in range(D.degree() + 1)], "N": [str(int(N[i])) for i in range(N.degree() + 1)],
          "cyclotomic": {str(r): c for r, c in cyc.items()}, "bound_degree": B.degree(), "K": K, "eps": eps}
ref_ok = True
if reference:
    ref = json.load(open(reference))
    ref_ok = ref['D'] == result['D'] and ref['N'] == result['N'] and int(ref['d']) == d
print(f"B: {len(p)} orders, deg {B.degree()}; K = {K}; eps = {eps:+d}; coefficients used 0..{half} (have {L})")
print(f"grid metadata valid: {meta}; lifted a_n in range and modulus {mod.bit_length()} bits > 2*C(K/2+dimV-1,dimV-1): {bounds_ok}")
print(f"least denominator degree {D.degree()}, numerator degree {N.degree()}; pole order at 1 = {m1} (Krull dim {delta})")
print(f"series of N/D reproduces a_0..a_{half}: {reproduces}; coefficients nonnegative to t^{L}: {nonneg}")
print("cyclotomic multiplicities:", cyc)
print(f"re-lifted a_n from {len(primes)} raw residue arrays: every congruence holds {congruent}; equals the stored lifted list {matches_stored}")
if reference: print(f"determined rational function equals the reference {os.path.basename(reference)}: {ref_ok}")
goods = []
for f in predicts:
    h = json.load(open(f)); q = h['primes'][0]; Lq = h['L']; rq = [int(x) for x in h['residues'][0]]
    sq = [0] * (Lq + 1)
    for n in range(Lq + 1):
        v = Nl[n] if n < len(Nl) else 0
        for j in range(1, min(n, len(Dl) - 1) + 1): v -= Dl[j] * sq[n - j]
        sq[n] = v // Dl[0]
    good = isprime(q) and (q - 1) % h['M'] == 0 and h['M'] > d * Lq + 4 and Lq > half and all(sq[n] % q == rq[n] for n in range(Lq + 1))
    print(f"out-of-sample prediction: prime {q}, M = {h['M']}, determined H agrees for every n <= {Lq} (data used: n <= {half}): {good}")
    goods.append(good)
pred_ok = no_predict or (len(goods) > 0 and all(goods))
if not predicts and not no_predict: print("no --predict file given: the determination is not certified")
ok = meta and bounds_ok and reproduces and m1 == delta and nonneg and congruent and matches_stored and ref_ok and pred_ok
if ok and writeto: json.dump(result, open(writeto, 'w'))
print(f"d = {d} DETERMINATION PASSES:", ok); sys.exit(0 if ok else 1)
