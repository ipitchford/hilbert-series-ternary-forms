# Internal editorial gate: synthesis, decision and response matrix

**Target:** `review-target-0.2.0-candidate.zip`, SHA-256 `0fda3e23d9235f50c1a88796abf1cb832794be2ca0ff6fed79b0cfb7ad1e3826`, commit `18eba0b` (paper.pdf `98efd414…`).

**Roles.** There were five differentiated roles, all model-based and producer-coordinated. Each read the frozen target independently, without seeing the other reports, and none edited it. This is internal editorial review. It is not specialist or journal peer review.

**Reports (SHA-256 of the files as filed):**
- `eic.json` `eb3410b6…`
- `method.json` `29dedc5a…`
- `domain.json` `e6cd2b14…`
- `apps.json` `5fe76c3c…`
- `da.json` `1c72ab4b…`

The shipped `da.json` has one local scratch path replaced by `<local path>`; its hash is `555203b6…`. No other change was made.

## Recommendations

| Role | Recommendation | Confidence | Critical | Major | Minor / Note |
|---|---|---|---|---|---|
| Editor-in-Chief | Minor Revision | see report | 0 | 1 (EIC-1) | 5 / 2 |
| Methodology specialist | Major Revision | see report | 0 | 3 (METH-1, METH-2, METH-3) | 4 / 3 |
| Domain specialist | Minor Revision | see report | 0 | 0 | 6 / 2 |
| Applications specialist | Minor Revision | see report | 0 | 2 (APP-1, APP-2) | 5 / 2 |
| Devil's Advocate | Minor Revision | see report | 0 | 0 | 5 / 2 |

## Consensus and disagreements

**No mathematical error was found.** Several reviewers recomputed load-bearing results with their own code:
- the Devil's Advocate reproduced the b_r for d = 5–9 and matched the series modulo two new primes for n ≤ 150 (d = 7, 8, 9);
- the methodology reviewer made an independent exact low-degree check;
- the applications reviewer loaded all three rational functions and reproduced the stated leading terms;
- three reviewers ran the archived replay successfully.

**Shared findings.**
- Wrong theorem numbers in the companion files: EIC-1, APP-1 and DA-5 found this independently.
- The missing full-mode receipt: METH-3 and APP-2.
- The octic/nonic dependence on one algorithm above degree 450/400: DA-1, DOM-6 and METH-6.
- The overstated "no mathematics in common" wording: EIC-5, METH-6 and DA-4.

**Arbitration.**
- *METH-1 / METH-2 (Major) against the other roles (Minor).* The methodology reviewer's point is that the certificate is only as sound as the pole bound, and that the internal checks cannot detect an undersized bound. The editor accepts this as Major. The proof of the bound must be in the paper, and the out-of-sample prediction must become part of the pass/fail. This is a material change to the certificate.
- *DOM-3.* The claim that the excess of 2 comes from GL₂ centralisers is a hypothesis. The editor required it to be tested rather than asserted.

**Decision: Major Revision → `HOLD_FOR_REPAIR`.** One repair batch, followed by the deterministic publication-ready checks.

## Response matrix

