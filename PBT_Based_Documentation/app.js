const form = document.querySelector("#documentation-form");
const documentationInput = document.querySelector("#documentation");
const apiNameInput = document.querySelector("#api-name");
const sourceObjectInput = document.querySelector("#source-object");
const lookupButton = document.querySelector("#lookup-button");
const toneInput = document.querySelector("#tone");
const openaiKeyInput = document.querySelector("#openai-key");
const assessMetricsInput = document.querySelector("#assess-metrics");
const reviewPanel = document.querySelector("#review-panel");
const comparePanel = document.querySelector("#compare-panel");
const testsPanel = document.querySelector("#tests-panel");
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
let currentMetrics = [];
let selectedTestIndex = 0;
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
  document.body.classList.remove("stage-input", "stage-review", "stage-compare", "stage-tests");
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

async function postJson(path, payload, options = {}) {
  const useCache = options.cache !== false;
  const cacheKey = `${path}:${JSON.stringify(payload)}`;
  if (useCache && requestCache.has(cacheKey)) {
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
  if (useCache) {
    requestCache.set(cacheKey, data);
  }
  return data;
}

async function postTextStream(path, payload, onChunk) {
  const response = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      ...payload,
      openai_key: openaiKeyInput.value.trim()
    })
  });
  if (!response.ok) {
    const text = await response.text();
    try {
      throw new Error(JSON.parse(text).error || "Request failed.");
    } catch {
      throw new Error(text || "Request failed.");
    }
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let text = "";
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const chunk = decoder.decode(value, { stream: true });
    text += chunk;
    onChunk(chunk, text);
  }
  const tail = decoder.decode();
  if (tail) {
    text += tail;
    onChunk(tail, text);
  }
  return text;
}

function createTypewriter(element) {
  let target = "";
  let visible = "";
  let done = false;
  let frameId = 0;

  function tick() {
    if (visible.length < target.length) {
      const nextLength = Math.min(target.length, visible.length + 8);
      visible = target.slice(0, nextLength);
      element.textContent = visible;
      element.scrollTop = element.scrollHeight;
    }
    if (!done || visible.length < target.length) {
      frameId = requestAnimationFrame(tick);
    }
  }

  frameId = requestAnimationFrame(tick);

  return {
    push(fullText) {
      target = fullText;
    },
    async finish(finalText) {
      target = finalText;
      done = true;
      while (visible.length < target.length) {
        await wait(16);
      }
      cancelAnimationFrame(frameId);
      element.textContent = target;
      element.scrollTop = element.scrollHeight;
      return target;
    }
  };
}

function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function showInputStage() {
  reviewPanel.classList.remove("is-hidden");
  comparePanel.classList.add("is-hidden");
  testsPanel.classList.add("is-hidden");
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
  testsPanel.classList.add("is-hidden");
  backReviewButton.classList.add("is-hidden");
  outputEyebrow.textContent = "Review invariants";
  outputTitle.textContent = "Check the claims";
  setStage("review");
  setStatus("review", "Check invariants");
}

function showCompareStage(force = false) {
  if (!force && !currentMarkdown) {
    showReviewStage();
    return;
  }
  reviewPanel.classList.add("is-hidden");
  comparePanel.classList.remove("is-hidden");
  testsPanel.classList.add("is-hidden");
  backReviewButton.classList.remove("is-hidden");
  outputEyebrow.textContent = "Markdown comparison";
  outputTitle.textContent = "Before and after";
  setStage("compare");
  setStatus("ready", "MD ready");
}

function showTestsStage(testIndex = selectedTestIndex) {
  if (!currentMetrics.length) {
    showReviewStage();
    return;
  }
  selectedTestIndex = Number.isInteger(testIndex) ? testIndex : 0;
  renderTestsPanel();
  reviewPanel.classList.add("is-hidden");
  comparePanel.classList.add("is-hidden");
  testsPanel.classList.remove("is-hidden");
  backReviewButton.classList.remove("is-hidden");
  outputEyebrow.textContent = "Generated PBT";
  outputTitle.textContent = "Property tests";
  setStage("tests");
  setStatus("ready", "Tests ready");
}

