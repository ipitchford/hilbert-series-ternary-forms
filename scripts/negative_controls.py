"""Negative controls for certify_ternary.py: each deliberately corrupted input must be REJECTED (nonzero exit).
Every control is run WITH the out-of-sample prediction file, so a rejection is never due to a missing input.
The undersized-denominator controls lower the exponent of one Phi_r at an order where the bound is tight; the internal
checks alone cannot see this (any B reproduces a_0..a_{K/2}), and the out-of-sample prediction must reject it.
Usage: negative_controls.py   (run from scripts/; writes only to a temporary directory)"""
import json, os, subprocess, sys, tempfile
tmp = tempfile.mkdtemp()
cases = []
def case(name, d, grid, ref, mutate_grid=None, mutate_ref=None, extra=()):
    g = json.load(open(grid)); r = json.load(open(ref))
    if mutate_grid: mutate_grid(g)
    if mutate_ref: mutate_ref(r)
    gp, rp = os.path.join(tmp, name + '_grid.json'), os.path.join(tmp, name + '_ref.json')
    json.dump(g, open(gp, 'w')); json.dump(r, open(rp, 'w'))
    rc = subprocess.run([sys.executable, 'certify_ternary.py', str(d), gp, '--predict', PRED[d], '--reference', rp, *extra], capture_output=True, text=True).returncode
    cases.append((name, rc))
    print(f"{name}: exit {rc} -> {'REJECTED' if rc != 0 else 'ACCEPTED (control FAILED)'}")
def flip(g, i, n):
    p = g['primes'][i]; g['residues'][i][n] = str((int(g['residues'][i][n]) + 1) % p)
G8, R8 = '../data/octic/d8_L1194_p6.json', '../data/octic/d8_rational.json'
G9, R9 = '../data/nonic/d9_L690_p6.json', '../data/nonic/d9_rational.json'
PRED = {8: '../data/octic/d8_L1600_p31.json', 9: '../data/nonic/d9_L1000_p31.json'}
case('d8_flipped_residue', 8, G8, R8, mutate_grid=lambda g: flip(g, 4, 900))
case('d9_flipped_residue', 9, G9, R9, mutate_grid=lambda g: flip(g, 2, 500))
case('d9_wrong_degree_label', 9, G9, R9, mutate_grid=lambda g: g.__setitem__('d', 8))
case('d8_truncated_residues', 8, G8, R8, mutate_grid=lambda g: g['residues'][0].pop())
def tamper_N(r):
    r['N'][10] = str(int(r['N'][10]) + 1)
case('d9_tampered_reference', 9, G9, R9, mutate_ref=tamper_N)
case('d9_undersized_denominator_Phi11', 9, G9, R9, extra=('--drop-factor', '11'))
case('d8_undersized_denominator_Phi3', 8, G8, R8, extra=('--drop-factor', '3'))
# positive control: the unmodified inputs must be ACCEPTED, so the rejections above are not an artefact of the harness
rc8 = subprocess.run([sys.executable, 'certify_ternary.py', '8', G8, '--predict', PRED[8], '--reference', R8], capture_output=True).returncode
print(f"positive control (unmodified d = 8 inputs): exit {rc8} -> {'ACCEPTED' if rc8 == 0 else 'REJECTED (harness FAILED)'}")
ok = all(rc != 0 for _, rc in cases) and rc8 == 0
print('ALL NEGATIVE CONTROLS REJECTED:', ok)
sys.exit(0 if ok else 1)
