# Ternary octics: pre-registered forecast (2026-09-26)

- **A priori denominator.** Derksen's universal denominator for the torus (Theorems 3.4 and 5.1), capped at δ = 37, gives deg B* = 2433. So exact a_n for n ≤ 1194 determine H(C[S^8 C^3]^SL3). This needs 272 bits; six 62-bit primes give 372.
- **Cost forecast** (probe at L = 150 and 300 on an M2, 7 threads): about 17 min per prime at L = 1194, so about 105 min for six primes.
- **Outcome predictions:**
  - P(run completes with a consistent H) = 0.9.
  - P(the least denominator of H has degree < 2433) = 0.95, since the torus bound is not sharp.
- **Checks planned:**
  - an independent weight-counting program (generic d) for exact a_n up to degree 450;
  - one extra 31-bit prime to a higher degree, for out-of-sample prediction.

## Extension scout (2026-09-26, before any d = 9 or d = 10 computation)

| d | deg B* | Exact a_n needed up to | Cost estimate | Decision |
|---|---|---|---|---|
| 9 | 1427 | 686 | about 5 min per prime × 6 | do it now |
| 10 | 6564 | 3249 | about 13 h per prime × 8 | OPEN: about 100 CPU-hours, not cheap |
| 11 | 10518 | 5220 | about 80 h per prime × 10 | OPEN |

- **Nonic prediction:** P(consistent determination) = 0.9.
- **Out-of-sample checks queued:**
  - one 31-bit prime for d = 8 to degree 1600;
  - one 31-bit prime for d = 9 to degree 1000;
  - independent weight counting (methodAd) modulo two 16-bit primes: d = 8 to degree 450, d = 9 to degree 400.

## Outcomes (2026-09-26)

**Cost.**
- d = 8: the six primes at L = 1194 took 853–937 s each, 89 min in total, against the 105 min forecast.
- d = 9: the six primes took about 5 min each, as forecast.

**d = 8.** Determined. The forecast event occurred.
- Least denominator: degree 2331 (< 2433).
- Numerator: degree 2286, palindromic.
- Pole order 37 at t = 1.
- Out-of-sample prediction modulo a 31-bit prime holds up to degree 1600.
- Independent weight counting agrees modulo 65521 and 65519 up to degree 450.

**d = 9.** Determined.
- Least denominator: degree 1393. Numerator: degree 1338, palindromic.
- Pole order 47 at t = 1.
- Prediction modulo a 31-bit prime holds up to degree 1000.
- Weight counting agrees up to degree 400.

**Known cases.** The same pipeline re-derives Bedratyuk–Xin's d = 5 and d = 6 rational functions exactly.

**Blind program.** It reproduces the torus bounds for d = 5–9.

## Residue-archiving rerun (26 September 2026, after the external review of v0.2.0)

**Forecast (recorded before the run):** recomputing the six octic and six nonic 62-bit primes with the same engine and primes reproduces the archived lifted coefficients exactly. Wall time is about 90 minutes (octic) and 30 minutes (nonic).

**Outcome:**
- Octic: 6 primes in 880–911 s each (log `data/octic/d8_L1194_p6.rerun.log`).
- Nonic: 6 primes in 268–301 s each (log `data/nonic/d9_L690_p6.rerun.log`).
- Lifted coefficients: identical to the earlier archived lists for both d = 8 and d = 9. The raw per-prime arrays are now archived.
- `certify_ternary.py` re-lifts the arrays, checks every congruence, and reproduces `d8_rational.json` and `d9_rational.json` exactly.
- Five negative controls (`scripts/negative_controls.py`) are all rejected.
