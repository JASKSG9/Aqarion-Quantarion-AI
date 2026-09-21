import Lake
open Lake DSL

package aqarion_lean where
  version := v!"0.1.0"
  description := "AQARION pullback closure and defect operator formalization"
  license := "Apache-2.0"

@[default_target]
lean_lib AqarionLean where
  roots := #[`AqarionLean]
