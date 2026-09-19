AQARION-CONDITIONING File Tree
Canonical package location
verification/aq-conditioning/
The outer folder uses a hyphen because it is a repository path. The inner Python implementation uses an underscore because Python imports cannot use hyphens.
Corrected current tree
verification/aq-conditioning/
├── README.md
├── readme.md
├── FILETREE.md
├── filetree.md
├── CONTRACT.json
├── contract.json
├── .gitignore
├──  TODO.md
│
├── aq_conditioning/
│   ├── __init__.py
│   ├── canonical.py
│   ├── exact_rank.py
│   ├── fixtures.py
│   ├── invariants.py
│   ├── numerical_svd.py
│   ├── replay.py
│   ├── report.py
│   └── self_audit.py
│
├── fixtures/
│   ├── singular_exact.json
│   ├── full_rank_permutation.json
│   ├── near_singular_epsilon.json
│   ├── column_stochastic_kernel.json
│   └── malformed_negative_control.js9n
│
├── schema/
│   ├── fixtures.schema.json
│   └── receipt.schema.json
│
├── verification/
│   ├── manifest.json
│   ├── run_all.py
│   ├── metamorphic.py
│   └── mutation/
│       ├── __init__.py
│       └── executor.py
│
├── docs/
│   ├── benchmark_protocol.md
│   ├── evidence_model.md
│   ├── governance.md
│   └── numerical_boundary.md
│
└── artifacts/
    └── conditioning-receipt.json      # Generated at runtime; normally ignored by Git
Path roles
Required invocation names
From inside verification/aq-conditioning/:
python3 -m aq_conditioning.self_audit
python3 -m aq_conditioning.replay
PYTHONPATH=. python3 verification/metamorphic.py
PYTHONPATH=. python3 verification/mutation/executor.py
Naming warnings
Do not use python -m aq-conditioning...; a hyphen is invalid in Python module syntax.
Do not rename aq-conditioning/ without updating the GitHub Actions workflow.
Do not rename aq_conditioning/ without updating Python imports.
full_rank_permutation.json is the corrected spelling used by the replay fixture path.
malformed_negative_control.js9n has a nonstandard extension and is excluded from canonical replay.
 TODO.md has a leading space in its filename according to the current committed tree; treat any rename as a deliberate, separate cleanup change.
