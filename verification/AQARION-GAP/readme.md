# AQARION-GAP — Exact Gap Identity for the 3-Cycle Support

**Path in repo:** [`verification/AQARION-GAP/`](https://github.com/JASKSG9/Aqarion-Quantarion-AI/tree/main/verification/AQARION-GAP)  
**CI workflow:** [`.github/workflows/aqarion-gap-lean-ci.yaml`](https://github.com/JASKSG9/Aqarion-Quantarion-AI/blob/main/.github/workflows/aqarion-gap-lean-ci.yaml)  
**Status:** Algebraic proof **[P]** · Finite regression **[V]** · Lean formalization **OPEN** · C4 **BLOCKED** · Promotion **false**

---

## One-sentence claim

Under the fixed 3-cycle \(T=(0\ 1\ 2)\) on support \(S=\{0,1,2\}\), for every pair of partitions \(P,Q\) of an \(n\)-set with \(n\ge 3\),

\[
\Delta_d(P,Q)-(c_S-c_G)
=
\begin{cases}
2 & \text{if \(M=P\wedge Q\) is SEP-pure and neither \(P\) nor \(Q\) is SEP-pure},\\
0 & \text{otherwise}.
\end{cases}
\]

This is an **all-\(n\) algebraic identity**, not a census-bounded observation.

---

## What lives in this folder

| File | Role |
|------|------|
| `defs.lean` | `T3`, restriction types (`ALL3` / `PAIR` / `SEP`), purity predicates |
| `restriction.lean` | Restriction to \(S\), meet/join, \(c_S\), \(c_G\), \(c_S\ge c_G\) |
| `defect.lean` | Orbit join \(J_T\), defect \(d_T\), four-way lemma, \(\Delta_d\), gap quantity |
| `gap-identity.lean` | Main theorem + cancellation / inheritance lemmas (case split on \(c_S\)) |
| `aqarion-gap.lean` | Root import + module documentation |
| `lakefile.toml` | Lake package pin (Mathlib) |
| `verify-gap-n6.py` | **Independent** pure-Python exhaustive check for \(n=6\) (no Lean) |
| `stdlib-gap-check.lean` | Optional Lean-side stub / notes for the stdlib regression |
| `filetree.md` | Layout snapshot |
| `subprocess.md` | Notes on subprocess / CI harness expectations |
| `readme.md` | This file (or mirror) |

Flat layout is intentional for the current `verification/` tree. Nested `AQARIONGap/` packages remain compatible if you later promote this to a standalone Lake package.

---

## Mathematical core (locked)

### Definitions (fixed conventions)

- \(S=\{0,1,2\}\), \(T=(0\ 1\ 2)\) extended by identity off \(S\).
- \(J_T(\Pi)=\Pi\vee T(\Pi)\vee T^2(\Pi)\).
- \(d_T(\Pi)=|\Pi|-|J_T(\Pi)|\).
- \(\tau(\Pi)=\) restriction of \(\Pi\) to \(S\).
- \(M=P\wedge Q\), \(U=P\vee Q\).
- \(c_S=|\tau(P)\vee\tau(Q)|\), \(c_G=|\tau(U)|\).
- \(\Delta_d=d_T(P)+d_T(Q)-d_T(M)-d_T(U)\).

### Four-way \(d_T\) table (proved for all \(n\ge 3\))

| Restriction class on \(S\) | \(d_T\) |
|----------------------------|--------:|
| ALL3 (one block) | 0 |
| PAIR (exactly two together) | 1 |
| SEP-pure (blocks exactly \(\{0\},\{1\},\{2\}\)) | 0 |
| SEP-ext (separate blocks, ≥1 carries external points) | 2 |

### Gap identity (proved)

Proof is a finite case analysis on \(c_S\in\{1,2,3\}\):

1. **\(c_S=1\)** — forces \(\tau(U)=\mathrm{ALL3}\), \(d_T(U)=0\), \(c_G=1\); reduces to local types.
2. **\(c_S=2\)** — cancellation \(d_T(U)-c_G=-1\); finite type pairs on the 3-set lattice.
3. **\(c_S=3\)** — pure input forces pure meet; both SEP-ext uses inheritance of extension so \(d_T(U)=c_G-1\).

No dependence on ambient \(n\) beyond \(n\ge 3\).

### Finite regression (supporting, not the proof)

| \(n\) | Partitions \(B_n\) | Unordered pairs | Mismatches |
|------:|------------------:|----------------:|-----------:|
| 6 | 203 | 20 503 | 0 |
| 7 | 877 | 384 126 | 0 (reported) |
| 8 | 4 140 | 8 567 730 | 0 (reported) |
| **Total** | — | **≈ 8.97M** | **0** |

Independent stdlib replay for \(n=6\) is the file `verify-gap-n6.py` in this folder.

---

## How to reproduce

### A. Pure Python (no Lean, no Mathlib) — must stay green

```bash
cd verification/AQARION-GAP
python3 verify-gap-n6.py
```

Expected output (shape):

```text
n=6 partitions=203
pairs_checked=20503
d_T_mismatches=0
gap_mismatches=0
diff_distribution={0: 12157, 2: 8346}
STATUS=PASS
GOVERNANCE: algebraic [P] · finite [V] · Lean [FV] OPEN · C4 BLOCKED
```

### B. Lean / Lake (when toolchain available)

```bash
cd verification/AQARION-GAP
lake update
lake build
```

**Honest expectation today:** the scaffold type-checks with i
... 

---

### What was added

| File | Role |
|------|------|
| `.github/workflows/lean-ci.yml` | Lean/Lake CI: install elan, cache, `lake update` + `lake build`, **sorry inventory**, upload `build.log`, governance banner. Soft-fail while scaffold still has `sorry`. |
| `.github/workflows/stdlib-gap-check.yml` | Pure-Python n=6 gap-rule regression (no Lean). Must stay green. |
| `scripts/verify_gap_n6.py` | Standalone checker: \(B_6=203\), 20 503 pairs, 0 mismatches. **Smoke-tested here: `STATUS=PASS`**. |
| `.gitignore` | Ignores `.lake/`, build artifacts, logs. |
| `README.md` | Updated with CI table + layout. |

### How to use on GitHub

1. Create a new repo (or push this folder as the root).
2. Push to `main` / open a PR → both workflows run automatically.
3. **stdlib job** should be green immediately.
4. **Lean job** will install Mathlib (first run is slow), then either:
   - type-check with intentional `sorry`s (expected while formalization is open), or
   - surface real import/pin errors in the uploaded `build.log`.

### Governance baked into CI

- Sorry count is reported in the job summary.
- Banner always prints: **[FV] not claimed · C4 BLOCKED · promotion false**.
- Build failure is soft by default (scaffold WIP). Flip the commented `exit 1` in `lean-ci.yml` when you want hard fail.

### Local commands

```bash
# No Lean needed — must pass
python3 scripts/verify_gap_n6.py

# When Lean/Mathlib available
lake update && lake build
```

The Lean formalization is no longer “under verification” as a loose pile of files; it is a self-contained package with runnable CI and a regression that already passes.

---

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
