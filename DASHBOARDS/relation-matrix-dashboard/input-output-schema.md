
***

# `relation-matrix-dashboard/INPUT_OUTPUT_SCHEMA.md`

```markdown
# Input and Output Schema

## Input matrix schema

The dashboard accepts a finite integer matrix.

```json
{
  "schema": "aqarion-relation-matrix-v1",
  "convention": "A: Z^n -> Z^m; output group is coker(A)=Z^m/im(A)",
  "matrix": [
[4][12]
  ]
}
