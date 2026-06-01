# Dateutil

# HUMAN
mutation_human_dateutil_parse = {
    "total_mutants": 2454,
    "killed_mutants": 388,
    "survived_mutants": 810,
    "timed_out_mutants": 51,
    "suspicious_mutants": 0,
    "untested_mutants": 1205,
    "skipped_mutants": 0,
    "equivalent_mutants": 0,
}

# CODEX
mutation_codex_dateutil_parse = {
    "total_mutants": 2454,
    "killed_mutants": 791,
    "survived_mutants": 594,
    "timed_out_mutants": 13,
    "suspicious_mutants": 0,
    "untested_mutants": 1056,
    "skipped_mutants": 0,
    "equivalent_mutants": 0,
}

# Mutation score: Overall effectiveness of testsuite
mutation_human_dateutil_parse["mutation_score"] = (
    (mutation_human_dateutil_parse["killed_mutants"]
    / mutation_human_dateutil_parse["total_mutants"]) * 100
)

mutation_codex_dateutil_parse["mutation_score"] = (
    (mutation_codex_dateutil_parse["killed_mutants"]
    / mutation_codex_dateutil_parse["total_mutants"]) * 100
)


# Covered mtuation_score: of the mutants discovered how many did it kill
mutation_human_dateutil_parse["covered_mutation_score"] = (
    mutation_human_dateutil_parse["killed_mutants"]
    / (
        mutation_human_dateutil_parse["total_mutants"]
        - mutation_human_dateutil_parse["untested_mutants"]
    )
) * 100

mutation_codex_dateutil_parse["covered_mutation_score"] = (
    mutation_codex_dateutil_parse["killed_mutants"]
    / (
        mutation_codex_dateutil_parse["total_mutants"]
        - mutation_codex_dateutil_parse["untested_mutants"]
    )
) * 100

print(mutation_human_dateutil_parse)
print()
print(mutation_codex_dateutil_parse)