function renderError(message, eyebrow = "GPT call failed", title = "Could not run the pipeline") {
  reviewPanel.classList.remove("is-hidden");
  comparePanel.classList.add("is-hidden");
  testsPanel.classList.add("is-hidden");
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

function formatScore(value) {
  const numeric = Number(value);
  if (!Number.isFinite(numeric)) return "0%";
  return `${Math.round(numeric * 100)}%`;
}

function metricScore(metric) {
  const score = Number(metric?.score);
  if (Number.isFinite(score)) {
    return score;
  }
  const validity = Number(metric?.validity);
  const soundness = Number(metric?.soundness);
  if (Number.isFinite(validity) && Number.isFinite(soundness)) {
    return (validity + soundness) / 2;
  }
  return 0;
}

function confidenceLabel(metric) {
  const label = String(metric?.confidence || "").toUpperCase();
  if (["HIGH", "MEDIUM", "LOW"].includes(label)) {
    return label;
  }
  const validity = typeof metric?.validity === "number" ? metric.validity : 0;
  const soundness = typeof metric?.soundness === "number" ? metric.soundness : 0;
  const average = (validity + soundness) / 2;
  if (average >= 0.85) return "HIGH";
  if (average >= 0.55) return "MEDIUM";
  return "LOW";
}

function metricForInvariant(invariant) {
  return currentMetrics.find((metric) => metric.invariant === invariant);
}

function metricMarkup(metric) {
  if (!metric) {
    return "";
  }
  const index = currentMetrics.indexOf(metric);
  const confidence = confidenceLabel(metric);
  return `
    <span class="metric-pills">
      <span class="confidence-pill confidence-${confidence.toLowerCase()}">${confidence} ${formatScore(metricScore(metric))}</span>
      <span>Validity ${formatScore(metric.validity)}</span>
      <span>Soundness ${formatScore(metric.soundness)}</span>
      <button type="button" class="metric-test-button ${metric.error ? "metric-warning" : ""}" data-test-index="${index}">Check test</button>
    </span>
  `;
}

function renderInvariantReview(invariants) {
  reviewPanel.innerHTML = `
    <div class="review-copy">
      <p class="eyebrow">Human review required</p>
      <h3>Approve the invariants</h3>
      <p>Uncheck any claim that feels too strong, vague, or not supported by the source code.</p>
    </div>
    <div class="invariant-list" id="invariant-list"></div>
    <button type="button" class="approve-button" id="approve-button">Looks good, generate Markdown</button>
  `;

  document.querySelector("#approve-button").addEventListener("click", generateMarkdownFromReview);
}

async function renderInvariantReviewAnimated(invariants) {
  renderInvariantReview([]);
  const list = document.querySelector("#invariant-list");
  for (const [index, invariant] of invariants.entries()) {
    const metric = metricForInvariant(invariant);
    const wrapper = document.createElement("label");
    wrapper.className = "invariant-item invariant-enter";
    wrapper.innerHTML = `
      <input type="checkbox" checked data-index="${index}">
      <span class="invariant-copy">${escapeHtml(invariant)}</span>
      ${metricMarkup(metric)}
    `;
    list.appendChild(wrapper);
    await wait(140);
    wrapper.classList.add("is-visible");
  }
}

function renderInvariantReviewWithMetrics(invariants, loading = false) {
  renderInvariantReview([]);
  const list = document.querySelector("#invariant-list");
  list.innerHTML = invariants.map((invariant, index) => {
    const metric = metricForInvariant(invariant);
    return `
      <label class="invariant-item">
        <input type="checkbox" checked data-index="${index}">
        <span class="invariant-copy">${escapeHtml(invariant)}</span>
        ${metricMarkup(metric)}
        ${loading && !metric ? `
          <span class="metric-pills is-loading">
            <span>Assessing...</span>
          </span>
        ` : ""}
      </label>
    `;
  }).join("");
}

function renderTestsPanel() {
  if (!currentMetrics.length) {
    testsPanel.innerHTML = `
      <p class="placeholder">
        Toggle metrics and run the invariant pass to generate property-based tests.
      </p>
    `;
    return;
  }

  testsPanel.innerHTML = `
    <div class="review-copy">
      <p class="eyebrow">Generated property-based tests</p>
      <h3>Inspect the tests</h3>
      <p>Each test was generated from one invariant. Scores appear beside the invariants; the Hypothesis code lives here.</p>
    </div>
    <div class="test-list">
      ${currentMetrics.map((metric, index) => `
        <details class="test-item" ${index === selectedTestIndex ? "open" : ""}>
          <summary>
            <span class="test-summary-title">Invariant ${index + 1}</span>
            <span class="test-summary-metrics">
              <span class="confidence-pill confidence-${confidenceLabel(metric).toLowerCase()}">${confidenceLabel(metric)} ${formatScore(metricScore(metric))}</span>
              <span>${formatScore(metric.validity)} valid / ${formatScore(metric.soundness)} sound</span>
            </span>
          </summary>
          <p>${escapeHtml(metric.invariant || "")}</p>
          ${metric.explanation ? `<p class="metric-explanation">${escapeHtml(metric.explanation)}</p>` : ""}
          ${metric.error ? `<p class="metric-error">${escapeHtml(metric.error)}</p>` : ""}
          <label class="test-editor">
            <span>Edit or paste a property-based test</span>
            <textarea data-test-editor="${index}" rows="11">${escapeHtml(metric.test_code || "")}</textarea>
          </label>
          <button type="button" class="secondary-button rerun-test-button" data-rerun-index="${index}">Rerun this invariant</button>
        </details>
      `).join("")}
    </div>
  `;
}

async function rerunEditedTest(index, button) {
  const metric = currentMetrics[index];
  const editor = testsPanel.querySelector(`[data-test-editor="${index}"]`);
  if (!metric || !editor) return;

  button.disabled = true;
  button.textContent = "Rerunning...";
  setStatus("review", "Rerunning test");

  try {
    const data = await postJson("/api/rerun-test", {
      api_name: apiNameInput.value.trim() || "api.function",
      source_code: currentSource,
      invariant: metric.invariant,
      test_code: editor.value
    }, { cache: false });

    currentMetrics[index] = {
      ...metric,
      ...data.metric,
      confidence: metric.confidence,
      score: metric.score,
      explanation: metric.explanation
    };
    selectedTestIndex = index;
    renderInvariantReviewWithMetrics(currentInvariants);
    renderTestsPanel();
    setStatus("ready", "Test rerun");
  } catch (error) {
    button.disabled = false;
    button.textContent = "Rerun this invariant";
    setStatus("draft", "Rerun failed");
    throw error;
  }
}

async function assessMetricsForReview() {
  if (!assessMetricsInput.checked || !currentInvariants.length) {
    currentMetrics = [];
    renderTestsPanel();
    return;
  }

  renderInvariantReviewWithMetrics(currentInvariants, true);
  renderTestsPanel();
  setStatus("review", "Assessing metrics");

  const data = await postJson("/api/metrics", {
    api_name: apiNameInput.value.trim() || "api.function",
    source_code: currentSource,
    invariants: currentInvariants
  });
  currentMetrics = data.metrics || [];
  renderInvariantReviewWithMetrics(currentInvariants);
  renderTestsPanel();
  setStatus("review", "Metrics ready");
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
    currentSource = documentationInput.value.trim();
    currentMarkdown = "";
    originalDoc.textContent = currentSource;
    generatedDoc.textContent = "";
    copyButton.disabled = true;
    showCompareStage(true);
    setStatus("review", "Streaming MD");
    generatedDoc.classList.add("is-streaming");
    const writer = createTypewriter(generatedDoc);

    const streamedMarkdown = await postTextStream("/api/documentation-stream", {
      api_name: apiName,
      source_code: currentSource,
      invariants: accepted,
      tone: toneInput.value
    }, (_chunk, fullText) => {
      writer.push(fullText);
    });
    currentMarkdown = await writer.finish(streamedMarkdown);
    copyButton.disabled = false;
    generatedDoc.classList.remove("is-streaming");
    showCompareStage();
  } catch (error) {
    generatedDoc.classList.remove("is-streaming");
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
    currentMetrics = [];
    selectedTestIndex = 0;
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
    currentMetrics = [];
    selectedTestIndex = 0;
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
  testsPanel.classList.add("is-hidden");
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
    currentMetrics = [];
    selectedTestIndex = 0;
    await renderInvariantReviewAnimated(currentInvariants);
    await assessMetricsForReview();
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

reviewPanel.addEventListener("click", (event) => {
  const button = event.target.closest(".metric-test-button");
  if (!button) return;
  event.preventDefault();
  event.stopPropagation();
  showTestsStage(Number(button.dataset.testIndex || 0));
});

testsPanel.addEventListener("click", async (event) => {
  const button = event.target.closest(".rerun-test-button");
  if (!button) return;
  try {
    await rerunEditedTest(Number(button.dataset.rerunIndex || 0), button);
  } catch (error) {
    renderError(error.message || "Could not rerun the edited test.", "Test rerun failed", "Could not assess this test");
  }
});

assessMetricsInput.addEventListener("change", async () => {
  if (!currentInvariants.length) {
    return;
  }
  try {
    await assessMetricsForReview();
  } catch (error) {
    renderError(error.message || "Metric assessment failed.", "Metric assessment failed", "Could not assess tests");
  }
});

stepTabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    if (tab.dataset.step === "input") {
      showInputStage();
    } else if (tab.dataset.step === "review") {
      showReviewStage();
    } else if (tab.dataset.step === "compare") {
      showCompareStage();
    } else if (tab.dataset.step === "tests") {
      showTestsStage();
    }
  });
});

setStage("input");
