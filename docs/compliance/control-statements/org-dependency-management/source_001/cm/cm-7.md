---
x-trestle-comp-def-rules:
  org-dependency-management:
    - name: sha-pins-verified
      description: All GitHub Actions uses: refs in the repo are SHA-pinned
    - name: actions-sast-scanned
      description: GitHub Actions workflows are scanned for security issues via centralized
        zizmor SAST analysis
---

# cm-7 - \[CM\] Least Functionality

## Control Statement

Configure the system to provide only mission-essential capabilities; prohibit or restrict the use of functions, ports, protocols, software, and/or services as defined by the organization.

## What is the solution and how is it implemented?

### org-dependency-management

#### Part a

SHA pinning ensures repos use only the exact, reviewed version of each Action — not whatever a mutable tag (e.g., `@v4` or `@main`) resolves to at any given moment. This reduces attack surface from mutable references and enforces least functionality for CI/CD pipeline dependencies.

The `pinDigests` setting converts all tag-based references to immutable SHA-256 commit hashes, ensuring only the specific reviewed code version executes in CI pipelines.

Centralized SAST analysis detects excessive permission scopes granted to workflow runners, flagging cases where `permissions:` declarations exceed what the workflow actually needs. This enforces least functionality for CI/CD workflow configurations beyond just dependency versions.

#### Rules:

  - sha-pins-verified
  - actions-sast-scanned

#### Implementation Status: implemented
