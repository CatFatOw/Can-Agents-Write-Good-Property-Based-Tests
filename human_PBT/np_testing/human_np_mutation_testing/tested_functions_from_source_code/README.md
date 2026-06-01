# Tested Functions From Source Code

The complete vendored `numpy` source tree remains in the parent directory so
imports and future API additions continue to work.

Mutmut is configured with `mutate_only_covered_lines=true`, so it generates
mutants only for source lines reached by the target API wrapper:

- `numpy.linspace()`

Configured source file:

- `../numpy/_core/function_base.py`
