# Opt-in adapter. ripsecrets is not bundled; enable in scanners.json after
# `cargo install ripsecrets` (or `brew install ripsecrets`).
# ripsecrets has no JSON mode, so we parse its "path:line: value" text output
# and discard the value column (redaction).

ripsecrets_available()      { command -v ripsecrets >/dev/null 2>&1; }
ripsecrets_validation()     { echo "no"; }
ripsecrets_config_interop() { echo "partial (.ripsecretsignore)"; }

ripsecrets_scan() {
  local target="$1" out="$2" raw
  raw="$(mktemp)"
  ( cd "$target" && ripsecrets . ) > "$raw" 2>/dev/null || true
  python3 - "$raw" > "$out" <<'PY'
import sys, re, os, json
findings = []
for line in open(sys.argv[1], errors="ignore"):
    m = re.match(r'^(.*?):(\d+):', line.rstrip("\n"))
    if m:
        findings.append({"file": os.path.basename(m.group(1)), "rule": "ripsecrets"})
print(json.dumps(findings))
PY
  rm -f "$raw"
}
