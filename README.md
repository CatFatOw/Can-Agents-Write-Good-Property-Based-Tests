# Can Agents Write Good Property-Based Tests?

Project for the Carnegie Mellon University (CMU) REU program by Michael Wu, May 2026.

This repository studies whether a modern coding agent can produce useful
property-based tests (PBTs) for real Python APIs. The experiment is inspired by
the paper [Can Large Language Models Write Good Property-Based Tests?](https://doi.org/10.48550/arXiv.2307.04346)
and adapts its prompt-driven workflow to a Codex-style coding agent.

The central comparison is between:

- human-written Hypothesis tests with hand-designed invariants and strategies
- Codex-generated Hypothesis tests produced from API documentation and two-staged prompts

## Tested Libraries

| Library | Version | APIs evaluated |
|---|---:|---|
| NumPy | `2.2.6` | `np.linspace()` |
| PyTorch | `2.7.0` | `torch.argmax()` |
| python-statistics | `3.12.7` | `statistics.mean()`, `statistics.geometric_mean()`, `statistics.correlation()`, `statistics.linear_regression()`, `statistics.median()`, `statistics.variance()` |
| python-html | `3.12.7` | `html.escape()`, `html.unescape()` |
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
dateutil parser APIs, the Python statistics and html libraries, and `np.linspace()` in
[`mutation_testing_results.py`](./mutation_testing_results.py). The covered
mutation score reports the fraction of tested mutants killed after excluding
untested mutants. The mutation runs use covered-line filtering so mutants are
generated from source lines reached by the selected API wrappers rather than
from every function in each vendored library.

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
| `dateutil.parser.isoparse()` | 100.0% | 100.0% | 100.0% | 100.0% |
| `dateutil.parser.parse()` | 66.7% | 100.0% | 100.0% | 100.0% |
| **dateutil average** | **83.3%** | **100.0%** | **100.0%** | **100.0%** |

## Mutation Testing Results

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
python Codex/dateutil_testing/test_codex_isoparse.py
python Codex/dateutil_testing/test_codex_parse.py
python mutation_testing_results.py
python result_plot.py
```

The graph images are stored in [`graphs/`](./graphs/). The plotting script
contains the recorded metric dictionaries used to generate the figures.
