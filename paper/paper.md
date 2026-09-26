# The Hilbert series of the invariants of ternary septics, octics and nonics

Anonymous. Version 0.2.0-candidate, 26 September 2026. DOI 10.5281/zenodo.22978726. **Unrefereed candidate.** This Markdown text is an accessible rendering of `paper.tex`; the PDF is authoritative.

## Abstract

We determine the Hilbert series of the rings of $`\mathrm{SL}_3(\mathbb{C})`$-invariants of ternary forms of degrees $`7`$, $`8`$ and $`9`$. Within the literature we found, the largest degree previously completed was $`6`$ (Bedratyuk–Xin, 2011).

- The septic series equals the candidate $`R_7`$ of version 0.1.0 of this work, where it was proved only through degree $`760`$ and conditionally beyond. Its least denominator has degree $`1386`$.

- The octic series has a least denominator of degree $`2331`$ and a palindromic numerator of degree $`2286`$.

- The nonic series has a least denominator of degree $`1393`$ and a palindromic numerator of degree $`1338`$.

The method is known. A priori pole-order bounds from torus data (Derksen’s theory of universal denominators) and the functional equation reduce each series to finitely many coefficients, as in Makam’s work on matrix semi-invariants. We give self-contained proofs of the bounds we use. Our contributions are:

- the exhaustive pole-bound computations for $`d=7,8,9`$, reproduced by a separately written program;

- correctness statements for the two coefficient algorithms, and exact coefficients from both over the whole range needed;

- certificates with archived per-prime data, out-of-sample predictions and negative controls, validated by re-deriving the known series for $`d=5,6`$;

- consequences: exact numbers of minimal generators in low degrees, and constraints on the degrees of every homogeneous system of parameters.

This version also corrects two attribution omissions in version 0.1.0.

# Introduction

Let $`I_{3,d}=\mathbb{C}[S^d\mathbb{C}^3]^{\mathrm{SL}_3}`$ and let $`H_d(t)=\sum_n a_nt^n`$ be its Hilbert series, graded by degree.

- The series is classical for $`d\le4`$; see \[BX\] and, for the history and methods up to 1991, Broer \[Broer\].

- Bedratyuk and Xin \[BX\] computed $`d=5,6`$ by MacMahon partition analysis.

- For $`d=7`$, Bedratyuk’s arXiv preprint \[Bed09\] prints the coefficients through degree $`21`$; they agree with ours. A survey \[BBDGK\] reports that his formulas \[Bed09, Bed10\] gave the terms of degree at most $`30`$ for forms of degree at most $`7`$. We have not seen those further values.

We found no complete series for any $`d\ge7`$. The search record, which includes zbMATH Open but not MathSciNet, is in `PRIOR_ART.md`.

Version 0.1.0 \[V01\] gave a rational function $`R_7`$ and proved $`H_7=R_7`$ through degree $`760`$. Full equality was proved only under an unverified hypothesis on a homogeneous system of parameters (hsop).

<div id="thm:main" class="theorem">

**Theorem 1** (computer-assisted).

1.  *$`H_7=R_7`$. The least denominator of $`H_7`$ is a product of cyclotomic polynomials of degree $`1386`$ (Table <a href="#tab:mult" data-reference-type="ref" data-reference="tab:mult">2</a>), and the numerator is palindromic of degree $`1350`$.*

2.  *$`H_8=N_8/D_8`$, where $`\deg D_8=2331`$, and $`N_8`$ is palindromic of degree $`2286`$.*

3.  *$`H_9=N_9/D_9`$, where $`\deg D_9=1393`$, and $`N_9`$ is palindromic of degree $`1338`$.*

*The polynomials are in `data/*/d{7,8,9}_rational.json` (format in `data/README.md`). The first terms are:
``` math
H_8=1+t^3+6t^6+81t^9+1990t^{12}+46543t^{15}+\cdots,\qquad
H_9=1+t^4+6t^6+3t^7+46t^8+118t^9+612t^{10}+\cdots.
```*

</div>

## Method and what is new

Each ingredient of the method is known.

- Derksen \[Der05\] bounds the poles of Hilbert series by the dimensions of fixed loci of the grading action. He introduces the universal denominator (the least common multiple of the denominators of all submodules) and reduces its computation for a connected reductive group to a maximal torus \[Der05, Thms. 1.10, 3.4, 5.1\]. Lemmas <a href="#lem:pole" data-reference-type="ref" data-reference="lem:pole">5</a>–<a href="#lem:kappa" data-reference-type="ref" data-reference="lem:kappa">7</a> below prove the case we need directly, so the certificate does not depend on the exact form of those statements.

- Knop’s criterion fixes the degree of $`H_d`$, and the rings are Gorenstein. Hence $`H_d\cdot B`$ satisfies a signed reciprocity for the denominators $`B`$ used below.

- Consequently half the coefficients determine the series. Makam used this combination for matrix semi-invariants \[Mak16, §§3,6\].

Our contributions are the new cases and what makes them auditable:

- exhaustive pole-bound computations (§<a href="#sec:torus" data-reference-type="ref" data-reference="sec:torus">4</a>), reproduced by a separately written program;

- correctness statements for both coefficient algorithms, which agree as exact integers over the whole range needed (§<a href="#sec:coef" data-reference-type="ref" data-reference="sec:coef">3</a>);

- the exact data, with archived per-prime residues, and the certificates;

- the consequences in §<a href="#sec:cons" data-reference-type="ref" data-reference="sec:cons">6</a>.

## Corrections to version 0.1.0

Version 0.1.0 is immutable; we record two attribution omissions here. Neither affects any stated result.

1.  Its §7 describes an a priori denominator for $`H_7`$ as available “by standard means”, without citing Derksen \[Der05\], who gives the sharper theory used here.

2.  It presents the combination of a denominator theorem, the functional equation and finitely many exact coefficients as part of its methodological contribution. This is Makam’s strategy \[Mak16, §6\], which \[V01\] cites only for Knop’s criterion.

# The finite-determination certificate

Let $`G=\mathrm{SL}_3`$, $`T\subset G`$ the diagonal torus, $`V=S^d\mathbb{C}^3`$, $`A=\mathbb{C}[V]^G`$, $`X=V/\!/G`$ with quotient map $`\pi`$, and $`\delta=\dim V-8`$, the Krull dimension. We use:

