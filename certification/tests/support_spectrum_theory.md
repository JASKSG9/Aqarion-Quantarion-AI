Support spectrum theorem


Status: conditional theorem package; AQARION realizability gate remains open.


Date: 2026-09-22


1. Scope


This document separates two statements:




an extremal theorem for abstract simple bipartite support graphs;


the stronger claim that every extremal graph required by that theorem is realizable by an AQARION partition-induced support construction.




The first statement is mathematical.


The second requires an AQARION-specific realizability proof and is not promoted here without that proof.



2. Abstract support graph


Let H be a finite simple bipartite graph with


[
s=|E(H)|.
]


Write


[
v=|V(H)|,
\qquad
c=c(H),
\qquad
\beta(H)=s-v+c.
]


For a connected graph,


[
\beta(H)=s-v+1.
]


Define the abstract curvature quantity


[
\kappa(H)=c(H)-1-\beta(H)
]


for the connected support component under consideration.


Using


[
\beta=s-v+1,
]


we obtain


[
\kappa


c-1-(s-v+c)


v-s-1.
]


For a connected support graph this therefore depends only on its vertex count.



3. Bipartite vertex lower bound


If a simple bipartite graph has a vertices on one side and b vertices on the other, then


[
s\le ab.
]


Hence


[
(a-b)^2\ge0
]


gives


[
(a+b)^2\ge4ab\ge4s.
]


Therefore


[
v=a+b\ge\lceil2\sqrt{s}\rceil.
]


Consequently,


[
\beta


s-v+1
\le
s-\lceil2\sqrt{s}\rceil+1.
]


This is the abstract cyclomatic upper bound.



4. Abstract lower envelope


For a connected simple bipartite graph with s edges,


[
\kappa=v-s-1.
]


Since


[
v\ge\lceil2\sqrt{s}\rceil,
]


we obtain


[
\kappa
\ge
\lceil2\sqrt{s}\rceil-s-1.
]


Thus the abstract lower envelope is


[
\boxed{
-s+\lceil2\sqrt{s}\rceil-1
}.
]



5. Abstract upper envelope


A connected bipartite graph with s edges can be realized as a tree whenever s\ge1.


For a tree,


[
v=s+1,
\qquad
\beta=0,
]


and therefore


[
\kappa=s-1.
]


Thus the abstract upper endpoint is


[
\boxed{s-1}.
]



6. Abstract spectrum


The extremal envelope is therefore


[
\boxed{
-s+\lceil2\sqrt{s}\rceil-1
\le
\kappa
\le
s-1.
}
]


This is an abstract simple-bipartite-graph statement.


It is NOT, by itself, the AQARION support-spectrum theorem.



7. Small values




s
abstract lower endpoint
abstract upper endpoint




1
0
0


2
0
1


3
0
2


4
-1
3


5
-1
4




Hence the first possible negative abstract value occurs at


[
s=4.
]


The canonical obstruction is K_{2,2}:


[
s=4,\qquad
v=4,\qquad
\beta=1,
]


giving


[
\kappa=-1.
]



8. AQARION promotion gate


To promote the abstract spectrum to


[
\operatorname{Spec}_s(\kappa_S)


{-s+\lceil2\sqrt{s}\rceil-1,\ldots,s-1},
]


AQARION must establish:




the exact definition of H_S;


that H_S is in the graph class used by the abstract theorem;


that the relevant \kappa_S reduces to the abstract quantity;


realizability of the lower-endpoint constructions;


realizability of every claimed interpolation value;


compatibility with the partition-induced support constraints.




Until these gates are closed, the complete interval is an abstract spectrum, not an AQARION theorem.



9. C3 consequence


The statement


[
s\le3\Longrightarrow\kappa\ge0
]


is valid for the abstract graph model.


An AQARION-specific C3 theorem requires the AQARION support graph to satisfy the hypotheses above.



10. Evidence status


Abstract extremal graph bound: [T]


AQARION support-spectrum realization: [O]


s=4 abstract negative obstruction: [T]


AQARION K_{2,2} realization: [O] until exact construction is bound to the AQARION support definition.


N8/N14 numerical witnesses: [SUP] unless independently bound to the exact formal definitions.


Lean formalization: [O]


Publication promotion: BLOCKED

