# Agreed Decision Records

This directory contains Agreed Decision Records (ADRs) for the scanning-service project.

ADRs[^1] record significant decisions along with their context and consequences.

## Index

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [ADR-0001](0001-adopt-an-adr-process.md) | Adopt an ADR process | Accepted | 2025-02-23 |
| [ADR-0002](0002-centralize-dependency-management.md) | Centralize dependency management and CI/CD security scanning | Accepted | 2026-03-26 |

## Creating a new ADR

1. Copy [adr-template.md](adr-template.md) to a new file named `NNNN-short-title.md` (zero-padded sequence number).
2. Fill in the sections. Remove any optional sections that aren't relevant.
3. Add an entry to the index table above.
4. Open a pull request for team review.

[^1]: For background on the ADR practice, see [this post](https://martinfowler.com/bliki/ArchitectureDecisionRecord.html). Rather than only memorialize decisions about "architecture", the "A" in ADR is repurposed to widen the scope for decisions captured here without losing the link to the well-known acronym. This project follows the [MADR 4.0](https://adr.github.io/madr/) format.
