# Research Foundation

Multi-Agent Council is based on a practical observation: different AI coding
agents are not interchangeable. They vary in tool behavior, context handling,
review style, sensitivity to risk, and failure modes.

The protocol uses that variation as a feature.

## Core Thesis

A maintainer should not ask several agents for the same generic opinion and then
average the answers. A useful council preserves independent judgment first,
then compares claims by evidence quality.

## Design Principles

### Independence Before Synthesis

Agents should provide first-pass reviews before seeing other reviews. This
reduces anchoring on the first confident answer.

### Perspective Assignment

Each reviewer gets a distinct lens, such as:

- implementation correctness
- security and trust boundary
- user impact
- contributor experience
- release risk
- counterfactual critique

The goal is not roleplay. The goal is search coverage.

### Evidence Weighting

Claims should cite code, diffs, docs, logs, tests, or direct observations. A
minority objection with concrete evidence can outweigh majority agreement.

### Constructive Dissent

Disagreement must name a failure scenario, missing constraint, or blocking
objection. Empty contrarianism is noise.

### Counterfactual Round

When the council converges too easily, ask reviewers to assume the consensus is
wrong. This often exposes hidden assumptions.

## What This Is Not

- Not a model popularity contest.
- Not a voting system.
- Not a replacement for the maintainer.
- Not a guarantee of correctness.
- Not an excuse to send private data to every tool.

## Output

The final artifact should be a maintainer-owned decision record, not a transcript
dump. The transcript is evidence; the decision record is the maintainable result.
