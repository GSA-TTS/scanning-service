## Context

The centralized scanning workflows downloaded zizmor from a mutable `latest` release URL, and the self-hosted Renovate runner was behind the current release.

## Changes

- Replace four duplicated zizmor installers with one local composite action.
- Pin `zizmor` to `v1.32.0` and verify the published Linux x86_64 artifact SHA-256 before extraction.
- Update `renovatebot/github-action` from `v46.1.7` to `v46.3.14`, retaining its full commit-SHA pin.
- Leave gitleaks at `v8.30.1`; it is already the latest release.

## Review focus

Review the reusable installer action. The official `zizmorcore/zizmor-action` cannot replace it because this service needs the `zizmor` CLI for per-repository report and `--fix=all` invocations. The version and published asset checksum are deliberately updated together; Renovate cannot update the checksum atomically.

<details>
<summary>Verification</summary>

Passed:

```text
git diff --check
shared zizmor installer archive and SHA-256 verification
Renovate JSON validation
Renovate v46.3.14 tag resolves to acdd6bda8b035c99ce59d5675816af2aa65a1774
actionlint .github/workflows/dependency-lint.yml .github/workflows/monitoring.yml .github/workflows/zizmor-sast.yml
adversarial review: no blockers
```

Blocked by existing baseline failures (also reproduced from `main`):

```text
bin/test-gitleaks-config
```

`bin/test-gitleaks-config` fails its existing false-positive suppression case and detects zero planted-secret findings. It is not caused by this update.

</details>

<details>
<summary>Rollback</summary>

Revert the branch commits to restore the former inline installers and Renovate action SHA.

</details>

## Security impact

Improves supply-chain integrity: zizmor downloads are version-pinned and checksum-verified before use. No authentication, authorization, data handling, or deployment behavior changes.

AI-assisted change; human review required before merge.
