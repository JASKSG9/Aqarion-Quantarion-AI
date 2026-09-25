# Aqarions-Quantarion-AI — Repository Snapshot

Date: 2026-09-17

## Snapshot identity

Repository:

JASKSG9/Aqarions-Quantarion-AI

Branch:

main

HEAD:

a7decb9bf00cbf1cfc92313b6dcd4c795c10645a

HEAD tree:

62954365caf42670beae1ee051beaa464be83477

This file is a repository-state snapshot.

The Git tree at the stated HEAD is authoritative.

This document MUST NOT be treated as authoritative for filesystem existence
when its recorded HEAD differs from the checked-out HEAD.

## Verification surface observed at this HEAD

.github/
└── workflows/
    └── verify.yml

verification/
├── manifest.json
├── run-all.py
├── provenance.py
├── aq_mutation-suit.py
├── aq_oracle/
│   └── aq_independent_oracle_suite.py
├── aq_contract/
│   └── aq_contract_semantic_suite.py
└── aq_s14/
    └── aq_s14_semantic_suite.py

## Live CI state

Latest observed workflow run for this HEAD:

AQARION Replay #94

Conclusion:

FAILURE

Failure boundary:

verification/aq_mutation_suite.py

The workflow requested the path:

verification/aq_mutation_suite.py

The actual executable present at this HEAD is:

verification/aq-mutation-suit.py

Therefore the mutation stage did not execute.

The preceding finite checks did execute successfully:

AQ-S14 semantic suite
AQ contract semantic suite
AQ independent exhaustive oracle

The canonical run-all receipt was skipped because the workflow stopped at
the mutation-suite path failure.

## Governance rule

Git tree > generated snapshot > README prose.

A historical snapshot remains valid as historical evidence when its recorded
HEAD is preserved, but it MUST NOT be labeled CURRENT after HEAD changes.

## Evidence distinction

A successful workflow run establishes the execution result of the registered
checks at the exact checked-out revision.

It does not by itself establish:

- a universal mathematical theorem;
- independent reproduction;
- formal verification;
- publication readiness.

## Next required repair

Repair the workflow caller to invoke the executable that actually exists:

verification/aq-mutation-suit.py

Then obtain and inspect the resulting workflow run before renaming or
restructuring the mutation suite.

filetree.md — Aqarion-Quantarion-AI
Root: https://github.com/JASKSG9/Aqarion-Quantarion-AI
Branch: main
Commit: 94bcefba5032afe4ab6ab3ac917b15969c7848f4 (observed 2026-09-25)
Stars: 3 / Commits: 542
Governance: C3 OPEN / C4 BLOCKED / Lean OPEN / SDS-002 QUARANTINED / Publication BLOCKED / Promotable false
License: Apache-2.0
Purpose: Canonical case-sensitive root inventory — repository truth, not mathematical truth.
Generated from live GitHub search + your mobile screenshots (2026-09-25).
No rename, no case normalization. Git/GitHub/Linux are case-sensitive.
Root — Directories (19)

.github/workflows/               # 4 days ago — CI workflowsAI/                              # 19 hours ago — JOIN-STABILITY, verification etc.Aqarion-Lean/                    # 4 days ago — Lean toolchain + Pending/Killed/MARKDOWNS/ScriptsDASHBOARDS/                      # 5 days agoHOOKS/                           # last weekapi/                             # last weekcertification/                   # 3 days ago — substantial subsystemclaims/                          # last weekcrate/                           # last weekdocs/                            # last weeklibrary/support/september/       # last week — resolves truncated library/support/septem... from screenshotobjects/                         # last weekpdf/                             # last weekprojects/                        # last weekschemas/                         # last weekskills/                          # last week — minimal live surface (aq-skill-001.json + readme.md observed historically)source/data/                     # last weektests/                           # last weekverification/                    # 5 days ago — adversarial, aq_s14, aq_contract, aq_oracle, k2r, etc.
Root — Files (14)

