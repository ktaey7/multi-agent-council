# OpenAI Codex OSS Application Notes

This file keeps the repository positioning aligned with the OpenAI Codex OSS
support program.

## Project Role

Maintainer and original author of the Multi-Agent Council protocol. The project
started as a local maintainer workflow for structured AI review and is now being
released as a model-agnostic open-source protocol with Codex as a first-class
review participant.

## Why This Project Fits

Multi-Agent Council helps maintainers use Codex and other coding agents for
evidence-based review instead of one-off chat. It targets real open-source
maintenance tasks: PR review, issue triage, architecture decisions,
security-sensitive change review, release readiness, and decision records. The
project focuses on reducing single-agent bias, making dissent explicit, and
turning AI output into reusable maintainer artifacts.

The repository is packaged as an installable skill for Codex and Claude Code,
with manual fallback prompts for users who prefer app or web interfaces.

The project includes a self-review transcript generated from multiple agent
perspectives: `examples/transcripts/self-review-2026-06-08.md`.

## API Credit Plan

OpenAI API credits would be used to build and test maintainer workflows around
Codex-assisted review: PR risk summaries, issue triage prompts, release
checklist generation, security-sensitive change review, and structured decision
record drafting. The goal is to publish reusable templates and examples that
help small open-source maintainers adopt safer, evidence-based agent workflows.

## Optional Additional Note

This project is intentionally small and documentation-first. Its value is in the
review protocol, safety model, and reusable examples rather than a heavy runtime.
The next milestone is to collect real-world review transcripts and add adapters
for common coding-agent tools while keeping private data out of examples.

## Pre-Submission Checklist

- [x] Public GitHub repository
- [x] README explains problem, solution, and Codex fit
- [x] LICENSE included
- [x] Safety model included
- [x] Codex adapter included
- [x] Installable skill package included
- [x] CLI prerequisites documented
- [x] Maintainer workflow examples included
- [x] First release tag created
- [x] Roadmap issues created
- [x] Self-review transcript included
- [ ] No private paths, secrets, customer data, or internal incident notes
