# Multi-Agent Council

Cross-validation and debate workflows for maintainers who use multiple coding
agents.

Multi-Agent Council is a lightweight protocol for making Codex, Claude, Gemini,
Grok, and other coding agents challenge each other before a maintainer decides.
It is designed for pull request review, architecture decisions,
security-sensitive changes, release checks, and incident follow-up.

The goal is not to make agents vote. The goal is to reduce single-agent bias by
using model diversity: independent reviews, explicit dissent, counterfactual
rounds, and evidence-weighted synthesis.

## Why This Exists

Different agents have different strengths, blind spots, context handling, tool
behavior, and failure modes. A single confident answer is often less useful than
several independent reviews that disagree for clear reasons.

Maintainers increasingly use coding agents for real project work, but most
agent workflows still have four failure modes:

- A single agent misses an edge case and sounds confident.
- Multiple agents produce long opinions without a decision structure.
- Later reviewers anchor on the first answer instead of independently checking.
- Review output cannot be reused as an issue, PR comment, or architecture note.

Multi-Agent Council turns those reviews into a repeatable maintainer workflow:

1. Define the question and evidence sources.
2. Ask each agent for an independent review from a distinct perspective.
3. Cross-examine: show each agent the others' reviews — anonymized by codename, with the consensus ratio hidden — and ask what they challenge.
4. Compare agreement, disagreement, assumptions, and blocking objections by evidence quality.
5. Run a dissent or counterfactual round when the answer converges too quickly.
6. Publish a short decision record with risks and follow-up tasks.

## Core Principles

- **Equal Standing**: rank arguments by evidence, not by model or speaking order.
- **Constructive Dissent**: disagreement is useful when it names a concrete risk.
- **Evidence Required**: claims should point to code, docs, logs, tests, or data.
- **Pass When Empty**: if there is no new evidence, say `PASS` instead of adding noise.
- **Read-Only by Default**: council participants analyze before any tool changes state.

To keep agents from collapsing back into a single anchored opinion, the protocol
adds four **bias controls**: codename anonymization, hiding the consensus ratio,
rotating speaking order, and using `PASS` as the convergence signal. See
[docs/research-foundation.md](docs/research-foundation.md#bias-controls).

## Repository Contents

```text
council.md                 Protocol template
.agents/skills/            Repo-scoped Codex skill package
adapters/                  Tool-specific invocation notes
examples/                  Example council outputs
docs/                      Maintainer workflow and safety guidance
scripts/print-council-prompt.sh  Print a copy/paste council prompt
scripts/council-runner.py  Orchestration logic: stage prompts, optionally run local CLIs, collect outputs
scripts/council-runner.sh  Wrapper that runs council-runner.py with the system Python
scripts/run-council.sh     Backward-compatible wrapper for prompt printing
scripts/install-skill.sh   Install the skill into Codex or Claude Code
scripts/check-prereqs.sh   Check optional local agent CLIs
```

## Quick Start

Install as a Codex skill:

```bash
git clone https://github.com/ktaey7/multi-agent-council.git
cd multi-agent-council
scripts/install-skill.sh codex
```

Codex also detects the repo-scoped skill directly from `.agents/skills/` when
you work inside this repository. Use `/skills` or mention
`$multi-agent-council` in Codex.

Install as a Claude Code skill:

```bash
scripts/install-skill.sh claude
```

Check optional local agent CLIs:

```bash
scripts/check-prereqs.sh
```

See [docs/installation.md](docs/installation.md) and
[docs/agents-and-prerequisites.md](docs/agents-and-prerequisites.md).

## Manual Quick Start

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
scripts/print-council-prompt.sh examples/pr-review.md
```

To stage a real council run with per-agent prompt files and a comparison
template:

```bash
scripts/council-runner.sh \
  --question "Should this PR merge?" \
  --evidence README.md \
  --evidence council.md
```

To invoke installed local CLIs in parallel, add `--execute`:

```bash
scripts/council-runner.sh \
  --question "Should this PR merge?" \
  --evidence README.md \
  --evidence council.md \
  --agents codex,claude,agy \
  --execute
```

Runner outputs are written under `.council-runs/<timestamp>/` by default. The
directory includes prompt files, raw outputs, metadata, a runbook, and a
comparison template.

Without `--execute`, the default `--agents auto` stages prompts for all four
agent perspectives. With `--execute`, `auto` only invokes CLIs found on the
local machine.

See a real self-review transcript:
[examples/transcripts/self-review-2026-06-08.md](examples/transcripts/self-review-2026-06-08.md).

See a real four-agent execution transcript, where two agents converged and two
failed for environment reasons the runner captured:
[examples/transcripts/four-agent-orchestrator-decision-2026-06-08.md](examples/transcripts/four-agent-orchestrator-decision-2026-06-08.md).

See a real local runner execution transcript:
[examples/transcripts/council-runner-claude-test-2026-06-08.md](examples/transcripts/council-runner-claude-test-2026-06-08.md).

## Example Use Cases

- PR review before merging a risky change.
- Architecture decision review before adopting a new dependency.
- Security review for code that touches files, shell commands, secrets, or auth.
- Release readiness review for changelog, tests, docs, and migration notes.
- Incident follow-up where the team needs competing explanations.

## Design Foundation

The project is built around multi-agent cross-validation, not agent voting. Read
[docs/research-foundation.md](docs/research-foundation.md) for the design
principles behind independence, perspective assignment, evidence weighting, and
counterfactual review.

## Do I Need Every CLI?

No. Codex, Claude Code, Gemini Antigravity, and Grok are optional participants.
For automated multi-agent runs, each CLI you want to call must be installed and
authenticated in your local environment. If a tool is missing, keep going with
the remaining tools or copy prompts into web/app UIs.

Useful modes:

- **Full council**: Codex, Claude, Gemini, and Grok.
- **Two-agent council**: Codex plus one other agent.
- **Single-agent council**: run separate implementation, security, maintainer
  experience, and counterfactual passes.

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
templates, real-world review transcripts, and lightweight runtime glue that
other maintainers can reuse.

## License

MIT License. See [LICENSE](LICENSE).
