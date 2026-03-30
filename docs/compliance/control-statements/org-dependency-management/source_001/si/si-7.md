---
x-trestle-comp-def-rules:
  org-dependency-management:
    - name: sha-pins-verified
      description: All GitHub Actions uses: refs in the repo are SHA-pinned
    - name: actions-sast-scanned
      description: GitHub Actions workflows are scanned for security issues via centralized
        zizmor SAST analysis
---

# si-7 - \[SI\] Software, Firmware, and Information Integrity

## Control Statement

Employ integrity verification tools to detect unauthorized changes to software, firmware, and information.

## What is the solution and how is it implemented?

### org-dependency-management

SHA-256 commit hashes provide cryptographic integrity verification for all GitHub Actions dependencies. The exact code that was reviewed is the code that runs. Tag references (`@v4`) are mutable and can be force-pushed by upstream maintainers; SHA references cannot be altered without detection.

The `pinDigests` setting enforces this automatically across all repos.

Beyond SHA pinning, centralized SAST analysis detects integrity threats specific to GitHub Actions workflows: template injection vulnerabilities where attacker-controlled inputs are expanded into executable code, credential persistence risks where secrets may leak into logs or artifacts, and `GITHUB_ENV` abuse that could allow code execution via environment variable injection. Findings are reported as issues or auto-fix PRs weekly.

#### Rules:

  - sha-pins-verified
  - actions-sast-scanned

#### Implementation Status: implemented
