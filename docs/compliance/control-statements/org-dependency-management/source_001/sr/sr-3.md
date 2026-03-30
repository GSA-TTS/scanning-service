---
x-trestle-comp-def-rules:
  org-dependency-management:
    - name: depmgmt-implemented
      description: This control is fully implemented for the scope of the org dependency
        management component
---

# sr-3 - \[SR\] Supply Chain Controls and Processes

## Control Statement

Establish a process or processes to identify and address weaknesses or deficiencies in the supply chain elements and processes.

## What is the solution and how is it implemented?

### org-dependency-management

The org establishes a supply chain risk management process for CI/CD dependencies: centralized scanning (Renovate), version pinning (SHA), integrity verification (cryptographic hash), vulnerability monitoring (Dependabot alerts + SLA tracking), and automated remediation (Renovate PRs). This covers all dependency ecosystems, not just GitHub Actions.

The process includes automated detection of abandoned or deprecated packages (`abandonments:recommended`), migration to known successors (`replacements:all`), and centralized monitoring of remediation timelines to ensure supply chain risks are addressed within organizational SLAs.

#### Rules:

  - depmgmt-implemented

#### Implementation Status: implemented
