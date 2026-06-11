from openai import OpenAI
import ast 
import json
from typing import List
import pytest 
import mutmut 
import subprocess
import os
import sys
import importlib.util
import tempfile, shutil
import textwrap
from pathlib import Path

OPENAI_SEED = 42
IMPORT_TO_PACKAGE = {
    "PIL": "Pillow",
    "bs4": "beautifulsoup4",
    "cv2": "opencv-python",
    "sklearn": "scikit-learn",
    "yaml": "PyYAML",
}
MUTATION_IMPORT_SKIP = {
    "__future__",
    "source",
    "pytest",
    "hypothesis",
}

def test_metrics(test_func, n=50):
    """Function used to calculate the soundness and validity metrics for display on the website"""

    validity_failures = 0
    soundness_failures = 0

    # We run this for 300 times
    for i in range(n):
        try:
            test_func()
        except AssertionError as e:
            soundness_failures += 1
        except Exception as e:
            validity_failures += 1
    # Calculate the valid and soundness metrics 
    valid = 1 - validity_failures / n
    sound = 1 - soundness_failures / n
    return (valid, sound)


import re

def strip_markdown_fences(text: str) -> str:
    text = text.strip()
    match = re.fullmatch(r"```(?:python|py)?\s*(.*?)\s*```", text, re.S)
    return match.group(1).strip() if match else text


def parse_json_object(text: str):
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


def confidence_from_scores(validity, soundness):
    score = round((validity + soundness) / 2, 2)
    if score >= 0.85:
        confidence = "HIGH"
    elif score >= 0.55:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"
    return confidence, score


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


def prepare_mutation_test_code(test_code, api_name):
    """Point generated tests at the temporary source.py module that mutmut changes."""
    module_name, _, attr_name = api_name.rpartition(".")
    if not attr_name:
        attr_name = api_name

    mutation_test_code = test_code
    if module_name and attr_name:
        mutation_test_code = mutation_test_code.replace(api_name, f"source.{attr_name}")
        mutation_test_code = mutation_test_code.replace(f"from {module_name} import {attr_name}", f"from source import {attr_name}")
    if attr_name:
        mutation_test_code = mutation_test_code.replace(f"np.{attr_name}", f"source.{attr_name}")

    return f"import source\nfrom source import {attr_name}\n" + mutation_test_code


def prepare_mutation_source_code(source_code, api_name):
    """Make inspected source snippets importable enough for mutmut."""
    module_name, _, attr_name = api_name.rpartition(".")
    import_modules = [module_name] if module_name else []

    if module_name and attr_name:
        try:
            module = __import__(module_name, fromlist=[attr_name])
            target = getattr(module, attr_name)
            target_module = getattr(target, "__module__", "")
            if target_module and target_module not in import_modules:
                import_modules.append(target_module)
        except Exception:
            pass
    if module_name == "numpy" or module_name.startswith("numpy."):
        for numpy_module in [
            "numpy._core.function_base",
            "numpy._core.overrides",
            "numpy._core.numeric",
            "numpy._core.multiarray",
        ]:
            if numpy_module not in import_modules:
                import_modules.append(numpy_module)

    bootstrap_lines = [
        "import importlib as _codex_importlib",
    ]
    for import_module in import_modules:
        bootstrap_lines.extend([
            "try:",
            f"    globals().update(_codex_importlib.import_module({import_module!r}).__dict__)",
            "except Exception:",
            "    pass",
        ])

    return "\n".join(bootstrap_lines) + "\n\n" + source_code


def parse_mutation_packages(mutation_packages):
    if not mutation_packages:
        return []
    if isinstance(mutation_packages, str):
        raw_packages = re.split(r"[\n,]+", mutation_packages)
    else:
        raw_packages = list(mutation_packages)
    return [package.strip() for package in raw_packages if str(package).strip()]


def imported_top_level_modules(*code_blocks):
    modules = set()
    for code in code_blocks:
        if not code:
            continue
        try:
            tree = ast.parse(code)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    modules.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module.split(".")[0])
    return modules


