# Multi-Agent Council Protocol

Use this template when a maintainer wants multiple agents to cross-check and
debate a decision before a merge, release, architecture change, security review,
or incident conclusion.

The core idea is model diversity. Each agent may notice different constraints,
make different mistakes, and reason from different tool behavior. The council
keeps those differences useful by separating independent review from later
comparison and counterfactual debate.

## Task

**Question:** [Write the decision or review question.]

**Repository or project:** [Name and URL/path.]

**Evidence sources:**

- [File, diff, issue, PR, log, test output, doc, or dataset.]
- [File, diff, issue, PR, log, test output, doc, or dataset.]

**Decision needed by:** [Date or milestone.]

## Council Principles

- **Equal Standing**: all analyses are evaluated by evidence, not by model name.
- **Constructive Dissent**: challenge assumptions with specific evidence.
- **Attack Ideas, Not Agents**: critique claims, not the participant.
- **Evidence Required**: cite code, docs, logs, tests, data, or direct observation.
- **Pass When Empty**: answer `PASS` only when there is no new evidence, no changed
  position, and no blocking objection.

## Bias Controls

A council is only useful if the agents stay independent. These four controls
exist to stop the most common ways multi-agent review collapses back into a
single anchored opinion. They are the difference between a council and a prompt
pack.

- **Codename anonymization**: when an agent's review is shown to another agent,
  label it with a neutral codename (Alpha, Bravo, Delta...), never the model
  name. Models defer to brands they recognize and over-trust their own prior
  output. Strip both signals. The maintainer keeps a private codename→model map
  and only restores real names in the final record's dissent section.
- **Hide the consensus ratio**: never tell an agent "three of four already agree"
  or "this is the majority view." Stated agreement counts manufacture conformity.
  Show the *content* of other reviews, never the *score*.
- **Rotate speaking order**: change which agent is summarized first in each round.
  Whoever is read first anchors the rest. Rotating the lead spreads that anchor.
- **PASS to converge**: an agent answers `PASS` only when it has no new evidence,
  no changed position, and no blocking objection. When two or more agents PASS in
  a round, treat it as real convergence and stop. PASS is how the council ends
  without padding.

## Phase 0: Context Preparation

The maintainer prepares the context before calling agents.

1. Convert all paths and URLs into unambiguous references.
2. Read the core files directly.
3. Summarize secondary files instead of sending unbounded context.
4. Assign distinct review perspectives.

Suggested perspectives:

- feasibility and implementation complexity
- security and trust boundary
- maintainability and contributor experience
- edge cases and failure scenarios
- user impact and migration risk
- test strategy and observability

## Phase 1: Independent Reviews

Each participant answers independently before seeing other reviews.

Do not share other agents' answers in this phase. The point is to preserve
independent judgment before synthesis.

Prompt template:

```text
You are one reviewer in a Multi-Agent Council.

Question:
[question]

Evidence sources:
[sources]

Your assigned perspective:
[perspective]

Principles:
- Equal Standing
- Constructive Dissent
- Evidence Required
- Pass When Empty

Return this structure:
1. Core judgment
2. Evidence, with at least two labeled items:
   - empirical: observed behavior, logs, tests, usage, data
   - mechanistic: how code or systems work
   - strategic: maintainer, ecosystem, or roadmap impact
   - ethical: safety, privacy, fairness, trust
   - heuristic: experience-based rule of thumb
3. Implementation impact
4. Risks and failure scenarios
5. Open questions
```

## Phase 2: Cross-Examination

This is the debate. Skip it and you only have parallel monologues.

Show each agent the *other* reviews from Phase 1 — anonymized by codename, with
the consensus ratio hidden (see Bias Controls). Rotate which review is presented
first. Then ask each agent to respond.

Prompt template:

```text
Here are the other reviewers' independent analyses, by codename.
They may contain errors or flawed reasoning. Some may be wrong.

[Alpha review]
[Bravo review]
[Delta review]

Do not assume agreement is correctness. Evaluate each claim on its evidence.

Return:
1. Which specific claim from another reviewer is strongest, and why (cite it).
2. Which specific claim you challenge, with a concrete failure scenario or
   missing evidence.
3. Whether your Phase 1 judgment changes, and exactly what changed it.
4. PASS only if you have no new evidence, no changed position, and no blocking
   objection.
```

Run at most one or two cross-examination rounds. When two or more agents PASS,
stop — that is convergence, not fatigue. Carry only the raw text of the latest
round plus a short running summary into the next round; do not re-feed the entire
history.

## Phase 3: Comparison

The maintainer creates a comparison table.

| Reviewer | Core judgment | Strongest evidence | Main risk | Blocking objection |
| --- | --- | --- | --- | --- |
| A |  |  |  |  |
| B |  |  |  |  |
| C |  |  |  |  |
| D |  |  |  |  |

Then summarize:

- agreement
- disagreement
- assumptions
- missing evidence
- decision options

Do not treat majority agreement as correctness. Prefer the argument with the
strongest evidence and the clearest failure-mode analysis.

## Phase 4: Dissent or Counterfactual Round

Run this when reviews converge too quickly or a decision is high impact.

Prompt template:

```text
Assume the current consensus is wrong.

Provide:
1. Two realistic failure scenarios.
2. One piece of evidence that would support the opposite decision.
3. One constraint the council may have missed.
4. Whether your prior judgment changes.
```

## Phase 5: Decision Record

End with a short maintainer-owned record. This is the one place codenames are
mapped back to real model names, and only in the dissent section, so a reader can
see which agent held which position.

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
- [ ] [Task]
```

## Operating Rule

The council analyzes. The maintainer decides.
