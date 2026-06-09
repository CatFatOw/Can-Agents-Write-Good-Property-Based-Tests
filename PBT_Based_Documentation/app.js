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
const docsExamplePanel = document.querySelector("#docs-example-panel");
const generatedDocsPanel = document.querySelector("#generated-docs-panel");
const generatedDocsTabs = document.querySelector("#generated-docs-tabs");
const generatedDocsRendered = document.querySelector("#generated-docs-rendered");
const generatedDocsTitle = document.querySelector("#generated-docs-title");
const originalExampleDocs = document.querySelector("#original-example-docs");
const invariantExampleDocs = document.querySelector("#invariant-example-docs");
const publicExampleTitle = document.querySelector("#public-example-title");
const invariantExampleTitle = document.querySelector("#invariant-example-title");
const generatedDoc = document.querySelector("#generated-doc");
const outputTitle = document.querySelector("#output-title");
const outputEyebrow = document.querySelector("#output-eyebrow");
const flowStatus = document.querySelector("#flow-status");
const copyButton = document.querySelector("#copy-button");
const downloadButton = document.querySelector("#download-button");
const backReviewButton = document.querySelector("#back-review-button");
const runButton = document.querySelector("#run-button");
const stepTabs = Array.from(document.querySelectorAll(".step-tab"));
const examples = document.querySelector("#prompt-examples");
const docsOpenButton = document.querySelector("#docs-open-button");
const generatedDocsButton = document.querySelector("#generated-docs-button");

const sourceHoverCard = document.createElement("aside");
sourceHoverCard.className = "source-hover-card";
sourceHoverCard.setAttribute("aria-hidden", "true");
document.body.appendChild(sourceHoverCard);

let currentMarkdown = "";
let currentInvariants = [];
let currentMetrics = [];
let selectedTestIndex = 0;
let currentSource = "";
let currentExampleMarkdown = "";
let currentExampleFilename = "invariant-documentation.md";
let generatedDocs = [];
let activeGeneratedDocId = "";
let inactivityTimer = 0;
const requestCache = new Map();
const GENERATED_DOCS_TTL_MS = 10 * 60 * 1000;

const exampleDocs = {
  "numpy-linspace": {
    api: "numpy.linspace",
    lookup: "np.linspace",
    path: "examples/numpy_linspace_source.py"
  },
  "numpy-pad": {
    api: "numpy.pad",
    lookup: "np.pad"
  }
};

const docsExamples = {
  "numpy-pad": {
    label: "np.pad",
    originalPath: "examples/numpy_pad_original_docs.md",
    invariantPath: "examples/numpy_pad_invariant_docs.md"
  },
  "numpy-linspace": {
    label: "np.linspace",
    originalPath: "examples/numpy_linspace_original_docs.md",
    invariantPath: "examples/numpy_linspace_invariant_docs.md"
  }
};

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;"
  }[char]));
}

function invariantText(invariant) {
  if (typeof invariant === "string") return invariant;
  return invariant?.invariant || invariant?.text || invariant?.claim || invariant?.description || "";
}

function numberFromUnknown(value) {
  if (Array.isArray(value)) {
    return numberFromUnknown(value[0]);
  }
  if (value && typeof value === "object") {
    return numberFromUnknown(value.lineno ?? value.line ?? value.start ?? value.start_line);
  }
  const match = String(value ?? "").match(/\d+/);
  return match ? Number(match[0]) : Number.NaN;
}

function rangeFromUnknown(value) {
  if (!value) return null;
  if (Array.isArray(value)) {
    const start = numberFromUnknown(value[0]);
    const end = numberFromUnknown(value[value.length > 1 ? value.length - 1 : 0]);
    return { start, end };
  }
  if (typeof value === "object") {
    const start = numberFromUnknown(value.start ?? value.lineno ?? value.line ?? value.start_line);
    const end = numberFromUnknown(value.end ?? value.end_lineno ?? value.end_line ?? value.stop ?? value.lineno ?? value.line ?? value.start_line);
    return { start, end };
  }
  return null;
}

