# Secret Scanner Benchmark

Reproducible harness to benchmark [gitleaks](https://github.com/gitleaks/gitleaks)
(the org baseline) against alternative secret scanners, addressing
[issue #23](https://github.com/GSA-TTS/scanning-service/issues/23).

Scanners covered:

| Scanner | Default | Source |
|---|---|---|
| gitleaks | on (baseline) | https://github.com/gitleaks/gitleaks |
| [trufflehog](https://github.com/trufflesecurity/trufflehog) | on | issue #23 |
| [kingfisher](https://github.com/mongodb/kingfisher) | on | issue #23 |
| [ripsecrets](https://github.com/sirwart/ripsecrets) | on | sirwart |

> [ggshield](https://github.com/GitGuardian/ggshield) is intentionally excluded:
> its detection engine is server-side (GitGuardian SaaS API), so it cannot run in
> an offline, deterministic benchmark. See [ADR-0003](../../docs/decisions/0003-exclude-saas-backed-secret-scanners-from-benchmark.md).

## Quick start

```bash
cd benchmarks/secret-scanners
./bin/run-benchmark                 # scores default scanners on the synthetic corpus
```

Output goes to `results/latest.md` and `results/latest.json`.

## Metrics

Scoring is at **file granularity** against a synthetic corpus whose ground truth
is encoded in filename prefixes (`pos_` = planted secret, `neg_` = benign
look-alike):

| Metric | Meaning |
|---|---|
| **Recall** | share of planted secrets detected — `TP / (TP + FN)` |
| **Precision** | share of flags that are real — `TP / (TP + FP)` |
| **F1** | harmonic mean of precision and recall |
| **TP / FN / FP** | positives caught / positives missed / benign files wrongly flagged |
| **Findings** | raw finding count (dedup insensitivity / noisiness) |
| **Median s** | median wall-clock scan time over N runs (`runs` in `scanners.json`) |
| **Validation** | can the tool verify a credential is live? (capability) |
| **Config interop** | shared/custom rule config support (for 1:1 matching) |

The negative set intentionally mirrors the real false-positive fixtures in
[bin/test-gitleaks-config](../../bin/test-gitleaks-config) (placeholders,
`${interpolation}` refs, PEM-strip shell commands, `VCAP_SERVICES` variable
refs, the allowlisted AWS `EXAMPLE` key) so precision reflects real-world tuning.

## Redaction

The corpus contains realistic — but **randomly generated and fake** — secret
material. Two safeguards keep specifics out of the repo:

1. The corpus is written to a `.gitignore`'d directory (`.corpus/`), so no
   literal secret is ever committed. Ground truth lives in filenames, not in a
   manifest of values.
2. Adapters normalize each tool's output to `{file, rule}` only — secret values,
   snippets, and raw matches are dropped before scoring. `results/*.md|json` are
   therefore safe to share, and are also gitignored by default.

## Enabling more scanners (for repos that extend this one)

The four bundled adapters run fully offline. Add your own scanner two ways:

1. **Flip a flag.** Toggle `"enabled"` in [scanners.json](scanners.json).
2. **Add an adapter.** Drop `scanners.d/<tool>.sh` implementing the adapter
   contract (documented at the top of [scanners.d/gitleaks.sh](scanners.d/gitleaks.sh))
   and add a matching entry to `scanners.json`. The runner discovers adapters
   automatically — downstream repos that vendor or extend this benchmark do the
   same without editing `bin/run-benchmark`.

> SaaS-backed scanners (e.g. GitGuardian ggshield) are out of scope for this
> offline harness — see [ADR-0003](../../docs/decisions/0003-exclude-saas-backed-secret-scanners-from-benchmark.md).

Run everything that happens to be installed, regardless of config:

```bash
./bin/run-benchmark --all-available
```

## Other options

```bash
./bin/run-benchmark --scanner gitleaks --scanner kingfisher   # subset
./bin/run-benchmark --runs 5                                   # more timing samples
./bin/run-benchmark --target /path/to/local/repo              # scan a real repo (unscored: findings + speed only)
./bin/run-benchmark --keep-corpus                             # reuse existing corpus
GITLEAKS_CONFIG=../../.gitleaks.toml ./bin/run-benchmark      # score gitleaks with the org config
```

## Layout

```
benchmarks/secret-scanners/
  scanners.json        enable/disable + runs config
  bin/run-benchmark    orchestrator (timing, selection, scoring)
  bin/generate-corpus  synthetic, redacted corpus generator
  scanners.d/*.sh      per-scanner adapters (extension point)
  lib/score.py         metric computation + markdown/JSON report
  results/             generated reports (gitignored)
```