- $`\dim V=36,45,55`$ and $`\delta=28,37,47`$ for $`d=7,8,9`$.

- $`A`$ is Cohen–Macaulay \[HR\]. It is factorial because $`\mathrm{SL}_3`$ has no nontrivial characters, and hence Gorenstein \[Murthy\].

- $`S^d\mathbb{C}^3`$ is not coregular for $`d\ge4`$ \[Sch78\]. Herbig and Schwarz \[HS, Thm. 3.7\] prove that every irreducible non-coregular module of a connected simple algebraic group is $`2`$-large, with no exceptions. $`\mathrm{SL}_3`$ is connected and simple and $`S^d\mathbb{C}^3`$ is irreducible, so $`V`$ is $`2`$-large.

- Knop’s criterion \[Knop\], as stated in \[Mak16, Thm. 3.3\], gives $`\deg H=-\dim V`$ for $`2`$-large modules of semisimple connected groups.

- Stanley’s theorem \[Stanley\] then gives $`H(1/t)=(-1)^\delta t^{\dim V}H(t)`$.

<div id="prop:cert" class="proposition">

**Proposition 2**. *For $`r\ge1`$ let $`b_r`$ be the maximum of $`\kappa(S)`$ over the level sets $`S`$ of order $`r`$ (Lemmas <a href="#lem:kappa" data-reference-type="ref" data-reference="lem:kappa">7</a> and <a href="#lem:enum" data-reference-type="ref" data-reference="lem:enum">8</a>), and let $`B=\prod_r\Phi_r^{p_r}`$ with $`p_r=\min(\delta,b_r)`$. Then $`P=H\cdot B`$ is a polynomial satisfying $`P(t)=t^KP(1/t)`$, where $`K=\deg B-\dim V`$. Consequently $`H`$ is determined by $`a_0,\dots,a_{\lfloor K/2\rfloor}`$.*

</div>

<div class="proof">

*Proof.* Let $`\zeta`$ be a primitive $`r`$-th root of unity. By Lemma <a href="#lem:pole" data-reference-type="ref" data-reference="lem:pole">5</a>, the pole order of $`H`$ at $`\zeta`$ is at most $`\dim X^\zeta`$. By Lemmas <a href="#lem:fixed" data-reference-type="ref" data-reference="lem:fixed">6</a> and <a href="#lem:kappa" data-reference-type="ref" data-reference="lem:kappa">7</a> this is at most $`b_r`$. It is also at most $`\delta`$: by homogeneous Noether normalisation $`A`$ is finite over a polynomial ring in $`\delta`$ variables, so Hilbert–Serre applies.

Hence $`H\cdot B`$ has no finite poles, and a rational function with no finite poles is a polynomial. We have $`B(1/t)=(-1)^{p_1}t^{-\deg B}B(t)`$. For $`r=1`$ the level set is all of $`W`$, so $`b_1=\kappa(W)=\dim V-2\ge\delta`$ and $`p_1=\delta`$. With the functional equation this gives $`P(t)=(-1)^{2\delta}t^KP(1/t)=t^KP(1/t)`$. A polynomial of degree at most $`K`$ with this symmetry is determined by its coefficients of degree at most $`\lfloor K/2\rfloor`$. ◻

</div>

Table <a href="#tab:sizes" data-reference-type="ref" data-reference="tab:sizes">1</a> gives the sizes involved.

<div id="tab:sizes">

| $`d`$ | $`\deg B`$ | $`K`$ | needed | exact data | modulus (bits) | $`2\times`$bound (bits) |
|:---|---:|---:|---:|:---|---:|---:|
| 7 | 1452 | 1416 | 708 | 0–760 (weight counting) | 240 | 201 |
| 8 | 2433 | 2388 | 1194 | 0–1194 (grid; weight counting) | 372 | 272 |
| 9 | 1427 | 1372 | 686 | 0–690 (grid; weight counting) | 372 | 276 |

Certificate sizes. “Needed” is $`\lfloor K/2\rfloor`$. “Exact data” is the range of the archived exact coefficients. “Modulus” is the product of the distinct primes of the determining data, compared with $`2\binom{n+\dim V-1}{\dim V-1}`$ at $`n=\lfloor K/2\rfloor`$. Since $`0\le a_n\le\binom{n+\dim V-1}{\dim V-1}`$ and the lift is taken in $`[0,\text{modulus})`$, the factor $`2`$ is conservative.

</div>

# Exact coefficients

Two algorithms compute $`a_n\bmod p`$. The Chinese remainder theorem then gives the integers. Throughout, $`W=\{(a-c,b-c):a+b+c=d\}\subset\mathbb{Z}^2`$ is the set of torus weights of $`V`$, one for each monomial $`x^ay^bz^c`$.

<div id="prop:grid" class="proposition">

**Proposition 3** (grid engine; `scripts/mw5.c`, `mw6.c`). *Let $`L\ge0`$ and $`M>dL+4`$. Let $`p`$ be a prime with $`M\mid p-1`$, and let $`\omega\in\mathbb{F}_p`$ have exact order $`M`$. For $`(i,j)\in(\mathbb{Z}/M)^2`$ set $`e_3=-i-j`$, $`E=(i,j,e_3)`$, and
``` math
w(i,j)=\prod_{a\ne b}(1-\omega^{E_a-E_b}),\qquad F_{i,j}(t)=\prod_{(u,v)\in W}\bigl(1-\omega^{ui+vj}t\bigr)^{-1}\in\mathbb{F}_p[[t]].
```
Then for every $`n\le L`$,
``` math
a_n\equiv M^{-2}\sum_{\substack{0\le i<j<e_3<M\\ i+j+e_3\equiv0}}w(i,j)\,[t^n]F_{i,j}(t)\pmod p.
```*

</div>

<div class="proof">

*Proof.* By the Weyl integration formula, $`H(t)=\frac16\operatorname{CT}_{z}\bigl[\prod_{\alpha}(1-z^\alpha)\prod_{w\in W}(1-tz^w)^{-1}\bigr]`$. Here $`z=(z_1,z_2)`$, $`z_3=(z_1z_2)^{-1}`$, the product over $`\alpha`$ runs over the six roots $`z_a/z_b`$, and $`\operatorname{CT}`$ takes the constant term of each $`t`$-coefficient.

