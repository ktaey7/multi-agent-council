---
name: multi-agent-council
description: Use when the user wants a structured multi-agent review for pull requests, issue triage, architecture decisions, security-sensitive changes, release readiness, incident follow-up, or any decision where Codex, Claude, Gemini, Grok, or other coding agents should provide independent evidence-based analysis before a maintainer decides.
---

# Multi-Agent Council

Run an evidence-first council review using the agents available in the user's
environment. The council analyzes; the maintainer decides.

## Core Rules

- **Equal Standing**: evaluate arguments by evidence, not by model name.
- **Constructive Dissent**: ask for concrete objections and failure scenarios.
- **Evidence Required**: require file paths, diffs, logs, tests, docs, or direct observations.
- **Pass When Empty**: if no new evidence exists, use `PASS` instead of filler.
- **Read-Only First**: begin with analysis only; writes require explicit user approval.

## Agent Availability

Do not assume every CLI is installed or authenticated.

1. Check available agents before planning:
   - Codex: `codex --version`
   - Claude Code: `claude --version`
   - Gemini Antigravity: `agy --version`
   - Grok: `grok --version`
2. If a CLI is missing or not logged in, continue with the remaining agents.
3. A full four-agent council is optional. A useful council can run with:
   - one agent plus a counterfactual round,
   - two agents with different perspectives,
   - or manual copy/paste prompts into web/app UIs.
4. Never send private data, secrets, customer data, patient data, or internal incident notes to third-party tools unless the user explicitly confirms it is safe.

## Workflow

### 1. Prepare Context

- Identify the exact question.
- List evidence sources: files, diffs, issues, logs, tests, docs.
- Read the core evidence directly.
- Summarize large secondary context instead of sending everything.
- Assign distinct perspectives, such as security, implementation risk, tests, contributor experience, user impact, or release risk.

### 2. Collect Independent Reviews

Use this prompt shape for each participant:

```text
You are one reviewer in a Multi-Agent Council.

Question:
[question]

Evidence sources:
[files, diffs, logs, tests, docs, or summaries]

Your assigned perspective:
[perspective]

Rules:
- Equal Standing
- Constructive Dissent
- Evidence Required
- Pass When Empty
- Read-only analysis only

Return:
1. Core judgment
2. Evidence, with labels: empirical, mechanistic, strategic, ethical, or heuristic
3. Implementation impact
4. Risks and failure scenarios
5. Open questions
```

If the repository has the Multi-Agent Council scripts available, the maintainer
can stage or run prompts with:

```bash
scripts/council-runner.sh --question "[question]" --evidence "[file-or-diff]"
scripts/council-runner.sh --question "[question]" --evidence "[file-or-diff]" --execute
```

Use `--execute` only when the user wants local CLIs invoked. It may consume model
credits and depends on each CLI's authentication.

### 3. Compare

Create a table:

| Reviewer | Core judgment | Strongest evidence | Main risk | Blocking objection |
| --- | --- | --- | --- | --- |

Then summarize:

- agreement
- disagreement
- assumptions
- missing evidence
- decision options

### 4. Run Counterfactual Round

Use this when the answer converges quickly or the decision is high impact:

```text
Assume the current consensus is wrong.

Provide:
1. Two realistic failure scenarios.
2. One piece of evidence that would support the opposite decision.
3. One constraint the council may have missed.
4. Whether your prior judgment changes.
```

### 5. Produce Decision Record

End with:

```markdown
# Decision Record: [Title]

## Decision
[What will be done.]

## Why
[Evidence-backed rationale.]

## Alternatives Considered
[Rejected options and why.]

## Risks
[Known risks and mitigations.]

## Follow-Up
- [ ] [Task]
```

## Invocation Notes

- Prefer Codex for code review, issue triage, release checks, and test gap analysis.
- Prefer Claude Code for facilitation, context synthesis, and decision records.
- Prefer Gemini or Grok for alternate perspectives and counterfactual analysis when available.
- If a CLI has unsafe or broad permissions, do not pass file paths directly; pass a maintainer-written summary instead.

## When Blocked

If no external agents are available, run a single-agent council by forcing separate passes:

1. First pass: implementation review.
2. Second pass: security review.
3. Third pass: counterfactual review.
4. Final pass: decision record.
