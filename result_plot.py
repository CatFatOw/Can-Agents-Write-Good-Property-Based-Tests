import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np

# np linspace
human_linspace = {'validity': 1.0, 'soundness': 0.6666666666666666, 'validity_errors': [], 'soundness_errors': ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']}
codex_linspace = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': [], 'soundness_errors': []}

# torch argmax
human_argmax = {'validity': 0.99, 'soundness': 1.0, 'validity_errors': ['FlakyFailure'], 'soundness_errors': []}
codex_argmax = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': [], 'soundness_errors': []}

# dateutil isoparse

human_isoparse = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}
codex_isoparse = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}
# Second prompt fixed 
gemini_isoparse = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}

# dateutil.parser.parse
human_parse = {'validity': 0.6666666666666666, 'soundness': 1.0, 'validity_errors': {'ParserError'}, 'soundness_errors': set()}
codex_parse = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}
gemini_parse = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}
# Compute the dateutil avg metrics
avg_human_dateutil = {"validity": (human_parse["validity"] + human_isoparse["validity"])/2, "soundness": (human_parse["soundness"] + human_isoparse["soundness"])/2}
avg_codex_dateutil = {"validity": (codex_parse["validity"] + codex_isoparse["validity"])/2, "soundness": (codex_parse["soundness"] + codex_isoparse["soundness"])/2}

# Statistics mean()
human_mean = {'validity': 0.75, 'soundness': 0.5, 'validity_errors': {'ZeroDivisionError'}, 'soundness_errors': {''}}
codex_mean = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}
VIM_mean = {'validity': 0.8333333333333334, 'soundness': 0.8333333333333334, 'validity_errors': {'FailedHealthCheck'}, 'soundness_errors': {''}}

# Statistics geometric mean()
human_geometric_mean = {'validity': 0.5, 'soundness': 0.75, 'validity_errors': {'ExceptionGroup', 'NameError'}, 'soundness_errors': {''}}
codex_geometric_mean = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}
VIM_geometric_mean = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}

# Statistics correlation()
human_correlation = {'validity': 0.75, 'soundness': 0.5, 'validity_errors': {'FailedHealthCheck'}, 'soundness_errors': {''}}
codex_correlation = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}

# Statistics linear_regression
human_linear_regression = {'validity': 1.0, 'soundness': 0.6743333333333333, 'validity_errors': set(), 'soundness_errors': {''}}
codex_linear_regression = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}

# Statistics Median
human_median = {'validity': 0.6666666666666666, 'soundness': 1.0, 'validity_errors': {'ExceptionGroup'}, 'soundness_errors': set()}
codex_median = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}

# Statistics Variance 
human_variance = {'validity': 1.0, 'soundness': 0.6666666666666666, 'validity_errors': set(), 'soundness_errors': {''}}
codex_variance = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}


avg_human_statistics = {
    "validity": (
        human_mean["validity"] +
        human_geometric_mean["validity"] +
        human_correlation["validity"] +
        human_linear_regression["validity"] +
        human_median["validity"] +
        human_variance["validity"]
    ) / 6,

    "soundness": (
        human_mean["soundness"] +
        human_geometric_mean["soundness"] +
        human_correlation["soundness"] +
        human_linear_regression["soundness"] +
        human_median["soundness"] +
        human_variance["soundness"]
    ) / 6,
}

avg_codex_statistics = {
    "validity": (
        codex_mean["validity"] +
        codex_geometric_mean["validity"] +
        codex_correlation["validity"] +
        codex_linear_regression["validity"] +
        codex_median["validity"] +
        codex_variance["validity"]
    ) / 6,

    "soundness": (
        codex_mean["soundness"] +
        codex_geometric_mean["soundness"] +
        codex_correlation["soundness"] +
        codex_linear_regression["soundness"] +
        codex_median["soundness"] +
        codex_variance["soundness"]
    ) / 6,
}


# HTML 

# html Escape 
human_escape = {'validity': 0.75, 'soundness': 1.0, 'validity_errors': {'AttributeError'}, 'soundness_errors': set()}
codex_escape = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}


# Html unescape 
human_unescape = {'validity': 0.6666666666666666, 'soundness': 0.6666666666666666, 'validity_errors': {'ExceptionGroup'}, 'soundness_errors': {''}}
codex_unescape = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}

avg_human_html = {
    "validity": (human_escape["validity"] + human_unescape["validity"]) / 2,
    "soundness": (human_escape["soundness"] + human_unescape["soundness"]) / 2,
}

