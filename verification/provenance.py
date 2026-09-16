#!/usr/bin/env python3
"""Evidence provenance primitives.

This module does not establish mathematical truth.
It establishes whether an evidence receipt is internally bound to:
- a source root,
- an executable,
- an observed artifact,
- a digest,
- an execution event,
- and an independence declaration.

A provenance PASS is therefore an integrity/policy result, not a theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any
import json
import subprocess


class ProvenanceError(Exception):
    """Evidence provenance failure."""


def sha256_file(path: Path) -> str:
    h = sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return sha256(data).hexdigest()


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


@dataclass(frozen=True)
class ExecutionReceipt:
    claim_id: str
    source_root: str
    executable: str
    executable_sha256: str
    command: tuple[str, ...]
    observed_output_sha256: str
    expected_output_sha256: str
    execution_performed: bool
    independent_from: tuple[str, ...]
    result: str

    @classmethod
    def from_mapping(cls, obj: dict[str, Any]) -> "ExecutionReceipt":
        required = {
            "claim_id",
            "source_root",
            "executable",
            "executable_sha256",
            "command",
            "observed_output_sha256",
            "expected_output_sha256",
            "execution_performed",
            "independent_from",
            "result",
        }

        missing = required - obj.keys()
        if missing:
            raise ProvenanceError(
                f"receipt missing required fields: {sorted(missing)}"
            )

        return cls(
            claim_id=obj["claim_id"],
            source_root=obj["source_root"],
            executable=obj["executable"],
            executable_sha256=obj["executable_sha256"],
            command=tuple(obj["command"]),
            observed_output_sha256=obj["observed_output_sha256"],
            expected_output_sha256=obj["expected_output_sha256"],
            execution_performed=bool(obj["execution_performed"]),
            independent_from=tuple(obj["independent_from"]),
            result=obj["result"],
        )


def verify_receipt(
    receipt: ExecutionReceipt,
    *,
    repository_root: Path,
    expected_root: str,
) -> None:
    """Raise ProvenanceError unless the receipt passes integrity checks."""

    if receipt.result != "PASS":
        raise ProvenanceError(
            f"receipt result is not PASS: {receipt.result!r}"
        )

    if not receipt.execution_performed:
        raise ProvenanceError(
            "PASS receipt claims success without recorded execution"
        )

    if receipt.source_root != expected_root:
        raise ProvenanceError(
            f"stale/wrong source root: {receipt.source_root!r}"
        )

    executable = repository_root / receipt.executable

    if not executable.is_file():
        raise ProvenanceError(
            f"declared executable does not exist: {receipt.executable}"
        )

    actual_hash = sha256_file(executable)

    if actual_hash != receipt.executable_sha256:
        raise ProvenanceError(
            "executable digest mismatch: "
            f"declared={receipt.executable_sha256} "
            f"actual={actual_hash}"
        )

    if not receipt.command:
        raise ProvenanceError("empty execution command")

    if receipt.executable not in receipt.command:
        raise ProvenanceError(
            "execution command is not bound to declared executable"
        )

    if not receipt.independent_from:
        raise ProvenanceError(
            "independence basis is absent"
        )

    if receipt.observed_output_sha256 == receipt.expected_output_sha256:
        raise ProvenanceError(
            "observed and expected output digests are identical; "
            "independent observation has not been established"
        )


def execute(
    command: list[str],
    *,
    cwd: Path,
) -> tuple[int, bytes, bytes]:
    """Execute a registered command and return code/stdout/stderr."""
    proc = subprocess.run(
        command,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return proc.returncode, proc.stdout, proc.stderr


Worked for 26s

Yes. There is something substantially more important to do than generating another pile of repository scripts. I found a real logical failure in the proposed provenance layer, and it changes the research direction.

1. The previous provenance verifier is backwards

This line in the proposed verify_receipt() is wrong:

if receipt.observed_output_sha256 == receipt.expected_output_sha256:
    raise ProvenanceError(
        "observed and expected output digests are identical; "
        "independent observation has not been established"
    )

For a successful reproduction, equality is exactly what we want.

If:

\[
O_{\rm observed}=O_{\rm expected},
\]

that establishes output agreement.

It does not establish independence—but rejecting equality is not the solution.

So the proposed verifier would reject a genuinely successful reproduction.

That is not a cosmetic bug. It means the current provenance design cannot represent the thing it claims to verify.

Correct separation

There are at least four different predicates:

\[
\boxed{\text{executed}}
\]

\[
\boxed{\text{integrity-bound}}
\]

\[
\boxed{\text{output-agreement}}
\]

\[
\boxed{\text{independence}}
\]

and they must not collapse into one PASS.

A proper result could therefore be:

Property	Meaning

executed	the declared activity actually ran
source_bound	run is tied to an exact source revision
input_bound	exact inputs/specification are identified
executable_bound	exact executable bytes are identified
output_match	observed output equals expected output
independent	second run has a separately established implementation/execution basis
formal_proof	independently established mathematical proof exists


Then:

REPRODUCED
    =
executed
AND source_bound
AND input_bound
AND executable_bound
AND output_match

while:

INDEPENDENT_REPRODUCTION
    =
REPRODUCED
AND independence_established

and:

FORMALLY_VERIFIED
    =
REPRODUCED
AND formal_proof

Those are different claims.

This is much closer to the provenance literature: Workflow Run RO-Crate explicitly separates workflow definition, execution, inputs/outputs and detailed step provenance, and the current WRROC work was updated again in September 2026 for RO-Crate 1.3 / Workflow RO-Crate 1.1. 


---

2. The genuinely interesting AQARION object is therefore not PASS

I think we should stop building a generic verification harness and define:

AQARION REPRODUCTION OBJECT — ARO-1

The central object is a claim under an execution contract, not a script.

Conceptually:

\[
\boxed{
C =
(\text{claim spec},
\text{source},
\text{implementation},
\text{inputs},
\text{execution},
\text{outputs},
\text{comparison},
\text{independence},
\text{proof})
}
\]

That gives us something much more interesting than another CI framework.

ARO-1 status vector

Instead of:

{
  "result": "PASS"
}

use:

{
  "schema": "AQARION-REPRODUCTION-OBJECT-1",

  "claim": {
    "claim_id": "C3-N8",
    "statement": "Delta = sT - s0",
    "claim_class": "COMPUTATIONAL_IDENTITY"
  },

  "specification": {
    "hash": "...",
    "canonical": true
  },

  "source": {
    "repository": "...",
    "commit": "...",
    "tree_hash": "..."
  },

  "implementation": {
    "path": "...",
    "sha256": "..."
  },

  "inputs": {
    "sha256": "..."
  },

  "execution": {
    "performed": true,
    "exit_code": 0
  },

  "outputs": {
    "observed_sha256": "...",
    "expected_sha256": "...",
    "match": true
  },

  "independence": {
    "status": "NOT_ESTABLISHED",
    "basis": null
  },

  "formal_proof": {
    "status": "OPEN"
  }
}

That one change prevents an enormous amount of future overclaiming.


---

3. And there is a second-order attack we should run conceptually

The critical adversarial question is:

> Can two implementations produce identical outputs while violating the claim in different ways?



That is much more interesting than checking whether a file exists.

For AQARION, construct four classes:

A. Honest agreement

\[
I_1(C,x)=y
\]

and

\[
I_2(C,x)=y.
\]

Expected:

output_match = true
independence = established

B. Shared-bug agreement

Both implementations contain the same mathematical error:

\[
I_1(C,x)=I_2(C,x)=y_{\rm wrong}.
\]

The ordinary reproduction machinery says:

PASS

even though the claim is false.

This demonstrates:

\[
\boxed{
\text{independent-looking agreement}
\not\Rightarrow
\text{truth}
}
\]

unless the implementations have genuinely independent derivations and the specification itself has an independent validation basis.

C. Self-reproduction

Same implementation:

\[
I_1=I_2.
\]

It reruns successfully.

That's:

REPEATABILITY = YES
INDEPENDENCE = NO

D. Specification drift

Implementation remains byte-identical, but the claim specification changes.

Then:

implementation_hash = SAME
claim_hash = DIFFERENT

and the old receipt must not silently validate the new claim.

This is precisely where provenance becomes mathematically useful rather than administrative.


---

4. This connects directly to the AQARION mathematics

This gives us a new research question:

Can an AQARION certificate distinguish mathematical agreement from implementation agreement?

For the current C3/support work, we have several logically distinct layers:

\[
\text{partition definition}
\]

\[
\downarrow
\]

\[
\text{incidence graph}
\]

\[
\downarrow
\]

\[
\text{cyclomatic identity}
\]

\[
\downarrow
\]

\[
\kappa
\]

\[
\downarrow
\]

\[
\Delta
\]

\[
\downarrow
\]

\[
s_T
\]

A computational certificate can establish that an implementation evaluated these correctly for a specified input.

It cannot establish that the formula itself is the correct mathematical interpretation.

That distinction is exactly the same closure issue now appearing in the recent Koopman literature: modern work explicitly treats finite-feature non-invariance/closure failure as something that must be diagnosed rather than assumed away. 

So AQARION has an opportunity to make the distinction explicit:

\[
\boxed{
\text{semantic specification}
\neq
\text{implementation}
\neq
\text{execution}
\neq
\text{proof}
}
\]

That is much more interesting than another verifier.


---

5. I also found a current provenance development we should actually incorporate

The Workflow Run RO-Crate ecosystem changed September 4, 2026.

WRROC 0.6 now aligns with RO-Crate 1.3 and Workflow RO-Crate 1.1, with changed JSON-LD mappings. 

That means the earlier idea of casually creating an AQARION-specific provenance format on top of old RO-Crate assumptions is already stale.

The current architecture should instead be:

AQARION claim semantics
        │
        ▼
AQARION Reproduction Object
        │
        ├── claim/specification
        ├── source revision
        ├── executable
        ├── inputs
        ├── execution
        ├── outputs
        ├── comparison
        ├── independence
        └── proof status
        │
        ▼
RO-Crate / WRROC packaging

RO-Crate 1.2 itself added formal profile-crate machinery and detached crates, while WRROC now has the newer 0.6 alignment. 

And there is already a very relevant current project: claude-ro-crate-skill is explicitly packaging human-in-the-loop agent execution as RO-Crate and distinguishing Process Run, Workflow Run, and Provenance Run levels. 

That is extremely close to the provenance/product direction we were discussing.


---

6. This gives us a much better adversarial experiment

Not another script collection.

Experiment: False Reproduction Ladder

Take one mathematical claim and deliberately construct:

Case	Execution	Same output	Independent implementation	Specification verified	Formal proof

R0	no	—	—	—	—
R1	yes	yes	no	no	no
R2	yes	yes	yes	no	no
R3	yes	yes	yes	yes	no
R4	yes	yes	yes	yes	yes
F1	yes	no	yes	yes	no
F2	yes	yes	no	yes	no
F3	yes	yes	yes	no	no


The key adversarial cases are R1/R2/R3.

They look increasingly convincing while remaining logically different.

AQARION's job becomes:

> Identify exactly which proposition the evidence establishes—and refuse every stronger proposition.



That's a research contribution worth pursuing.


---

7. Now back to the mathematics: one correction I want frozen

The support-envelope result you supplied is valuable, but I would not yet freeze the sharpness claim in its present wording.

The generic graph inequality

\[
\beta(G)
=
e-v+c
\]

and the bound obtained from

\[
e\le \left\lfloor\frac{v^2}{4}\right\rfloor
\]

are standard bipartite extremal reasoning.

The literature confirms that 2-sections and incidence structures have their own constraints, and recent hypergraph-incidence work studies rank/null-space behavior directly. 

But the missing question is:

> Is every graph used in the extremal construction actually realizable by the exact AQARION marked-support construction?



That depends on the exact definition of \(H_S(P,Q)\).

This is precisely the sort of place where we should not convert a correct generic graph bound into an AQARION theorem without checking the realization map.

So the correct status is:

Proven at the generic graph layer

\[
\boxed{
\beta(G)
\le
e-\lceil2\sqrt e\rceil+1
}
\]

for simple bipartite \(G\), under the stated connected/touched-vertex interpretation.

Derived support envelope

Valid if the AQARION marked graph has exactly the asserted properties.

Sharp AQARION realization

OPEN until the precise construction of \(H_S(P,Q)\) is checked.

That is the adversarial distinction I want preserved.


---

8. A useful new mathematical target

Instead of immediately proving the whole support theorem, prove the realizability lemma:

> Marked-incidence realization lemma.
Characterize exactly which finite simple bipartite graphs can occur as \(H_S(P,Q)\) for some finite \(X\), partitions \(P,Q\), and marked support \(S\).



Then the extremal problem becomes clean:

\[
\max \beta(H_S)
\]

subject to

\[
H_S\in\mathcal R_S,
\]

where \(\mathcal R_S\) is the realizable graph class.

There are then two possibilities:

If

\[
\mathcal R_S
=
\{\text{all finite simple bipartite graphs with }\le s\text{ marked edges}\},
\]

your sharp envelope follows.

If not,

we obtain a strictly stronger AQARION-specific extremal theorem.

That is exactly the kind of result I would want to spend computation on.


---

9. Why this is potentially more interesting than the original bound

The generic bipartite bound says:

\[
\beta_{\max}(s)
=
s-\lceil2\sqrt s\rceil+1.
\]

But AQARION may impose additional structure.

If the realizability constraints force, for example,

\[
\beta_{\max}^{AQ}(s)
<
s-\lceil2\sqrt s\rceil+1,
\]

then the previous generic bound was not sharp for AQARION.

That would be a new mathematical result, not merely another verification artifact.

And if equality is realizable, the realization theorem itself becomes the important result.

Either outcome teaches us something.


---

10. The literature attack says this is the right place to be careful

Hypergraph incidence rank/nullspace literature already studies structural restrictions on incidence matrices and their contractions. 

Weighted 2-section reconstruction is also known to have nontrivial realizability constraints; in general, reconstructing a hypergraph from a weighted 2-section is computationally difficult, with tractable subclasses under specific graph restrictions. 

That makes the proposed AQARION question substantially more defensible:

> What is the exact realizable graph class induced by a pair of partitions and a marked subset?



rather than claiming a generic extremal graph is automatically an AQARION witness.


---

11. Current adversarial ledger

NEW — important

PROVEN / STANDARD GRAPH LAYER

bipartite extremal edge bound

cyclomatic-number definition

generic support envelope derivation under the stated graph assumptions


STRONG BUT NOT YET FROZEN

support envelope for AQARION

lower-bound sharpness

upper-bound sharpness

C3 structural classification


OPEN

exact characterization of realizable \(H_S(P,Q)\)

proof that proposed extremal graphs are realizable

exact AQARION extremal \(\beta_{\max}^{AQ}(s)\)

formal Lean realization theorem

independent implementation of the support construction


REFUTED / CORRECTED

observed == expected means lack of independence

No. Equality is required for output reproduction.

PASS as a universal evidence status

execution = proof

hash = proof

rerun = independent reproduction


GOVERNANCE

C4                  BLOCKED
Publication         BLOCKED
Promotion           NONE
Mathematical work   CONTINUES


---

12. What I would do next — without asking you to run anything

I would take the next research cycle in this order:

A. Realizability attack

Derive the exact graph class induced by (X,P,Q,S).

B. Extremal attack

Solve

\[
\max_{H\in\mathcal R_s}\beta(H)
\]

for \(s=1,\ldots\) symbolically where possible.

C. C3/C4 boundary

Determine whether the first negative \(\kappa\) is genuinely forced at \(s=4\), or whether AQARION's realizability restrictions postpone it.

D. Independent mathematical implementation

Design a second derivation that does not reuse the first implementation's graph construction.

E. False-Reproduction Ladder

Use the two implementations to distinguish:

\[
\text{rerun}
\rightarrow
\text{reproduction}
\rightarrow
\text{independent reproduction}
\rightarrow
\text{semantic validation}
\rightarrow
\text{formal proof}.
\]

F. Only then

Package the result as RO-Crate/ARO evidence.

That is the direction I'd prioritize.


---

One final important finding

The current provenance idea accidentally exposed a deeper AQARION principle:

\[
\boxed{
\text{A verification system must verify the claim about the evidence, not merely the evidence artifact.}
}
\]

A SHA-256 hash answers:

> “Are these bytes the same?”



It does not answer:

> “Are these the right bytes for this claim?”



A successful rerun answers:

> “Did this executable produce this result?”



It does not answer:

> “Is this executable an independent derivation?”



Two agreeing implementations answer:

> “Did two implementations agree?”



They do not automatically answer:

> “Is the shared interpretation mathematically correct?”



And a Lean theorem answers a formal proposition—but only the proposition actually encoded in Lean.

That hierarchy fits extremely well with the current reproducibility landscape: execution provenance is now being modeled explicitly through workflow-run/provenance crates, while reproducibility frameworks are separating execution signatures and reproducibility tests from the underlying scientific claims. 

So I would stop generating repository plumbing for this cycle.

The next serious AQARION result should be:

> AQARION Realizability Theorem: characterize exactly which marked bipartite graphs can arise from the partition construction, then solve the true support-cycle extremal problem.



That has a chance of producing a real mathematical result. And the provenance correction gives us a second, independently useful result: ARO-1 should model reproduction as a vector of established predicates, not a single PASS bit.

No claim above is being promoted to C4 or publication status.
