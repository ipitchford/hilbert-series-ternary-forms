# The Hilbert series of the invariants of ternary septics, octics and nonics

This is an **unrefereed candidate**, version 0.2.0-candidate, dated 26 September 2026. The creator is Anonymous and the publisher is Evidence Press. It follows version 0.1.0-candidate (doi:10.5281/zenodo.22974308), which is immutable. This bundle is prepared for external review and is **not yet published**.

The paper is [paper/paper.pdf](paper/paper.pdf), with source [paper/paper.tex](paper/paper.tex).

## Results
- **Theorem 1 (septics, d = 7).** H(C[S⁷C³]^SL₃, t) = R₇(t). This is unconditional.
  - R₇'s least denominator has degree 1386 and its numerator degree 1350.
  - Version 0.1.0 had proved this only through degree 760, and conditionally beyond.
- **Theorem 2 (octics, d = 8, and nonics, d = 9).** The series are determined, with rational functions in `data/octic/d8_rational.json` and `data/nonic/d9_rational.json`.
  - Octics: least denominator of degree 2331, numerator of degree 2286.
  - Nonics: least denominator of degree 1393, numerator of degree 1338.
- **Prior results.** Within the literature we found, the largest degree previously completed was d = 6 (Bedratyuk–Xin 2011). See [PRIOR_ART.md](PRIOR_ART.md).

## Method (known; cited)
The paper claims no new method.
- **Derksen (J. Algebra 285, 2005)**, universal denominators. His Theorems 1.10, 3.4 and 5.1 bound the pole orders by torus data.
- **Makam (J. Algebra 454, 2016, §6)** combines three ingredients:
  - a universal denominator;
  - Knop's criterion for the degree;
  - the functional equation.

  Together they mean half of the numerator's coefficients determine the series.

The contributions are:
- the exhaustive torus-bound enumeration for S^d C³, reproduced by a blind program;
- the exact coefficients for d = 8, 9;
- the certificates;
- corrections to the attribution in version 0.1.0 (paper §1).

## Evidence
| Claim | Evidence | Status |
|---|---|---|
| Torus bounds b_r, d = 5–9 | `scripts/pole_bounds.py`; blind program in `independent/blind_torus_bounds/` | identical |
| Method validated | `scripts/check_validation.py` re-derives Bedratyuk–Xin's d = 5, 6 exactly from fresh data | exact |
| Theorem 1 | `scripts/certify_septic_unconditional.py`, using the exact a_n for n ≤ 760 (15 weight-counting primes, regenerable) | exact certificate |
| Theorem 2, d = 8 | `scripts/certify_ternary.py`, using exact a_n for n ≤ 1194 (six 62-bit primes). Out-of-sample prediction modulo a 31-bit prime to degree 1600; independent weight counting modulo two 16-bit primes to degree 450 | exact certificate; mod-p checks |
| Theorem 2, d = 9 | Same pipeline: exact a_n for n ≤ 686. Prediction to degree 1000; weight counting to degree 400 | exact certificate; mod-p checks |
| Research gates | `RESEARCH_GATES.json`: contribution-unit prior art, limitation triage, extension scout | passed |

## Replay
```bash
PY=/path/to/python ./replay.sh          # about 3 min: all certificates, checks and validation, plus a fresh spot recomputation
FULL=1 PY=/path/to/python ./replay.sh   # also regenerates the exact septic integers to t^760 (4.8 GB RAM)
```
Requirements: `requirements.txt` (python-flint, sympy) and a C compiler with OpenMP. The replay verifies `MANIFEST.sha256` before and after it runs.

To recompute the octic and nonic grid residues from scratch (all but the first two take several minutes to hours):
- `scripts/driver.py 8 1194 6 out.json` (about 90 min);
- `scripts/driver.py 9 690 6 out.json` (about 30 min);
- `scripts/run32.py 8 1600 1 out.json` and `scripts/run32.py 9 1000 1 out.json` (the out-of-sample primes);
- `scripts/methodAd 8 450 p` and `scripts/methodAd 9 400 p` for p = 65521, 65519.

## Status and limitations
- The theorems are computer-assisted. No step is formally verified.
- All review is model-based:
  - two GPT-5.6 rounds on the septic argument (`review/`);
  - version 0.1.0's reviews are in its own package.
- Knop's and Formanek's theorems are used through published restatements.
- d = 10 would need about 100 CPU-hours and is left open.

## Contents
| Path | Content |
|---|---|
| `paper/` | paper.tex, paper.pdf, octic_macros.tex |
| `scripts/` | Enumeration (`pole_bounds.py`), certificates, checks, grid engines (`mw5.c`, `mw6.c`, drivers), weight counting (`methodAd.c`), gate checker |
| `data/septic/` | Candidate R₇, exact a_n to 760, per-prime weight-counting outputs, regeneration driver |
| `data/octic/`, `data/nonic/` | Exact grid residues, determined rational functions, out-of-sample and weight-counting residues, run logs |
| `data/validation/` | Fresh d = 5, 6 grid data and Bedratyuk–Xin numerators |
| `independent/blind_torus_bounds/` | The blind program, its README, sanity and cross-checks, and results for d = 5–9 |
| `review/` | GPT-5.6 reviews (two rounds) and the proof note they reviewed |
| `PRIOR_ART.md`, `RESEARCH_GATES.json`, `PRE-REGISTERED.md` | Prior art; research gates; forecasts and outcomes |
| `LICENSES.md`, `ENVIRONMENT.txt`, `MANIFEST.sha256`, `REPLAY_RECEIPT.md` | Licences, environment, hashes, replay receipt |
