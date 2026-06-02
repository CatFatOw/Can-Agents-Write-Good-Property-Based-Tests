# Tested Functions From Source Code

The complete vendored `html` package remains in the parent directory so imports
and future API additions continue to work.

Mutmut is configured with `mutate_only_covered_lines=true`, so it generates
mutants only for source lines reached by the target API wrappers:

- `html.escape()`
- `html.unescape()`

Configured source file:

- `../html/__init__.py`