1.  *Exponent bound.* The coefficient of $`t^n`$ is an integer Laurent polynomial whose exponents have absolute value at most $`dn+4`$: the weights contribute at most $`dn`$ and the Weyl numerator at most $`4`$.

2.  *No aliasing.* For a monomial $`z^m`$ with $`|m_1|,|m_2|<M`$, the average $`M^{-2}\sum_{(i,j)}\omega^{m_1i+m_2j}`$ equals $`1`$ if $`m=0`$ and $`0`$ otherwise, since $`\omega`$ has exact order $`M`$ and $`M`$ is invertible mod $`p`$. So the average over the order-$`M`$ grid computes the constant term exactly modulo $`p`$ whenever $`M>dL+4`$.

3.  *Orbit reduction.* The integrand is invariant under $`S_3`$ permuting $`(E_1,E_2,E_3)`$, and it vanishes when two $`E_a`$ coincide. So the grid sum is $`6`$ times the sum over representatives $`i<j<e_3`$, which cancels the factor $`\tfrac16`$.

4.  *Power series.* The engine builds $`F_{i,j}`$ one factor at a time using $`s_n\leftarrow s_n+x\,s_{n-1}`$, which is multiplication by $`(1-xt)^{-1}`$.

 ◻

</div>

*Code map for `mw5.c`.*

- Line 24 checks $`M\mid p-1`$ and $`p<2^{62}`$. Line 25 enforces $`M\ge2(dL+2)+1>dL+4`$.

- Lines 29–31 choose $`\omega`$ and verify its exact order $`M`$ by testing $`\omega^{M/q}\ne1`$ for every prime $`q\mid M`$.

- Line 49 selects $`i<j<e_3`$. Line 51 forms $`w(i,j)`$. Line 56 forms $`\omega^{ui+vj}`$. Lines 57–58 perform the recurrence.

- Line 65 computes $`M^{-2}`$, and lines 66–67 apply it.

- Arithmetic is Montgomery reduction with 128-bit products for $`p<2^{62}`$. The engine refuses weight sets with more than $`64`$ elements (line 35), so $`d\le9`$.

- `mw6.c` is the same algorithm for $`p<2^{31}`$.

<div id="prop:wc" class="proposition">

**Proposition 4** (weight counting; `scripts/methodAd.c`, `scripts/methodAd2.c`, `data/septic/methodA16.c`). *Let $`f_n(A,B)`$ be the number of multisets of $`n`$ elements of the multiset of $`\mathrm{GL}_3`$-weights $`\{(a,b,c):a+b+c=d\}`$ with sum $`(A,B,dn-A-B)`$. If $`3\nmid dn`$ then $`a_n=0`$. Otherwise, with $`k=dn/3`$,
``` math
a_n=f_n(k,k)-f_n(k{-}1,k{+}1)-f_n(k,k{-}1)-f_n(k{-}2,k)+f_n(k{-}1,k{-}1)+f_n(k{-}2,k{+}1).
```*

</div>

<div class="proof">

*Proof.* $`a_n`$ is the multiplicity of $`\det^k`$ in $`S^n(S^dV)`$ as a $`\mathrm{GL}_3`$-module. By the Weyl character formula this multiplicity is $`\sum_{w\in S_3}\operatorname{sgn}(w)\,\mathrm{mult}\bigl(w(\lambda+\rho)-\rho\bigr)`$, with $`\lambda=(k,k,k)`$ and $`\rho=(2,1,0)`$. The six terms are those displayed.

The programs compute $`f_n`$ by one unbounded-knapsack pass per weight, keeping only the coordinates at most $`dn/3+2`$. This is enough because weights are nonnegative and every target coordinate is at most $`k+2`$. Arithmetic is modulo a prime $`p<2^{16}`$, which the programs check, with 16-bit storage. `methodAd2.c` stores only the cells with all three coordinates in range, about a third of the memory. Its output is byte-identical to that of `methodAd.c` wherever both have been run. ◻

</div>

*Data.*

- *Septics:* exact $`a_n`$ for $`n\le760`$ by Proposition <a href="#prop:wc" data-reference-type="ref" data-reference="prop:wc">4</a> at $`15`$ distinct $`16`$-bit primes. The archived per-prime outputs are re-lifted on every replay, and the full replay mode (`./replay.sh full`) regenerates them.

- *Octics and nonics, first algorithm:* exact $`a_n`$ by Proposition <a href="#prop:grid" data-reference-type="ref" data-reference="prop:grid">3</a> at six distinct $`62`$-bit primes. For each case the six raw residue arrays are archived, and `certify_ternary.py` re-lifts them itself. It checks every congruence, the array lengths, the metadata and the bound.

- *Octics and nonics, second algorithm:* exact $`a_n`$ by Proposition <a href="#prop:wc" data-reference-type="ref" data-reference="prop:wc">4</a> at $`17`$ ($`d=8`$, $`n\le1194`$) and $`18`$ ($`d=9`$, $`n\le690`$) distinct $`16`$-bit primes, whose products exceed twice the coefficient bound (`scripts/wc_exact.py`). The lifted integers equal those of the first algorithm for every $`n`$ in these ranges. The whole determining range is therefore computed twice, as exact integers, by programs that share no code.

- The two algorithms are independent in code, not in mathematics. Both rest on the weight decomposition of $`S^d\mathbb{C}^3`$ and on Weyl’s formulas, used in different forms (the integration formula and the character formula).

- *Random versus systematic error.* A corrupted residue at any single prime would almost surely give a lift outside the proven range $`[0,\binom{n+\dim V-1}{\dim V-1}]`$, because each modulus exceeds the required size by $`39`$ to $`100`$ bits. What remains is a systematic error common to all primes; the second algorithm, the out-of-sample predictions and the validation on $`d=5,6`$ address it.

# The pole-order bounds

The following three lemmas make the bound in Proposition <a href="#prop:cert" data-reference-type="ref" data-reference="prop:cert">2</a> self-contained. They are the case of Derksen’s theory \[Der05, §§1–5\] that we need.

