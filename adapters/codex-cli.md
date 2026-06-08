# Codex CLI Adapter

Use Codex as a first-class participant for code review, issue triage,
architecture evaluation, and release readiness checks.

## Basic Review Prompt

```bash
codex "Read council.md and review the referenced diff. Focus on security and maintainability. Return core judgment, evidence, impact, risks, and open questions."
```

## Pull Request Review

```bash
codex "Review this PR using the Multi-Agent Council format. Evidence sources: git diff origin/main...HEAD, README.md, tests. Perspective: implementation risk and missing tests."
```

## Issue Triage

```bash
codex "Triage this issue using the Multi-Agent Council format. Identify likely root causes, reproduction steps, affected files, and whether this should block the next release."
```

## Security-Sensitive Change

```bash
codex "Review this change as security-sensitive. Focus on file writes, shell execution, auth, secrets, network calls, and trust boundaries. Do not edit files. Return blocking objections first."
```

## Recommended Defaults

- Start with read-only analysis.
- Ask Codex to cite file paths, tests, docs, or observed output.
- Separate findings from proposed patches.
- Run a counterfactual round for high-risk merges.
- Keep the maintainer as the final decision maker.
