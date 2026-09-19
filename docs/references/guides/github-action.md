GitHub Actions Subdirectory Reference
AQARION internal workflow guide
This guide explains how GitHub Actions resolves files stored below a non-root directory such as:
main/verification/
└── aq-condioning/
    ├── README.md
    ├── replay.py
    ├── self_audit.py
    ├── metamorphic.py
    ├── mutation/
    │   └── executor.py
    └── action.yml                 # only if this directory is a composite action
Repository spelling note: This guide uses the path you reported: verification/aq-condioning/. Preserve that spelling exactly in workflow commands. GitHub-hosted Linux runners are case-sensitive and do not correct spelling errors.
1. Required checkout order
A workflow cannot use repository files until it checks out the repository. Put actions/checkout before any run: command that references local files and before any local composite-action reference such as uses: ./main/verification/....
name: AQARION verification example

on:
  workflow_dispatch:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  verify:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Show repository root
        run: |
          echo "GITHUB_WORKSPACE=$GITHUB_WORKSPACE"
          pwd
          ls -la
actions/checkout places the repository in $GITHUB_WORKSPACE, allowing later steps to access committed files. GitHub Actions checkout documentation
2. First determine the real path
The correct path depends on your repository tree. These are different layouts:
Layout A — verification is at repository root
repository-root/
├── .github/workflows/verify.yml
└── verification/
    └── aq-condioning/
        └── replay.py
Use:
verification/aq-condioning/replay.py
Layout B — verification is nested under main/
repository-root/
├── .github/workflows/verify.yml
└── main/
    └── verification/
        └── aq-condioning/
            └── replay.py
Use:
main/verification/aq-condioning/replay.py
Do not guess. Add a temporary discovery step, run it once, and copy the exact path it prints:
- name: Inspect verification tree
  run: |
    echo "Workspace: $GITHUB_WORKSPACE"
    find . -maxdepth 5 -type f | sort
3. Template: relative paths from repository root
Use this when each command starts from the default repository-root working directory. The explicit ./ prefix is optional but recommended because it makes local paths obvious.
Layout A: verification/aq-condioning/
name: AQARION conditioning — relative paths

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  conditioning:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          python -m pip install numpy

      - name: Confirm required files
        run: |
          test -f ./verification/aq-condioning/README.md
          test -f ./verification/aq-condioning/replay.py
          test -f ./verification/aq-condioning/self_audit.py
          test -f ./verification/aq-condioning/metamorphic.py
          test -f ./verification/aq-condioning/mutation/executor.py

      - name: Run self-audit
        run: python ./verification/aq-condioning/self_audit.py

      - name: Run replay
        run: python ./verification/aq-condioning/replay.py

      - name: Run metamorphic checks
        run: python ./verification/aq-condioning/metamorphic.py

      - name: Run mutation checks
        run: python ./verification/aq-condioning/mutation/executor.py
Layout B: main/verification/aq-condioning/
Only the paths change:
- name: Confirm required files
  run: |
    test -f ./main/verification/aq-condioning/README.md
    test -f ./main/verification/aq-condioning/replay.py

- name: Run replay
  run: python ./main/verification/aq-condioning/replay.py
4. Template: working-directory
Use working-directory when several commands operate on the same nested package. It avoids repeating a long path and makes local input/output paths easier to reason about.
Layout A: root verification/
name: AQARION conditioning — working directory

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  conditioning:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          python -m pip install numpy

      - name: Inspect package directory
        working-directory: ./verification/aq-condioning
        run: |
          pwd
          find . -maxdepth 3 -type f | sort

      - name: Run self-audit
        working-directory: ./verification/aq-condioning
        run: python self_audit.py

      - name: Run replay
        working-directory: ./verification/aq-condioning
        run: python replay.py

      - name: Run metamorphic checks
        working-directory: ./verification/aq-condioning
        run: python metamorphic.py

      - name: Run mutation checks
        working-directory: ./verification/aq-condioning
        run: python mutation/executor.py
Layout B: nested main/verification/
- name: Run replay
  working-directory: ./main/verification/aq-condioning
  run: python replay.py
Set a job-wide default
When all run: steps use the same location, reduce repetition:
jobs:
  conditioning:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./verification/aq-condioning

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Run audit
        run: python self_audit.py

      - name: Run replay
        run: python replay.py
Do not place actions/checkout inside a defaults.run.working-directory assumption: uses: steps are actions, not shell commands, and a job-level working directory affects run: steps only.
5. Python invocation choices
Choose one import strategy and keep it consistent.
Strategy A — direct script execution
Use direct script paths when scripts use imports local to their own directory or when the package has not been configured for module execution:
- name: Run replay directly
  working-directory: ./verification/aq-condioning
  run: python replay.py
This is simple, but imports in replay.py must be compatible with direct execution.
Strategy B — module execution
Use module execution when the directory hierarchy contains Python package markers and imports are fully qualified.
Required markers:
verification/__init__.py
verification/aq-condioning/__init__.py
Important: A hyphen (-) is not permitted in a Python module name. Your folder aq-condioning can be used as a filesystem path, but it cannot be imported as:
python -m verification.aq-condioning.replay
That command is invalid.
If you want python -m ..., use an import-safe folder name such as:
verification/aq_conditioning/
Then run:
- name: Run replay as a module
  run: python -m verification.aq_conditioning.replay
