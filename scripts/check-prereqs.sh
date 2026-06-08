#!/usr/bin/env bash
set -euo pipefail

check_cmd() {
  local label="$1"
  local cmd="$2"

  if command -v "$cmd" >/dev/null 2>&1; then
    local version
    version="$("$cmd" --version 2>/dev/null | head -n 1 || true)"
    if [ -n "$version" ]; then
      printf "ok      %-18s %s\n" "$label" "$version"
    else
      printf "ok      %-18s installed\n" "$label"
    fi
  else
    printf "missing %-18s install or use manual copy/paste fallback\n" "$label"
  fi
}

echo "Multi-Agent Council prerequisite check"
echo
check_cmd "Codex CLI" codex
check_cmd "Claude Code" claude
check_cmd "Gemini agy" agy
check_cmd "Grok CLI" grok

cat <<'EOF'

Notes:
- This script checks command availability, not provider authentication.
- A full four-agent council is optional.
- If a CLI is missing or not logged in, run the council with the remaining tools
  or copy prompts into web/app UIs.
EOF
