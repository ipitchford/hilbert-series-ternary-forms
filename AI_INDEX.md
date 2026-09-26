# Agent-readable research index

- **Title:** The Hilbert series of the invariants of ternary septics, octics and nonics.
- **Version:** 0.2.0-candidate (unrefereed candidate). DOI [10.5281/zenodo.22978726](https://doi.org/10.5281/zenodo.22978726). It follows [v0.1.0](https://doi.org/10.5281/zenodo.22974308).
- **Creator:** Anonymous. **Publisher:** Evidence Press.
- **Files:** [paper](paper/paper.pdf) ([Markdown](paper/paper.md)), [claims](CLAIMS.json), [prior art](PRIOR_ART.md), [research gates](RESEARCH_GATES.json), [data formats](data/README.md), [README](README.md).

**Claims** (paper numbering: Theorem 1(1)–(3), Propositions 2–4, Lemmas 5–8, Remark 9).
- SEPTIC-SERIES (unconditional), OCTIC-SERIES, NONIC-SERIES, CONSEQUENCES and CENTRALISER-REFINEMENT; see [CLAIMS.json](CLAIMS.json).
- The series are computer-assisted theorems resting on pole-order bounds (paper Lemmas 5–8, the torus case of Derksen 2005), the functional equation and exact coefficients.

**Not claimed:**
- methodological novelty (the method is Derksen 2005 and Makam 2016);
- formal verification;
- specialist review;
- an independent certificate of the solver-computed hsop degree-sum minima;
- priority beyond the bounded search in [PRIOR_ART.md](PRIOR_ART.md).

**Evidence.**
- [scripts/certify_septic_unconditional.py](scripts/certify_septic_unconditional.py) and [scripts/certify_ternary.py](scripts/certify_ternary.py) are the exact certificates; the out-of-sample prediction is part of the latter's pass/fail.
- [scripts/wc_exact.py](scripts/wc_exact.py): the second algorithm gives the same integers over the whole determining range for d = 8, 9.
- [scripts/negative_controls.py](scripts/negative_controls.py) checks that corrupted inputs and undersized denominators are rejected.
- [scripts/check_validation.py](scripts/check_validation.py) validates the method on the known d = 5, 6 cases.
- [independent/blind_torus_bounds/](independent/blind_torus_bounds/README.md) is the blind program for the pole bounds.

**Replay.** Run `PY=python3 ./replay.sh [archived|fresh|full]` on a writable copy. The modes are labelled by verification level, and each writes a JSON receipt with code hashes; see [README.md](README.md). The coefficient algorithms are justified in paper §3 (Propositions 3 and 4, with a code map).

**Trust boundaries.**
- The trusted base is the C grid engines, the weight-counting code, Python, python-flint, sympy and scipy (HiGHS, for the hsop degree sums only).
- Knop's criterion is used through Makam's restatement.
- The two coefficient algorithms share no code but both rest on Weyl's formulas.
- All review is model-based: see [review/](review/).

**Rights.** CC0-1.0 for content and MIT for code; see [LICENSES.md](LICENSES.md).