def inferred_mutation_packages(source_code, test_code):
    packages = []
    for module_name in sorted(imported_top_level_modules(source_code, test_code)):
        if module_name in MUTATION_IMPORT_SKIP:
            continue
        if module_name in getattr(sys, "stdlib_module_names", set()):
            continue
        if importlib.util.find_spec(module_name) is not None:
            continue
        packages.append(IMPORT_TO_PACKAGE.get(module_name, module_name))
    return packages


def mutation_deps_dir(temp_dir):
    """Directory where mutation packages get pip-installed. Must be a subdirectory:
    mutmut strips the project root itself from sys.path, so packages installed
    directly into temp_dir would be unimportable during the mutation runs."""
    return Path(temp_dir) / "mutation_deps"


def install_mutation_packages(temp_dir, mutation_packages, source_code="", test_code="", auto_install=True):
    packages = parse_mutation_packages(mutation_packages)
    if auto_install:
        for package in inferred_mutation_packages(source_code, test_code):
            if package not in packages:
                packages.append(package)
    if not packages:
        return ""

    install_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--quiet",
            "--target",
            str(mutation_deps_dir(temp_dir)),
            *packages,
        ],
        cwd=temp_dir,
        capture_output=True,
        text=True,
        timeout=180,
    )
    if install_result.returncode != 0:
        return (
            "Could not install mutation packages into the temporary environment.\n\n"
            f"Packages: {', '.join(packages)}\n\n"
            f"{install_result.stdout.strip() or install_result.stderr.strip()}"
        )
    return ""


def mutation_subprocess_env(temp_dir):
    """Put the deps directory on PYTHONPATH so pytest/mutmut subprocesses can import
    the packages installed by install_mutation_packages. The temp dir root itself
    would not work: mutmut removes it from sys.path before running the tests."""
    env = os.environ.copy()
    python_path = [str(mutation_deps_dir(temp_dir))]
    if env.get("PYTHONPATH"):
        python_path.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(python_path)
    return env



def analyze_mutants(working_dir, model="gpt-5.4-mini", streaming=True, seed=OPENAI_SEED):
    """Function runs a deep analysis on all survived mutants, and then uses GPT to provided a in-depth summary
    high, medium, low on the criticality of the mutants killed/not killed
    """
    mutation_env = mutation_subprocess_env(working_dir)
    survived_mutants = subprocess.run(
        ["mutmut","results"],
        cwd=working_dir,
        capture_output=True,
        text=True,
        env=mutation_env,
    )
    output = []
    client = OpenAI()
            

    # List of all mutants that have survived :D
    all_survived_mutants = survived_mutants.stdout.splitlines()
    for survived in all_survived_mutants:
        mutant_id = survived.split(":")[0].strip()
        if not mutant_id:
            continue
        # show why the mutant was not killed 
        analysis = subprocess.run(
            ["mutmut", "show", mutant_id],
            cwd=working_dir,
            capture_output=True,
            text=True,
            env=mutation_env,
        )
        output.append(
            f"Mutant ID: {mutant_id}\n"
            f"STDOUT:\n{analysis.stdout}\n"
            f"STDERR:\n{analysis.stderr}\n"
            "END OF ANALYSIS"
        )

    mutant_details = "\n\n".join(output) if output else "No surviving mutants were reported."

    # PROMPT GPT, and ask it to create a comprehensive prompt 
    PROMPT = f"""
        You are an expert Python software engineer specializing in mutation testing, property-based testing, invariants, and test quality assessment.

        Your task is to analyze the surviving mutants produced by mutmut.

        A surviving mutant indicates that the current test suite did not detect a behavioral change. However, not all surviving mutants are equally important. Some represent serious gaps in testing, while others are equivalent mutations or changes with little practical impact.

        SURVIVING MUTANTS:
        {mutant_details}

        For EACH surviving mutant:

        1. Identify:
        - Mutant ID
        - File name
        - Function name (if available)
        - Line number(s)
        - Original code
        - Mutated code

        2. Determine the severity of the survivor:

        SEVERE:
        - The mutation changes observable behavior.
        - A strong invariant or property-based test should likely have detected it.
        - Indicates a significant gap in test coverage or invariant quality.

        MEDIUM:
        - The mutation may affect behavior, but its impact is unclear.
        - Additional context or domain knowledge is required.
        - It is uncertain whether the invariant should have caught it.

        LOW:
        - The mutation is likely equivalent, cosmetic, unreachable, redundant, or has minimal behavioral impact.
        - Its survival does not strongly indicate a weakness in the test suite.

        3. Assign:
        - Severity: SEVERE / MEDIUM / LOW
        - Confidence Percentage (0-100)
        - Brief justification for the confidence score

        4. Explain:
        - Why the mutant survived
        - What behavior changed
        - Whether an invariant-based test should reasonably have detected it
        - What additional invariant or Hypothesis test could kill this mutant

        5. If the mutation appears equivalent or unkillable, explicitly state that.

        Generate a comprehensive markdown report.

        Use the following format for each mutant:

        # Mutant: <ID>

        ## Summary
        - Severity:
        - Confidence:
        - File:
        - Function:
        - Line Number:

        ## Mutation
        ```diff
        <mutation diff>
    """

    
    if not streaming:
        # Display the text all at once
        response = client.responses.create(
            model=model,
            input=PROMPT,
        )
    
        output = response.output_text
    else:
        # display the text gradually
        events = client.responses.create(
            model=model,
            input=PROMPT,
            stream=streaming,
        )

        chunks = []
        for event in events:
            if event.type == "response.output_text.delta":
                print(event.delta, end="", flush=True)
                chunks.append(event.delta)
        print()
        output = "".join(chunks)
    return output

    

    




