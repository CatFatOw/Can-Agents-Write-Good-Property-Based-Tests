# Invariant-Based Documentation Generator Workflow

This workflow reconstructs stronger API documentation from source-code behavior.
It runs in the reverse direction of ordinary documentation-based test
generation:

```text
source code
  -> candidate invariants
  -> human review
  -> Hypothesis tests
  -> validity / soundness / mutation analysis
  -> accepted semantic guarantees
  -> improved documentation
```

## Goal

Given an implementation, identify observable semantic invariants, let a human
curator accept or reject them, generate property-based tests for the accepted
invariants, evaluate those tests, and use only the validated behavioral
guarantees to write clearer API documentation.

The final documentation should describe what users can rely on. It should not
mention the testing workflow, mutation scores, validity scores, soundness
scores, or internal mutant details.

## Stage 1: Source-Code Invariant Extraction

Input:

- API name
- Function signature
- Source code for the function and relevant helpers
- Existing documentation, if available
- Known constraints or intended audience, if available

Use [`properties_prompt.md`](./properties_prompt.md) to generate candidate
semantic invariants.

Output:

```text
1. Property:
   Evidence from source:
   User-facing interpretation:
   Preconditions / input domain:
   Edge cases:
   Expected mutation-killing strength:
   Human decision: Pending
```

Rules:

- Prefer observable behavior over implementation details.
- Separate likely guarantees from guesses.
- State preconditions explicitly.
- Include edge cases that matter for user behavior.
- Do not generate tests yet.

## Stage 2: Human Review

The human reviewer labels each candidate invariant:

| Decision | Meaning |
|---|---|
| Accept | The invariant is intended behavior and should be tested/documented. |
| Reject | The invariant is false, accidental, implementation-specific, or not useful. |
| Revise | The invariant is close but needs a narrower domain or clearer wording. |
| Needs Evidence | The invariant may be true, but source evidence is weak or ambiguous. |

Only accepted invariants move to test generation.

Rejected invariants should be kept in a review log with a short reason, because
they help separate intended API guarantees from accidental implementation
behavior.

## Stage 3: Property-Based Test Generation

Input:

- Accepted invariants
- Function signature
- Source code
- Any reviewer notes about valid input domains

Use [`pbt_generation_prompt.md`](./pbt_generation_prompt.md) to generate pytest
and Hypothesis tests.

Output requirements:

- One test per accepted invariant.
- Strategies should generate valid, realistic, and edge-case inputs.
- Tests should use independent oracles when possible.
- Tests should avoid simply reimplementing the same mutated source logic.
- Tests should include fixed examples for important boundaries when random
  generation is unlikely to hit them.

## Stage 4: Test Evaluation Gate

Run the generated tests and collect:

- Validity: tests do not raise unexpected exceptions.
- Soundness: accepted invariants hold for generated inputs.
- Mutation results: survived, killed, timed-out, suspicious, and untested
  mutants.

Gate decisions:

| Result | Action |
|---|---|
| Valid and sound, strong mutation performance | Promote invariant to documentation candidate. |
| Valid and sound, but high-confidence mutants survive | Revise invariant or generate additional tests. |
| Invalid test | Fix strategy or narrow preconditions. |
| Unsound property | Send invariant back to human review. |
| Equivalent / low-confidence mutant survives | Record as acceptable survival. |

Use [`invariant_metrics_prompt.md`](./invariant_metrics_prompt.md) to interpret
survived mutants and decide whether the invariant/test should be revised.

## Stage 5: Invariant Revision Loop

For each meaningful survived mutant:

1. Identify the missing behavioral distinction.
2. Decide whether that behavior is intended API behavior.
3. If intended, write or revise an invariant.
4. Generate or update the corresponding Hypothesis test.
5. Rerun the metric gate.

This loop stops when:

- The human reviewer accepts the remaining survivors as low-value or out of
  scope, or
- Additional tests no longer improve meaningful mutation coverage, or
- The accepted invariant set is stable enough for documentation.

## Stage 6: Documentation Reconstruction

Input:

- Source code
- Accepted invariants
- Passing property-based tests
- Mutation analysis summaries
- Existing documentation, if any

Use [`documentation_generation_prompt.md`](./documentation_generation_prompt.md)
to generate improved documentation.

Documentation rules:

- Document only accepted and validated semantic guarantees.
- Preserve important preconditions and exceptions.
- Include examples that illustrate normal behavior and edge cases.
- Do not expose testing methodology or mutation-testing details to users.
- Avoid presenting accidental implementation details as API guarantees.

## Final Artifacts

Each API should produce:

| Artifact | Purpose |
|---|---|
| Candidate invariant list | Source-derived hypotheses before review. |
| Human review log | Accept/reject/revise decisions and rationale. |
| Generated PBT suite | Executable Hypothesis tests for accepted invariants. |
| Metrics report | Validity, soundness, and mutation-testing interpretation. |
| Reconstructed documentation | User-facing API docs derived from validated behavior. |

## Recommended Directory Layout

```text
PBT_Based_Documentation/
  invariant_extraction_prompts/
    backward_pbt_documentation_workflow.md
    properties_prompt.md
    pbt_generation_prompt.md
    invariant_metrics_prompt.md
    documentation_generation_prompt.md
  source_code/
    <library>/
  artifacts/
    <api_name>/
      candidate_invariants.md
      human_review.md
      generated_tests.py
      metrics_report.md
      reconstructed_documentation.md
```
