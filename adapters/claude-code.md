# Claude Code Adapter

Claude Code can be used as a council participant or as the facilitator that
prepares context, compares independent reviews, and writes the final decision
record.

## Participant Prompt

```text
Use the Multi-Agent Council format. Review the referenced files from the
assigned perspective only. Do not assume other reviewers agree. Cite evidence.
```

## Facilitator Prompt

```text
You are the council facilitator. Compare the independent reviews. Do not choose
based on majority. Choose based on evidence quality, blocking objections, and
maintainer constraints. Produce a decision record.
```

## Notes

- Keep tool-specific runtime details outside public decision records.
- Prefer summaries for large secondary context.
- Keep private paths, credentials, and internal incident notes out of shared
  prompts and examples.
