# claims

## Purpose
Claim records — machine-readable statements of mathematical claims and their hub-level replay status.

## Current Files — Live 4 minutes ago
- `sv-001-v2.json` — trace=2m alpha^2, op-norm even 2alpha odd 2alpha cos(pi/2m)
    - evidence: 5720 cases
    - current_hub_status: artifact_present_in_this_repository false, replayable_from_this_repository false, independence_established false
    - disposition: REPLAY_BLOCKED_MISSING_ARTIFACT, governance C4=BLOCKED

## Evidence Semantics
A file in claims/ does not mean the claim is proved. It means the claim is declared and its replay status is tracked.

- AVAILABLE: declared
- EXECUTED: ran in CI
- REPRODUCED: output_match
- INDEPENDENTLY_REPRODUCED: REPRODUCED + independence basis
- FORMALIZED / PROVED: requires Lean + checked proof

Current hub correctly blocks SV-001-V2 because VERIFICATION/sv001_v2_check.py is absent and external pin contains synthetic placeholder section. This is honest quarantine, not refutation.
