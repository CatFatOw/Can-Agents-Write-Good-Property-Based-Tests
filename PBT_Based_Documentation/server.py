from __future__ import annotations

import json
import os
import re
import importlib
import inspect
import pydoc
import sys
from contextlib import contextmanager
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gpt_documentation_generator import response_text as project_response_text
from gpt_documentation_generator import strip_markdown_fences
from metrics import evaluate_pbt_test
from metrics import invariant_metrics_test
from metrics import mutation_analysis_for_test

MODEL = os.environ.get("OPENAI_MODEL", "gpt-5.5")
METRICS_MODEL = os.environ.get("OPENAI_METRICS_MODEL", "gpt-5.4-mini")
GPT_CACHE: dict[tuple[str, str], str] = {}
METRICS_CACHE: dict[tuple[str, str, str, bool], dict[str, Any]] = {}
SOURCE_CACHE: dict[str, dict[str, str]] = {}


def strip_fences(text: str) -> str:
    text = text.strip()
    match = re.fullmatch(r"```(?:json|markdown|md)?\s*(.*?)\s*```", text, re.S)
    return match.group(1).strip() if match else text


@contextmanager
def request_openai_key(openai_key: str | None):
    old_key = os.environ.get("OPENAI_API_KEY")
    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key
    try:
        yield
    finally:
        if openai_key:
            if old_key is None:
                os.environ.pop("OPENAI_API_KEY", None)
            else:
                os.environ["OPENAI_API_KEY"] = old_key


def run_project_gpt(prompt: str, openai_key: str | None) -> str:
    if not openai_key and not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("Paste an OpenAI API key or set OPENAI_API_KEY before starting server.py.")
    cache_key = (MODEL, prompt)
    if cache_key in GPT_CACHE:
        return GPT_CACHE[cache_key]
    with request_openai_key(openai_key):
        text = project_response_text(MODEL, prompt, stream=False)
    GPT_CACHE[cache_key] = text
    return text


def stream_project_gpt(prompt: str, openai_key: str | None):
    if not openai_key and not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("Paste an OpenAI API key or set OPENAI_API_KEY before starting server.py.")
    cache_key = (MODEL, prompt)
    if cache_key in GPT_CACHE:
        yield GPT_CACHE[cache_key]
        return

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("Install the openai package with: python3 -m pip install openai") from exc

    chunks: list[str] = []
    with request_openai_key(openai_key):
        client = OpenAI()
        if hasattr(client, "responses"):
            events = client.responses.create(model=MODEL, input=prompt, stream=True)
            for event in events:
                if getattr(event, "type", "") == "response.output_text.delta":
                    chunks.append(event.delta)
                    yield event.delta
        else:
            events = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a careful Python property-based testing and API documentation assistant.",
                    },
                    {"role": "user", "content": prompt},
                ],
                stream=True,
            )
            for event in events:
                delta = event.choices[0].delta.content or ""
                if delta:
                    chunks.append(delta)
                    yield delta
    GPT_CACHE[cache_key] = "".join(chunks)


def parse_json_array(text: str) -> list[Any]:
    text = strip_fences(text)
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\[[\s\S]*\]", text)
        if not match:
            raise
        data = json.loads(match.group(0))
    if not isinstance(data, list):
        raise ValueError("Expected a JSON array.")
    return data


ALIASES = {
    "np": "numpy",
    "pd": "pandas",
    "plt": "matplotlib.pyplot",
    "sp": "scipy",
    "tf": "tensorflow",
}


def normalize_object_name(object_name: str) -> str:
    normalized = object_name.strip()
    if not normalized:
        raise ValueError("Enter a Python object name, for example np.linspace.")
    first, dot, rest = normalized.partition(".")
    if dot and first in ALIASES:
        return f"{ALIASES[first]}.{rest}"
    return normalized


def fallback_source(api_name: str, obj: Any, source_error: Exception) -> tuple[str, str]:
    try:
        signature = str(inspect.signature(obj))
    except Exception:
        signature = "(signature unavailable)"
    doc = inspect.getdoc(obj) or pydoc.render_doc(obj, "Help on %s")
    fallback = f'''# Python source unavailable for {api_name}
#
# inspect.getsource({api_name}) failed because this object does not expose
# Python source in the current environment.
#
# Common reasons:
# - the object is implemented in C/C++/Rust/Fortran,
# - the object is a NumPy ufunc or builtin,
# - the package was installed without source files.
#
# Original inspect error:
# {source_error}
#
# Signature:
# {api_name}{signature}
#
# Docstring / help text:
"""
{doc}
"""
'''
    return fallback, (
        "Python source was not available, so the app loaded the object's signature and docstring/help text instead. "
        "For true source-code invariants, paste source manually."
    )


