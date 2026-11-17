## Context

The centralized scanning workflows downloaded zizmor from a mutable `latest` release URL, and the self-hosted Renovate runner was behind the current release.

## Changes

- Pin all zizmor installations to `v1.32.0` and verify the published Linux x86_64 artifact SHA-256 before extraction.
- Update `renovatebot/github-action` from `v46.1.7` to `v46.3.14`, retaining its full commit-SHA pin.
- Leave gitleaks at `v8.30.1`; it is already the latest release.

## Review focus

Routine dependency update. Review the zizmor release URL and checksum (`bb110cc765eca9cd7efb2e284a956be5974c60027b0970f16397d86208a9957b`) in the four installation sites.

<details>
<summary>Verification</summary>

Passed:

```text
git diff --check
zizmor v1.32.0 Linux x86_64 artifact SHA-256 verification
zizmor archive contains the expected executable
Renovate v46.3.14 tag resolves to acdd6bda8b035c99ce59d5675816af2aa65a1774
adversarial review: no blockers
```

Blocked by existing baseline failures (also reproduced from `main`):

```text
actionlint .github/workflows/*.yml
bin/test-gitleaks-config
```

`actionlint` reports pre-existing ShellCheck findings. `bin/test-gitleaks-config` fails its existing false-positive suppression case and detects zero planted-secret findings. Neither failure is caused by this five-file version update.

</details>

<details>
<summary>Rollback</summary>

Revert commit `2fed5a6` to restore the former zizmor download behavior and Renovate action SHA.

</details>

## Security impact

Improves supply-chain integrity: zizmor downloads are version-pinned and checksum-verified before use. No authentication, authorization, data handling, or deployment behavior changes.

AI-assisted change; human review required before merge.
