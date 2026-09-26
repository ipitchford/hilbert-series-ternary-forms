"""Replay with explicitly labelled verification levels and a machine-readable receipt.

Modes (cumulative):
  archived  (default)  Checks performed on the archived data. It freshly runs our torus enumerator and all certificates,
                       re-lifts every archived residue array, and compares with the archived output of the blind torus
                       program. It does not regenerate any coefficient.
  fresh                Everything in 'archived', plus bounded fresh recomputation:
                       - the blind torus program, rerun in a temporary copy for d = 5..9;
                       - grid data for the d = 5, 6 validation, regenerated;
                       - the exact septic integers to degree 120;
                       - one fresh 62-bit grid prime for d = 8 to degree 200;
                       - weight counting mod 65497 for d = 8 and 9 to degree 60.
  full                 Everything in 'fresh', plus full regeneration, each output byte-compared with or re-certified
                       against the archive:
                       - the septic integers to degree 760;
                       - the six octic primes to degree 1194 and the six nonic primes to degree 690 (about 2 h);
                       - the 31-bit out-of-sample primes;
                       - the weight-counting runs.
Usage: python scripts/replay.py [archived|fresh|full]   (writes receipts/replay_<mode>_<time>.json; the producer's receipts are shipped as REPLAY_RECEIPT_*.json)"""
import hashlib, json, os, shutil, subprocess, sys, tempfile, time
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
MODE = sys.argv[1] if len(sys.argv) > 1 else 'archived'
LEVELS = {'archived': 0, 'fresh': 1, 'full': 2}
if MODE not in LEVELS: sys.exit(__doc__)
PY = sys.executable
steps = []
REDACT = [(PY, 'python'), (ROOT, '.')]   # receipts record portable commands, never local paths

def portable(text):
    for real, shown in REDACT: text = text.replace(real, shown)
    return text

def sha(path):
    return hashlib.sha256(open(os.path.join(ROOT, path), 'rb').read()).hexdigest() if os.path.exists(os.path.join(ROOT, path)) else None

def step(name, level, cmd, cwd='.', inputs=(), outputs=(), rng='', expect=None, shell=False):
    if LEVELS[level] > LEVELS[MODE]: return
    t0 = time.time()
    r = subprocess.run(cmd, cwd=os.path.join(ROOT, cwd), capture_output=True, text=True, shell=shell)
    tail = (r.stdout.strip().splitlines() or [''])[-1]
    ok = r.returncode == 0 and (expect is None or expect in r.stdout)
    steps.append({"name": name, "level": level, "command": portable(cmd if isinstance(cmd, str) else ' '.join(cmd)), "cwd": cwd,
                  "range": rng, "inputs": {p: sha(p) for p in inputs}, "outputs": {p: sha(p) for p in outputs},
                  "exit": r.returncode, "result": portable(tail), "seconds": round(time.time() - t0, 1), "passed": ok})
    print(f"[{level:8s}] {'PASS' if ok else 'FAIL'}  {name}: {tail}")
    if not ok:
        print(r.stdout[-2000:], r.stderr[-2000:]); finish(False)

def finish(ok):
    rec = {"mode": MODE, "passed": ok, "completedAt": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
           "python": sys.version.split()[0], "steps": steps}
    leaked = [x for x in (ROOT, os.path.expanduser('~')) if x in json.dumps(rec)]
    if leaked: print("receipt would record local paths:", leaked); rec["passed"] = ok = False
    os.makedirs(os.path.join(ROOT, 'receipts'), exist_ok=True)
    json.dump(rec, open(os.path.join(ROOT, 'receipts', f"replay_{MODE}_{rec['completedAt'].replace(':', '')}.json"), 'w'), indent=1)
    print("REPLAY", MODE.upper(), "PASSED" if ok else "FAILED"); sys.exit(0 if ok else 1)

cc = os.environ.get('CC') or next(c for c in ['gcc-16', 'gcc-15', 'gcc-14', 'gcc-13', 'gcc', 'clang']
                                   if shutil.which(c) and subprocess.run([c, '-fopenmp', '-x', 'c', '-', '-o', os.devnull], input='int main(){return 0;}', text=True, capture_output=True).returncode == 0)
if not os.access(os.path.join(ROOT, 'scripts'), os.W_OK): sys.exit('run on a writable copy')
check = 'sha256sum' if shutil.which('sha256sum') else 'shasum -a 256'
step('manifest before replay', 'archived', f'{check} -c MANIFEST.sha256 --quiet', shell=True, inputs=['MANIFEST.sha256'])
for src, cwd in [('mw5.c', 'scripts'), ('mw6.c', 'scripts'), ('methodAd.c', 'scripts'), ('methodA16.c', 'data/septic')]:
    step(f'build {src}', 'archived', [cc, '-O3', '-fopenmp', src, '-o', src[:-2]], cwd=cwd, inputs=[f'{cwd}/{src}'])
