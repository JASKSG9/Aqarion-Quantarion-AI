# AQARION Gap Identity — Lean 4 Formalization (AQ-GAP-001)

**Status:** Scaffold complete · Algebraic proof [P] · Lean discharge OPEN · C4 BLOCKED · No promotion

## Statement

Under the fixed 3-cycle \(T = (0\ 1\ 2)\) on support \(S = \{0,1,2\}\), for all partitions \(P,Q\) of a finite set of size \(n \ge 3\),

\[
\Delta_d(P,Q) - (c_S - c_G)
=
\begin{cases}
2 & \text{if \(M\) is SEP-pure and neither \(P\) nor \(Q\) is SEP-pure},\\
0 & \text{otherwise}.
\end{cases}
\]

## File layout

```
AQARION-Gap/
├── lakefile.toml
├── AQARIONGap.lean          # root import + documentation
├── AQARIONGap/
│   ├── Defs.lean            # partitions, T3, RestrType, IsSepPure/Ext
│   ├── Restriction.lean     # restrict, meet/join axioms, cS/cG
│   ├── Defect.lean          # dT, orbitJoin, four-way lemma, gapDiff
│   └── GapIdentity.lean     # main theorem + cancellation lemmas
└── README.md
```

## Proof structure (mirrors paper)

1. **Defs** — `T3`, `RestrType`, purity predicates  
2. **Restriction** — `restrict`, meet/join, `cS ≥ cG`  
3. **Defect** — `dT_four_way` (ALL3→0, PAIR→1, SEP-pure→0, SEP-ext→2)  
4. **GapIdentity** — case split on `cS ∈ {1,2,3}`:
   - `cS = 1`: forces ALL3 on join, reduces to local types  
   - `cS = 2`: cancellation `dT(U) - cG = -1`, finite type pairs  
   - `cS = 3`: pure-input forces pure meet; both-ext uses inheritance lemma  

## Build (when Mathlib available)

```bash
cd AQARION-Gap
lake update
lake build
```

Expected: the file type-checks with intentional `sorry`s marking the remaining combinatorial obligations. No `[FV]` claim until every `sorry` is discharged and the kernel accepts the build.

## Governance

| Item | Status |
|------|--------|
| Algebraic proof (paper) | [P] |
| Lean scaffold | present |
| All `sorry` discharged | OPEN |
| Independent n=6 stdlib replay | [V] 0 mismatches |
| C4 / publication / promotion | BLOCKED / BLOCKED / false |

## Next discharge targets (priority order)

1. `T3_bijective` — already proved in Defs  
2. `dT_four_way` — four short orbit-join computations on the support  
3. `cancellation_cS_two` — PAIR/ALL3 arithmetic  
4. `inherit_sep_ext` — block inheritance under coarsening  
5. Three case branches of `gap_identity`  
6. Replace meet/join axioms with Mathlib `Finpartition` lattice instances when available  

Do not enlarge the computational census. The algebra is closed; formalization is the remaining gate.
