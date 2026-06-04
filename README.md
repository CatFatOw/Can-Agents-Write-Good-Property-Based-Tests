# Can Agents Write Good Property-Based Tests Via Documentation?

Research for the Carnegie Mellon University (CMU) REU program by Michael Wu, May 2026.

This repository studies whether a modern coding agent can produce useful
property-based tests (PBTs) for real Python APIs. The experiment is inspired by
the paper [Can Large Language Models Write Good Property-Based Tests?](https://doi.org/10.48550/arXiv.2307.04346)
and adapts its prompt-driven workflow to a Codex-style coding agent.

The central comparison is between:

- human-written Hypothesis tests with hand-designed invariants and strategies
- Codex-generated Hypothesis tests produced from API documentation and two-staged prompts

## Mutation Analysis

The main mutation-testing takeaway is that perfect validity and soundness do
not imply strong fault detection. Mutation testing exposes where the generated
properties are too broad, where edge cases are missing, and where wrappers pass
round-trip checks while still ignoring API options.

Detailed Codex survivor reports:

| Library | Codex mutation score | Covered mutation score | Survivor analysis |
|---|---:|---:|---|
| `dateutil` | 66.0% | 66.0% | [`survived_mutants_dateutil.md`](./Codex/dateutil_testing/codex_dateutil_mutation_test/survived_mutants_dateutil.md) |
| `statistics` | 77.9% | 81.6% | [`survived_mutations_statistics.md`](./Codex/statistics/codex_statistics_mutation_testing/survived_mutations_statistics.md) |
| `html` | 85.9% | 85.9% | [`survived_mutants_html.md`](./Codex/html/codex_html_mutation_testing/survived_mutants_html.md) |
| `zlib` adapter | 82.4% | 82.4% | [`survived_mutants_zlib.md`](./Codex/zlib/codex_zlib_mutation_testing/survived_mutants_zlib.md) |
| `decimal` | 56.8% | 56.8% | [`survived_mutants_decimal.md`](./Codex/decimal/codex_decimal_mutation_tests/survived_mutants_decimal.md) |

The reports classify survived mutants by confidence and highlight high-signal
survivors that should guide the next round of targeted property improvements.

## Tested Libraries

| Library | Version | APIs evaluated |
|---|---:|---|
| NumPy | `2.2.6` | `np.linspace()` |
| PyTorch | `2.7.0` | `torch.argmax()` |
| python-statistics | `3.12.7` | `statistics.mean()`, `statistics.geometric_mean()`, `statistics.correlation()`, `statistics.linear_regression()`, `statistics.median()`, `statistics.variance()` |
| python-html | `3.12.7` | `html.escape()`, `html.unescape()` |
| zlib | `1.2.13` | `zlib.compress()`, `zlib.decompress()`, `zlib.adler32()` |
| python-decimal | `3.12.7` | `Decimal.as_integer_ratio()`, `Decimal.compare()`, `Decimal.fma()`, `Decimal.from_float()`, `Decimal.quantize()` |
| python-dateutil | `2.9.0.post0` | `dateutil.parser.isoparse()`, `dateutil.parser.parse()` |

## Methodology

Each API is evaluated with a small human-written PBT suite and a Codex-generated
PBT suite. The Codex tests are produced using the prompt templates in
[`two_staged_prompt.py`](./two_staged_prompt.py), which ask the model to extract
properties from documentation and then implement Hypothesis tests for those
properties.

The evaluation harness in [`metrics.py`](./metrics.py) runs each test function
1,000 times and reports two execution metrics:

- **Validity**: fraction of executions that do not raise unexpected exceptions.
- **Soundness**: fraction of executions that do not fail an assertion.
- **Mutation Score/Coverage**: killed/total mutations or kill / (total-untested)

In this setup, validity failures usually indicate malformed strategies,
unhandled parser errors, or runtime exceptions. Soundness failures indicate that
the asserted property is false for at least some generated inputs.

The additional **mutation score** metric is the fraction of generated mutants
killed by a test suite. Mutation testing is currently recorded for the
dateutil parser APIs, the Python statistics, html, and decimal libraries, zlib, and `np.linspace()` in
[`mutation_testing_results.py`](./mutation_testing_results.py). The covered
mutation score reports the fraction of tested mutants killed after excluding
untested mutants. The mutation runs use covered-line filtering so mutants are
generated from source lines reached by the selected API wrappers rather than
from every function in each vendored library.

Python's `zlib` module is a compiled C extension, so its `mutmut` results apply
to the selected Python adapter functions rather than direct mutations of the
underlying zlib C implementation.

For Decimal mutation testing, the mutation directories use Python's pure-Python
`_pydecimal.py` implementation copied as `decimal.py`, because the installed
top-level `decimal.py` primarily delegates to the compiled `_decimal` extension.

## Test Artifacts

| API | Human-written test | Codex-generated test | Documentation |
|---|---|---|---|
| `np.linspace()` | [`human_test_np_linspace.py`](./human_PBT/np_testing/human_test_np_linspace.py) | [`test_codex_np_linspace.py`](./Codex/np_testing/test_codex_np_linspace.py) | [NumPy `linspace`](https://numpy.org/doc/2.3/reference/generated/numpy.linspace.html) |
| `torch.argmax()` | [`human_test_torch_argmax.py`](./human_PBT/torch_testing/human_test_torch_argmax.py) | [`test_codex_torch_argmax.py`](./Codex/torch_testing/test_codex_torch_argmax.py) | [PyTorch `argmax`](https://docs.pytorch.org/docs/2.12/generated/torch.argmax.html) |
| `statistics.mean()` | [`human_test_statistics_mean.py`](./human_PBT/statistics/human_test_statistics_mean.py) | [`test_codex_statistics_mean.py`](./Codex/statistics/test_codex_statistics_mean.py) | [Python `statistics.mean`](https://docs.python.org/3.12/library/statistics.html#statistics.mean) |
| `statistics.geometric_mean()` | [`human_test_statistics_geometric_mean.py`](./human_PBT/statistics/human_test_statistics_geometric_mean.py) | [`test_codex_statistics_geometric_mean.py`](./Codex/statistics/test_codex_statistics_geometric_mean.py) | [Python `statistics.geometric_mean`](https://docs.python.org/3.12/library/statistics.html#statistics.geometric_mean) |
| `statistics.correlation()` | [`test_human_test_statistics_correlation.py`](./human_PBT/statistics/test_human_test_statistics_correlation.py) | [`test_codex_statistics_correlation.py`](./Codex/statistics/test_codex_statistics_correlation.py) | [Python `statistics.correlation`](https://docs.python.org/3.12/library/statistics.html#statistics.correlation) |
| `statistics.linear_regression()` | [`test_human_test_statistics_linear_regression.py`](./human_PBT/statistics/test_human_test_statistics_linear_regression.py) | [`test_codex_statistics_linear_regression.py`](./Codex/statistics/test_codex_statistics_linear_regression.py) | [Python `statistics.linear_regression`](https://docs.python.org/3.12/library/statistics.html#statistics.linear_regression) |
| `statistics.median()` | [`test_human_test_statistics_median.py`](./human_PBT/statistics/test_human_test_statistics_median.py) | [`test_codex_statistics_median.py`](./Codex/statistics/test_codex_statistics_median.py) | [Python `statistics.median`](https://docs.python.org/3.12/library/statistics.html#statistics.median) |
| `statistics.variance()` | [`test_human_test_statistics_variance.py`](./human_PBT/statistics/test_human_test_statistics_variance.py) | [`test_codex_statistics_variance.py`](./Codex/statistics/test_codex_statistics_variance.py) | [Python `statistics.variance`](https://docs.python.org/3.12/library/statistics.html#statistics.variance) |
| `html.escape()` | [`test_human_html_escape.py`](./human_PBT/html/test_human_html_escape.py) | [`test_codex_html_escape.py`](./Codex/html/test_codex_html_escape.py) | [Python `html.escape`](https://docs.python.org/3.12/library/html.html#html.escape) |
| `html.unescape()` | [`test_human_html_unescape.py`](./human_PBT/html/test_human_html_unescape.py) | [`test_codex_html_unescape.py`](./Codex/html/test_codex_html_unescape.py) | [Python `html.unescape`](https://docs.python.org/3.12/library/html.html#html.unescape) |
| `zlib.compress()` | [`test_human_zlib_compress.py`](./human_PBT/zlib/test_human_zlib_compress.py) | [`test_codex_zlib_compress.py`](./Codex/zlib/test_codex_zlib_compress.py) | [Python `zlib.compress`](https://docs.python.org/3.12/library/zlib.html#zlib.compress) |
| `zlib.decompress()` | [`test_human_zlib_decompress.py`](./human_PBT/zlib/test_human_zlib_decompress.py) | [`test_codex_zlib_decompress.py`](./Codex/zlib/test_codex_zlib_decompress.py) | [Python `zlib.decompress`](https://docs.python.org/3.12/library/zlib.html#zlib.decompress) |
| `zlib.adler32()` | [`test_human_zlib_adler32.py`](./human_PBT/zlib/test_human_zlib_adler32.py) | [`test_codex_zlib_adler32.py`](./Codex/zlib/test_codex_zlib_adler32.py) | [Python `zlib.adler32`](https://docs.python.org/3.12/library/zlib.html#zlib.adler32) |
| `Decimal.as_integer_ratio()` | [`test_human_decimal_as_integer_ratio.py`](./human_PBT/decimal/test_human_decimal_as_integer_ratio.py) | [`test_codex_decimal_as_integer_ratio.py`](./Codex/decimal/test_codex_decimal_as_integer_ratio.py) | [Python `Decimal.as_integer_ratio`](https://docs.python.org/3.12/library/decimal.html#decimal.Decimal.as_integer_ratio) |
| `Decimal.compare()` | [`test_human_decimal_compare.py`](./human_PBT/decimal/test_human_decimal_compare.py) | [`test_codex_decimal_compare.py`](./Codex/decimal/test_codex_decimal_compare.py) | [Python `Decimal.compare`](https://docs.python.org/3.12/library/decimal.html#decimal.Decimal.compare) |
| `Decimal.fma()` | [`test_human_decimal_fma.py`](./human_PBT/decimal/test_human_decimal_fma.py) | [`test_codex_decimal_fma.py`](./Codex/decimal/test_codex_decimal_fma.py) | [Python `Decimal.fma`](https://docs.python.org/3.12/library/decimal.html#decimal.Decimal.fma) |
| `Decimal.from_float()` | [`test_human_decimal_from_float.py`](./human_PBT/decimal/test_human_decimal_from_float.py) | [`test_codex_decimal_from_float.py`](./Codex/decimal/test_codex_decimal_from_float.py) | [Python `Decimal.from_float`](https://docs.python.org/3.12/library/decimal.html#decimal.Decimal.from_float) |
| `Decimal.quantize()` | [`test_human_decimal_quantized.py`](./human_PBT/decimal/test_human_decimal_quantized.py) | [`test_codex_decimal_quantize.py`](./Codex/decimal/test_codex_decimal_quantize.py) | [Python `Decimal.quantize`](https://docs.python.org/3.12/library/decimal.html#decimal.Decimal.quantize) |
| `dateutil.parser.isoparse()` | [`human_testing_isoparse.py`](./human_PBT/dateutil_testing/human_testing_isoparse.py) | [`test_codex_isoparse.py`](./Codex/dateutil_testing/test_codex_isoparse.py) | [`dateutil.parser.isoparse`](https://dateutil.readthedocs.io/en/stable/parser.html#dateutil.parser.isoparse) |
| `dateutil.parser.parse()` | [`human_testing_parser.py`](./human_PBT/dateutil_testing/human_testing_parser.py) | [`test_codex_parse.py`](./Codex/dateutil_testing/test_codex_parse.py) | [`dateutil.parser.parse`](https://dateutil.readthedocs.io/en/stable/parser.html#dateutil.parser.parse) |

## Quantitative Results

| API | Human validity | Human soundness | Codex validity | Codex soundness |
|---|---:|---:|---:|---:|
| `np.linspace()` | 100.0% | 66.7% | 100.0% | 100.0% |
| `torch.argmax()` | 99.0% | 100.0% | 100.0% | 100.0% |
| `statistics.mean()` | 75.0% | 50.0% | 100.0% | 100.0% |
| `statistics.geometric_mean()` | 50.0% | 75.0% | 100.0% | 100.0% |
| `statistics.correlation()` | 75.0% | 50.0% | 100.0% | 100.0% |
| `statistics.linear_regression()` | 100.0% | 67.4% | 100.0% | 100.0% |
| `statistics.median()` | 66.7% | 100.0% | 100.0% | 100.0% |
| `statistics.variance()` | 100.0% | 66.7% | 100.0% | 100.0% |
| **statistics average** | **77.8%** | **68.2%** | **100.0%** | **100.0%** |
| `html.escape()` | 75.0% | 100.0% | 100.0% | 100.0% |
| `html.unescape()` | 66.7% | 66.7% | 100.0% | 100.0% |
| **html average** | **70.8%** | **83.3%** | **100.0%** | **100.0%** |
| `zlib.compress()` | 66.7% | 100.0% | 100.0% | 100.0% |
| `zlib.decompress()` | 100.0% | 100.0% | 100.0% | 100.0% |
| `zlib.adler32()` | 100.0% | 100.0% | 100.0% | 100.0% |
| **zlib average** | **88.9%** | **100.0%** | **100.0%** | **100.0%** |
| `Decimal.as_integer_ratio()` | 100.0% | 100.0% | 100.0% | 100.0% |
| `Decimal.compare()` | 100.0% | 100.0% | 100.0% | 100.0% |
| `Decimal.fma()` | 100.0% | 100.0% | 100.0% | 100.0% |
| `Decimal.from_float()` | 100.0% | 100.0% | 100.0% | 100.0% |
| `Decimal.quantize()` | 100.0% | 100.0% | 100.0% | 100.0% |
| **decimal average** | **100.0%** | **100.0%** | **100.0%** | **100.0%** |
| `dateutil.parser.isoparse()` | 100.0% | 100.0% | 100.0% | 100.0% |
| `dateutil.parser.parse()` | 66.7% | 100.0% | 100.0% | 100.0% |
| **dateutil average** | **83.3%** | **100.0%** | **100.0%** | **100.0%** |

## Mutation Testing Results

The table below gives the aggregate mutation metrics. The linked survivor
reports above explain what the remaining Codex survivors mean and which test
properties would most directly kill them.

| API | Test suite | Total mutants | Killed mutants | Untested mutants | Mutation score | Covered mutation score |
|---|---|---:|---:|---:|---:|---:|
| `np` | Human-written | 141 | 50 | 0 | 35.5% | 35.5% |
| `np` | Codex-generated | 141 | 50 | 0 | 35.5% | 35.5% |
| `dateutil` | Human-written | 973 | 366 | 6 | 37.6% | 37.8% |
| `dateutil` | Codex-generated | 1,178 | 777 | 0 | 66.0% | 66.0% |
| `statistics` | Human-written | 270 | 204 | 13 | 75.6% | 79.4% |
| `statistics` | Codex-generated | 290 | 226 | 13 | 77.9% | 81.6% |
| `html` | Human-written | 92 | 73 | 0 | 79.3% | 79.3% |
| `html` | Codex-generated | 85 | 73 | 0 | 85.9% | 85.9% |
| `zlib` adapter | Human-written | 17 | 12 | 0 | 70.6% | 70.6% |
| `zlib` adapter | Codex-generated | 17 | 14 | 0 | 82.4% | 82.4% |
| `decimal` | Human-written | 900 | 522 | 0 | 58.0% | 58.0% |
| `decimal` | Codex-generated | 1,128 | 641 | 0 | 56.8% | 56.8% |


## Figures

### Baseline From Prior Work

<p align="center">
  <img src="./graphs/previous_paper_results.png" width="650" alt="Results from the prior LLM property-based testing paper">
</p>

The figure above reproduces the earlier paper's reported results for historical
comparison. The remaining figures show the local agent-vs-human evaluations in
this repository.

### NumPy and PyTorch

<p align="center">
  <img src="./graphs/np_linspace_data.png" width="360" alt="Property-based test evaluation for np.linspace">
  <img src="./graphs/torch_argmax_data.png" width="360" alt="Property-based test evaluation for torch.argmax">
</p>

### Statistics APIs

<p align="center">
  <img src="./graphs/statistic_mean_data.png" width="360" alt="Property-based test evaluation for statistics.mean">
  <img src="./graphs/statistic_geometric_mean_data.png" width="360" alt="Property-based test evaluation for statistics.geometric_mean">
</p>
<p align="center">
  <img src="./graphs/statistics_correlation_data.png" width="360" alt="Property-based test evaluation for statistics.correlation">
  <img src="./graphs/statistics_linearregression_data.png" width="360" alt="Property-based test evaluation for statistics.linear_regression">
</p>

<p align="center">
  <img src="./graphs/statistics_median_data.png" width="360" alt="Property-based test evaluation for statistics.median">
  <img src="./graphs/statistics_data_variance.png" width="360" alt="Property-based test evaluation for statistics.variance">
</p>

<p align="center">
  <img src="./graphs/avg_stats_api_data.png" width="480" alt="Average property-based test evaluation for statistics APIs">
</p>

### HTML APIs

<p align="center">
  <img src="./graphs/html_escape_data.png" width="360" alt="Property-based test evaluation for html.escape">
  <img src="./graphs/html_unescape_data.png" width="360" alt="Property-based test evaluation for html.unescape">
</p>

<p align="center">
  <img src="./graphs/avg_html_metrics_data.png" width="480" alt="Average property-based test evaluation for html APIs">
</p>

### Zlib APIs

<p align="center">
  <img src="./graphs/zlib_compress_data.png" width="360" alt="Property-based test evaluation for zlib.compress">
  <img src="./graphs/zlib_decompress_data.png" width="360" alt="Property-based test evaluation for zlib.decompress">
</p>

<p align="center">
  <img src="./graphs/zlib_adler32_data.png" width="360" alt="Property-based test evaluation for zlib.adler32">
</p>

<p align="center">
  <img src="./graphs/avg_zlib_data.png" width="480" alt="Average property-based test evaluation for zlib APIs">
</p>

### Decimal APIs

<p align="center">
  <img src="./graphs/decimal_integer_ratio_data.png" width="360" alt="Property-based test evaluation for Decimal.as_integer_ratio">
  <img src="./graphs/decimal_compare_data.png" width="360" alt="Property-based test evaluation for Decimal.compare">
</p>

<p align="center">
  <img src="./graphs/decimal_fma_data.png" width="360" alt="Property-based test evaluation for Decimal.fma">
  <img src="./graphs/decimal_from_float_data.png" width="360" alt="Property-based test evaluation for Decimal.from_float">
</p>

<p align="center">
  <img src="./graphs/decimal_quantize_data.png" width="360" alt="Property-based test evaluation for Decimal.quantize">
</p>

### Dateutil Parser APIs

<p align="center">
  <img src="./graphs/parser_isoparse_data_dateutil.png" width="330" alt="Property-based test evaluation for dateutil.parser.isoparse">
  <img src="./graphs/parse_dateutil_data.png" width="330" alt="Property-based test evaluation for dateutil.parser.parse">
</p>

<p align="center">
  <img src="./graphs/avg_PBT_dateutil_data.png" width="480" alt="Average property-based test evaluation for dateutil parser APIs">
</p>


## Reproducing Results

From this directory:

```bash
python Codex/np_testing/test_codex_np_linspace.py
python Codex/torch_testing/test_codex_torch_argmax.py
python Codex/statistics/test_codex_statistics_mean.py
python Codex/statistics/test_codex_statistics_geometric_mean.py
python Codex/statistics/test_codex_statistics_correlation.py
python Codex/statistics/test_codex_statistics_linear_regression.py
python Codex/statistics/test_codex_statistics_median.py
python Codex/statistics/test_codex_statistics_variance.py
python Codex/html/test_codex_html_escape.py
python Codex/html/test_codex_html_unescape.py
python Codex/zlib/test_codex_zlib_compress.py
python Codex/zlib/test_codex_zlib_decompress.py
python Codex/zlib/test_codex_zlib_adler32.py
python Codex/decimal/test_codex_decimal_as_integer_ratio.py
python Codex/decimal/test_codex_decimal_compare.py
python Codex/decimal/test_codex_decimal_fma.py
python Codex/decimal/test_codex_decimal_from_float.py
python Codex/decimal/test_codex_decimal_quantize.py
python Codex/dateutil_testing/test_codex_isoparse.py
python Codex/dateutil_testing/test_codex_parse.py
python mutation_testing_results.py
python result_plot.py
```

The graph images are stored in [`graphs/`](./graphs/). The plotting script
contains the recorded metric dictionaries used to generate the figures.
