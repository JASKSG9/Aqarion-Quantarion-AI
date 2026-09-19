# AQARION × QUANTARION — CONVENTIONS.md
# Repository: JASKSG9/Aqarions-Quantarion-AI
# Status: CANONICAL DRAFT for freeze · C4 BLOCKED · Promotion false
# Purpose: Single source of truth for parameter roles, matrix constructions,
#          evidence labels, and governance vocabulary. Prevents semantic-type
#          errors (especially m ↔ k swaps).

================================================================================
0. SCOPE
================================================================================

This file freezes conventions used by:

  - verification/sv-001-v2/  (cyclic block-shift defect, 1176-case contract)
  - verification/manifest.json
  - POLICY-LOCK.md
  - claim records under claims/
  - CI workflows under .github/workflows/

It does NOT prove theorems. It defines what symbols mean so that
computational evidence and formal targets stay aligned.

================================================================================
1. EVIDENCE LABELS (do not inflate)
================================================================================

  [D]   DEFINED          — statement fixed; not yet computed/proved
  [V]   VERIFIED         — finite computational replay passed under contract
  [P]   PROVED           — mathematical proof (hand or formal) accepted
  [PV]  PROVED+VERIFIED  — both
  [C]   CONJECTURE
  [R]   RESEARCH / exploratory
  [F]   REFUTED / KILLED
  [Q]   QUARANTINED
  [H]   HISTORICAL       — superseded; do not use as live domain

Rules:
  - Green CI ≠ [P]
  - Receipt hash ≠ mathematical truth
  - Matching outputs ≠ independent reproduction
  - Lean source without checker receipt ≠ FORMALLY VERIFIED
  - public ≠ certified
  - runnable ≠ verified

================================================================================
2. GOVERNANCE STATE (current)
================================================================================

  C3              OPEN
  C4              BLOCKED
  Lean            OPEN
  SDS-002         QUARANTINED
  Publication     BLOCKED
  Promotable      false

POLICY-LOCK.md is authoritative for promotion rules.
CLAIMLOCK answers policy satisfaction, not mathematical truth.

================================================================================
3. SV-001-V2 PARAMETER ROLES (CRITICAL — DO NOT SWAP)
================================================================================

Live package convention (contract.json + verifier build_U):

  m   = number of blocks          (Gram / Laplacian dimension)
  k   = block size                (states per block)
  n   = m * k                     (total states)
  s   = cyclic shift              (integer, 1 <= s <= n-1)
  r   = s mod k                   (within-block residue / leakage)

Blocks:
  B_j = { j*k, j*k+1, ..., j*k + k - 1 }   for j = 0 .. m-1

FORBIDDEN alternate naming in this package:
  Do NOT write k "number of blocks" or m "block size" inside SV-001-V2.
  That swap was the source of earlier formula-confusion audits.

Dual presentation (for external papers only):
  If a derivation uses "k blocks of size m", translate by
    m_repo = k_paper,   k_repo = m_paper
  before comparing to the package oracle.

================================================================================
4. MATRIX CONSTRUCTIONS (SV-001-V2)
================================================================================

U  (n by m):
  U[x, j] = 1/sqrt(k)  if floor(x / k) == j
  U[x, j] = 0          otherwise
  Columns are orthonormal: U^T U = I_m

Q:
  Q = U U^T
  Orthogonal projector onto block-constant functions
  Q^2 = Q,  Q^T = Q

K  (n by n):
  K[x, (x + s) mod n] = 1
  (permutation matrix of the cyclic shift; Koopman/composition orientation)

D:
  D = (I - Q) K Q
  Residual / defect operator

S  (m by m):
  S[i, (i + 1) mod m] = 1
  Cyclic shift on the block index set

L:
  L = 2I - S - S^T
  Cycle Laplacian on m nodes

