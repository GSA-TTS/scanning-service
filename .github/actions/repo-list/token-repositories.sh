#!/usr/bin/env bash
# Convert a validated managed-repository list to GitHub App token scope.
set -euo pipefail
jq -er --arg owner "$1" '
  if type != "array" or length == 0 then
    error("Token repository scope must be a non-empty array")
  elif any(.[]; type != "string") then
    error("Repository identifiers must be strings")
  elif any(.[]; test("\\A[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\\z") | not) then
    error("Expected owner/repository identifiers")
  elif any(.[]; split("/")[0] | ascii_downcase != ($owner | ascii_downcase)) then
    error("Token scope must belong to the installation owner")
  else map(split("/")[1]) | unique | join(",") end
'
