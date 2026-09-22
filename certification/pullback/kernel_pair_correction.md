Kernel-pair correction for pullback stability


Definitions


For an equivalence relation E on X, let


[
q_E:X\to X/E
]


denote the quotient map.


Its kernel pair is


[
\ker(q_E)=E.
]


For a deterministic map


[
T:X\to X,
]


the pullback relation is


[
T^{-1}(E)


{(x,y): (Tx,Ty)\in E}.
]


Therefore


[
T^{-1}(E)


\ker(q_E\circ T).
]


This is the correct categorical representation.


Backward stability


The condition


[
T^{-1}(E)\le E
]


is therefore


[
\ker(q_E\circ T)
\le
\ker(q_E).
]


It says that the observable equality represented by E is not destroyed when pulled backward through T.


It does not imply


[
E\le T^{-1}(E).
]


The latter is the forward-preservation direction and requires a separate hypothesis.


Backward closure


Define


[
F_T(E)=E\vee T^{-1}(E).
]


Iterate:


[
E_0=E,
\qquad
E_{j+1}=E_j\vee T^{-1}(E_j).
]


Because the partition lattice of a finite set is finite, this sequence stabilizes.


The stable relation is the least backward-stable equivalence relation containing E.


Research status


The finite stabilization statement is structural.


The stronger join-stability claims being investigated for AQARION remain separate.


Evidence:


[C1] algebraic structure


[SUP] finite computational support


[O] general join-stability proof


No quotient-bijection theorem is used.

