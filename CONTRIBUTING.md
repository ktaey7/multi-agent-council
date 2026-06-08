# Contributing

Contributions are welcome, especially:

- real maintainer workflows
- council examples with private data removed
- adapter notes for coding agents
- safety improvements
- issue triage and PR review templates

## Guidelines

- Do not include secrets, tokens, customer data, patient data, or private logs.
- Keep examples evidence-based and reusable.
- Prefer small changes with clear motivation.
- Add or update examples when changing the protocol.

## Development

This repository is mostly Markdown. Run these checks before a PR:

```bash
scripts/print-council-prompt.sh examples/pr-review.md
scripts/install-skill.sh --dry-run both
```