def invariant_metrics_test(source_code:str, invariants:List[str], model="gpt-5.4-mini", streaming=True, api_name="api.function", show_mutation_tests = True, mutation_packages="", mutation_auto_install=True, seed=OPENAI_SEED):
    """Function calls ChatGPT, and via the model, assess a confidence level on how good the invariant is
    where high, high level of confidence the invariant is robust, medium, where the model is unsure, and low where the model thinks the
    invariant may be incorrect"""

    # array to contain a dictionary in the format of
    # {"invariant": invariant,"test_code": output, "validity": validity, "soundness": soundness, "error": error,}
    results = []

    # Call the open AI client
    client = OpenAI()

    for test_invariant in invariants:
        PROMPT = f"""
        You are an expert in property-based testing, program analysis, and invariant inference.

        Function/API Name:
        {api_name}

        Source Code:
        {source_code}

        Invariant Candidate:
        {test_invariant}

        Tasks:

        1. Evaluate the invariant.
        2. Find the line numbers in the source code where the invariant applies

        Confidence Levels:

        HIGH:
        - Directly supported by the source code.
        - Likely true for all valid executions.
        - Precise and useful.

        MEDIUM:
        - Plausible but may depend on assumptions.
        - Potential edge cases exist.

        LOW:
        - Contradicted by the implementation.
        - Overly broad, trivial, or likely incorrect.

        2. Generate ONE small Hypothesis property-based test that attempts to falsify the invariant.

        Requirements for the test:
        - Use appropriate Hypothesis strategies.
        - Keep runtime small.
        - Limit generated collection sizes.
        - Include edge cases naturally.
        - Assume the function exists and call it as {api_name}.
        - Import all required modules.
        - Produce executable Python code.
        - No markdown fences.
        - No explanations inside the code.
        - Generate exactly one test function.

        Respond ONLY with valid JSON:

        {{
            "confidence": "HIGH",
            "score": 0.95,
            "explanation": "Brief explanation.",
            "test_code": "complete python code here",
            "lineno": "line number in the source code where the invariant applies"
        }}
        """

        try:
            # Streaming = false, so we output text immediately
            if not streaming:
                response = client.responses.create(
                    model=model,
                    input=PROMPT,
                )
                output = response.output_text

            # Streaming = true, so we gradually output text
            else:
                events = client.responses.create(
                    model=model,
                    input=PROMPT,
                    stream=True,
                )

                chunks = []
                for event in events:
                    if event.type == "response.output_text.delta":
                        print(event.delta, end="", flush=True)
                        chunks.append(event.delta)

                print()
                output = "".join(chunks)

            # Turn the output into a json object, even if the model wrapped it in a fence.
            data = parse_json_object(output)

            confidence = str(data.get("confidence", "")).upper()
            score = float(data.get("score", 0))
            explanation = str(data.get("explanation", ""))
            test_code = str(data.get("test_code", ""))
            lineno = list(data.get("lineno", []))
            covered_mutants_score = None
            mutation_error = ""

            # If the user selected to do mutmut mutation testing
            if show_mutation_tests:
                # Create a directory for workflow
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_dir = Path(temp_dir)

                    # Save the user provided source code. This will be crucial for the setup.cfg later
                    source_path = temp_dir / "source.py"
                    # Writes the source code to source path
                    source_path.write_text(prepare_mutation_source_code(source_code, api_name), encoding="utf-8")

                    # Save/write the generated hypothesis invariant
                    test_path = temp_dir / "test_invariant.py"
                    test_path.write_text(prepare_mutation_test_code(test_code, api_name), encoding="utf-8")


                    # 3. Create mutmut config setup.cfg
                    # textwrap.dedent so the written file has no leading indentation:
                    # indented lines are invalid INI and make pytest/mutmut reject the config
                    setup_path = temp_dir / "setup.cfg"
                    setup_path.write_text(
                        textwrap.dedent("""
                        [mutmut]
                        paths_to_mutate=source.py
                        mutate_only_covered_lines=true
                        pytest_add_cli_args_test_selection=.
                        """).strip(), encoding="utf-8",

                    )

                    mutation_error = install_mutation_packages(
                        temp_dir,
                        mutation_packages,
                        source_code=source_code,
                        test_code=test_code,
                        auto_install=mutation_auto_install,
                    )

                    # Subprocesses need the temp dir on PYTHONPATH to import source.py
                    # and the packages installed above
                    mutation_env = mutation_subprocess_env(temp_dir)

                    if not mutation_error:
                        clean_test_output = subprocess.run(
                            [sys.executable, "-m", "pytest", "-q", str(test_path.name)],
                            cwd=temp_dir,
                            capture_output=True,
                            text=True,
                            env=mutation_env,
                        )
                        if clean_test_output.returncode != 0:
                            mutation_error = (
                                clean_test_output.stdout.strip()
                                or clean_test_output.stderr.strip()
                                or "Generated mutation test failed before mutmut could run."
                            )

                    # Run the terminal commands :D 
                    if not mutation_error:
                        mutmut_output = subprocess.run(
                            ["mutmut", "run"],
                            cwd=temp_dir,
                            capture_output=True,
                            text=True,
                            env=mutation_env,
                        )

                        output = mutmut_output.stdout
                        mutation_stderr = mutmut_output.stderr
                        if mutmut_output.returncode not in {0, 1}:
                            mutation_error = mutation_stderr.strip() or output.strip()
                    else:
                        output = ""
                        mutation_stderr = ""
                    # Match the output to closer format :D


                    matches = re.findall(
    r"🎉\s+(\d+)\s+🫥\s+(\d+)\s+⏰\s+(\d+)\s+🤔\s+(\d+)\s+🙁\s+(\d+)\s+🔇\s+(\d+)\s+🧙\s+(\d+)",
    output
)

                    if matches:
                        killed, no_tests, timeout, suspicious, survived, skipped, wizard = map(int, matches[-1])

                        metrics = {
                            "killed": killed,
                            "no_tests": no_tests,
                            "timeout": timeout,
                            "suspicious": suspicious,
                            "survived": survived,
                            "skipped": skipped,
                            "wizard": wizard,
                        }
                        metrics["total_mutants"] = (
                            metrics["killed"]
                            + metrics["no_tests"]
                            + metrics["timeout"]
                            + metrics["suspicious"]
                            + metrics["survived"]
                            + metrics["skipped"]
                            + metrics["wizard"]
                        )

                        # Calculate the mutation score. Killed mutants are good;
                        # survived/no-test/timeouts/suspicious mutants lower the score.
                        scored_mutants = (
                            metrics["killed"]
                            + metrics["survived"]
                            + metrics["no_tests"]
                            + metrics["timeout"]
                            + metrics["suspicious"]
                        )
                        if scored_mutants:
                            covered_mutants_score = metrics["killed"] / scored_mutants
                    elif not mutation_error:
                        mutation_error = (mutation_stderr.strip() or output.strip() or "mutmut did not return a parseable summary.")


            # {"invariant": invariant,"test_code": output, "validity": validity, "soundness": soundness, "error": error,}
            result = evaluate_pbt_test(
                source_code,
                test_invariant,
                test_code,
                api_name=api_name
            )

            if confidence not in {"HIGH", "MEDIUM", "LOW"}:
                confidence, score = confidence_from_scores(result["validity"], result["soundness"])

            result["confidence"] = confidence
            result["score"] = max(0, min(1, score))
            result["explanation"] = explanation
            # Adding lineno where the update pertains
            result["lineno"] = lineno
            if show_mutation_tests:
                result["mutation_score"] = covered_mutants_score
                result["mutation_error"] = mutation_error

            results.append(result)

        except Exception as e:
            results.append({
                "invariant": test_invariant,
                "test_code": "",
                "validity": 0,
                "soundness": 0,
                "confidence": "LOW",
                "score": 0,
                "explanation": "Could not generate or evaluate a metric for this invariant.",
                "error": str(e)
            })

    return {"results": results}


