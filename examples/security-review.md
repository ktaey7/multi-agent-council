# Example: Security Review

## Question

Is it safe to add remote chat control to a coding-agent tool?

## Evidence Sources

- bot command handlers
- auth configuration
- file operation code
- shell execution code
- deployment guide

## Required Review Questions

- Who is allowed to issue commands?
- Can the bot read files outside the intended workspace?
- Can the bot write or delete files?
- Are shell commands allowed?
- Are tokens stored safely?
- Is there an audit trail?
- Can maintainers disable the bot quickly?

## Decision Pattern

Remote control is acceptable only with:

- explicit allowlist
- read-only default
- approval for writes and shell execution
- scoped workspace
- audit log
- documented emergency shutdown
