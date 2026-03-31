---
x-trestle-comp-def-rules:
  org-dependency-management:
    - name: vulnerability-sla-tracked
      description: Centralized vulnerability SLA tracking is active for this 
        repo via the org GitHub App
x-trestle-param-values:
  si-02_odp:
x-trestle-global:
  profile:
    title: Electronic Version of NIST SP 800-53 Rev 5.1.1 Controls and SP 
      800-53A Rev 5.1.1 Assessment Procedures
    href: 
      https://raw.githubusercontent.com/usnistgov/oscal-content/refs/tags/v1.3.0/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json
  sort-id: si-02
---

# si-2 - \[System and Information Integrity\] Flaw Remediation

## Control Statement

- \[a.\] Identify, report, and correct system flaws;

- \[b.\] Test software and firmware updates related to flaw remediation for effectiveness and potential side effects before installation;

- \[c.\] Install security-relevant software and firmware updates within {{ insert: param, si-02_odp }} of the release of the updates; and

- \[d.\] Incorporate flaw remediation into the organizational configuration management process.

## Control Assessment Objective

- \[SI-02a.\]

  - \[SI-02a.[01]\] system flaws are identified;
  - \[SI-02a.[02]\] system flaws are reported;
  - \[SI-02a.[03]\] system flaws are corrected;

- \[SI-02b.\]

  - \[SI-02b.[01]\] software updates related to flaw remediation are tested for effectiveness before installation;
  - \[SI-02b.[02]\] software updates related to flaw remediation are tested for potential side effects before installation;
  - \[SI-02b.[03]\] firmware updates related to flaw remediation are tested for effectiveness before installation;
  - \[SI-02b.[04]\] firmware updates related to flaw remediation are tested for potential side effects before installation;

- \[SI-02c.\]

  - \[SI-02c.[01]\] security-relevant software updates are installed within {{ insert: param, si-02_odp }} of the release of the updates;
  - \[SI-02c.[02]\] security-relevant firmware updates are installed within {{ insert: param, si-02_odp }} of the release of the updates;

- \[SI-02d.\] flaw remediation is incorporated into the organizational configuration management process.

## Control guidance

The need to remediate system flaws applies to all types of software and firmware. Organizations identify systems affected by software flaws, including potential vulnerabilities resulting from those flaws, and report this information to designated organizational personnel with information security and privacy responsibilities. Security-relevant updates include patches, service packs, and malicious code signatures. Organizations also address flaws discovered during assessments, continuous monitoring, incident response activities, and system error handling. By incorporating flaw remediation into configuration management processes, required remediation actions can be tracked and verified.

Organization-defined time periods for updating security-relevant software and firmware may vary based on a variety of risk factors, including the security category of the system, the criticality of the update (i.e., severity of the vulnerability related to the discovered flaw), the organizational risk tolerance, the mission supported by the system, or the threat environment. Some types of flaw remediation may require more testing than other types. Organizations determine the type of testing needed for the specific type of flaw remediation activity under consideration and the types of changes that are to be configuration-managed. In some situations, organizations may determine that the testing of software or firmware updates is not necessary or practical, such as when implementing simple malicious code signature updates. In testing decisions, organizations consider whether security-relevant software or firmware updates are obtained from authorized sources with appropriate digital signatures.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

Dependency updates are incorporated into the organizational configuration management process — all changes go through Renovate PRs, CI validation, and team review before merging to the default branch. The PR-based workflow ensures flaw remediation follows the same CM controls as any other code change.

### Rules:

  - vulnerability-sla-tracked

### Implementation Status: implemented

______________________________________________________________________

## Implementation for part a.

Renovate automatically detects when pinned dependencies have newer versions available (including security patches) and creates PRs. The vulnerabilityAlerts setting creates immediate PRs when GitHub Security Advisory alerts fire, bypassing the normal schedule window. Onboarded repos automatically receive a per-repository tracking issue that reports all open Dependabot alerts by severity and SLA status, ensuring flaws are identified and reported directly in the repo's issue tracker.

### Rules:

  - vulnerability-sla-tracked

### Implementation Status: implemented

______________________________________________________________________

## Implementation for part b.

CI tests run against every dependency update PR before merge, validating that the flaw remediation does not break system functionality. Teams review test results before merging.

### Rules:

  - vulnerability-sla-tracked

### Implementation Status: implemented

______________________________________________________________________

## Implementation for part c.

The 2-day minimumReleaseAge ensures stability while the centralized vulnerability SLA tracker enforces GSA CIO 2100.1 remediation timelines (Critical/High 30d, Medium 90d, Low 180d, CISA KEV 14d). Repos that opt in receive a per-repository tracking issue that is updated weekly with current SLA status, reopened automatically if new alerts appear after all-clear, and closed when no open alerts remain.

### Rules:

  - vulnerability-sla-tracked

### Implementation Status: implemented

______________________________________________________________________

## Implementation for part d.

Dependency updates are incorporated into the organizational configuration management process — all changes go through Renovate PRs, CI validation, and team review before merging to the default branch.

### Rules:

  - vulnerability-sla-tracked

### Implementation Status: implemented

______________________________________________________________________
