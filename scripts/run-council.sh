#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cat >&2 <<'EOF'
warning: scripts/run-council.sh prints a council prompt; it does not invoke agents.
use scripts/print-council-prompt.sh directly for the same behavior.
EOF

exec "$script_dir/print-council-prompt.sh" "$@"
