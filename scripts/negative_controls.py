"""Negative controls for certify_ternary.py: each deliberately corrupted input must be REJECTED (nonzero exit).
Usage: negative_controls.py   (run from scripts/; writes only to a temporary directory)"""
import json, os, subprocess, sys, tempfile
tmp = tempfile.mkdtemp()
cases = []
def case(name, d, grid, ref, mutate_grid=None, mutate_ref=None):
    g = json.load(open(grid)); r = json.load(open(ref))
    if mutate_grid: mutate_grid(g)
    if mutate_ref: mutate_ref(r)
    gp, rp = os.path.join(tmp, name + '_grid.json'), os.path.join(tmp, name + '_ref.json')
    json.dump(g, open(gp, 'w')); json.dump(r, open(rp, 'w'))
    rc = subprocess.run([sys.executable, 'certify_ternary.py', str(d), gp, '--reference', rp], capture_output=True, text=True).returncode
    cases.append((name, rc))
    print(f"{name}: exit {rc} -> {'REJECTED' if rc != 0 else 'ACCEPTED (control FAILED)'}")
def flip(g, i, n):
    p = g['primes'][i]; g['residues'][i][n] = str((int(g['residues'][i][n]) + 1) % p)
G8, R8 = '../data/octic/d8_L1194_p6.json', '../data/octic/d8_rational.json'
G9, R9 = '../data/nonic/d9_L690_p6.json', '../data/nonic/d9_rational.json'
case('d8_flipped_residue', 8, G8, R8, mutate_grid=lambda g: flip(g, 4, 900))
case('d9_flipped_residue', 9, G9, R9, mutate_grid=lambda g: flip(g, 2, 500))
case('d9_wrong_degree_label', 9, G9, R9, mutate_grid=lambda g: g.__setitem__('d', 8))
case('d8_truncated_residues', 8, G8, R8, mutate_grid=lambda g: g['residues'][0].pop())
def tamper_N(r):
    r['N'][10] = str(int(r['N'][10]) + 1)
case('d9_tampered_reference', 9, G9, R9, mutate_ref=tamper_N)
ok = all(rc != 0 for _, rc in cases)
print('ALL NEGATIVE CONTROLS REJECTED:', ok)
sys.exit(0 if ok else 1)
