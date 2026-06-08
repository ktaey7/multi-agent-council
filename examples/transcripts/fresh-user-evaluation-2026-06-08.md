# Fresh-User Evaluation Transcript

Date: 2026-06-08

A reviewer with no prior knowledge of this repository cloned it fresh, followed
only its own docs, installed it (into a sandbox to avoid clobbering an existing
local command), and ran a real four-agent council **on this repository itself**.
The council's decision record flagged concrete bugs in the runner; those findings
were then fixed in v0.3.1. This is included as honest dogfooding evidence: the
tool was used to review its own code, and it found real problems.

## Setup

- Clean `git clone` into a scratch directory. No build step, no dependencies.
- `scripts/check-prereqs.sh` reported 4/4 CLIs present (`codex`, `claude`, `agy`,
  `grok`), each annotated `(auth not checked)`.
- `scripts/install-skill.sh claude` (redirected via the documented
  `CLAUDE_SKILLS_DIR` / `CLAUDE_COMMANDS_DIR` overrides) installed the skill and
  the `/council` command exactly as documented.

## Question

> Is this repo's install + runner actually usable for a new maintainer, and does
> it handle missing/failed agent CLIs gracefully?

Evidence: `README.md`, `scripts/council-runner.py`.

## Execution

```bash
scripts/council-runner.sh --execute \
  --question "<question above>" \
  --evidence README.md --evidence scripts/council-runner.py \
  --agents auto --timeout 240
```

**4/4 agents produced a usable review.** The runner wrote per-agent output files,
a comparison scaffold, a runbook, and `metadata.json` with per-agent status and
timing. No crash. Codenames below: Alpha = Claude, Bravo = Codex, Delta = agy,
Echo = Grok.

## Comparison (anonymized)

| Reviewer | Core judgment | Main risk |
| --- | --- | --- |
| Alpha | Usable, with two sharp edges | Council collapse reported as success |
| Bravo | Partially usable; turnkey-vs-reality gap | Auth failure indistinguishable from model failure |
| Delta | Conceptually strong, pragmatically brittle | Large prompts exceed agy's argv-only interface |
| Echo | Not reliably usable without all CLIs pre-configured | No execution-path tests to back the degradation claim |

All four converged that the prompt-staging, install script, and templates are
solid, and that the runner's auto-mode could mislead a user about how many agents
actually ran.

## Decision Record (as produced by the run)

### Decision

Adopt the protocol and manual facilitation now; adopt the `--execute` runner once
the honesty and robustness gaps are fixed.

### Why

The install script and protocol docs are above the bar for an early release, and
the runner already isolates per-agent failures without crashing. But auto-mode
reported `Executed 1/1 agents successfully` while silently dropping uninstalled
CLIs — directly undercutting the project's own value claim — and the execution
path had no test coverage.

### Dissent (real names)

- **Grok** (Echo) was harshest: not reliably usable without all four CLIs.
- **Claude** (Alpha) was more charitable: the foundation is solid for an early release.

### Follow-Up (all addressed in v0.3.1)

- [x] Report skipped CLIs and a truthful run summary instead of `Executed 1/1 successfully`.
- [x] Add execution-path tests (`run_agent` success/failure/timeout/OSError, agent selection).
- [x] Stop appending stderr session logs to successful output files.
- [x] Clearer message when a prompt exceeds agy's argv-only interface.
- [x] Lower the default timeout from 900s to 300s.
- [x] Fix the README "falls back to the manual protocol" claim to match actual behavior.

## Honest Verdict (reviewer's own words)

- Idea / methodology: **8/10** — the diagnosed failure modes and bias controls are real and specific.
- Current usability (at time of evaluation): **5/10** — strong install, clear protocol, but honesty/robustness gaps in the runner.

The single highest-leverage fix the reviewer named — honest auto-mode reporting —
was implemented as the headline change of v0.3.1.

## Note

No private paths, secrets, or customer data appear in this transcript.
