from openai import OpenAI
import os, subprocess, inspect 
import json

def find_documentation_coverage(documentation, source_code, model="gpt-5.5", streaming=True):
    """This function, for each key section of the documentation, calls GPT and lets it assess the coverage of the documentation back to the sourc
    code. Both the documentation and source_code should be expressed as strings.

    Returns a valid JSON to be used...
    """
    source_code_w_lineno = ""
    # Populate the source code with line numbers
    for idx, line in enumerate(source_code.strip().splitlines()):
        lineno = f"{idx+1}: {line}\n"
        source_code_w_lineno += lineno 

    PROMPT = f"""
    You are an expert software engineer.

    Your task is to determine which lines of source code are explained or covered by the documentation.

    For EACH documentation statement:

    1. Identify the source code lines whose behavior is described.
    2. Include all relevant lines necessary to understand the behavior.
    3. Do NOT include unrelated implementation details.
    4. If a statement is not supported by the source code, return an empty list.
    5. Use exact line numbers from the provided source code.
    6. Be conservative. Only map lines when there is clear evidence.

    Return ONLY valid JSON.

    Format:

    [
        {{
            "documentation": "<documentation statement>",
            "covered_lines": [12, 13, 14],
            "confidence": "HIGH"
        }},
        {{
            "documentation": "<documentation statement>",
            "covered_lines": [27, 28],
            "confidence": "MEDIUM"
        }}
    ]

    SOURCE CODE:
    ----------------
    {source_code_w_lineno}

    DOCUMENTATION:
    ----------------
    {documentation}
    """

    # Call the model :D 
    client = OpenAI()
    # No streaming, display all at once 
    if not streaming:
        response = client.responses.create(
            model=model,
            input=PROMPT,
            streaming=False,
        )
        output = response.output_text
    
    # Streaming, display gradually
    else:
        chunks = []
        events = client.responses.create(
            model=model,
            input=PROMPT,
            streaming=True
        )
        for event in events:
            if event.type == "responses.output_text.delta":
                print(event.delta, end="", flush=True)
                chunks.append(event.delta)
        output = "".join(chunks)
    # output should be a json file
    data = json.loads(output)
    return data



def create_heatmap_and_bar(output_json, source_code, documentation, mode="dark"):
    """This function uses the output json to create a bar showing % of source code covered by documentation and 
    when users highlight over specific areas of a documentation, shows the coresponding lines in the source code
    """

    if mode == "dark":
        line_color = "#ff9b58"
    else:
        line_color = "#596f5f"
    
    # (documentation, docs, confidence)
    output = []
    # if documentation line was already analyzed no need
    seen_docs = set()

    for section in output_json:
        docs = section["documentation"]
        covered_lines = section["covered_lines"]
        confidence = section["confidence"]

        temp = (docs, covered_lines, confidence)
        output.append(temp)
    
    return output, line_color

def find_covered(data, source_code):
    """function assess the metrics given a json file"""
    total_lines = 0
    covered_lines = 0
    seen = set()

    for idx, lineno in enumerate(source_code.strip().splitlines()):
        total_lines += 1
    
    for item in data:
        linenos = item["covered_lines"]
        for line in linenos:
            if line not in seen:
                seen.add(line)
                covered_lines += 1
    return total_lines, covered_lines, seen




# Stable app-facing wrapper used by the local web UI. The prototype helpers above
# are intentionally left in place; this function packages the same coverage idea
# into a predictable JSON shape for the frontend.
def _parse_json_array(text):
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        import re
        match = re.search(r"\[[\s\S]*\]", text or "")
        if not match:
            raise
        data = json.loads(match.group(0))
    if not isinstance(data, list):
        raise ValueError("Expected a JSON array from documentation coverage assessment.")
    return data


def _normalize_coverage_entries(raw_entries, source_line_count, coverable_lines=None):
    entries = []
    covered = set()
    for index, item in enumerate(raw_entries or []):
        if not isinstance(item, dict):
            continue
        statement = str(
            item.get("documentation_statement")
            or item.get("statement")
            or item.get("docs")
            or item.get("documentation")
            or ""
        ).strip()
        raw_lines = item.get("covered_lines") or item.get("lines") or []
        if isinstance(raw_lines, int):
            raw_lines = [raw_lines]
        normalized_lines = []
        for raw_line in raw_lines:
            try:
                line_number = int(raw_line)
            except (TypeError, ValueError):
                continue
            if not (1 <= line_number <= source_line_count):
                continue
            # Drop mappings to docstrings, comments, and blank lines so the
            # documentation cannot claim coverage of non-coverable source.
            if coverable_lines is not None and line_number not in coverable_lines:
                continue
            if line_number not in normalized_lines:
                normalized_lines.append(line_number)
                covered.add(line_number)
        confidence = str(item.get("confidence") or "MEDIUM").upper()
        if confidence not in {"HIGH", "MEDIUM", "LOW"}:
            confidence = "MEDIUM"
        entries.append({
            "id": f"coverage-{index + 1}",
            "statement": statement,
            "covered_lines": normalized_lines,
            "confidence": confidence,
        })
    return entries, covered


