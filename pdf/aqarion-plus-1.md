AQARION / FOQDS “+1” Lemma and Kemeny–Snell Lumpability
Formal comparison report • finite-state Markov chains • adversarial scope statement
Scope. This report separates (i) the established necessary-and-sufficient Kemeny–Snell criterion for exact strong
lumpability, (ii) its operator/intertwining formulation, and (iii) a conditional “+1” nilpotent-depth extension statement.
The “+1” statement is not, by itself, a necessary-and-sufficient criterion for state aggregation.
1. Kemeny–Snell condition
Let X={1,…,n}, P be a row-stochastic n×n transition matrix, and Π={B_1,…,B_q} a partition. The indicator
Z∈{0,1}n×q has Zxi=1 precisely when x∈Bi
. The x-th row of PZ contains the one-step probabilities from x into the
partition blocks:
(PZ)[x,j] = sum(y in B_j) P[x,y].
Strong lumpability means this row is constant when x ranges over one source block Bi
. Equivalently, there exists a
q×q row-stochastic quotient P_bar such that:
P Z = Z P_bar. (KS)
This is necessary and sufficient for the block process to be Markov for every initial distribution, with transition
matrix P_bar. [web:53][web:56]
2. Indicator-matrix derivation
Define L=(Z^T Z)^(-1)Z^T, so LZ=I
q
, and Q=ZL, the standard block-averaging projection. If (KS) holds, multiplying
on the left by L yields:
P_bar = L P Z.
For every k≥0, the intertwining iterates:
P^k Z = Z P_bar^k.
Conversely, PZ=ZP_bar says exactly that all rows of PZ belonging to Bi
 equal row i of P_bar. Thus it is exactly the
Kemeny–Snell block-row-sum condition. Since QZ=Z:
PZ = Z(LPZ) iff (I-Q)PZ = 0.
Equivalently, the state-side residual R_Pi=(I-Q)PQ vanishes. With an observable convention K=P^T, one must
transpose the appropriate invariance statement. Therefore a defect formula such as (I-Q)KQ=0 is valid only after
explicitly fixing whether K acts on columns of observables or on state distributions.
3. Refinement and Z
For a refinement Π′ of Π, write Z=Z′C, where C aggregates refined blocks to old blocks. If Π′ is strongly lumpable,
PZ′=Z′Pprime_bar. Then:
PZ = PZprime C = Zprime Pprime_bar C.
The coarser Π is lumpable exactly when this factors through Z=Z′C; equivalently, there must exist P_bar with:
Pprime_bar C = C P_bar. (compatibility)
Consequently, lumpability is not monotone under arbitrary refinement or coarsening. The matrix C and this
compatibility equation are the exact algebraic test.
4. Conditional “+1” lemma
Let E_Pi be a declared defect/transient module with a nilpotent residual operator N_Pi. Let nu(Pi) be its nilpotent
index, with nu=0 for the zero module. Suppose refinement Π′ produces an invariant one-dimensional extension
E_Pi′=E_Pi ⊕ span{eta}, N_Pi′ restricts to N_Pi, and:N_Pi′ eta = u, with u in ker(N_Pi^nu) minus ker(N_Pi^(nu-1)).
Then eta attaches to the end of a maximal nilpotent chain. Hence:
N_Pi′^nu eta != 0, N_Pi′^(nu+1) eta = 0,
therefore nu(Pi′) = nu(Pi) + 1.
This is a conditional linear-algebra theorem. It describes the depth of a specifically defined residual filtration after a
controlled split. It does not follow from Kemeny–Snell alone, and it is not equivalent to exact state aggregation.
5. Exact status table
Statement Status for exact aggregation
PZ = Z P_bar Necessary and sufficient (Kemeny–Snell)
(I-Q)PZ = 0 Equivalent to PZ=ZP_bar
R_Pi=(I-Q)PQ = 0 Equivalent with Q=Z(Z^TZ)^(-1)Z^T
“depth rises by one after a split” Neither necessary nor sufficient by itself
+1 plus specified E, N, extension and attachment Conditional theorem on residual depth only
6. Illustrative matrix example
Let X={1,2,3}, Π={{1,2},{3}}, and
P = [[1/2, 1/4, 1/4], [1/4, 1/2, 1/4], [0, 0, 1]],
Z = [[1,0], [1,0], [0,1]].
The first two states have identical block-transition profiles (3/4,1/4). Direct calculation gives:
PZ = [[3/4,1/4], [3/4,1/4], [0,1]]
= Z [[3/4,1/4], [0,1]].
Thus Π is strongly lumpable with P_bar=[[3/4,1/4],[0,1]]. The aggregation residual is zero. A nontrivial +1
statement is unavailable unless an independently specified nonzero residual module and controlled extension are
present.
To break lumpability, replace the second row by [1/4,1/4,1/2]. Its block profile becomes (1/2,1/2), differing from
(3/4,1/4), so no quotient P_bar can satisfy PZ=ZP_bar.
7. Research-record conclusion
Established. AQARION’s zero-defect condition can be mapped to strong lumpability when its state/observable
convention is fixed: it is the invariant-subspace residual formulation of PZ=ZP_bar.
Conditional. The FOQDS +1 lemma is properly a one-dimensional extension result for a declared nilpotent
residual module. Its eigenvalue claim is that the residual action remains nilpotent and its largest nilpotent
Jordan-chain length increases by one; it is not an eigenvalue-invariance theorem for the lumped stochastic matrix.
Withheld. This report does not assert that every refinement has a +1 depth shift, that +1 is necessary/sufficient for
lumpability, or that AQARION has a Lean proof or repository-bound receipt for the proposed module.
References
[web:53] Kemeny and Snell, Finite Markov Chains, Chapter 6 excerpts: necessary-and-sufficient block row-sum
criterion.
[web:56] Jernigan and Higham, “Testing lumpability in Markov chains” (2003): strong-lumpability block-transition
characterization.
[web:50] Lumpability overview: stochastic-matrix row-sum formulation (secondary source).
[web:46] Zhang, Lumpability approximation methods for Markov models: matrix characterizations (secondary
source).
