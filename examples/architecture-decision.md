# Example: Architecture Decision

## Question

Should a project add a persistent vector index for documentation search?

## Evidence Sources

- current search implementation
- repository size
- update frequency
- contributor setup docs
- CI runtime budget

## Council Summary

Agreement:

- A vector index can improve discovery for long-form docs.
- The index should not contain private content or generated local artifacts.

Disagreement:

- Whether the first release should include embeddings or only a pluggable search
  interface.

Counterfactual:

- The index may create a maintenance burden if contributors need heavyweight
  model dependencies to run tests.

## Decision

Start with a pluggable search interface and a sample local indexer. Do not commit
generated embeddings. Revisit hosted or prebuilt index support after usage
signals exist.
