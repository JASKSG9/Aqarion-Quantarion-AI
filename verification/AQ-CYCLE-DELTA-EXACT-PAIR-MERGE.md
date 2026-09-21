AQ-CYCLE-DELTA-001


Exact Pair-Merge Defect Lemmas


Definitions


Let X be finite, T:X\to X, and let
[
\Pi={{a,b}}\cup{{x}:x\notin{a,b}}.
]


Let P=P_\Pi be the block-averaging projection and let
[
K_{ij}=1_{{T(i)=j}}.
]


Define
[
D_\Pi=(I-P)KP.
]


Lemma 1 — Exact rank-one factorization


Let
[
u=e_a-e_b.
]


Then
[
D_\Pi


\frac12
(e_a-e_b)
\left[
(e_{T(a)}-e_{T(b)})^TP
\right].
]


Equivalently,
[
D_\Pi


\frac12
(e_a-e_b)
\left[
P(e_{T(a)}-e_{T(b)})
\right]^T.
]


Corollary 1 — Universal rank bound


For every finite deterministic map T,
[
\boxed{\operatorname{rank}D_\Pi\le1.}
]


Corollary 2 — Exact zero/nonzero criterion


[
\boxed{
\operatorname{rank}D_\Pi=0
\iff
T(a),T(b)
\text{ belong to the same }\Pi\text{-block}.
}
]


Otherwise
[
\boxed{\operatorname{rank}D_\Pi=1.}
]


Cycle specialization


For
[
X=\mathbb Z/k\mathbb Z,
\qquad
T(i)=i+1\pmod{k},
]
and
[
\Pi={{0,d}}\cup{{x}:x\notin{0,d}},
\qquad
1\le d\le k-1,
]
we have
[
T(0)=1,
\qquad
T(d)=d+1\pmod{k},
]
and these lie in distinct \Pi-blocks.


Therefore
[
\boxed{\operatorname{rank}D_\Pi=1.}
]


BRT agreement


The BRT forward constraint graph has m=k-1 vertices and exactly one edge joining the two target blocks containing 1 and d+1. Hence
[
c(\Gamma)=k-2.
]


Using the frozen BRT identity
[
\operatorname{rank}D_\Pi=m-c(\Gamma),
]
we obtain
[
\operatorname{rank}D_\Pi
=(k-1)-(k-2)=1.
]


Thus the direct operator factorization and the BRT graph calculation agree exactly.


Scope


The rank-\le1 theorem is proved for every finite map T whenever the partition has exactly one doubleton and all remaining blocks are singletons.


The cycle-specific one-edge statement is proved independently from the cycle structure.


No computational census is required for either theorem.


Lean formalization remains OPEN.

