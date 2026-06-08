# Security Policy

Multi-Agent Council is a review protocol, but examples and adapters may discuss
tools that can read files, write files, run commands, or call external services.

## Reporting

Please open a private security advisory or contact the maintainer if you find a
workflow that could encourage unsafe execution, secret exposure, or accidental
publication of private data.

## Safety Expectations

- Council runs should start read-only.
- Sensitive data must be redacted before examples are shared.
- Tool adapters should document write and network boundaries clearly.
- Destructive actions require explicit maintainer approval.
