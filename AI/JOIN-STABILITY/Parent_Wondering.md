# Join Stability — Parent-Wandering / Range-Gap Analysis

## Status

Finite join theorem: PROVED [P] — incidence-graph argument + σ(I)=I
Arbitrary-set theorem: REFUTED [F] — explicit infinite counterexample
Surjective theorem: PROVED CONDITIONALLY [P]
Range-Gap Lemma: PROVED [P]
Exact finite census n=1..6: VERIFIED [V] — 1,016,496 ordered pairs, 0 failures
Combined finite evidence: [PV]
Lean: OPEN
C4: BLOCKED
Publication: BLOCKED
Promotion: FALSE

Previous six-line proof remains retracted in PROOF_v1_retracted.md
Census remains corroboration, not proof by itself.

---

## 1. Target

Let T: X→X, E,F ∈ Eq(X)
Define IsPullbackStable(E) := T⁻¹(E) ⊆ E where T⁻¹(E)={(x,y): T(x) E T(y)}

Target: IsPullbackStable(E) ∧ IsPullbackStable(F) ⇒ IsPullbackStable(E∨F)
Write G := E∨F = EqCl(E∪F)

---

## 2. Finite Theorem — CLOSED — Incidence Proof [P]

**Theorem:** Let X finite, T: X→X total, E,F stable ⇒ G stable.

**Proof:**

1. Finite Pullback Rigidity [P]: Let π:X→X/E. Then E=kerπ, T⁻¹(E)=ker(π∘T).
   If T⁻¹(E)⊆E then |X/T⁻¹(E)|=|im(π∘T)| ≤ |X/E| ≤ |X/T⁻¹(E)| ⇒ equality ⇒ T⁻¹(E)=E.
   Same for F. Hence T induces permutations σ_E: Q_E→Q_E, σ_F: Q_F→Q_F where Q_E=X/E.

2. Incidence: I⊆Q_E×Q_F, (A,B)∈I iff A∩B≠∅. For x∈X, edge e_x=([x]_E,[x]_F).

3. σ=σ_E×σ_F. If (A,B)∈I, pick x∈A∩B, then T(x)∈σ_E(A)∩σ_F(B) ⇒ σ(I)⊆I.

4. **Finite step:** Q_E×Q_F finite, σ permutation ⇒ |σ(I)|=|I| ⇒

   σ(I)=I

   Hence genuine graph automorphism, not just forward preservation.

5. Connected components of bipartite graph (Q_E⊔Q_F, I) are exactly E∨F classes.
   Graph automorphisms preserve components.
   If T(x) G T(y) then e_T(x), e_T(y) same component ⇒ e_T(x)=σ(e_x) ⇒ e_x, e_y same component ⇒ x G y.

Hence T⁻¹(G)⊆G. QED.

---

## 3. Range-Gap Lemma — [P]

**Lemma E:** If E,F stable but G not stable, then ∃ x not G y with Tx G Ty and every G-path Tx=z0..zk=Ty leaves im(T).

**Proof:** If path stays in im(T), choose wi with T(wi)=zi. If zi E zi+1 then T(wi) E T(wi+1) ⇒ wi E wi+1 by stability. Same for F. Then w0 G.. G wk ⇒ x G y contradiction. Hence range-gap necessary.

Box: join failure ⇒ range gap.

If every G-component remains G-connected after restricting to im(T), join theorem follows immediately.

---

## 4. Explicit Counterexamples — Unrestricted Theorem REFUTED [F]

**Infinite:** X=ℕ, T(n)=n+1. E class {0,2}, F class {0,3}, rest singletons.
Then 2 E 0 F 3 ⇒ 2 G 3 but 1 not G 2. T(1)=2, T(2)=3 ⇒ T(1) G T(2) while 1 not G 2.
Missing point 0∉im(T) is canonical witness. Hence unrestricted theorem false.

**Finite hypothesis essential.** This also shows where finite proof uses finiteness: |σ(I)|=|I| and |X/T⁻¹(E)|=|im(π∘T)|.

---

## 5. Surjective Boundary — PROVED CONDITIONALLY [P]

If T surjective then im(T)=X, range-gap cannot occur. Range-Gap Lemma immediately gives:

T⁻¹(E)⊆E ∧ T⁻¹(F)⊆F ⇒ T⁻¹(E∨F)⊆E∨F

For finite X, define X_k=im(T^k). X_{k+1}⊆X_k stabilizes to X_∞ invariant, T|X_∞ surjective. Transient vertices are only possible source of range-gap.

---

## 6. Counting Reconciliation [V]

For fixed T, k_T = |{E stable}|
Σk_T = 1,6,51,592,8565,148896 = (T,E) objects
Σk_T² = 1,10,117,1960,40385,1016496 = ordered (T,E,F)
Σk_T(k_T+1)/2 = 1,8,84,1276,24475,582696 = unordered with repetition
unordered = (ordered+individual)/2 ⇒ (1016496+148896)/2=582696

**Independent audit:** n=1..6 ordered 1,10,117,1960,40385,1016496 → join failures 0, incidence failures 0 (σ(I)=I for every pair)

Previous census through n=4: 3984 (T,E) pairs, backward_only=0, corroborates rigidity.

---

## 7. Targeted Search — Corroboration Only [V]

Generator: parent_wandering_search.py, seed 22092026, P→P∨T⁻¹(P) coarsening.

n=7: maps 2000, seeds/map 500, stable-pair samples 36735, range-gap candidates 0
n=8: maps 1000, seeds/map 500, samples 23663, candidates 0
n=9: maps 500, seeds/map 500, samples 15493, candidates 0
n=10: maps 200, seeds/map 1000, samples 4199, candidates 0

Not exhaustive, not proof. Future search should separate range-gap candidate vs actual join failure.

---

## 8. Best Next Attack

1. LEAN-JS-001: finite_pullback_rigidity (kernel/card)
2. LEAN-JS-002: class permutations
3. LEAN-JS-003: σ(I)=I cardinality upgrade
4. LEAN-JS-004: JOIN-STABILITY
5. Characterize transient structure permitting G-path between image points to leave image: |im(T)|, eventual image size, transient depth, G-components, image∩component connectivity.

Do not collapse into single counterexample statistic.

---

## 9. Governance

Range-Gap Lemma PROVED [P]
Infinite counterexample EXPLICIT [F]
Surjective theorem PROVED CONDITIONALLY [P]
Finite theorem PROVED [P] incidence + σ(I)=I
Exact census VERIFIED [V] n≤6 1,016,496
Combined [PV] finite
Lean OPEN
C4 BLOCKED
Publication BLOCKED
Promotion FALSE

Formal certification requires Lean build with no sorry/axiom violations + independent replay.