def assess_documentation_coverage(documentation, source_code, model="gpt-5.4-mini", seed=42):
    """Assess how much source behavior is covered by documentation.

    Returns a JSON-serializable dict for the app:
    - coverage_percent: percent of non-empty source lines mapped by at least one doc statement
    - entries: documentation statements with source line mappings
    - source_lines: numbered source lines for heatmap rendering
    """
    source_lines_raw = source_code.strip("\n").splitlines()
    numbered_source = "\n".join(
        f"{index}: {line}" for index, line in enumerate(source_lines_raw, start=1)
    )
    prompt = f"""You are an expert software engineer assessing documentation coverage.

Determine which lines of source code are explained or covered by the documentation.
For EACH meaningful documentation statement:
1. Identify the source code lines whose behavior is described.
2. Include all relevant lines necessary to understand that behavior.
3. Do NOT include unrelated implementation details.
4. If the statement is unsupported by the source, return an empty covered_lines list.
5. Use exact 1-based line numbers from the provided source code.
6. Be conservative. Only map lines when there is clear evidence.
7. Map ONLY to executable source lines. Never map to docstring lines,
   comment lines, or blank lines, even when they describe the behavior.

Return ONLY valid JSON, as an array of objects:
[
  {{
    "documentation_statement": "The documentation claim or sentence.",
    "covered_lines": [12, 13, 14],
    "confidence": "HIGH"
  }}
]

SOURCE CODE WITH LINE NUMBERS:
----------------
{numbered_source}

DOCUMENTATION:
----------------
{documentation}
"""
    client = OpenAI()
    response = client.responses.create(
        model=model,
        input=prompt,
    )
    coverable_lines = _coverable_source_lines(source_code)
    raw_entries = _parse_json_array(response.output_text)
    entries, covered_lines = _normalize_coverage_entries(
        raw_entries, len(source_lines_raw), coverable_lines
    )

    # covered_lines is already restricted to coverable lines, so docstrings,
    # comments, and blank lines count toward neither numerator nor denominator.
    total_coverable = len(coverable_lines)
    coverage_percent = round((len(covered_lines) / total_coverable) * 100, 1) if total_coverable else 0

    return {
        "coverage_percent": coverage_percent,
        "covered_line_count": len(covered_lines),
        "total_line_count": total_coverable,
        "covered_lines": sorted(covered_lines),
        "coverable_lines": sorted(coverable_lines),
        "source_lines": [
            {
                "line": index,
                "text": line,
                "covered": index in covered_lines,
                "coverable": index in coverable_lines,
                "blank": not line.strip(),
            }
            for index, line in enumerate(source_lines_raw, start=1)
        ],
        "entries": entries,
        "model": model,
    }


def _docstring_line_numbers(source_code):
    import ast
    docstring_lines = set()
    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        return docstring_lines

    def visit_body(body):
        if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant) and isinstance(body[0].value.value, str):
            start = getattr(body[0], "lineno", None)
            end = getattr(body[0], "end_lineno", start)
            if start:
                docstring_lines.update(range(start, (end or start) + 1))
        for node in body:
            child_body = getattr(node, "body", None)
            if isinstance(child_body, list):
                visit_body(child_body)
    visit_body(getattr(tree, "body", []))
    return docstring_lines


def _coverable_source_lines(source_code):
    """Return source lines that should count toward documentation coverage.

    The heatmap still displays every line, but the denominator should not punish
    the documentation for blank lines, comments, or giant embedded docstrings.
    """
    # Normalize identically to the numbered source sent to the model so that
    # ast line numbers align with the 1-based heatmap line numbers.
    normalized = source_code.strip("\n")
    docstring_lines = _docstring_line_numbers(normalized)
    coverable = set()
    for index, line in enumerate(normalized.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or index in docstring_lines:
            continue
        coverable.add(index)
    return coverable
