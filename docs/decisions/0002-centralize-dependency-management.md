---
status: "accepted"
date: 2026-03-26
decision-makers:
  - Bret Amogilefsky
---

# Centralize dependency management and CI/CD security scanning

## Context and Problem Statement

GSA-TTS maintains ~300 GitHub repositories. Each team independently configures dependency updates, and many repos still reference GitHub Actions by mutable tag (e.g., `@v4`) rather than immutable SHA, exposing the org to supply-chain attacks. NIST 800-53 requires controls across six families (CM, IA, RA, SA, SI, SR), including flaw remediation, unsupported-component replacement, and supply-chain integrity — but there is no centralized mechanism to implement or evidence these controls consistently.

How should we provide org-wide dependency management and CI/CD security scanning in a way that is auditable, easily incorporated as a common component, and adoptable by teams with minimal friction?

## Decision Drivers

- Teams lack a consistent, low-effort way to keep dependencies current and pin Actions to SHAs
- NIST 800-53 controls (14 across 6 families) benefit from a shared implementation that individual system SSPs can inherit
- GSA CIO 2100.1 defines vulnerability remediation timelines (14d critical / 30d high / 90d moderate) that require centralized tracking
- Dependabot cannot share org-wide configuration or enforce policy choices like minimum release age
- The org already uses AllStar for branch-protection enforcement; this capability should complement rather than overlap

## Considered Options

- Dependabot only (status quo)
- Self-hosted Renovate via GitHub Actions (central preset repo)
- Hosted Mend Renovate (SaaS)

## Decision Outcome

Chosen option: "Self-hosted Renovate via GitHub Actions", with zizmor for CI/CD SAST as a complement, because it gives us a single org-wide preset that teams inherit by adding one file, runs entirely on GitHub-hosted infrastructure with no SaaS dependency, and can be wrapped with an OSCAL component definition that systems import into their SSPs.

**Key sub-decisions:**

**Renovate over Dependabot.** Renovate supports a shared preset (`extends: ["local>GSA-TTS/scanning-service"]`) that Dependabot cannot match. One file in `default.json5` defines SHA-pinning policy, minimum release age, vulnerability alerts, and package replacement rules for the entire org.

**Separate from AllStar.** AllStar enforces branch-protection *settings* that support controls (e.g., requiring reviews), but it doesn't implement controls itself. This service implements the dependency-management and supply-chain-integrity controls directly — updating packages, pinning digests, flagging abandoned components, and tracking remediation SLAs — which are distinct responsibilities with different operational profiles.

**Annotated configuration.** The shared preset uses JSON5 format specifically so that each compliance-significant setting is annotated with the NIST 800-53 control parts it supports. This makes the link between technical configuration and control implementation auditable without a separate mapping document.

**Key policy choices:**
- `minimumReleaseAge: "2 days"` — lets the ecosystem surface regressions before we adopt
- Auto-merge excluded from central config — teams opt in per-repo based on their risk tolerance
- `vulnerabilityAlerts: true` — Renovate raises security PRs immediately, independent of the regular update schedule
- Remediation SLA: 14 days critical (CVSS 9.0+), 30 days high (7.0–8.9), 90 days moderate (4.0–6.9), aligning with GSA CIO 2100.1
- `replacements:all` and `abandonments:recommended` — automatically migrates to known replacements and flags end-of-life components (SA-22)

**zizmor for CI/CD SAST.** Renovate handles dependency freshness and SHA pinning; zizmor handles the workflow-specific attack surface — template injection, credential exposure, excessive permissions, mutable refs in third-party actions. These are complementary capabilities under different controls (SI-3 vs SI-2/CM-3).

**OSCAL component definition.** The repo ships a machine-readable component definition following the cg-egress-proxy pattern. Systems import it via `copy-component` and reference the narratives in their SSPs. 14 controls across 6 families, all marked `partial` — teams still document their own overrides and residual responsibilities.

**Phased rollout.** Initial deployment is scoped to 5 pilot repos via `autodiscoverFilter`. Org-wide expansion happens after validating the operational model.

### Consequences

- Good, because 14 NIST 800-53 controls become an shared component — individual system SSPs reference rather than re-implement
- Good, because teams onboard with a single `renovate.json` file
- Good, because SA-22 (unsupported components) gap is closed — Dependabot has no equivalent capability
- Good, because vulnerability SLA tracking is centralized rather than per-team
- Bad, because the GitHub App that runs Renovate holds `contents:write` and `workflows:write` across onboarded repos — a high-value credential that must be carefully protected
- Bad, because central configuration creates a single point of failure — a bad preset update could generate disruptive PRs across all onboarded repos

### Confirmation

- `docs/compliance/component-definitions/org-dependency-management/component-definition.json` exists and passes OSCAL schema validation
- `default.json5` contains annotated settings with control-part references
- Pilot repos receive Renovate PRs with SHA-pinned Actions
- `monitoring.yml` weekly report shows onboarding and pinning metrics
- `vulnerability-sla.yml` produces SLA compliance reports

## Pros and Cons of the Options

### Dependabot only (status quo)

GitHub's built-in dependency update service.

- Good, because zero setup — already available on every repo
- Good, because native GitHub UI integration
- Bad, because no shared configuration — each repo maintains its own `dependabot.yml`
- Bad, because no preset inheritance — policy changes require updating hundreds of files
- Bad, because no `replacements` or `abandonments` — cannot address SA-22
- Bad, because no `minimumReleaseAge` — adopts releases immediately
- Bad, because limited ecosystem support compared to Renovate

### Self-hosted Renovate via GitHub Actions

Renovate running on a cron schedule in a central repo, using a GitHub App for authentication.

- Good, because shared preset via `extends` — one config governs the org
- Good, because JSON5 supports inline comments for compliance annotations
- Good, because `pinDigests`, `replacements`, `abandonments`, `minimumReleaseAge` are all built-in
- Good, because runs on GitHub-hosted infrastructure — no external SaaS dependency
- Good, because `vulnerabilityAlerts` integrates with GitHub's advisory database
- Bad, because requires a GitHub App with broad write permissions
- Bad, because self-hosted means we own the runner maintenance and debugging

### Hosted Mend Renovate (SaaS)

Mend's managed Renovate service.

- Good, because no runner maintenance — Mend handles infrastructure
- Good, because same Renovate configuration language and presets
- Bad, because sends repository metadata to a third-party SaaS — requires ATO review for data handling
- Bad, because adds an external dependency to the CI/CD pipeline
- Bad, because less control over scheduling, rate limiting, and runner behavior

## More Information

- [Onboarding playbook](../onboarding-playbook.md) — step-by-step guide for repo owners
- [OSCAL component definition](../compliance/README.md) — how to import the common control into your SSP
- [Renovate documentation](https://docs.renovatebot.com/) — full configuration reference
- [zizmor](https://github.com/woodruffw/zizmor) — GitHub Actions SAST tool
- [GSA CIO 2100.1](https://www.gsa.gov/policy-regulations/policy/information-technology-policy/it-security-procedural-guides) — vulnerability remediation timelines
