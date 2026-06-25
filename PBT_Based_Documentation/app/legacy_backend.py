"""Shared backend logic migrated from server.py.

server.py is still kept as the original backup implementation.  This module
copies its non-HTTP behavior so the FastAPI routers can expose the same
/api/... contract without depending on SimpleHTTPRequestHandler.
"""

from __future__ import annotations

import importlib
import importlib.util
import inspect
import json
import os
import pydoc
import re
import sys
import urllib.error
import urllib.request
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

APP_DIR = Path(__file__).resolve().parent
ROOT = APP_DIR.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gpt_documentation_generator import response_text as project_response_text
from gpt_documentation_generator import strip_markdown_fences
from routers.model_api import DEFAULT_CMU_GATEWAY_BASE_URL, PROVIDERS


def _load_root_module(module_name: str, filename: str):
    """Load root-level modules even when an app router has the same name."""
    spec = importlib.util.spec_from_file_location(module_name, ROOT / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_metrics_module = _load_root_module("pbt_root_metrics", "metrics.py")
_coverage_module = _load_root_module("pbt_root_coverage", "coverage.py")

evaluate_pbt_test = _metrics_module.evaluate_pbt_test
invariant_metrics_test = _metrics_module.invariant_metrics_test
mutation_analysis_for_test = _metrics_module.mutation_analysis_for_test
assess_documentation_coverage = _coverage_module.assess_documentation_coverage

MODEL = os.environ.get("OPENAI_MODEL", "gpt-5.5")
METRICS_MODEL = os.environ.get("OPENAI_METRICS_MODEL", "gpt-5.4-mini")
OPENAI_SEED = 42

class _BoundedCache(dict):
    """A dict that evicts the oldest entry once it exceeds ``maxsize``.

    These caches live for the lifetime of the process, so without a cap they grow
    with every unique request and slowly leak memory (METRICS_CACHE in particular
    holds large mutation-analysis payloads). Dicts preserve insertion order, so
    evicting ``next(iter(self))`` drops the oldest entry.
    """

    def __init__(self, maxsize: int):
        super().__init__()
        self._maxsize = max(1, maxsize)

    def __setitem__(self, key, value):
        if key not in self and len(self) >= self._maxsize:
            del self[next(iter(self))]
        super().__setitem__(key, value)


GPT_CACHE: dict[tuple[str, str, int], str] = _BoundedCache(256)
METRICS_CACHE: dict[tuple[Any, ...], dict[str, Any]] = _BoundedCache(32)
SOURCE_CACHE: dict[str, dict[str, str]] = _BoundedCache(256)


def strip_fences(text: str) -> str:
    text = text.strip()
    match = re.fullmatch(r"```(?:json|markdown|md)?\s*(.*?)\s*```", text, re.S)
    return match.group(1).strip() if match else text


@contextmanager
def request_openai_key(openai_key: str | None):
    """Temporarily prefer a request-provided key over the process env key."""
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


def model_provider_config(
    payload: dict[str, Any],
    fallback_key: str | None = None,
    fallback_model: str = MODEL,
    model_field: str = "model",
) -> dict[str, str]:
    """Normalize provider/key/model fields while keeping openai_key compatible."""
    provider = str(payload.get("model_provider") or payload.get("provider") or "openai")
    if provider not in PROVIDERS:
        raise ValueError(f"Unknown model provider: {provider}")

    if model_field == "metrics_model":
        provider_model = PROVIDERS[provider].get("default_metrics_model")
    else:
        provider_model = PROVIDERS[provider].get("default_markdown_model") or PROVIDERS[provider].get("default_model")
    provider_model = provider_model or fallback_model
    requested_model = str(payload.get(model_field) or payload.get("model") or "").strip()
    config = {
        "provider": provider,
        "api_key": str(
            payload.get("api_key")
            or payload.get("model_api_key")
            or payload.get("openai_key")
            or fallback_key
            or ""
        ),
        "base_url": str(payload.get("base_url") or ""),
        "model": requested_model or str(provider_model or fallback_model),
    }

    if provider == "cmu_gateway":
        config["api_key"] = config["api_key"] or os.environ.get("CMU_AI_GATEWAY_API_KEY", "")
        config["base_url"] = (
            config["base_url"]
            or os.environ.get("CMU_AI_GATEWAY_BASE_URL", "")
            or DEFAULT_CMU_GATEWAY_BASE_URL
        )
        if "/ui/" in config["base_url"] or "login=" in config["base_url"]:
            raise ValueError(
                "CMU AI Gateway base_url must be the API endpoint, not the dashboard URL. "
                f"Use {DEFAULT_CMU_GATEWAY_BASE_URL} unless CMU lists a different OpenAI-compatible base URL."
            )
    elif provider == "claude":
        config["api_key"] = config["api_key"] or os.environ.get("ANTHROPIC_API_KEY", "")
        config["model"] = config["model"] or os.environ.get("ANTHROPIC_MODEL", "")

    return config


@contextmanager
def request_model_api(
    payload: dict[str, Any],
    fallback_key: str | None = None,
    fallback_model: str = MODEL,
    model_field: str = "model",
):
    """Apply request provider settings to the environment for existing wrappers.

    OpenAI and the CMU gateway are handled through OPENAI_API_KEY and
    OPENAI_BASE_URL. Claude uses ANTHROPIC_API_KEY in the direct Messages API
    helper below.
    """
    config = model_provider_config(
        payload,
        fallback_key=fallback_key,
        fallback_model=fallback_model,
        model_field=model_field,
    )
    provider = config["provider"]

    old_openai_key = os.environ.get("OPENAI_API_KEY")
    old_openai_base_url = os.environ.get("OPENAI_BASE_URL")
    old_anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    try:
        if provider == "claude":
            if not config["api_key"]:
                raise RuntimeError("Anthropic key is required. Paste a key or set ANTHROPIC_API_KEY.")
            os.environ["ANTHROPIC_API_KEY"] = config["api_key"]
        elif config["api_key"]:
            os.environ["OPENAI_API_KEY"] = config["api_key"]

        if provider == "cmu_gateway":
            if not config["api_key"]:
                raise RuntimeError("CMU AI Gateway key is required. Paste a key or set CMU_AI_GATEWAY_API_KEY.")
            if not config["base_url"]:
                raise RuntimeError("CMU AI Gateway base URL is required. Set CMU_AI_GATEWAY_BASE_URL or pass base_url.")
            os.environ["OPENAI_BASE_URL"] = config["base_url"]
        yield config
    finally:
        if old_openai_key is None:
            os.environ.pop("OPENAI_API_KEY", None)
        else:
            os.environ["OPENAI_API_KEY"] = old_openai_key

        if old_openai_base_url is None:
            os.environ.pop("OPENAI_BASE_URL", None)
        else:
            os.environ["OPENAI_BASE_URL"] = old_openai_base_url

        if old_anthropic_key is None:
            os.environ.pop("ANTHROPIC_API_KEY", None)
        else:
            os.environ["ANTHROPIC_API_KEY"] = old_anthropic_key


def anthropic_response_text(model: str, prompt: str, api_key: str, max_tokens: int = 4096) -> str:
    """Call Anthropic's Messages API without adding a hard SDK dependency."""
    body = json.dumps(
        {
            "model": model,
            "max_tokens": max_tokens,
            "system": "You are a careful Python property-based testing and API documentation assistant.",
            "messages": [{"role": "user", "content": prompt}],
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=body,
        headers={
            "content-type": "application/json",
            "anthropic-version": "2023-06-01",
            "x-api-key": api_key,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        error_text = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Anthropic API error {exc.code}: {error_text}") from exc

    chunks: list[str] = []
    for block in data.get("content", []) or []:
        if block.get("type") == "text":
            chunks.append(block.get("text", ""))
    return "".join(chunks)


def prefers_chat_completions(config: dict[str, Any]) -> bool:
    """Whether to call Chat Completions instead of the Responses API.

    OpenAI's native API supports the newer Responses API, but OpenAI-compatible
    gateways (such as the CMU AI Gateway) generally implement only Chat
    Completions. Calling ``responses.create`` against them returns a 404, so any
    provider that is not native OpenAI -- or anything pointed at a custom
    base_url -- must use Chat Completions.
    """
    return config.get("provider") != "openai" or bool(config.get("base_url"))


def request_seed(payload: dict[str, Any]) -> int:
    try:
        return int(payload.get("openai_seed", OPENAI_SEED))
    except (TypeError, ValueError):
        return OPENAI_SEED


def run_project_gpt(prompt: str, openai_key: str | None, seed: int = OPENAI_SEED, payload: dict[str, Any] | None = None) -> str:
    payload = payload or {}
    config = model_provider_config(payload, fallback_key=openai_key, model_field="markdown_model")
    if config["provider"] == "openai" and not config["api_key"] and not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("Paste an OpenAI API key or set OPENAI_API_KEY before starting the FastAPI server.")
    cache_key = (config["provider"], config["model"], config["base_url"], prompt, seed)
    if cache_key in GPT_CACHE:
        return GPT_CACHE[cache_key]
    with request_model_api(payload, fallback_key=openai_key, model_field="markdown_model") as active_config:
        if active_config["provider"] == "claude":
            text = anthropic_response_text(active_config["model"], prompt, active_config["api_key"])
        else:
            text = project_response_text(
                active_config["model"],
                prompt,
                stream=False,
                seed=seed,
                prefer_chat_completions=prefers_chat_completions(active_config),
            )
    GPT_CACHE[cache_key] = text
    return text


def stream_project_gpt(prompt: str, openai_key: str | None, seed: int = OPENAI_SEED, payload: dict[str, Any] | None = None) -> Iterator[str]:
    payload = payload or {}
    config = model_provider_config(payload, fallback_key=openai_key, model_field="markdown_model")
    if config["provider"] == "openai" and not config["api_key"] and not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("Paste an OpenAI API key or set OPENAI_API_KEY before starting the FastAPI server.")
    cache_key = (config["provider"], config["model"], config["base_url"], prompt, seed)
    if cache_key in GPT_CACHE:
        yield GPT_CACHE[cache_key]
        return

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("Install the openai package with: python3 -m pip install openai") from exc

    chunks: list[str] = []
    with request_model_api(payload, fallback_key=openai_key, model_field="markdown_model") as active_config:
        if active_config["provider"] == "claude":
            text = anthropic_response_text(active_config["model"], prompt, active_config["api_key"])
            chunks.append(text)
            yield text
            GPT_CACHE[cache_key] = text
            return

        client = OpenAI()
        if not prefers_chat_completions(active_config) and hasattr(client, "responses"):
            events = client.responses.create(model=active_config["model"], input=prompt, stream=True)
            for event in events:
                if getattr(event, "type", "") == "response.output_text.delta":
                    chunks.append(event.delta)
                    yield event.delta
        else:
            events = client.chat.completions.create(
                model=active_config["model"],
                messages=[
                    {
                        "role": "system",
                        "content": "You are a careful Python property-based testing and API documentation assistant.",
                    },
                    {"role": "user", "content": prompt},
                ],
                stream=True,
                seed=seed,
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


def traditional_markdown_prompt(api_name: str, source_code: str, traditional_docs: str) -> str:
    return f"""You are a professional Python API documentation editor.

Convert the provided traditional/reference documentation for {api_name} into clean, publishable Markdown.

Source code for context:
{source_code}

Traditional/reference documentation to convert:
{traditional_docs}

Important:
- Preserve the factual content from the provided traditional/reference documentation.
- Do not add invariant-based claims, testing methodology, Elo scores, arena labels, GPT wording, or research-study wording.
- Do not invent behavior not present in the provided documentation or source code.
- Remove source URLs and navigation clutter.
- Keep the result useful as the baseline/original documentation side of a blind comparison.

Output Markdown only."""


def generate_invariants(payload: dict[str, Any]) -> dict[str, Any]:
    api_name = str(payload.get("api_name") or "api.function")
    source_code = str(payload.get("source_code") or payload.get("documentation") or "")
    if not source_code.strip():
        raise ValueError("Source code is required.")
    raw = run_project_gpt(
        invariant_prompt(api_name, source_code),
        str(payload.get("openai_key") or ""),
        seed=request_seed(payload),
        payload=payload,
    )
    return {"invariants": parse_json_array(raw), "model": model_provider_config(payload, model_field="markdown_model")["model"]}


def generate_metrics(payload: dict[str, Any]) -> dict[str, Any]:
    api_name = str(payload.get("api_name") or "api.function")
    source_code = str(payload.get("source_code") or payload.get("documentation") or "")
    invariants = payload.get("invariants") or []
    if not source_code.strip() or not isinstance(invariants, list):
        raise ValueError("Source code and invariants are required.")

    # Mutation testing is slower because it shells out to pytest/mutmut. The
    # metrics layer batches generated tests into one mutmut run; the legacy
    # run_mutation_in_overall flag is still accepted for old callers.
    show_mutation_tests = bool(payload.get("show_mutation_tests") or payload.get("run_mutation_in_overall"))
    mutation_packages = str(payload.get("mutation_packages") or "")
    mutation_auto_install = bool(payload.get("mutation_auto_install", True))
    seed = request_seed(payload)
    config = model_provider_config(payload, fallback_model=METRICS_MODEL, model_field="metrics_model")
    if config["provider"] == "claude":
        raise ValueError("Claude is wired for invariant/documentation generation, but metrics still require GPT/OpenAI or an OpenAI-compatible gateway.")
    if not invariants:
        return {"metrics": [], "model": config["model"]}
    cache_key = (
        config["provider"],
        config["model"],
        config["base_url"],
        source_code,
        json.dumps(invariants, sort_keys=True),
        show_mutation_tests,
        mutation_packages,
        mutation_auto_install,
        seed,
    )
    if cache_key not in METRICS_CACHE:
        with request_model_api(
            payload,
            fallback_key=str(payload.get("openai_key") or ""),
            fallback_model=METRICS_MODEL,
            model_field="metrics_model",
        ) as active_config:
            METRICS_CACHE[cache_key] = invariant_metrics_test(
                source_code=source_code,
                invariants=invariants,
                model=active_config.get("model") or METRICS_MODEL,
                streaming=False,
                api_name=api_name,
                show_mutation_tests=show_mutation_tests,
                mutation_packages=mutation_packages,
                mutation_auto_install=mutation_auto_install,
                seed=seed,
            )
    return {"metrics": METRICS_CACHE[cache_key]["results"], "model": config["model"]}


def generate_mutation_analysis(payload: dict[str, Any]) -> dict[str, Any]:
    api_name = str(payload.get("api_name") or "api.function")
    source_code = str(payload.get("source_code") or payload.get("documentation") or "")
    test_code = str(payload.get("test_code") or "")
    if not source_code.strip() or not test_code.strip():
        raise ValueError("Source code and test code are required.")
    if model_provider_config(payload, fallback_model=METRICS_MODEL, model_field="metrics_model")["provider"] == "claude":
        raise ValueError("Claude mutation analysis is not wired yet; use GPT/OpenAI or the CMU gateway for metrics.")
    with request_model_api(
        payload,
        fallback_key=str(payload.get("openai_key") or ""),
        fallback_model=METRICS_MODEL,
        model_field="metrics_model",
    ) as active_config:
        analysis = mutation_analysis_for_test(
            source_code=source_code,
            test_code=test_code,
            api_name=api_name,
            model=active_config.get("model") or METRICS_MODEL,
            mutation_packages=str(payload.get("mutation_packages") or ""),
            mutation_auto_install=bool(payload.get("mutation_auto_install", True)),
            seed=request_seed(payload),
        )
    return analysis if isinstance(analysis, dict) else {"analysis": analysis, "mutants": []}


def rerun_test(payload: dict[str, Any]) -> dict[str, Any]:
    api_name = str(payload.get("api_name") or "api.function")
    source_code = str(payload.get("source_code") or payload.get("documentation") or "")
    invariant = str(payload.get("invariant") or "")
    test_code = str(payload.get("test_code") or "")
    if not source_code.strip() or not invariant.strip() or not test_code.strip():
        raise ValueError("Source code, invariant, and test code are required.")
    result = evaluate_pbt_test(source_code, invariant, test_code, api_name=api_name)
    return {"metric": result}


def generate_coverage(payload: dict[str, Any]) -> dict[str, Any]:
    source_code = str(payload.get("source_code") or payload.get("documentation") or "")
    docs = str(payload.get("docs") or payload.get("markdown") or "")
    openai_key = str(payload.get("openai_key") or "")
    config = model_provider_config(payload, fallback_key=openai_key, fallback_model=METRICS_MODEL, model_field="metrics_model")
    if not source_code.strip() or not docs.strip():
        raise ValueError("Source code and documentation are required.")
    if config["provider"] == "claude":
        raise ValueError("Claude coverage assessment is not wired yet; use GPT/OpenAI or the CMU gateway for coverage.")
    if config["provider"] == "openai" and not config["api_key"] and not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("OpenAI key is required for coverage assessment. Paste a key or set OPENAI_API_KEY.")
    with request_model_api(payload, fallback_key=openai_key, fallback_model=METRICS_MODEL, model_field="metrics_model") as active_config:
        return assess_documentation_coverage(
            documentation=docs,
            source_code=source_code,
            model=active_config.get("model") or METRICS_MODEL,
            seed=request_seed(payload),
        )


def generate_documentation(payload: dict[str, Any]) -> dict[str, Any]:
    api_name = str(payload.get("api_name") or "api.function")
    source_code = str(payload.get("source_code") or payload.get("documentation") or "")
    invariants = payload.get("invariants") or []
    if not source_code.strip() or not isinstance(invariants, list):
        raise ValueError("Source code and invariants are required.")
    markdown = strip_markdown_fences(
        run_project_gpt(
            documentation_prompt(api_name, source_code, invariants, str(payload.get("tone") or "contract")),
            str(payload.get("openai_key") or ""),
            seed=request_seed(payload),
            payload=payload,
        )
    )
    return {"markdown": markdown, "model": model_provider_config(payload, model_field="markdown_model")["model"]}


def generate_traditional_markdown(payload: dict[str, Any]) -> dict[str, Any]:
    api_name = str(payload.get("api_name") or "api.function")
    source_code = str(payload.get("source_code") or payload.get("documentation") or "")
    traditional_docs = str(payload.get("td_text") or payload.get("traditional_docs") or payload.get("TD_md") or "")
    if not traditional_docs.strip():
        raise ValueError("Traditional documentation text is required.")
    markdown = strip_markdown_fences(
        run_project_gpt(
            traditional_markdown_prompt(api_name, source_code, traditional_docs),
            str(payload.get("openai_key") or ""),
            seed=request_seed(payload),
            payload=payload,
        )
    )
    return {"markdown": markdown, "model": model_provider_config(payload, model_field="markdown_model")["model"]}


def stream_documentation(payload: dict[str, Any]) -> Iterator[str]:
    api_name = str(payload.get("api_name") or "api.function")
    source_code = str(payload.get("source_code") or payload.get("documentation") or "")
    invariants = payload.get("invariants") or []
    if not source_code.strip() or not isinstance(invariants, list):
        raise ValueError("Source code and invariants are required.")
    prompt = documentation_prompt(api_name, source_code, invariants, str(payload.get("tone") or "contract"))
    yield from stream_project_gpt(prompt, str(payload.get("openai_key") or ""), seed=request_seed(payload), payload=payload)
