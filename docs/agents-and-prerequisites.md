# Agents and Prerequisites

Multi-Agent Council supports several coding agents, but they are optional
participants. The protocol is useful even when only one or two agents are
available.

## Availability Matrix

| Agent | Role | Required? | Notes |
| --- | --- | --- | --- |
| Codex | code review, issue triage, test gaps, release checks | Recommended | First-class OpenAI participant |
| Claude Code | facilitator, context synthesis, decision record | Optional | Useful when already working in Claude Code |
| Gemini Antigravity (`agy`) | broad alternate analysis | Optional | Use summaries when file access is unsafe |
| Grok CLI | counterfactual and web-aware critique | Optional | Keep web research separate from private repo data |

## Authentication

Each CLI has its own authentication model. Installing this skill does not log in
to any provider.

Before expecting automated calls, confirm the tool works by running a small
non-sensitive prompt in that tool.

Examples:

```bash
codex "Say ready"
claude --version
agy --print "Say ready"
grok -p "Say ready"
```

If a tool fails, keep the council running with the remaining tools or switch to
manual copy/paste.

## Minimum Useful Modes

### Full Council

Use Codex, Claude, Gemini, and Grok as independent reviewers. Best for high-risk
architecture, security, or release decisions.

### Two-Agent Council

Use Codex plus one other agent. Assign different perspectives, such as:

- Codex: implementation and tests
- Other agent: counterfactual or security review

### Single-Agent Council

Use one agent in separate passes:

1. Implementation pass.
2. Security pass.
3. Maintainer experience pass.
4. Counterfactual pass.

This is weaker than independent agents but still better than a single generic
answer.

## File Access Policy

Do not give every tool the same file access by default.

- Give direct file paths only to tools you trust in the current environment.
- Use summaries for tools with broad permissions or unclear sandboxing.
- Redact secrets, private user data, patient data, internal hostnames, and
  confidential incident details.
- Keep the final decision record free of private operational details.
