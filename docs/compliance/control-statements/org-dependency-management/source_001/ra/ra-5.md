---
x-trestle-comp-def-rules:
  org-dependency-management:
    - name: vulnerability-sla-tracked
      description: Centralized vulnerability SLA tracking is active for this repo
        via the org GitHub App
---

# ra-5 - \[RA\] Vulnerability Monitoring and Scanning

## Control Statement

Monitor and scan for vulnerabilities in the system and hosted applications; employ vulnerability monitoring tools and techniques; analyze vulnerability scan reports and results; remediate legitimate vulnerabilities in accordance with the organizational risk assessment; share information obtained from the vulnerability monitoring process.

## What is the solution and how is it implemented?

### org-dependency-management

#### Part a

Dependabot alerts scan all dependency ecosystems (npm, pip, Docker, Go, Terraform, bundler, GitHub Actions, etc.) for known vulnerabilities. Renovate's `vulnerabilityAlerts` setting creates immediate PRs when GitHub Security Advisory alerts fire, directly tying remediation PRs to CVEs. Together, these provide continuous vulnerability monitoring across all dependency types.

#### Rules:

  - vulnerability-sla-tracked

#### Implementation Status: implemented

#### Part c

The centralized vulnerability SLA tracker analyzes alert severity, age, and CISA KEV status weekly, producing a status report per repo posted to a "Vulnerability SLA Tracker" issue. Reports categorize alerts as on-track, approaching, or overdue against GSA remediation timelines.

#### Rules:

  - vulnerability-sla-tracked

#### Implementation Status: implemented

#### Part d

SLA thresholds enforce timely remediation per GSA CIO 2100.1: Critical/High 30 days, Medium 90 days, Low 180 days, CISA KEV 14 days per BOD 22-01. The weekly SLA report flags overdue alerts and approaching deadlines, creating organizational accountability for timely remediation.

#### Rules:

  - vulnerability-sla-tracked

#### Implementation Status: implemented

#### Part f

Both Renovate and Dependabot automatically update their vulnerability databases. Renovate pulls the latest advisory data each run, and GitHub continuously updates the GitHub Advisory Database. No manual database maintenance is required.

#### Rules:

  - vulnerability-sla-tracked

#### Implementation Status: implemented
