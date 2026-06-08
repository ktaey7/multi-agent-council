# Installation

Multi-Agent Council is primarily a skill/protocol package. It can be used in
three ways:

1. Install as a Codex or Claude skill.
2. Clone and run prompts manually.
3. Copy prompts into web or app-based AI tools.

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
skills/multi-agent-council/
```

to one or both of:

```text
~/.codex/skills/multi-agent-council/
~/.claude/skills/multi-agent-council/
```

Restart the target app or start a new session if it does not pick up the skill
immediately.

## Manual Use

You can use the protocol without installing a skill:

```bash
scripts/run-council.sh examples/pr-review.md
```

Then paste the generated prompt into Codex, Claude, Gemini, Grok, or another
review tool.

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
