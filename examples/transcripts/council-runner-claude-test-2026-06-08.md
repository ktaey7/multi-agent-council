# Runner Transcript: Claude CLI Execution Test

Date: 2026-06-08

Purpose:

Validate that `scripts/council-runner.sh --execute` can invoke local agent CLIs,
capture output, and write run metadata.

Command:

```bash
scripts/council-runner.sh \
  --question "Review scripts/check-prereqs.sh for clarity and safety." \
  --evidence scripts/check-prereqs.sh \
  --agents claude \
  --out /private/tmp/mac-council-runner-claude-exec-test \
  --execute \
  --timeout 240
```

Result:

```text
Council run staged: /private/tmp/mac-council-runner-claude-exec-test
Executed 1/1 agents successfully
```

Second execution check:

```bash
scripts/council-runner.sh \
  --question "Review scripts/check-prereqs.sh for clarity and safety." \
  --evidence scripts/check-prereqs.sh \
  --agents agy \
  --out /private/tmp/mac-council-runner-agy-exec-test-2 \
  --execute \
  --timeout 240
```

Result:

```text
Council run staged: /private/tmp/mac-council-runner-agy-exec-test-2
Executed 1/1 agents successfully
```

Generated files:

```text
RUNBOOK.md
comparison.md
metadata.json
outputs/claude.md
prompts/claude.md
```

Metadata summary:

```json
{
  "execute": true,
  "agents": ["claude"],
  "results": [
    {
      "agent": "claude",
      "status": "ok",
      "returncode": 0
    }
  ]
}
```

Reviewer finding summary:

Claude judged `scripts/check-prereqs.sh` safe but found adoption issues:

- It checked command availability but not authentication.
- It had no machine-readable strict mode.
- `--version` calls should close stdin to reduce hang risk.
- Output should avoid false confidence by showing that auth is not checked.

Follow-up implemented:

- Added `--strict`.
- Added `Available: N/4` summary.
- Added `(auth not checked)` to found CLI rows.
- Closed stdin on version checks with `</dev/null`.
- Moved prerequisite detection into `council-runner.py`.
- Added Python wrapper fallback from `python3` to `python` when it is Python 3.
- Captured version output from stderr as well as stdout.
- Changed prompt-only `--agents auto` to stage all supported agent prompts, so
  the default documented command works even before local CLIs are installed.

Known limitation:

Nested `codex exec` may fail inside restricted Codex-managed sandboxes with
app-server initialization errors. In a normal user shell, Codex CLI should be
tested directly by the maintainer.
