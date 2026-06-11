from openai import OpenAI
import ast 
import json
from typing import List
import pytest 
import mutmut 
import subprocess
import os
import tempfile, shutil
from pathlib import Path

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



def analyze_mutants(working_dir, model="gpt-5.4-mini", streaming=True):
    """Function runs a deep analysis on all survived mutants, and then uses GPT to provided a in-depth summary
    high, medium, low on the criticality of the mutants killed/not killed
    """
    survived_mutants = subprocess.run(
        ["mutmut","results"],
        cwd=working_dir,
        capture_output=True,
        text=True,
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
            input=PROMPT
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

    

    




def invariant_metrics_test(source_code:str, invariants:List[str], model="gpt-5.4-mini", streaming=True, api_name="api.function", show_mutation_tests = True):
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
                    input=PROMPT
                )
                output = response.output_text

            # Streaming = true, so we gradually output text
            else:
                events = client.responses.create(
                    model=model,
                    input=PROMPT,
                    stream=True
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
            mutation_analysis = ""

            # If the user selected to do mutmut mutation testing
            if show_mutation_tests:
                # Create a directory for workflow
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_dir = Path(temp_dir)

                    # Save the user provided source code. This will be crucial for the setup.cfg later
                    source_path = temp_dir / "source.py"
                    # Writes the source code to source path
                    source_path.write_text(source_code, encoding="utf-8")

                    # Save/write the generated hypothesis invariant
                    test_path = temp_dir / "test_invariant.py"
                    test_path.write_text(test_code, encoding="utf-8")


                    # 3. Create mutmut config setup.cfg
                    setup_path = temp_dir / "setup.cfg"
                    setup_path.write_text(
                        """
                        [mutmut]
                        paths_to_mutate=source.py
                        mutate_only_covered_lines=true
                        pytest_add_cli_args_test_selection=.
                        """.strip(), encoding="utf-8",
                        
                    )

                    # Run the terminal commands :D 
                    mutmut_output = subprocess.run(
                        ["mutmut", "run"],
                        cwd=temp_dir,
                        capture_output=True,
                        text=True

                    )

                    output = mutmut_output.stdout 
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

                        # Calculate the mutation score
                        if metrics["total_mutants"]:
                            covered_mutants_score = metrics["killed"] / metrics["total_mutants"]


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


def mutation_analysis_for_test(source_code, test_code, model="gpt-5.4-mini"):
    """Create a temporary mutmut project and generate an analysis report for surviving mutants."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)

        source_path = temp_dir / "source.py"
        source_path.write_text(source_code, encoding="utf-8")

        test_path = temp_dir / "test_invariant.py"
        test_path.write_text(test_code, encoding="utf-8")

        setup_path = temp_dir / "setup.cfg"
        setup_path.write_text(
            """
            [mutmut]
            paths_to_mutate=source.py
            mutate_only_covered_lines=true
            pytest_add_cli_args_test_selection=.
            """.strip(), encoding="utf-8",
        )

        subprocess.run(
            ["mutmut", "run"],
            cwd=temp_dir,
            capture_output=True,
            text=True,
        )
        return analyze_mutants(temp_dir, model=model, streaming=False)
