# Replay receipt

- **Date (UTC):** 2026-09-26T12:49:14Z.
- **Machine:** macOS 27.0, Apple M2 (8 cores, 16 GB); gcc-16 16.1.0; Python 3.13.5; python-flint 0.9.0; sympy 1.14.0.
- **Replayed bytes:** a fresh `git archive` extraction of commit `5bfb81f`. Since then only this receipt and `MANIFEST.sha256` have changed.
- **Command:** `FULL=1 PY=<python> ./replay.sh` (121 s). The main certificates also pass under `python -O`.
- **Result:** exit status 0; every stage passed.

```
== environment
3.13.5 python-flint 0.9.0 sympy 1.14.0
gcc-16 (Homebrew GCC 16.1.0) 16.1.0
== manifest
MANIFEST OK
== build
built
built-septic
== torus bounds (Derksen Thm 3.4 + 5.1), our enumeration vs the blind program, d = 5..9
  d = 5: identical True
  d = 6: identical True
  d = 7: identical True
  d = 8: identical True
  d = 9: identical True
TORUS BOUNDS AGREE: True
== validation: the method re-derives Bedratyuk-Xin's d = 5, 6
VALIDATION ON KNOWN CASES PASSES: True
== septic exact integers
lifted a_0..a_760; in range [0, C(n+35,35)]: True; equals methodA_exact_760.json on n <= 760: True
EXACT REGENERATION CHECK PASSES: True
lifted a_0..a_120; in range [0, C(n+35,35)]: True; equals methodA_exact_760.json on n <= 120: True
EXACT REGENERATION CHECK PASSES: True
EXACT REGENERATION CHECK PASSES: True
== Theorem 1 (septics, unconditional)
UNCONDITIONAL SEPTIC CERTIFICATE PASSES: True
== Theorem 2 (octics)
d = 8 DETERMINATION PASSES: True
d = 8 EXTRA CHECKS PASS: True
== Theorem 2 (nonics)
d = 9 DETERMINATION PASSES: True
d = 9 EXTRA CHECKS PASS: True
== fresh spot recomputation: grid engine, d = 8, one 62-bit prime to t^200, and weight counting to t^60
  fresh grid prime 4611686018427250891: agrees True; fresh weight counting mod 65497: agrees True
SPOT RECOMPUTATION PASSES: True
== research gates
RESEARCH GATES: passed
== manifest again (no shipped file modified)
MANIFEST STILL OK
REPLAY COMPLETED
```
