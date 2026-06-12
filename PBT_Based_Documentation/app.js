const form = document.querySelector("#documentation-form");
const documentationInput = document.querySelector("#documentation");
const apiNameInput = document.querySelector("#api-name");
const sourceObjectInput = document.querySelector("#source-object");
const lookupButton = document.querySelector("#lookup-button");
const themeToggle = document.querySelector("#theme-toggle");
const toneInput = document.querySelector("#tone");
const openaiKeyInput = document.querySelector("#openai-key");
const openaiSeedInput = document.querySelector("#openai-seed");
const assessMetricsInput = document.querySelector("#assess-metrics");
const showMutationTestingInput = document.querySelector("#show-mutation-testing");
const mutationPackagesInput = document.querySelector("#mutation-packages");
const mutationAutoInstallInput = document.querySelector("#mutation-auto-install");
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
const DARK_MODE_STORAGE_KEY = "invariant-docs-dark-mode";

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

function applyTheme(mode) {
  const dark = mode === "dark";
  document.body.classList.toggle("dark-mode", dark);
  if (themeToggle) {
    themeToggle.setAttribute("aria-pressed", dark ? "true" : "false");
    themeToggle.innerHTML = `
      <span class="theme-orbit" aria-hidden="true">
        <span class="theme-sun"></span>
        <span class="theme-moon"></span>
      </span>
      <span class="theme-label">${dark ? "Light mode" : "Dark mode"}</span>
    `;
    themeToggle.title = dark ? "Switch to light mode" : "Switch to dark mode";
  }
}

applyTheme(localStorage.getItem(DARK_MODE_STORAGE_KEY) || "dark");

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

