---
x-trestle-comp-def-rules:
  org-dependency-management:
    - name: renovate-onboarded
      description: The system repo has merged the Renovate onboarding PR and extends
        the org preset
---

# cm-6 - \[CM\] Configuration Settings

## Control Statement

Establish and document configuration settings for components employed within the system that reflect the most restrictive mode consistent with operational requirements.

## What is the solution and how is it implemented?

### org-dependency-management

#### Part a

The centralized Renovate preset defines mandatory configuration settings for all repos, with inline compliance annotations (JSON5 comments) documenting which NIST 800-53 control parts each setting supports. Deviations require explicit overrides documented in the repo's `renovate.json`.

The JSON5 format enables comments that make each setting's compliance significance visible to future editors, reducing the risk of someone removing `pinDigests` or `vulnerabilityAlerts` without understanding the compliance impact.

#### Rules:

  - renovate-onboarded

#### Implementation Status: implemented
