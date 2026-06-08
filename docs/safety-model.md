# Safety Model

Multi-Agent Council is an analysis workflow. It should not grant agents broad
write access by default.

## Default Boundary

Start every council run as read-only:

- read files
- inspect diffs
- inspect logs
- inspect test output
- read public docs
- summarize evidence

Require maintainer approval before:

- editing files
- deleting files
- running destructive commands
- posting comments or messages
- changing repository settings
- changing infrastructure
- calling external services with private data

## Sensitive Context

Do not send the following to public examples or third-party tools:

- tokens, passwords, API keys, and private keys
- customer or patient data
- private incident records
- private company contracts
- internal hostnames or deployment secrets
- confidential logs

## Review Priority

For security-sensitive changes, ask reviewers to report in this order:

1. Blocking issues.
2. Trust boundary changes.
3. Data exposure risks.
4. Missing tests.
5. Safer alternatives.

## Human Decision Rule

The council provides structured evidence. The maintainer decides what ships.