.gitignore                       # last weekCHANGELOG.md                     # last weekCONVENTIONS.md                   # last week — defines [D][V][P][PV][C][R][F][Q][H]LICENSE                          # last week — Apache-2.0POLICY-LOCK.md                   # last weekPullbackStableJoin.lean          # 4 days ago — ROOT INVALID UNRESTRICTED THEOREM → KILLED/HISTORICAL, DO NOT IMPORTREADME.md                        # 5 days agoTermux-check-2026-9-19.md        # last week — resolves Termux-check-2026-9-1... truncatedaqarion.toml                     # last week — declares workflow pathcross-repo-manifest.json         # last week — pinned commitsfiletree.md                      # last week — THIS FILE (self-referential)readme-light.md                  # last week — lower-case name, preserverequirements.txt                 # last week
Combined Canonical Tree (copy-paste)
text
.├── .github/│   └── workflows/               # Aqarion-ci.yml, aqarion-ci.yaml, aqarion-gap-lean-ci.yml, sv-001-v2.yml, etc.├── AI/                          # JOIN-STABILITY/ etc.├── Aqarion-Lean/│   ├── lakefile.lean│   ├── lean-toolchain           # v4.14.0 observed live│   ├── AqarionLean.lean│   ├── AqarionLean/│   ├── Pending/                 # exact case — not pending│   ├── Killed/                  # exact case│   ├── MARKDOWNS/               # exact case│   ├── Scripts/                 # exact case│   └── SESSION-RECORD.md├── DASHBOARDS/├── HOOKS/├── api/├── certification/               # active subsystem├── claims/                      # claim registry├── crate/├── docs/├── library/│   └── support/│       └── september/├── objects/├── pdf/├── projects/├── schemas/├── skills/                      # minimal live: aq-skill-001.json + readme.md├── source/│   └── data/├── tests/├── verification/                # aq_s14, aq-conditioning, aq_contract, aq_oracle, AQARION-GAP, k2r, sv-001-v2, etc.├── .gitignore├── CHANGELOG.md├── CONVENTIONS.md├── LICENSE├── POLICY-LOCK.md├── PullbackStableJoin.lean      # HISTORICAL / KILLED — unrestricted version├── README.md├── Termux-check-2026-9-19.md├── aqarion.toml├── cross-repo-manifest.json├── filetree.md├── readme-light.md└── requirements.txt
Critical Case-Sensitivity Audit
Aqarion-Lean ≠ aqarion-lean ≠ AQARION-LEAN — live is Aqarion-Lean
Pending ≠ pending / PENDING — live is Pending
Killed ≠ killed — live is Killed
MARKDOWNS / Scripts — exact caps as observed
DASHBOARDS / HOOKS — all caps live
api / certification / claims / crate / docs — lower-case live
POLICY-LOCK.md vs CONVENTIONS.md — both upper + .md lower
readme-light.md is lower-case while README.md is upper — preserve both
Build Contract — Where to Build
bash
git rev-parse --show-toplevelgit status --shortgit branch --show-currentgit rev-parse HEAD  # should be 94bcefba...
# exact tree, no truncationgit ls-tree -r --name-only HEAD | sort > /tmp/full_tree_AQ_QAI.txtwc -l /tmp/full_tree_AQ_QAI.txtcat /tmp/full_tree_AQ_QAI.txt
# Lean target (from live repo)cd Aqarion-Leancat lean-toolchain   # expect leanprover/lean4:v4.14.0cat lakefile.leanlake --versionlean --versionlake build           # fundamental test, not `lean SomeFile.lean` alone
Disposition Notes (from live search + README)
PullbackStableJoin.lean at root: theorem pullback_stable_join {α : Type} with NO finiteness hypothesis — INVALID UNRESTRICTED. Mark as HISTORICAL / KILLED formalization candidate. Canonical finite theorem lives in AI/JOIN-STABILITY/JOIN_STABILITY_PROOF.md [P] candidate, Lean OPEN.
aqarion.toml says workflow = ".github/workflows/sv-001-v2.yaml" but live observed is sv-001-v2.yml — mismatch flagged for Research OS contradiction detector.
verification/ is major subsystem: aq_s14, aq-conditioning, aq_contract, aq_oracle, AQARION-GAP, adversarial tests, k2r, sv-001-v2 (1176-case canonical domain, 5720 deprecated).
skills/ minimal live — 12-skill catalogue is proposed architecture, not live.
Governance badges: license Apache-2.0 / C4 BLOCKED / Lean OPEN / SDS-002 QUARANTINED — engagement badges are communication metadata, not mathematical evidence.
Verification Command for This File
bash
sha256sum filetree.md# expected after you commit: record hash in MANIFEST.json
Governance remains:

C3: OPENC4: BLOCKEDLean: OPENPublication: BLOCKEDPromotable: falseReceipts are runtime artifacts — do not commit receipt/latest.json
Do not promote on filetree generation alone. Filetree = repository truth layer, separate from computational truth and mathematical truth.

https://github.com/JASKSG9/Aqarion-Quantarion-AI
