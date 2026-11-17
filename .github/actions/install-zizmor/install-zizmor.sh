#!/usr/bin/env bash

set -euo pipefail

# Keep this version and checksum coupled. Renovate cannot update a GitHub
# release-asset checksum with the version, so updating only the version would
# fail closed at verification time.
ZIZMOR_VERSION="1.32.0"
ZIZMOR_SHA256="bb110cc765eca9cd7efb2e284a956be5974c60027b0970f16397d86208a9957b"
ARCHIVE="${RUNNER_TEMP}/zizmor-${ZIZMOR_VERSION}-x86_64-unknown-linux-gnu.tar.gz"
INSTALL_DIR="${RUNNER_TEMP}/zizmor-${ZIZMOR_VERSION}"

curl -sfL "https://github.com/woodruffw/zizmor/releases/download/v${ZIZMOR_VERSION}/zizmor-x86_64-unknown-linux-gnu.tar.gz" -o "$ARCHIVE"
echo "${ZIZMOR_SHA256}  ${ARCHIVE}" | sha256sum --check

rm -rf "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
tar xzf "$ARCHIVE" -C "$INSTALL_DIR"
chmod +x "$INSTALL_DIR/zizmor"
echo "$INSTALL_DIR" >> "$GITHUB_PATH"
