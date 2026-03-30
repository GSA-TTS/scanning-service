---
x-trestle-comp-def-rules:
  org-dependency-management:
    - name: depmgmt-implemented
      description: This control is fully implemented for the scope of the org dependency
        management component
---

# ia-9 - \[IA\] Service Identification and Authentication

## Control Statement

Uniquely identify and authenticate organizational services and service providers.

## What is the solution and how is it implemented?

### org-dependency-management

The GitHub App used by Renovate has scoped permissions (`contents: write`, `pull-requests: write`, `workflows: write`, `metadata: read`, `vulnerability_alerts: read`, `issues: write`) and provides an auditable identity for all automated PRs. This is distinct from human identities, enabling clear attribution of automated vs. manual dependency changes in the audit trail.

The App's identity appears on every PR it creates, making it straightforward to distinguish automated dependency management actions from human-initiated changes in audit logs and PR history.

#### Rules:

  - depmgmt-implemented

#### Implementation Status: implemented
