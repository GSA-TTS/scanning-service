---
x-trestle-comp-def-rules:
  org-dependency-management:
    - name: renovate-onboarded
      description: The system repo has merged the Renovate onboarding PR and 
        extends the org preset
x-trestle-param-values:
  cm-03_odp.01:
  cm-03_odp.02:
  cm-03_odp.03:
  cm-03_odp.04:
  cm-03_odp.05:
x-trestle-global:
  profile:
    title: Electronic Version of NIST SP 800-53 Rev 5.1.1 Controls and SP 
      800-53A Rev 5.1.1 Assessment Procedures
    href: 
      https://raw.githubusercontent.com/usnistgov/oscal-content/refs/tags/v1.3.0/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json
  sort-id: cm-03
---

# cm-3 - \[Configuration Management\] Configuration Change Control

## Control Statement

- \[a.\] Determine and document the types of changes to the system that are configuration-controlled;

- \[b.\] Review proposed configuration-controlled changes to the system and approve or disapprove such changes with explicit consideration for security and privacy impact analyses;

- \[c.\] Document configuration change decisions associated with the system;

- \[d.\] Implement approved configuration-controlled changes to the system;

- \[e.\] Retain records of configuration-controlled changes to the system for {{ insert: param, cm-03_odp.01 }};

- \[f.\] Monitor and review activities associated with configuration-controlled changes to the system; and

- \[g.\] Coordinate and provide oversight for configuration change control activities through {{ insert: param, cm-03_odp.02 }} that convenes {{ insert: param, cm-03_odp.03 }}.

## Control Assessment Objective

- \[CM-03a.\] the types of changes to the system that are configuration-controlled are determined and documented;

- \[CM-03b.\]

  - \[CM-03b.[01]\] proposed configuration-controlled changes to the system are reviewed;
  - \[CM-03b.[02]\] proposed configuration-controlled changes to the system are approved or disapproved with explicit consideration for security and privacy impact analyses;

- \[CM-03c.\] configuration change decisions associated with the system are documented;

- \[CM-03d.\] approved configuration-controlled changes to the system are implemented;

- \[CM-03e.\] records of configuration-controlled changes to the system are retained for {{ insert: param, cm-03_odp.01 }};

- \[CM-03f.\]

  - \[CM-03f.[01]\] activities associated with configuration-controlled changes to the system are monitored;
  - \[CM-03f.[02]\] activities associated with configuration-controlled changes to the system are reviewed;

- \[CM-03g.\]

  - \[CM-03g.[01]\] configuration change control activities are coordinated and overseen by {{ insert: param, cm-03_odp.02 }};
  - \[CM-03g.[02]\] the configuration control element convenes {{ insert: param, cm-03_odp.03 }}.

## Control guidance

Configuration change control for organizational systems involves the systematic proposal, justification, implementation, testing, review, and disposition of system changes, including system upgrades and modifications. Configuration change control includes changes to baseline configurations, configuration items of systems, operational procedures, configuration settings for system components, remediate vulnerabilities, and unscheduled or unauthorized changes. Processes for managing configuration changes to systems include Configuration Control Boards or Change Advisory Boards that review and approve proposed changes. For changes that impact privacy risk, the senior agency official for privacy updates privacy impact assessments and system of records notices. For new systems or major upgrades, organizations consider including representatives from the development organizations on the Configuration Control Boards or Change Advisory Boards. Auditing of changes includes activities before and after changes are made to systems and the auditing activities required to implement such changes. See also [SA-10](#sa-10).

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

Renovate's weekday schedule, PR concurrency limits (5 concurrent, 1 per hour), and grouping rules provide controlled change windows. Changes are scheduled before 7am on weekdays, ensuring changes are introduced in a controlled, reviewable manner aligned with the organization's change management process.

### Rules:

  - renovate-onboarded

### Implementation Status: implemented

______________________________________________________________________

## Implementation for part b.

All dependency version changes go through PR review — Renovate creates a PR, CI checks run, and a team member reviews and merges. The org-level lint check and optional ruleset enforce this gate. No ad-hoc version changes are possible once enforcement is active.

### Rules:

  - renovate-onboarded

### Implementation Status: implemented

______________________________________________________________________

## Implementation for part f.

Renovate's weekly schedule, PR concurrency limits, and grouping rules provide controlled change windows. Changes are scheduled before 7am on weekdays, limited to 5 concurrent PRs and 1 per hour, ensuring changes are introduced in a controlled, reviewable manner.

### Rules:

  - renovate-onboarded

### Implementation Status: implemented

______________________________________________________________________
