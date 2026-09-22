AQARION Layer 1 — Mutation Detection Receipt


Date: 2026-09-22


Purpose


This receipt records an adversarial mutation test for the Koopman operator convention used by the AQARION defect calculation.


The canonical convention is


[
K_{i,T(i)}=1.
]


The deliberate index mutation is


[
K_{T(i),i}=1.
]


The mutation is intended to be rejected by the same mathematical receipt used to validate the canonical operator.


Result




Test
Result




Canonical Koopman
5000/5000 PASS


Mutant Koopman
0/5000 PASS


Mutation detected
TRUE


Gate
PASS




Interpretation


The test demonstrates that the current BRT rank receipt is sensitive to the known operator-index reversal.


This is verification infrastructure.


It is not a proof of the underlying rank theorem.


Required gate


The test process MUST exit nonzero if:




any canonical trial fails; or


any mutant trial satisfies the canonical receipt.




A printed Mutation DETECTED: TRUE without a nonzero failure path is not a CI gate.


Status


Evidence class: [SUP]


Claim status: verified computational regression


Theorem status: unchanged


Lean status: OPEN


C4 status: BLOCKED


Publication promotion: BLOCKED