<div id="lem:pole" class="lemma">

**Lemma 5** (pole order and fixed locus). *Let $`A`$ be a finitely generated positively graded $`\mathbb{C}`$-algebra with $`A_0=\mathbb{C}`$, let $`\zeta`$ be a primitive $`r`$-th root of unity, and let $`I_r\subset A`$ be the ideal generated by the homogeneous elements whose degree is not divisible by $`r`$. Then the pole order of $`H_A`$ at $`\zeta`$ is at most $`\dim A/I_r`$.*

</div>

<div class="proof">

*Proof.* Let $`f_1,\dots,f_m`$ be homogeneous generators of $`I_r`$, of degrees $`e_i`$ with $`r\nmid e_i`$. For a finitely generated graded $`A`$-module $`M`$ and $`f=f_i`$, the exact sequence $`0\to(0:_Mf)(-e_i)\to M(-e_i)\to M\to M/fM\to0`$ gives $`(1-t^{e_i})H_M=H_{M/fM}-t^{e_i}H_{(0:_Mf)}`$. Since $`1-\zeta^{e_i}\ne0`$, the pole order of $`H_M`$ at $`\zeta`$ is at most the larger of the pole orders of $`H_{M/fM}`$ and $`H_{(0:_Mf)}`$, both of which are annihilated by $`f`$. Applying this for $`f_1,\dots,f_m`$ in turn, starting from $`M=A`$, bounds the pole order of $`H_A`$ at $`\zeta`$ by that of finitely many finitely generated graded $`A/I_r`$-modules. By Noether normalisation and Hilbert–Serre, each of these has pole order at most $`\dim A/I_r`$. ◻

</div>

For a torus element $`t`$ and a root of unity $`\zeta`$ put $`S(t,\zeta)=\{w\in W:\chi_w(t)=\zeta\}`$, and let $`V_S`$ be the span of the monomials with weights in $`S`$.

<div id="lem:fixed" class="lemma">

**Lemma 6** (the fixed locus). *For $`A=\mathbb{C}[V]^G`$, the zero set of $`I_r`$ in $`X`$ is the fixed locus $`X^\zeta`$ of the grading action of $`\zeta`$, and $`X^\zeta=\bigcup_{t\in T}\pi\bigl(V_{S(t,\zeta)}\bigr)`$, a finite union.*

</div>

<div class="proof">

*Proof.* For homogeneous $`f`$ of degree $`e`$, $`f(\zeta v)=\zeta^ef(v)`$. So $`\pi(v)`$ lies in the zero set of $`I_r`$ exactly when every invariant takes the same value at $`v`$ and $`\zeta v`$, that is, when $`\pi(\zeta v)=\pi(v)`$. Take $`v`$ with $`Gv`$ closed. Then $`G(\zeta v)=\zeta\,Gv`$ is closed and lies in the same fibre, which contains exactly one closed orbit, so $`\zeta v=gv`$ for some $`g\in G`$. If $`g=g_sg_u`$ is the Jordan decomposition, an eigenvector of $`g`$ for $`\zeta`$ lies in the $`\zeta`$-generalised eigenspace of $`g_s`$, so $`g_sv=\zeta v`$. Conjugating $`g_s`$ into $`T`$ gives $`t=hg_sh^{-1}`$ with $`t(hv)=\zeta(hv)`$, $`hv\in V_{S(t,\zeta)}`$ and $`\pi(hv)=\pi(v)`$. The converse inclusion is immediate. Only finitely many sets $`S(t,\zeta)\subseteq W`$ occur. (Whether $`\zeta`$ or $`\zeta^{-1}`$ appears depends on conventions; the bounds below take the maximum over all primitive $`r`$-th roots.) ◻

</div>

For finite $`S\subset\mathbb{Z}^2`$ put $`\kappa(S)=\dim V_S/\!/T`$.

<div id="lem:kappa" class="lemma">

**Lemma 7**. *$`\dim\pi(V_S)\le\kappa(S)`$, and $`\kappa(S)=|S_0|-\operatorname{rank}S_0`$, where $`S_0=\{w\in S:-w\in\operatorname{cone}(S)\}`$. In particular:*

- *$`\kappa`$ is monotone under inclusion;*

- *$`\kappa(S)=0`$ if $`S`$ lies in an open half-plane through $`0`$ (for example, on an affine line not through $`0`$);*

- *$`\kappa(\{0\})=1`$, and $`\kappa(\{w\})=0`$ for $`w\neq0`$.*

</div>

<div class="proof">

*Proof.* $`\pi`$ restricted to $`V_S`$ is $`T`$-invariant, so it factors through the categorical quotient $`V_S\to V_S/\!/T`$; this gives the inequality. $`\mathbb{C}[V_S]^T`$ is the monoid algebra of the nonnegative integer relations $`\sum c_ww=0`$, so its dimension is that of the relation cone. That cone lies in $`\mathbb{R}^{S_0}`$ and contains a relation that is strictly positive on $`S_0`$. So it has the dimension of $`\ker(\mathbb{R}^{S_0}\to\mathbb{R}^2)`$, which is $`|S_0|-\operatorname{rank}S_0`$. The remaining statements follow directly. ◻

</div>

<div id="lem:enum" class="lemma">

**Lemma 8** (exhaustive enumeration). *Every level set $`S=W\cap\phi^{-1}(\zeta)`$ of a homomorphism $`\phi:\mathbb{Z}^2\to\mathbb{C}^*`$ at a root of unity $`\zeta`$ of exact order $`r`$ is contained in one of the following sets, with the same $`r`$:*

1.  **Rank two.* If the differences of $`S`$ span a rank-$`2`$ lattice, then $`S=W\cap(w_0+\Lambda)`$, where $`\Lambda=\ker\phi`$ is the kernel of $`(x,y)\mapsto cx+ey\bmod N`$ for some $`N`$ at most the largest $`|\det|`$ of two weight differences ($`147`$, $`192`$, $`243`$ for $`d=7,8,9`$). One may take $`c\mid N`$. Here $`r`$ is the order of $`w_0`$ in $`\mathbb{Z}^2/\Lambda\cong\mathbb{Z}/N`$.*

