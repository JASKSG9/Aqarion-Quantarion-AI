/-
Copyright (c) 2026 AQARION Research.
Released under Apache 2.0 license.
Authors: AQARION formalization scaffold
-/
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Setoid.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Order.Partition.Finpartition

/-!
# Core definitions for the AQARION gap identity

We work with finite partitions of a finite type `X` with `|X| ≥ 3`.
The distinguished support is the first three elements when `X = Fin n` with `n ≥ 3`.
-/

namespace AQARIONGap

/-- A partition of a finite type, represented as a `Finpartition`. -/
abbrev Partition (X : Type*) [DecidableEq X] [Fintype X] := Finpartition (Set.univ : Set X)

/-- Rank function: number of blocks. -/
def rank {X : Type*} [DecidableEq X] [Fintype X] (P : Finpartition (Set.univ : Set X)) : ℕ :=
  P.parts.card

/-- The distinguished 3-element support indices (for `Fin n`, n ≥ 3). -/
def S3 : Finset (Fin 3) := Finset.univ

/-- The 3-cycle permutation on `Fin 3`: 0 → 1 → 2 → 0. -/
def cycle3 : Equiv.Perm (Fin 3) :=
  Equiv.swap 0 1 * Equiv.swap 1 2
  -- Explicitly: 0↦1, 1↦2, 2↦0
  -- Verify: swap01 then swap12: 0→1→2, 1→0→0, 2→2→1? Need careful construction.

/-- Explicit 3-cycle: 0 → 1, 1 → 2, 2 → 0. -/
def T3 : Fin 3 → Fin 3
  | ⟨0, _⟩ => ⟨1, by omega⟩
  | ⟨1, _⟩ => ⟨2, by omega⟩
  | ⟨2, _⟩ => ⟨0, by omega⟩

/-- `T3` is a permutation (bijective). -/
lemma T3_bijective : Function.Bijective T3 := by
  refine ⟨?inj, ?surj⟩
  · intro a b h
    fin_cases a <;> fin_cases b <;> simp [T3] at h <;> try omega
  · intro b
    fin_cases b
    · exact ⟨⟨2, by omega⟩, rfl⟩
    · exact ⟨⟨0, by omega⟩, rfl⟩
    · exact ⟨⟨1, by omega⟩, rfl⟩

/-- The permutation equivalence for the 3-cycle. -/
def T3Equiv : Equiv.Perm (Fin 3) := Equiv.ofBijective T3 T3_bijective

/-- Local restriction type of a partition of `Fin 3`. -/
inductive RestrType
  | ALL3   -- single block {0,1,2}
  | PAIR   -- exactly one doubleton
  | SEP    -- three singletons
  deriving DecidableEq, Repr

/-- Classify a partition of `Fin 3` by number of blocks (and structure). -/
def classify3 (P : Finpartition (Set.univ : Set (Fin 3))) : RestrType :=
  match P.parts.card with
  | 1 => RestrType.ALL3
  | 2 => RestrType.PAIR
  | _ => RestrType.SEP  -- card = 3 for discrete

/-- Purity: a global partition on `Fin n` (n ≥ 3) is SEP-pure on the support
    `{0,1,2}` when those three points lie in distinct singleton blocks. -/
def IsSepPure {n : ℕ} (hn : n ≥ 3) (P : Finpartition (Set.univ : Set (Fin n))) : Prop :=
  -- The blocks containing 0, 1, 2 are exactly {0}, {1}, {2}
  ∃ (B0 B1 B2 : Set (Fin n)),
    B0 ∈ P.parts ∧ B1 ∈ P.parts ∧ B2 ∈ P.parts ∧
    B0 = {⟨0, by omega⟩} ∧
    B1 = {⟨1, by omega⟩} ∧
    B2 = {⟨2, by omega⟩}

/-- SEP-ext: the three support points are in distinct blocks, but at least one
    of those blocks has an external element. -/
def IsSepExt {n : ℕ} (hn : n ≥ 3) (P : Finpartition (Set.univ : Set (Fin n))) : Prop :=
  -- Distinct blocks for 0,1,2, and not SEP-pure
  (∃ (B0 B1 B2 : Set (Fin n)),
    B0 ∈ P.parts ∧ B1 ∈ P.parts ∧ B2 ∈ P.parts ∧
    (⟨0, by omega⟩ : Fin n) ∈ B0 ∧
    (⟨1, by omega⟩ : Fin n) ∈ B1 ∧
    (⟨2, by omega⟩ : Fin n) ∈ B2 ∧
    B0 ≠ B1 ∧ B1 ≠ B2 ∧ B0 ≠ B2) ∧
  ¬ IsSepPure hn P

end AQARIONGap
