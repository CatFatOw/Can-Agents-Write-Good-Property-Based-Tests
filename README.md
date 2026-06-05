# Can Agents Write Good Property-Based Tests from Documentation?

Research project for the Carnegie Mellon University REU program by Michael Wu and Gorden Jin,
May 2026.

This repository studies whether modern coding agents can generate useful
property-based tests (PBTs) for real Python APIs using only API documentation and
prompted reasoning. The work is inspired by
[Can Large Language Models Write Good Property-Based Tests?](https://doi.org/10.48550/arXiv.2307.04346)
and adapts its documentation-driven workflow to Codex-style and Gemini-generated
Hypothesis tests.

## Research Question

Can agent-generated property-based tests match or exceed human-written PBTs on:

1. **Validity**: the test executes without unexpected runtime errors.
2. **Soundness**: the asserted property is true for generated inputs.
3. **Fault detection**: the test kills realistic source-code mutants.

The central finding so far is that high validity and soundness do not guarantee
strong fault detection. Mutation testing exposes missing edge cases, overly broad
properties, oracle coupling, and adapter tests that preserve round trips while
ignoring API options.

## Experimental Design

Each target API is evaluated with one or more Hypothesis test suites:

| Suite | Description |
|---|---|
| Human-written | Hand-designed strategies and invariants. |
| Codex-generated | Codex 5.5 Medium tests for selected APIs|
| Gemini-generated | Gemini 5.5 Thinking tests for selected APIs |

The execution harness in [`metrics.py`](./metrics.py) repeatedly runs each test
function and records validity and soundness. Mutation testing uses `mutmut` with
covered-line filtering so that mutants are generated from source lines reached
by the selected wrapper tests.

## Evaluated APIs

| Library | Version / source | APIs evaluated |
|---|---|---|
| NumPy | `2.2.6` | `np.add`, `np.sum`, `np.cumsum`, `np.dot`, `np.linalg.norm` |
| PyTorch | `2.7.0` | `torch.argmax` |
| Python `statistics` | Python `3.12.7` | `mean`, `geometric_mean`, `correlation`, `linear_regression`, `median`, `variance` |
| Python `html` | Python `3.12.7` | `escape`, `unescape` |
| Python `zlib` | zlib `1.2.13` | `compress`, `decompress`, `adler32` |
| Python `decimal` | Python `3.12.7` | `Decimal.as_integer_ratio`, `compare`, `fma`, `from_float`, `quantize` |
| python-dateutil | `2.9.0.post0` | `dateutil.parser.isoparse`, `dateutil.parser.parse` |

For `zlib`, mutation testing targets a Python adapter around the compiled C
extension. For `decimal`, mutation testing uses the pure-Python `_pydecimal.py`
implementation copied as `decimal.py`, because the installed top-level module
delegates primarily to the compiled `_decimal` extension.

## Quantitative Results

Validity and soundness measure whether tests run and assert true properties.
They do not measure how many implementation faults the tests detect.

| API group | Human validity | Human soundness | Codex validity | Codex soundness |
|---|---:|---:|---:|---:|
| NumPy `linspace` baseline | 100.0% | 66.7% | 100.0% | 100.0% |
| PyTorch `argmax` baseline | 99.0% | 100.0% | 100.0% | 100.0% |
| `statistics` average | 77.8% | 68.2% | 100.0% | 100.0% |
| `html` average | 70.8% | 83.3% | 100.0% | 100.0% |
| `zlib` average | 88.9% | 100.0% | 100.0% | 100.0% |
| `decimal` average | 100.0% | 100.0% | 100.0% | 100.0% |
| `dateutil` average | 83.3% | 100.0% | 100.0% | 100.0% |

Detailed per-function validity and soundness values are encoded in
[`result_plot.py`](./result_plot.py).

## Mutation Testing Results

Mutation score is `killed_mutants / total_mutants`. Covered mutation score is
`killed_mutants / (total_mutants - untested_mutants)`.

| Library / target | Test suite | Total mutants | Killed | Survived | Untested | Mutation score | Covered score |
|---|---|---:|---:|---:|---:|---:|---:|
| NumPy | Human-written | 99 | 26 | 28 | 0 | 26.3% | 26.3% |
| NumPy | Codex-generated | 122 | 72 | 49 | 0 | 59.0% | 59.0% |
| NumPy | Gemini-generated | 122 | 65 | 56 | 0 | 53.3% | 53.3% |
| dateutil | Human-written | 973 | 366 | 591 | 6 | 37.6% | 37.8% |
| dateutil | Codex-generated | 1,178 | 777 | 388 | 0 | 66.0% | 66.0% |
| dateutil | Gemini-generated | 816 | 333 | 481 | 0 | 40.8% | 40.8% |
| statistics | Human-written | 270 | 204 | 53 | 13 | 75.6% | 79.4% |
| statistics | Codex-generated | 290 | 226 | 51 | 13 | 77.9% | 81.6% |
| html | Human-written | 92 | 73 | 19 | 0 | 79.3% | 79.3% |
| html | Codex-generated | 85 | 73 | 12 | 0 | 85.9% | 85.9% |
| zlib adapter | Human-written | 17 | 12 | 5 | 0 | 70.6% | 70.6% |
| zlib adapter | Codex-generated | 17 | 14 | 3 | 0 | 82.4% | 82.4% |
| decimal | Human-written | 900 | 522 | 371 | 0 | 58.0% | 58.0% |
| decimal | Codex-generated | 1,128 | 641 | 481 | 0 | 56.8% | 56.8% |
| decimal | Gemini-generated | 1,128 | 665 | 456 | 4 | 59.0% | 59.2% |



## Survivor Analyses

Survivor reports classify remaining mutants by confidence and identify targeted
properties that would most directly kill high-signal survivors.

| Suite | Library | Survivor report |
|---|---|---|
| Codex | NumPy | [`survived_mutants_codex_numpy.md`](./Codex/np_testing/codex_np_mutation_testing/survived_mutants_codex_numpy.md) |
| Gemini | NumPy | [`survived_mutants_gemini_np.md`](./Gemini/np/gemini_np_mutation_testing/survived_mutants_gemini_np.md) |
| Codex | dateutil | [`survived_mutants_codex_dateutil.md`](./Codex/dateutil_testing/codex_dateutil_mutation_test/survived_mutants_codex_dateutil.md) |
| Gemini | dateutil | [`survived_mutants_gemini_dateutil.md`](./Gemini/dateutil/gemini_dateutil_mutation_test/survived_mutants_gemini_dateutil.md) |
| Codex | statistics | [`survived_mutations_statistics.md`](./Codex/statistics/codex_statistics_mutation_testing/survived_mutations_statistics.md) |
| Codex | html | [`survived_mutants_html.md`](./Codex/html/codex_html_mutation_testing/survived_mutants_html.md) |
| Codex | zlib adapter | [`survived_mutants_zlib.md`](./Codex/zlib/codex_zlib_mutation_testing/survived_mutants_zlib.md) |
| Codex | decimal | [`survived_mutants_codex_decimal.md`](./Codex/decimal/codex_decimal_mutation_tests/survived_mutants_codex_decimal.md) |
| Gemini | decimal | [`survived_mutants_gemini_decimal.md`](./Gemini/decimal/gemini_decimal_mutation_tests/survived_mutants_gemini_decimal.md) |

## Repository Map

| Path | Contents |
|---|---|
| [`human_PBT/`](./human_PBT) | Human-written PBT suites and mutation wrappers. |
| [`Codex/`](./Codex) | Codex-generated tests, mutation wrappers, and survivor reports. |
| [`Gemini/`](./Gemini) | Gemini-generated tests, mutation wrappers, and survivor reports. |
| [`metrics.py`](./metrics.py) | Validity and soundness evaluation harness. |
| [`mutation_testing_results.py`](./mutation_testing_results.py) | Mutation-testing result dictionaries and score calculation. |
| [`result_plot.py`](./result_plot.py) | Result aggregation and plotting data. |
| [`two_staged_prompt.py`](./two_staged_prompt.py) | Prompt templates used for Codex property extraction and test generation. |

Mutation-testing directories contain copied source trees and `mutants/`
directories produced by `mutmut`. Generated cache directories such as
`__pycache__`, `.pytest_cache`, and `.hypothesis` are not part of the research
artifacts and can be removed safely.

## Reproducing Mutation Runs

Run mutation tests from the relevant mutation-testing directory. For example:

```bash
cd Codex/np_testing/codex_np_mutation_testing
mutmut run
mutmut results
mutmut browse
```

The `setup.cfg` in each mutation directory defines:

- `paths_to_mutate`: source files that mutmut mutates.
- `also_copy`: source packages copied into the isolated mutants workspace.
- `pytest_add_cli_args_test_selection`: wrapper tests selected for that run.

For NumPy, test selection is explicit rather than `.` so pytest does not collect
NumPy's internal copied test suite under the mutation workspace.
