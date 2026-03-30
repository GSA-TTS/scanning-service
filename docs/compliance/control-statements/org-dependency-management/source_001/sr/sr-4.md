---
x-trestle-comp-def-rules:
  org-dependency-management:
    - name: sha-pins-verified
      description: All GitHub Actions uses: refs in the repo are SHA-pinned
---

# sr-4 - \[SR\] Provenance

## Control Statement

Document, monitor, and maintain valid provenance of systems, system components, and associated data.

## What is the solution and how is it implemented?

### org-dependency-management

SHA pins create a verifiable chain from the exact upstream commit to the workflow that runs in the org's CI. Version comments (e.g., `# v4.2.2`) provide human-readable provenance alongside the machine-verifiable hash.

The `pinDigestsHelper` setting adds these version comments automatically, ensuring every SHA-pinned reference includes both the cryptographic identifier and the human-readable version for provenance documentation. This enables auditors to trace exactly which version of each dependency was used in any given CI run.

#### Rules:

  - sha-pins-verified

#### Implementation Status: implemented
