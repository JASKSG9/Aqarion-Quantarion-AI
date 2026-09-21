AQ-DYN Semantic Identity Lock


Mandatory distinction


AQARION recognizes two non-equivalent operators.


Forward operator


[
T_*^{+}(P)


\operatorname{EqvGen}
{(Tx,Ty):(x,y)\in P}.
]


This generates forward-compatible equivalences and is associated with unary-algebra congruence semantics.


Pullback operator


[
T_*^{-}(E)


T^{-1}(E)


{(x,y):(Tx,Ty)\in E}.
]


Its iterative closure is


[
E_{j+1}


\operatorname{EqvGen}
(E_j\cup T^{-1}(E_j)).
]


These operators MUST NOT share an unqualified identifier.


Required registry fields


Every dynamic-closure claim MUST contain:


{
  "operator_direction": "FORWARD_IMAGE | PULLBACK",
  "operator_definition_hash": "...",
  "closure_rule_hash": "...",
  "partition_semantics": "...",
  "implementation_hash": "...",
  "evidence_definition_hash": "..."
}



Promotion invariant


No evidence may be used for promotion when


[
\texttt{evidence_definition_hash}
\ne
\texttt{claim.operator_definition_hash}.
]


A direction change creates a new semantic claim identity.


It is not a revision of the old claim.


Current status


AQ-DYN-GRAPH-ORBIT-001:
KILLED.


AQ-DYN-FWD:
definition retained; previous forward-closure results remain separately addressable.


AQ-DYN-PULL:
current computational submodularity evidence belongs here.


Dynamic-closure submodularity under PULLBACK:
COMPUTATIONALLY SUPPORTED; ANALYTIC PROOF OPEN.


No promotion.

