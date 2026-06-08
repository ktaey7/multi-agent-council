# Maintainer Workflows

Multi-Agent Council is designed for maintainers, not generic brainstorming.
These workflows keep agent output tied to a concrete repository decision.

## Pull Request Review

Use when a PR touches shared behavior, auth, security, data migration, public
API shape, build tooling, or contributor workflows.

Evidence:

- PR diff
- relevant tests
- docs changed by the PR
- issue or design note
- CI output

Perspectives:

- implementation correctness
- missing tests
- security and trust boundary
- contributor experience

Decision record:

- merge
- request changes
- split PR
- block pending evidence

## Issue Triage

Use when maintainers need to decide whether an issue is valid, urgent, or
release-blocking.

Evidence:

- issue body
- reproduction steps
- logs or screenshots
- affected version
- related code paths

Output:

- likely component
- reproduction plan
- priority
- owner
- next action

## Architecture Decision

Use when adopting a dependency, changing an API, adding a subsystem, or removing
a legacy path.

Evidence:

- design proposal
- current architecture docs
- code ownership boundaries
- performance, security, or migration constraints

Output:

- decision
- alternatives considered
- migration plan
- rollback plan

## Release Readiness

Use before a release tag or package publish.

Evidence:

- changelog
- diff since last release
- CI output
- open issues marked release-blocking
- docs and migration notes

Output:

- release or hold
- blockers
- release notes
- post-release monitoring tasks
