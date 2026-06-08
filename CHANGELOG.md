# Changelog

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
