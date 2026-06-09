# Known Issues and Limitations

This project is honest about what it does not do well yet. If one of these blocks
you, open an issue.

## Scope

- **It reviews; it does not build.** There is no task lifecycle, no worker
  delegation, no code generation. See "What This Is — and Isn't" in the README.
  Pair it with an orchestration tool if you want agents to produce work.

## Execution (`--execute`)

- **Requires the participant CLIs installed and authenticated.** With no CLIs on
  PATH, `--execute` cannot run; use the manual protocol or omit `--execute` to
  stage prompts for copy/paste. The runner reports which CLIs it skipped.
- **A single available agent is a pass, not a council.** If only one CLI is
  installed, you get a single-agent review. The runner prints a warning; do not
  mistake it for cross-validation.
- **The turnkey flow is instruction-driven, not deterministic.** `/council` works
  by the driving agent following the skill. Quality depends on the model honoring
  the protocol, so results vary more than a hardcoded pipeline would.
- **`agy` (Gemini) takes the prompt only as a command-line argument** — it has no
  stdin or `--prompt-file` path. A very large prompt can exceed the OS argument
  limit; the runner captures this cleanly, reports it, and continues with the
  other agents, but that agent's review is lost for that run. Keep evidence
  bounded or summarize it.
- **Round 2 writes a new run directory.** The optional cross-examination round
  (`--prompts-dir`) creates a fresh `.council-runs/<ts>/` rather than overwriting
  round 1; the driver reads both. Pass `--out` to choose the location.

## Data and trust

- **Council multiplies data exposure.** Evidence goes to several third-party
  providers at once. On consumer plans, providers may train on your inputs by
  default. Never send secrets, customer data, or patient data; prefer paid API
  tiers for sensitive work. See `docs/safety-model.md`.

## Platform

- Developed and tested on macOS and Linux. The runner is Python 3 standard
  library plus Bash; Windows is untested (use WSL).

## Testing

- CI runs the runner's unit tests, shell syntax checks, a dry-run install, and a
  prereq check. The live multi-agent `--execute` path is not exercised in CI
  (it needs authenticated third-party CLIs); see the transcripts in
  `examples/transcripts/` for real runs.
