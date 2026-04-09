---
x-trestle-comp-def-rules:
  org-dependency-management:
    - name: sha-pins-verified
      description: 'All GitHub Actions uses: refs in the repo are SHA-pinned'
    - name: actions-sast-scanned
      description: GitHub Actions workflows are scanned for security issues via 
        centralized zizmor SAST analysis
    - name: secrets-scanned
      description: Source code is scanned for leaked secrets, credentials, and 
        keys via centralized gitleaks configuration
x-trestle-param-values:
  si-7_prm_1:
  si-7_prm_2:
  si-07_odp.01:
  si-07_odp.02:
  si-07_odp.03:
  si-07_odp.04:
  si-07_odp.05:
  si-07_odp.06:
x-trestle-global:
  profile:
    title: Electronic Version of NIST SP 800-53 Rev 5.1.1 Controls and SP 
      800-53A Rev 5.1.1 Assessment Procedures
    href: 
      https://raw.githubusercontent.com/usnistgov/oscal-content/refs/tags/v1.3.0/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json
  sort-id: si-07
---

# si-7 - \[System and Information Integrity\] Software, Firmware, and Information Integrity

## Control Statement

- \[a.\] Employ integrity verification tools to detect unauthorized changes to the following software, firmware, and information: {{ insert: param, si-7_prm_1 }} ; and

- \[b.\] Take the following actions when unauthorized changes to the software, firmware, and information are detected: {{ insert: param, si-7_prm_2 }}.

## Control Assessment Objective

- \[SI-07a.\]

  - \[SI-07a.[01]\] integrity verification tools are employed to detect unauthorized changes to {{ insert: param, si-07_odp.01 }};
  - \[SI-07a.[02]\] integrity verification tools are employed to detect unauthorized changes to {{ insert: param, si-07_odp.02 }};
  - \[SI-07a.[03]\] integrity verification tools are employed to detect unauthorized changes to {{ insert: param, si-07_odp.03 }};

- \[SI-07b.\]

  - \[SI-07b.[01]\] {{ insert: param, si-07_odp.04 }} are taken when unauthorized changes to the software, are detected;
  - \[SI-07b.[02]\] {{ insert: param, si-07_odp.05 }} are taken when unauthorized changes to the firmware are detected;
  - \[SI-07b.[03]\] {{ insert: param, si-07_odp.06 }} are taken when unauthorized changes to the information are detected.

## Control guidance

Unauthorized changes to software, firmware, and information can occur due to errors or malicious activity. Software includes operating systems (with key internal components, such as kernels or drivers), middleware, and applications. Firmware interfaces include Unified Extensible Firmware Interface (UEFI) and Basic Input/Output System (BIOS). Information includes personally identifiable information and metadata that contains security and privacy attributes associated with information. Integrity-checking mechanisms—including parity checks, cyclical redundancy checks, cryptographic hashes, and associated tools—can automatically monitor the integrity of systems and hosted applications.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

SHA-256 commit hashes provide cryptographic integrity verification for all GitHub Actions dependencies. The exact code that was reviewed is the code that runs. Tag references (`@v4`) are mutable and can be force-pushed by upstream maintainers; SHA references cannot be altered without detection.

The `pinDigests` setting enforces this automatically across all repos.

Beyond SHA pinning, centralized SAST analysis detects integrity threats specific to GitHub Actions workflows: template injection vulnerabilities where attacker-controlled inputs are expanded into executable code, credential persistence risks where secrets may leak into logs or artifacts, and `GITHUB_ENV` abuse that could allow code execution via environment variable injection. Findings are reported as issues or auto-fix PRs weekly.

Centralized gitleaks scanning detects embedded secrets, credentials, and private keys that compromise source code integrity.

### Rules:

  - sha-pins-verified
  - actions-sast-scanned
  - secrets-scanned

### Implementation Status: implemented

______________________________________________________________________
