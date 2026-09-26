# The Hilbert series of the invariants of ternary septics, octics and nonics

This is an **unrefereed candidate**, version 0.2.0-candidate, dated 26 September 2026. The creator is Anonymous and the publisher is Evidence Press. It follows version 0.1.0-candidate (doi:10.5281/zenodo.22974308), which is immutable. DOI: [10.5281/zenodo.22978726](https://doi.org/10.5281/zenodo.22978726). Repository: https://github.com/ipitchford/hilbert-series-ternary-forms.

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
The single entry point is `PY=/path/to/python ./replay.sh [mode]`. The modes are cumulative:

| Mode | What it does | Time |
|---|---|---|
| `archived` (default) | Freshly runs our torus enumerator and every certificate. Re-lifts every archived residue array: the 15 septic weight-counting arrays and the six octic and six nonic grid arrays. Compares with the archived output of the blind torus program. Recomputes and compares the consequences. Checks the research gates and the manifest before and after. No coefficient is regenerated | about 1 min |
| `fresh` | Adds bounded fresh recomputation: the blind torus program is rerun for d = 5–9; the d = 5, 6 validation grids are regenerated and byte-compared; the septic weight counting is regenerated to degree 120; one fresh 62-bit grid prime is run for d = 8 to degree 200; weight counting mod 65497 is run for d = 8, 9 to degree 60 | about 3 min |
| `full` | Adds full regeneration of every archived coefficient file, byte-compared with the archive: septics to 760; the six octic primes to 1194; the six nonic primes to 690; the 31-bit out-of-sample primes; the weight-counting runs | about 2.5 h |

Each run writes `receipts/replay_<mode>_<time>.json`. The receipt records every command, its input and output hashes, the range computed and the result. The producer's receipts are shipped as `REPLAY_RECEIPT_archived.json`, `REPLAY_RECEIPT_fresh.json` and `REPLAY_RECEIPT_full.json`.

Requirements: `requirements.txt` (python-flint, sympy, numpy, scipy) and a C compiler with OpenMP.

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
| `scripts/` | Enumeration (`pole_bounds.py`), certificates (`certify_septic_unconditional.py`, `certify_ternary.py`), checks, negative controls (`negative_controls.py`), `consequences.py`, grid engines (`mw5.c`, `mw6.c`, `driver.py`, `run32.py`), weight counting (`methodAd.c`), `replay.py`, gate checker |
| `data/septic/` | Candidate R₇, exact a_n to 760, per-prime weight-counting outputs, regeneration driver |
| `data/octic/`, `data/nonic/` | Raw per-prime grid residue arrays with the CRT lifts; determined rational functions; out-of-sample and weight-counting residues; run logs |
| `data/consequences.json` | Generator counts, hsop constraints and leading constants (paper §6) |
| `data/validation/` | Fresh d = 5, 6 grid data and Bedratyuk–Xin numerators |
| `independent/blind_torus_bounds/` | The blind program, its README, sanity and cross-checks, and results for d = 5–9 |
| `review/` | GPT-5.6 reviews (two rounds) and the proof note they reviewed; the response to the external review of v0.2.0; the editorial-gate records |
| `PRIOR_ART.md`, `RESEARCH_GATES.json`, `PRE-REGISTERED.md` | Prior art; research gates; forecasts and outcomes |
| `LICENSES.md`, `ENVIRONMENT.txt`, `MANIFEST.sha256`, `REPLAY_RECEIPT_*.json` | Licences, environment, hashes, producer replay receipts (one per mode) |
