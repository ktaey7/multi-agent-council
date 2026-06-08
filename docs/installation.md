# Installation

Multi-Agent Council is primarily a skill/protocol package. It can be used in
three ways:

1. Install as a Codex or Claude skill.
2. Clone and run prompts manually.
3. Copy prompts into web or app-based AI tools.

The installable skill teaches Codex or Claude Code how to run the council
workflow. The optional local runner can also stage prompts or invoke installed
local CLIs when you explicitly pass `--execute`.

## Turnkey Use (`/council`)

`scripts/install-skill.sh claude` installs both the skill and a `/council`
slash command into `~/.claude/commands/`. In a new Claude Code session, run
`/council <question>`; the agent drives a full council and returns a decision
record. This needs the participant CLIs you want to call (see Required Tools)
installed and authenticated. Codex users get the same flow via the skill
(`$multi-agent-council`); the slash command is Claude Code specific.

## Install as a Skill

Clone the repository:

```bash
git clone https://github.com/ktaey7/multi-agent-council.git
cd multi-agent-council
```

Install for Codex:

```bash
scripts/install-skill.sh codex
```

Install for Claude Code:

```bash
scripts/install-skill.sh claude
```

Install for both:

```bash
scripts/install-skill.sh both
```

The installer copies:

```text
.agents/skills/multi-agent-council/   (skill, both targets)
commands/council.md                   (Claude Code only -> ~/.claude/commands/)
```

to one or both of:

```text
~/.agents/skills/multi-agent-council/
~/.claude/skills/multi-agent-council/
```

Codex also discovers repo-scoped skills from `.agents/skills/` when you work
inside a repository. After cloning this repository, Codex can use the
repo-scoped skill without a global install. Use `/skills` or mention
`$multi-agent-council`.

The Codex user-skill directory follows the Codex agent skills convention:
`$HOME/.agents/skills`. Set `CODEX_SKILLS_DIR` to override it. Set
`CLAUDE_SKILLS_DIR` to override the Claude Code target.

Restart the target app or start a new session if it does not pick up the skill
immediately.

## Manual Use

You can use the protocol without installing a skill:

```bash
scripts/print-council-prompt.sh examples/pr-review.md
```

Then paste the generated prompt into Codex, Claude, Gemini, Grok, or another
review tool.

## Local Runner

Stage a council run without calling any agent:

```bash
scripts/council-runner.sh \
  --question "Should this PR merge?" \
  --evidence README.md \
  --evidence council.md
```

This creates:

```text
.council-runs/<timestamp>/
├── RUNBOOK.md
├── comparison.md
├── metadata.json
└── prompts/
```

Invoke installed local CLIs in parallel:

```bash
scripts/council-runner.sh \
  --question "Should this PR merge?" \
  --evidence README.md \
  --evidence council.md \
  --agents codex,claude,agy \
  --execute
```

Use `--execute` intentionally. It may consume model credits and depends on local
CLI authentication. If a tool is missing, omit it or use `--agents auto`.
Without `--execute`, `auto` stages prompt files for all four supported agent
perspectives even when no local CLIs are installed.

## Required Tools

No external CLI is required to read the protocol or use the examples manually.

For automated multi-agent runs, each agent you want to call must be installed
and authenticated locally. A full council does not require every supported tool.
Use whatever is available.

| Tool | Required for | Check |
| --- | --- | --- |
| Codex CLI | Codex review participant | `codex --version` |
| Claude Code | Claude participant or facilitator | `claude --version` |
| Gemini Antigravity | Gemini participant | `agy --version` |
| Grok CLI | Grok participant | `grok --version` |

Run:

```bash
scripts/check-prereqs.sh
```

This only checks whether commands are present. Authentication still depends on
each vendor's CLI.

The installer supports a safe preview and uninstall:

```bash
scripts/install-skill.sh --dry-run both
scripts/install-skill.sh --uninstall codex
```

## Practical Expectations

- **Best experience**: Codex plus at least one other agent is installed and logged in.
- **Good experience**: only Codex or only Claude is available; run separate passes with different perspectives.
- **Manual fallback**: copy prompts into web/app UIs.
- **Do not block** just because one optional CLI is unavailable.

## Safety

Start council reviews in read-only mode. Do not give external tools private
paths, secrets, customer data, patient data, internal hostnames, or confidential
incident notes unless the maintainer explicitly confirms the context is safe to
share.
