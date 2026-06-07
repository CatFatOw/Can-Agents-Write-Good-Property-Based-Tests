const form = document.querySelector("#documentation-form");
const documentationInput = document.querySelector("#documentation");
const apiNameInput = document.querySelector("#api-name");
const toneInput = document.querySelector("#tone");
const reviewPanel = document.querySelector("#review-panel");
const comparePanel = document.querySelector("#compare-panel");
const originalDoc = document.querySelector("#original-doc");
const generatedDoc = document.querySelector("#generated-doc");
const outputTitle = document.querySelector("#output-title");
const outputEyebrow = document.querySelector("#output-eyebrow");
const flowStatus = document.querySelector("#flow-status");
const copyButton = document.querySelector("#copy-button");
const stepTabs = Array.from(document.querySelectorAll(".step-tab"));
const examples = document.querySelector("#prompt-examples");

let currentMarkdown = "";
let currentInvariants = [];

const exampleDocs = {
  "numpy-add": {
    api: "numpy.add",
    text: `numpy.add(x1, x2, /, out=None, *, where=True, casting='same_kind', order='K', dtype=None, subok=True)

Add arguments element-wise.

The arguments must be broadcastable to a common shape. If x1 and x2 have different numeric dtypes, NumPy applies its normal casting and promotion rules. The result is an ndarray unless both inputs are scalars. The optional out parameter may be used to place the result in an existing array. The where mask controls which locations are updated.`
  },
  "torch-softmax": {
    api: "torch.softmax",
    text: `torch.softmax(input, dim, dtype=None)

Applies the Softmax function to an n-dimensional input Tensor.

Rescales slices of the input along dim so that the elements lie in the range [0, 1] and sum to 1. The dim argument chooses which axis is normalized. If dtype is provided, the input is cast before the operation is performed.`
  },
  "python-sorted": {
    api: "sorted",
    text: `sorted(iterable, /, *, key=None, reverse=False)

Return a new sorted list from the items in iterable.

The key function, if supplied, is called once for each item and controls the comparison key. The original iterable is not modified. When reverse is true, the result is ordered descending. Sorting is stable, so equal keys preserve their original relative order.`
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

function guessInvariants(apiName, docText) {
  const lower = docText.toLowerCase();
  const invariants = [];

  if (/broadcast|shape/.test(lower)) {
    invariants.push("Inputs that participate in element-wise operations must be broadcastable to a common shape.");
  }
  if (/dtype|cast|promotion|type/.test(lower)) {
    invariants.push("Documented dtype conversion or promotion must happen before the result contract is evaluated.");
  }
  if (/out parameter|out=|existing array|place/.test(lower)) {
    invariants.push("When an output buffer is accepted, valid writes must respect the documented output shape and dtype.");
  }
  if (/where|mask/.test(lower)) {
    invariants.push("Masked or conditional updates must leave unselected positions outside the documented operation.");
  }
  if (/sum to 1|softmax|probabilit/.test(lower)) {
    invariants.push("Each normalized slice must contain finite probabilities whose sum is approximately one.");
  }
  if (/\[0,\s*1\]|between 0 and 1/.test(lower)) {
    invariants.push("Normalized outputs must stay within the closed interval from zero to one.");
  }
  if (/dim|axis/.test(lower)) {
    invariants.push("Axis-specific behavior must affect only the selected dimension and preserve the other dimensions.");
  }
  if (/new .*list|not modified|original/.test(lower)) {
    invariants.push("The operation must not mutate the original input when the documentation promises a new result.");
  }
  if (/\bstable\b/.test(lower)) {
    invariants.push("Items with equal comparison keys must preserve their original relative order.");
  }
  if (/reverse|descending/.test(lower)) {
    invariants.push("Reverse ordering must invert the final ordering without changing the set of returned elements.");
  }

  invariants.push(`${apiName} must preserve every explicit precondition, return-shape rule, and exception boundary stated in the original documentation.`);
  return Array.from(new Set(invariants)).slice(0, 7);
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

function generateMarkdown(apiName, sourceDoc, acceptedInvariants, tone) {
  const firstLine = sourceDoc.split(/\n+/).find(Boolean) || apiName;
  const summary = sourceDoc
    .split(/\n+/)
    .map((line) => line.trim())
    .filter(Boolean)
    .slice(1, 4)
    .join(" ");
  const toneLine = {
    contract: "This documentation is organized as a behavioral contract.",
    friendly: "This version keeps the original reference feel while making the behavior easier to test.",
    strict: "This version foregrounds preconditions, invalid states, and edge-case boundaries."
  }[tone];

  const invariantLines = acceptedInvariants.map((item) => `- ${item}`).join("\n");
  const edgeCases = acceptedInvariants
    .filter((item) => /dtype|shape|axis|mask|mutate|exception|precondition|output/i.test(item))
    .map((item) => `- Check: ${item}`)
    .join("\n") || "- No additional edge cases were inferred from the accepted invariants.";

  return `# ${apiName}

\`${firstLine}\`

${summary || "This API should be documented through explicit behavior that can be reviewed and tested."}

${toneLine}

## Preconditions

The caller should satisfy every input-domain rule implied by the original documentation. In particular:

${invariantLines}

## Behavioral Guarantees

For valid inputs, \`${apiName}\` should preserve the accepted invariants above. These claims are written so they can become property-based tests instead of remaining prose-only documentation.

## Edge Cases To Test

${edgeCases}

## Example Property-Based Test Sketch

\`\`\`python
from hypothesis import given, strategies as st

@given(st.data())
def test_${apiName.replace(/[^a-zA-Z0-9_]/g, "_")}_contract(data):
    # Generate valid inputs from the documented preconditions.
    # Call ${apiName}.
    # Assert each accepted invariant against the result.
    pass
\`\`\`

## Notes

This invariant-based version intentionally separates contract claims from examples. That makes review easier and gives test generators a cleaner target.`;
}

function generateMarkdownFromReview() {
  const apiName = apiNameInput.value.trim() || "api.function";
  const accepted = Array.from(reviewPanel.querySelectorAll("input[type='checkbox']"))
    .filter((input) => input.checked)
    .map((input) => currentInvariants[Number(input.dataset.index)]);

  currentMarkdown = generateMarkdown(apiName, documentationInput.value.trim(), accepted, toneInput.value);
  originalDoc.textContent = documentationInput.value.trim();
  generatedDoc.textContent = currentMarkdown;
  reviewPanel.classList.add("is-hidden");
  comparePanel.classList.remove("is-hidden");
  outputEyebrow.textContent = "Markdown comparison";
  outputTitle.textContent = "Before and after";
  copyButton.disabled = false;
  setStage("compare");
  setStatus("ready", "MD ready");
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

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const docText = documentationInput.value.trim();
  const apiName = apiNameInput.value.trim() || "api.function";
  if (!docText) return;

  currentInvariants = guessInvariants(apiName, docText);
  comparePanel.classList.add("is-hidden");
  reviewPanel.classList.remove("is-hidden");
  outputEyebrow.textContent = "Review invariants";
  outputTitle.textContent = "Check the claims";
  copyButton.disabled = true;
  renderInvariantReview(currentInvariants);
  setStage("review");
  setStatus("review", "Check invariants");
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
