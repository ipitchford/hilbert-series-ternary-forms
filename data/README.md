# Data formats

## Rational functions: `septic/d7_rational.json`, `octic/d8_rational.json`, `nonic/d9_rational.json`

H_d(t) = N(t) / D(t) in lowest terms. The fields are:

| Key | Meaning |
|---|---|
| `d` | the degree of the forms |
| `D` | the least denominator, as integer coefficients in ascending degree, with D(0) = 1 (JSON numbers) |
| `N` | the numerator, as coefficients in ascending degree, stored as decimal strings for exactness |
| `eps` | the sign of the reciprocity of the numerator (+1 in all three cases: N is palindromic) |
| `cyclotomic` | (d = 8, 9) the multiplicity of Φ_r in D, keyed by r |
| `bound_degree` | (d = 8, 9) the degree of the a priori denominator B of Proposition 2 |
| `K` | **differs by file.** For d = 8, 9 it is the paper's K = deg B − dim V. In the d = 7 file (written in v0.1.0) it is deg N = 1350 |
| `primes_used`, `stable_on_last_prime` | (d = 7 only) historical fields from v0.1.0, recording how the candidate R₇ was first reconstructed; they play no role in the proof |

For d = 7 the multiplicities of Φ_r are in `septic/d7_denominator.json` (key `cyclotomic`), and `septic/d7_product_form.json` gives R₇ as a numerator over ∏(1 − t^k) for 28 degrees k. The d = 7 file is left unchanged because it is the immutable reference of the septic certificate.

A minimal loader, which reproduces the leading terms quoted in the paper:

```python
import json
R = json.load(open('data/octic/d8_rational.json'))
D = [int(x) for x in R['D']]; N = [int(x) for x in R['N']]
a = []
for n in range(16):
    v = N[n] if n < len(N) else 0
    v -= sum(D[j] * a[n - j] for j in range(1, min(n, len(D) - 1) + 1))
    a.append(v // D[0])
print(a)   # [1, 0, 0, 1, 0, 0, 6, 0, 0, 81, 0, 0, 1990, 0, 0, 46543]
```

## Coefficient data

| File | Content |
|---|---|
| `octic/d8_L1194_p6.json`, `nonic/d9_L690_p6.json` | Grid engine (Proposition 3): `primes`, grid size `M`, degree `L`, the raw per-prime `residues` (one array of decimal strings per prime, n = 0..L) and their CRT lift `coeffs` |
| `octic/d8_L1600_p31.json`, `nonic/d9_L1000_p31.json` | The out-of-sample prediction files: one 31-bit prime, a different grid size, the same schema |
| `octic/wc_exact/`, `nonic/wc_exact/` | Second algorithm (Proposition 4): `wc_d{d}_N{N}_p{p}.txt`, one line `n a_n mod p` per degree, for 17 (d = 8) and 18 (d = 9) primes |
| `octic/wc_d8_N450_p*.txt`, `nonic/wc_d9_N400_p*.txt` | Earlier weight-counting check files, same format |
| `septic/methodA_exact_760.json`, `septic/runs/` | Exact septic a_n for n ≤ 760, and the per-prime weight-counting outputs they are lifted from |
| `consequences.json` | Paper §6. `secondaries_if_min_sum_hsop_exists` is c_d ∏ k_i for the solver's minimal degree multiset; it is meaningful only if an hsop with those degrees exists |
| `validation/` | Fresh d = 5, 6 grid data and Bedratyuk–Xin's numerators |

All `*.log` files are run logs (timings), not evidence.
