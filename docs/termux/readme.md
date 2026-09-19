# Termux Lab - Louisville Night Shift

Phone lab for Aqarions-Quantarion-AI. GitHub is just storage, this phone is the lab.

## 2026-09-18 Proof
- semantic_executor.py 60 lines: CANONICAL 5/5 PASS + 3 killers KILLED
- residue_metamorphic.py 34 lines: 784/784 G(s)=G(s+qk) PASS
- Total 94 lines semantic adequacy upgrade

## Environment Fingerprint
- Device: Android aarch64 Termux u0_a352
- Python 3.13.13 + NumPy 2.4.4
- Commit dec3700 Update contract.json
- RO-Crate 1.1 VALID crate/ro-crate-metadata.json
- croc 10.4.4 installed for p2p send without GitHub

## Replay Commands (Termux)
python verification/sv-001-v2/mutation/semantic_executor.py
python verification/sv-001-v2/mutation/residue_metamorphic.py
sha256sum verification/sv-001-v2/*.py

## Next Experiments (needs termux-api F-Droid app)
1. termux-sensor -> live s stream -> test G(s) with physical entropy
2. ollama tinyllama -> draft Lean file offline
3. qemu-system-x86-64-headless -> second arch replay same phone
4. croc send crate/ -> share RO-Crate without GitHub
