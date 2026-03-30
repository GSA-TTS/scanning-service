---
x-trestle-comp-def-rules:
  org-dependency-management:
    - name: vulnerability-sla-tracked
      description: Centralized vulnerability SLA tracking is active for this repo
        via the org GitHub App
---

# si-2 - \[SI\] Flaw Remediation

## Control Statement

Identify, report, and correct system flaws; test software and firmware updates related to flaw remediation for effectiveness and potential side effects before installation; install security-relevant software and firmware updates within the time period directed by the organization; and incorporate flaw remediation into the organizational configuration management process.

## What is the solution and how is it implemented?

### org-dependency-management

#### Part a

Renovate automatically detects when pinned dependencies have newer versions available (including security patches) and creates PRs. The `vulnerabilityAlerts` setting creates immediate PRs when GitHub Security Advisory alerts fire, bypassing the normal schedule window to ensure rapid response to known vulnerabilities.

#### Rules:

  - vulnerability-sla-tracked

#### Implementation Status: implemented

#### Part b

CI tests run against every dependency update PR before merge, validating that the flaw remediation does not break system functionality. Teams review test results before merging, ensuring updates are tested for effectiveness and potential side effects.

#### Rules:

  - vulnerability-sla-tracked

#### Implementation Status: implemented

#### Part c

The 2-day `minimumReleaseAge` ensures stability while the centralized vulnerability SLA tracker enforces GSA CIO 2100.1 remediation timelines (Critical/High 30 days, Medium 90 days, Low 180 days, CISA KEV 14 days per BOD 22-01). Weekly SLA reports flag overdue alerts and approaching deadlines.

#### Rules:

  - vulnerability-sla-tracked

#### Implementation Status: implemented

#### Part d

Dependency updates are incorporated into the organizational configuration management process — all changes go through Renovate PRs, CI validation, and team review before merging to the default branch. The PR-based workflow ensures flaw remediation follows the same CM controls as any other code change.

#### Rules:

  - vulnerability-sla-tracked

#### Implementation Status: implemented
