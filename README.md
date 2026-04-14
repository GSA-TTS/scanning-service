# Centralized Scanning for Dependency Management & CI/CD Security

This repo provides centralized dependency management (using [Renovate](https://docs.renovatebot.com/)), GitHub Actions security analysis (using [zizmor](https://github.com/woodruffw/zizmor)), and secret scanning (using [gitleaks](https://github.com/gitleaks/gitleaks)) for the GSA-TTS GitHub org. It ships an **OSCAL component definition** covering 17 NIST 800-53 controls that individual systems can import into their SSPs.

## What this does

- **Pins GitHub Actions** — converts mutable tag refs (`@v4`) to immutable SHA-256 commit hashes, closing an attack vector
- **Manages all dependency updates** — npm, pip, Docker, Go, Terraform, bundler, and more
- **Detects unsupported components** — flags abandoned packages and auto-migrates to known replacements
- **Scans Actions for security issues** — template injection, credential leaks, excessive permissions, and more
- **Scans for leaked secrets** — centralized gitleaks configuration detects credentials, keys, and tokens in source code
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

This capability covers 17 NIST 800-53 controls across 7 families (CM, IA, RA, SA, SC, SI, SR). See:

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
| `.github/workflows/gitleaks-audit.yml` | Weekly secret scanning audit across org |
| `.github/workflows/secret-scan.yml` | Reusable workflow for per-repo PR secret scanning |
| `.github/workflows/secret-scan-test.yml` | CI self-test for secret scanning config and action |
| `.github/workflows/dependency-lint.yml` | Reusable workflow for per-repo PR dependency checks |
| `.github/actions/secret-scan/action.yml` | Composite action wrapper for secret scanning |
| `.github/actions/dependency-check/action.yml` | Composite action wrapper for dependency checks |
| `.gitleaks.toml` | Centralized gitleaks config with GSA-specific rules |
| `bin/merge-gitleaks-config` | Merges repo-local `.gitleaks.toml` allowlists into the org config |
| `docs/compliance/component-definitions/org-dependency-management/component-definition.json` | Distributable OSCAL artifact |