2.  **Rank one.* If $`S`$ lies on a line through $`0`$ with primitive direction $`u`$, then $`S\subseteq\{ku:k\equiv\rho\ (\mathrm{mod}\ m)\}`$ for some $`m`$ at most the diameter of the line’s weight set, with $`r=m/\gcd(m,\rho)`$. If $`S`$ lies on a line not through $`0`$, then $`\kappa(S)=0`$.*

3.  **One element.* If $`S=\{w\}`$, then $`\kappa=0`$ for $`w\neq0`$. For the zero weight, which occurs when $`3\mid d`$, $`S=\{0\}`$ has $`\kappa=1`$ and $`\zeta=\phi(0)=1`$, so $`r=1`$.*

*Consequently $`b_r=\max\kappa`$ over the finitely many sets listed. For every $`r`$ not attained with $`\kappa>0`$, $`b_r=0`$.*

</div>

<div class="proof">

*Proof.*

1.  $`\ker\phi`$ contains the rank-$`2`$ lattice of differences, so its index divides that lattice’s index. It is therefore at most the $`|\det|`$ of any two independent differences. $`\mathbb{Z}^2/\ker\phi`$ embeds in $`\mathbb{C}^*`$, so it is finite cyclic and $`\phi`$ induces an isomorphism onto $`\mu_N`$. A primitive map $`(a,b)`$ can be multiplied by a unit $`k`$ with $`ka\equiv\gcd(a,N)`$, which gives the normal form $`c\mid N`$.

2.  Points $`ku`$ lie in $`S`$ exactly when $`\phi(u)^k=\zeta`$. If $`\phi(u)`$ has infinite order, then $`|S|\le1`$. If it has order $`m`$, the condition is a congruence class, and classes of size at least $`2`$ require $`m`$ to be at most the diameter. On an affine line not through $`0`$ a linear form is positive, so $`\kappa=0`$ by Lemma <a href="#lem:kappa" data-reference-type="ref" data-reference="lem:kappa">7</a>.

3.  This is Lemma <a href="#lem:kappa" data-reference-type="ref" data-reference="lem:kappa">7</a> together with $`\phi(0)=1`$.

Monotonicity of $`\kappa`$ gives the conclusion. ◻

</div>

`scripts/pole_bounds.py` implements Lemma <a href="#lem:enum" data-reference-type="ref" data-reference="lem:enum">8</a>. A second program, written blind by a separate agent (`independent/blind_torus_bounds/`), evaluates the lattice condition of \[Der05, Thm. 5.1\] directly. It maximises $`\kappa(S)`$ over subsets $`S=W\cap(w_0+L)`$ with $`r\mid o(S)`$, where $`o(S)`$ is the order of $`(0,1)`$ modulo the lattice generated by the $`(w,1)`$, $`w\in S`$. The two programs give identical $`b_r`$ for $`d=5,\dots,9`$. The blind program checks the enumeration given the level-set formulation; the formulation itself rests on Lemmas <a href="#lem:pole" data-reference-type="ref" data-reference="lem:pole">5</a>–<a href="#lem:kappa" data-reference-type="ref" data-reference="lem:kappa">7</a>. For the known cases $`d=5,6`$, $`b_r`$ is at least the true multiplicity everywhere and positive exactly on the true pole set.

<div id="rem:centraliser" class="remark">

*Remark 9* (a centraliser refinement, and what it does not explain). The map $`\pi|_{V_S}`$ is also invariant under the centraliser $`Z=Z_G(t)`$, which preserves $`V_S`$, so $`\dim\pi(V_S)\le\dim V_S/\!/Z\le\dim V_S-(\text{generic $Z$-orbit dimension})`$ by Rosenlicht \[Ros56\]. This improves $`\kappa`$ only when $`t`$ has a repeated eigenvalue, where $`Z\cong\mathrm{GL}_2`$. The script `scripts/centraliser_bounds.py` computes the refined bound, bounding the generic orbit dimension from below by the rank of the $`\mathfrak{gl}_2`$-action at a random point modulo a prime. For $`d=5,\dots,9`$ the refined bound is never below the true multiplicity. It removes the excess of $`2`$ over the true multiplicity (Table <a href="#tab:mult" data-reference-type="ref" data-reference="tab:mult">2</a>) only at $`r=2`$ for $`d=5,7,8`$. At every other starred order the maximum is attained by a level set of a torus element with three distinct eigenvalues, whose centraliser is $`T`$. So the recurring excess is not explained by centralisers alone. We do not use the refinement in the certificates.

</div>

# The three series

*Septics.* For $`d=7`$, Proposition <a href="#prop:cert" data-reference-type="ref" data-reference="prop:cert">2</a> requires $`a_0,\dots,a_{708}`$, which are exact. The script `certify_septic_unconditional.py` regenerates the bounds and checks four things in exact arithmetic:

- the least denominator $`D_7`$ of $`R_7`$ divides $`B`$;

- $`Q=R_7B`$ is a polynomial of degree at most $`1416`$ with $`Q(t)=t^{1416}Q(1/t)`$;

- the series of $`R_7`$ equals the exact $`a_n`$ for $`n\le708`$;

- out of sample, the series of $`R_7`$ also equals the $`52`$ exact $`a_n`$ with $`709\le n\le760`$, which the certificate does not use.

So $`H_7B=Q`$, and $`H_7=R_7`$.

*Octics and nonics.* No candidate is needed. The script `certify_ternary.py` proceeds as follows:

1.  it re-lifts the archived residues of the first algorithm;

2.  it forms the lower half of $`P=H\cdot B`$ and completes it by reciprocity;

3.  it reduces $`P/B`$ to lowest terms;

4.  it checks that the pole order at $`t=1`$ equals $`\delta`$ and that the series is nonnegative;

5.  it requires the determined function to predict the residues of a further prime beyond the data used. This is part of the pass/fail, for the following reason.