def resolve_source(object_name: str) -> dict[str, str]:
    normalized = normalize_object_name(object_name)
    if normalized in SOURCE_CACHE:
        return SOURCE_CACHE[normalized]

    parts = normalized.split(".")
    last_error: Exception | None = None
    for index in range(len(parts), 0, -1):
        module_name = ".".join(parts[:index])
        attr_parts = parts[index:]
        try:
            obj: Any = importlib.import_module(module_name)
            for attr in attr_parts:
                obj = getattr(obj, attr)
            try:
                result = {
                    "api_name": normalized,
                    "source_code": inspect.getsource(inspect.unwrap(obj)),
                    "source_kind": "source",
                    "warning": "",
                }
                SOURCE_CACHE[normalized] = result
                return result
            except Exception as source_error:
                source_code, warning = fallback_source(normalized, obj, source_error)
                result = {
                    "api_name": normalized,
                    "source_code": source_code,
                    "source_kind": "fallback",
                    "warning": warning,
                }
                SOURCE_CACHE[normalized] = result
                return result
        except Exception as exc:
            last_error = exc

    raise ValueError(
        f"Could not import or inspect {object_name}. Try a fully qualified name like numpy.linspace, "
        f"or paste the source code manually. Last error: {last_error}"
    )


def invariant_prompt(api_name: str, source_code: str) -> str:
    return f"""You are extracting candidate invariants for property-based testing and invariant-based documentation.

API name:
{api_name}

Source code:
{source_code}

Task:
Identify 5 to 8 high-value semantic invariants that are directly supported by the source code and its docstring.

Requirements:
- Focus on observable behavior users can rely on.
- Include preconditions when a property is not valid for every input.
- Prefer strong API contracts over vague restatements.
- Include edge cases suggested by branches, exceptions, dtype, shape, axis handling, return values, or version notes.
- Do not invent behavior not supported by the source code.
- Do not write tests.
- Include 1-based source line metadata when possible.

Return ONLY a JSON array. Each item should be:
{{"invariant": "...", "lineno": 10, "end_lineno": 14}}

Use the smallest line range that supports the invariant. If no specific line supports it, use null for lineno and end_lineno. No markdown, no commentary."""


