# Self-Review Transcript: Is This Project Immediately Useful?

Date: 2026-06-08

Question:

> Is `multi-agent-council` immediately useful for other maintainers as an
> installable multi-agent council skill/protocol, and what must improve before
> it is convincing as an OpenAI Codex OSS application?

Evidence inspected:

- `README.md`
- `.agents/skills/multi-agent-council/SKILL.md`
- `docs/installation.md`
- `docs/agents-and-prerequisites.md`
- `council.md`
- `examples/`
- `scripts/`

## Reviewer Perspectives

| Reviewer | Perspective |
| --- | --- |
| Codex | Product usefulness and Codex OSS readiness |
| Claude | User adoption and installability |
| Gemini via `agy` | Conceptual strength and differentiation |
| Grok | Skeptical OSS maintainer review |

## Independent Review Summary

| Reviewer | Core judgment | Strongest evidence | Main risk | Blocking objection |
| --- | --- | --- | --- | --- |
| Codex | Useful as a protocol, not yet compelling as a turnkey project | Repo has clear workflow docs and skill packaging, but no real execution proof | Users may see it as a prompt collection | Needs real transcript and verified install path |
| Claude | Conditionally useful, not yet convincing | Install path and docs are clear, but examples are synthetic | Codex install path was unverified | Verify Codex skill discovery and add real transcript |
| Gemini via `agy` | Conceptually strong but not automated | Phases and principles show clear debate methodology; scripts do not orchestrate agents | High manual friction | Needs programmatic orchestrator or honest prompt-pack positioning |
| Grok | Not immediately useful as turnkey installable software | Installer copies a Markdown skill; `run-council.sh` only prints prompts | Expectation mismatch for skeptical maintainers | Needs self-contained runnable example and tighter Codex story |

## Agreement

- The core thesis is strong: different agents have different blind spots, so
  independent review plus structured dissent can reduce single-agent bias.
- The current project is strongest as a protocol and skill package.
- The project is not yet a turnkey multi-agent orchestrator.
- The original install path for Codex needed correction to Codex's `.agents/skills`
  convention.
- Real transcripts matter more than more synthetic examples.

## Disagreement

- How much automation is required before the project is useful:
  - Claude considered it useful as a manual protocol once install is verified.
  - Grok judged it not immediately useful for skeptical maintainers because it
    still requires manual facilitation.
- Whether the project should build an orchestrator now:
  - Gemini and Grok favored runtime glue.
  - Codex prioritized clearer positioning, install verification, and real
    transcripts first.

## Counterfactual

Assume the positive conclusion is wrong and the project is useful enough today.

The strongest defense is that many skills are intentionally instruction-first.
For a maintainer already using Codex or Claude Code, installing a concise,
well-scoped skill may be enough to standardize review behavior without a new
runtime.

Assume the negative conclusion is wrong and the project is not worth shipping.

The strongest critique is that the project advertises cross-agent review but
does not yet run cross-agent review. If users expect automation, the current
implementation disappoints.

## Decision Record

### Decision

Keep the project as a skill/protocol package, but reposition it explicitly as a
cross-validation and debate protocol. Do not imply that it currently orchestrates
agents automatically.

### Why

The strongest evidence across reviewers was that the protocol is coherent and
the skill packaging is useful, but the project lacks real transcripts and runtime
automation. The next increment should make the current scope honest and
verifiable before adding more automation.

### Follow-Up

- [x] Move Codex skill package to `.agents/skills`.
- [x] Correct Codex user install target to `$HOME/.agents/skills`.
- [x] Add this self-review transcript.
- [ ] Add a self-contained runnable council example against files in this repo.
- [ ] Add optional orchestrator script that can call available CLIs and collect outputs.
- [ ] Add CI check for scripts and Markdown links.
