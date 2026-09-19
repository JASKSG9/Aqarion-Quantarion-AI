# Changelog

## [2026-09-18] - Termux Lock - Semantic Adequacy Upgrade (94 lines)
### Added
- verification/sv-001-v2/mutation/semantic_executor.py (60 lines)
    - CANONICAL 5/5 PASS
    - U_wrong_scale KILLED when m!=k err 0.333,0.4,0.25
    - U_wrong_block_index KILLED IndexError j=3 out of bounds m=3 (m/k swap bug)
    - residue_mod_m KILLED Gram err
- verification/sv-001-v2/mutation/residue_metamorphic.py (34 lines)
    - G(s)=G(s+qk) ok=784 fail=0 PASS m,k 2..8 all r 1..k-1

### Proven Tonight Louisville Night Shift
- L1 finite [V]: oracle 1176 cases 0 fail, receipt hash-bound
- L2 semantic NEW: 94 lines, construction mutants killed
- L3 portable: RO-Crate 1.1 VALID + sha256sum + croc 10.4.4 p2p

### Environment Fingerprint
- Commit: dec3700 Update contract.json
- Python 3.13.13 + NumPy 2.4.4 Android aarch64 Termux u0_a352
- Governance: C4 BLOCKED, publication BLOCKED, promotion false, external_repro false, [V] only

### Defects Noted
- manifest.json 404 aq-mutation-suit.py (disk has semantic_executor.py)
- claims/sv-001-v2.json invalid JSON concat
- contract.json duplicate object

## [dec3700] Previous - Update contract.json
- Previous state: old mutation only corrupted expected values, not construction
