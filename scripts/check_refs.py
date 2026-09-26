"""Gate: every 'Theorem N', 'Proposition N', 'Lemma N' or 'Remark N' cited outside the paper must exist, with that
type, in the compiled paper (paper/paper.aux). Numbers written with a dot (e.g. 'Theorem 3.7' of a cited work) are
not references to this paper and are ignored. Ranges such as 'Lemmas 5-8' are checked at both ends.
Usage: check_refs.py [extra files ...]   (run from the package root or scripts/)"""
import json, os, re, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
aux = open(os.path.join(ROOT, 'paper', 'paper.aux')).read()
KIND = {'thm': 'Theorem', 'prop': 'Proposition', 'lem': 'Lemma', 'rem': 'Remark'}
have = {}
for lab, num in re.findall(r'\\newlabel\{(\w+):[^}]*\}\{\{(\d+)\}', aux):
    if lab in KIND: have.setdefault(KIND[lab], set()).add(int(num))
files = ['README.md', 'AI_INDEX.md', 'CLAIMS.json', 'RESEARCH_GATES.json', 'PRIOR_ART.md', 'PRE-REGISTERED.md', 'data/README.md']
files += [os.path.join('review', f) for f in sorted(os.listdir(os.path.join(ROOT, 'review'))) if f.endswith('.md') and 'v0.2' in f]
files += [os.path.join('scripts', f) for f in sorted(os.listdir(os.path.join(ROOT, 'scripts'))) if f.endswith(('.py', '.c')) and f != 'check_refs.py']
files += sys.argv[1:]
pat = re.compile(r'\b(Theorem|Proposition|Lemma|Remark)s?\s+(\d+)(?![.\d])(?:\s*(?:-|\u2013|--|and|,|to)\s*(\d+)(?![.\d]))?')
bad = []
for f in files:
    p = f if os.path.isabs(f) else os.path.join(ROOT, f)
    if not os.path.exists(p): continue
    for i, line in enumerate(open(p, encoding='utf-8', errors='replace'), 1):
        for kind, a, b in pat.findall(line):
            for n in [a] + ([b] if b else []):
                if int(n) not in have.get(kind, set()): bad.append(f"{f}:{i}: {kind} {n}")
print('paper numbering:', {k: sorted(v) for k, v in have.items()})
for x in bad: print('dangling reference:', x)
print('CROSS-REFERENCES VALID:', not bad); sys.exit(0 if not bad else 1)
