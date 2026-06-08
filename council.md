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

## Phase 2: Comparison

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

## Phase 3: Dissent or Counterfactual Round

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

## Phase 4: Decision Record

End with a short maintainer-owned record.

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
