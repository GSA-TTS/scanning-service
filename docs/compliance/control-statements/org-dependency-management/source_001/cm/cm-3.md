---
x-trestle-comp-def-rules:
  org-dependency-management:
    - name: renovate-onboarded
      description: The system repo has merged the Renovate onboarding PR and extends
        the org preset
---

# cm-3 - \[CM\] Configuration Change Control

## Control Statement

Determine and document the types of changes to the system that are configuration-controlled; review proposed configuration-controlled changes; implement configuration-controlled changes with appropriate safeguards.

## What is the solution and how is it implemented?

### org-dependency-management

#### Part b

All dependency version changes go through PR review — Renovate creates a PR, CI checks run, and a team member reviews and merges. The org-level lint check and optional ruleset enforce this gate. No ad-hoc version changes are possible once enforcement is active.

#### Rules:

  - renovate-onboarded

#### Implementation Status: implemented

#### Part f

Renovate's weekday schedule, PR concurrency limits (5 concurrent, 1 per hour), and grouping rules provide controlled change windows. Changes are scheduled before 7am on weekdays, ensuring changes are introduced in a controlled, reviewable manner aligned with the organization's change management process.

#### Rules:

  - renovate-onboarded

#### Implementation Status: implemented
