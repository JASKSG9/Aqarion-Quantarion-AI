# IN-MINE DETAILED REPORT - Louisville Night Shift
Generated: 2026-09-18 Termux Android aarch64, awake 3h, Commit dec3700

## Fingerprint
- Python 3.13.13 + NumPy 2.4.4
- Commit dec3700, 20 commits log
- SHA oracle 40558a99f768223aa297..., verifier c8b8d3ee...
- Files: 60 lines semantic_executor, 34 lines residue = 94 total

## L1 Finite [V] - Proven
- oracle 1176 cases / verifier 0 fail / metamorphic old 4/4 PASS
- Receipt hash-bound, finite case enumeration

## L2 Semantic NEW Tonight
- CANONICAL 5/5 PASS
- U_wrong_scale KILLED m!=k err 0.333,0.4,0.25 (scale bug when m!=k)
- U_wrong_block_index KILLED IndexError j=3 out of bounds m=3 = m/k swap bug
- U_residue_mod_m KILLED Gram err
- residue_metamorphic 784/784 PASS G(s)=G(s+qk) m,k 2..8 all r

## L3 Portable
- ro-crate-metadata.json VALID RO-Crate 1.1
- sha256sum verification/sv-001-v2/*.py done (GitHub mobile CANT do this)
- croc 10.4.4 installed 10.4 MB for p2p send crate/ without GitHub

## Defects Found
- manifest 404 aq-mutation-suit.py (disk has semantic_executor.py)
- claims json invalid concat
- contract.json dup object

## Governance
- C4 BLOCKED, publication BLOCKED, promotion false, external_repro false, only[V]

## Next Termux
1. termux-sensor -> live s stream
2. ollama tinyllama -> Lean file
3. qemu-system-x86-64-headless -> second arch
4. croc send crate/ -> share
