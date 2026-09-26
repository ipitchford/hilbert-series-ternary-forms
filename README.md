# The Hilbert series of the invariants of ternary septics, octics and nonics

This is an **unrefereed candidate**, version 0.2.0-candidate, dated 26 September 2026. The creator is Anonymous and the publisher is Evidence Press. It follows version 0.1.0-candidate (doi:10.5281/zenodo.22974308), which is immutable. DOI: [10.5281/zenodo.22978726](https://doi.org/10.5281/zenodo.22978726). Repository: https://github.com/ipitchford/hilbert-series-ternary-forms.

The paper is [paper/paper.pdf](paper/paper.pdf), with source [paper/paper.tex](paper/paper.tex) and an accessible Markdown version [paper/paper.md](paper/paper.md). Theorem numbers below are those of the paper: Theorem 1(1)–(3), Propositions 2–4, Lemmas 5–8, Remark 9 (`scripts/check_refs.py` enforces this).

## Results
- **Theorem 1(1), septics, d = 7.** H(C[S⁷C³]^SL₃, t) = R₇(t), unconditionally.
  - R₇'s least denominator has degree 1386 and its numerator degree 1350.
  - Version 0.1.0 had proved this only through degree 760, and conditionally beyond.
- **Theorem 1(2), octics, d = 8.** Determined: least denominator of degree 2331, palindromic numerator of degree 2286 (`data/octic/d8_rational.json`).
- **Theorem 1(3), nonics, d = 9.** Determined: least denominator of degree 1393, palindromic numerator of degree 1338 (`data/nonic/d9_rational.json`).
- **Consequences (paper §6).** Exact minimal-generator counts in low degree, for example g₈ = 45, g₉ = 118, g₁₀ = 606 and g₁₁ = 2009 for nonics. Every homogeneous system of parameters has a member of degree divisible by 108, 147 and 64 for d = 7, 8, 9 respectively.
- **Prior results.** As far as we could find (zbMATH Open, arXiv, Crossref, web; not MathSciNet), the largest degree previously completed was d = 6 (Bedratyuk–Xin 2011). See [PRIOR_ART.md](PRIOR_ART.md).

## Method (known; cited)
The paper claims no new method.
- **Derksen (J. Algebra 285, 2005)**: pole orders of Hilbert series are bounded by fixed loci, which reduce to torus data (Thms 1.10, 3.4, 5.1). Paper Lemmas 5–8 prove the case used directly.
- **Makam (J. Algebra 454, 2016, §6)**: a denominator bound, Knop's degree criterion and the functional equation together mean that half of the numerator's coefficients determine the series.

The contributions are:
- the exhaustive pole-bound enumeration for S^d C³, reproduced by a blind program;
- the exact coefficients, computed as exact integers by two algorithms that share no code;
- the certificates, with out-of-sample predictions and negative controls;
- the consequences, and the corrections to the attribution in version 0.1.0 (paper §1).

## Evidence
| Claim | Evidence | Status |
|---|---|---|
| Pole bounds b_r, d = 5–9 | `scripts/pole_bounds.py`; blind program in `independent/blind_torus_bounds/` | identical |
| Method validated | `scripts/check_validation.py` re-derives Bedratyuk–Xin's d = 5, 6 exactly from fresh data | exact |
| Theorem 1(1) | `scripts/certify_septic_unconditional.py`: exact a_n for n ≤ 708 used; the 52 further exact a_n (709–760) reproduced out of sample | exact certificate |
| Theorem 1(2), d = 8 | `scripts/certify_ternary.py`: exact a_n for n ≤ 1194 (six 62-bit grid primes, raw residues re-lifted), plus a required out-of-sample prediction modulo a 31-bit prime to degree 1600 | exact certificate |
| Theorem 1(3), d = 9 | Same pipeline: exact a_n for n ≤ 686; prediction to degree 1000 | exact certificate |
| Second algorithm, d = 8, 9 | `scripts/wc_exact.py`: weight counting at 17 / 18 sixteen-bit primes gives the same integers for every n ≤ 1194 / 690 | exact agreement |
| Negative controls | `scripts/negative_controls.py`: corrupted residues, wrong label, truncated array, tampered reference and two undersized denominators are all rejected; unmodified inputs are accepted | passed |
| Centraliser refinement | `scripts/centraliser_bounds.py`: valid, never below the true multiplicities; explains the excess of 2 only at r = 2 (paper Remark 9) | consistent |
| Consequences | `scripts/consequences.py` → `data/consequences.json` | recomputed and compared |
| Research gates | `RESEARCH_GATES.json`: contribution-unit prior art, limitation triage, extension scout | passed |

## Replay
Work on a writable copy (`cp -R` of a read-only checkout keeps the permissions; use `chmod -R u+w` first). The single entry point is `PY=/path/to/python ./replay.sh [mode]`. The modes are cumulative:

| Mode | What it does | Time |
|---|---|---|
| `archived` (default) | Freshly runs the enumerator, every certificate and the negative controls. Re-lifts every archived residue array (15 septic, six octic and six nonic arrays, and the 35 second-algorithm arrays) and compares the two algorithms. Compares with the archived output of the blind program. Recomputes the consequences and the centraliser bounds. Checks the research gates, the cross-references and the manifest before and after. No coefficient is regenerated | about 2 min |
| `fresh` | Adds bounded recomputation: the blind program is rerun for d = 5–9; the d = 5, 6 validation grids are regenerated and byte-compared; septic weight counting to degree 120; one fresh 62-bit grid prime for d = 8 to degree 200; weight counting mod 65497 for d = 8, 9 to degree 60; the 18 nonic second-algorithm arrays regenerated and byte-compared | about 15 min |
| `full` | Adds full regeneration of every other archived coefficient file, byte-compared with the archive: septics to 760; the six octic and six nonic grid primes; the 31-bit out-of-sample primes; the weight-counting check files; the 17 octic second-algorithm arrays | about 3.5 h |

Each run writes `receipts/replay_<mode>_<time>.json`, recording every command, its input and output hashes, the range computed, the result, the SHA-256 of every script and C source, the compiler and the platform. The producer's receipts are shipped as `REPLAY_RECEIPT_archived.json`, `REPLAY_RECEIPT_fresh.json` and `REPLAY_RECEIPT_full.json`. `MANIFEST.sha256` lists every other file; the receipts record its hash, so they bind to exactly the shipped files.

Requirements: `requirements.txt` (python-flint, sympy, numpy, scipy) and a C compiler with OpenMP. The d = 8 second-algorithm regeneration needs about 7 GB of memory.

## Status and limitations
- The theorems are computer-assisted. No step is formally verified.
- The two coefficient algorithms are independent in code, not in mathematics: both use the weight decomposition of S^d C³ and Weyl's formulas.
- Knop's criterion is used through Makam's published statement (Thm 3.3 of arXiv:1510.08420).
- All review is model-based: two GPT-5.6 rounds on the septic argument, an external model review of v0.2.0 and a five-role internal editorial gate (`review/`). Version 0.1.0's reviews are in its own package.
- d = 10 has 66 weights (the grid engine accepts 64) and would need exact a_n to degree 3249; it is left open.

## Contents
| Path | Content |
|---|---|
| `paper/` | paper.tex, paper.pdf, paper.md |
| `scripts/` | Enumeration (`pole_bounds.py`), certificates (`certify_septic_unconditional.py`, `certify_ternary.py`), `negative_controls.py`, `check_ternary_extra.py`, `check_validation.py`, second algorithm (`wc_exact.py`), `centraliser_bounds.py`, `consequences.py`, grid engines (`mw5.c`, `mw6.c`, `driver.py`, `run32.py`), weight counting (`methodAd.c`, `methodAd2.c`), `replay.py`, `check_refs.py`, `check_research_gates.py`, `make_paper_md.py` |
| `data/README.md` | Data formats and a short loader |
| `data/septic/` | Candidate R₇, exact a_n to 760, per-prime weight-counting outputs, regeneration driver, `methodA16.c` |
| `data/octic/`, `data/nonic/` | Raw per-prime grid residue arrays with the CRT lifts; determined rational functions; out-of-sample and weight-counting residues; second-algorithm arrays (`wc_exact/`); run logs |
| `data/consequences.json` | Generator counts, hsop constraints and leading constants (paper §6) |
| `data/validation/` | Fresh d = 5, 6 grid data and Bedratyuk–Xin numerators |
| `independent/blind_torus_bounds/` | The blind program, its README, sanity and cross-checks, and results for d = 5–9 |
| `review/` | GPT-5.6 reviews (two rounds) and the proof note they reviewed; the response to the external review of v0.2.0; the editorial-gate reports, decision and response matrix (`review/editorial-gate/`) |
| `PRIOR_ART.md`, `RESEARCH_GATES.json`, `PRE-REGISTERED.md`, `CLAIMS.json`, `AI_INDEX.md` | Prior art; research gates; forecasts and outcomes; machine-readable claims; index for AI readers |
| `LICENSES.md`, `ENVIRONMENT.txt`, `MANIFEST.sha256`, `REPLAY_RECEIPT_*.json` | Licences, environment, hashes, producer replay receipts (one per mode) |
