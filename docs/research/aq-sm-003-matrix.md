# AQ-SM-003-MATRIX — Block-Transition Defect Geometry

**Status:** [D] analytic derivation + [V] finite computational checks. Lean OPEN. C4 BLOCKED.

## 1. Setup

Partition Π={B_1,...,B_q}, p_i=|B_i|. Block-transition counts m_ij = #{x∈B_i : T(x)∈B_j}, with sum_j m_ij = p_i. K is the row-stochastic Koopman matrix. P=P_Π. D=(I-P)KP.

## 2. Exact Frobenius law

||D||_F² = Σ_{i,j} (m_ij/p_j)(1 - m_ij/p_i).

Derivation: For x∈B_i with T(x)∈B_j, D_x = v_j - v̄_i where v_j=1_{B_j}/p_j, v̄_i=(1/p_i)Σ_j m_ij v_j. Orthogonality of the v_j gives the stated formula.

**Consequence:** ||D||_F depends on T only through M=(m_ij).

## 3. Rank bound

rank(D) ≤ q-1.

Proof: Every row of D has coordinate sum zero (both v_j and v̄_i sum to 1). So D·1=0, hence Im(D)⊆1^⊥, dimension q-1.

## 4. Reduced Gram covariance form

G_Π = U^T D^T D U = Σ_i p_i Cov_{a_i}(z), a_ij=m_ij/p_i, z_j=e_j/√p_j.

tr(G_Π)=||D||_F², ||D||_2²=λ_max(G_Π).

## 5. Two-block corollary

q=2: ||D||_F² = [b(p-b)/p + c(q-c)/q][1/p+1/q]. Since rank(D)≤1, σ_max(D)²=||D||_F².

## 6. S14 specialization

p=4, q=1, c=0: ||D||_F² = 5b(4-b)/16 = 5/4 - (5/16)(b-2)².

b=1→15/16, b=2→5/4, b=3→15/16. Counts 256,96,16. Total 368.

## 7. Computational checks

- Frobenius identity vs direct matrix construction: all deterministic maps + all partitions, n≤4; random n=5,6. 258,983 cases. 0 failures.
- Rank bound: 0 violations.
- Three-block rank-2 witness: n=5, T=(3,0,4,2,3), partition {{1,3,4},{0},{2}}. rank(D)=2.
- Two-block exact rational check: 2≤p,q≤6. No counterexample.
- S14 exact recomputation: matches 15/16,5/4,15/16; counts 256,96,16.

## 8. Evidence boundary

This is not a Lean proof. It does not establish a universal spectral maximizer for q≥3. It does not certify C4 or publication.

# AQ-SM-003-MATRIX — Block-Transition Defect Geometry

**Status:** [D] analytic derivation + [V] finite computational checks.
Lean: OPEN. C4: BLOCKED. Publication: BLOCKED.

## 1. Setup

Partition Π = {B₁, …, B_q} of a finite state space. Write p_i = |B_i|.

For a deterministic map T, define the block-transition counts

    m_ij = #{x ∈ B_i : T(x) ∈ B_j}

so that Σ_j m_ij = p_i.

Let K be the row-stochastic Koopman matrix (K[x, T(x)] = 1). Let P = P_Π
be the orthogonal block-averaging projection. Define the defect

    D = (I − P) K P.

## 2. Exact Frobenius law

    ‖D‖_F²  =  Σ_{i,j}  (m_ij / p_j) · (1 − m_ij / p_i)

**Derivation.** For x ∈ B_i with T(x) ∈ B_j, the corresponding row of D is

    v_j − v̄_i,

where v_j = 1_{B_j} / p_j and v̄_i = (1/p_i) Σ_j m_ij v_j.

The v_j are mutually orthogonal with ‖v_j‖² = 1 / p_j. Expanding
‖v_j − v̄_i‖² and weighting by m_ij yields the stated formula. ∎

**Consequence.** ‖D‖_F depends on T only through M = (m_ij). Two maps with
the same block-transition matrix have identical Frobenius defect.

## 3. Rank bound

    rank(D)  ≤  q − 1.

**Proof.** Every row of D has coordinate sum zero, because both v_j and
v̄_i sum to 1. Hence D·1 = 0, so Im(D) ⊆ 1^⊥, which has dimension q − 1. ∎

## 4. Reduced Gram covariance form

Let u_j = 1_{B_j} / √p_j, z_j = e_j / √p_j, and
z̄_i = (1/p_i) Σ_j m_ij z_j. Then

    G_Π  =  U^T D^T D U  =  Σ_{i,j} m_ij (z_j − z̄_i)(z_j − z̄_i)^T.

Equivalently,

    G_Π  =  Σ_i  p_i · Cov_{a_i}(z),     a_ij = m_ij / p_i.

Hence G_Π ⪰ 0, tr(G_Π) = ‖D‖_F², and ‖D‖_2² = λ_max(G_Π).

## 5. Two-block corollary

For q = 2 with block sizes p, q and cross-counts b, c:

    ‖D‖_F²  =  [ b(p − b)/p + c(q − c)/q ] · [ 1/p + 1/q ].

Since rank(D) ≤ 1, σ_max(D)² = ‖D‖_F².

## 6. S14 specialization

For p = 4, q = 1, c = 0:

    ‖D‖_F²  =  5 b (4 − b) / 16  =  5/4 − (5/16)(b − 2)².

Values: b = 1 → 15/16, b = 2 → 5/4, b = 3 → 15/16.
Realization counts: 256, 96, 16. Total: 368.

## 7. Computational checks

| Check | Scope | Result |
|-------|-------|--------|
| Frobenius identity vs direct matrix | all deterministic maps + all partitions, n ≤ 4 | 0 failures |
| Frobenius identity | random maps, n = 5, 6 | 0 failures |
| Rank bound rank(D) ≤ q − 1 | same scope | 0 violations |
| Three-block rank-2 witness | n = 5, T = (3, 0, 4, 2, 3), Π = {{1,3,4},{0},{2}} | rank(D) = 2 |
| Two-block exact rational check | 2 ≤ p, q ≤ 6 | no counterexample |
| S14 exact recomputation | b = 1, 2, 3 | matches 15/16, 5/4, 15/16; counts 256, 96, 16 |

Total cases checked: 258,983. All formula checks passed.

## 8. Evidence boundary

This is not a Lean proof. It does not establish a universal spectral
maximizer for q ≥ 3. It does not certify C4 or publication. It records a
finite computational check plus a derivation.

## 9. Next mathematical target

Three-block classifier: enumerate admissible integer matrices M with row
sums p_i, construct exact rational G(M), and classify eigenvalues of
G(M). The optimization has moved from maps T to integer matrices M.