The internal steps cannot detect a denominator bound that is too small: any $`B`$ yields a function reproducing $`a_0,\dots,a_{\lfloor K/2\rfloor}`$. With the exponent of one $`\Phi_r`$ lowered by one at an order where the bound is tight, the internal checks still pass, but the prediction fails. Two such negative controls ($`d=8`$, $`\Phi_3`$; $`d=9`$, $`\Phi_{11}`$) are part of every replay, with controls for corrupted residues, a wrong degree label, a truncated array and a tampered reference. The prediction uses a fresh $`31`$-bit prime and a different grid size with the same algorithm (`mw6.c`), up to degree $`1600`$ ($`d=8`$) and $`1000`$ ($`d=9`$). It tests the pole bound, the degree $`K`$ and the sign jointly, since an error in any of them would make the symmetric completion fail beyond the data.

The octic determination uses $`a_n`$ for $`n\le1194`$. The nonic determination uses $`n\le686`$ of the archived range $`0`$–$`690`$. Both ranges are also covered by the second algorithm as exact integers (§<a href="#sec:coef" data-reference-type="ref" data-reference="sec:coef">3</a>). Finally, the same pipeline re-derives Bedratyuk and Xin’s $`H_5`$ and $`H_6`$ from fresh grid data and reproduces their rational functions exactly.

<div id="tab:mult">

|  |  |
|:---|:---|
| $`d=7`$ | 1:28, 2:16\*, 3:28, 4:8\*, 5:7\*, 6:16\*, 7:3, 8:4, 9:11\*, 10:4, 11:2, 12:8\*, 13:2, 14:1, 15:7\*, 16:1, 17:1, 18:6\*, 19:1, 20:1, 21:3, 22:1, 23:1, 24:4, 25:1, 26:1, 27:3, 29:1, 30:4, 33:2, 36:3, 39:2, 42:1, 45:2, 48:1, 51:1, 54:2, 57, 60, …, 78 (step 3):1, 87:1, 90:1, 108:1 |
| $`d=8`$ | 1:37, 2:16\*, 3:37, 4:8\*, 5:9\*, 6:16\*, 7:7\*, 8:4, 9:14\*, 10:4, 11:2, 12:8\*, 13:2, 14:3, 15:9\*, 16:1, 17:2, 18:6\*, 19:1, 20:1, 21:7\*, 22:1, 23:1, 24:4, 25:1, 26:1, 27:4, 28:1, 29:1, 30:4, 31:1, 33:2, 35:1, 36:3, 37:1, 39:2, 41:1, 42:3, 45:3, 48:1, 49:1, 51:2, 54:2, 57:1, 60:1, 63:2, 66:1, 69:1, 72:1, 75:1, 78:1, 81:1, 84:1, 87:1, 90:1, 93:1, 105:1, 108:1, 111:1, 123:1, 126:1, 147:1 |
| $`d=9`$ | 1:47, 2:26\*, 3:16, 4:14\*, 5:11\*, 6:8, 7:9\*, 8:8\*, 9:4, 10:6, 11:3, 12:4, 13:3, 14:5, 15:3, 16:4, 17:2, 18:2, 19:2, 20:3, 21:2, 22:2, 23:2, 24:2, 25:2, 26:1, 27:1, 28:2, 29:1, 30:1, 31:1, 32:2, 33:1, 34:1, 35:1, 36:1, 37:1, 38:1, 40:1, 41:1, 42:1, 43:1, 44:1, 46:1, 47:1, 48:1, 49:1, 50:1, 55:1, 56:1, 64:1 |

Multiplicities $`m_r`$ of $`\Phi_r`$ in the least denominators ($`r{:}m_r`$; others $`0`$). An asterisk marks orders where the pole bound $`\min(\delta,b_r)`$ exceeds $`m_r`$; it always exceeds it by exactly $`2`$.

</div>

# What the series determine

The series constrain the structure of the invariant rings. The following statements are consequences of Theorem <a href="#thm:main" data-reference-type="ref" data-reference="thm:main">1</a> alone. The script `scripts/consequences.py` computes them, and the output is in `data/consequences.json`.

*Minimal generators in low degree.* Write $`g_n=\dim(A_+/A_+^2)_n`$ for the number of minimal generators of degree $`n`$, so that $`g_n=a_n-\dim(A_+^2)_n`$. Here $`(A_+^2)_n`$ is spanned by the monomials of degree $`n`$, with at least two factors, in generators of lower degree. Two facts bound its dimension:

- *Common factor.* If every such monomial contains one generator $`f`$ of degree $`e`$, then $`(A_+^2)_n=f\,A_{n-e}`$. Multiplication by $`f`$ is injective because $`A`$ is a domain, so $`\dim(A_+^2)_n=a_{n-e}`$.

- *Otherwise,* $`\max_{0<m<n}(a_m+a_{n-m}-1)\le\dim(A_+^2)_n\le`$ the number of monomials. The lower bound is Hopf’s: a bilinear map $`\mathbb{C}^p\times\mathbb{C}^q\to\mathbb{C}^s`$ without zero divisors has rank at least $`p+q-1`$, since the projectivised kernel must miss the Segre variety of dimension $`p+q-2`$.

Processing degrees in order while the lower counts are exact gives:

- $`d=7`$: $`g_6=3`$ and $`g_9=13`$, while $`415\le g_{12}\le416`$.

- $`d=8`$: $`g_3=1`$, $`g_6=5`$ and $`g_9=75`$, while $`1894\le g_{12}\le1909`$.

- $`d=9`$: $`g_4=1`$, $`g_6=6`$, $`g_7=3`$, $`g_8=45`$, $`g_9=118`$, $`g_{10}=606`$ and $`g_{11}=2009`$, while $`8233\le g_{12}\le8254`$.

*Systems of parameters.* If $`A`$ is finite over $`\mathbb{C}[f_1,\dots,f_\delta]`$ with homogeneous $`f_i`$ of degrees $`k_i`$, then the least denominator divides $`\prod_i(1-t^{k_i})`$. So for every $`r`$ at least $`m_r`$ of the $`k_i`$ are divisible by $`r`$. This is the method used by Dixmier \[Dix83\] and by Brouwer, Draisma and Popoviciu \[BDP15\] for binary forms. Consequences:

- every hsop of $`I_{3,7}`$ has a member of degree divisible by $`108`$, a member of degree divisible by $`90`$, a member of degree divisible by $`87`$ (not necessarily distinct), and so on;

