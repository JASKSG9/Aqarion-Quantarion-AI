# Aqarions-Quantarion-AI

![License](https://img.shields.io/badge/license-Apache--2.0-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-3776AB)
![C3](https://img.shields.io/badge/C3-OPEN-yellow)
![C4](https://img.shields.io/badge/C4-BLOCKED-red)
![Lean](https://img.shields.io/badge/Lean-not%20compiled-lightgrey)
![SDS--002](https://img.shields.io/badge/SDS--002-QUARANTINED-orange)
![Publication](https://img.shields.io/badge/publication-BLOCKED-red)
![Promotable](https://img.shields.io/badge/promotable-false-lightgrey)
![CLAIMLOCK](https://img.shields.io/badge/CLAIMLOCK-policy%20kernel-blueviolet)

Governance, policy, and cross-repo orchestration hub for the AQARION / Quantarion research corpus.

This repository is a **hub**, not a self-contained mathematical library. It defines promotion policy (CLAIMLOCK), declares the layout of sibling AQARION repositories, and enforces a strict separation between idea, computation, replay, formalization, and certification.

---

## Status

```

Governance:
C3 ............. OPEN        (active research)
C4 ............. BLOCKED     (publication gate closed)
Lean ........... OPEN        (no compiled kernel receipts)
SDS-002 ........ QUARANTINED (semantic-drift surface under audit)
Publication .... BLOCKED
Promotable ..... false

```

No claim in this hub, or in any branch it references, is currently authorized for external submission.

---

## What this repository is

A **branching hub** that:

1. **Declares** the layout of the AQARION/Quantarion research corpus across sibling repositories.
2. **Evaluates** promotion policy via the CLAIMLOCK kernel — given a claim's evidence items and a promotion request, it authorizes or refuses the promotion.
3. **Orchestrates** verification runs across declared branches, producing receipts.
4. **Enforces** the discipline that no promotion happens without policy-compliance checks.

---

## What this repository is NOT

- It is **not** a verifier of mathematical truth. The CLAIMLOCK kernel decides whether *policy allows* promotion, not whether a claim is *mathematically correct*.
- It does **not** compile Lean. No Lean toolchain is vendored.
- It does **not** perform cryptographic signing or Sigstore/Rekor inclusion.
- It does **not** contain the AQARION defect-operator mathematics. That lives in `AQARION-ARITHMETIC-FDS-*`.
- It does **not** clear C4, SDS-002, or publication. Those gates remain blocked by governance.

---

## Repository contents

```

Aqarions-Quantarion-AI/
├── README.md
├── LICENSE                          (Apache 2.0)
├── requirements.txt                 (pytest only)
├── project/
│   └── Project.toml                 (package config)
├── source/
│   └── python/
│       └── claimlock.py             (CLAIMLOCK policy kernel)
├── verification/
│   ├── run-all.py                   (orchestrator)
│   ├── replay-harness.py            (compatibility wrapper)
│   └── mainfest.json                (manifest — see known issues)
├── docs/
│   ├── logs/
│   │   └── aq-s16.txt               (governance status)
│   └── markdowns/
│       └── executable-surface-migration.md
└── .github/
└── workflow/
└── verify.yml               (CI: runs verification/run-all.py)

```

Planned but not yet implemented: `AQARION-CORE/`, `AQARION-LAKE/`, `AQARION-SKILLS/AQARION-REPLAY-LAB/`, `QUICKSTART/`, `EXAMPLES/`, `claims/`, `engines/`, `fixtures/`, `receipts/`, `lean/`.

If you expect a mathematical verifier here, look in `JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-` instead.

---

## CLAIMLOCK kernel

**File:** `source/python/claimlock.py`

CLAIMLOCK is a **policy evaluator**. Given:

- a **claim** (JSON) with a list of evidence items, each carrying a scope, exactness flag, formalization flag, and independent-check flag,
- a **policy** (JSON) declaring the minimum scope rank and required evidence flags for a requested promotion,

it emits a receipt with outcome one of:

| Outcome | Meaning |
|---------|---------|
| `ALLOW` | Requested promotion is authorized by policy |
| `CL_SCOPE_INSUFFICIENT` | Claim's strongest evidence scope is below the policy minimum |
| `CL_MISSING_EVIDENCE` | A required evidence flag is absent |
| `CL_EXACT_COMPUTATION_MISSING` | Policy requires exact computation; none present |
| `CL_FORMALIZATION_MISSING` | Policy requires formalization; none present |
| `CL_INDEPENDENT_CHECK_MISSING` | Policy requires independent check; none present |

CLAIMLOCK explicitly does **not**:

- decide whether a mathematical statement is true,
- validate a SHA-256 digest against real artifact bytes,
- perform Lean compilation,
- clear SDS-002, C4, or publication.

Policy authorization is orthogonal to mathematical truth. Conflating the two is the failure mode this hub exists to prevent.

---

## Branching architecture

This hub references sibling repositories as **branches**:

| Branch | Repository | Provides |
|--------|------------|----------|
| `aqarion-core` | `JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-` | Defect operator `D_Π = (I−P)KP`, rank formula, trace equivalence |
| `kaprekar` | `JASKSG9/KAPREKAR-SPECTRAL-GEOMETRY` | 55-state Kaprekar quotient, Jordan-block analysis |
| `fibonacci` | `JASKSG9/FIBONACCI-SPECTRAL-DYNAMICS-` | Fibonacci operator dynamics |
| `mandelbrot` | `JASKSG9/MANDELBROT-INFINITE-DYNAMICS` | Escape-time analysis, orbit classification |
| `academy` | `huggingface.co/spaces/Quantarion9/AQARION-ACADEMY` | DEFECT.LEAN, verification harness, checkpoint notes |

**Branch manifest is not yet implemented.** A `cross-repo-manifest.json` declaring each branch's URL, commit pin, and `provides` list is required to make branching auditable. Until that exists, the branching described here is architectural intent, not a frozen dependency graph.

---

## Known issues

### Self-check path mismatch (functional)

`verification/run-all.py` performs a self-check that looks for:

```

verification/run_all.py        (underscore)
verification/replay_harness.py (underscore)
verification/manifest.json     (correct spelling)

```

The actual files are named:

```

verification/run-all.py        (hyphen)
verification/replay-harness.py (hyphen)
verification/mainfest.json     (typo: "mainfest")

```

**Consequence:** the self-check reports three missing files and returns `FAIL`. The CI workflow `.github/workflow/verify.yml` will fail on first push.

**Fix:** rename files to match the checks, or update the checks to match the files. The typo `mainfest.json` → `manifest.json` should be fixed regardless.

### Undefined items (scope)

The following items have been referenced in audit context but are **not defined in this repository, nor in any accessible AQARION repository**:

- `phase lift lemma`
- `voltage cover counterexample`
- `H_T` / `transport graph`
- `C(G-R)`

They must not be cited as AQARION objects until either (a) a definition is committed to a named branch, or (b) they are formally removed from the research ledger.

### Layout description drift

Prior versions of this README described directories (`AQARION-CORE/`, `AQARION-LAKE/`, `AQARION-SKILLS/`, `QUICKSTART/`, `EXAMPLES/`, `DOCS/`) that do not exist in this repository. That description has been replaced with the actual contents listed above. Planned directories are labeled as planned.

---

## Governance rules

The hub enforces four rules at the policy layer:

1. **Evidence scope must meet or exceed the promotion target.** A claim whose strongest evidence is numeric replay cannot be promoted to `FORMAL`.
2. **Exact computation must be present if policy requires it.** Float64 agreement is not exact.
3. **Formalization must be present if policy requires it.** A Lean target file is not a Lean compilation.
4. **Independent check must be present if policy requires it.** Same-implementation self-verification does not count.

These rules exist to prevent specific, observed failure modes: finite-to-universal promotion, numeric-to-formal promotion, aspirational-to-actual promotion, and self-referential verification.

---

## Running the verification orchestrator

```bash
python3 verification/run-all.py
```

Expected current behavior: the self-check reports FAIL due to the path-mismatch issue described above. This is a known bug, not an orchestration problem.

Once the path mismatch is fixed, the orchestrator will iterate the manifest's declared checks and produce a summary receipt.

## Evidence Status

AQARION distinguishes mathematical evidence from software availability.

- `[D]` Definition
- `[V]` Independently verified computation
- `[P]` Formal mathematical proof
- `[PV]` Proof plus independent verification
- `[C]` Conjecture
- `[R]` Research
- `[F]` Refuted / killed
- `[Q]` Quarantined

A public repository, running application, numerical agreement, or generated
certificate does not by itself constitute a mathematical proof.

AI-assisted development is recorded as provenance where applicable. The
system does not claim to determine whether AI was used; it records the
research and verification process.

---

Roadmap

Priority Action
P0 Fix filename mismatches in verification/run-all.py
P0 Rename mainfest.json → manifest.json
P1 Add cross-repo-manifest.json with branch URLs and commit pins
P1 Implement one real mathematical verification module (e.g. D² = 0 exact replay)
P2 Add claims/, fixtures/, receipts/ directories with a first worked example
P2 Define or formally drop phase lift, voltage cover, H_T, C(G-R)
P3 Add a real Lean target in a pinned Lake package

---

Contributing

Before opening a PR:

1. Every new claim must have a corresponding manifest entry.
2. Every new evidence item must declare its scope: NUMERIC, EXACT, FORMAL, or INDEPENDENT.
3. Promotion requests must go through CLAIMLOCK; do not edit governance status flags directly.
4. Do not add aspirational documentation. If a directory does not exist, do not describe it as though it does.
5. Do not add a status badge the repository cannot currently defend.

---

License

Apache 2.0. See LICENSE.

---

Pointers

· Core AQARION mathematics: github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-
· Kaprekar case study: github.com/JASKSG9/KAPREKAR-SPECTRAL-GEOMETRY
· HuggingFace space: huggingface.co/spaces/Quantarion9/AQARION-ACADEMY

---