step('torus bounds: our enumerator (fresh) vs archived blind output, d = 5..9', 'archived',
     [PY, '-c', "import json,subprocess,sys\nok=True\nfor d in (5,6,7,8,9):\n subprocess.run([sys.executable,'pole_bounds.py',str(d)],check=True,capture_output=True)\n a={int(k):v[0] for k,v in json.load(open(f'pole_bounds_d{d}.json')).items() if v[0]>0}\n t=json.load(open(f'../independent/blind_torus_bounds/results_d{d}.json')); t=t.get('b_r',t)\n b={int(k):int(v) for k,v in t.items() if int(v)>0}\n ok&=a==b\nprint('TORUS BOUNDS AGREE:',ok); sys.exit(0 if ok else 1)"],
     cwd='scripts', inputs=['scripts/pole_bounds.py'] + [f'independent/blind_torus_bounds/results_d{d}.json' for d in (5, 6, 7, 8, 9)], rng='d = 5..9', expect='AGREE: True')
step('validation: method re-derives Bedratyuk-Xin H5, H6 from archived grid data', 'archived', [PY, 'check_validation.py'], cwd='scripts',
     inputs=['data/validation/d5_L160_p4.json', 'data/validation/d6_L120_p4.json', 'data/validation/bx_numerators.json'], expect='PASSES: True')
step('septic: re-lift of the 15 archived weight-counting arrays', 'archived', [PY, 'regenerate_exact.py', 'lift', '760'], cwd='data/septic',
     inputs=['data/septic/methodA_exact_760.json'], rng='n <= 760', expect='PASSES: True')
step('Theorem 1(1): septic certificate (bounds regenerated)', 'archived', [PY, 'certify_septic_unconditional.py'], cwd='scripts',
     inputs=['data/septic/d7_rational.json', 'data/septic/methodA_exact_760.json'], rng='n <= 708', expect='PASSES: True')
for d, g, ref, extra in [(8, 'data/octic/d8_L1194_p6.json', 'data/octic/d8_rational.json', ['data/octic/d8_L1600_p31.json', 'data/octic/wc_d8_N450_p65521.txt', 'data/octic/wc_d8_N450_p65519.txt']),
                         (9, 'data/nonic/d9_L690_p6.json', 'data/nonic/d9_rational.json', ['data/nonic/d9_L1000_p31.json', 'data/nonic/wc_d9_N400_p65521.txt', 'data/nonic/wc_d9_N400_p65519.txt'])]:
    step(f'Theorem 1({d-6}): re-lift six archived residue arrays, determine H_{d}, compare with reference', 'archived',
         [PY, 'certify_ternary.py', str(d), '../' + g, '--reference', '../' + ref], cwd='scripts', inputs=[g, ref], expect='PASSES: True')
    step(f'H_{d}: out-of-sample prediction and weight-counting agreement (archived residues)', 'archived',
         [PY, 'check_ternary_extra.py', str(d), '../' + ref] + ['../' + e for e in extra], cwd='scripts', inputs=[ref] + extra, expect='PASS: True')
step('negative controls: corrupted residues, wrong degree label, truncated array and tampered reference are all rejected', 'archived',
     [PY, 'negative_controls.py'], cwd='scripts', inputs=['data/octic/d8_L1194_p6.json', 'data/nonic/d9_L690_p6.json'], expect='REJECTED: True')
step('consequences (generators, hsop constraints, leading constants) recomputed and compared', 'archived', [PY, 'consequences.py', '--check'], cwd='scripts',
     inputs=['data/consequences.json'], expect='True')
step('research gates', 'archived', [PY, 'scripts/check_research_gates.py', '.'], inputs=['RESEARCH_GATES.json'], expect='"passed"')
# ---- fresh ----
tmp = tempfile.mkdtemp(); REDACT.insert(0, (tmp, '$TMP'))
step('blind torus program rerun (temporary copy), d = 5..9, compared with our enumerator', 'fresh',
     f'cp -R independent/blind_torus_bounds {tmp}/b && cd {tmp}/b && {PY} poles.py 5 6 7 8 9 > /dev/null && cd - > /dev/null && {PY} -c "import json,sys\nok=True\nfor d in (5,6,7,8,9):\n a={{int(k):v[0] for k,v in json.load(open(f\'scripts/pole_bounds_d{{d}}.json\')).items() if v[0]>0}}\n t=json.load(open(f\'{tmp}/b/results_d{{d}}.json\')); t=t.get(\'b_r\',t)\n b={{int(k):int(v) for k,v in t.items() if int(v)>0}}\n ok&=a==b\nprint(\'FRESH BLIND AGREES:\',ok); sys.exit(0 if ok else 1)"',
     shell=True, rng='d = 5..9', expect='AGREES: True')
