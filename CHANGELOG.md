# Changelog

## 0.3.1 - 2026-06-08

- **Honest auto-mode reporting**: `--execute --agents auto` now lists skipped CLIs and prints a truthful `X ok / Y failed of N run; M skipped` summary instead of a misleading `Executed 1/1 agents successfully`. Records `configured`/`skipped` in metadata and warns on single-agent runs.
- **Cleaner output files**: agent stderr (e.g. Codex session logs) is appended only on failure or empty output, so successful reviews are no longer bloated.
- Clearer message when a prompt is too large for `agy`'s argv-only interface; lowered the default `--timeout` from 900s to 300s.
- Added **execution-path tests** (`run_agent` success/failure/timeout/OSError, agent selection) and a **GitHub Actions CI** workflow (pytest, shell syntax, dry-run install, prereq check).
- Fixed the README "falls back to the manual protocol" claim to match actual behavior; added a fresh-user evaluation transcript where the tool reviewed its own code and surfaced these fixes.

## 0.3.0 - 2026-06-08

- Added a **turnkey `/council` flow**: the coding agent drives a full council from one command — gather evidence, run participants in parallel, anonymize, debate on divergence, and synthesize a decision record.
- Added a `/council` slash command for Claude Code (`commands/council.md`); the installer now also installs it to `~/.claude/commands/`.
- Added a `--prompts-dir` mode to `council-runner.py` so the driver can execute round-2 cross-examination prompts in parallel.
- Added `tests/test_council_runner.py` covering the new runner behavior.

## 0.2.0 - 2026-06-08

- Added explicit **bias controls** to the protocol: codename anonymization, hiding the consensus ratio, speaking-order rotation, and `PASS` as the convergence signal.
- Added a **Cross-Examination** phase so agents debate each other's anonymized reviews instead of producing parallel monologues.
- Documented the rationale for each bias control in `docs/research-foundation.md`.
- Updated `council.md`, the skill `SKILL.md`, and the README to reflect the cross-examination step and bias controls.
- Added a real four-agent execution transcript (Codex, Claude, Gemini, Grok) under `examples/transcripts/`.
- Moved OpenAI Codex OSS application notes out of the repository to keep it positioned as a protocol, not an application artifact.

- Added `scripts/council-runner.py` and `scripts/council-runner.sh` for prompt staging and optional parallel local CLI execution.
- Added real local runner execution transcript using Claude CLI.
- Improved prerequisite checker with `--strict`, summary counts, stdin-closed version checks, and auth caveats.
- Moved prerequisite detection into `council-runner.py`; `check-prereqs.sh` is now a wrapper.
- Added Python executable fallback in `check-prereqs.sh` and captured stderr during version checks.
- Made prompt-only `--agents auto` stage all supported agent prompts, even on machines without local agent CLIs.
- Reframed the project around multi-agent cross-validation and debate.
- Moved the skill package to Codex's repo-scoped `.agents/skills` layout.
- Corrected Codex user install target to `$HOME/.agents/skills`.
- Added dry-run and uninstall support to the installer.
- Added prompt-printing script and kept `run-council.sh` as a compatibility wrapper.
- Added a real self-review transcript from Claude, Gemini, Grok, and Codex perspectives.
- Added installable `multi-agent-council` skill package.
- Added Codex and Claude Code skill installation script.
- Added optional local CLI prerequisite checker.
- Added installation and agent prerequisite documentation.

## 0.1.0 - 2026-06-08

- Initial public protocol draft.
- Added Codex, Claude Code, Gemini, and Grok adapter notes.
- Added PR review, architecture decision, and security review examples.
- Added maintainer workflow and safety model documentation.