avg_codex_html = {
    "validity": (codex_escape["validity"] + codex_unescape["validity"]) / 2,
    "soundness": (codex_escape["soundness"] + codex_unescape["soundness"]) / 2,
}

# ZLIB compress
# HUMAN
human_compress = {'validity': 0.6666666666666666, 'soundness': 1.0, 'validity_errors': {'error'}, 'soundness_errors': set()}
codex_compress = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}

# ZLIB decompress
human_decompress = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}
codex_decompress = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}


# Zlib adler 32
human_adler32 = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}
codex_adler32 = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}


avg_human_zlib = {
    "validity": (human_compress["validity"] + human_decompress["validity"] + human_adler32["validity"]) / 3,
    "soundness": (human_compress["soundness"] + human_decompress["soundness"] + human_adler32["validity"]) / 3,
}

avg_codex_zlib = {
    "validity": (codex_compress["validity"] + codex_decompress["validity"] + codex_adler32["validity"]) / 3,
    "soundness": (codex_compress["soundness"] + codex_decompress["soundness"] + codex_adler32["validity"]) / 3,
}

# DECIMAL LIBRARY

# decimal as_integer_ratio()
human_as_integer_ratio = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}
codex_as_integer_ratio = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}
# 2nd Prompt fix
gemini_as_integer_ratio = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}

# Decimal compare()
human_compare = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}
codex_compare = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}
gemini_compare = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}

# Decimal fma 
human_fma = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}
codex_fma = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}
gemini_fma = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}
# Decimal from_float
human_from_float = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}
codex_from_float = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}
gemini_from_float = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}

# Decimal Quantize 
human_quantize = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}
codex_quantize = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}
gemini_quantize = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}

# Numpy

# Numpy add
human_np_add = {'validity': 0.6666666666666666, 'soundness': 1.0, 'validity_errors': {'TypeError'}, 'soundness_errors': set()}
codex_np_add = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}
gemini_np_add = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}

# Numpy cumsum
human_np_cumsum = {'validity': 0.6666666666666666, 'soundness': 1.0, 'validity_errors': {'ValueError'}, 'soundness_errors': set()}
codex_np_cumsum = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}
gemini_np_cumsum = {'validity': 1.0, 'soundness': 0.15000000000000002, 'validity_errors': set(), 'soundness_errors': {'\nNot equal to tolerance rtol=0.0001, atol=0.0001\n\nMismatched elements: 1 / 17 (5.88%)\nMax absolute difference among violations: 0.00016275\nMax relative difference among violations: 0.00048825\n ACTUAL: array([256.      , 256.      , 256.      , 256.      , 256.      ,\n       256.      , 256.      , 256.      , 256.      , 256.      ,\n       256.      , 256.      , 256.      , 256.      , 256.      ,\n         0.333496, 256.      ], dtype=float32)\n DESIRED: array([256.      , 256.      , 256.      , 256.      , 256.      ,\n       256.      , 256.      , 256.      , 256.      , 256.      ,\n       256.      , 256.      , 256.      , 256.      , 256.      ,\n         0.333333, 256.      ], dtype=float32)'}}


# Numpy dot
human_np_dot = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}
codex_np_dot = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}


# Numpy linalg.norm()
human_linalg_norm = {'validity': 0.6666666666666666, 'soundness': 1.0, 'validity_errors': {'ExceptionGroup'}, 'soundness_errors': set()}
codex_linalg_norm = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}


# Numpy sum
human_np_sum = {'validity': 0.6666666666666666, 'soundness': 0.3333333333333333, 'validity_errors': {'TypeError'}, 'soundness_errors': {''}}
codex_np_sum = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}
gemini_np_sum = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}

def plot_pbt_results(human_results, agent_results, api_name, agent_name="Codex"):
    models = ["Human", agent_name]

    validity_scores = [
        human_results["validity"] * 100,
        agent_results["validity"] * 100
    ]

    soundness_scores = [
        human_results["soundness"] * 100,
        agent_results["soundness"] * 100
    ]

    x = np.arange(len(models))
    width = 0.35

    plt.figure(figsize=(8, 5))

    validity_bars = plt.bar(
        x - width / 2,
        validity_scores,
        width,
        label="Validity"
    )

    soundness_bars = plt.bar(
        x + width / 2,
        soundness_scores,
        width,
        label="Soundness"
    )

    # Add percentage labels above bars
    plt.bar_label(
        validity_bars,
        fmt="%.1f%%",
        padding=3
    )

    plt.bar_label(
        soundness_bars,
        fmt="%.1f%%",
        padding=3
    )

    plt.xticks(x, models)

    plt.ylim(0, 110)

    plt.ylabel("Percentage (%)")

    plt.title(f"Property-Based Test Evaluation for {api_name}")

    plt.legend()

    plt.show()


