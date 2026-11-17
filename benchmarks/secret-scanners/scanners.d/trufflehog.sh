trufflehog_available()      { command -v trufflehog >/dev/null 2>&1; }
trufflehog_validation()     { echo "yes"; }
trufflehog_config_interop() { echo "partial (detector allow/exclude config)"; }

trufflehog_scan() {
  local target="$1" out="$2" raw
  raw="$(mktemp)"
  # --no-verification keeps the benchmark offline & deterministic; verification
  # is scored separately as a capability, not a per-run behavior.
  trufflehog filesystem "$target" --json --no-verification > "$raw" 2>/dev/null || true
  # Findings are NDJSON; keep only lines that are real finding objects.
  grep '"SourceMetadata"' "$raw" 2>/dev/null \
    | jq -s '[.[] | {file:(.SourceMetadata.Data.Filesystem.file | sub("^.*/";"")), rule:.DetectorName}]' \
    > "$out" 2>/dev/null || echo '[]' > "$out"
  rm -f "$raw"
}
