---
x-trestle-comp-def-rules:
  org-dependency-management:
    - name: renovate-onboarded
      description: The system repo has merged the Renovate onboarding PR and extends
        the org preset
---

# cm-2 - \[CM\] Baseline Configuration

## Control Statement

Develop, document, and maintain under configuration control, a current baseline configuration of the information system.

## What is the solution and how is it implemented?

### org-dependency-management

SHA-pinned workflow files and lockfiles establish a documented, reviewable baseline for CI/CD pipeline dependencies. Renovate PRs create an auditable change trail for each baseline update. A centralized preset ensures all repos maintain a consistent baseline configuration for dependency management.

When a repo onboards by merging the onboarding PR, it inherits the org's baseline dependency configuration. All subsequent dependency changes are tracked via Renovate PRs, providing a complete audit trail of baseline modifications.

#### Rules:

  - renovate-onboarded

#### Implementation Status: implemented
