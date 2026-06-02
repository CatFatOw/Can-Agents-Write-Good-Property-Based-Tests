# Tested Functions From Source Code

Python's `zlib` module is a compiled extension rather than a Python module.
The matching CPython 3.12.7 source remains in the parent directory at
`../cpython_source/zlibmodule.c` for reference and future API additions.

Mutmut cannot mutate C source. It is therefore configured to mutate the narrow
Python adapter in `../zlib_target.py`, which exposes only the selected APIs:

- `zlib.compress()`
- `zlib.decompress()`
- `zlib.adler32()`

Mutmut also uses `mutate_only_covered_lines=true`, so it generates mutants only
for adapter lines reached by the selected API wrappers.
