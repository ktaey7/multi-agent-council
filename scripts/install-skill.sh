#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
usage: scripts/install-skill.sh [--dry-run] [--uninstall] codex|claude|both

Environment overrides:
  CODEX_SKILLS_DIR     default: $HOME/.agents/skills
  CLAUDE_SKILLS_DIR    default: $HOME/.claude/skills
  CLAUDE_COMMANDS_DIR  default: $HOME/.claude/commands
EOF
}

dry_run=0
uninstall=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --dry-run)
      dry_run=1
      shift
      ;;
    --uninstall)
      uninstall=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      break
      ;;
  esac
done

if [ "$#" -ne 1 ]; then
  usage
  exit 2
fi

target="$1"
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skill_src="$repo_root/.agents/skills/multi-agent-council"

if [ ! -f "$skill_src/SKILL.md" ]; then
  echo "skill source not found: $skill_src" >&2
  exit 1
fi

run() {
  if [ "$dry_run" -eq 1 ]; then
    printf 'dry-run:'
    printf ' %q' "$@"
    printf '\n'
  else
    "$@"
  fi
}

install_one() {
  local app="$1"
  local base
  local dest

  case "$app" in
    codex)
      # Codex reads user skills from ~/.agents/skills and repo skills from
      # .agents/skills. Override when testing or using a custom environment.
      base="${CODEX_SKILLS_DIR:-$HOME/.agents/skills}"
      ;;
    claude)
      base="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
      ;;
    *)
      echo "unknown target: $app" >&2
      exit 2
      ;;
  esac

  dest="$base/multi-agent-council"

  if [ "$uninstall" -eq 1 ]; then
    run rm -rf "$dest"
    if [ "$dry_run" -eq 1 ]; then
      echo "would uninstall $app skill: $dest"
    else
      echo "uninstalled $app skill: $dest"
    fi
    if [ "$app" = "claude" ]; then
      local cmd_dest="${CLAUDE_COMMANDS_DIR:-$HOME/.claude/commands}/council.md"
      run rm -f "$cmd_dest"
      if [ "$dry_run" -eq 1 ]; then
        echo "would uninstall claude command: $cmd_dest"
      else
        echo "uninstalled claude command: $cmd_dest"
      fi
    fi
    return
  fi

  run mkdir -p "$base"
  run rm -rf "$dest"
  run cp -R "$skill_src" "$dest"

  if [ "$dry_run" -eq 0 ] && [ ! -f "$dest/SKILL.md" ]; then
    echo "install failed: $dest/SKILL.md was not created" >&2
    exit 1
  fi

  if [ "$app" = "claude" ]; then
    local cmd_src="$repo_root/commands/council.md"
    local cmd_base="${CLAUDE_COMMANDS_DIR:-$HOME/.claude/commands}"
    if [ -f "$cmd_src" ]; then
      run mkdir -p "$cmd_base"
      run cp "$cmd_src" "$cmd_base/council.md"
      if [ "$dry_run" -eq 1 ]; then
        echo "would install claude command: $cmd_base/council.md"
      else
        echo "installed claude command: $cmd_base/council.md"
      fi
    fi
  fi

  if [ "$dry_run" -eq 1 ]; then
    echo "would install $app skill: $dest"
  else
    echo "installed $app skill: $dest"
  fi
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

if [ "$uninstall" -eq 0 ] && [ "$dry_run" -eq 0 ]; then
  echo "restart the target app or start a new session if the skill is not visible"
fi
