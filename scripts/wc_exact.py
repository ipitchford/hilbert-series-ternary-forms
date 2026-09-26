"""Second-algorithm exact determination of the octic and nonic coefficients by weight counting (methodAd2).

Weight counting (Proposition 4) is run modulo enough 16-bit primes that their product exceeds 2*C(N+dimV-1, dimV-1),
an upper bound for a_n. The residues are lifted by CRT, and the lifted integers are required to lie in [0, C(n+dimV-1, dimV-1)]
and to EQUAL the grid-engine coefficients (Proposition 3) for every n <= N. The two algorithms share no code.

Usage:
  wc_exact.py run d N        run ./methodAd2 d N p for the chosen primes; store ../data/<folder>/wc_exact/*.txt
  wc_exact.py fresh d N      run into a temporary directory, require byte-identical outputs to the archive, then lift
  wc_exact.py lift d N [DIR] CRT-lift the stored outputs and compare with the grid coefficients
Exit status 0 only if every check passes."""
import json, os, subprocess, sys, tempfile, filecmp
from math import comb, prod
from sympy import isprime, prevprime
from sympy.ntheory.modular import crt
HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = {8: 'octic', 9: 'nonic'}
GRID = {8: 'd8_L1194_p6.json', 9: 'd9_L690_p6.json'}
def dimV(d): return (d + 1) * (d + 2) // 2
def primes_for(d, N):
    need = 2 * comb(N + dimV(d) - 1, dimV(d) - 1); ps = []; p = 65536
    while prod(ps) <= need: p = prevprime(p); ps.append(p)
    return ps
def outdir(d): return os.path.join(HERE, '..', 'data', FOLDER[d], 'wc_exact')
def path(D, d, N, p): return os.path.join(D, f'wc_d{d}_N{N}_p{p}.txt')
def run(d, N, D):
    os.makedirs(D, exist_ok=True)
    for p in primes_for(d, N):
        out = subprocess.run([os.path.join(HERE, 'methodAd2'), str(d), str(N), str(p)], check=True, capture_output=True, text=True).stdout
        open(path(D, d, N, p), 'w').write(out); print(f'd={d} N={N} p={p}: stored', flush=True)
def lift(d, N, D):
    ps = primes_for(d, N); ok = True; res = []
    for p in ps:
        f = path(D, d, N, p)
        if not os.path.exists(f): print('missing', os.path.basename(f)); return False
        vals = {int(a): int(b) for a, b in (l.split() for l in open(f) if l.strip())}
        ok &= sorted(vals) == list(range(N + 1)) and all(0 <= v < p for v in vals.values()); res.append(vals)
    need = 2 * comb(N + dimV(d) - 1, dimV(d) - 1)
    print(f'd = {d}: {len(ps)} distinct 16-bit primes; modulus {prod(ps).bit_length()} bits > 2*C(N+{dimV(d)-1},{dimV(d)-1}) ({need.bit_length()} bits): {prod(ps) > need}')
    a = []
    for n in range(N + 1):
        x = int(crt(ps, [r[n] for r in res])[0]); ok &= 0 <= x <= comb(n + dimV(d) - 1, dimV(d) - 1); a.append(x)
    grid = [int(c) for c in json.load(open(os.path.join(HERE, '..', 'data', FOLDER[d], GRID[d])))['coeffs']]
    same = a == grid[:N + 1]
    print(f'lifted a_0..a_{N} in range: {ok}; equal to the grid-engine coefficients for every n <= {N}: {same}')
    allok = ok and same and prod(ps) > need
    print(f'd = {d} SECOND-ALGORITHM EXACT AGREEMENT PASSES: {allok}')
    return allok
if __name__ == '__main__':
    cmd, d, N = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    if cmd == 'run': run(d, N, outdir(d))
    elif cmd == 'lift': sys.exit(0 if lift(d, N, sys.argv[4] if len(sys.argv) > 4 else outdir(d)) else 1)
    elif cmd == 'fresh':
        T = tempfile.mkdtemp(); run(d, N, T)
        same = all(filecmp.cmp(path(T, d, N, p), path(outdir(d), d, N, p), shallow=False) for p in primes_for(d, N))
        print(f'fresh outputs byte-identical to the archived wc_exact files: {same}')
        sys.exit(0 if (lift(d, N, T) and same) else 1)
    else: sys.exit(__doc__)
