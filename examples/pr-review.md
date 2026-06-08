# Example: Pull Request Review

## Question

Should we merge a PR that adds a shell-command helper to a maintainer tool?

## Evidence Sources

- `git diff origin/main...HEAD`
- `src/commands/run.ts`
- `src/config/permissions.ts`
- `tests/commands/run.test.ts`

## Assigned Perspectives

- Reviewer A: security and trust boundary
- Reviewer B: implementation correctness
- Reviewer C: contributor experience
- Reviewer D: test coverage and release risk

## Sample Finding

| Reviewer | Core judgment | Strongest evidence | Main risk | Blocking objection |
| --- | --- | --- | --- | --- |
| A | Request changes | command args are passed through without allowlist checks | arbitrary shell execution | yes |
| B | Request changes | parser handles quotes but not newline injection | malformed command behavior | no |
| C | Split PR | docs mix user commands and maintainer commands | contributor confusion | no |
| D | Request tests | no test for denied commands | regression risk | no |

## Decision Record

Request changes before merge.

Required follow-up:

- [ ] Add explicit command allowlist.
- [ ] Add deny-by-default behavior.
- [ ] Add tests for denied commands and newline input.
- [ ] Separate user docs from maintainer docs.
