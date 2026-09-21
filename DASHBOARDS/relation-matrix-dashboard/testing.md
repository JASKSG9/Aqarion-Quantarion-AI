
***

# `relation-matrix-dashboard/TESTING.md`

```markdown
# Testing Guide

## Purpose

This document defines the minimum manual and automated checks for the AQARION
Relation Matrix Dashboard.

The dashboard is a static browser application. Its mathematical core is the
interpretation:

[
A:mathbb Z^n\tomathbb Z^m,
qquad
operatorname{coker}(A)=mathbb Z^m/operatorname{im}(A).
]

## Required static checks

From the repository root:

```bash
test -f relation-matrix-dashboard/index.html
test -f relation-matrix-dashboard/styles.css
test -f relation-matrix-dashboard/app.js
test -f relation-matrix-dashboard/README.md
test -f relation-matrix-dashboard/MATHEMATICAL_SPECIFICATION.md
test -f relation-matrix-dashboard/INPUT_OUTPUT_SCHEMA.md
test -f relation-matrix-dashboard/TESTING.md
node --check relation-matrix-dashboard/app.js
