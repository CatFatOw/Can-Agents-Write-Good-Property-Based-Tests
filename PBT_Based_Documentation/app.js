const form = document.querySelector("#documentation-form");
const documentationInput = document.querySelector("#documentation");
const apiNameInput = document.querySelector("#api-name");
const sourceObjectInput = document.querySelector("#source-object");
const lookupButton = document.querySelector("#lookup-button");
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
const backReviewButton = document.querySelector("#back-review-button");
const runButton = document.querySelector("#run-button");
const stepTabs = Array.from(document.querySelectorAll(".step-tab"));
const examples = document.querySelector("#prompt-examples");

let currentMarkdown = "";
let currentInvariants = [];
let currentSource = "";
const requestCache = new Map();

const exampleDocs = {
  "numpy-linspace": {
    api: "numpy.linspace",
    path: "examples/numpy_linspace_source.py"
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
  const cacheKey = `${path}:${JSON.stringify(payload)}`;
  if (requestCache.has(cacheKey)) {
    return requestCache.get(cacheKey);
  }
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
  requestCache.set(cacheKey, data);
  return data;
}

function showInputStage() {
  reviewPanel.classList.remove("is-hidden");
  comparePanel.classList.add("is-hidden");
  backReviewButton.classList.add("is-hidden");
  outputEyebrow.textContent = "Review invariants";
  outputTitle.textContent = "Check the claims";
  setStage("input");
}

function showReviewStage() {
  if (!currentInvariants.length) {
    showInputStage();
    return;
  }
  reviewPanel.classList.remove("is-hidden");
  comparePanel.classList.add("is-hidden");
  backReviewButton.classList.add("is-hidden");
  outputEyebrow.textContent = "Review invariants";
  outputTitle.textContent = "Check the claims";
  setStage("review");
  setStatus("review", "Check invariants");
}

function showCompareStage() {
  if (!currentMarkdown) {
    showReviewStage();
    return;
  }
  reviewPanel.classList.add("is-hidden");
  comparePanel.classList.remove("is-hidden");
  backReviewButton.classList.remove("is-hidden");
  outputEyebrow.textContent = "Markdown comparison";
  outputTitle.textContent = "Before and after";
  setStage("compare");
  setStatus("ready", "MD ready");
}

function renderError(message, eyebrow = "GPT call failed", title = "Could not run the pipeline") {
  reviewPanel.classList.remove("is-hidden");
  comparePanel.classList.add("is-hidden");
  backReviewButton.classList.add("is-hidden");
  reviewPanel.innerHTML = `
    <div class="review-copy">
      <p class="eyebrow">${escapeHtml(eyebrow)}</p>
      <h3>${escapeHtml(title)}</h3>
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
      <p>Uncheck any claim that feels too strong, vague, or not supported by the source code.</p>
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
      source_code: documentationInput.value.trim(),
      invariants: accepted,
      tone: toneInput.value
    });
    currentMarkdown = data.markdown;
    currentSource = documentationInput.value.trim();
    originalDoc.textContent = currentSource;
    generatedDoc.textContent = currentMarkdown;
    copyButton.disabled = false;
    showCompareStage();
  } catch (error) {
    renderError(error.message || "Documentation generation failed.");
  } finally {
    approveButton.disabled = false;
    approveButton.textContent = "Looks good, generate Markdown";
  }
}

examples.addEventListener("click", async (event) => {
  const button = event.target.closest("[data-example]");
  if (!button) return;
  const example = exampleDocs[button.dataset.example];
  try {
    const response = await fetch(example.path);
    if (!response.ok) throw new Error("Could not load example source file.");
    documentationInput.value = await response.text();
    currentSource = documentationInput.value;
    currentMarkdown = "";
    currentInvariants = [];
    apiNameInput.value = example.api;
    sourceObjectInput.value = "np.linspace";
    documentationInput.focus();
    setStage("input");
    setStatus("draft", "Example loaded");
  } catch (error) {
    renderError(error.message || "Example load failed.");
  }
});

lookupButton.addEventListener("click", async () => {
  const objectName = sourceObjectInput.value.trim();
  if (!objectName) return;
  lookupButton.disabled = true;
  lookupButton.textContent = "Loading...";
  try {
    const data = await postJson("/api/source", { object_name: objectName });
    documentationInput.value = data.source_code;
    currentSource = data.source_code;
    currentMarkdown = "";
    currentInvariants = [];
    apiNameInput.value = data.api_name;
    setStage("input");
    setStatus("draft", data.source_kind === "fallback" ? "Fallback loaded" : "Source loaded");
    if (data.warning) {
      reviewPanel.classList.remove("is-hidden");
      comparePanel.classList.add("is-hidden");
      outputEyebrow.textContent = "Source lookup";
      outputTitle.textContent = "Fallback loaded";
      reviewPanel.innerHTML = `
        <div class="review-copy">
          <p class="eyebrow">Inspect fallback</p>
          <h3>No Python source available</h3>
          <p>${escapeHtml(data.warning)}</p>
        </div>
      `;
    }
  } catch (error) {
    renderError(
      `${error.message || "Could not load source."} If lookup fails, copy and paste the source code manually.`,
      "Source lookup failed",
      "Could not inspect that object"
    );
  } finally {
    lookupButton.disabled = false;
    lookupButton.textContent = "Load source";
  }
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
      source_code: docText
    });
    currentSource = docText;
    currentMarkdown = "";
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

backReviewButton.addEventListener("click", showReviewStage);

stepTabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    if (tab.dataset.step === "input") {
      showInputStage();
    } else if (tab.dataset.step === "review") {
      showReviewStage();
    } else if (tab.dataset.step === "compare") {
      showCompareStage();
    }
  });
});

setStage("input");