================================================================================
5. SV-001-V2 IDENTITIES (package form)
================================================================================

  alpha^2 = r * (k - r) / (k * k)

  Gram identity:
    U^T D^T D U  =  alpha^2 * L

  Trace identity:
    tr(U^T D^T D U)  =  2 * m * alpha^2

  Frobenius (same under this normalization):
    ||D||_F^2  =  2 * m * alpha^2

  Rank:
    rank(D) = 0        if r = 0
    rank(D) = m - 1    if 0 < r < k

  Operator norm:
    ||D||_2 = 2 * sqrt(alpha^2)                         if m even
    ||D||_2 = 2 * sqrt(alpha^2) * cos(pi / (2*m))       if m odd

  Nilpotency (always):
    D^2 = 0
    (follows from Q^2 = Q; independent of cyclicity)

  Residue metamorphic:
    G(m, k, s) = G(m, k, s + q*k)   whenever both shifts are in domain
    (residual geometry depends only on r = s mod k)

Domain:
  m, k in {2, ..., 8}
  s in {1, ..., m*k - 1}
  Total cases: 1176
  Zero-residue (r = 0): 196
  Nonzero-residue: 980

Deprecated:
  Historical domain size 5720 is REJECTED. Never execute or cite as live.

Tolerance (float path):
  absolute 1e-12, relative 1e-12
  NaN / Inf comparisons must fail closed.

================================================================================
6. GENERAL DEFECT OPERATOR (beyond SV-001)
================================================================================

For arbitrary finite map T and orthogonal projector P onto a subspace V:

  D = (I - P) K P

Always:
  D^2 = 0

  D = 0  iff  K(V) subset V
           iff  the partition (or subspace) is forward-invariant
           (recovers strong lumpability / exact observable quotient at zero)

Residual rank is the graded obstruction (dimension of leakage).

Do not conflate:
  rank(D)          with   rank(partition) = n - |blocks|
  residual energy  with   combinatorial cycle counts without stated normalization

================================================================================
7. EVIDENCE / REPLAY OBJECTS
================================================================================

Reproduction predicates (separate axes):
  CLAIM, SPECIFICATION, SOURCE, IMPLEMENTATION, FIXTURE,
  EXECUTION, OUTPUT, COMPARISON, INDEPENDENCE, FORMAL STATUS, DRIFT

Receipt rules:
  - Generated at runtime; not committed as "latest.json" if policy forbids
  - Must bind: commit SHA, contract hash, manifest hash, exit code
  - Valid hash ≠ semantic correctness
  - external_independent_reproduction remains false until a second environment
    matches hashes on the same commit

Manifest rules:
  - Every command path in verification/manifest.json must exist on disk
  - Missing artifact = FAIL (fail-closed)
  - NOT_IMPLEMENTED = FAIL

================================================================================
8. PATH / FILENAME DISCIPLINE
================================================================================

Case-sensitive. Linux / GitHub exact match required.

Known risk class (fix when present):
  aq-mutation-suit.py   vs   aq_mutation_suite.py
  repo-self-audit.py    vs   repo_self_audit.py
  run-all.py            vs   run_all.py
  reciept/              vs   receipts/

Single source of truth:
  Disk filename wins. Manifest and workflow must be edited to match disk,
  not the other way around, unless a deliberate rename is committed.

================================================================================
9. SEMANTIC MUTATION TAXONOMY (recommended depth)
================================================================================

Weak (current-style): corrupt expected oracle values (wrong_trace, wrong_norm, …).

Strong (target): mutate construction and require verifier kill:

  U_parameter_swap      m/k role inversion in build_U
  U_wrong_scale         1/sqrt(k) vs 1/sqrt(m) or unnormalized
  U_wrong_block_index   floor(x/k) vs floor(x/m)
  K_transpose           shift sign / orientation
  K_off_by_one
  residue_mod_m         s mod m instead of s mod k
  D_wrong_order         QKQ, KPQ, etc.
  S_wrong_dimension

Success = full verifier fails the mutant (not a hand-coded expect).

================================================================================
10. WHAT THIS FILE IS NOT
================================================================================

  - Not a theorem proof
  - Not a C4 unlock
  - Not a publication claim
  - Not a substitute for Lean
  - Not authority over other repositories unless they explicitly adopt it

================================================================================
11. CHANGE CONTROL
================================================================================

Any change to sections 3–5 (SV-001 roles or identities) requires:
  1. Contract version bump
  2. Re-run of the 1176-case verifier
  3. New receipt bound to the committing SHA
  4. Explicit note in claims/sv-001-v2.json

Do not silently rename m/k inside code without updating this file and the contract.

================================================================================
END CONVENTIONS.md
