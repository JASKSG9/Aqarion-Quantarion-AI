# AQARION-GAP — CI notes for maintainers

## Current GitHub layout (as of screenshots 2026-09-19)

**Sources (flat):**  
`https://github.com/JASKSG9/Aqarion-Quantarion-AI/tree/main/verification/AQARION-GAP`

**Workflow:**  
`https://github.com/JASKSG9/Aqarion-Quantarion-AI/blob/main/.github/workflows/aqarion-gap-lean-ci.yaml`

Observed files in folder (flat, lowercase):

```text
.gitignore
aqarion-gap.lean
defect.lean
defs.lean
filetree.md
gap-identity.lean
lakefile.toml
readme.md
restriction.lean
stdlib-gap-check.lean
subprocess.md
verify-gap-n6.py
```

## Checklist for a working workflow

### 1. Working directory

The job must run inside `verification/AQARION-GAP` (or set `defaults.run.working-directory`).

```yaml
defaults:
  run:
    working-directory: verification/AQARION-GAP
```

Otherwise `lake` will not find `lakefile.toml`.

### 2. Two jobs recommended

| Job | Command | Fail policy |
|-----|---------|-------------|
| `stdlib-n6` | `python3 verify-gap-n6.py` | **Hard fail** if mismatches ≠ 0 |
| `lean-scaffold` | `lake update && lake build` | Soft fail while sorry > 0; hard fail optional later |

### 3. Sorry inventory

```bash
grep -R --include='*.lean' -E '\bsorry\b|\badmit\b' . \
  | grep -v '^\s*--' | wc -l
```

Print this in `$GITHUB_STEP_SUMMARY`. If count > 0, print:

```text
[FV] NOT CLAIMED — sorry > 0 · C4 BLOCKED · promotion false
```

### 4. Python version

Pin `python-version: "3.12"` (or 3.11+). Script uses only the standard library.

### 5. Caching (Lean job)

Cache `~/.elan` and `.lake` keyed on `lakefile.toml` (+ `lake-manifest.json` if committed).

### 6. Artifacts

Upload `build.log` on always(). Retention 7–14 days is enough.

### 7. Concurrency

```yaml
concurrency:
  group: aqarion-gap-${{ github.ref }}
  cancel-in-progress: true
```

## Minimal second workflow (stdlib only)

If you prefer a separate file under `.github/workflows/`:

```yaml
name: AQARION-GAP stdlib n6
on:
  push:
    paths: ['verification/AQARION-GAP/**']
  pull_request:
    paths: ['verification/AQARION-GAP/**']
  workflow_dispatch:
jobs:
  n6:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: verification/AQARION-GAP
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python3 verify-gap-n6.py
```

## Common failure modes

| Symptom | Likely cause |
|---------|----------------|
| `lakefile.toml` not found | Wrong working-directory |
| Mathlib fetch timeout | Network / first-run; increase `timeout-minutes` |
| Python assertion on B6 | Broken partition generator or Python < 3.9 |
| SEP-pure miscount | Block representation not canonical tuples |
| CI green but local red | Different Python or uncommitted script changes |

## What “good progress” means (aligned with your note)

- Algebraic identity is written and case-closed — **done**.
- Independent n=6 check is in-repo and runnable — **done**.
- Lean scaffold and a workflow file exist — **done**.
- Full `[FV]` and C4 — **not done**, and correctly blocked until sorries are gone.

That is genuine, reproducible progress.
