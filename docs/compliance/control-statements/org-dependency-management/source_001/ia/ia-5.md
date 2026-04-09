---
x-trestle-comp-def-rules:
  org-dependency-management:
    - name: secrets-scanned
      description: Source code is scanned for leaked secrets, credentials, and 
        keys via centralized gitleaks configuration
x-trestle-param-values:
  ia-05_odp.01:
  ia-05_odp.02:
  ia-05_odp.03:
  ia-05_odp.04:
  ia-05_odp.05:
  ia-05_odp.06:
  ia-05_odp.07:
  ia-05_odp.08:
  ia-05_odp.09:
  ia-05_odp.10:
  ia-05_odp.11:
  ia-05_odp.12:
x-trestle-global:
  profile:
    title: Electronic Version of NIST SP 800-53 Rev 5.1.1 Controls and SP 
      800-53A Rev 5.1.1 Assessment Procedures
    href: 
      https://raw.githubusercontent.com/usnistgov/oscal-content/refs/tags/v1.3.0/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json
  sort-id: ia-05
---

# ia-5 - \[Identification and Authentication\] Authenticator Management

## Control Statement

Manage system authenticators by:

- \[a.\] Verifying, as part of the initial authenticator distribution, the identity of the individual, group, role, service, or device receiving the authenticator;

- \[b.\] Establishing initial authenticator content for any authenticators issued by the organization;

- \[c.\] Ensuring that authenticators have sufficient strength of mechanism for their intended use;

- \[d.\] Establishing and implementing administrative procedures for initial authenticator distribution, for lost or compromised or damaged authenticators, and for revoking authenticators;

- \[e.\] Changing default authenticators prior to first use;

- \[f.\] Changing or refreshing authenticators {{ insert: param, ia-05_odp.01 }} or when {{ insert: param, ia-05_odp.02 }} occur;

- \[g.\] Protecting authenticator content from unauthorized disclosure and modification;

- \[h.\] Requiring individuals to take, and having devices implement, specific controls to protect authenticators; and

- \[i.\] Changing authenticators for group or role accounts when membership to those accounts changes.

## Control Assessment Objective

- \[IA-05a.\] authenticators are managed through the verification of the identity of the individual, group, role, service, or device receiving the authenticator as part of the initial authenticator distribution;

- \[IA-05b.\] authenticators are managed through the establishment of initial authenticator content for any authenticators issued by the organization;

- \[IA-05c.\] authenticators are managed to ensure that authenticators have sufficient strength of mechanism for their intended use;

- \[IA-05d.\] authenticators are managed through the establishment and implementation of administrative procedures for initial authenticator distribution; for lost, compromised, or damaged authenticators; and for revoking authenticators;

- \[IA-05e.\] authenticators are managed through the change of default authenticators prior to first use;

- \[IA-05f.\] authenticators are managed through the change or refreshment of authenticators {{ insert: param, ia-05_odp.01 }} or when {{ insert: param, ia-05_odp.02 }} occur;

- \[IA-05g.\] authenticators are managed through the protection of authenticator content from unauthorized disclosure and modification;

- \[IA-05h.\]

  - \[IA-05h.[01]\] authenticators are managed by requiring individuals to take specific controls to protect authenticators;
  - \[IA-05h.[02]\] authenticators are managed by having devices implement specific controls to protect authenticators;

- \[IA-05i.\] authenticators are managed through the change of authenticators for group or role accounts when membership to those accounts changes.

## Control guidance

Authenticators include passwords, cryptographic devices, biometrics, certificates, one-time password devices, and ID badges. Device authenticators include certificates and passwords. Initial authenticator content is the actual content of the authenticator (e.g., the initial password). In contrast, the requirements for authenticator content contain specific criteria or characteristics (e.g., minimum password length). Developers may deliver system components with factory default authentication credentials (i.e., passwords) to allow for initial installation and configuration. Default authentication credentials are often well known, easily discoverable, and present a significant risk. The requirement to protect individual authenticators may be implemented via control [PL-4](#pl-4) or [PS-6](#ps-6) for authenticators in the possession of individuals and by controls [AC-3](#ac-3), [AC-6](#ac-6), and [SC-28](#sc-28) for authenticators stored in organizational systems, including passwords stored in hashed or encrypted formats or files containing encrypted or hashed passwords accessible with administrator privileges.

Systems support authenticator management by organization-defined settings and restrictions for various authenticator characteristics (e.g., minimum password length, validation time window for time synchronous one-time tokens, and number of allowed rejections during the verification stage of biometric authentication). Actions can be taken to safeguard individual authenticators, including maintaining possession of authenticators, not sharing authenticators with others, and immediately reporting lost, stolen, or compromised authenticators. Authenticator management includes issuing and revoking authenticators for temporary access when no longer needed.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

Centralized gitleaks scanning detects leaked authenticators (passwords, API keys, tokens, private keys) in source code repositories. The org-wide `.gitleaks.toml` configuration includes GSA-specific patterns for cloud.gov service keys, Cloud Foundry credentials, and Login.gov private key material. Weekly audits scan all onboarded repos, and per-PR checks prevent new secrets from being committed. Pre-commit hooks provide an additional layer of prevention before secrets reach the remote repository.

### Rules:

  - secrets-scanned

### Implementation Status: implemented

______________________________________________________________________
