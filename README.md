# Multi-Agent Council

Evidence-first review workflows for maintainers who use multiple coding agents.

Multi-Agent Council is a lightweight protocol for using Codex, Claude, Gemini,
Grok, and other coding agents as independent reviewers. It is designed for pull
request review, architecture decisions, security-sensitive changes, release
checks, and incident follow-up.

The goal is not to make agents vote. The goal is to reduce single-agent bias by
collecting independent analysis, requiring evidence, surfacing dissent, and
ending with a clear decision record.

## Why This Exists

Maintainers increasingly use coding agents for real project work, but most
agent workflows still have three failure modes:

- A single agent misses an edge case and sounds confident.
- Multiple agents produce long opinions without a decision structure.
- Review output cannot be reused as an issue, PR comment, or architecture note.

Multi-Agent Council turns those reviews into a repeatable maintainer workflow:

1. Define the question and evidence sources.
2. Ask each agent for an independent review from a distinct perspective.
3. Compare agreement, disagreement, assumptions, and blocking objections.
4. Run a dissent or counterfactual round when the answer looks too easy.
5. Publish a short decision record with risks and follow-up tasks.

## Core Principles

- **Equal Standing**: rank arguments by evidence, not by model or speaking order.
- **Constructive Dissent**: disagreement is useful when it names a concrete risk.
- **Evidence Required**: claims should point to code, docs, logs, tests, or data.
- **Pass When Empty**: if there is no new evidence, say `PASS` instead of adding noise.
- **Read-Only by Default**: council participants analyze before any tool changes state.

## Repository Contents

```text
council.md                 Protocol template
adapters/                  Tool-specific invocation notes
examples/                  Example council outputs
docs/                      Maintainer workflow and safety guidance
scripts/run-council.sh     Minimal local prompt runner scaffold
```

## Quick Start

Copy `council.md` into a maintainer note, replace the bracketed fields, and run
the first round with the agents you already use.

```bash
cp council.md /tmp/council-review.md
editor /tmp/council-review.md
```

For Codex-based review, start with:

```bash
codex "Review the task in /tmp/council-review.md. Follow the Multi-Agent Council principles. Return: 1. core judgment 2. evidence 3. impact 4. risks."
```

For local experimentation, the scaffold script prints a normalized prompt:

```bash
scripts/run-council.sh examples/pr-review.md
```

## Example Use Cases

- PR review before merging a risky change.
- Architecture decision review before adopting a new dependency.
- Security review for code that touches files, shell commands, secrets, or auth.
- Release readiness review for changelog, tests, docs, and migration notes.
- Incident follow-up where the team needs competing explanations.

## OpenAI Codex Fit

Codex is a first-class review participant in this protocol. The project is built
around maintainer workflows where Codex can help with:

- issue triage and reproduction planning
- pull request risk review
- security-sensitive change review
- release checklist generation
- documentation and test gap analysis
- decision-record drafting from review evidence

See [adapters/codex-cli.md](adapters/codex-cli.md) and
[docs/maintainer-workflows.md](docs/maintainer-workflows.md).

## Safety Model

Council runs should begin read-only. Participants should inspect code, docs,
logs, test output, and diffs before suggesting changes. Any command that writes
files, modifies infrastructure, posts messages, or calls an external service
should require explicit maintainer approval.

See [docs/safety-model.md](docs/safety-model.md).

## Status

This repository is an early public release of a workflow that started as a local
maintainer practice. The current focus is documentation, examples, adapter
templates, and real-world review transcripts that other maintainers can reuse.

## License

MIT License. See [LICENSE](LICENSE).
