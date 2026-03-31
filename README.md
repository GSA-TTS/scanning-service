# Centralized Dependency Management & CI/CD Security Scanning

This repo provides centralized dependency management (using [Renovate](https://docs.renovatebot.com/)) and GitHub Actions security analysis (using [zizmor](https://github.com/woodruffw/zizmor)) for the GSA-TTS GitHub org. Together, these implement **NIST 800-53 common controls** — individual systems inherit the control implementations by onboarding.

## What this does

- **Pins GitHub Actions** — converts mutable tag refs (`@v4`) to immutable SHA-256 commit hashes, closing an attack vector
- **Manages all dependency updates** — npm, pip, Docker, Go, Terraform, bundler, and more
- **Detects unsupported components** — flags abandoned packages and auto-migrates to known replacements
- **Scans Actions for security issues** — template injection, credential leaks, excessive permissions, and more
- **Tracks vulnerability SLAs** — centralized weekly reporting against GSA CIO 2100.1 timelines
- **Provides machine-readable control narratives** — systems can import an OSCAL component definition into their SSPs

## Quick start for repo owners

Add a `renovate.json` to your repo:

```json
{
  "extends": ["local>GSA-TTS/scanning-service"]
}
```

This inherits all org defaults. See [docs/onboarding-playbook.md](docs/onboarding-playbook.md) for the full onboarding guide.

## For compliance teams

This capability covers 14 NIST 800-53 controls across 6 families (CM, IA, RA, SA, SI, SR). See:

- [docs/compliance/README.md](docs/compliance/README.md) — OSCAL component definition usage
- [docs/onboarding-playbook.md](docs/onboarding-playbook.md) — includes SSP boilerplate and OSCAL import instructions

## Key files

| File | Purpose |
|------|---------|
| `default.json5` | Shared Renovate preset with compliance annotations |
| `.github/workflows/renovate.yml` | Self-hosted Renovate runner (daily weekday cron) |
| `.github/workflows/monitoring.yml` | Weekly adoption and compliance metrics |
| `.github/workflows/vulnerability-sla.yml` | Centralized vulnerability SLA tracking |
| `.github/workflows/oscal-check.yml` | CI check preventing OSCAL markdown/JSON drift |
| `.github/workflows/oscal-update-consumers.yml` | Auto-PRs to consuming repos on OSCAL updates |
| `.github/workflows/zizmor-sast.yml` | Weekly GitHub Actions SAST analysis across org |
| `.github/workflows/dependency-lint.yml` | Reusable workflow for per-repo PR dependency checks |
| `.github/actions/dependency-check/action.yml` | Composite action wrapper for dependency checks |
| `docs/compliance/component-definitions/org-dependency-management/component-definition.json` | Distributable OSCAL artifact |
