AQARION PROVENANCE RULE

A computational result is REPRODUCED when:

1. The executable is present in the repository.
2. The executable is invoked by the registered manifest.
3. The manifest is committed.
4. CI executes the manifest at a known commit.
5. The receipt records that commit and tree.
6. The receipt records the manifest SHA-256.
7. Every registered check returns PASS.
8. The promotion gate verifies that the receipt binds to
   the current committed tree.

A computational result is LOCAL-VERIFIED when its executable
has been run successfully outside the certified repository
pipeline.

A computational result is CLAIMED when reported without the
above executable evidence.

LOCAL-VERIFIED MUST NOT be represented as REPRODUCED.
CLAIMED MUST NOT be represented as VERIFIED.
