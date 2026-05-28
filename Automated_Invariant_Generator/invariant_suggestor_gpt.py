#!/usr/bin/env python3

import os
import sys
from openai import OpenAI

MODEL = "gpt-5.4-mini"  # change to "gpt-5.5", "gpt-5-mini", etc.
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

highlighted_documentation = sys.stdin.read()

prompt = f"""
You are a world-class Python programmer that rarely makes mistakes.
Suggest up to 5 sound property-based testing invariants based on the selected Python API function documentation.

Rules:
- Output Python.
- Write Python Hypothesis tests, invariants, and generators.
- Import all necessary libraries.
- Prefer specific semantic properties.
- Mark risky or conditional properties.
- Think of novel properties that are good for testing.
- Make sure tests are valid and sound.
- Add medium amount of comments.
- DO NOT BE TALKATIVE. Only give the code, do not give ```python``` type output. ONLY CODE

Selected documentation:
{highlighted_documentation}
"""

stream = client.responses.create(
    model=MODEL,
    input=prompt,
    stream=True,
)

chunks = []

for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
        chunks.append(event.delta)

output = "".join(chunks)

# Optional cleanup if model outputs markdown fences
output = output.replace("```python", "")
output = output.replace("```", "").strip()
