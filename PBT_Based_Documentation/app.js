const form = document.querySelector("#documentation-form");
const documentationInput = document.querySelector("#documentation");
const apiNameInput = document.querySelector("#api-name");
const toneInput = document.querySelector("#tone");
const openaiKeyInput = document.querySelector("#openai-key");
const reviewPanel = document.querySelector("#review-panel");
const comparePanel = document.querySelector("#compare-panel");
const originalDoc = document.querySelector("#original-doc");
const generatedDoc = document.querySelector("#generated-doc");
const outputTitle = document.querySelector("#output-title");
const outputEyebrow = document.querySelector("#output-eyebrow");
const flowStatus = document.querySelector("#flow-status");
const copyButton = document.querySelector("#copy-button");
const runButton = document.querySelector("#run-button");
const stepTabs = Array.from(document.querySelectorAll(".step-tab"));
const examples = document.querySelector("#prompt-examples");

let currentMarkdown = "";
let currentInvariants = [];

const exampleDocs = {
  "numpy-linspace": {
    api: "numpy.linspace",
    text: `# numpy.linspace

\`numpy.linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None, axis=0, *, device=None)\` [source]

Return evenly spaced numbers over a specified interval.

Returns \`num\` evenly spaced samples, calculated over the interval \`[start, stop]\`.

The endpoint of the interval can optionally be excluded.

Changed in version 1.20.0: Values are rounded towards \`-inf\` instead of \`0\` when an integer dtype is specified. The old behavior can still be obtained with \`np.linspace(start, stop, num).astype(np.int_)\`.

## Parameters

### start : array_like

The starting value of the sequence.

### stop : array_like

The end value of the sequence, unless \`endpoint\` is set to \`False\`. In that case, the sequence consists of all but the last of \`num + 1\` evenly spaced samples, so that \`stop\` is excluded. Note that the step size changes when \`endpoint\` is \`False\`.

### num : int, optional

Number of samples to generate. Default is \`50\`. Must be non-negative.

### endpoint : bool, optional

If \`True\`, \`stop\` is the last sample. Otherwise, it is not included. Default is \`True\`.

### retstep : bool, optional

If \`True\`, return \`(samples, step)\`, where \`step\` is the spacing between samples.

### dtype : dtype, optional

The type of the output array. If \`dtype\` is not given, the data type is inferred from \`start\` and \`stop\`. The inferred dtype will never be an integer; float is chosen even if the arguments would produce an array of integers.

### axis : int, optional

The axis in the result to store the samples. Relevant only if \`start\` or \`stop\` are array-like. By default \`0\`, the samples will be along a new axis inserted at the beginning. Use \`-1\` to get an axis at the end.

### device : str, optional

The device on which to place the created array. Default: \`None\`. For Array-API interoperability only, so must be \`"cpu"\` if passed.

New in version 2.0.0.

## Returns

### samples : ndarray

There are \`num\` equally spaced samples in the closed interval \`[start, stop]\` or the half-open interval \`[start, stop)\`, depending on whether \`endpoint\` is \`True\` or \`False\`.

### step : float, optional

Only returned if \`retstep\` is \`True\`.

Size of spacing between samples.

## See also

- \`arange\`: Similar to \`linspace\`, but uses a step size instead of the number of samples.
- \`geomspace\`: Similar to \`linspace\`, but with numbers spaced evenly on a log scale, a geometric progression.
- \`logspace\`: Similar to \`geomspace\`, but with the end points specified as logarithms.
- How to create arrays with regularly-spaced values.

## Examples

Try it in your browser!

\`\`\`python
import numpy as np

np.linspace(2.0, 3.0, num=5)
# array([2.  , 2.25, 2.5 , 2.75, 3.  ])

np.linspace(2.0, 3.0, num=5, endpoint=False)
# array([2. ,  2.2,  2.4,  2.6,  2.8])

np.linspace(2.0, 3.0, num=5, retstep=True)
# (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)
\`\`\`

## Graphical illustration

\`\`\`python
import matplotlib.pyplot as plt
import numpy as np

N = 8
y = np.zeros(N)
x1 = np.linspace(0, 10, N, endpoint=True)
x2 = np.linspace(0, 10, N, endpoint=False)

plt.plot(x1, y, 'o')
# [<matplotlib.lines.Line2D object at 0x...>]

plt.plot(x2, y + 0.5, 'o')
# [<matplotlib.lines.Line2D object at 0x...>]

plt.ylim([-0.5, 1])
# (-0.5, 1)

plt.show()
\`\`\``
  }
};

function escapeHtml(value) {
  return value.replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;"
  }[char]));
}