If the committed folder is truly named aq-condioning, use direct-script execution with working-directory or a relative path. Do not rename the folder solely to make module imports work unless you intentionally update every manifest and workflow reference.
6. Template: local composite action
A local composite action is not a Python script. It is a directory containing action.yml or action.yaml with runs.using: composite.
Example location:
verification/aq-condioning/actions/run-conditioning/action.yml
Example action.yml:
name: Run AQARION conditioning checks
description: Runs the local conditioning audit, replay, metamorphic, and mutation checks.

runs:
  using: composite
  steps:
    - name: Run self-audit
      shell: bash
      run: python "$GITHUB_WORKSPACE/verification/aq-condioning/self_audit.py"

    - name: Run replay
      shell: bash
      run: python "$GITHUB_WORKSPACE/verification/aq-condioning/replay.py"

    - name: Run metamorphic checks
      shell: bash
      run: python "$GITHUB_WORKSPACE/verification/aq-condioning/metamorphic.py"

    - name: Run mutation checks
      shell: bash
      run: python "$GITHUB_WORKSPACE/verification/aq-condioning/mutation/executor.py"
Workflow usage:
name: AQARION conditioning — composite action

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  conditioning:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository first
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install NumPy
        run: python -m pip install numpy

      - name: Run local conditioning action
        uses: ./verification/aq-condioning/actions/run-conditioning
For a layout nested under main/, use:
uses: ./main/verification/aq-condioning/actions/run-conditioning
The local action path is resolved only after checkout, which is why actions/checkout must come first. GitHub’s checkout action checks the repository into $GITHUB_WORKSPACE, making local committed files available to later workflow steps. GitHub Actions checkout documentation
7. Artifact paths
A script often writes a receipt to a relative output path. That path depends on the script’s current working directory.
Safer approach: write to an explicit workspace path
- name: Run replay and write receipt
  working-directory: ./verification/aq-condioning
  run: |
    mkdir -p "$GITHUB_WORKSPACE/artifacts/aq-condioning"
    python replay.py       --output "$GITHUB_WORKSPACE/artifacts/aq-condioning/receipt.json"

- name: Upload receipt
  uses: actions/upload-artifact@v4
  with:
    name: aq-condioning-receipt
    path: artifacts/aq-condioning/receipt.json
    if-no-files-found: error
If your actual replay script does not accept --output, do not add this command unchanged. First add a documented output argument or use the output path that the script already defines.
8. Minimal path preflight
Put this immediately before your core commands during initial CI setup:
- name: Path preflight
  shell: bash
  run: |
    set -euo pipefail
    echo "Workspace: $GITHUB_WORKSPACE"
    echo "Current directory: $(pwd)"
    test -d "$GITHUB_WORKSPACE/verification/aq-condioning"
    test -f "$GITHUB_WORKSPACE/verification/aq-condioning/README.md"
    test -f "$GITHUB_WORKSPACE/verification/aq-condioning/replay.py"
    test -f "$GITHUB_WORKSPACE/verification/aq-condioning/self_audit.py"
    test -f "$GITHUB_WORKSPACE/verification/aq-condioning/metamorphic.py"
    test -f "$GITHUB_WORKSPACE/verification/aq-condioning/mutation/executor.py"
    find "$GITHUB_WORKSPACE/verification/aq-condioning" -maxdepth 3 -type f | sort
This fails early and clearly if the repository path is wrong.
9. Troubleshooting checklist
10. Local pre-push commands
Run these from the repository root before pushing:
pwd
git rev-parse --show-toplevel
git status --short

find verification/aq-condioning -maxdepth 4 -type f | sort

python3 -m compileall -q verification/aq-condioning

python3 verification/aq-condioning/self_audit.py
python3 verification/aq-condioning/replay.py
python3 verification/aq-condioning/metamorphic.py
python3 verification/aq-condioning/mutation/executor.py

git diff --check
git diff --name-status
If any command fails, do not interpret it as a mathematical failure until you identify whether it is a path, import, dependency, JSON, or runtime-contract problem.
11. Recommended initial workflow
For the reported folder spelling verification/aq-condioning/, this direct-script workflow is the least ambiguous first implementation:
name: AQARION Conditioning Verification

on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  conditioning:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout exact revision
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install runtime dependency
        run: |
          python -m pip install --upgrade pip
          python -m pip install numpy

      - name: Verify local package paths
        run: |
          set -euo pipefail
          test -f verification/aq-condioning/README.md
          test -f verification/aq-condioning/self_audit.py
          test -f verification/aq-condioning/replay.py
          test -f verification/aq-condioning/metamorphic.py
          test -f verification/aq-condioning/mutation/executor.py

      - name: Run self-audit
        working-directory: ./verification/aq-condioning
        run: python self_audit.py

      - name: Run exact-versus-numerical replay
        working-directory: ./verification/aq-condioning
        run: python replay.py

      - name: Run metamorphic checks
        working-directory: ./verification/aq-condioning
        run: python metamorphic.py

      - name: Run mutation checks
        working-directory: ./verification/aq-condioning
        run: python mutation/executor.py
This template is an execution template only. A green workflow would establish that the committed commands completed under the recorded CI environment; it would not establish a formal theorem, independent reproduction, C4 clearance, publication approval, or promotion.
12. Governance boundary
Keep the project status constrained: C4 blocked · publication blocked · promotion false until those independent governance gates are satisfied.
