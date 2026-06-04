# Tested Functions From Source Code

The complete vendored `dateutil` source tree remains in the parent directory so
imports and future API additions continue to work.

Mutmut is configured with `mutate_only_covered_lines=true`, so it generates
mutants only for source lines reached by the target API wrappers:

- `dateutil.parser.isoparse()`
- `dateutil.parser.parse()`

Configured source files:

- `../dateutil/parser/isoparser.py`
- `../dateutil/parser/_parser.py`
