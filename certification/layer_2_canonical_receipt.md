AQARION Layer 2 — Canonical Verification Receipt


Date: 2026-09-22


Operator convention


[
K_{i,T(i)}=1.
]


All Layer-2 tests use this convention.


R1 — Bipartite rank receipt


[
\operatorname{rank}(D_\Pi)=m-c_{\mathrm{bip}}.
]


Result:


200/200 PASS



Evidence class: [SUP]


R2 — AQ-001


Tested equivalence:


[
D_\Pi=0
\Longleftrightarrow
\Pi\text{ is a congruence}
]


under the tested AQ-001 partition instances.


Result:


0 violations
PASS



Important scope restriction:


This receipt records the tested instances. It does not by itself constitute a universal theorem proof.


Evidence class: [SUP]


R3 — Depth partition


The computed depth partition has zero defect rank.


Result:


rank = 0
PASS



Evidence class: [SUP]


R4 — Frobenius formula


For


[
T(i)=i+s\pmod{mk}
]


and equal blocks of size k,


[
|D|_F^2


\frac{2mr(k-r)}{k^2},
\qquad
r=s\bmod k.
]


The executable parameter ranges are:


k = 2,...,5
m = 2,...,4
1 <= s < mk
s mod k != 0



Total tested cases:


90



Result:


0/90 failures
PASS



Maximum observed absolute numerical discrepancy in independent replay:


6.66e-16



The tolerance used by the test is:


1e-8



Evidence class: [SUP]


Canonical Layer-2 result


R1  200/200 PASS
R2  0 violations PASS
R3  rank=0 PASS
R4  0/90 failures PASS



Layer-2 status:


PASS — computational receipt



This does not promote any result to theorem status.

