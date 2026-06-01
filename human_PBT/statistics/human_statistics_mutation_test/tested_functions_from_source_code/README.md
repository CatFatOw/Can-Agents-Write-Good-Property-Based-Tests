# Tested Functions From Source Code

The complete vendored `statistics.py` source file remains in the parent
directory so imports and future API additions continue to work.

Mutmut is configured with `mutate_only_covered_lines=true`, so it generates
mutants only for source lines reached by the target API wrappers:

- `statistics.mean()`
- `statistics.geometric_mean()`
- `statistics.correlation()`
- `statistics.linear_regression()`

Configured source file:

- `../statistics.py`
