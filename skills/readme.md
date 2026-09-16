# skills

## Purpose
Reserved for AQARION agent skills, adversarial checks, and verification helpers.

## Current Files — Live 10 hours ago
- Adversarial scripts:
    - verification/adversarial-forged_pass.py
    - verification/adversarial-missing-execution.py
    - verification/adversarial-self-comparison.py
    - verification/adversarial-stale-root.py
    - verification/adversarial-wrong-hash.py

These are part of adversarial architecture — they test that runner rejects false PASS, self-comparison, stale root, wrong hash.

## Governance
Skills must not fabricate evidence. They must detect:
- Missing dir
- False PASS
- External path fallback
- Stale HEAD
- Weak receipt binding