def mutation_analysis_for_test(source_code, test_code, api_name="api.function", model="gpt-5.4-mini", mutation_packages="", mutation_auto_install=True, seed=OPENAI_SEED):
    """Create a temporary mutmut project and generate an analysis report for surviving mutants."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)

        source_path = temp_dir / "source.py"
        source_path.write_text(prepare_mutation_source_code(source_code, api_name), encoding="utf-8")

        test_path = temp_dir / "test_invariant.py"
        test_path.write_text(prepare_mutation_test_code(test_code, api_name), encoding="utf-8")

        # textwrap.dedent so the written file has no leading indentation:
        # indented lines are invalid INI and make pytest/mutmut reject the config
        setup_path = temp_dir / "setup.cfg"
        setup_path.write_text(
            textwrap.dedent("""
            [mutmut]
            paths_to_mutate=source.py
            mutate_only_covered_lines=true
            pytest_add_cli_args_test_selection=.
            """).strip(), encoding="utf-8",
        )

        mutation_error = install_mutation_packages(
            temp_dir,
            mutation_packages,
            source_code=source_code,
            test_code=test_code,
            auto_install=mutation_auto_install,
        )
        if mutation_error:
            return (
                "# Mutation Analysis Unavailable\n\n"
                "The requested temporary mutation packages could not be installed.\n\n"
                "```text\n"
                f"{mutation_error}\n"
                "```"
            )

        # Subprocesses need the temp dir on PYTHONPATH to import source.py
        # and the packages installed above
        mutation_env = mutation_subprocess_env(temp_dir)

        clean_test_output = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", str(test_path.name)],
            cwd=temp_dir,
            capture_output=True,
            text=True,
            env=mutation_env,
        )
        if clean_test_output.returncode != 0:
            return (
                "# Mutation Analysis Unavailable\n\n"
                "The generated property-based test failed against the temporary source.py before mutmut could run.\n\n"
                "```text\n"
                f"{clean_test_output.stdout.strip() or clean_test_output.stderr.strip()}\n"
                "```"
            )

        subprocess.run(
            ["mutmut", "run"],
            cwd=temp_dir,
            capture_output=True,
            text=True,
            env=mutation_env,
        )
        return analyze_mutants(temp_dir, model=model, streaming=False, seed=seed)