- every hsop of $`I_{3,8}`$ and of $`I_{3,9}`$ has a member of degree divisible by $`147`$ and $`64`$ respectively.

Minimising $`\sum_ik_i`$ subject to these constraints, with each $`k_i`$ a degree in which invariants exist, is an integer program. No optimal multiset contains a degree above $`S-(\delta-1)k_{\min}`$, where $`S`$ is the sum of any feasible multiset; we use this cap ($`1266`$, $`2283`$, $`1273`$). The solver (HiGHS) reports the minima $`\sum_ik_i\ge1428`$, $`2391`$ and $`1457`$ for $`d=7,8,9`$. These values are solver-computed, not independently certified, and the optimal multisets satisfy the constraints in exact arithmetic. For septics the minimum is attained by the multiset $`K`$ of \[V01, Thm. 2\]. Whether an hsop with minimal degree sum exists is not determined by the series; Dixmier’s criterion together with the Hilbert–Mumford description of the nullcone is the known route to deciding it.

*Secondary invariants.* Let $`c_d=\lim_{t\to1}(1-t)^\delta H_d(t)`$. Since $`A`$ is Cohen–Macaulay, it is free over any hsop, and the number of secondary invariants over an hsop of degrees $`k_i`$ is $`c_d\prod_ik_i`$. The exact values of $`c_d`$ are in `data/consequences.json`; for example $`c_7\approx3.3029\cdot10^{-10}`$.

*What is not determined.* The series do not determine the generators themselves, the degrees of an actual hsop, the relations beyond the counts implied above, or whether the rings are complete intersections. They do provide exact targets for all such computations.

# Verification

<div id="tab:checks">

| Check | Result |
|:---|:---|
| Pole bounds $`b_r`$, $`d=5,\dots,9`$: two separately written programs | identical |
| Pole bounds versus the known least denominators, $`d=5,6`$ | $`b_r\ge m_r`$; same support |
| Method re-derives Bedratyuk–Xin’s $`H_5`$, $`H_6`$ from fresh grid data | exact, equal |
| $`H_7`$: certificate with exact $`a_n`$, $`n\le708`$ (weight counting, $`15`$ primes) | exact |
| $`H_7`$: $`52`$ further exact $`a_n`$ ($`709\le n\le760`$) reproduced | exact, out of sample |
| $`H_8`$, $`H_9`$: re-lift of six archived residue arrays each; determination; pole orders $`37`$, $`47`$ | exact |
| $`H_8`$, $`H_9`$: second algorithm (weight counting, $`17`$ and $`18`$ primes) equals the first for every $`n\le1194`$, $`690`$ | exact |
| $`H_8`$, $`H_9`$: prediction modulo a fresh $`31`$-bit prime ($`n\le1600`$, $`1000`$), same algorithm, different grid | mod $`p`$, agree |
| Negative controls: corrupted residues, wrong label, truncated array, tampered reference, undersized denominator ($`2`$ cases) | all rejected |
| Centraliser-refined bounds (Remark <a href="#rem:centraliser" data-reference-type="ref" data-reference="rem:centraliser">9</a>) never below the true multiplicities, $`d=5,\dots,9`$ | consistent |

Checks. “Exact” means integer equality; “mod $`p`$” means agreement modulo the stated prime(s), which is evidence and not an integer certificate.

</div>

*Review record* (provenance, not a mathematical test):

- the septic argument, including Lemmas <a href="#lem:pole" data-reference-type="ref" data-reference="lem:pole">5</a>–<a href="#lem:kappa" data-reference-type="ref" data-reference="lem:kappa">7</a>, was reviewed adversarially by a model from another vendor (GPT-5.6) in two rounds: round 1 found write-up gaps, and round 2 gave “valid with minor gaps”, which were repaired;

- version 0.2.0 was reviewed by an external model review, whose required revisions are made here, and then by a five-role internal editorial gate, whose required revisions are also made here (see `review/`).

# Limitations

- All three theorems are computer-assisted. They rest on the cited theorems, on Lemmas <a href="#lem:pole" data-reference-type="ref" data-reference="lem:pole">5</a>–<a href="#lem:enum" data-reference-type="ref" data-reference="lem:enum">8</a>, on Propositions <a href="#prop:grid" data-reference-type="ref" data-reference="prop:grid">3</a> and <a href="#prop:wc" data-reference-type="ref" data-reference="prop:wc">4</a> and their implementations.

- The two coefficient algorithms agree as exact integers over the whole determining range, but they are independent in code rather than in mathematics (§<a href="#sec:coef" data-reference-type="ref" data-reference="sec:coef">3</a>).

- No step is formally verified. Knop’s criterion is used through Makam’s statement \[Mak16, Thm. 3.3\]. All review is model-based.

- The next case, $`d=10`$, has $`66`$ weights. The grid engine accepts at most $`64`$, so it needs an implementation change and renewed checking. With the present bound it would need exact $`a_n`$ up to degree $`3249`$. That is roughly $`100`$ CPU-hours for the grid engine, and far beyond the memory of the weight-counting programs. The recurring excess of $`2`$ in the pole bounds is only partly explained by centralisers (Remark <a href="#rem:centraliser" data-reference-type="ref" data-reference="rem:centraliser">9</a>); a full explanation could lower this cost.

# Provenance and AI-use statement

This work was produced by an AI research agent (Claude, Anthropic) under the direction of the publisher, Evidence Press. The problems, computations, proofs and text are AI-generated, and no human mathematical contribution is claimed. Parts of the verification were written by separate AI agents working from the definitions alone. No human specialist has checked the work.

<div class="thebibliography">

