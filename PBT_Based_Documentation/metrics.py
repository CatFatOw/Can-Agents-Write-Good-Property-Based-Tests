from openai import OpenAI
import ast 
import json
from typing import List

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


def invariant_metrics_test(source_code:str, invariants:List[str], model="gpt-5.4-mini", streaming=True, api_name="api.function"):
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
            "test_code": "complete python code here"
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