function invariantRange(invariant) {
  if (!invariant || typeof invariant === "string") return null;
  const explicitRange = rangeFromUnknown(
    invariant.lines ?? invariant.source_lines ?? invariant.line_numbers ?? invariant.line_range ?? invariant.range ?? invariant.evidence_lines
  );
  const start = explicitRange ? explicitRange.start : numberFromUnknown(invariant.lineno ?? invariant.line ?? invariant.start_line);
  const end = explicitRange ? explicitRange.end : numberFromUnknown(invariant.end_lineno ?? invariant.end_line ?? invariant.lineno ?? invariant.line ?? invariant.start_line);
  if (!Number.isFinite(start) || start <= 0) return null;
  const normalizedStart = Math.max(1, Math.floor(start));
  const normalizedEnd = Number.isFinite(end) && end > 0 ? Math.floor(end) : normalizedStart;
  return {
    start: Math.min(normalizedStart, normalizedEnd),
    end: Math.max(normalizedStart, normalizedEnd)
  };
}

function invariantTexts(invariants) {
  return invariants.map(invariantText).filter(Boolean);
}

function renderInlineMarkdown(value) {
  return escapeHtml(value)
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\[([^\]]+)\]\((https?:\/\/[^)]+)\)/g, '<a href="$2" target="_blank" rel="noreferrer">$1</a>');
}