99 L. Bedratyuk, Analogue of the Sylvester–Cayley formula for invariants of ternary form (Ukrainian), *Mat. Visn. Nauk. Tov. Im. Shevchenka* 6 (2009) 50–61; English version arXiv:0806.1920. L. Bedratyuk, Analogue of the Cayley–Sylvester formula and the Poincaré series for an algebra of invariants of ternary form, *Ukr. Mat. Zh.* 62 (2010) 1561–1570; translation *Ukrainian Math. J.* 62 (2010) 1810–1821. F. Benanti, S. Boumova, V. Drensky, G. K. Genov, P. Koev, Computing with rational symmetric functions and applications to invariant theory and PI-algebras, *Serdica Math. J.* 38 (2012) 137–188; arXiv:1201.4448. L. Bedratyuk, G. Xin, MacMahon partition analysis and the Poincaré series of the algebras of invariants of ternary and quaternary forms, *Linear Multilinear Algebra* 59 (2011) 789–799, doi:10.1080/03081087.2010.536763. A. E. Brouwer, J. Draisma, M. Popoviciu, The degrees of a system of parameters of the ring of invariants of a binary form, *Transform. Groups* 20 (2015) 953–967, doi:10.1007/s00031-015-9335-8. B. Broer, Hilbert series for ternary forms, in: A. M. Cohen (ed.), *Computational aspects of Lie group representations and related topics*, CWI Tract 84, CWI, Amsterdam, 1991, 1–18. H. Derksen, Universal denominators of Hilbert series, *J. Algebra* 285 (2005) 586–607, doi:10.1016/j.jalgebra.2004.10.029. J. Dixmier, Série de Poincaré et systèmes de paramètres pour les invariants des formes binaires, *Acta Sci. Math. (Szeged)* 45 (1983) 151–160. H.-C. Herbig, G. W. Schwarz, The Koszul complex of a moment map, arXiv:1205.4608. M. Hochster, J. L. Roberts, Rings of invariants of reductive groups acting on regular rings are Cohen–Macaulay, *Adv. Math.* 13 (1974) 115–175. F. Knop, Über die Glattheit von Quotientenabbildungen, *Manuscripta Math.* 56 (1986) 419–427, doi:10.1007/BF01168503. V. Makam, Hilbert series and degree bounds for matrix (semi-)invariants, *J. Algebra* 454 (2016) 14–28, doi:10.1016/j.jalgebra.2016.01.032; arXiv:1510.08420 (theorem numbers refer to the arXiv version). M. P. Murthy, A note on factorial rings, *Arch. Math.* 15 (1964) 418–420. M. Rosenlicht, Some basic theorems on algebraic groups, *Amer. J. Math.* 78 (1956) 401–443. G. W. Schwarz, Representations of simple Lie groups with regular rings of invariants, *Invent. Math.* 49 (1978) 167–191. R. P. Stanley, Hilbert functions of graded algebras, *Adv. Math.* 28 (1978) 57–83. Anonymous, Hilbert series of the invariants of tuples of $`4\times4`$ and $`5\times5`$ matrices, and a candidate series for plane septics, version 0.1.0-candidate, Evidence Press (2026), doi:10.5281/zenodo.22974308.

</div>

## References

- \[Bed09\] L. Bedratyuk, Analogue of the Sylvester–Cayley formula for invariants of ternary form (Ukrainian), *Mat. Visn. Nauk. Tov. Im. Shevchenka* 6 (2009) 50–61; English version arXiv:0806.1920.
- \[Bed10\] L. Bedratyuk, Analogue of the Cayley–Sylvester formula and the Poincaré series for an algebra of invariants of ternary form, *Ukr. Mat. Zh.* 62 (2010) 1561–1570; translation *Ukrainian Math. J.* 62 (2010) 1810–1821.
- \[BBDGK\] F. Benanti, S. Boumova, V. Drensky, G. K. Genov, P. Koev, Computing with rational symmetric functions and applications to invariant theory and PI-algebras, *Serdica Math. J.* 38 (2012) 137–188; arXiv:1201.4448.
- \[BX\] L. Bedratyuk, G. Xin, MacMahon partition analysis and the Poincaré series of the algebras of invariants of ternary and quaternary forms, *Linear Multilinear Algebra* 59 (2011) 789–799, doi:10.1080/03081087.2010.536763.
- \[BDP15\] A. E. Brouwer, J. Draisma, M. Popoviciu, The degrees of a system of parameters of the ring of invariants of a binary form, *Transform. Groups* 20 (2015) 953–967, doi:10.1007/s00031-015-9335-8.
- \[Broer\] B. Broer, Hilbert series for ternary forms, in: A. M. Cohen (ed.), *Computational aspects of Lie group representations and related topics*, CWI Tract 84, CWI, Amsterdam, 1991, 1–18.
- \[Der05\] H. Derksen, Universal denominators of Hilbert series, *J. Algebra* 285 (2005) 586–607, doi:10.1016/j.jalgebra.2004.10.029.
- \[Dix83\] J. Dixmier, Série de Poincaré et systèmes de paramètres pour les invariants des formes binaires, *Acta Sci. Math. (Szeged)* 45 (1983) 151–160.
- \[HS\] H.-C. Herbig, G. W. Schwarz, The Koszul complex of a moment map, arXiv:1205.4608.
- \[HR\] M. Hochster, J. L. Roberts, Rings of invariants of reductive groups acting on regular rings are Cohen–Macaulay, *Adv. Math.* 13 (1974) 115–175.
- \[Knop\] F. Knop, Über die Glattheit von Quotientenabbildungen, *Manuscripta Math.* 56 (1986) 419–427, doi:10.1007/BF01168503.
- \[Mak16\] V. Makam, Hilbert series and degree bounds for matrix (semi-)invariants, *J. Algebra* 454 (2016) 14–28, doi:10.1016/j.jalgebra.2016.01.032; arXiv:1510.08420 (theorem numbers refer to the arXiv version).
- \[Murthy\] M. P. Murthy, A note on factorial rings, *Arch. Math.* 15 (1964) 418–420.
- \[Ros56\] M. Rosenlicht, Some basic theorems on algebraic groups, *Amer. J. Math.* 78 (1956) 401–443.
- \[Sch78\] G. W. Schwarz, Representations of simple Lie groups with regular rings of invariants, *Invent. Math.* 49 (1978) 167–191.
- \[Stanley\] R. P. Stanley, Hilbert functions of graded algebras, *Adv. Math.* 28 (1978) 57–83.
- \[V01\] Anonymous, Hilbert series of the invariants of tuples of $`4\times4`$ and $`5\times5`$ matrices, and a candidate series for plane septics, version 0.1.0-candidate, Evidence Press (2026), doi:10.5281/zenodo.22974308.
