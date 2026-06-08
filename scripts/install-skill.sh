#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "usage: scripts/install-skill.sh codex|claude|both" >&2
}

if [ "$#" -ne 1 ]; then
  usage
  exit 2
fi

target="$1"
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skill_src="$repo_root/skills/multi-agent-council"

if [ ! -f "$skill_src/SKILL.md" ]; then
  echo "skill source not found: $skill_src" >&2
  exit 1
fi

install_one() {
  local app="$1"
  local dest

  case "$app" in
    codex)
      dest="$HOME/.codex/skills/multi-agent-council"
      ;;
    claude)
      dest="$HOME/.claude/skills/multi-agent-council"
      ;;
    *)
      echo "unknown target: $app" >&2
      exit 2
      ;;
  esac

  mkdir -p "$(dirname "$dest")"
  rm -rf "$dest"
  cp -R "$skill_src" "$dest"
  echo "installed $app skill: $dest"
}

case "$target" in
  codex)
    install_one codex
    ;;
  claude)
    install_one claude
    ;;
  both)
    install_one codex
    install_one claude
    ;;
  *)
    usage
    exit 2
    ;;
esac

echo "restart the target app or start a new session if the skill is not visible"
