#!/usr/bin/env python3
"""Generate invariant-backed documentation from source code.

Pipeline:
source code + prompts/config -> candidate invariants -> Hypothesis tests ->
test/mutation metrics -> high-confidence Markdown documentation.
"""

from __future__ import annotations
# parse cli arguments
import argparse
# abstract syntax tree for analysis of code
import ast
import json
import os
import re
# Runs temrinal commands
import subprocess
import sys
# Autogenerate constructor and methods for classes 
from dataclasses import dataclass
from pathlib import Path
# Used to import saved python functions
import importlib.util
# temp dict
import tempfile 
from typing import Any
# Adding test_validity
from metrics import test_metrics, invariant_metrics_test
# Import hypothesis in case user wants to display how valid/sound it is 
from hypothesis import given, settings, Verbosity, note
from hypothesis.strategies import composite, integers, floats, lists, booleans, text
from openai import OpenAI



ROOT = Path(__file__).resolve().parent
# - Default OpenAI model selection
DEFAULT_PROMPT_DIR = ROOT / "invariant_extraction_prompts"
# - Terminal color enable/disable settings
DEFAULT_MODEL = os.environ.get("OPENAI_MODEL", "gpt-5.4-mini")
OPENAI_SEED = 42
# - Root directory and prompt locations
COLOR_ENABLED = os.environ.get("NO_COLOR") is None
# ANSI colors for displaying status updates
COLORS = {
    "green": "\033[92m",
    "red": "\033[91m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "bold": "\033[1m",
    "reset": "\033[0m",
}

# Use the dataclass to create ApiContext class quickly and frozen=True makes it immutable
@dataclass(frozen=True)
class ApiContext:
    source_path: Path
    source_code: str
    function_name: str
    function_signature: str
    existing_documentation: str


def read_text(path: str | Path | None, default: str = "") -> str:
    """Function, given a .txt object reads/displays the contents of the file"""
    if not path:
        return default
    # read the contents 
    with open(path, encoding="utf-8") as file:
       return file.read()


def color(text: str, name: str) -> str:
    """Function allows colored text to be printed in terminal"""
    if not COLOR_ENABLED:
        return text
    return f"{COLORS.get(name, '')}{text}{COLORS['reset']}"


def log_step(message: str) -> None:
    """Function logs a running message"""
    print(color(f"[RUN] {message}", "blue"))


def log_success(message: str) -> None:
    """function logs a success instance"""
    print(color(f"[OK] {message}", "green"))


def log_stop(message: str) -> None:
    """function logs a stop message"""
    print(color(f"[STOP] {message}", "yellow"))


def log_error(message: str) -> None:
    """function logs an error message due to low metrics (validity, soundness, and mutation)"""
    print(color(f"[BLOCKED] {message}", "red"))


def load_config(path: str | None) -> dict[str, Any]:
    """Function loads a JSON file and returns it as a dictionary"""
    
    # path not given
    if not path:
        return {}
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def strip_markdown_fences(text: str) -> str:
    """removes model markdown code and returns only the paython code"""
    # Remove whitespace
    text = text.strip()
    match = re.fullmatch(r"```(?:python|py|markdown|md)?\s*(.*?)\s*```", text, re.S)
    return match.group(1).strip() if match else text


def render_prompt(prompt_path: Path, values: dict[str, str]) -> str:
    """Function loads a template file and fills in placeholder using values of the dictionary, utf for telling python to convert into characters"""
    with open(prompt_path, encoding="utf-8") as file:
        template = file.read()
        return template.format(**values)



def extract_signature(source_code: str, node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """Function extracts the full function code from source code (even if it spans multi-lined)"""
    lines = source_code.splitlines()
    signature_lines: list[str] = []
    depth = 0
    started = False
    for line in lines[node.lineno - 1 :]:
        stripped = line.strip()
        if not started and not stripped.startswith(("def ", "async def ")):
            continue
        started = True
        signature_lines.append(stripped)
        depth += stripped.count("(") + stripped.count("[") + stripped.count("{")
        depth -= stripped.count(")") + stripped.count("]") + stripped.count("}")
        if depth == 0 and (stripped.endswith(":") or stripped.endswith("...")):
            break
    return " ".join(part.rstrip(":") for part in signature_lines).strip()


def response_text(model: str, prompt: str, stream: bool = True, seed: int = OPENAI_SEED, prefer_chat_completions: bool = False) -> str:
    """Function is an OpenAI Wrapper that calls the model

    ``prefer_chat_completions`` skips the Responses API for OpenAI-compatible
    gateways (e.g. the CMU AI Gateway) that only implement Chat Completions and
    return a 404 for ``responses.create``.
    """
    # Check if user provided an API key via os.environ
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("Set OPENAI_API_KEY before running GPT stages.")

    try:
        from openai import OpenAI
    except ImportError:
        return response_text_with_legacy_openai(model, prompt, stream=stream, seed=seed)
    # We create the openAI client
    client = OpenAI()
    # Checks if contains responses attribute. Skip it for gateways that only
    # speak Chat Completions, otherwise responses.create raises a 404.
    if not prefer_chat_completions and hasattr(client, "responses"):
        try:
            return response_text_with_responses(client, model, prompt, stream=stream, seed=seed)
        except AttributeError:
            pass
    # If has attribute chat and completition
    if hasattr(client, "chat") and hasattr(client.chat, "completions"):
        return response_text_with_chat_completions(client, model, prompt, stream=stream, seed=seed)
    raise SystemExit(
        "This openai package exposes neither client.responses nor client.chat.completions. "
        "Upgrade it with: python3 -m pip install --upgrade openai"
    )


def response_text_with_responses(client: Any, model: str, prompt: str, stream: bool = True, seed: int = OPENAI_SEED) -> str:
    # If stream = false, then we just output the data immediately
    if not stream:
        response = client.responses.create(model=model, input=prompt)
        return getattr(response, "output_text", "") or extract_response_output_text(response)

    # Otherwise we stream the data
    chunks: list[str] = []
    events = client.responses.create(model=model, input=prompt, stream=True)
    for event in events:
        # Log only the output_text.delta events
        if event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)
            chunks.append(event.delta)
    print()
    return "".join(chunks)


def response_text_with_legacy_openai(model: str, prompt: str, stream: bool = True, seed: int = OPENAI_SEED) -> str:
    try:
        import openai
    except ImportError as exc:
        raise SystemExit("Install the openai package before running GPT stages.") from exc

    if not hasattr(openai, "ChatCompletion"):
        raise SystemExit(
            "Your openai package is too old for this script. Upgrade it with: "
            "python3 -m pip install --upgrade openai"
        )

    messages = [
        {
            "role": "system",
            "content": "You are a careful Python property-based testing and API documentation assistant.",
        },
        {"role": "user", "content": prompt},
    ]
    if not stream:
        response = openai.ChatCompletion.create(model=model, messages=messages, seed=seed)
        return response["choices"][0]["message"]["content"] or ""

    chunks: list[str] = []
    events = openai.ChatCompletion.create(model=model, messages=messages, stream=True, seed=seed)
    for event in events:
        delta = event["choices"][0].get("delta", {}).get("content", "")
        if delta:
            print(delta, end="", flush=True)
            chunks.append(delta)
    print()
    return "".join(chunks)


def response_text_with_chat_completions(client: Any, model: str, prompt: str, stream: bool = True, seed: int = OPENAI_SEED) -> str:
    """Older version in case OpenAI version is old"""
    messages = [
        {
            "role": "system",
            "content": "You are a careful Python property-based testing and API documentation assistant.",
        },
        {"role": "user", "content": prompt},
    ]
    if not stream:
        response = client.chat.completions.create(model=model, messages=messages, seed=seed)
        return response.choices[0].message.content or ""

    chunks: list[str] = []
    events = client.chat.completions.create(model=model, messages=messages, stream=True, seed=seed)
    for event in events:
        delta = event.choices[0].delta.content or ""
        if delta:
            print(delta, end="", flush=True)
            chunks.append(delta)
    print()
    return "".join(chunks)


def extract_response_output_text(response: Any) -> str:
    """Backup code for older version openai versions"""
    chunks: list[str] = []
    for item in getattr(response, "output", []) or []:
        for content in getattr(item, "content", []) or []:
            text = getattr(content, "text", None)
            if text:
                chunks.append(text)
    return "".join(chunks)


def find_api_context(
    source_path: Path,
    function_name: str | None,
    existing_documentation: str,
) -> ApiContext:
    """Function extracts source code and feeds into GPT"""
    source_code = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source_code)
    candidates: list[ast.FunctionDef | ast.AsyncFunctionDef] = [
        node for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    selected = None
    if function_name:
        selected = next((node for node in candidates if node.name == function_name), None)
    elif len(candidates) == 1:
        selected = candidates[0]

    if selected is None:
        api_name = function_name or source_path.stem
        signature = f"{api_name}(...)"
    else:
        api_name = selected.name
        signature = extract_signature(source_code, selected) or f"{api_name}(...)"

    return ApiContext(
        source_path=source_path,
        source_code=source_code,
        function_name=api_name,
        function_signature=signature,
        existing_documentation=existing_documentation,
    )


def artifact_dir(base_dir: Path, api_name: str) -> Path:
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", api_name).strip("_") or "api"
    path = base_dir / safe_name
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_artifact(path: Path, content: str) -> None:
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    log_success(f"Wrote {path}")


def default_review_path(out_dir: Path) -> Path:
    return out_dir / "human_review.md"


def resolve_review_path(review_path: str | None, out_dir: Path, auto_continue: bool) -> str | None:
    if review_path:
        return review_path
    inferred = default_review_path(out_dir)
    if auto_continue and inferred.exists():
        return str(inferred)
    return None


def run_command(command: list[str], cwd: Path) -> dict[str, Any]:
    try:
        result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
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


def run_pytest(test_file: Path, cwd: Path) -> dict[str, Any]:
    return run_command([sys.executable, "-m", "pytest", "-q", str(test_file)], cwd=cwd)


def run_mutmut(mutation_dir: Path) -> dict[str, Any]:
    run_result = run_command(["mutmut", "run"], cwd=mutation_dir)
    results_result = run_command(["mutmut", "results"], cwd=mutation_dir)
    return {"run": run_result, "results": results_result}


def parse_pytest_counts(output: str) -> dict[str, int]:
    counts = {"passed": 0, "failed": 0, "errors": 0}
    for key in counts:
        match = re.search(rf"(\d+)\s+{key}\b", output)
        if match:
            counts[key] = int(match.group(1))
    return counts


def score_metrics(pytest_result: dict[str, Any], mutation_result: dict[str, Any] | None) -> dict[str, Any]:
    pytest_output = (pytest_result.get("stdout") or "") + "\n" + (pytest_result.get("stderr") or "")
    if not pytest_result.get("available") or pytest_result.get("returncode") is None:
        validity = 0.0
        soundness = 0.0
    elif pytest_result.get("returncode") == 0:
        validity = 1.0
        soundness = 1.0
    else:
        counts = parse_pytest_counts(pytest_output)
        total = counts["passed"] + counts["failed"] + counts["errors"]
        if total:
            validity = 1 - counts["errors"] / total
            soundness = 1 - counts["failed"] / total
        else:
            has_errors = bool(re.search(r"\bERROR(S)?\b|ImportError|ModuleNotFoundError|SyntaxError", pytest_output))
            has_failures = bool(re.search(r"\bFAILED\b|AssertionError|assert ", pytest_output))
            validity = 0.0 if has_errors else 1.0
            soundness = 0.0 if has_failures else 1.0
    mutation_usefulness = None

    if mutation_result:
        mutation_stdout = (
            mutation_result.get("results", {}).get("stdout", "")
            + "\n"
            + mutation_result.get("run", {}).get("stdout", "")
        )
        killed = len(re.findall(r"\bkilled\b", mutation_stdout, re.I))
        survived = len(re.findall(r"\bsurvived\b", mutation_stdout, re.I))
        if killed or survived:
            mutation_usefulness = killed / (killed + survived)

    confidence = 0.45 * validity + 0.45 * soundness
    if mutation_usefulness is not None:
        confidence += 0.10 * mutation_usefulness
    elif mutation_result is None:
        confidence += 0.05

    return {
        "validity": validity,
        "soundness": soundness,
        "mutation_usefulness": mutation_usefulness,
        "confidence": round(confidence, 3),
        "passes_documentation_gate": validity == 1.0 and soundness == 1.0 and confidence >= 0.9,
        "note": (
            "Mutation usefulness is best-effort because mutmut output is version dependent."
            if mutation_result
            else "Mutation testing was skipped."
        ),
    }


def metrics_gate_failure(
    scores: dict[str, Any],
    *,
    min_validity: float,
    min_soundness: float,
    min_confidence: float,
    min_mutation: float | None,
) -> str | None:
    failures: list[str] = []
    if scores["validity"] < min_validity:
        failures.append(f"validity {scores['validity']:.2f} < {min_validity:.2f}")
    if scores["soundness"] < min_soundness:
        failures.append(f"soundness {scores['soundness']:.2f} < {min_soundness:.2f}")
    if scores["confidence"] < min_confidence:
        failures.append(f"confidence {scores['confidence']:.3f} < {min_confidence:.3f}")
    mutation_usefulness = scores.get("mutation_usefulness")
    if min_mutation is not None and mutation_usefulness is not None and mutation_usefulness < min_mutation:
        failures.append(f"mutation usefulness {mutation_usefulness:.2f} < {min_mutation:.2f}")
    if not failures:
        return None
    return "; ".join(failures)


def markdown_metrics(
    pytest_result: dict[str, Any],
    mutation_result: dict[str, Any] | None,
    scores: dict[str, Any],
    gate_failure: str | None,
) -> str:
    lines = [
        "# Metrics Report",
        "",
        "## Scores",
        "",
        f"- Validity: {scores['validity']:.2f}",
        f"- Soundness: {scores['soundness']:.2f}",
        f"- Mutation usefulness: {scores['mutation_usefulness']}",
        f"- Confidence: {scores['confidence']:.3f}",
        f"- Documentation gate: {'pass' if gate_failure is None else 'review needed'}",
        f"- Note: {scores['note']}",
        "",
        "## Pytest",
        "",
        f"- Command: `{' '.join(pytest_result['command'])}`",
        f"- Available: {pytest_result['available']}",
        f"- Return code: {pytest_result['returncode']}",
        "",
        "```text",
        (pytest_result.get("stdout") or "").strip(),
        (pytest_result.get("stderr") or "").strip(),
        "```",
    ]
    if mutation_result:
        lines.extend(
            [
                "",
                "## Mutation Testing",
                "",
                f"- Run return code: {mutation_result['run']['returncode']}",
                f"- Results return code: {mutation_result['results']['returncode']}",
                "",
                "```text",
                (mutation_result["run"].get("stdout") or "").strip(),
                (mutation_result["run"].get("stderr") or "").strip(),
                (mutation_result["results"].get("stdout") or "").strip(),
                (mutation_result["results"].get("stderr") or "").strip(),
                "```",
            ]
        )
    return "\n".join(lines)


def build_common_values(context: ApiContext) -> dict[str, str]:
    return {
        "function_name": context.function_name,
        "function_signature": context.function_signature,
        "api_source_code": context.source_code,
        "api_documentation": context.existing_documentation,
        "existing_documentation": context.existing_documentation,
    }



def strip_markdown_fences(text: str) -> str:
    text = text.strip()
    match = re.fullmatch(r"```(?:python|py)?\s*(.*?)\s*```", text, re.S)
    return match.group(1).strip() if match else text


def parse_json_object(text: str) -> dict[str, Any]:
    text = strip_markdown_fences(text)
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", text)
        if not match:
            raise
        data = json.loads(match.group(0))
    if not isinstance(data, dict):
        raise ValueError("Expected a JSON object.")
    return data


def evaluate_pbt_test(source_code, invariant, test_code, api_name="api.function"):
    """Run one property-based test and calculate validity/soundness metrics."""
    output = strip_markdown_fences(test_code)
    namespace = {}
    try:
        import math
        import numpy as np

        namespace.update({"math": math, "np": np, "numpy": np})
        module_name, _, attr_name = api_name.rpartition(".")
        if module_name and attr_name:
            try:
                module = __import__(module_name, fromlist=[attr_name])
                namespace[attr_name] = getattr(module, attr_name)
            except Exception:
                pass
        try:
            exec(source_code, namespace)
        except Exception:
            # Pasted library source can depend on hidden decorators/private globals.
            # The imported API binding above still lets generated tests call the real function.
            pass
        exec(output, namespace)

        test_function = next(
            value for name, value in namespace.items()
            if name.startswith("test_") and callable(value)
        )
        validity, soundness = test_metrics(test_function)
        error = ""
    except Exception as exc:
        validity = 0
        soundness = 0
        error = str(exc)

    return {
        "invariant": invariant,
        "test_code": output,
        "validity": validity,
        "soundness": soundness,
        "error": error,
    }


def confidence_from_scores(validity, soundness):
    score = round((validity + soundness) / 2, 2)
    if score >= 0.85:
        confidence = "HIGH"
    elif score >= 0.55:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"
    return confidence, score

# Redunant function call due to merged calls in metrics.py under the name invariant_metric_test

# def generate_pbt_test(model, source_code, invariants, streaming=True, api_name="api.function"):
#     """Function feeds gpt the test_invariant (text) that is generated and creates an hypohtesis test via the fed text"""

#     # Call the model each time /invariants
#     results = []

#     for test_invariant in invariants:
#         prompt = f"""
#             You are an expert in property-based testing, program analysis, and invariant inference.

#             Function/API Name:
#             {api_name}

#             Source Code:
#             {source_code}

#             Invariant Candidate:
#             {test_invariant}

#             Tasks:
#             1. Assess this invariant with a confidence label and numeric score.
#             2. Generate a small Hypothesis property-based test that attempts to falsify the invariant.

#             Confidence Levels:
#             HIGH:
#             - Directly supported by the source code.
#             - Likely true for all valid executions.
#             - Precise and useful.

#             MEDIUM:
#             - Plausible but may depend on assumptions.
#             - Potential edge cases exist.

#             LOW:
#             - Contradicted by the implementation.
#             - Overly broad, trivial, or likely incorrect.

#             Requirements:
#             - Use Hypothesis strategies appropriate for the function inputs.
#             - Avoid expensive or slow strategies.
#             - Limit generated collection sizes to keep runtime reasonable (especially crucial for a working app/tool).
#             - Include edge cases naturally through Hypothesis.
#             - Assume the function under test already exists and call it as {api_name}.
#             - Import all required Hypothesis modules.
#             - The test should fail if a counterexample to the invariant exists.
#             - Produce only executable Python code.
#             - Do not include markdown fences.
#             - Do not include explanations or comments.
#             - Do not include extra clutter, markdown, etc that interferes with code running.
#             - generate ONE FUNCTION.

#             Respond ONLY with valid JSON:
#             {{
#                 "confidence": "HIGH",
#                 "score": 0.95,
#                 "explanation": "Brief explanation.",
#                 "test_code": "complete python code here"
#             }}
#             """
        
#         client = OpenAI()
#         # If not streaming, just display the generated gpt text all at once
#         if not streaming:
#             response = client.responses.create(
#                 model=model,
#                 input=prompt,
#                 stream=False,
#             )
#             output = response.output_text
#         # if streaming, we display the text as it is getting generated
#         else:
#             chunks = []
#             events = client.responses.create(
#                 model=model,
#                 input=prompt,
#                 stream=True,
#             )
            
#             for event in events:
#                 if event.type == "response.output_text.delta":
#                     # Flush=True makes it show everything at once 
#                     print(event.delta, end="", flush=True)
#                     chunks.append(event.delta)
#                 print()

#             output = "".join(chunks)
#         try:
#             data = parse_json_object(output)
#             test_code = str(data.get("test_code") or "")
#             confidence = str(data.get("confidence") or "").upper()
#             score = float(data.get("score") or 0)
#             explanation = str(data.get("explanation") or "")
#         except Exception:
#             test_code = strip_markdown_fences(output)
#             confidence = ""
#             score = 0
#             explanation = ""

#         result = evaluate_pbt_test(source_code, test_invariant, test_code, api_name=api_name)
#         if confidence not in {"HIGH", "MEDIUM", "LOW"}:
#             confidence, score = confidence_from_scores(result["validity"], result["soundness"])
#         result["confidence"] = confidence
#         result["score"] = max(0, min(1, score))
#         result["explanation"] = explanation
#         results.append(result)
        
#     return {"results": results}

    


def run_pipeline(
    *,
    source_path: Path,
    function_name: str | None,
    docs_path: str | None,
    review_path: str | None,
    reviewer_notes: str,
    prompt_dir: Path,
    artifact_root: Path,
    model: str,
    stream: bool,
    skip_tests: bool,
    run_mutation_flag: bool,
    mutation_dir: Path,
    auto_approve: bool,
    auto_continue: bool,
    force_docs: bool,
    min_validity: float,
    min_soundness: float,
    min_confidence: float,
    min_mutation: float | None,
    display_metrics: bool = True,
) -> Path:
    context = find_api_context(source_path, function_name, read_text(docs_path))
    out_dir = artifact_dir(artifact_root, context.function_name)
    review_path = resolve_review_path(review_path, out_dir, auto_continue)
    common = build_common_values(context)

    if not review_path:
        candidate_prompt = render_prompt(prompt_dir / "properties_prompt.md", common)
        log_step(f"Generating candidate invariants for {context.function_name}...")
        candidates = response_text(model, candidate_prompt, stream=stream)
        write_artifact(out_dir / "candidate_invariants.md", candidates)
        review_log = (
            "# Human Review\n\n"
            "Review the candidate invariants below. Delete rejected invariants, revise weak ones, "
            "and leave only accepted invariants in this file. Then rerun the same command. "
            "The script will automatically continue from this review file.\n\n"
            + candidates
        )
        write_artifact(out_dir / "human_review.md", review_log)
        # Display the soundness and validity metrics + the invariant test by the proposted invariants 
        if display_metrics:
            # Use a cheaper model for faster generation
            results = invariant_metrics_test(source_code=context.source_code, invariants=candidates, model="gpt-5.4-mini")
        if not auto_approve:
            log_stop(
                f"Stopped for human review. Edit {out_dir / 'human_review.md'} and rerun the same command."
            )
            return out_dir

    if review_path:
        approved_invariants = read_text(review_path)
        log_step(f"Using human-reviewed invariants from {review_path}")
    else:
        approved_invariants = candidates

    import_notes = (
        f"Source file path: {context.source_path}\n"
        "If the module is not importable by package name, load the source file with importlib.util "
        "inside the generated pytest file."
    )
    all_reviewer_notes = "\n\n".join(part for part in [import_notes, reviewer_notes] if part)

    test_prompt = render_prompt(
        prompt_dir / "pbt_generation_prompt.md",
        common
        | {
            "approved_invariants": approved_invariants,
            "reviewer_notes": all_reviewer_notes,
        },
    )
    log_step(f"Generating Hypothesis properties for {context.function_name}...")
    generated_tests = strip_markdown_fences(response_text(model, test_prompt, stream=stream))
    test_path = out_dir / "generated_tests.py"
    write_artifact(test_path, generated_tests)

    pytest_result = {
        "command": [sys.executable, "-m", "pytest", "-q", str(test_path)],
        "available": False,
        "returncode": None,
        "stdout": "",
        "stderr": "Test execution skipped.",
    }
    if not skip_tests:
        log_step(f"Executing generated properties for {context.function_name}...")
        pytest_result = run_pytest(test_path, cwd=ROOT)

    mutation_result = None
    if run_mutation_flag:
        log_step(f"Running mutation checks for {context.function_name}...")
        mutation_result = run_mutmut(mutation_dir)

    scores = score_metrics(pytest_result, mutation_result)
    gate_failure = metrics_gate_failure(
        scores,
        min_validity=min_validity,
        min_soundness=min_soundness,
        min_confidence=min_confidence,
        min_mutation=min_mutation if run_mutation_flag else None,
    )
    metrics_report = markdown_metrics(pytest_result, mutation_result, scores, gate_failure)
    write_artifact(out_dir / "metrics_report.md", metrics_report)
    if gate_failure and not force_docs:
        write_artifact(
            out_dir / "documentation_blocked.md",
            "# Documentation Blocked\n\n"
            "Documentation generation stopped because the metric gate did not pass.\n\n"
            f"Reason: {gate_failure}\n\n"
            "Review `metrics_report.md`, revise the accepted invariants or generated tests, "
            "and rerun. Use `--force-docs` only if you intentionally want documentation "
            "despite the failed gate.",
        )
        log_error(f"Stopped before documentation for {context.function_name}: {gate_failure}")
        return out_dir

    mutant_analysis = metrics_report
    if mutation_result:
        metrics_prompt = render_prompt(
            prompt_dir / "invariant_metrics_prompt.md",
            {
                "original": context.source_code,
                "mutant": mutation_result["results"].get("stdout", ""),
                "tests": generated_tests,
                "approved_invariants": approved_invariants,
                "metrics": metrics_report,
            },
        )
        log_step(f"Analyzing mutation results for {context.function_name}...")
        mutant_analysis = response_text(model, metrics_prompt, stream=stream)
        write_artifact(out_dir / "mutation_analysis.md", mutant_analysis)

    doc_prompt = render_prompt(
        prompt_dir / "documentation_generation_prompt.md",
        common
        | {
            "invariants": approved_invariants,
            "tests": generated_tests,
            "mutant_analysis": mutant_analysis,
            "reviewer_notes": all_reviewer_notes,
        },
    )
    log_step(f"Generating Markdown documentation for {context.function_name}...")
    documentation = response_text(model, doc_prompt, stream=stream)
    write_artifact(out_dir / "reconstructed_documentation.md", strip_markdown_fences(documentation))
    log_success(f"Documentation complete for {context.function_name}")
    return out_dir


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate invariant-backed API documentation using the bundled prompts."
    )
    parser.add_argument("source", nargs="?", help="Python source file to document.")
    parser.add_argument("--config", help="JSON config file. CLI flags override config values.")
    parser.add_argument("--function", help="Function/API name to document.")
    parser.add_argument("--functions", nargs="+", help="Several functions in the same source file.")
    parser.add_argument("--docs", help="Existing documentation file.")
    parser.add_argument("--review", help="Human-reviewed invariant file. Required to continue unless --auto-approve is set.")
    parser.add_argument("--reviewer-notes", default="", help="Extra reviewer notes.")
    parser.add_argument("--prompt-dir", default=str(DEFAULT_PROMPT_DIR))
    parser.add_argument("--artifact-root", default=str(ROOT / "artifacts"))
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--no-stream", action="store_true")
    parser.add_argument("--skip-tests", action="store_true")
    parser.add_argument("--run-mutation", action="store_true")
    parser.add_argument("--mutation-dir", help="Directory containing mutmut config.")
    parser.add_argument("--auto-approve", action="store_true", help="Use generated candidates without human review.")
    parser.add_argument("--no-auto-continue", action="store_true", help="Do not reuse an existing human_review.md automatically.")
    parser.add_argument("--force-docs", action="store_true", help="Generate documentation even if metrics fail.")
    parser.add_argument("--min-validity", type=float, default=0.8)
    parser.add_argument("--min-soundness", type=float, default=0.8)
    parser.add_argument("--min-confidence", type=float, default=0.75)
    parser.add_argument("--min-mutation", type=float, default=0.25)
    args = parser.parse_args()

    config = load_config(args.config)
    prompt_dir = Path(config.get("prompt_dir", args.prompt_dir)).expanduser().resolve()
    artifact_root = Path(config.get("artifact_root", args.artifact_root)).expanduser().resolve()
    model = config.get("model", args.model)
    run_mutation_flag = args.run_mutation or bool(config.get("run_mutation", False))
    skip_tests = args.skip_tests or bool(config.get("skip_tests", False))
    auto_approve = args.auto_approve or bool(config.get("auto_approve", False))
    auto_continue = bool(config.get("auto_continue", not args.no_auto_continue))
    force_docs = args.force_docs or bool(config.get("force_docs", False))
    min_validity = float(config.get("min_validity", args.min_validity))
    min_soundness = float(config.get("min_soundness", args.min_soundness))
    min_confidence = float(config.get("min_confidence", args.min_confidence))
    min_mutation = config.get("min_mutation", args.min_mutation)
    min_mutation = None if min_mutation is None else float(min_mutation)

    api_configs = config.get("apis")
    if api_configs:
        if not isinstance(api_configs, list):
            raise SystemExit("Config field 'apis' must be a list.")
    else:
        source = args.source or config.get("source")
        if not source:
            raise SystemExit("Provide a source file, or a JSON config with 'source' or 'apis'.")
        function_names = args.functions or [args.function or config.get("function")]
        api_configs = [
            {
                "source": source,
                "function": function_name,
                "docs": args.docs or config.get("docs"),
                "review": args.review or config.get("review"),
                "reviewer_notes": args.reviewer_notes or config.get("reviewer_notes", ""),
                "mutation_dir": args.mutation_dir or config.get("mutation_dir"),
            }
            for function_name in function_names
        ]

    output_dirs: list[Path] = []
    for api_config in api_configs:
        source = api_config.get("source")
        if not source:
            raise SystemExit("Every API config must include a 'source' field.")
        source_path = Path(source).expanduser().resolve()
        mutation_dir = Path(
            api_config.get("mutation_dir")
            or args.mutation_dir
            or config.get("mutation_dir")
            or source_path.parent
        ).resolve()
        output_dirs.append(
            run_pipeline(
                source_path=source_path,
                function_name=api_config.get("function"),
                docs_path=api_config.get("docs"),
                review_path=api_config.get("review"),
                reviewer_notes=api_config.get("reviewer_notes", args.reviewer_notes or config.get("reviewer_notes", "")),
                prompt_dir=prompt_dir,
                artifact_root=artifact_root,
                model=api_config.get("model", model),
                stream=not args.no_stream,
                skip_tests=skip_tests,
                run_mutation_flag=run_mutation_flag or bool(api_config.get("run_mutation", False)),
                mutation_dir=mutation_dir,
                auto_approve=bool(api_config.get("auto_approve", auto_approve)),
                auto_continue=bool(api_config.get("auto_continue", auto_continue)),
                force_docs=bool(api_config.get("force_docs", force_docs)),
                min_validity=float(api_config.get("min_validity", min_validity)),
                min_soundness=float(api_config.get("min_soundness", min_soundness)),
                min_confidence=float(api_config.get("min_confidence", min_confidence)),
                min_mutation=(
                    None
                    if api_config.get("min_mutation", min_mutation) is None
                    else float(api_config.get("min_mutation", min_mutation))
                ),
            )
        )

    log_success("Done. Artifacts are in:")
    for output_dir in output_dirs:
        print(color(f"- {output_dir}", "green"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
