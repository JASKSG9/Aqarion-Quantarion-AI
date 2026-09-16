JASKSG9/Aqarions-Quantarion-AI/
│
├── .github/
│   └── workflows/
│       └── verify.yml
│
├── source/
│   └── python/
│       └── claimlock.py
│
└── verification/
    ├── README.md
    ├── requirements.txt
    ├── manifest.json
    │
    ├── run_all.py
    ├── replay_harness.py
    ├── verify_paths.py
    ├── verify_registry_schema.py
    ├── verify_hashes.py
    ├── verify_repository.py
    ├── provenance.py
    │
    ├── adversarial/
    │   ├── __init__.py
    │   ├── forged_pass.py
    │   ├── stale_root.py
    │   ├── wrong_hash.py
    │   ├── self_comparison.py
    │   └── missing_execution.py
    │
    └── fixtures/
        ├── c3_n8.json
        ├── c3_n14.json
        └── k2r_family.json
