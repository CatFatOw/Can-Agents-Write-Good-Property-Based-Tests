def calculate_mutation_scores(results):
    """Adds mutation_score and covered_mutation_score to a mutation results dictionary."""

    results["mutation_score"] = (
        results["killed_mutants"]
        / results["total_mutants"]
    ) * 100

    results["covered_mutation_score"] = (
        results["killed_mutants"]
        / (
            results["total_mutants"]
            - results["untested_mutants"]
        )
    ) * 100

    return results

# Dateutil

# HUMAN
mutation_human_dateutil = {
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
mutation_codex_dateutil = {
    "total_mutants": 2454,
    "killed_mutants": 791,
    "survived_mutants": 594,
    "timed_out_mutants": 13,
    "suspicious_mutants": 0,
    "untested_mutants": 1056,
    "skipped_mutants": 0,
    "equivalent_mutants": 0,
}


# Statistics Library

# Human 

mutation_human_statistics = {
    "total_mutants": 1268,
    "killed_mutants": 95,
    "survived_mutants": 1039,
    "timed_out_mutants": 0,
    "suspicious_mutants": 0,
    "untested_mutants": 0,
    "skipped_mutants": 134,
    "equivalent_mutants": 0,
}

# Codex
mutation_codex_statistics = {
    "total_mutants": 1279,
    "killed_mutants": 112,
    "survived_mutants": 1039,
    "timed_out_mutants": 0,
    "suspicious_mutants": 0,
    "untested_mutants": 0,
    "skipped_mutants": 128,
    "equivalent_mutants": 0,
}



# NP

# Human 
mutation_human_np_linspace = {
    "total_mutants": 192,
    "killed_mutants": 54,
    "survived_mutants": 0,
    "timed_out_mutants": 0,
    "suspicious_mutants": 0,
    "untested_mutants": 138,
    "skipped_mutants": 0,
    "equivalent_mutants": 0,
}


mutation_codex_np_linspace = {
    "total_mutants": 192,
    "killed_mutants": 51,
    "survived_mutants": 0,
    "timed_out_mutants": 0,
    "suspicious_mutants": 0,
    "untested_mutants": 141,
    "skipped_mutants": 0,
    "equivalent_mutants": 0,
}
calculate_mutation_scores(mutation_human_dateutil)
calculate_mutation_scores(mutation_codex_dateutil)
calculate_mutation_scores(mutation_human_statistics)
calculate_mutation_scores(mutation_codex_statistics)
calculate_mutation_scores(mutation_human_np_linspace)
calculate_mutation_scores(mutation_codex_np_linspace)



print("dateutil")
print(mutation_human_dateutil)
print()
print(mutation_codex_dateutil)
print()
print()
print("stats")
print(mutation_human_statistics)
print()
print(mutation_codex_statistics)
print()
print("np")
print(mutation_human_np_linspace)
print()
print(mutation_codex_np_linspace)