function renderMarkdown(markdown) {
  const lines = markdown.split(/\r?\n/);
  const html = [];
  let index = 0;

  while (index < lines.length) {
    const line = lines[index];
    if (!line.trim()) {
      index += 1;
      continue;
    }

    if (line.startsWith("```")) {
      const language = line.slice(3).trim();
      index += 1;
      const codeLines = [];
      while (index < lines.length && !lines[index].startsWith("```")) {
        codeLines.push(lines[index]);
        index += 1;
      }
      index += 1;
      html.push(`<pre class="md-code"><code class="language-${escapeHtml(language)}">${escapeHtml(codeLines.join("\n"))}</code></pre>`);
      continue;
    }

    if (/^\|.+\|$/.test(line.trim())) {
      const rows = [];
      while (index < lines.length && /^\|.+\|$/.test(lines[index].trim())) {
        if (!/^\|\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?$/.test(lines[index].trim())) {
          rows.push(lines[index].trim().replace(/^\||\|$/g, "").split("|").map((cell) => cell.trim()));
        }
        index += 1;
      }
      const [head = [], ...body] = rows;
      html.push(`
        <table>
          <thead><tr>${head.map((cell) => `<th>${renderInlineMarkdown(cell)}</th>`).join("")}</tr></thead>
          <tbody>${body.map((row) => `<tr>${row.map((cell) => `<td>${renderInlineMarkdown(cell)}</td>`).join("")}</tr>`).join("")}</tbody>
        </table>
      `);
      continue;
    }

    if (/^- /.test(line.trim())) {
      const items = [];
      while (index < lines.length && /^- /.test(lines[index].trim())) {
        items.push(lines[index].trim().slice(2));
        index += 1;
      }
      html.push(`<ul>${items.map((item) => `<li>${renderInlineMarkdown(item)}</li>`).join("")}</ul>`);
      continue;
    }

    const heading = /^(#{1,4})\s+(.+)$/.exec(line);
    if (heading) {
      const level = heading[1].length;
      html.push(`<h${level}>${renderInlineMarkdown(heading[2])}</h${level}>`);
      index += 1;
      continue;
    }

    const paragraph = [line.trim()];
    index += 1;
    while (index < lines.length && lines[index].trim() && !/^(#{1,4})\s+/.test(lines[index]) && !lines[index].startsWith("```") && !/^- /.test(lines[index].trim()) && !/^\|.+\|$/.test(lines[index].trim())) {
      paragraph.push(lines[index].trim());
      index += 1;
    }
    html.push(`<p>${renderInlineMarkdown(paragraph.join(" "))}</p>`);
  }

  return html.join("");
}

function setStage(stage) {
  hideSourceHoverCard();
  document.body.classList.remove("stage-input", "stage-review", "stage-compare", "stage-tests", "stage-docs-example", "stage-generated-docs");
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

function slugify(value, fallback = "generated-documentation") {
  return (value || fallback)
    .replace(/[^a-z0-9_-]+/gi, "-")
    .replace(/^-|-$/g, "")
    .toLowerCase() || fallback;
}

function getActiveMarkdownPayload() {
  if (document.body.classList.contains("stage-generated-docs")) {
    const doc = generatedDocs.find((item) => item.id === activeGeneratedDocId);
    return {
      text: doc?.markdown || "",
      filename: doc?.filename || "generated-documentation.md"
    };
  }
  if (document.body.classList.contains("stage-docs-example")) {
    return {
      text: currentExampleMarkdown,
      filename: currentExampleFilename
    };
  }
  return {
    text: currentMarkdown,
    filename: `${slugify(apiNameInput.value.trim() || "invariant-documentation")}.md`
  };
}

function syncMarkdownActions() {
  const { text } = getActiveMarkdownPayload();
  const enabled = Boolean(text);
  copyButton.disabled = !enabled;
  downloadButton.disabled = !enabled;
}

function resetGeneratedDocsInactivityTimer() {
  window.clearTimeout(inactivityTimer);
  inactivityTimer = window.setTimeout(() => {
    generatedDocs = [];
    activeGeneratedDocId = "";
    renderGeneratedDocsLibrary();
    if (document.body.classList.contains("stage-generated-docs")) {
      showInputStage();
      setStatus("draft", "Docs cleared");
    }
  }, GENERATED_DOCS_TTL_MS);
}

function addGeneratedDoc(markdown, invariants) {
  const apiName = apiNameInput.value.trim() || "api.function";
  const createdAt = new Date();
  const id = `${Date.now()}-${Math.random().toString(16).slice(2)}`;
  const doc = {
    id,
    apiName,
    title: apiName,
    markdown,
    invariants: [...invariants],
    createdAt,
    filename: `${slugify(apiName)}-${createdAt.toISOString().slice(0, 19).replace(/[:T]/g, "-")}.md`
  };
  generatedDocs = [doc, ...generatedDocs].slice(0, 12);
  activeGeneratedDocId = id;
  renderGeneratedDocsLibrary();
  resetGeneratedDocsInactivityTimer();
}

function renderGeneratedDocsLibrary() {
  generatedDocsButton.disabled = generatedDocs.length === 0;
  generatedDocsButton.textContent = `Generated docs (${generatedDocs.length})`;

  if (!generatedDocs.length) {
    generatedDocsTabs.innerHTML = "";
    generatedDocsTitle.textContent = "Generated docs";
    generatedDocsRendered.innerHTML = '<p class="placeholder">Generated documentation from this page session will appear here.</p>';
    syncMarkdownActions();
    return;
  }

  if (!generatedDocs.some((doc) => doc.id === activeGeneratedDocId)) {
    activeGeneratedDocId = generatedDocs[0].id;
  }

  generatedDocsTabs.innerHTML = generatedDocs.map((doc, index) => `
    <button type="button" class="generated-doc-tab ${doc.id === activeGeneratedDocId ? "is-active" : ""}" data-doc-id="${doc.id}">
      <span>${escapeHtml(doc.title)}</span>
      <small>${index === 0 ? "latest" : doc.createdAt.toLocaleTimeString([], { hour: "numeric", minute: "2-digit" })}</small>
    </button>
  `).join("");
}

function showGeneratedDoc(docId = activeGeneratedDocId || generatedDocs[0]?.id || "") {
  const doc = generatedDocs.find((item) => item.id === docId);
  reviewPanel.classList.add("is-hidden");
  comparePanel.classList.add("is-hidden");
  testsPanel.classList.add("is-hidden");
  docsExamplePanel.classList.add("is-hidden");
  generatedDocsPanel.classList.remove("is-hidden");
  backReviewButton.classList.add("is-hidden");
  outputEyebrow.textContent = "Session library";
  outputTitle.textContent = "Generated documentation";
  setStage("generated-docs");
  setStatus("ready", "Session docs");

  if (!doc) {
    renderGeneratedDocsLibrary();
    syncMarkdownActions();
    return;
  }

  activeGeneratedDocId = doc.id;
  renderGeneratedDocsLibrary();
  generatedDocsTitle.textContent = doc.title;
  generatedDocsRendered.innerHTML = `
    <section class="saved-invariants">
      <p class="eyebrow">Invariants used</p>
      <ul>${doc.invariants.map((invariant) => `<li>${escapeHtml(invariant)}</li>`).join("")}</ul>
    </section>
    ${renderMarkdown(doc.markdown)}
  `;
  syncMarkdownActions();
}

async function writeClipboardText(text) {
  if (typeof navigator !== "undefined" && navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(text);
    return;
  }
  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.setAttribute("readonly", "");
  textarea.style.position = "fixed";
  textarea.style.left = "-9999px";
  document.body.appendChild(textarea);
  textarea.select();
  if (typeof document.execCommand === "function") {
    document.execCommand("copy");
  }
  textarea.remove();
}

function downloadMarkdown(text, filename) {
  const blob = new Blob([text], { type: "text/markdown;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
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

function loadingDots(label) {
  return `
    <span class="loading-label">${escapeHtml(label)}</span>
    <span class="loading-dots" aria-hidden="true">
      <span></span><span></span><span></span>
    </span>
  `;
}

function showInputStage() {
  reviewPanel.classList.remove("is-hidden");
  comparePanel.classList.add("is-hidden");
  testsPanel.classList.add("is-hidden");
  docsExamplePanel.classList.add("is-hidden");
  generatedDocsPanel.classList.add("is-hidden");
  backReviewButton.classList.add("is-hidden");
  outputEyebrow.textContent = "Review invariants";
  outputTitle.textContent = "Check the claims";
  setStage("input");
  syncMarkdownActions();
}

function showReviewStage() {
  if (!currentInvariants.length) {
    showInputStage();
    return;
  }
  reviewPanel.classList.remove("is-hidden");
  comparePanel.classList.add("is-hidden");
  testsPanel.classList.add("is-hidden");
  docsExamplePanel.classList.add("is-hidden");
  generatedDocsPanel.classList.add("is-hidden");
  backReviewButton.classList.add("is-hidden");
  outputEyebrow.textContent = "Review invariants";
  outputTitle.textContent = "Check the claims";
  setStage("review");
  setStatus("review", "Check invariants");
  syncMarkdownActions();
}

function showCompareStage(force = false) {
  if (!force && !currentMarkdown) {
    showReviewStage();
    return;
  }
  reviewPanel.classList.add("is-hidden");
  comparePanel.classList.remove("is-hidden");
  testsPanel.classList.add("is-hidden");
  docsExamplePanel.classList.add("is-hidden");
  generatedDocsPanel.classList.add("is-hidden");
  backReviewButton.classList.remove("is-hidden");
  outputEyebrow.textContent = "Generated Markdown";
  outputTitle.textContent = "Invariant-based documentation";
  setStage("compare");
  setStatus("ready", "MD ready");
  syncMarkdownActions();
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
  docsExamplePanel.classList.add("is-hidden");
  generatedDocsPanel.classList.add("is-hidden");
  backReviewButton.classList.remove("is-hidden");
  outputEyebrow.textContent = "Generated PBT";
  outputTitle.textContent = "Property tests";
  setStage("tests");
  setStatus("ready", "Tests ready");
  syncMarkdownActions();
}

async function loadDocsExample(exampleId = "numpy-pad") {
  const example = docsExamples[exampleId] || docsExamples["numpy-pad"];
  outputTitle.textContent = `${example.label} comparison`;
  publicExampleTitle.textContent = `Original ${example.label}`;
  invariantExampleTitle.textContent = `Contract-style ${example.label}`;
  docsExamplePanel.querySelectorAll(".docs-example-choice").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.docExample === exampleId);
  });

  originalExampleDocs.innerHTML = '<p class="placeholder">Loading public documentation comparison...</p>';
  invariantExampleDocs.innerHTML = '<p class="placeholder">Loading invariant-based documentation...</p>';
  const [originalResponse, invariantResponse] = await Promise.all([
    fetch(example.originalPath),
    fetch(example.invariantPath)
  ]);
  if (!originalResponse.ok || !invariantResponse.ok) {
    throw new Error(`Could not load the ${example.label} documentation example.`);
  }
  originalExampleDocs.innerHTML = renderMarkdown(await originalResponse.text());
  const invariantText = await invariantResponse.text();
  invariantExampleDocs.innerHTML = renderMarkdown(invariantText);
  currentExampleMarkdown = invariantText;
  currentExampleFilename = `${example.label.replace(/[^a-z0-9_-]+/gi, "-").replace(/^-|-$/g, "").toLowerCase()}-invariant-documentation.md`;
  docsExamplePanel.dataset.activeExample = exampleId;
  syncMarkdownActions();
}

async function showDocsExampleStage(exampleId = docsExamplePanel.dataset.activeExample || "numpy-pad") {
  reviewPanel.classList.add("is-hidden");
  comparePanel.classList.add("is-hidden");
  testsPanel.classList.add("is-hidden");
  docsExamplePanel.classList.remove("is-hidden");
  generatedDocsPanel.classList.add("is-hidden");
  backReviewButton.classList.add("is-hidden");
  outputEyebrow.textContent = "Example invariant docs";
  setStage("docs-example");
  setStatus("ready", "Example docs");
  syncMarkdownActions();

  if (docsExamplePanel.dataset.activeExample === exampleId && originalExampleDocs.dataset.loaded === "true") {
    return;
  }

  await loadDocsExample(exampleId);
  originalExampleDocs.dataset.loaded = "true";
}

function renderError(message, eyebrow = "GPT call failed", title = "Could not run the pipeline") {
  reviewPanel.classList.remove("is-hidden");
  comparePanel.classList.add("is-hidden");
  testsPanel.classList.add("is-hidden");
  docsExamplePanel.classList.add("is-hidden");
  generatedDocsPanel.classList.add("is-hidden");
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
  syncMarkdownActions();
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
  const text = invariantText(invariant);
  return currentMetrics.find((metric) => metric.invariant === text);
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
    <div class="source-preview" id="source-preview" aria-label="Source code line preview">
      ${renderSourcePreview(currentSource)}
    </div>
    <div class="invariant-list" id="invariant-list"></div>
    <button type="button" class="approve-button" id="approve-button">Looks good, generate Markdown</button>
  `;

  document.querySelector("#approve-button").addEventListener("click", generateMarkdownFromReview);
}

function renderSourcePreview(source) {
  const lines = (source || "").split(/\r?\n/);
  if (!lines.length || !source.trim()) {
    return '<p class="source-preview-empty">Source line highlighting appears here after extraction.</p>';
  }
  return `
    <p class="eyebrow">Source evidence</p>
    <pre>${lines.map((line, index) => `
      <span class="source-line" data-line="${index + 1}"><span class="source-line-number">${index + 1}</span><code>${escapeHtml(line || " ")}</code></span>
    `).join("")}</pre>
  `;
}

function sourceRangeExcerpt(range, padding = 2) {
  if (!range || !currentSource.trim()) return "";
  const lines = currentSource.split(/\r?\n/);
  const start = Math.max(1, range.start - padding);
  const end = Math.min(lines.length, range.end + padding);
  return lines.slice(start - 1, end).map((line, offset) => {
    const lineNumber = start + offset;
    const highlighted = lineNumber >= range.start && lineNumber <= range.end;
    return `
      <span class="source-line ${highlighted ? "is-highlighted" : ""}" data-line="${lineNumber}">
        <span class="source-line-number">${lineNumber}</span><code>${escapeHtml(line || " ")}</code>
      </span>
    `;
  }).join("");
}

function showSourceHoverCard(item, range) {
  if (!range) {
    hideSourceHoverCard();
    return;
  }
  sourceHoverCard.innerHTML = `
    <p class="eyebrow">Source evidence</p>
    <pre>${sourceRangeExcerpt(range)}</pre>
  `;
  const rect = item.getBoundingClientRect();
  const cardWidth = Math.min(460, Math.max(320, window.innerWidth * 0.34));
  const leftSpace = rect.left;
  const rightSpace = window.innerWidth - rect.right;
  const left = rightSpace >= cardWidth + 18
    ? rect.right + 14
    : Math.max(12, rect.left - cardWidth - 14);
  const top = Math.min(Math.max(12, rect.top), window.innerHeight - 320);
  sourceHoverCard.style.width = `${cardWidth}px`;
  sourceHoverCard.style.left = `${Math.min(left, window.innerWidth - cardWidth - 12)}px`;
  sourceHoverCard.style.top = `${top}px`;
  sourceHoverCard.classList.add("is-visible");
  sourceHoverCard.setAttribute("aria-hidden", "false");
}

function hideSourceHoverCard() {
  sourceHoverCard.classList.remove("is-visible");
  sourceHoverCard.setAttribute("aria-hidden", "true");
}

function highlightSourceRange(range) {
  reviewPanel.querySelectorAll(".source-line").forEach((line) => {
    const lineNumber = Number(line.dataset.line);
    const highlighted = Boolean(range && lineNumber >= range.start && lineNumber <= range.end);
    line.classList.toggle("is-highlighted", highlighted);
  });
}

function attachInvariantHoverHandlers() {
  reviewPanel.querySelectorAll(".invariant-item").forEach((item) => {
    const index = Number(item.dataset.index);
    const showRange = () => {
      const range = invariantRange(currentInvariants[index]);
      item.classList.toggle("has-active-range", Boolean(range));
      highlightSourceRange(range);
      showSourceHoverCard(item, range);
    };
    item.addEventListener("mouseenter", showRange);
    item.addEventListener("focusin", showRange);
    item.addEventListener("mousemove", showRange);
    item.addEventListener("mouseleave", () => {
      item.classList.remove("has-active-range");
      highlightSourceRange(null);
      hideSourceHoverCard();
    });
    item.addEventListener("focusout", () => {
      item.classList.remove("has-active-range");
      highlightSourceRange(null);
      hideSourceHoverCard();
    });
  });
}

async function renderInvariantReviewAnimated(invariants) {
  renderInvariantReview([]);
  const list = document.querySelector("#invariant-list");
  for (const [index, invariant] of invariants.entries()) {
    const metric = metricForInvariant(invariant);
    const wrapper = document.createElement("label");
    wrapper.className = "invariant-item invariant-enter";
    wrapper.dataset.index = String(index);
    const range = invariantRange(invariant);
    wrapper.innerHTML = `
      <input type="checkbox" checked data-index="${index}">
      <span class="invariant-copy">${escapeHtml(invariantText(invariant))}</span>
      ${range ? `<span class="line-chip">Lines ${range.start}${range.end !== range.start ? `-${range.end}` : ""}</span>` : '<span class="line-chip line-chip-muted" title="No line metadata returned for this invariant">No lines</span>'}
      ${metricMarkup(metric)}
    `;
    list.appendChild(wrapper);
    await wait(140);
    wrapper.classList.add("is-visible");
  }
  attachInvariantHoverHandlers();
}

function renderInvariantReviewWithMetrics(invariants, loading = false) {
  renderInvariantReview([]);
  const list = document.querySelector("#invariant-list");
  list.innerHTML = invariants.map((invariant, index) => {
    const metric = metricForInvariant(invariant);
    const range = invariantRange(invariant);
    return `
      <label class="invariant-item" data-index="${index}">
        <input type="checkbox" checked data-index="${index}">
        <span class="invariant-copy">${escapeHtml(invariantText(invariant))}</span>
        ${range ? `<span class="line-chip">Lines ${range.start}${range.end !== range.start ? `-${range.end}` : ""}</span>` : '<span class="line-chip line-chip-muted" title="No line metadata returned for this invariant">No lines</span>'}
        ${metricMarkup(metric)}
        ${loading && !metric ? `
          <span class="metric-pills is-loading">
            <span>Assessing...</span>
          </span>
        ` : ""}
      </label>
    `;
  }).join("");
  attachInvariantHoverHandlers();
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
    invariants: invariantTexts(currentInvariants)
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
    .map((input) => invariantText(currentInvariants[Number(input.dataset.index)]));

  const approveButton = document.querySelector("#approve-button");
  approveButton.disabled = true;
  approveButton.textContent = "Calling GPT...";
  setStatus("review", "Writing MD");

  try {
    currentSource = documentationInput.value.trim();
    currentMarkdown = "";
    generatedDoc.textContent = "";
    syncMarkdownActions();
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
    generatedDoc.classList.remove("is-streaming");
    generatedDoc.innerHTML = renderMarkdown(currentMarkdown);
    addGeneratedDoc(currentMarkdown, accepted);
    syncMarkdownActions();
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
    if (example.path) {
      const response = await fetch(example.path);
      if (!response.ok) throw new Error("Could not load example source file.");
      documentationInput.value = await response.text();
    } else {
      const data = await postJson("/api/source", { object_name: example.lookup }, { cache: false });
      documentationInput.value = data.source_code;
    }
    currentSource = documentationInput.value;
    currentMarkdown = "";
    currentInvariants = [];
    currentMetrics = [];
    selectedTestIndex = 0;
    apiNameInput.value = example.api;
    sourceObjectInput.value = example.lookup;
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
  runButton.innerHTML = loadingDots("Generating");
  comparePanel.classList.add("is-hidden");
  testsPanel.classList.add("is-hidden");
  docsExamplePanel.classList.add("is-hidden");
  generatedDocsPanel.classList.add("is-hidden");
  reviewPanel.classList.remove("is-hidden");
  reviewPanel.innerHTML = `
    <div class="loading-card">
      <p class="eyebrow">Generating invariants</p>
      <h3>${loadingDots("Calling GPT")}</h3>
      <p>Extracting candidate invariants from the source code and looking for line-level evidence.</p>
    </div>
  `;
  outputEyebrow.textContent = "Review invariants";
  outputTitle.textContent = "Check the claims";
  copyButton.disabled = true;
  downloadButton.disabled = true;
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
  const { text, filename } = getActiveMarkdownPayload();
  if (!text) return;
  try {
    await writeClipboardText(text);
    copyButton.textContent = "Copied";
  } catch {
    downloadMarkdown(text, filename);
    copyButton.textContent = "Downloaded MD";
  }
  setTimeout(() => {
    copyButton.textContent = "Copy MD";
  }, 1200);
});

downloadButton.addEventListener("click", () => {
  const { text, filename } = getActiveMarkdownPayload();
  if (!text) return;
  downloadMarkdown(text, filename);
  downloadButton.textContent = "Downloaded";
  setTimeout(() => {
    downloadButton.textContent = "Download MD";
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

docsOpenButton.addEventListener("click", () => {
  showDocsExampleStage().catch((error) => {
    renderError(error.message || "Could not load the example documentation.", "Example docs failed", "Could not load example");
  });
});

generatedDocsButton.addEventListener("click", () => {
  showGeneratedDoc();
});

generatedDocsPanel.addEventListener("click", (event) => {
  const button = event.target.closest(".generated-doc-tab");
  if (!button) return;
  showGeneratedDoc(button.dataset.docId);
});

docsExamplePanel.addEventListener("click", (event) => {
  const button = event.target.closest(".docs-example-choice");
  if (!button) return;
  loadDocsExample(button.dataset.docExample).catch((error) => {
    renderError(error.message || "Could not load the example documentation.", "Example docs failed", "Could not load example");
  });
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

["click", "keydown", "input", "mousemove", "touchstart"].forEach((eventName) => {
  window.addEventListener(eventName, () => {
    if (generatedDocs.length) {
      resetGeneratedDocsInactivityTimer();
    }
  }, { passive: true });
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

renderGeneratedDocsLibrary();
setStage("input");