function setStage(stage) {
  document.body.classList.remove("stage-input", "stage-review", "stage-compare");
  document.body.classList.add(`stage-${stage}`);
  stepTabs.forEach((tab) => {
    const active = tab.dataset.step === stage;
    tab.classList.toggle("is-active", active);
    tab.setAttribute("aria-current", active ? "step" : "false");
  });
}

function setStatus(mode, label) {
  flowStatus.dataset.mode = mode;
  flowStatus.querySelector("span:last-child").textContent = label;
}

async function postJson(path, payload) {
  const response = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      ...payload,
      openai_key: openaiKeyInput.value.trim()
    })
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Request failed.");
  }
  return data;
}

function renderError(message) {
  reviewPanel.classList.remove("is-hidden");
  comparePanel.classList.add("is-hidden");
  reviewPanel.innerHTML = `
    <div class="review-copy">
      <p class="eyebrow">GPT call failed</p>
      <h3>Could not run the pipeline</h3>
      <p>${escapeHtml(message)}</p>
    </div>
  `;
  outputEyebrow.textContent = "Needs attention";
  outputTitle.textContent = "Backend error";
  setStatus("draft", "Check key");
}

function renderInvariantReview(invariants) {
  const items = invariants.map((invariant, index) => `
    <label class="invariant-item">
      <input type="checkbox" checked data-index="${index}">
      <span>${escapeHtml(invariant)}</span>
    </label>
  `).join("");

  reviewPanel.innerHTML = `
    <div class="review-copy">
      <p class="eyebrow">Human review required</p>
      <h3>Approve the invariants</h3>
      <p>Uncheck any claim that feels too strong, vague, or not supported by the documentation.</p>
    </div>
    <div class="invariant-list">${items}</div>
    <button type="button" class="approve-button" id="approve-button">Looks good, generate Markdown</button>
  `;

  document.querySelector("#approve-button").addEventListener("click", generateMarkdownFromReview);
}

async function generateMarkdownFromReview() {
  const apiName = apiNameInput.value.trim() || "api.function";
  const accepted = Array.from(reviewPanel.querySelectorAll("input[type='checkbox']"))
    .filter((input) => input.checked)
    .map((input) => currentInvariants[Number(input.dataset.index)]);

  const approveButton = document.querySelector("#approve-button");
  approveButton.disabled = true;
  approveButton.textContent = "Calling GPT...";
  setStatus("review", "Writing MD");

  try {
    const data = await postJson("/api/documentation", {
      api_name: apiName,
      documentation: documentationInput.value.trim(),
      invariants: accepted,
      tone: toneInput.value
    });
    currentMarkdown = data.markdown;
    originalDoc.textContent = documentationInput.value.trim();
    generatedDoc.textContent = currentMarkdown;
    reviewPanel.classList.add("is-hidden");
    comparePanel.classList.remove("is-hidden");
    outputEyebrow.textContent = "Markdown comparison";
    outputTitle.textContent = "Before and after";
    copyButton.disabled = false;
    setStage("compare");
    setStatus("ready", "MD ready");
  } catch (error) {
    renderError(error.message || "Documentation generation failed.");
  } finally {
    approveButton.disabled = false;
    approveButton.textContent = "Looks good, generate Markdown";
  }
}

examples.addEventListener("click", (event) => {
  const button = event.target.closest("[data-example]");
  if (!button) return;
  const example = exampleDocs[button.dataset.example];
  documentationInput.value = example.text;
  apiNameInput.value = example.api;
  documentationInput.focus();
  setStage("input");
  setStatus("draft", "Example loaded");
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const docText = documentationInput.value.trim();
  const apiName = apiNameInput.value.trim() || "api.function";
  if (!docText) return;

  runButton.disabled = true;
  runButton.textContent = "Calling GPT...";
  comparePanel.classList.add("is-hidden");
  reviewPanel.classList.remove("is-hidden");
  reviewPanel.innerHTML = '<p class="placeholder">Calling the project GPT pipeline for candidate invariants...</p>';
  outputEyebrow.textContent = "Review invariants";
  outputTitle.textContent = "Check the claims";
  copyButton.disabled = true;
  setStage("review");
  setStatus("review", "Calling GPT");

  try {
    const data = await postJson("/api/invariants", {
      api_name: apiName,
      documentation: docText
    });
    currentInvariants = data.invariants;
    renderInvariantReview(currentInvariants);
    setStatus("review", "Check invariants");
  } catch (error) {
    renderError(error.message || "Invariant extraction failed.");
  } finally {
    runButton.disabled = false;
    runButton.innerHTML = '<span class="button-icon" aria-hidden="true">+</span> Run';
  }
});

copyButton.addEventListener("click", async () => {
  if (!currentMarkdown) return;
  await navigator.clipboard.writeText(currentMarkdown);
  copyButton.textContent = "Copied";
  setTimeout(() => {
    copyButton.textContent = "Copy MD";
  }, 1200);
});

setStage("input");
