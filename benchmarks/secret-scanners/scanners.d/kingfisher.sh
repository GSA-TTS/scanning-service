kingfisher_available()      { command -v kingfisher >/dev/null 2>&1; }
kingfisher_validation()     { echo "yes"; }
kingfisher_config_interop() { echo "yes (--rules-path custom YAML)"; }

kingfisher_scan() {
  local target="$1" out="$2" raw
  raw="$(mktemp)"
  kingfisher scan "$target" --no-validate --no-update-check \
    --format json --output "$raw" >/dev/null 2>&1 || true
  jq '[.findings[]? | {file:(.finding.path | sub("^.*/";"")), rule:.rule.name}]' "$raw" \
    > "$out" 2>/dev/null || echo '[]' > "$out"
  rm -f "$raw"
}