step('validation grid data regenerated (d = 5: 4 primes to 160; d = 6: 4 primes to 120) and byte-compared', 'fresh',
     f'cd scripts && {PY} driver.py 5 160 4 {tmp}/d5.json > /dev/null 2>&1 && {PY} driver.py 6 120 4 {tmp}/d6.json > /dev/null 2>&1 && cmp {tmp}/d5.json ../data/validation/d5_L160_p4.json && cmp {tmp}/d6.json ../data/validation/d6_L120_p4.json && echo IDENTICAL',
     shell=True, expect='IDENTICAL')
step('septic weight counting regenerated to degree 120 (15 primes) and lifted', 'fresh', [PY, 'regenerate_exact.py', 'fresh', '120'], cwd='data/septic', rng='n <= 120', expect='PASSES: True')
step('fresh grid prime (d = 8, 62-bit, to degree 200) and weight counting mod 65497 (d = 8, 9, to 60) vs determined series', 'fresh',
     [PY, '-c', "import json,subprocess,sys\nfrom sympy import isprime\nok=True\nfor d,f in ((8,'../data/octic/d8_rational.json'),(9,'../data/nonic/d9_rational.json')):\n R=json.load(open(f)); D=[int(x) for x in R['D']]; N=[int(x) for x in R['N']]\n L=200; a=[0]*(L+1)\n for n in range(L+1):\n  v=N[n] if n<len(N) else 0\n  for j in range(1,min(n,len(D)-1)+1): v-=D[j]*a[n-j]\n  a[n]=v//D[0]\n if d==8:\n  M=2*(8*L+2)+1; q=(2**62-12345)//M\n  while not isprime(q*M+1): q-=1\n  p=q*M+1; out=subprocess.run(['./mw5','8',str(L),str(p),str(M)],capture_output=True,text=True,check=True).stdout.split()\n  ok&=all(a[n]%p==int(out[n]) for n in range(L+1))\n wc=subprocess.run(['./methodAd',str(d),'60','65497'],capture_output=True,text=True,check=True).stdout.split('\\n')\n ok&=all(a[int(l.split()[0])]%65497==int(l.split()[1]) for l in wc if l.strip())\nprint('FRESH SPOT CHECKS:',ok); sys.exit(0 if ok else 1)"],
     cwd='scripts', rng='grid n <= 200; weight counting n <= 60', expect='CHECKS: True')
# ---- full ----
step('septic weight counting regenerated to degree 760 (15 primes), byte-compared and lifted', 'full', [PY, 'regenerate_exact.py', 'fresh', '760'], cwd='data/septic', rng='n <= 760', expect='PASSES: True')
for d, L, out in [(8, 1194, 'data/octic/d8_L1194_p6.json'), (9, 690, 'data/nonic/d9_L690_p6.json')]:
    step(f'd = {d}: six 62-bit primes regenerated to degree {L} and byte-compared with the archive', 'full',
         f'cd scripts && {PY} driver.py {d} {L} 6 {tmp}/g{d}.json > /dev/null 2>&1 && cmp {tmp}/g{d}.json ../{out} && echo IDENTICAL', shell=True, rng=f'n <= {L}', expect='IDENTICAL')
for d, L, out in [(8, 1600, 'data/octic/d8_L1600_p31.json'), (9, 1000, 'data/nonic/d9_L1000_p31.json')]:
    step(f'd = {d}: 31-bit out-of-sample prime regenerated to degree {L} and compared', 'full',
         f'cd scripts && {PY} run32.py {d} {L} 1 {tmp}/o{d}.json > /dev/null 2>&1 && {PY} -c "import json;a=json.load(open(\'{tmp}/o{d}.json\'));b=json.load(open(\'../{out}\'));print(\'IDENTICAL\' if a[\'residues\']==b[\'residues\'] and a[\'primes\']==b[\'primes\'] else \'DIFFERENT\')"',
         shell=True, rng=f'n <= {L}', expect='IDENTICAL')
for d, N, folder in [(8, 450, 'octic'), (9, 400, 'nonic')]:
    for p in (65521, 65519):
        step(f'd = {d}: weight counting mod {p} regenerated to degree {N} and byte-compared', 'full',
             f'cd scripts && ./methodAd {d} {N} {p} > {tmp}/w.txt && cmp {tmp}/w.txt ../data/{folder}/wc_d{d}_N{N}_p{p}.txt && echo IDENTICAL', shell=True, rng=f'n <= {N}', expect='IDENTICAL')
for f in os.listdir(os.path.join(ROOT, 'scripts')):
    if f.startswith('pole_bounds_d') and f.endswith('.json'): os.remove(os.path.join(ROOT, 'scripts', f))
step('manifest after replay: no shipped file was modified', 'archived', f'{check} -c MANIFEST.sha256 --quiet', shell=True)
finish(all(s['passed'] for s in steps))