function normalizeInvariantKey(value) {
  return String(value || "")
    .toLowerCase()
    .replace(/[`*_~()[\]{}:;,.!?-]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
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
    .replace(/\*([^*]+)\*/g, "<em>$1</em>")
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

    if (/^[-*] /.test(line.trim())) {
      const items = [];
      while (index < lines.length && /^[-*] /.test(lines[index].trim())) {
        items.push(lines[index].trim().slice(2));
        index += 1;
      }
      html.push(`<ul>${items.map((item) => `<li>${renderInlineMarkdown(item)}</li>`).join("")}</ul>`);
      continue;
    }

    if (/^\d+\.\s+/.test(line.trim())) {
      const items = [];
      while (index < lines.length && /^\d+\.\s+/.test(lines[index].trim())) {
        items.push(lines[index].trim().replace(/^\d+\.\s+/, ""));
        index += 1;
      }
      html.push(`<ol>${items.map((item) => `<li>${renderInlineMarkdown(item)}</li>`).join("")}</ol>`);
      continue;
    }

    if (/^>\s?/.test(line.trim())) {
      const quotes = [];
      while (index < lines.length && /^>\s?/.test(lines[index].trim())) {
        quotes.push(lines[index].trim().replace(/^>\s?/, ""));
        index += 1;
      }
      html.push(`<blockquote>${quotes.map(renderInlineMarkdown).join("<br>")}</blockquote>`);
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
    while (index < lines.length && lines[index].trim() && !/^(#{1,4})\s+/.test(lines[index]) && !lines[index].startsWith("```") && !/^[-*] /.test(lines[index].trim()) && !/^\d+\.\s+/.test(lines[index].trim()) && !/^>\s?/.test(lines[index].trim()) && !/^\|.+\|$/.test(lines[index].trim())) {
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
      openai_key: openaiKeyInput.value.trim(),
      openai_seed: Number(openaiSeedInput.value || 42)
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
      openai_key: openaiKeyInput.value.trim(),
      openai_seed: Number(openaiSeedInput.value || 42)
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

function mutationScoreClass(value) {
  if (value === null || value === undefined || value === "") return "mutation-low";
  const numeric = Number(value);
  if (!Number.isFinite(numeric)) return "mutation-low";
  if (numeric >= 0.8) return "mutation-high";
  if (numeric >= 0.5) return "mutation-medium";
  return "mutation-low";
}

function mutationScoreMarkup(metric, index) {
  if (!showMutationTestingInput.checked || !metric) {
    return "";
  }
  const mutationError = metric.mutation_error ? ` title="${escapeHtml(metric.mutation_error)}"` : "";
  if (metric.mutation_score === null || metric.mutation_score === undefined || metric.mutation_score === "") {
    return `<span class="mutation-pill mutation-low"${mutationError}>Mutation unavailable</span>`;
  }
  const score = Number(metric.mutation_score);
  if (!Number.isFinite(score)) {
    return `<span class="mutation-pill mutation-low"${mutationError}>Mutation unavailable</span>`;
  }
  return `
    <button type="button" class="mutation-pill ${mutationScoreClass(score)} mutation-analysis-button" data-mutation-index="${index}">
      Mutation ${formatScore(score)}
    </button>
  `;
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

function metricForInvariant(invariant, index = -1) {
  const text = invariantText(invariant);
  const exact = currentMetrics.find((metric) => metric.invariant === text);
  if (exact) return exact;

  const key = normalizeInvariantKey(text);
  const normalized = currentMetrics.find((metric) => normalizeInvariantKey(metric.invariant) === key);
  if (normalized) return normalized;

  return currentMetrics[index] || null;
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
      ${mutationScoreMarkup(metric, index)}
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
  const rightSpace = window.innerWidth - rect.right;
  const left = rightSpace >= cardWidth + 18
    ? rect.right + 14
    : Math.max(12, rect.left - cardWidth - 14);
  const top = Math.min(Math.max(12, rect.top), window.innerHeight - 320);
  sourceHoverCard.style.width = `${cardWidth}px`;
  sourceHoverCard.style.left = `${left}px`;
  sourceHoverCard.style.top = `${top}px`;
  sourceHoverCard.classList.add("is-visible");
  sourceHoverCard.setAttribute("aria-hidden", "false");
}

function clearSourceEvidenceState() {
  document.querySelectorAll(".source-line.is-highlighted, .source-line.is-hovered, .source-code-line.is-highlighted, .source-code-line.is-hovered").forEach((line) => {
    line.classList.remove("is-highlighted", "is-hovered");
  });
  reviewPanel.querySelectorAll(".invariant-item.has-active-range").forEach((item) => {
    item.classList.remove("has-active-range");
  });
}

function hideSourceHoverCard() {
  sourceHoverCard.classList.remove("is-visible");
  sourceHoverCard.setAttribute("aria-hidden", "true");
  clearSourceEvidenceState();
}

function highlightSourceRange(range) {
  document.querySelectorAll(".source-line, .source-code-line").forEach((line) => {
    const lineNumber = Number(line.dataset.line);
    const highlighted = Boolean(range && lineNumber >= range.start && lineNumber <= range.end);
    line.classList.toggle("is-highlighted", highlighted);
    line.classList.toggle("is-hovered", highlighted);
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
    const hideRange = () => {
      hideSourceHoverCard();
    };

    item.addEventListener("pointerenter", showRange);
    item.addEventListener("pointermove", showRange);
    item.addEventListener("pointerleave", hideRange);
    item.addEventListener("mouseenter", showRange);
    item.addEventListener("mouseleave", hideRange);
    item.addEventListener("focusin", showRange);
    item.addEventListener("focusout", hideRange);
  });
}

function pointerIsInsideActiveInvariant(event) {
  const target = event.target;
  return Boolean(target?.closest?.(".invariant-item"));
}

function eventIsInsideInvariant(event) {
  return Boolean(event.target?.closest?.(".invariant-item"));
}

document.addEventListener("pointermove", (event) => {
  if (!sourceHoverCard.classList.contains("is-visible")) return;
  if (eventIsInsideInvariant(event)) return;
  hideSourceHoverCard();
}, true);

document.addEventListener("mouseover", (event) => {
  if (!sourceHoverCard.classList.contains("is-visible")) return;
  if (eventIsInsideInvariant(event)) return;
  hideSourceHoverCard();
}, true);

reviewPanel.addEventListener("pointerout", (event) => {
  if (!sourceHoverCard.classList.contains("is-visible")) return;
  const nextTarget = event.relatedTarget;
  if (nextTarget?.closest?.(".invariant-item")) return;
  hideSourceHoverCard();
}, true);

reviewPanel.addEventListener("mouseout", (event) => {
  if (!sourceHoverCard.classList.contains("is-visible")) return;
  const nextTarget = event.relatedTarget;
  if (nextTarget?.closest?.(".invariant-item")) return;
  hideSourceHoverCard();
}, true);

document.addEventListener("scroll", () => {
  if (sourceHoverCard.classList.contains("is-visible")) hideSourceHoverCard();
}, true);

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") hideSourceHoverCard();
});

async function renderInvariantReviewAnimated(invariants) {
  renderInvariantReview([]);
  const list = document.querySelector("#invariant-list");
  for (const [index, invariant] of invariants.entries()) {
    const metric = metricForInvariant(invariant, index);
    const wrapper = document.createElement("label");
    wrapper.className = "invariant-item invariant-enter";
    wrapper.dataset.index = String(index);
    const range = invariantRange(invariant);
    wrapper.innerHTML = `
      <input type="checkbox" checked data-index="${index}">
      <div class="invariant-copy">${renderMarkdown(invariantText(invariant))}</div>
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
    const metric = metricForInvariant(invariant, index);
    const range = invariantRange(invariant);
    return `
      <label class="invariant-item" data-index="${index}">
        <input type="checkbox" checked data-index="${index}">
        <div class="invariant-copy">${renderMarkdown(invariantText(invariant))}</div>
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

function mutationSeverity(mutant) {
  const text = `${mutant?.severity || ""} ${mutant?.status || ""} ${mutant?.raw || ""}`.toLowerCase();
  if (text.includes("severe") || text.includes("high")) return "severe";
  if (text.includes("medium") || text.includes("suspicious")) return "medium";
  if (text.includes("low") || text.includes("equivalent")) return "low";
  return "survived";
}

function mutationCountsMarkup(metric) {
  const counts = metric?.mutation_counts || {};
  const entries = [
    ["killed", "Killed"],
    ["survived", "Survived"],
    ["no_tests", "No tests"],
    ["timeout", "Timeout"],
    ["suspicious", "Suspicious"],
    ["skipped", "Skipped"],
  ].filter(([key]) => counts[key] !== undefined && counts[key] !== null && counts[key] !== "");

  if (!entries.length) return "";
  return `
    <div class="mutation-counts" aria-label="Mutation counts">
      ${entries.map(([key, label]) => `
        <span class="mutation-count mutation-count-${key}">
          <strong>${escapeHtml(counts[key])}</strong>
          ${label}
        </span>
      `).join("")}
    </div>
  `;
}

function renderSurvivedMutants(metric, index) {
  const mutants = Array.isArray(metric?.mutants) ? metric.mutants : [];
  if (!mutants.length) {
    return `
      <div class="mutation-empty">
        ${metric?.mutation_score === 1 ? "No survived mutants for this invariant." : "Run mutation analysis to list survived mutants."}
      </div>
    `;
  }

  return `
    <div class="survived-mutants">
      ${mutants.map((mutant, mutantIndex) => {
        const severity = mutationSeverity(mutant);
        const title = mutant.id || `Survived mutant ${mutantIndex + 1}`;
        return `
          <details class="survived-mutant survived-mutant-${severity}">
            <summary>
              <span class="survived-mutant-title">${escapeHtml(title)}</span>
              <span class="survived-mutant-badge">${escapeHtml(severity)}</span>
            </summary>
            ${mutant.raw ? `<p class="survived-mutant-status">${escapeHtml(mutant.raw)}</p>` : ""}
            ${mutant.diff ? `<pre class="mutation-diff"><code>${escapeHtml(mutant.diff)}</code></pre>` : ""}
            ${mutant.stderr ? `<pre class="mutation-stderr"><code>${escapeHtml(mutant.stderr)}</code></pre>` : ""}
            <button type="button" class="secondary-button retest-mutants-button" data-retest-index="${index}">Retest mutants</button>
          </details>
        `;
      }).join("")}
    </div>
  `;
}

function mutationIssueLabel(text, severity) {
  const normalized = `${text || ""}`.toLowerCase();
  if (normalized.includes("equivalent") || normalized.includes("unkillable") || severity === "low") {
    return "Likely equivalent / low impact";
  }
  if (normalized.includes("test") || normalized.includes("hypothesis") || normalized.includes("assert")) {
    return "PBT test gap";
  }
  if (normalized.includes("invariant") || normalized.includes("contract") || normalized.includes("documentation")) {
    return "Invariant gap";
  }
  if (severity === "medium") return "Needs review";
  return "Coverage gap";
}

function mutationSectionSeverity(text) {
  const normalized = `${text || ""}`.toLowerCase();
  if (normalized.includes("severe") || normalized.includes("high")) return "high";
  if (normalized.includes("low") || normalized.includes("equivalent") || normalized.includes("unkillable")) return "low";
  if (normalized.includes("medium") || normalized.includes("suspicious")) return "medium";
  return "medium";
}

function cleanMutationHeading(text) {
  return `${text || ""}`
    .replace(/^#{1,6}\s*/gm, "")
    .replace(/^[-*]\s*/gm, "")
    .replace(/\*\*/g, "")
    .replace(/`/g, "")
    .trim();
}

function splitMutationAnalysisSections(markdown) {
  const text = `${markdown || ""}`.trim();
  if (!text) return [];
  const lines = text.split(/\r?\n/);
  const sections = [];
  let current = [];

  const looksLikeNewMutant = (line) => /^\s*(#{1,5}\s*)?(?:mutant\s*(?:id)?|surviving mutant|severity\s*:)/i.test(line)
    || /^\s*[-*]\s*(?:mutant\s*(?:id)?|severity\s*:)/i.test(line);

  const flush = () => {
    const body = current.join("\n").trim();
    if (body) sections.push({ severity: mutationSectionSeverity(body), text: body });
    current = [];
  };

  lines.forEach((line) => {
    if (looksLikeNewMutant(line) && current.length) flush();
    current.push(line);
  });
  flush();

  if (sections.length <= 1) {
    const paragraphs = text.split(/\n{2,}/).map((part) => part.trim()).filter(Boolean);
    if (paragraphs.length > 1) {
      return paragraphs.map((part) => ({ severity: mutationSectionSeverity(part), text: part }));
    }
  }
  return sections;
}

function compactMutationText(markdown, maxLength = 280) {
  const plain = cleanMutationHeading(markdown)
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/\s+/g, " ")
    .trim();
  if (plain.length <= maxLength) return plain;
  return `${plain.slice(0, maxLength).trim()}...`;
}

function mutationGroupSummary(groups) {
  return [
    ["high", "High", groups.high.length],
    ["medium", "Medium", groups.medium.length],
    ["low", "Low", groups.low.length],
  ].map(([key, label, count]) => `
    <span class="mutation-summary-pill mutation-summary-${key}">
      <strong>${count}</strong>${label}
    </span>
  `).join("");
}

function renderMutationUnavailable(metric) {
  if (!metric?.mutation_error) return "";
  const error = `${metric.mutation_error}`;
  const lower = error.toLowerCase();
  let reason = "Mutation testing could not finish for this invariant.";
  let source = "Runner issue";
  if (lower.includes("generated mutation test failed") || lower.includes("pytest") || lower.includes("hypothesis")) {
    reason = "The generated PBT failed on the original source, so mutmut was skipped.";
    source = "PBT test issue";
  } else if (lower.includes("install") || lower.includes("import") || lower.includes("module") || lower.includes("dependency")) {
    reason = "A dependency/import failed while preparing the temporary mutation project.";
    source = "Dependency issue";
  } else if (lower.includes("no usable mutation") || lower.includes("no mutants") || lower.includes("did not produce")) {
    reason = "mutmut ran but did not produce usable scored mutants for this snippet.";
    source = "Snippet issue";
  }
  return `
    <aside class="mutation-unavailable-card">
      <span class="mutation-diagnostic-chip">${escapeHtml(source)}</span>
      <strong>Mutation analysis unavailable</strong>
      <p>${escapeHtml(reason)}</p>
      <details>
        <summary>Show diagnostic</summary>
        <pre>${escapeHtml(error)}</pre>
      </details>
    </aside>
  `;
}

function renderMutationAnalysisGrouped(metric) {
  const markdown = `${metric?.mutation_analysis || ""}`.trim();
  if (!markdown) return "";

  const groups = { high: [], medium: [], low: [] };
  splitMutationAnalysisSections(markdown).forEach((section) => {
    groups[section.severity || "medium"].push(section);
  });

  const meta = [
    ["high", "High severity", "Likely real gap", "Prioritize these. They usually mean the invariant or the PBT should catch behavior that currently survives."],
    ["medium", "Medium severity", "Review carefully", "These may be meaningful, but could need stronger source context or a better generated test."],
    ["low", "Low severity", "Likely equivalent", "These are often equivalent, cosmetic, unreachable, or too low-impact to document heavily."],
  ];

  const renderedGroups = meta.map(([key, title, subtitle, help]) => {
    const items = groups[key];
    return `
      <section class="mutation-risk-group mutation-risk-${key}" style="--group-count: ${items.length}">
        <header class="mutation-risk-header">
          <div>
            <span class="mutation-severity-chip">${title}</span>
            <h5>${subtitle}</h5>
          </div>
          <span class="mutation-group-count">${items.length}</span>
        </header>
        <p class="mutation-group-help">${help}</p>
        ${items.length ? `
          <div class="mutation-analysis-items">
            ${items.map((item, itemIndex) => `
              <article class="mutation-analysis-item" style="--item-index: ${itemIndex}">
                <div class="mutation-item-topline">
                  <span class="mutation-origin-chip">${escapeHtml(mutationIssueLabel(item.text, key))}</span>
                </div>
                <p class="mutation-analysis-preview">${escapeHtml(compactMutationText(item.text))}</p>
                <details>
                  <summary>Details</summary>
                  <div class="markdown-rendered mutation-analysis-detail">${renderMarkdown(item.text)}</div>
                </details>
              </article>
            `).join("")}
          </div>
        ` : `<p class="mutation-none">No ${title.toLowerCase()} mutants detected.</p>`}
      </section>
    `;
  }).join("");

  return `
    <div class="mutation-analysis-pretty">
      <header class="mutation-analysis-hero">
        <div>
          <p class="eyebrow">Mutation analysis</p>
          <h4>Surviving mutants by risk</h4>
          <p>High usually means a real invariant/PBT gap; medium needs human review; low is often equivalent or low-impact.</p>
        </div>
        <div class="mutation-summary-strip">${mutationGroupSummary(groups)}</div>
      </header>
      <div class="mutation-risk-grid">${renderedGroups}</div>
      <details class="mutation-raw-analysis">
        <summary>Show original GPT notes</summary>
        <div class="markdown-rendered mutation-analysis-detail">${renderMarkdown(markdown)}</div>
      </details>
    </div>
  `;
}

function renderMutationReport(metric, index) {
  if (!showMutationTestingInput.checked && !metric?.mutation_analysis && !metric?.mutants) {
    return "";
  }
  return `
    <div class="mutation-report">
      <div class="mutation-report-header">
        <div>
          <p class="eyebrow">Mutation testing</p>
          <h4>${metric?.mutation_score === null || metric?.mutation_score === undefined ? "Mutation details" : `Mutation score ${formatScore(metric.mutation_score)}`}</h4>
        </div>
        <button type="button" class="secondary-button retest-mutants-button" data-retest-index="${index}">Retest mutants</button>
      </div>
      ${mutationCountsMarkup(metric)}
      ${renderSurvivedMutants(metric, index)}
      ${renderMutationUnavailable(metric)}
      ${metric?.mutation_analysis ? `
        <details class="mutation-analysis-copy">
          <summary>Analysis notes</summary>
          <div class="mutation-analysis-markdown">${renderMutationAnalysisGrouped(metric)}</div>
        </details>
      ` : ""}
    </div>
  `;
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
        <details class="test-item ${metric?.mutation_analysis || metric?.mutation_error || (Array.isArray(metric?.mutants) && metric.mutants.length) ? "has-mutation-report" : ""}" ${index === selectedTestIndex ? "open" : ""}>
          <summary>
            <span class="test-summary-title">Invariant ${index + 1}</span>
            <span class="test-summary-metrics">
              <span class="confidence-pill confidence-${confidenceLabel(metric).toLowerCase()}">${confidenceLabel(metric)} ${formatScore(metricScore(metric))}</span>
              <span>${formatScore(metric.validity)} valid / ${formatScore(metric.soundness)} sound</span>
              ${mutationScoreMarkup(metric, index)}
            </span>
          </summary>
          <div class="test-invariant-copy">${renderMarkdown(metric.invariant || "")}</div>
          ${metric.explanation ? `<p class="metric-explanation">${escapeHtml(metric.explanation)}</p>` : ""}
          ${metric.error ? `<p class="metric-error">${escapeHtml(metric.error)}</p>` : ""}
          ${renderMutationReport(metric, index)}
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

async function runMutationAnalysis(index, button) {
  const metric = currentMetrics[index];
  if (!metric || !metric.test_code) return;

  button.disabled = true;
  button.textContent = "Analyzing...";
  setStatus("review", "Analyzing mutants");

  try {
    const data = await postJson("/api/mutation-analysis", {
      api_name: apiNameInput.value.trim() || "api.function",
      source_code: currentSource,
      test_code: metric.test_code,
      mutation_packages: mutationPackagesInput.value.trim(),
      mutation_auto_install: mutationAutoInstallInput.checked
    }, { cache: false });

    currentMetrics[index] = {
      ...metric,
      mutation_analysis: data.analysis || "",
      mutants: Array.isArray(data.mutants) ? data.mutants : [],
      mutation_counts: data.mutation_counts || metric.mutation_counts || {},
      mutation_score: data.mutation_score ?? metric.mutation_score
    };
    selectedTestIndex = index;
    renderInvariantReviewWithMetrics(currentInvariants);
    renderTestsPanel();
    showTestsStage(index);
    setStatus("ready", "Mutation report ready");
  } catch (error) {
    button.disabled = false;
    button.textContent = `Mutation ${formatScore(metric.mutation_score)}`;
    setStatus("draft", "Mutation analysis failed");
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
    invariants: invariantTexts(currentInvariants),
    show_mutation_tests: showMutationTestingInput.checked,
    mutation_packages: mutationPackagesInput.value.trim(),
    mutation_auto_install: mutationAutoInstallInput.checked
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
  const mutationButton = event.target.closest(".mutation-analysis-button");
  if (mutationButton) {
    event.preventDefault();
    event.stopPropagation();
    runMutationAnalysis(Number(mutationButton.dataset.mutationIndex || 0), mutationButton).catch((error) => {
      renderError(error.message || "Could not analyze the mutation report.", "Mutation analysis failed", "Could not analyze mutants");
    });
    return;
  }

  const button = event.target.closest(".metric-test-button");
  if (!button) return;
  event.preventDefault();
  event.stopPropagation();
  showTestsStage(Number(button.dataset.testIndex || 0));
});

testsPanel.addEventListener("click", async (event) => {
  const mutationButton = event.target.closest(".mutation-analysis-button");
  if (mutationButton) {
    event.preventDefault();
    try {
      await runMutationAnalysis(Number(mutationButton.dataset.mutationIndex || 0), mutationButton);
    } catch (error) {
      renderError(error.message || "Could not analyze the mutation report.", "Mutation analysis failed", "Could not analyze mutants");
    }
    return;
  }

  const retestButton = event.target.closest(".retest-mutants-button");
  if (retestButton) {
    event.preventDefault();
    try {
      await runMutationAnalysis(Number(retestButton.dataset.retestIndex || 0), retestButton);
    } catch (error) {
      renderError(error.message || "Could not retest the survived mutants.", "Mutation retest failed", "Could not retest mutants");
    }
    return;
  }

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

if (themeToggle) {
  themeToggle.addEventListener("click", () => {
    const nextMode = document.body.classList.contains("dark-mode") ? "light" : "dark";
    localStorage.setItem(DARK_MODE_STORAGE_KEY, nextMode);
    applyTheme(nextMode);
  });
}

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

showMutationTestingInput.addEventListener("change", async () => {
  if (!currentInvariants.length) {
    return;
  }
  if (!assessMetricsInput.checked) {
    renderInvariantReviewWithMetrics(currentInvariants);
    renderTestsPanel();
    return;
  }
  try {
    await assessMetricsForReview();
  } catch (error) {
    renderError(error.message || "Mutation metric assessment failed.", "Mutation metrics failed", "Could not assess mutation");
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
