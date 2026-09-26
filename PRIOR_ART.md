# Prior art and novelty boundary (v0.2.0-candidate)

**Search dates:** 25 and 26 September 2026 (zbMATH Open queries added on 26 September after the editorial gate).
- The v0.1.0 search covered result and object prior art for ternary forms and matrix invariants.
- A method search on 26 September 2026 covered pole orders at roots of unity, universal and a priori denominators, and fixed loci.

**Corpus:** arXiv full text and API; Crossref; zbMATH Open (API; query families: 'ternary form Poincaré series invariants', 'Hilbert series invariants ternary forms', 'ternary septic/octic/nonic invariants', 'Poincaré series SL3 invariants forms', 'invariants plane curves degree seven', 'Molien-Weyl ternary forms', 'algebra of invariants ternary form degree', 'Poincaré series algebra of invariants'; no computation for d ≥ 7 found); web search; publisher pages; A. E. Brouwer's tables. MathSciNet and several textbooks (Stanley 1979, Benson, Derksen–Kemper, Smith) were not searched.

**Sources read in full:**
- Derksen 2005 (§§1–5 and 6);
- Makam 2016 (arXiv version, §§1–6);
- Bedratyuk–Xin (arXiv 1007.1064);
- Bedratyuk (arXiv 0806.1920, 0811.0256);
- Đoković (math/0608147);
- Herbig–Schwarz (1205.4608).

The machine-readable contribution map, limitation triage and extension scout are in `RESEARCH_GATES.json`.

## Method (known; cited)

| Ingredient | Source | Use here |
|---|---|---|
| Universal denominator; pole order at a primitive r-th root ≤ dim M/I^[r]M; fixed-point description | Derksen, J. Algebra 285 (2005), Def. 1.9, Thm 1.10, Lemma 2.2 | Proposition 2; the case used is proved directly in Lemmas 5–7 |
| gv = ζv characterisation; reduction to a maximal torus (udenom S^G divides udenom S^T) | Derksen 2005, Prop. 3.3, Thm 3.4 | Lemma 6 (proved directly) |
| Torus universal denominator: m_d = max(#I − rank Ω_I) under a lattice condition | Derksen 2005, Thm 5.1 | our enumeration computes these numbers for S^d C^3 |
| Strategy: universal denominator + Knop degree + functional equation ⇒ half the coefficients suffice | Makam, J. Algebra 454 (2016), §3 and §6 (matrix semi-invariants) | same strategy, applied to ternary forms |
| Heuristic precursors for binary forms | Đoković 2006; Howe–Saly (cited by Đoković) | context |
| hsop degree constraints from the cyclotomic factors of the least denominator | Dixmier, Acta Sci. Math. 45 (1983) 151–160; Brouwer–Draisma–Popoviciu, Transform. Groups 20 (2015) 953–967 (binary forms) | paper §6: method known, numbers new |
| Generator counts: common-factor rule and Hopf's rank bound for bilinear maps without zero divisors | classical (domain property; Hopf's bound) | paper §6 |
| Centraliser refinement of the fixed-locus bound | Derksen 2005 (Prop. 3.3 / proof of Thm 3.4); Rosenlicht 1956 | paper Remark 9 (computed; not used in the certificates) |

**Verdict: KNOWN.** The paper claims no methodological novelty.

## Results (object)

| Object | Closest prior work | Verdict |
|---|---|---|
| H for ternary septics (d = 7) | Bedratyuk, Mat. Visn. NTSh 6 (2009) 50–61 (arXiv:0806.1920): coefficients up to t^21, which agree with ours. Benanti–Boumova–Drensky–Genov–Koev, Serdica Math. J. 38 (2012) 137–188 (arXiv:1201.4448) report that Bedratyuk's formulas (also Ukr. Mat. Zh. 62 (2010) 1561–1570) gave terms of degree ≤ 30 for m ≤ 7; those values were not seen; v0.1.0 of this work: exact to degree 760 and conditional beyond | new in the bounded search |
| H for ternary octics (d = 8) | none found | new in the bounded search |
| H for ternary nonics (d = 9) | none found | new in the bounded search |
| H for d ≤ 6 | classical (d ≤ 4); Bedratyuk–Xin 2011 (d = 5, 6) | known; re-derived here as validation |
| History and methods up to 1991 | B. Broer, *Hilbert series for ternary forms*, CWI Tract 84 (1991) 1–18. It covers cubic concomitants, some quartic covariants and systems of forms, not d = 7, 8, 9 (confirmed by the external reviewer, 26 Sep 2026) | context; cited |

## Corrections to v0.1.0 (recorded here and in the paper, §1)

- **Derksen not cited.** v0.1.0 §7 described an a priori denominator as available "by standard means". Derksen 2005 gives the sharper theory.
- **Method novelty overstated.** v0.1.0 claimed the combination of a denominator theorem, the functional equation and finitely many exact coefficients as part of its contribution. That is Makam's strategy (2016, §6), which v0.1.0 cited only for Knop's criterion.
