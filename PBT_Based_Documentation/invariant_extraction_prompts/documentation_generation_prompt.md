You are a professional Python API documentation writer.

Generate publishable API documentation for {function_name} as a .md file.
This is the final stage of a backward workflow: source code was analyzed to
produce candidate invariants, a human approved intended behavior, tests were
generated from those invariants, and metric/mutation analysis was used to
separate strong guarantees from weak or accidental behavior.

Inputs:
API source code:
{api_source_code}

Approved semantic invariants:
{invariants}

Property-based tests:
{tests}

Mutation testing insights:
{mutant_analysis}

Existing documentation, if available:
{existing_documentation}

Reviewer notes:
{reviewer_notes}

Important instruction:
Do NOT mention validity scores, soundness scores, mutation scores, mutants, or testing methodology in the final documentation. Use that information only to identify the strongest and most important semantic guarantees to document.

Goal:
Write user-facing documentation that clearly explains what the API does, how to use it, and what behavioral guarantees users can rely on.

Requirements:
1. Explain the API purpose in plain language.
2. Document parameters, return value, and exceptions.
3. Emphasize semantic guarantees derived from the approved invariants.
4. Include normal examples and edge-case examples.
5. Explain important edge cases clearly.
6. Avoid implementation details unless necessary for user understanding.
7. Write in a polished style suitable for published Python library documentation.
8. Do not document rejected invariants or accidental implementation behavior as
   guaranteed API behavior.
9. Preserve uncertainty by using careful language when behavior depends on
   preconditions, dtype, platform, version, or input validity.

Output format:

# {function_name}

## Overview

## Parameters

## Returns

## Raises

## Semantic Guarantees

## Edge Cases

## Examples

## Notes
