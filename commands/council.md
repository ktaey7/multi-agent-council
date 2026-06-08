---
description: Run an evidence-first multi-agent council on a question and produce a decision record.
---

# Council

Run a Multi-Agent Council on the user's request and end with a maintainer-owned
decision record.

User request: $ARGUMENTS

Follow the Multi-Agent Council protocol in the `multi-agent-council` skill
(`.agents/skills/multi-agent-council/SKILL.md`), specifically its **Turnkey
Execution** flow:

1. Gather evidence from the request (files, diffs, issues named in `$ARGUMENTS`).
2. Run round-1 independent reviews in parallel via
   `scripts/council-runner.sh --execute --question "..." --evidence ... --agents auto`.
3. Anonymize reviews with codenames; build the comparison table without stating
   the consensus ratio.
4. Run one cross-examination round only if reviews diverge or `$ARGUMENTS`
   contains `--debate`, using `scripts/council-runner.sh --execute --prompts-dir`.
5. Synthesize a decision record (Decision / Why / Alternatives / Risks / dissent
   with real names / Follow-up).
6. If fewer agents are available or one fails, continue and note
   `⚠️ council reduced to N agents (reason)`.

Apply the bias controls (codename anonymization, hide the consensus ratio,
rotate speaking order, PASS to converge) throughout. Begin read-only; never send
private data to third-party CLIs without explicit confirmation.
