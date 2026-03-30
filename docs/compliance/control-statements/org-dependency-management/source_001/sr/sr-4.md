---
x-trestle-comp-def-rules:
  org-dependency-management:
    - name: sha-pins-verified
      description: 'All GitHub Actions uses: refs in the repo are SHA-pinned'
x-trestle-param-values:
  sr-04_odp:
x-trestle-global:
  profile:
    title: Electronic Version of NIST SP 800-53 Rev 5.1.1 Controls and SP 
      800-53A Rev 5.1.1 Assessment Procedures
    href: 
      https://raw.githubusercontent.com/usnistgov/oscal-content/refs/tags/v1.3.0/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json
  sort-id: sr-04
---

# sr-4 - \[Supply Chain Risk Management\] Provenance

## Control Statement

Document, monitor, and maintain valid provenance of the following systems, system components, and associated data: {{ insert: param, sr-04_odp }}.

## Control Assessment Objective

- \[SR-04[01]\] valid provenance is documented for {{ insert: param, sr-04_odp }};

- \[SR-04[02]\] valid provenance is monitored for {{ insert: param, sr-04_odp }};

- \[SR-04[03]\] valid provenance is maintained for {{ insert: param, sr-04_odp }}.

## Control guidance

Every system and system component has a point of origin and may be changed throughout its existence. Provenance is the chronology of the origin, development, ownership, location, and changes to a system or system component and associated data. It may also include personnel and processes used to interact with or make modifications to the system, component, or associated data. Organizations consider developing procedures (see [SR-1](#sr-1) ) for allocating responsibilities for the creation, maintenance, and monitoring of provenance for systems and system components; transferring provenance documentation and responsibility between organizations; and preventing and monitoring for unauthorized changes to the provenance records. Organizations have methods to document, monitor, and maintain valid provenance baselines for systems, system components, and related data. These actions help track, assess, and document any changes to the provenance, including changes in supply chain elements or configuration, and help ensure non-repudiation of provenance information and the provenance change records. Provenance considerations are addressed throughout the system development life cycle and incorporated into contracts and other arrangements, as appropriate.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

SHA pins create a verifiable chain from the exact upstream commit to the workflow that runs in the org's CI. Version comments (e.g., `# v4.2.2`) provide human-readable provenance alongside the machine-verifiable hash.

The `pinDigestsHelper` setting adds these version comments automatically, ensuring every SHA-pinned reference includes both the cryptographic identifier and the human-readable version for provenance documentation. This enables auditors to trace exactly which version of each dependency was used in any given CI run.

### Rules:

  - sha-pins-verified

### Implementation Status: implemented

______________________________________________________________________
