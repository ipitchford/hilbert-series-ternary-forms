"""End-to-end validation of the method on the known cases d = 5, 6 (Bedratyuk-Xin 2011).
Re-derives H_5 and H_6 with certify_ternary.py from fresh grid data (data/validation/d{5,6}_L*_p4.json) and checks that
they equal Bedratyuk-Xin's rational functions, i.e. numerators over prod(1 - t^k) with the published degrees."""
import json, os, subprocess, sys
from flint import fmpz_poly
here = os.path.dirname(os.path.abspath(__file__)); V = os.path.join(here, '..', 'data', 'validation')
DEN = {5: [6, 9, 12, 15, 18, 18, 21, 24, 27, 30, 33, 36, 48],
       6: [3, 4, 6, 6, 7, 7, 8, 9, 9, 10, 11, 12, 13, 15, 15, 16, 17, 19, 20, 25]}
nums = json.load(open(os.path.join(V, 'bx_numerators.json')))
ok = True
for d, f in [(5, 'd5_L160_p4.json'), (6, 'd6_L120_p4.json')]:
    r = subprocess.run([sys.executable, os.path.join(here, 'certify_ternary.py'), str(d), os.path.join(V, f)], capture_output=True, text=True)
    mine = json.load(open(os.path.join(V, f'd{d}_rational.json')))
    N = fmpz_poly([int(x) for x in mine['N']]); D = fmpz_poly(mine['D'])
    nb = nums['b%d' % d]; deg = max(int(k) for k in nb)
    Nb = fmpz_poly([nb.get(str(i), 0) for i in range(deg + 1)])
    Db = fmpz_poly([1])
    for k in DEN[d]: Db *= fmpz_poly([1] + [0] * (k - 1) + [-1])
    same = r.returncode == 0 and N * Db == Nb * D
    ok &= same
    print(f"d = {d}: re-derived by the method and equal to Bedratyuk-Xin's rational function: {same}")
    os.remove(os.path.join(V, f'd{d}_rational.json'))
print("VALIDATION ON KNOWN CASES PASSES:", ok); sys.exit(0 if ok else 1)
