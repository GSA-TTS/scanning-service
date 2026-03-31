---
x-trestle-comp-def-rules:
  org-dependency-management:
    - name: renovate-onboarded
      description: The system repo has merged the Renovate onboarding PR and 
        extends the org preset
x-trestle-param-values:
  cm-02_odp.01:
  cm-02_odp.02:
x-trestle-global:
  profile:
    title: Electronic Version of NIST SP 800-53 Rev 5.1.1 Controls and SP 
      800-53A Rev 5.1.1 Assessment Procedures
    href: 
      https://raw.githubusercontent.com/usnistgov/oscal-content/refs/tags/v1.3.0/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json
  sort-id: cm-02
---

# cm-2 - \[Configuration Management\] Baseline Configuration

## Control Statement

- \[a.\] Develop, document, and maintain under configuration control, a current baseline configuration of the system; and

- \[b.\] Review and update the baseline configuration of the system:

  - \[1.\] {{ insert: param, cm-02_odp.01 }};
  - \[2.\] When required due to {{ insert: param, cm-02_odp.02 }} ; and
  - \[3.\] When system components are installed or upgraded.

## Control Assessment Objective

- \[CM-02a.\]

  - \[CM-02a.[01]\] a current baseline configuration of the system is developed and documented;
  - \[CM-02a.[02]\] a current baseline configuration of the system is maintained under configuration control;

- \[CM-02b.\]

  - \[CM-02b.01\] the baseline configuration of the system is reviewed and updated {{ insert: param, cm-02_odp.01 }};
  - \[CM-02b.02\] the baseline configuration of the system is reviewed and updated when required due to {{ insert: param, cm-02_odp.02 }};
  - \[CM-02b.03\] the baseline configuration of the system is reviewed and updated when system components are installed or upgraded.

## Control guidance

Baseline configurations for systems and system components include connectivity, operational, and communications aspects of systems. Baseline configurations are documented, formally reviewed, and agreed-upon specifications for systems or configuration items within those systems. Baseline configurations serve as a basis for future builds, releases, or changes to systems and include security and privacy control implementations, operational procedures, information about system components, network topology, and logical placement of components in the system architecture. Maintaining baseline configurations requires creating new baselines as organizational systems change over time. Baseline configurations of systems reflect the current enterprise architecture.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

SHA-pinned workflow files and lockfiles establish a documented, reviewable baseline for CI/CD pipeline dependencies. Renovate PRs create an auditable change trail for each baseline update. A centralized preset ensures all repos maintain a consistent baseline configuration for dependency management.

When a repo onboards by merging the onboarding PR, it adopts the org's baseline dependency configuration. All subsequent dependency changes are tracked via Renovate PRs, providing a complete audit trail of baseline modifications.

### Rules:

  - renovate-onboarded

### Implementation Status: implemented

______________________________________________________________________
