# Gemini CLI Adapter

Use Gemini as a council participant for broad alternative generation, product
impact, documentation review, or second-opinion analysis.

## Prompt Shape

Prefer plain Markdown prompts.

```text
## Question
[question]

## Evidence
[files, summaries, logs, or diffs]

## Perspective
[assigned perspective]

Return:
1. Core judgment
2. Evidence
3. Implementation impact
4. Risks
5. Open questions
```

## Notes

- Avoid tool-specific markup that your local CLI cannot parse.
- Do not send secrets, private logs, or confidential customer data.
- Ask for explicit uncertainty when evidence is incomplete.
