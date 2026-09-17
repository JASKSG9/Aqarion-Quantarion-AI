# AQARION-ARITHMETIC

## Current Research Status — 2026-09-17

**Status:** RESEARCH ACTIVE — CLAIM-SPECIFIC EVIDENCE RECONCILIATION IN PROGRESS

**ARCH-369:** WORK IN PROGRESS

**Publication status:** NOT A GLOBAL REPOSITORY LABEL

**Lean:** OPTIONAL FORMALIZATION INFRASTRUCTURE

---

## Canonical Four-Digit Baseline

The canonical four-digit non-repdigit domain is

\[
X =
\{1000,\ldots,9999\}
\setminus
\{1111,\ldots,9999\},
\]

with

\[
|X|=8991.
\]

The canonical gap observable is

\[
\pi(n)=(a-d,b-c)
\]

for sorted digits \(a\ge b\ge c\ge d\).

The canonical gap quotient contains

\[
|G|=54
\]

states.

The induced dynamics satisfies

\[
\pi\circ K=T_G\circ\pi.
\]

The canonical attracting state is 6174, corresponding to gap state

\[
(6,2).
\]

The current quotient image chain is

\[
54\rightarrow20\rightarrow14\rightarrow10
\rightarrow7\rightarrow4\rightarrow1.
\]

The full-system maximum depth is 7 and the quotient depth is 6.

---

## Important Terminology

The canonical Kaprekar gap quotient is the **54-state** system.

Historical/auxiliary **55-state FOQDS** constructions are separate objects
and must not be conflated with the canonical gap quotient.

---

## Chamber Status

The affine-chamber count remains under reconciliation.

Historical repository material contains conflicting chamber counts.

Therefore the chamber count is currently:

**OPEN**

No chamber count is represented here as a frozen theorem.

---

## Evidence Policy

AQARION distinguishes:

- definition
- analytic proof
- computational verification
- independent verification
- formal verification
- counterexample
- refutation
- conjecture
- open problem
- historical material
- quarantine

A computation is not silently upgraded to a proof.

A Lean source file is not silently upgraded to a formal receipt.

A historical checkpoint is not silently upgraded to current truth.

---

## Research Direction

Current priority is repository reconciliation:

1. synchronize definitions;
2. remove stale completion claims;
3. reconcile state-space conventions;
4. separate 54-state and 55-state constructions;
5. quarantine unresolved chamber claims;
6. synchronize claim/theorem registries;
7. preserve historical checkpoints without presenting them as current.

New theory and implementation work follows after this reconciliation pass.

https://github.com/JASKSG9

https://huggingface.co/Quantarion9
