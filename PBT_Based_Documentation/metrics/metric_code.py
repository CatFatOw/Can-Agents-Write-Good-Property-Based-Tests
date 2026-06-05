"""Metrics helpers for generated property-based documentation tests."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

from tqdm import tqdm


def evaluate_validity_soundness(test_func: Callable[[], None], n: int = 1000) -> dict[str, Any]:
    """Repeatedly execute a property and separate invalid tests from false claims."""
    validity_errors: set[str] = set()
    soundness_errors: set[str] = set()

    validity_failures = 0
    soundness_failures = 0

    for _ in tqdm(range(n)):
        try:
            test_func()
        except AssertionError as exc:
            soundness_failures += 1
            soundness_errors.add(str(exc))
        except Exception as exc:
            validity_failures += 1
            validity_errors.add(type(exc).__name__)

    validity = 1 - validity_failures / n
    soundness = 1 - soundness_failures / n

    return {
        "validity": validity,
        "soundness": soundness,
        "validity_errors": sorted(validity_errors),
        "soundness_errors": sorted(soundness_errors),
    }


def run_command(command: list[str], cwd: str | Path) -> dict[str, Any]:
    """Run a metrics command and return structured output without raising."""
    try:
        result = subprocess.run(
            command,
            cwd=Path(cwd),
            text=True,
            capture_output=True,
            check=False,
        )
    except FileNotFoundError as exc:
        return {
            "command": command,
            "available": False,
            "returncode": None,
            "stdout": "",
            "stderr": str(exc),
        }

    return {
        "command": command,
        "available": True,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def evaluate_pytest(test_file: str | Path, cwd: str | Path = ".") -> dict[str, Any]:
    """Run generated pytest/Hypothesis properties."""
    return run_command([sys.executable, "-m", "pytest", "-q", str(test_file)], cwd=cwd)


def evaluate_mutation_testing(mutation_dir: str | Path) -> dict[str, Any]:
    """Run mutmut and collect both execution and result summaries."""
    mutation_path = Path(mutation_dir)
    return {
        "run": run_command(["mutmut", "run"], cwd=mutation_path),
        "results": run_command(["mutmut", "results"], cwd=mutation_path),
    }


def score_validity_soundness_mutation(
    pytest_result: dict[str, Any],
    mutation_result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Produce a conservative confidence score for documentation promotion."""
    pytest_output = (pytest_result.get("stdout") or "") + "\n" + (pytest_result.get("stderr") or "")
    if not pytest_result.get("available") or pytest_result.get("returncode") is None:
        validity = 0.0
        soundness = 0.0
    elif pytest_result.get("returncode") == 0:
        validity = 1.0
        soundness = 1.0
    else:
        has_errors = bool(re.search(r"\bERROR(S)?\b|ImportError|ModuleNotFoundError|SyntaxError", pytest_output))
        has_failures = bool(re.search(r"\bFAILED\b|AssertionError|assert ", pytest_output))
        validity = 0.0 if has_errors else 1.0
        soundness = 0.0 if has_failures else 1.0
    mutation_usefulness = None

    if mutation_result:
        mutation_text = (
            mutation_result.get("run", {}).get("stdout", "")
            + "\n"
            + mutation_result.get("results", {}).get("stdout", "")
        )
        killed = len(re.findall(r"\bkilled\b", mutation_text, re.I))
        survived = len(re.findall(r"\bsurvived\b", mutation_text, re.I))
        if killed or survived:
            mutation_usefulness = killed / (killed + survived)

    confidence = 0.45 * validity + 0.45 * soundness
    if mutation_usefulness is None:
        confidence += 0.05
    else:
        confidence += 0.10 * mutation_usefulness

    return {
        "validity": validity,
        "soundness": soundness,
        "mutation_usefulness": mutation_usefulness,
        "confidence": round(confidence, 3),
        "passes_documentation_gate": validity == 1.0 and soundness == 1.0 and confidence >= 0.9,
    }
