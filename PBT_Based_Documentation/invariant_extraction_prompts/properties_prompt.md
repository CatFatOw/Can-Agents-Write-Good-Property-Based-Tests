You are reviewing the implementation and optional documentation of
{function_name}.

This workflow runs backward from implementation to documentation. Your task is
to identify up to 5 high-value candidate semantic invariants from the source
code. These invariants will be reviewed by a human before tests or
documentation are generated.

Inputs:

Function signature:
{function_signature}

Source code:
{api_source_code}

Existing documentation, if available:
{api_documentation}

Your candidate invariants should be suitable for:

1. Property-based testing
2. Documentation
3. Mutation testing

Requirements:

- Focus on observable behavior.
- Properties should be strong enough to detect implementation bugs.
- Prefer semantic guarantees over generic algebraic laws.
- Avoid redundant properties.
- Avoid properties that merely restate implementation steps.
- Clearly separate intended behavior from implementation accidents.
- Include preconditions when the property is not valid for every input.
- Include edge cases suggested by the code.
- Do not write tests.

For each property provide:

Property:
Evidence from source:
User-facing interpretation:
Preconditions / input domain:
Important edge cases:
Why it matters:
Expected mutation-killing strength:
(High / Medium / Low)
Human decision:
Pending

Return only the list.
