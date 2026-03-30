---
x-trestle-comp-def-rules:
  org-dependency-management:
    - name: depmgmt-implemented
      description: This control is fully implemented for the scope of the org 
        dependency management component
x-trestle-param-values:
  sr-03_odp.01:
  sr-03_odp.02:
  sr-03_odp.03:
  sr-03_odp.04:
  sr-03_odp.05:
x-trestle-global:
  profile:
    title: Electronic Version of NIST SP 800-53 Rev 5.1.1 Controls and SP 
      800-53A Rev 5.1.1 Assessment Procedures
    href: 
      https://raw.githubusercontent.com/usnistgov/oscal-content/refs/tags/v1.3.0/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json
  sort-id: sr-03
---

# sr-3 - \[Supply Chain Risk Management\] Supply Chain Controls and Processes

## Control Statement

- \[a.\] Establish a process or processes to identify and address weaknesses or deficiencies in the supply chain elements and processes of {{ insert: param, sr-03_odp.01 }} in coordination with {{ insert: param, sr-03_odp.02 }};

- \[b.\] Employ the following controls to protect against supply chain risks to the system, system component, or system service and to limit the harm or consequences from supply chain-related events: {{ insert: param, sr-03_odp.03 }} ; and

- \[c.\] Document the selected and implemented supply chain processes and controls in {{ insert: param, sr-03_odp.04 }}.

## Control Assessment Objective

- \[SR-03a.\]

  - \[SR-03a.[01]\] a process or processes is/are established to identify and address weaknesses or deficiencies in the supply chain elements and processes of {{ insert: param, sr-03_odp.01 }};
  - \[SR-03a.[02]\] the process or processes to identify and address weaknesses or deficiencies in the supply chain elements and processes of {{ insert: param, sr-03_odp.01 }} is/are coordinated with {{ insert: param, sr-03_odp.02 }};

- \[SR-03b.\] {{ insert: param, sr-03_odp.03 }} are employed to protect against supply chain risks to the system, system component, or system service and to limit the harm or consequences from supply chain-related events;

- \[SR-03c.\] the selected and implemented supply chain processes and controls are documented in {{ insert: param, sr-03_odp.04 }}.

## Control guidance

Supply chain elements include organizations, entities, or tools employed for the research and development, design, manufacturing, acquisition, delivery, integration, operations and maintenance, and disposal of systems and system components. Supply chain processes include hardware, software, and firmware development processes; shipping and handling procedures; personnel security and physical security programs; configuration management tools, techniques, and measures to maintain provenance; or other programs, processes, or procedures associated with the development, acquisition, maintenance and disposal of systems and system components. Supply chain elements and processes may be provided by organizations, system integrators, or external providers. Weaknesses or deficiencies in supply chain elements or processes represent potential vulnerabilities that can be exploited by adversaries to cause harm to the organization and affect its ability to carry out its core missions or business functions. Supply chain personnel are individuals with roles and responsibilities in the supply chain.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

The org establishes a supply chain risk management process for CI/CD dependencies: centralized scanning (Renovate), version pinning (SHA), integrity verification (cryptographic hash), vulnerability monitoring (Dependabot alerts + SLA tracking), and automated remediation (Renovate PRs). This covers all dependency ecosystems, not just GitHub Actions.

The process includes automated detection of abandoned or deprecated packages (`abandonments:recommended`), migration to known successors (`replacements:all`), and centralized monitoring of remediation timelines to ensure supply chain risks are addressed within organizational SLAs.

### Rules:

  - depmgmt-implemented

### Implementation Status: implemented

______________________________________________________________________
