from __future__ import annotations

import json
import os
import re
from contextlib import contextmanager
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from gpt_documentation_generator import response_text as project_response_text
from gpt_documentation_generator import strip_markdown_fences


ROOT = Path(__file__).resolve().parent
MODEL = os.environ.get("OPENAI_MODEL", "gpt-5.5")


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
    with request_openai_key(openai_key):
        return project_response_text(MODEL, prompt, stream=False)


def parse_json_array(text: str) -> list[str]:
    text = strip_fences(text)
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\[[\s\S]*\]", text)
        if not match:
            raise
        data = json.loads(match.group(0))
    if not isinstance(data, list) or not all(isinstance(item, str) for item in data):
        raise ValueError("Expected a JSON array of strings.")
    return data


def invariant_prompt(api_name: str, documentation: str) -> str:
    return f"""You are extracting candidate invariants for property-based testing and invariant-based documentation.

API name:
{api_name}

Existing documentation:
{documentation}

Task:
Identify 5 to 8 high-value semantic invariants that are directly supported by the documentation.

Requirements:
- Focus on observable behavior users can rely on.
- Include preconditions when a property is not valid for every input.
- Prefer strong API contracts over vague restatements.
- Include edge cases suggested by parameters, return values, examples, dtype, shape, axis, or version notes.
- Do not invent behavior not supported by the documentation.
- Do not write tests.

Return ONLY a JSON array of strings. No markdown, no commentary."""


def documentation_prompt(api_name: str, documentation: str, invariants: list[str], tone: str) -> str:
    return f"""You are a professional Python API documentation writer.

Generate publishable Markdown documentation for {api_name}.

Existing documentation:
{documentation}

Human-approved semantic invariants:
{json.dumps(invariants, indent=2)}

Requested tone:
{tone}

Important:
- Do not mention GPT, prompts, validity scores, soundness scores, mutation scores, or testing methodology.
- Use the approved invariants as semantic guarantees.
- Preserve useful factual details from the original documentation.
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

    def do_POST(self) -> None:
        try:
            if self.path == "/api/invariants":
                payload = self.read_json()
                api_name = str(payload.get("api_name") or "api.function")
                documentation = str(payload.get("documentation") or "")
                openai_key = str(payload.get("openai_key") or "")
                if not documentation.strip():
                    self.send_json(400, {"error": "Documentation is required."})
                    return
                raw = run_project_gpt(invariant_prompt(api_name, documentation), openai_key)
                self.send_json(200, {"invariants": parse_json_array(raw), "model": MODEL})
                return

            if self.path == "/api/documentation":
                payload = self.read_json()
                api_name = str(payload.get("api_name") or "api.function")
                documentation = str(payload.get("documentation") or "")
                invariants = payload.get("invariants") or []
                tone = str(payload.get("tone") or "contract")
                openai_key = str(payload.get("openai_key") or "")
                if not documentation.strip() or not isinstance(invariants, list):
                    self.send_json(400, {"error": "Documentation and invariants are required."})
                    return
                markdown = strip_markdown_fences(
                    run_project_gpt(documentation_prompt(api_name, documentation, invariants, tone), openai_key)
                )
                self.send_json(200, {"markdown": markdown, "model": MODEL})
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
