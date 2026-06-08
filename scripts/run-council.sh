#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "usage: scripts/run-council.sh <prompt-or-example.md>" >&2
  exit 2
fi

input="$1"

if [ ! -f "$input" ]; then
  echo "not found: $input" >&2
  exit 1
fi

cat <<'EOF'
Multi-Agent Council prompt scaffold
===================================

Copy the prompt below into Codex or another coding agent.

EOF

cat council.md

cat <<'EOF'

--- Evidence / task input ---

EOF

cat "$input"
