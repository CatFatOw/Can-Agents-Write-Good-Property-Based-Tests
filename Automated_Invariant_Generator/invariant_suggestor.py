#!/usr/bin/env python3

import sys
import json
import requests

MODEL = "qwen2.5-coder:14b"
OLLAMA_URL = "http://localhost:11434/api/generate"

highlighted_documentation = sys.stdin.read()

SYSTEM_PROMPT = f"""
You are a world-class Python programmer that rarely makes mistakes.
Suggest up to 5 sound property-based testing invariants based on the selected Python API function documentation.

Rules:
- Output Python.
- Write Python Hypothesis tests, invariants, and generators. Make sure you import all necessary libraries
- Prefer specific semantic properties.
- Mark risky or conditional properties.
- Think of novel properties that are good for testing.
- Make sure tests are valid and sound.
- Add medium amount of comments
- DO NOT BE TALKATIVE. Only give the code, do not give ```python``` type output. ONLY CODE

Selected documentation:
{highlighted_documentation}
"""

response = requests.post(
    OLLAMA_URL,
    json={
        "model": MODEL,
        "prompt": SYSTEM_PROMPT,
        "stream": True,
    },
    stream=True,
    timeout=120,
)

response.raise_for_status()

chunks = []

for line in response.iter_lines():
    if not line:
        continue

    data = json.loads(line.decode("utf-8"))

    if "response" in data:
        chunks.append(data["response"])

    if data.get("done"):
        break

# Combine streamed chunks
output = "".join(chunks)

# Remove markdown fences
output = output.replace("```python", "")
output = output.replace("```", "")

print(output.strip())