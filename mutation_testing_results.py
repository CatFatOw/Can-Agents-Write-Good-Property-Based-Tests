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
    "total_mutants": 973,
    "killed_mutants": 366,
    "survived_mutants": 591,
    "timed_out_mutants": 10,
    "suspicious_mutants": 0,
    "untested_mutants": 6,
    "skipped_mutants": 0,
    "equivalent_mutants": 0,
}

# CODEX
mutation_codex_dateutil = {
    "total_mutants": 1178,
    "killed_mutants": 777,
    "survived_mutants": 388,
    "timed_out_mutants": 13,
    "suspicious_mutants": 0,
    "untested_mutants": 0,
    "skipped_mutants": 0,
    "equivalent_mutants": 0,
}


# Statistics Library

# Human 

mutation_human_statistics = {
    "total_mutants": 270,
    "killed_mutants": 204,
    "survived_mutants": 53,
    "timed_out_mutants": 0,
    "suspicious_mutants": 0,
    "untested_mutants": 13,
    "skipped_mutants": 0,
    "equivalent_mutants": 0,
}

# Codex
mutation_codex_statistics = {
    "total_mutants": 290,
    "killed_mutants": 226,
    "survived_mutants": 51,
    "timed_out_mutants": 0,
    "suspicious_mutants": 0,
    "untested_mutants": 13,
    "skipped_mutants": 0,
    "equivalent_mutants": 0,
}



# NP

# Human 
mutation_human_np = {
    "total_mutants": 141,
    "killed_mutants": 50,
    "survived_mutants": 91,
    "timed_out_mutants": 0,
    "suspicious_mutants": 0,
    "untested_mutants": 0,
    "skipped_mutants": 0,
    "equivalent_mutants": 0,
}


mutation_codex_np = {
    "total_mutants": 141,
    "killed_mutants": 50,
    "survived_mutants": 91,
    "timed_out_mutants": 0,
    "suspicious_mutants": 0,
    "untested_mutants": 0,
    "skipped_mutants": 0,
    "equivalent_mutants": 0,
}

# HTML
mutation_human_html = {
    "total_mutants": 92,
    "killed_mutants": 73,
    "survived_mutants": 19,
    "timed_out_mutants": 0,
    "suspicious_mutants": 0,
    "untested_mutants": 0,
    "skipped_mutants": 0,
    "equivalent_mutants": 0,
}
# Codex
mutation_codex_html = {
    "total_mutants": 85,
    "killed_mutants": 73,
    "survived_mutants": 12,
    "timed_out_mutants": 0,
    "suspicious_mutants": 0,
    "untested_mutants": 0,
    "skipped_mutants": 0,
    "equivalent_mutants": 0,
}

calculate_mutation_scores(mutation_human_dateutil)
calculate_mutation_scores(mutation_codex_dateutil)
calculate_mutation_scores(mutation_human_statistics)
calculate_mutation_scores(mutation_codex_statistics)
calculate_mutation_scores(mutation_human_np)
calculate_mutation_scores(mutation_codex_np)
calculate_mutation_scores(mutation_human_html)
calculate_mutation_scores(mutation_codex_html)



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
print(mutation_human_np)
print()
print(mutation_codex_np)
print("html")
print(mutation_human_html)
print()
print(mutation_codex_html)