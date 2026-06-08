# Four-Agent Council Transcript: Orchestrator vs. Protocol

Date: 2026-06-08

This is a real, redacted run of `scripts/council-runner.py --execute` against this
repository. It is included as honest evidence: two agents produced full reviews
and converged, and two failed for environment reasons that the runner captured
without crashing the run. The failures are kept in the record on purpose — a
council protocol has to be honest about partial participation.

Codenames are used in the comparison to demonstrate the protocol's codename
anonymization bias control. Real model names are restored only in the decision
record's dissent section.

## Question

> Should `multi-agent-council` ship a programmatic orchestrator that auto-runs
> every agent and synthesizes the result, or stay a documentation-first protocol
> with the optional local runner? Weigh real maintainer value, scope creep risk,
> and OSS positioning.

## Evidence

- `README.md`
- `scripts/council-runner.py`
- `docs/research-foundation.md`
- `examples/transcripts/self-review-2026-06-08.md` (prior self-review concluded:
  stay protocol-first; do not imply automatic orchestration)

## Run Summary

Command: `council-runner.py --execute --agents codex,claude,agy,grok --timeout 600`

| Participant | Model | Result | Notes |
| --- | --- | --- | --- |
| Codex | gpt-5.5 | **failed** | CLI returned `Your workspace is out of credits` — no review produced |
| Gemini (`agy`) | gemini | **timed out** | hit the 5-minute print timeout while still reading evidence files |
| Claude | claude (Alpha) | ok | full review |
| Grok | grok (Bravo) | ok | full review (some `read_file` calls blocked by read-only sandbox) |

Two of four agents produced a usable review. The runner captured both failures,
wrote the partial outputs, and still emitted the comparison and runbook
templates. The council ran on the two reviews that returned.

> The Codex out-of-credits failure is the most literal possible illustration of
> why broader Codex access matters for this kind of maintainer workflow: the
> first-class participant could not participate because the local workspace had
> no credits.

## Phase 1: Independent Reviews (anonymized)

### Reviewer Alpha — perspective: facilitation, adoption, decision-record clarity

**Core judgment:** Stay documentation-first. Ship the *mechanical* half of
orchestration (run agents in parallel + collect outputs), which the runner already
does, but reject the *judgment* half (auto-synthesizing a verdict). The question
bundles two different features and the split is the answer: auto-run is already
shipped and low-risk; auto-synthesize contradicts the core thesis.

Strongest cited evidence:

- Auto-synthesis re-introduces the single point of judgment the project exists to
  remove (`research-foundation.md`: "Independence Before Synthesis"; a minority
  objection with evidence can outweigh majority agreement).
- The runner deliberately stops at `comparison.md` and a runbook that tells the
  human to weigh evidence — a designed forcing function that auto-synthesis would
  delete.
- New gap, self-reported: the only execution proof so far was **single-agent**
  runs; the README's "Repository Contents" lists `council-runner.sh` but omits
  `council-runner.py`, where the orchestration logic actually lives.

Highest-leverage improvement: draw and document a bright line — automation may
*run and collect*, never *decide* — and produce one real multi-agent transcript
before any further orchestration work. Verdict: **not PASS** (new evidence
strengthens the protocol-first decision).

### Reviewer Bravo — perspective: skeptical OSS maintainer, failure scenarios

**Core judgment:** Stay documentation-first. The project already delivered the
scoped optional runner the prior self-review asked for (stage + parallel execute +
collect). Full auto-synthesis is a different product with different risk and
ownership properties.

Strongest cited evidence:

- The prior decision record explicitly said "do not imply that it currently
  orchestrates agents automatically"; the follow-up asked only for a script that
  can *collect* outputs, not synthesize them.
- Mechanistically the runner stops at raw outputs plus skeleton templates — no
  synthesis logic, no consensus engine — matching "the council analyzes, the
  maintainer decides."
- The differentiator in a crowded multi-agent-framework space is honest
  minimalism plus forcing functions, not "we ran the council so you don't have to
  think."

Key risks named: expectation inversion (users assume the tool decides); synthesis
failure modes that are hard to see (treating four-agent agreement as stronger than
one cited blocking objection; masking a tool/sandbox limitation as "the council
considered it"); and a brittleness tax where every CLI auth/sandbox regression
becomes "the council is broken." Verdict: **not PASS**.

## Phase 2: Comparison

| Reviewer | Core judgment | Strongest evidence | Main risk | Blocking objection |
| --- | --- | --- | --- | --- |
| Alpha | Run-and-collect yes; auto-synthesize no | Synthesis = single judgment point the project exists to remove | Synthesis-as-authority drift | Ship a real multi-agent transcript + document the bright line first |
| Bravo | Stay protocol-first; runner already satisfies prior follow-up | Prior decision record + runner stops at raw outputs by design | Expectation inversion; hidden synthesis failures | None blocking; reinforce scope boundary |

- **Agreement:** Both converged on the same answer from different lenses — keep the
  protocol primary and the runner as optional glue; do not add auto-synthesis.
- **Disagreement:** None material. Alpha pushed an optional, clearly-labeled
  `--synthesis-draft` (a non-binding scaffold for `comparison.md`); Bravo did not
  call for it but its "honest minimalism" stance is compatible with a draft that
  never decides.
- **Missing evidence (now being addressed):** a real multi-agent execution
  transcript — which is this file.

Because the two reviews converged on evidence rather than on a head count, and
each labeled itself **not PASS** only because it added new evidence, no further
cross-examination round was needed.

## Decision Record: Orchestrator vs. Protocol

### Decision

Keep `multi-agent-council` documentation-first. The runner may *run and collect*
agent outputs in parallel; it must never *decide*. Do not build an
auto-synthesizing orchestrator.

### Why

Both agents that returned reviews converged, with citations, on the same
conclusion: auto-synthesis re-introduces the single anchored judgment the protocol
exists to remove, raises the install floor against the project's own adoption
promise, and trades a defensible niche for a maintenance treadmill.

### Alternatives Considered

- **Full auto-synthesis orchestrator** — rejected: contradicts core thesis,
  high and recurring maintenance surface, expectation inversion.
- **Optional `--synthesis-draft` scaffold** — deferred: acceptable only if clearly
  labeled a non-binding draft the maintainer must edit; not required now.

### Dissent (real names restored)

- **Claude** (Alpha) and **Grok** (Bravo) agreed on the decision. Their only
  divergence was Claude proposing an optional draft-not-verdict helper that Grok
  did not request; neither treated it as blocking.
- **Codex** (gpt-5.5) could not participate (out of credits).
- **Gemini** (`agy`) timed out before producing a verdict.

### Follow-Up

- [x] Produce a real multi-agent execution transcript (this file).
- [ ] Document the bright line in README + RUNBOOK: automation runs and collects,
  never decides.
- [ ] Add `council-runner.py` to README "Repository Contents"; label `.sh` a wrapper.
- [ ] Improve runner partial-failure reporting ("X/Y agents produced usable output").

## Notes on Honesty

- Reviewer Bravo cited a `docs/openai-codex-oss-application.md` file that was
  present at run time and has since been removed from the repository; its content
  was moved out so the repo reads as a protocol rather than an application
  artifact. The citation is preserved here as a point-in-time record.
- No private paths, secrets, or customer data appear in this transcript.
