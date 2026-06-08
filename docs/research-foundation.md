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

## Bias Controls

Independence is fragile. The moment one agent sees another's answer, several
well-documented failure modes appear, and a naive multi-agent setup amplifies
them instead of cancelling them out. The protocol uses four explicit controls.

### Codename Anonymization

When a review is shown to another agent, it is relabeled with a neutral codename
rather than a model name. Two biases are suppressed at once: brand deference,
where a model treats a recognized name as more authoritative, and self-preference,
where a model over-trusts output it recognizes as its own. The maintainer keeps a
private codename→model map and restores real names only in the final dissent
section, where attribution helps the reader.

### Hiding the Consensus Ratio

Telling an agent that it is in the minority — "three of four already agree" —
manufactures conformity. The council shares the *content* of other reviews and
withholds the *tally*. A correct minority position should survive on evidence, not
be argued out of existence by a head count.

### Speaking-Order Rotation

Whichever review is read first anchors the ones that follow. Rotating the lead
across rounds spreads that anchor instead of letting one agent set the frame for
the whole debate.

### PASS as a Convergence Signal

Agents answer `PASS` only when they have no new evidence, no changed position, and
no blocking objection. When two or more PASS in a round, the council stops. This
gives convergence a concrete stopping rule and prevents agents from padding later
rounds with restated agreement.

## What This Is Not

- Not a model popularity contest.
- Not a voting system.
- Not a replacement for the maintainer.
- Not a guarantee of correctness.
- Not an excuse to send private data to every tool.

## Output

The final artifact should be a maintainer-owned decision record, not a transcript
dump. The transcript is evidence; the decision record is the maintainable result.