| Item | Response | Changed location | Verification |
|---|---|---|---|
| METH-1 (Major), DA-2 | The pole bound is now proved in the paper. The chain that was reviewed by GPT-5.6 but never shipped (NOTE.md) is added as Lemma 5 (pole order ≤ dim of the fixed locus), Lemma 6 (the fixed locus is a union of torus pieces) and Lemma 7 (dim π(V_S) ≤ κ(S)). Proposition 2 now rests on Lemmas 5–8, and Derksen is credited for the theory. The blind program is described as checking the enumeration given this formulation. The stale pole_bounds.py docstring is fixed | paper §2, §4; `scripts/pole_bounds.py` | text; `check_refs.py` |
| METH-2 (Major) | `certify_ternary.py` requires `--predict` (a further prime beyond the data) as part of its pass/fail. Two undersized-denominator negative controls were added (d = 8, Φ₃; d = 9, Φ₁₁): the internal checks pass, and the prediction alone rejects them. A positive control was also added. §5 explains why | `scripts/certify_ternary.py`, `scripts/negative_controls.py`; paper §5 | replay (archived) |
| METH-3 (Major), APP-2(a) | The full mode is run on the final commit and its receipt shipped. The receipts now record code hashes and the manifest hash (METH-4) | `REPLAY_RECEIPT_full.json` | the receipt |
| EIC-1 (Major), APP-1 (Major), DA-5 | Every citation was renumbered against the final paper (Theorem 1(1)–(3), Propositions 2–4, Lemmas 5–8, Remark 9), including the code comments. A new gate, `scripts/check_refs.py`, fails if any cited number is absent from `paper.aux`. It runs in every replay and also against the site page | README, CLAIMS, AI_INDEX, gates, prior art, responses, `mw5.c`, `mw6.c`, site body/meta | replay (archived) |
| APP-2(b) | The stale v0.1 fields in the site metadata (availability, CI URL, gate wording) were rewritten for v0.2 | site `meta.json` | site preflight |
| DA-1, DOM-6, METH-6(b), EIC cheap list | **Closed at integer level.** Weight counting (Proposition 4) at 17 (d = 8) and 18 (d = 9) sixteen-bit primes gives, after CRT lifting, the same integers as the grid engine for every n ≤ 1194 and ≤ 690. This needed a packed-storage implementation (`methodAd2.c`, byte-identical to `methodAd.c` where both run), because `methodAd.c` needs about 24 GB for d = 8 at n = 1194 | `scripts/methodAd2.c`, `scripts/wc_exact.py`, `data/*/wc_exact/`; paper §3 | replay (archived: lift; fresh: d = 9 regenerated; full: d = 8 regenerated) |
| METH-6(a), EIC-5, DA-4 | Reworded: "independent in code, not in mathematics; both rest on the weight decomposition and Weyl's formulas" | paper §3, §8; README; AI_INDEX | text |
| METH-4 | Each receipt records the SHA-256 of every script and C source, the compiler, the platform and the manifest hash. `MANIFEST.sha256` excludes the receipts, so the manifest hash inside a receipt equals the shipped one | `scripts/replay.py` | receipts |
| METH-5, EIC-2 | Fixed: `FULL=1` replaced by the full mode; `methodA16.c` path; code map (line 65 computes M⁻², lines 66–67 apply it); stale engine comments; README contents | paper §3; README; `mw5.c`, `mw6.c` | text |
| METH-7 | README documents the writable-copy step and gives corrected timings | README | text |
| METH-8 | Table 1 says that the factor 2 is conservative | paper Table 1 | text |
| METH-9 | The septic certificate now also checks the 52 unused exact coefficients (709–760) and requires them to agree; they do | `certify_septic_unconditional.py`; paper §5 | replay (archived) |
| METH-10 | Not added as a control: the engine refuses M < 2(dL+2)+1 itself (line 25), so no aliased output can be produced | — | code |
| DOM-1 | Adopted and extended: a common-factor rule (exact) and Hopf's rank bound. New exact counts: g₉ = 75 (d = 8); g₁₀ = 606 and g₁₁ = 2009 (d = 9). Range 415 ≤ g₁₂ ≤ 416 (d = 7), plus new ranges at degree 12 for d = 8, 9. These match the reviewer's values | `scripts/consequences.py`, `data/consequences.json`; paper §6; CLAIMS | replay (archived) |
| DOM-2, DA-6 | The degree cap is set to S − (δ−1)k_min (1266, 2283, 1273) with its justification; the optima are unchanged; solutions are checked in exact arithmetic; the minima are labelled solver-computed | `consequences.py`; paper §6 | replay (archived) |
| DOM-3 | **Tested; partial negative result.** The centraliser refinement is implemented (`scripts/centraliser_bounds.py`, paper Remark 9). It is valid and never below the true multiplicity for d = 5–9, but it removes the excess only at r = 2 for d = 5, 7, 8. Every other excess is attained by level sets of regular torus elements, whose centraliser is T. The gate entry is re-triaged accordingly (OPEN, reason recorded) | Remark 9; RESEARCH_GATES; §8 | replay (archived) |
| DOM-4 | Dixmier (1983) and Brouwer–Draisma–Popoviciu (2015) are cited for the hsop method; Dixmier's criterion is named as the route to deciding existence | paper §6; PRIOR_ART; gates | text |
| DOM-5, EIC-3 | Bedratyuk is split into the 2009 (arXiv 0806.1920) and 2010 (Ukr. Mat. Zh.) papers. The range statement is exact: t^21 printed in the arXiv version; the survey by Benanti et al. (cited) reports degree ≤ 30, which we have not seen | paper §1; PRIOR_ART | text |
| DOM-6 | See DA-1 (closed at integer level) | — | — |
| DOM-7 | Wording fixed: "for a fixed pair (t, ζ)" via Lemma 6's notation; "not necessarily distinct"; ε = +1 identically, because b₁ = dim V − 2 ≥ δ (proof of Proposition 2) | paper §2, §6 | text |
| DOM-8 | No change required. Knop is cited directly and via Makam | — | — |
| EIC-4, APP-5 | Formanek and Berele are removed from the README, AI_INDEX and gates | README; AI_INDEX; gates | text |
| EIC-6 | zbMATH Open was searched (eight query families); no computation for d ≥ 7 was found; logged | PRIOR_ART; gates | logged queries |
| EIC-7 | The paper states Herbig–Schwarz Thm 3.7's hypotheses (connected simple group, irreducible non-coregular module, no exceptions) and checks them | paper §2 | text |
| EIC-8, DA-3 | Added: random versus systematic error (§3); the prediction tests the pole bound, K and the sign jointly (§5) | paper §3, §5 | text |
| APP-3, APP-8 | A new `data/README.md` gives the schemas, the d = 7 key differences, historical fields, and a loader that reproduces the stated terms. The consequences key is renamed `secondaries_if_min_sum_hsop_exists` | `data/README.md`; `consequences.json` | loader run |
| APP-4 | The narration and page body now say that one algorithm computes the coefficients exactly, that a second, independent algorithm computes the same integers, and give the true ranges | site body/narration | site review |
| APP-6 | "As far as we could find" added to the page's frontier sentences | site body | text |
| APP-7 | Rewritten: "every homogeneous system of parameters has a member of degree divisible by 108, 147 and 64 for d = 7, 8, 9 respectively; degree sum at least 1428, 2391, 1457 (solver-computed)" | site meta/body; README; paper §6 | text |
| APP-9 | Page wording: "exactly 45 new basic invariants are needed in degree 8" | site body | text |
| DA-7 | No further 31-bit primes: against systematic error the second algorithm (DA-1) is the stronger check | — | — |

**Publication-ready checks.** After the repair batch, the deterministic checks were run on the repaired package (commit `cec66de`, archive SHA-256 `f51f2b2e…`) and all passed:
- archived replay from a fresh extraction;
- PDF TeX preflight (0 raw-TeX findings);
- AI-index link check;
- no local paths;
- research gates;
- cross-references.

**Evidence Press state:** `PASS_WITH_NOTES`. The note: all review is internal and model-based.
