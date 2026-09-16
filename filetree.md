Aqarions-Quantarion-AI / ROOT FILETREE — 2026-09-16 FROZEN AUDIT
HEAD: 37f281d998450af9f8b1a7731fc0a6e19d8f378a (as reported)
Mode: FROZEN · ADVERSARIAL · NO FABRICATION

Aqarions-Quantarion-AI/│├── .github/│   └── workflows/          # CI gates — must block CERTIFIED if stale│├── api/                    # Federation Hub — https://aqarion-federation-hub--quantarion9.replit.app/│   ├── healthz             # → {"status":"ok"} PASS│   ├── overview            # reports 3 sources, 4 repos, 2 HF assets, 5 claims, 9 projects│   ├── sources│   └── evidence            # reports bootstrapStatus: CERTIFIED, 2/2 tests, verifiedAt=2026-09-11 STALE vs HEAD 2026-09-16│├── schemas/│   └── aro-1.schema.json   # ARO-1 Reproduction Contract — NEW (was missing)│├── objects/│   ├── reproduction-object-001.json          # CURRENT: INVALID_RECEIPT — placeholder hashes "..."│   └── examples/│       ├── R0-unexecuted.json               # UNEXECUTED│       ├── R1-self-reproduction.json        # REPRODUCED_NOT_INDEPENDENT│       ├── R2-independent-shared-bug.json   # INDEPENDENT_REPRODUCTION but SPEC_DRIFT — critical R2 case│       ├── R3-independent-validated.json    # INDEPENDENT_REPRODUCTION + spec validated│       ├── F1-output-drift.json             # REFUTED / RED│       └── F2-spec-drift.json               # SPEC_DRIFT / ORANGE│├── verification/│   ├── aro_verify.py       # FIXED: was rejecting observed==expected (inverted logic)│   ├── provenance.py       # binds source/input/executable hashes│   ├── drift.py            # GREEN/YELLOW/ORANGE/RED/BLACK + freshness attack│   └── independence.py     # separates OUTPUT_AGREEMENT from INDEPENDENCE│├── tests/│   ├── test_aro_schema.py│   ├── test_output_agreement.py│   ├── test_independence.py│   ├── test_drift.py│   ├── test_adversarial_receipts.py         # R0-R3, F1-F2 ladder│   └── test_false_reproduction_ladder.py    # killer test: R2 shared bug != proved│├── skills/│   └── aq-skill-001.json   # CURRENT: EMPIRICALLY_VALIDATED unbound — needs run IDs/logs│├── source/                 # Kaprekar kernel etc — state convention drift: Hub 10000 states vs genuine 8992│├── projects/               # 9 projects reported by Hub│├── docs/│   ├── ARO-1-REPRODUCTION-CONTRACT.md       # NEW — contract spec│   ├── CLAIMLOCK.md│   └── EVIDENCE-LADDER.md  # D,R,V,IV,P,F,G orthogonal│├── .gitignore├── project.toml            # renamed from Project.toml 37f281d — case-sensitive drift risk└── FILETREE.md             # THIS FILE — honest snapshot
# WHERE IS runall.py ?NOT FOUND at root. Search:
find . -name "runall.py" → 0 results (as of screenshot)
RECOMMENDED LOCATION (create if missing):
/verification/runall.py or /tests/runall.py — should execute:  python -m pytest tests/ -v  python verification/aro_verify.py objects/reproduction-object-001.json  python verification/drift.py --compare HEAD vs evidence verifiedAt
See template in docs/ below.
DRIFT DETECTED (2026-09-16)
Hub snapshot asOf 2026-09-11 vs HEAD 2026-09-16 → 5 day stale → FAIL FRESHNESS
State space: Hub reports periodicPoints=2, cycles {0},{6174}, basin 10/9990 = 10000-state convention
vs frozen genuine-state convention X=1000..9999 excluding 9 repdigits |X|=8992 → DEFINITION_ID missing → ORANGE
reproduction-object-001.json hashes = "..." placeholders → BLACK / INVALID_RECEIPT
provenance verifier logic inverted: rejects equality → critical defect
AQ-SKILL-001 baselineRuns 20/20 status EMPIRICALLY_VALIDATED without run IDs → declared not established
EVIDENCE LADDER (FROZEN)
D DEFINED, R REPRODUCED, V VERIFIED, IV INDEPENDENT, P PROVED, F FORMALIZED, G GOVERNED
V ≠ IV ≠ P ≠ F ≠ G. G does not manufacture P.
NEXT REQUIRED ENDPOINTS (not yet /certificate)

/api/reproduction/{id}/api/reproduction/{id}/verify/api/reproduction/{id}/drift/api/reproduction/{id}/lineage
CERTIFIED must remain BLOCKED until ARO-1 GREEN.
