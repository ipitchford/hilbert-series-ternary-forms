# Agent-readable research index

- **Title:** The Hilbert series of the invariants of ternary septics, octics and nonics.
- **Version:** 0.2.0-candidate (unrefereed candidate). DOI [10.5281/zenodo.22978726](https://doi.org/10.5281/zenodo.22978726). It follows [v0.1.0](https://doi.org/10.5281/zenodo.22974308).
- **Creator:** Anonymous. **Publisher:** Evidence Press.
- **Files:** [paper](paper/paper.pdf), [claims](CLAIMS.json), [prior art](PRIOR_ART.md), [research gates](RESEARCH_GATES.json), [README](README.md).

**Claims.**
- SEPTIC-SERIES (unconditional), OCTIC-SERIES and NONIC-SERIES; see [CLAIMS.json](CLAIMS.json).
- These are computer-assisted theorems resting on Derksen's universal-denominator theorems, the functional equation and exact coefficients.

**Not claimed:**
- methodological novelty (the method is Derksen 2005 and Makam 2016);
- formal verification;
- specialist review;
- priority beyond the bounded search in [PRIOR_ART.md](PRIOR_ART.md).

**Evidence.**
- [scripts/certify_septic_unconditional.py](scripts/certify_septic_unconditional.py) and [scripts/certify_ternary.py](scripts/certify_ternary.py) are the exact certificates; [scripts/negative_controls.py](scripts/negative_controls.py) checks that corrupted inputs are rejected.
- [scripts/check_ternary_extra.py](scripts/check_ternary_extra.py) runs the out-of-sample and independent checks.
- [scripts/check_validation.py](scripts/check_validation.py) validates the method on the known d = 5, 6 cases.
- [independent/blind_torus_bounds/](independent/blind_torus_bounds/README.md) is the blind program for the torus bounds.

**Replay.** Run `PY=python3 ./replay.sh [archived|fresh|full]`. The modes are labelled by verification level, and each writes a JSON receipt; see [README.md](README.md). The coefficient engines are justified in paper §3 (Propositions 5 and 6, with a code map).

**Trust boundaries.**
- The trusted base is the C grid engines, the weight-counting code, Python, python-flint and sympy.
- Knop's and Formanek's theorems are used through restatements.
- All review is model-based: see [review/](review/SOL_REVIEW_2.md).

**Rights.** CC0-1.0 for content and MIT for code; see [LICENSES.md](LICENSES.md).
