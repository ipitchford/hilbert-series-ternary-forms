"""Independent cross-check: enumerate torsion t = (e^{2pi i a/n}, e^{2pi i b/n}) directly,
all level sets, exact kappa. Must never exceed poles.compute (upper-bound check) and should
attain it for every r (lower-bound check)."""
import json, sys
from math import gcd
from poles import weights, kappa
for d in map(int, sys.argv[1:]):
    W=weights(d); ours={int(k):v for k,v in json.load(open(f"results_d{d}.json")).items()}
    ns=set(range(1,41))|{m*r for r in ours for m in (1,2,3)}
    cache={}; brute={}
    for n in sorted(ns):
        for a in range(n):
            for b in range(n):
                groups={}
                for w in W: groups.setdefault((a*w[0]+b*w[1])%n,[]).append(w)
                for k,S in groups.items():
                    S=frozenset(S)
                    if S not in cache: cache[S]=kappa(S)
                    if cache[S]:
                        r=n//gcd(n,k); brute[r]=max(brute.get(r,0),cache[S])
    over=[r for r in brute if brute[r]>ours.get(r,0)]
    under=[r for r in ours if brute.get(r,0)!=ours[r]]
    print(d, "exceed:",over, "not attained:",under, "levelsets:",len(cache), flush=True)
