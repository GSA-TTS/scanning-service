---
x-trestle-comp-def-rules:
  org-dependency-management:
    - name: sha-pins-verified
      description: 'All GitHub Actions uses: refs in the repo are SHA-pinned'
    - name: actions-sast-scanned
      description: GitHub Actions workflows are scanned for security issues via 
        centralized zizmor SAST analysis
x-trestle-param-values:
  cm-7_prm_2:
  cm-07_odp.01:
  cm-07_odp.02:
  cm-07_odp.03:
  cm-07_odp.04:
  cm-07_odp.05:
  cm-07_odp.06:
x-trestle-global:
  profile:
    title: Electronic Version of NIST SP 800-53 Rev 5.1.1 Controls and SP 
      800-53A Rev 5.1.1 Assessment Procedures
    href: 
      https://raw.githubusercontent.com/usnistgov/oscal-content/refs/tags/v1.3.0/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json
  sort-id: cm-07
---

# cm-7 - \[Configuration Management\] Least Functionality

## Control Statement

- \[a.\] Configure the system to provide only {{ insert: param, cm-07_odp.01 }} ; and

- \[b.\] Prohibit or restrict the use of the following functions, ports, protocols, software, and/or services: {{ insert: param, cm-7_prm_2 }}.

## Control Assessment Objective

- \[CM-07a.\] the system is configured to provide only {{ insert: param, cm-07_odp.01 }};

- \[CM-07b.\]

  - \[CM-07b.[01]\] the use of {{ insert: param, cm-07_odp.02 }} is prohibited or restricted;
  - \[CM-07b.[02]\] the use of {{ insert: param, cm-07_odp.03 }} is prohibited or restricted;
  - \[CM-07b.[03]\] the use of {{ insert: param, cm-07_odp.04 }} is prohibited or restricted;
  - \[CM-07b.[04]\] the use of {{ insert: param, cm-07_odp.05 }} is prohibited or restricted;
  - \[CM-07b.[05]\] the use of {{ insert: param, cm-07_odp.06 }} is prohibited or restricted.

## Control guidance

Systems provide a wide variety of functions and services. Some of the functions and services routinely provided by default may not be necessary to support essential organizational missions, functions, or operations. Additionally, it is sometimes convenient to provide multiple services from a single system component, but doing so increases risk over limiting the services provided by that single component. Where feasible, organizations limit component functionality to a single function per component. Organizations consider removing unused or unnecessary software and disabling unused or unnecessary physical and logical ports and protocols to prevent unauthorized connection of components, transfer of information, and tunneling. Organizations employ network scanning tools, intrusion detection and prevention systems, and end-point protection technologies, such as firewalls and host-based intrusion detection systems, to identify and prevent the use of prohibited functions, protocols, ports, and services. Least functionality can also be achieved as part of the fundamental design and development of the system (see [SA-8](#sa-8), [SC-2](#sc-2) , and [SC-3](#sc-3)).

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

SHA pinning ensures repos use only the exact, reviewed version of each Action — not whatever a mutable tag (e.g., `@v4` or `@main`) resolves to at any given moment. This reduces attack surface from mutable references and enforces least functionality for CI/CD pipeline dependencies.

The `pinDigests` setting converts all tag-based references to immutable SHA-256 commit hashes, ensuring only the specific reviewed code version executes in CI pipelines.

Centralized SAST analysis detects excessive permission scopes granted to workflow runners, flagging cases where `permissions:` declarations exceed what the workflow actually needs. This enforces least functionality for CI/CD workflow configurations beyond just dependency versions.

### Rules:

  - sha-pins-verified
  - actions-sast-scanned

### Implementation Status: implemented

______________________________________________________________________

## Implementation for part a.

SHA pinning ensures repos use only the exact, reviewed version of each Action — not whatever a mutable tag (e.g., @v4 or @main) resolves to at any given moment. This reduces attack surface from mutable references and enforces least functionality for CI/CD pipeline dependencies. Centralized zizmor SAST analysis detects excessive permission scopes granted to workflow runners, flagging cases where permissions exceed what the workflow actually needs.

### Rules:

  - sha-pins-verified
  - actions-sast-scanned

### Implementation Status: implemented

______________________________________________________________________
