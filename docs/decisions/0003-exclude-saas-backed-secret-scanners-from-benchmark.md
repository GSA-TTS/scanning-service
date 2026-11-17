---
status: "proposed"
date: 2026-08-13
decision-makers: []
---

# Exclude SaaS-backed secret scanners from the benchmark

## Context and Problem Statement

[Issue #23](https://github.com/GSA-TTS/scanning-service/issues/23) asks us to
benchmark gitleaks against alternative secret scanners. While building the
harness we evaluated GitGuardian [ggshield](https://github.com/GitGuardian/ggshield),
whose detection engine is server-side: every `ggshield secret scan` uploads file
content to the GitGuardian SaaS API and requires a `GITGUARDIAN_API_KEY`. There
is no local/offline detection mode (`ggshield -m local` and similar do not
exist). Should a SaaS-backed scanner participate in an offline benchmark?

## Decision Drivers

- The benchmark must be **offline, deterministic, and reproducible** in CI without external credentials or network egress.
- Sending scan content — including deliberately planted secret material — to a **third-party SaaS is a data-handling concern** that would require ATO review before use on real repositories.
- A **fair comparison** requires every tool to scan the same corpus locally under comparable methodology; a network round-trip confounds the speed metric.
- Including a tool that silently produces zero findings when unauthenticated yields **misleading precision/recall**.

## Considered Options

- Include ggshield, gated on authentication (auto-skip when no API key)
- Exclude SaaS-backed scanners entirely
- Stub/mock the GitGuardian API for the benchmark

## Decision Outcome

Chosen option: "Exclude SaaS-backed scanners entirely", because the benchmark's
value comes from being an offline, credential-free, reproducible comparison, and
a scanner that cannot run without shipping content to a third party violates that
premise. The harness keeps only locally-executing scanners — gitleaks,
trufflehog, kingfisher, and ripsecrets. ggshield's `scanners.json` entry is
retained but marked `enabled: false` / `role: excluded` with a pointer to this
ADR, so the exclusion is documented rather than silently dropped.

### Consequences

- Good, because the benchmark runs with no network egress, no credentials, and identical local methodology for every tool — results are reproducible in CI.
- Good, because no planted or real secret material is transmitted to a third-party SaaS during benchmarking.
- Good, because timing and detection metrics are not confounded by network latency or an unauthenticated no-op run.
- Bad, because the benchmark does not measure GitGuardian's detection quality, which some teams may want to compare.
- Neutral, because teams that already hold a GitGuardian ATO can still evaluate ggshield out-of-band; the extensible adapter model (`scanners.d/<tool>.sh`) makes re-adding it straightforward if the offline constraint is ever relaxed.

### Confirmation

- `benchmarks/secret-scanners/scanners.d/` contains no `ggshield.sh` adapter.
- `scanners.json` lists ggshield with `enabled: false` and `role: excluded`, referencing this ADR.
- `bin/run-benchmark` completes with no outbound network calls for the default scanner set.

## Pros and Cons of the Options

### Include ggshield, gated on authentication

Run ggshield only when `GITGUARDIAN_API_KEY` (or a cached session) is present;
skip otherwise.

- Good, because it lets teams with GitGuardian credentials get a data point.
- Bad, because results become non-reproducible — they depend on who holds a key.
- Bad, because it transmits corpus content (including planted secrets) to a third-party SaaS.
- Bad, because the network round-trip makes the speed metric non-comparable.

### Exclude SaaS-backed scanners entirely

Restrict the harness to locally-executing scanners.

- Good, because offline, deterministic, credential-free, and reproducible in CI.
- Good, because no data leaves the machine.
- Bad, because GitGuardian's detection quality is not represented.

### Stub/mock the GitGuardian API

Point ggshield at a local mock instance.

- Good, because it would keep everything offline.
- Bad, because a mock does not exercise GitGuardian's real detectors — it measures nothing meaningful.
- Bad, because significant effort to build and maintain a faithful mock.

## More Information

- [Benchmark harness](../../benchmarks/secret-scanners/README.md) — usage, metrics, and redaction model
- [Issue #23](https://github.com/GSA-TTS/scanning-service/issues/23) — original benchmark request
- Revisit this decision if a future ggshield release adds an offline detection mode, or if the org obtains an ATO covering GitGuardian data handling.
