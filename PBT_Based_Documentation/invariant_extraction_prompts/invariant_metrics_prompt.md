You are analyzing survived mutants from mutation testing.

Original code:
{original}

Mutated code:
{mutant}

Current property-based tests:
{tests}

Approved invariants:
{approved_invariants}

Current metrics:
{metrics}

Task:
Analyze whether this survived mutant represents a meaningful weakness in the current property-based tests.

For each survived mutant, answer:

1. Behavioral change:
What changed between the original code and the mutant?

2. Test gap:
Which property or invariant should have detected this mutant, if any?

3. Why it survived:
Explain why the current tests failed to catch it.

4. Documentation relevance:
Does this mutant reveal behavior that should be documented as a user-facing
semantic guarantee, or is it internal/accidental behavior?

5. Severity classification:
Classify the mutant as one of:

- Low confidence:
  The mutant is likely equivalent, unreachable, defensive-only, or outside the intended API behavior.

- Medium confidence:
  The mutant changes behavior, but only for a narrow edge case or ambiguous behavior.

- High confidence:
  The mutant changes observable, documented, or semantically important behavior that the tests should catch.

6. Decision:
- If Low or Medium confidence: mark as ACCEPTABLE SURVIVAL.
- If High confidence: mark as TEST GAP and propose one new invariant that would likely kill the mutant.

7. Recommendation

Based on the analysis:

- ACCEPTABLE SURVIVAL
  The mutant is unlikely to represent a meaningful testing weakness.

- REVIEW NEEDED
  The mutant may indicate a missing edge case or underspecified behavior.

- REGENERATE TESTS
  The mutant exposes an important behavioral change that the current tests should detect.

8. User Action

Please choose one:

A. Accept this mutant as acceptable.

B. Regenerate properties targeting the identified gap.

C. Regenerate tests using the proposed invariant.

D. Generate additional invariants for this API.

E. Analyze the next survived mutant.
