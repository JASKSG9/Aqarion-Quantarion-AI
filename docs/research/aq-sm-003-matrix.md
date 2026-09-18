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
