# Safety Model

Multi-Agent Council is an analysis workflow. It should not grant agents broad
write access by default.

## Default Boundary

Start every council run as read-only:

- read files
- inspect diffs
- inspect logs
- inspect test output
- read public docs
- summarize evidence

Require maintainer approval before:

- editing files
- deleting files
- running destructive commands
- posting comments or messages
- changing repository settings
- changing infrastructure
- calling external services with private data

## Sensitive Context

Do not send the following to public examples or third-party tools:

- tokens, passwords, API keys, and private keys
- customer or patient data
- private incident records
- private company contracts
- internal hostnames or deployment secrets
- confidential logs

## Provider Data and Training

A council sends your evidence to several third-party AI providers at once, which
multiplies where that data can go. Before running `--execute`, understand how
each provider treats your inputs. The notes below reflect provider terms as of
2026; terms change, so verify the current policy for any regulated or sensitive
data.

- **Consumer subscriptions generally train on your inputs by default.** OpenAI
  (ChatGPT plans), Google (free Gemini / app tier), and xAI (consumer Grok) may
  use inputs and outputs to improve their models unless you opt out in each
  tool's data controls. Anthropic uses a per-account choice. Turn training off on
  every consumer plan you run through a council.
- **Paid API / business tiers generally do not train on your data.** OpenAI API
  and Business, Anthropic Commercial/API, the paid Gemini API, and the xAI API
  state that inputs are not used to train their models by default. For anything
  sensitive, run the council against API-key-backed CLIs rather than consumer
  subscriptions.
- **Treat the free Gemini / app tier as the least private.** Its terms allow
  inputs to be used for product improvement and human review, with retention that
  can outlast deletion. Prefer a paid Gemini API key for non-trivial code.
- **Invoke each vendor CLI directly.** Do not route a provider's authentication
  through third-party OAuth proxies or wrappers — several providers treat that as
  a terms violation and have suspended accounts for it. This project calls the
  official CLIs (`codex`, `claude`, `agy`, `grok`) as subprocesses, which is the
  intended, supported path; keep it that way.
- **Do not use council outputs to train models.** Providers restrict using their
  output to train or build competing models. A council's human review and
  comparison is not model training — but feeding these outputs into model
  training or a competing AI product would cross that line.

When in doubt, send a maintainer-written summary instead of raw private context,
and never put secrets, customer data, or patient data through any tier.

## Review Priority

For security-sensitive changes, ask reviewers to report in this order:

1. Blocking issues.
2. Trust boundary changes.
3. Data exposure risks.
4. Missing tests.
5. Safer alternatives.

## Human Decision Rule

The council provides structured evidence. The maintainer decides what ships.