def documentation_prompt(api_name: str, source_code: str, invariants: list[str], tone: str) -> str:
    return f"""You are a professional Python API documentation writer.

Generate publishable Markdown documentation for {api_name}.

Source code:
{source_code}

Human-approved semantic invariants:
{json.dumps(invariants, indent=2)}

Requested tone:
{tone}

Important:
- Do not mention GPT, prompts, validity scores, soundness scores, mutation scores, or testing methodology.
- Use the approved invariants as semantic guarantees.
- Derive the documentation from the source code, including docstring facts, branches, exceptions, and return behavior.
- Be careful around behavior that depends on dtype, endpoint, axis, version, platform, or input validity.

Output exactly this Markdown structure:

# {api_name}

## Overview

## Parameters

## Returns

## Raises

## Semantic Guarantees

## Edge Cases

## Examples

## Notes"""


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode("utf-8")
        return json.loads(raw or "{}")

    def send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_text_stream(self, generator) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        for chunk in generator:
            if not chunk:
                continue
            self.wfile.write(chunk.encode("utf-8"))
            self.wfile.flush()

    def do_POST(self) -> None:
        try:
            if self.path == "/api/source":
                payload = self.read_json()
                object_name = str(payload.get("object_name") or "")
                self.send_json(200, resolve_source(object_name))
                return

            if self.path == "/api/invariants":
                payload = self.read_json()
                api_name = str(payload.get("api_name") or "api.function")
                source_code = str(payload.get("source_code") or payload.get("documentation") or "")
                openai_key = str(payload.get("openai_key") or "")
                if not source_code.strip():
                    self.send_json(400, {"error": "Source code is required."})
                    return
                raw = run_project_gpt(invariant_prompt(api_name, source_code), openai_key)
                self.send_json(200, {"invariants": parse_json_array(raw), "model": MODEL})
                return

            if self.path == "/api/metrics":
                payload = self.read_json()
                api_name = str(payload.get("api_name") or "api.function")
                source_code = str(payload.get("source_code") or payload.get("documentation") or "")
                invariants = payload.get("invariants") or []
                openai_key = str(payload.get("openai_key") or "")
                show_mutation_tests = bool(payload.get("show_mutation_tests"))
                if not source_code.strip() or not isinstance(invariants, list):
                    self.send_json(400, {"error": "Source code and invariants are required."})
                    return
                cache_key = (METRICS_MODEL, source_code, json.dumps(invariants, sort_keys=True), show_mutation_tests)
                if cache_key not in METRICS_CACHE:
                    with request_openai_key(openai_key):
                        METRICS_CACHE[cache_key] = invariant_metrics_test(
                            source_code=source_code,
                            invariants=invariants,
                            model=METRICS_MODEL,
                            streaming=False,
                            api_name=api_name,
                            show_mutation_tests=show_mutation_tests,
                        )
                self.send_json(
                    200,
                    {
                        "metrics": METRICS_CACHE[cache_key]["results"],
                        "model": METRICS_MODEL,
                    },
                )
                return

            if self.path == "/api/mutation-analysis":
                payload = self.read_json()
                source_code = str(payload.get("source_code") or payload.get("documentation") or "")
                test_code = str(payload.get("test_code") or "")
                openai_key = str(payload.get("openai_key") or "")
                if not source_code.strip() or not test_code.strip():
                    self.send_json(400, {"error": "Source code and test code are required."})
                    return
                with request_openai_key(openai_key):
                    analysis = mutation_analysis_for_test(
                        source_code=source_code,
                        test_code=test_code,
                        model=METRICS_MODEL,
                    )
                self.send_json(200, {"analysis": analysis})
                return

            if self.path == "/api/rerun-test":
                payload = self.read_json()
                api_name = str(payload.get("api_name") or "api.function")
                source_code = str(payload.get("source_code") or payload.get("documentation") or "")
                invariant = str(payload.get("invariant") or "")
                test_code = str(payload.get("test_code") or "")
                if not source_code.strip() or not invariant.strip() or not test_code.strip():
                    self.send_json(400, {"error": "Source code, invariant, and test code are required."})
                    return
                result = evaluate_pbt_test(source_code, invariant, test_code, api_name=api_name)
                self.send_json(200, {"metric": result})
                return

            if self.path == "/api/documentation":
                payload = self.read_json()
                api_name = str(payload.get("api_name") or "api.function")
                source_code = str(payload.get("source_code") or payload.get("documentation") or "")
                invariants = payload.get("invariants") or []
                tone = str(payload.get("tone") or "contract")
                openai_key = str(payload.get("openai_key") or "")
                if not source_code.strip() or not isinstance(invariants, list):
                    self.send_json(400, {"error": "Source code and invariants are required."})
                    return
                markdown = strip_markdown_fences(
                    run_project_gpt(documentation_prompt(api_name, source_code, invariants, tone), openai_key)
                )
                self.send_json(200, {"markdown": markdown, "model": MODEL})
                return

            if self.path == "/api/documentation-stream":
                payload = self.read_json()
                api_name = str(payload.get("api_name") or "api.function")
                source_code = str(payload.get("source_code") or payload.get("documentation") or "")
                invariants = payload.get("invariants") or []
                tone = str(payload.get("tone") or "contract")
                openai_key = str(payload.get("openai_key") or "")
                if not source_code.strip() or not isinstance(invariants, list):
                    self.send_json(400, {"error": "Source code and invariants are required."})
                    return
                prompt = documentation_prompt(api_name, source_code, invariants, tone)
                self.send_text_stream(stream_project_gpt(prompt, openai_key))
                return

            self.send_json(404, {"error": "Unknown endpoint."})
        except Exception as exc:
            self.send_json(500, {"error": str(exc)})


def main() -> None:
    port = int(os.environ.get("PORT", "8011"))
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Invariant Documentation Studio running at http://127.0.0.1:{port}")
    print(f"OpenAI model: {MODEL}")
    server.serve_forever()


if __name__ == "__main__":
    main()
