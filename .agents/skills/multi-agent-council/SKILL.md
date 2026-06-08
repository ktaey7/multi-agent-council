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

## Bias Controls

These keep a council from collapsing into one anchored opinion. Apply them
whenever you show one agent's output to another.

- **Codename anonymization**: relabel each agent's review with a neutral codename
  (Alpha, Bravo, Delta...) before showing it to another agent. Never reveal which
  model wrote it. Keep a private codename→model map; restore real names only in
  the final decision record's dissent section.
- **Hide the consensus ratio**: never say "most agents agree" or "three of four
  said yes." Share the content of other reviews, never the tally.
- **Rotate speaking order**: change which review is summarized first each round to
  spread anchoring.
- **PASS to converge**: an agent says `PASS` only with no new evidence, no changed
  position, and no blocking objection. Two or more PASS in a round means stop.

## Turnkey Execution

When the user asks for a council on a concrete question (or runs `/council`),
drive the whole run yourself and end with a decision record. Default to one
round; only debate when reviews diverge or the user asks.

1. **Gather evidence.** Read the named files/diffs directly. Summarize large
   secondary context. Pick distinct perspectives for the question.
2. **Round 1 — independent reviews.** Run the participants in parallel through
   the runner, which handles sandboxing and partial failures:

   ```bash
   scripts/council-runner.sh --execute \
     --question "<question>" \
     --evidence "<file-or-note>" [--evidence ...] \
     --agents auto
   ```

   Read each `outputs/<agent>.md` under the printed `.council-runs/<ts>/` dir.
3. **Anonymize.** Assign neutral codenames (Alpha, Bravo, Delta...) to the
   reviews. Keep your private codename→model map. Build the comparison table by
   codename; never state the consensus ratio.
4. **Decide if you need round 2.** If reviews converge with strong evidence or
   two or more effectively PASS, skip to synthesis. If they materially diverge,
   or the user passed `--debate`, run one cross-examination round.
5. **Round 2 — cross-examination (optional).** Write one prompt per agent into a
   temp dir as `<dir>/<agent>.md`. Each prompt shows that agent the OTHER
   reviews under codenames (rotate which is first), hides the consensus ratio,
   and asks: strongest opposing claim, weakest, does your judgment change, PASS
   if nothing new. Then execute them:

   ```bash
   scripts/council-runner.sh --execute --prompts-dir <dir> --agents <same-set>
   ```

   This creates a new `.council-runs/<ts>/` directory (it does not overwrite
   round 1). Read the round-2 replies from that new dir's `outputs/<agent>.md`,
   and synthesize from both rounds. Pass `--out <path>` if you want to choose
   where round 2 lands.

6. **Synthesize.** Produce the comparison table (codenames) and a
   maintainer-owned decision record. Restore real model names only in the
   dissent section.
7. **Degrade honestly.** If only one or two agents are available, or an agent
   fails mid-run (e.g., out of credits, timeout), continue with the rest and add
   a visible note: `⚠️ council reduced to N agents (reason)`.

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

### 3. Cross-Examine

Show each agent the other agents' Phase 2 reviews, anonymized by codename and with
the consensus ratio hidden. Rotate which review is presented first. Ask each agent
to name the strongest opposing claim, the weakest, and whether its judgment changes.
Stop when two or more agents answer `PASS`.

```text
Here are the other reviews, by codename. Some may be wrong.

[Alpha] ...
[Bravo] ...

Do not treat agreement as correctness. Return:
1. Strongest opposing claim and why (cite it).
2. Claim you challenge, with a concrete failure scenario.
3. Whether your judgment changes, and what changed it.
4. PASS only if you have nothing new.
```

### 4. Compare

Create a table:

| Reviewer | Core judgment | Strongest evidence | Main risk | Blocking objection |
| --- | --- | --- | --- | --- |

Then summarize:

- agreement
- disagreement
- assumptions
- missing evidence
- decision options

Do not treat majority agreement as correctness. Prefer the argument with the
strongest evidence and the clearest failure-mode analysis.

### 5. Run Counterfactual Round

Use this when the answer converges quickly or the decision is high impact:

```text
Assume the current consensus is wrong.

Provide:
1. Two realistic failure scenarios.
2. One piece of evidence that would support the opposite decision.
3. One constraint the council may have missed.
4. Whether your prior judgment changes.
```

### 6. Produce Decision Record

End with (map codenames back to real model names only in the dissent section):

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
