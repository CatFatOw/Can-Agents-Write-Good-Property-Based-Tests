You are generating property-based tests from human-approved invariants.

Inputs:

Function name:
{function_name}

Function signature:
{function_signature}

Source code:
{api_source_code}

Approved invariants:
{approved_invariants}

Reviewer notes:
{reviewer_notes}

Generate Hypothesis tests that maximize bug detection while remaining valid and
sound.

Requirements:

- One test per property.
- Avoid duplicating coverage.
- Use assumptions sparingly.
- Generate realistic inputs.
- Avoid excessive filtering.
- Handle overflow, NaN, infinities, and invalid inputs when relevant.
- Prefer small, finite, bounded numeric values unless the approved invariant is
  specifically about NaN, infinities, overflow, or extreme values.
- Prefer relational properties over exact-output examples.
- Prefer independent oracles over calling the same implementation under test.
- Include targeted boundary examples when random generation is unlikely to hit
  them.
- Explicitly encode each invariant's preconditions in the strategy or with a
  minimal assumption.
- Do not write negative/rejection tests unless the approved invariant directly
  states the exact exception behavior and the source evidence is strong.
- For NumPy arrays, construct valid shapes directly. Do not call functions such
  as `np.broadcast_shapes(...)` inside `assume(...)` unless exceptions are
  caught; an exception during data generation makes the test invalid.
- For floating point comparisons, use `np.testing.assert_allclose` or
  `np.allclose(..., equal_nan=True)` with tolerances. Avoid exact equality for
  floating point or complex reductions.
- When testing `keepdims=True`, assert the expected kept dimensions explicitly
  or compare against an oracle that also uses `keepdims=True`.
- For byte string dtypes, avoid generated values with embedded or trailing null
  bytes unless the invariant is specifically about null-byte handling.
- If the API is an imported ufunc or module attribute rather than a local
  Python `def`, prefer importing the public runtime API named in reviewer notes.
- Include comments explaining which property is being tested.

The resulting tests must be executable with pytest and Hypothesis.

Return only Python code.
