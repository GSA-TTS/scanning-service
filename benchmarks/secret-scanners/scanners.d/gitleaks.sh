# Adapter contract (sourced by bin/run-benchmark; bash 3.2 compatible)
#
#   <id>_available        -> exit 0 if the scanner binary is installed
#   <id>_validation       -> echo "yes"/"no" (can it verify live credentials?)
#   <id>_config_interop   -> echo short note on shared/custom config support
#   <id>_scan DIR OUT     -> scan DIR, write normalized findings JSON to OUT:
#                              [{"file":"<basename>","rule":"<rule-id>"}, ...]
#
# The normalized output MUST NOT contain secret values — only file basenames and
# rule identifiers. This keeps every generated report safe to share (redacted).

gitleaks_available()      { command -v gitleaks >/dev/null 2>&1; }
gitleaks_validation()     { echo "no"; }
gitleaks_config_interop() { echo "yes (.gitleaks.toml / --config)"; }

gitleaks_scan() {
  local target="$1" out="$2" raw cfg=""
  raw="$(mktemp)"
  [ -n "${GITLEAKS_CONFIG:-}" ] && cfg="--config=${GITLEAKS_CONFIG}"
  gitleaks detect --source="$target" --no-git $cfg \
    --report-format=json --report-path="$raw" >/dev/null 2>&1 || true
  jq '[.[] | {file:(.File | sub("^.*/";"")), rule:.RuleID}]' "$raw" \
    > "$out" 2>/dev/null || echo '[]' > "$out"
  rm -f "$raw"
}
