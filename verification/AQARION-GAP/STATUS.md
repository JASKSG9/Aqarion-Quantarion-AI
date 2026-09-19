# AQARION-GAP — Status snapshot

**Date:** 2026-09-19  
**Repo path:** `verification/AQARION-GAP/`  
**Workflow:** `.github/workflows/aqarion-gap-lean-ci.yaml`

## Scoreboard

| Item | State |
|------|--------|
| Gap identity (all \(n\ge 3\)) | **[P]** algebraic |
| Four-way \(d_T\) | **[P]** |
| Meet/restriction commutation | **[P]** |
| \(c_S\ge c_G\) | **[P]** |
| Independent n=6 Python regression | **[V]** 0 / 20 503 |
| n=7, n=8 pair checks | Reported [V] (supporting) |
| Lean definitions scaffold | Present |
| Lean proofs fully discharged | **OPEN** |
| CI workflow file present | Yes |
| CI hard-green on Lean proofs | Not required yet |
| C4 | **BLOCKED** |
| Publication | **BLOCKED** |
| Promotion | **false** |

## Diff distribution (n=6, independent)

```text
diff = 0 : 12157 pairs
diff = 2 :  8346 pairs
mismatches to gap rule: 0
```

## Next single highest-value action

Discharge `dT_four_way` in Lean (or the three `cS` cases), one file at a time, without enlarging the census.

## Explicit non-claims

- Not a Kaprekar theorem.
- Not an SV-001 residual-energy theorem.
- Not a formal verification certificate.
- Not a statement about semi-decidable relations on infinite domains.
