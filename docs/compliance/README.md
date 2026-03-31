# OSCAL Component Definition: org-dependency-management

This directory contains the OSCAL 1.1.2 component definition for the GSA-TTS centralized dependency management service, covering 14 NIST 800-53 Rev 5 controls across 6 families.

## What this is

The `org-dependency-management` component defines how the org's centralized Renovate configuration, GitHub App, vulnerability SLA tracking, and CI lint checks implement dependency management controls. Systems that onboard to this service can import the component definition and incorporate its control narratives into their own SSPs.

## Controls covered

| Family | Controls |
|--------|----------|
| CM | CM-2, CM-3, CM-6, CM-7 |
| IA | IA-9 |
| RA | RA-5 |
| SA | SA-10, SA-11, SA-22 |
| SI | SI-2, SI-7 |
| SR | SR-3, SR-4, SR-11 |

## Importing into your system's SSP

Inside `docker-trestle`, from your system's `docs/compliance` directory:

```bash
copy-component -n org-dependency-management \
  -u https://raw.githubusercontent.com/GSA-TTS/scanning-service/refs/heads/main/docs/compliance/component-definitions/org-dependency-management/component-definition.json
```

Then add to your `trestle-config.yaml`:

```yaml
components:
  - org-dependency-management
  # ... your other components
```

The next SSP assembly merges the component's control narratives alongside your system's own `### This System` sections.

## Authoring workflow

To edit control narratives:

```bash
# Enter docker-trestle
docker run -it --rm -e SKIP_TRESTLE_CONFIG=true -v $(pwd):/app/docs \
  ghcr.io/gsa-tts/trestle bash

# Edit markdown files under control-statements/
# Then assemble back to JSON:
bin/assemble-depmgmt-json

# Or regenerate markdown from JSON:
bin/generate-depmgmt-markdown
```

## CI validation

The `oscal-check.yml` workflow validates on every PR that touches `docs/compliance/`:
- `component-definition.json` is valid OSCAL 1.1.2
- Committed markdown and JSON are in sync (no drift)

## Versioning

When control narratives change substantively:
1. Edit the markdown, run `bin/assemble-depmgmt-json`
2. Bump `version` in `component-definition.json` metadata
3. After merge, create a GitHub Release with the new version tag
4. The `oscal-update-consumers.yml` workflow automatically opens PRs in consuming repos