# Plots the vim results also
def plot_pbt_results_three(
    human_results,
    agent_results,
    vim_results,
    api_name,
    agent_name="Codex",
    vim_name="VIM"
):
    models = ["Human", agent_name, vim_name]

    validity_scores = [
        human_results["validity"] * 100,
        agent_results["validity"] * 100,
        vim_results["validity"] * 100
    ]

    soundness_scores = [
        human_results["soundness"] * 100,
        agent_results["soundness"] * 100,
        vim_results["soundness"] * 100
    ]

    x = np.arange(len(models))
    width = 0.35

    plt.figure(figsize=(8, 5))

    validity_bars = plt.bar(
        x - width / 2,
        validity_scores,
        width,
        label="Validity"
    )

    soundness_bars = plt.bar(
        x + width / 2,
        soundness_scores,
        width,
        label="Soundness"
    )

    plt.bar_label(
        validity_bars,
        fmt="%.1f%%",
        padding=3
    )

    plt.bar_label(
        soundness_bars,
        fmt="%.1f%%",
        padding=3
    )

    plt.xticks(x, models)
    plt.ylim(0, 110)
    plt.ylabel("Percentage (%)")
    plt.title(f"Property-Based Test Evaluation for {api_name}")
    plt.legend()

    plt.tight_layout()
    plt.show()

plot_pbt_results(
    human_linspace,
    codex_linspace,
    "np.linspace()"
)

plot_pbt_results(
    human_argmax,
    codex_argmax,
    "torch.argmax()"
)

plot_pbt_results(
    human_isoparse,
    codex_isoparse,
    "dateutil.parser.isoparse()"
    
)

plot_pbt_results(
    human_parse,
    codex_parse,
    "dateutil.parser.parse()"
    
)

plot_pbt_results(
    avg_human_dateutil,
    avg_codex_dateutil,
    "Average PBT Results for dateutil module (2 functions)"
    
)


plot_pbt_results(
    human_mean,
    codex_mean,
    "statistics.mean()"
    
)

plot_pbt_results(
    human_geometric_mean,
    codex_geometric_mean,
    "statistics.geometric_mean()"
    
)

plot_pbt_results(
    human_correlation,
    codex_correlation,
    "statistics.correlation()"
)

plot_pbt_results(
    human_linear_regression,
    codex_linear_regression,
    "statistics.linear_regression()"
)

plot_pbt_results(
    human_median,
    codex_median,
    "statistics.median()"
)

plot_pbt_results(
    human_variance,
    codex_variance,
    "statistics.variance()"
)

plot_pbt_results(
    avg_human_statistics,
    avg_codex_statistics,
    "AVG METRICS for statistics API"
)

plot_pbt_results(
    human_escape,
    codex_escape,
    "html.escape()"
)


plot_pbt_results(
    human_unescape,
    codex_unescape,
    "html.unescape()"
)

plot_pbt_results(
    avg_human_html,
    avg_codex_html,
    "avg html"
)

plot_pbt_results(
    human_compress,
    codex_compress,
    "zlib.compress()"
)

plot_pbt_results(
    human_decompress,
    codex_decompress,
    "zlib.decompress()"
)

plot_pbt_results(
    human_adler32,
    codex_adler32,
    "zlib.adler32()"
)

plot_pbt_results(
    avg_human_zlib,
    avg_codex_zlib,
    "AVG zlib"
)

plot_pbt_results(
    human_as_integer_ratio,
    codex_as_integer_ratio,
    "Decimal().as_integer_ratio()"
)


plot_pbt_results(
    human_compare,
    codex_compare,
    "Decimal().compare()"
)

plot_pbt_results(
    human_fma,
    codex_fma,
    "Decimal().fma()"
)

plot_pbt_results(
    human_from_float,
    codex_from_float,
    "Decimal.from_float()"
)

plot_pbt_results(
    human_quantize,
    codex_quantize,
    "Decimal.quantize()"
)





