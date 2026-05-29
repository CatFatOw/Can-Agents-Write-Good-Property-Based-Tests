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

# dateutil.parser.parse
human_parse = {'validity': 0.6666666666666666, 'soundness': 1.0, 'validity_errors': {'ParserError'}, 'soundness_errors': set()}
codex_parse = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}

# Compute the dateutil avg metrics
avg_human_dateutil = {"validity": (human_parse["validity"] + human_isoparse["validity"])/2, "soundness": (human_parse["soundness"] + human_isoparse["soundness"])/2}
avg_codex_dateutil = {"validity": (codex_parse["validity"] + codex_isoparse["validity"])/2, "soundness": (codex_parse["soundness"] + codex_isoparse["soundness"])/2}

# Statistics mean()
human_mean = {'validity': 0.75, 'soundness': 0.5, 'validity_errors': {'ZeroDivisionError'}, 'soundness_errors': {''}}
codex_mean = {'validity': 1.0, 'soundness': 1.0, 'validity_errors': set(), 'soundness_errors': set()}
VIM_mean = {'validity': 0.8333333333333334, 'soundness': 0.8333333333333334, 'validity_errors': {'FailedHealthCheck'}, 'soundness_errors': {''}}



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


plot_pbt_results_three(
    human_mean,
    codex_mean,
    VIM_mean,
    api_name="statistics.mean()",
    
)

