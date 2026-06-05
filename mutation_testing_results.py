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

mutation_gemini_dateutil = {
    "total_mutants": 816,
    "killed_mutants": 333,
    "survived_mutants": 481,
    "timed_out_mutants": 2,
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

# Zlib
mutation_human_zlib = {
    "total_mutants": 17,
    "killed_mutants": 12,
    "survived_mutants": 5,
    "timed_out_mutants": 0,
    "suspicious_mutants": 0,
    "untested_mutants": 0,
    "skipped_mutants": 0,
    "equivalent_mutants": 0,
}

mutation_codex_zlib = {
    "total_mutants": 17,
    "killed_mutants": 14,
    "survived_mutants": 3,
    "timed_out_mutants": 0,
    "suspicious_mutants": 0,
    "untested_mutants": 0,
    "skipped_mutants": 0,
    "equivalent_mutants": 0,
}

# Decimal
mutation_human_decimal = {
    "total_mutants": 900,
    "killed_mutants": 522,
    "survived_mutants": 371,
    "timed_out_mutants": 2,
    "suspicious_mutants": 0,
    "untested_mutants": 0,
    "skipped_mutants": 0,
    "equivalent_mutants": 5,
}

mutation_codex_decimal = {
    "total_mutants": 1128,
    "killed_mutants": 641,
    "survived_mutants": 481,
    "timed_out_mutants": 2,
    "suspicious_mutants": 0,
    "untested_mutants": 0,
    "skipped_mutants": 0,
    "equivalent_mutants": 4,
}
mutation_gemini_decimal = {
    "total_mutants": 1128,
    "killed_mutants": 665,
    "survived_mutants": 456,
    "timed_out_mutants": 3,
    "suspicious_mutants": 0,
    "untested_mutants": 4,
    "skipped_mutants": 0,
    "equivalent_mutants": 0,
}

# NP
# NumPy
mutation_human_numpy = {
    "total_mutants": 99,
    "killed_mutants": 26,
    "survived_mutants": 28,
    "timed_out_mutants": 0,
    "suspicious_mutants": 0,
    "untested_mutants": 0,
    "skipped_mutants": 0,
    "equivalent_mutants": 45,
}

# NumPy (Codex)
mutation_codex_numpy = {
    "total_mutants": 122,
    "killed_mutants": 72,
    "survived_mutants": 49,
    "timed_out_mutants": 0,
    "suspicious_mutants": 0,
    "untested_mutants": 0,
    "skipped_mutants": 0,
    "equivalent_mutants": 1,
}
# NumPy (Gemini)
mutation_gemini_numpy = {
    "total_mutants": 122,
    "killed_mutants": 65,
    "survived_mutants": 56,
    "timed_out_mutants": 0,
    "suspicious_mutants": 0,
    "untested_mutants": 0,
    "skipped_mutants": 0,
    "equivalent_mutants": 1,
}



calculate_mutation_scores(mutation_human_dateutil)
calculate_mutation_scores(mutation_codex_dateutil)
calculate_mutation_scores(mutation_gemini_dateutil)

calculate_mutation_scores(mutation_human_statistics)
calculate_mutation_scores(mutation_codex_statistics)


calculate_mutation_scores(mutation_human_html)
calculate_mutation_scores(mutation_codex_html)

calculate_mutation_scores(mutation_human_zlib)
calculate_mutation_scores(mutation_codex_zlib)

calculate_mutation_scores(mutation_human_decimal)
calculate_mutation_scores(mutation_codex_decimal)
calculate_mutation_scores(mutation_gemini_decimal)

calculate_mutation_scores(mutation_human_numpy)
calculate_mutation_scores(mutation_codex_numpy)
calculate_mutation_scores(mutation_gemini_numpy)

print("dateutil")
print("Human: \n")
print(mutation_human_dateutil)
print()
print("CODEX: \n")
print(mutation_codex_dateutil)
print()
print("GEMINI: \n")
print(mutation_gemini_dateutil)
print()
print()
print("stats")
print(mutation_human_statistics)
print()
print(mutation_codex_statistics)
print()
print("html")
print(mutation_human_html)
print()
print(mutation_codex_html)
print()
print("zlib")
print(mutation_human_zlib)
print()
print(mutation_codex_zlib)
print()
print("decimal")
print("human: \n")
print(mutation_human_decimal)
print()
print("codex: \n")
print(mutation_codex_decimal)
print("gemini: \n")
print(mutation_gemini_decimal)
print()
print("human: \n")
print(mutation_human_numpy)
print("codex: \n")
print(mutation_codex_numpy)
print("gemini: \n")
print(mutation_gemini_numpy)