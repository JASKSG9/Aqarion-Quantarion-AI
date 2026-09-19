# AQARION-Gap — independent stdlib gap-rule regression (no Lean required)
# Verifies the n=6 exhaustive pair check that supports the algebraic proof.
name: stdlib gap-rule check (n=6)

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]
  workflow_dispatch:

permissions:
  contents: read

jobs:
  n6-gap:
    name: pure-Python n=6 gap identity
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Run independent gap-rule check
        run: |
          python3 scripts/verify_gap_n6.py
          echo "EXIT=$?"
