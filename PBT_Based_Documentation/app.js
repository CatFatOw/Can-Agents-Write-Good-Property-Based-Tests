const form = document.querySelector("#documentation-form");
const landingPage = document.querySelector("#landing-page");
const loginPage = document.querySelector("#login-page");
const areaPage = document.querySelector("#area-page");
const appShell = document.querySelector("#app-shell");
const launchAppButtons = Array.from(document.querySelectorAll(".launch-app-button"));
const loginOpenButtons = Array.from(document.querySelectorAll(".login-open-button"));
const areaOpenButtons = Array.from(document.querySelectorAll(".area-open-button"));
const homeButton = document.querySelector("#home-button");
const areaBackButton = document.querySelector(".area-back-button");
const areaNextButton = document.querySelector("#area-next-button");
const areaVoteButton = document.querySelector("#area-vote-button");
const areaVoteMessage = document.querySelector("#area-vote-message");
const areaCommentInput = document.querySelector("#area-comment-input");
const areaRankCount = document.querySelector("#area-rank-count");
const areaRankLimitInput = document.querySelector("#area-rank-limit");
const areaLimitMessage = document.querySelector("#area-limit-message");
const areaTitle = document.querySelector("#area-battle-title");
const areaTdTitle = document.querySelector("#area-td-title");
const areaIbdTitle = document.querySelector("#area-ibd-title");
const areaTdDoc = document.querySelector("#area-td-doc");
const areaIbdDoc = document.querySelector("#area-ibd-doc");
const areaSidebar = document.querySelector("#area-sidebar");
const areaStudyView = document.querySelector("#area-study-view");
const areaStudyTab = document.querySelector("#area-study-tab");
const areaResultsTab = document.querySelector("#area-results-tab");
const areaLeaderboardList = document.querySelector("#area-leaderboard-list");
const landingLeaderboardSection = document.querySelector("#leaderboard");
const landingLeaderboardList = document.querySelector("#landing-leaderboard-list");
const areaChoices = Array.from(document.querySelectorAll(".area-choice"));
const authBackButton = document.querySelector(".auth-back-button");
const authForm = document.querySelector("#auth-form");
const authEmailInput = document.querySelector("#auth-email");
const authPasswordInput = document.querySelector("#auth-password");
const authMessage = document.querySelector("#auth-message");
const authSubmitButton = document.querySelector("#auth-submit-button");
const authModeToggle = document.querySelector("#auth-mode-toggle");
const researchModal = document.querySelector("#research-modal");
const researchPhraseInput = document.querySelector("#research-phrase");
const researchLimitInput = document.querySelector("#research-limit");
const researchMessage = document.querySelector("#research-message");
const researchConfirmButton = document.querySelector("#research-confirm-button");
const researchCancelButton = document.querySelector("#research-cancel-button");
const researchCurrentPhraseInput = document.querySelector("#research-current-phrase");
const researchNewPhraseInput = document.querySelector("#research-new-phrase");
const researchChangePhraseButton = document.querySelector("#research-change-phrase-button");
const researchPhraseMessage = document.querySelector("#research-phrase-message");
const landingAccountButton = document.querySelector("#landing-account-button");
const databaseStatus = document.querySelector("#database-status");
const databaseStatusText = document.querySelector("#database-status-text");
const accountMenuButton = document.querySelector("#account-menu-button");
const accountMenuLabel = document.querySelector("#account-menu-label");
const accountMenu = document.querySelector("#account-menu");
const savedDocSearchInput = document.querySelector("#saved-doc-search");
const savedDocRefreshButton = document.querySelector("#saved-doc-refresh");
const savedDocList = document.querySelector("#saved-doc-list");
const logoutButton = document.querySelector("#logout-button");
const accountPageButton = document.querySelector("#account-page-button");
const accountPage = document.querySelector("#account-page");
const accountBackButton = document.querySelector(".account-back-button");
const accountEmail = document.querySelector("#account-email");
const accountCreated = document.querySelector("#account-created");
const accountId = document.querySelector("#account-id");
const accountDocCount = document.querySelector("#account-doc-count");
const accountStats = document.querySelector("#account-stats");
const accountDocsList = document.querySelector("#account-docs-list");
const accountDocsRefresh = document.querySelector("#account-docs-refresh");
const accountDocsSearch = document.querySelector("#account-docs-search");
const passwordForm = document.querySelector("#password-form");
const currentPasswordInput = document.querySelector("#current-password");
const newPasswordInput = document.querySelector("#new-password");
const confirmPasswordInput = document.querySelector("#confirm-password");
const passwordMessage = document.querySelector("#password-message");
const passwordSubmit = document.querySelector("#password-submit");
const deleteAccountButton = document.querySelector("#delete-account-button");
const deleteMessage = document.querySelector("#delete-message");
const accountDeleteConfirm = document.querySelector("#account-delete-confirm");
const deleteConfirmInput = document.querySelector("#delete-confirm-input");
const deleteConfirmButton = document.querySelector("#delete-confirm-button");
const deleteCancelButton = document.querySelector("#delete-cancel-button");
const deleteConfirmPhrase = document.querySelector("#delete-confirm-phrase");
const accountDocsSort = document.querySelector("#account-docs-sort");
const accountDetailModal = document.querySelector("#account-detail-modal");
const accountDetailClose = document.querySelector("#account-detail-close");
const accountDetailTitle = document.querySelector("#account-detail-title");
const accountDetailEyebrow = document.querySelector("#account-detail-eyebrow");
const accountDetailBody = document.querySelector("#account-detail-body");
const documentationInput = document.querySelector("#documentation");
const apiNameInput = document.querySelector("#api-name");
const sourceObjectInput = document.querySelector("#source-object");
const lookupButton = document.querySelector("#lookup-button");
const themeToggle = document.querySelector("#theme-toggle");
const themeToggles = Array.from(document.querySelectorAll(".theme-toggle"));
const toneInput = document.querySelector("#tone");
const modelProviderInput = document.querySelector("#model-provider");
const openaiKeyInput = document.querySelector("#openai-key");
const apiKeyLabel = document.querySelector("#api-key-label");
const modelBaseUrlField = document.querySelector("#model-base-url-field");
const modelBaseUrlInput = document.querySelector("#model-base-url");
const markdownModelInput = document.querySelector("#markdown-model");
const metricsModelInput = document.querySelector("#metrics-model");
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
const coveragePanel = document.querySelector("#coverage-panel");
const coverageDocsInput = document.querySelector("#coverage-docs-input");
const runCoverageButton = document.querySelector("#run-coverage-button");
const coverageEmpty = document.querySelector("#coverage-empty");
const coverageResults = document.querySelector("#coverage-results");
const coverageScoreRing = document.querySelector("#coverage-score-ring");
const coverageScoreValue = document.querySelector("#coverage-score-value");
const coverageScoreTitle = document.querySelector("#coverage-score-title");
const coverageScoreNote = document.querySelector("#coverage-score-note");
const coverageDocStatements = document.querySelector("#coverage-doc-statements");
const coverageRenderedDocs = document.querySelector("#coverage-rendered-docs");
const coverageSourceLines = document.querySelector("#coverage-source-lines");
const coverageFullscreenButton = document.querySelector("#coverage-fullscreen-button");
const coverageFullscreenModal = document.querySelector("#coverage-fullscreen-modal");
const coverageFullscreenClose = document.querySelector("#coverage-fullscreen-close");
const coverageFullscreenSourceLines = document.querySelector("#coverage-fullscreen-source-lines");
const coverageFullscreenRenderedDocs = document.querySelector("#coverage-fullscreen-rendered-docs");
const coverageFullscreenDocStatements = document.querySelector("#coverage-fullscreen-doc-statements");
const generatedDocsTitle = document.querySelector("#generated-docs-title");
const originalExampleDocs = document.querySelector("#original-example-docs");
const invariantExampleDocs = document.querySelector("#invariant-example-docs");
const publicExampleTitle = document.querySelector("#public-example-title");
const invariantExampleTitle = document.querySelector("#invariant-example-title");
const generatedDoc = document.querySelector("#generated-doc");
const tdPanel = document.querySelector("#td-panel");
const tdSourceInput = document.querySelector("#td-source-input");
const tdFormatButton = document.querySelector("#td-format-button");
const tdSaveButton = document.querySelector("#td-save-button");
const tdPreview = document.querySelector("#td-preview");
const tdMessage = document.querySelector("#td-message");
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
let currentCoverageData = null;
let clickSparkId = 0;

function installClickPolish() {
  const clickableSelector = [
    "button",
    "[role='button']",
    "summary",
    ".docs-example-choice",
    ".generated-doc-tab",
    ".coverage-doc-highlight-block",
    ".coverage-source-line"
  ].join(", ");

  document.addEventListener("pointerdown", (event) => {
    if (event.button !== undefined && event.button !== 0) return;
    const target = event.target.closest(clickableSelector);
    if (!target || target.disabled || target.getAttribute("aria-disabled") === "true") return;

    target.classList.remove("is-click-pulsing");
    void target.offsetWidth;
    target.classList.add("is-click-pulsing");
    window.setTimeout(() => target.classList.remove("is-click-pulsing"), 520);

    if (!target.matches("button, [role='button'], summary, .docs-example-choice, .generated-doc-tab")) return;
    const rect = target.getBoundingClientRect();
    const spark = document.createElement("span");
    spark.className = "click-spark";
    spark.style.left = `${event.clientX - rect.left}px`;
    spark.style.top = `${event.clientY - rect.top}px`;
    spark.dataset.sparkId = String(clickSparkId += 1);
    target.appendChild(spark);
    window.setTimeout(() => spark.remove(), 620);
  }, { passive: true });
}


installClickPolish();
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
const ACCESS_TOKEN_STORAGE_KEY = "ibd-access-token";
const USER_EMAIL_STORAGE_KEY = "ibd-user-email";
const ARENA_RANK_COUNT_STORAGE_KEY = "ibd-arena-rank-count";
const ARENA_RANK_LIMIT_STORAGE_KEY = "ibd-arena-rank-limit";
const RESEARCH_MODE_STORAGE_KEY = "ibd-research-mode";
const RESEARCH_PHRASE_STORAGE_KEY = "ibd-research-phrase";
const API_BASE_URL = window.location.protocol === "file:" ? "http://127.0.0.1:8011" : "";
let authMode = "login";
let researchModalMode = "enter";
let savedDocumentation = [];
let activeSavedDocumentation = null;
let comparisonLeaderboardRows = [];
let activeAreaIndex = 0;
let selectedAreaWinner = null;
let activeAreaSides = { A: "TD", B: "IBD" };
let areaVoteSubmitted = false;
let areaLoading = false;
let currentAreaPost = null;
const areaFallbackPosts = [
  {
    title: "Anonymous np.pad documentation comparison",
    label: "np.pad",
    originalPath: "examples/numpy_pad_original_docs.md",
    invariantPath: "examples/numpy_pad_invariant_docs.md",
    tdDoc: "",
    ibdDoc: "",
    ibdElo: 1248,
    tdElo: 1189,
    ibdWins: 26,
    tdWins: 16,
    bt: 0.62
  },
  {
    title: "Anonymous np.linspace documentation comparison",
    label: "np.linspace",
    originalPath: "examples/numpy_linspace_original_docs.md",
    invariantPath: "examples/numpy_linspace_invariant_docs.md",
    tdDoc: "",
    ibdDoc: "",
    ibdElo: 1312,
    tdElo: 1166,
    ibdWins: 34,
    tdWins: 13,
    bt: 0.71
  }
];

function showLandingPage() {
  if (isResearchModeActive()) {
    showAreaPage();
    return;
  }
  landingPage?.classList.remove("is-hidden");
  loginPage?.classList.add("is-hidden");
  areaPage?.classList.add("is-hidden");
  appShell?.classList.add("is-hidden");
  accountPage?.classList.add("is-hidden");
  document.body.classList.remove("app-active", "auth-active", "account-active", "area-active");
  document.body.classList.add("landing-active");
  updateAccountMenuLabel();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function showAppPage() {
  if (isResearchModeActive()) {
    showAreaPage();
    return;
  }
  landingPage?.classList.add("is-hidden");
  loginPage?.classList.add("is-hidden");
  areaPage?.classList.add("is-hidden");
  appShell?.classList.remove("is-hidden");
  accountPage?.classList.add("is-hidden");
  document.body.classList.remove("landing-active", "auth-active", "account-active", "area-active");
  document.body.classList.add("app-active");
  updateAccountMenuLabel();
  refreshDatabaseStatus();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

async function showAreaPage() {
  landingPage?.classList.add("is-hidden");
  loginPage?.classList.add("is-hidden");
  appShell?.classList.add("is-hidden");
  accountPage?.classList.add("is-hidden");
  areaPage?.classList.remove("is-hidden");
  document.body.classList.remove("landing-active", "auth-active", "app-active", "account-active");
  document.body.classList.add("area-active");
  document.body.classList.toggle("research-mode", isResearchModeActive());
  accountMenu?.classList.add("is-hidden");
  accountMenuButton?.setAttribute("aria-expanded", "false");
  updateAreaSessionUI();
  await loadAreaComparison();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function isResearchModeActive() {
  return localStorage.getItem(RESEARCH_MODE_STORAGE_KEY) === "true";
}

function researchPhrase() {
  return localStorage.getItem(RESEARCH_PHRASE_STORAGE_KEY) || "rice";
}

function openResearchModal(mode = isResearchModeActive() ? "exit" : "enter") {
  researchModalMode = mode;
  researchModal?.classList.remove("is-hidden");
  document.body.classList.add("research-modal-open");
  if (researchMessage) researchMessage.textContent = "";
  if (researchPhraseMessage) researchPhraseMessage.textContent = "";
  if (researchPhraseInput) researchPhraseInput.value = "";
  if (researchCurrentPhraseInput) researchCurrentPhraseInput.value = "";
  if (researchNewPhraseInput) researchNewPhraseInput.value = "";
  if (researchLimitInput) {
    researchLimitInput.value = mode === "enter" ? String(areaRankLimitValue() || 10) : "";
    researchLimitInput.closest(".field")?.classList.toggle("is-hidden", mode === "exit");
  }
  if (researchConfirmButton) {
    researchConfirmButton.textContent = mode === "exit" ? "Exit research mode" : "Enter research mode";
  }
  researchPhraseInput?.focus();
}

function closeResearchModal() {
  researchModal?.classList.add("is-hidden");
  document.body.classList.remove("research-modal-open");
}

function toggleResearchMode() {
  const active = isResearchModeActive();
  openResearchModal(active ? "exit" : "enter");
}

function confirmResearchMode() {
  if (researchPhraseInput?.value !== researchPhrase()) {
    if (researchMessage) researchMessage.textContent = "Incorrect phrase.";
    researchPhraseInput?.focus();
    return;
  }
  if (researchModalMode === "enter") {
    const limit = Number(researchLimitInput?.value || 10);
    if (!limit || limit < 1) {
      if (researchMessage) researchMessage.textContent = "Set a ranking limit for research mode.";
      researchLimitInput?.focus();
      return;
    }
    localStorage.setItem(ARENA_RANK_LIMIT_STORAGE_KEY, String(limit));
    localStorage.setItem(ARENA_RANK_COUNT_STORAGE_KEY, "0");
    localStorage.setItem(RESEARCH_MODE_STORAGE_KEY, "true");
    document.body.classList.add("research-mode");
    closeResearchModal();
    showAreaPage();
  } else {
    localStorage.setItem(RESEARCH_MODE_STORAGE_KEY, "false");
    localStorage.removeItem(ARENA_RANK_LIMIT_STORAGE_KEY);
    document.body.classList.remove("research-mode");
    closeResearchModal();
    showLandingPage();
  }
}

function changeResearchPhrase() {
  if (researchCurrentPhraseInput?.value !== researchPhrase()) {
    if (researchPhraseMessage) researchPhraseMessage.textContent = "Current phrase is incorrect.";
    researchCurrentPhraseInput?.focus();
    return;
  }
  const nextPhrase = (researchNewPhraseInput?.value || "").trim();
  if (nextPhrase.length < 3) {
    if (researchPhraseMessage) researchPhraseMessage.textContent = "Use at least 3 characters.";
    researchNewPhraseInput?.focus();
    return;
  }
  localStorage.setItem(RESEARCH_PHRASE_STORAGE_KEY, nextPhrase);
  if (researchPhraseMessage) researchPhraseMessage.textContent = "Research phrase updated.";
  if (researchCurrentPhraseInput) researchCurrentPhraseInput.value = "";
  if (researchNewPhraseInput) researchNewPhraseInput.value = "";
}

function areaRankCountValue() {
  return Number(localStorage.getItem(ARENA_RANK_COUNT_STORAGE_KEY) || 0);
}

function areaRankLimitValue() {
  if (!isResearchModeActive()) return 0;
  return Number(localStorage.getItem(ARENA_RANK_LIMIT_STORAGE_KEY) || 0);
}

function updateAreaSessionUI() {
  const count = areaRankCountValue();
  const limit = areaRankLimitValue();
  if (areaRankCount) {
    areaRankCount.textContent = limit ? `${count} / ${limit} ranked` : `${count} ranked`;
  }
  if (areaRankLimitInput) {
    areaRankLimitInput.value = limit ? String(limit) : "";
  }
  if (areaLimitMessage) {
    areaLimitMessage.textContent = isResearchModeActive()
      ? (limit && count >= limit ? "Research limit reached. Enter the phrase to exit or increase the limit." : "Research mode limit is enforced.")
      : "Normal mode is unlimited.";
  }
  if (areaVoteButton) {
    areaVoteButton.disabled = Boolean((limit && count >= limit) || !selectedAreaWinner);
  }
}

function incrementAreaRankCount() {
  localStorage.setItem(ARENA_RANK_COUNT_STORAGE_KEY, String(areaRankCountValue() + 1));
  updateAreaSessionUI();
}

function getAccessToken() {
  return localStorage.getItem(ACCESS_TOKEN_STORAGE_KEY) || "";
}

function getSavedUserEmail() {
  return localStorage.getItem(USER_EMAIL_STORAGE_KEY) || "";
}

function authHeaders(extra = {}) {
  const token = getAccessToken();
  return token ? { ...extra, Authorization: `Bearer ${token}` } : extra;
}

function apiUrl(path) {
  if (/^https?:\/\//i.test(path)) return path;
  return `${API_BASE_URL}${path.startsWith("/") ? path : `/${path}`}`;
}

function areaPostVoteCount(post) {
  return (post.ibdWins || 0) + (post.tdWins || 0);
}

function normalizeAreaPost(data) {
  return {
    id: data.documentation_id,
    title: data.documentation_title || "Documentation comparison",
    label: data.documentation_title || "Documentation sample",
    tdDoc: data.td_doc || "",
    ibdDoc: data.ibd_doc || "",
    ibdElo: Number(data.ibd_doc_elo_rating || 1000),
    tdElo: Number(data.td_doc_elo_rating || 1000),
    ibdWins: Number(data.IBD_wins || 0),
    tdWins: Number(data.TD_wins || 0),
    ibdWinPercentage: Number(data.IBD_win_percentage || 0),
    tdWinPercentage: Number(data.TD_win_percentage || 0),
    bt: Number(data.bt_ibd_win_prob || 0)
  };
}

async function hydrateAreaPostDocs(post) {
  if (!post || post.docsLoaded || (!post.originalPath && !post.invariantPath)) return post;
  const [originalResponse, invariantResponse] = await Promise.all([
    fetch(post.originalPath),
    fetch(post.invariantPath)
  ]);
  if (!originalResponse.ok || !invariantResponse.ok) {
    throw new Error("Could not load bundled documentation examples.");
  }
  post.tdDoc = await originalResponse.text();
  post.ibdDoc = await invariantResponse.text();
  post.docsLoaded = true;
  return post;
}

async function loadAreaComparison() {
  if (areaLoading) return;
  areaLoading = true;
  areaVoteSubmitted = false;
  randomizeAreaSides();
  if (areaVoteMessage) areaVoteMessage.textContent = "Loading anonymous documentation samples...";
  if (areaVoteButton) areaVoteButton.disabled = true;
  try {
    const response = await fetch(apiUrl("/comparison/random"));
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || "No comparison documents are available yet.");
    currentAreaPost = normalizeAreaPost(data);
  } catch (error) {
    currentAreaPost = areaFallbackPosts[activeAreaIndex] || areaFallbackPosts[0];
    await hydrateAreaPostDocs(currentAreaPost).catch((fallbackError) => {
      if (areaVoteMessage) areaVoteMessage.textContent = fallbackError.message;
    });
    if (areaVoteMessage) {
      areaVoteMessage.textContent = `${error.message || "Could not load a saved comparison."} Showing bundled examples.`;
    }
  } finally {
    areaLoading = false;
    if (areaVoteButton) areaVoteButton.disabled = false;
    renderAreaPost();
    updateAreaSessionUI();
  }
}

function anonymizeAreaDocument(markdown, label) {
  const candidate = `Candidate ${label}`;
  return String(markdown || "")
    .split(/\r?\n/)
    .map((line) => {
      // Blind-study anonymization: keep the documentation itself intact, while
      // removing labels, source lines, and URLs that reveal the generation path.
      if (/^\s*(?:>\s*)?(?:source|url|original source|reference source)\s*:/i.test(line)) {
        return "";
      }
      if (/^\s{0,3}#{1,6}\s+.*\b(original|ibd|td|traditional|invariant[-\s]?based|baseline|generated)\b/i.test(line)) {
        const depth = line.match(/^\s{0,3}(#{1,6})/)?.[1] || "##";
        return `${depth} ${candidate}`;
      }
      return line
        .replace(/\[[^\]]+\]\((?:https?:\/\/|www\.)[^)]+\)/gi, "reference")
        .replace(/https?:\/\/\S+|www\.\S+/gi, "")
        .replace(/\b(?:public|official|original)?\s*(?:NumPy\s+)?reference documentation\b/gi, "reference documentation")
        .replace(/\b(IBD_generated_md|TD_md|ibd_doc|td_doc|post_IBD|post_TD)\b/gi, candidate)
        .replace(/\b(?:original|traditional|baseline)\s+documentation\b/gi, `${candidate} documentation`)
        .replace(/\binvariant[-\s]?based documentation\b/gi, `${candidate} documentation`)
        .replace(/\b(?:IBD|TD)\b/gi, candidate);
    })
    .join("\n");
}

function getAreaCandidateDocument(post, label) {
  const type = activeAreaSides[label];
  const sourceDoc = type === "IBD" ? post.ibdDoc : post.tdDoc;
  const text = anonymizeAreaDocument(sourceDoc, label).trim();
  return text || "No documentation text is available for this candidate.";
}

function areaCandidateLabelForWinner(winner) {
  return activeAreaSides.A === winner ? "Candidate A" : "Candidate B";
}

function formatLeaderboardComments(entry) {
  const raw = entry.comments || entry.recent_comments || entry.review_comments || entry.voter_comments || [];
  const comments = Array.isArray(raw)
    ? raw
    : String(raw || "").split(/\n+/).filter(Boolean);
  if (!comments.length) return '<p class="placeholder">No reviewer comments recorded yet.</p>';
  return `
    <ul class="area-comment-list">
      ${comments.slice(0, 8).map((comment) => {
        const winner = typeof comment === "string" ? "" : String(comment.winner || comment.choice || "").toUpperCase();
        const label = winner === "IBD" ? "Invariant-based" : winner === "TD" ? "Baseline" : "Comment";
        const text = typeof comment === "string" ? comment : comment.comments || comment.comment || "No comment";
        const tone = winner === "IBD" ? "ibd" : winner === "TD" ? "td" : "neutral";
        return `
          <li class="area-comment-item is-${tone}">
            <span>${escapeHtml(label)}</span>
            <p>${escapeHtml(text)}</p>
          </li>
        `;
      }).join("")}
    </ul>
  `;
}

function renderLeaderboardDocumentationMenu(entry) {
  const ibdMarkdown = entry.IBD_generated_md || entry.ibd_doc || entry.ibd_markdown || "";
  const tdMarkdown = entry.TD_md || entry.td_doc || entry.td_markdown || "";
  const sourceCode = entry.source_code || entry.source || "";
  const invariants = parseStoredInvariants(entry.invariants);
  const metrics = parseStoredMetrics(entry.hypothesis_tests);
  if (!ibdMarkdown && !tdMarkdown && !sourceCode && !invariants.length && !metrics.length) {
    return '<p class="placeholder">No documentation details are available for this leaderboard row yet.</p>';
  }
  return `
    <div class="leaderboard-doc-menu">
      ${ibdMarkdown ? `
        <details>
          <summary>IBD Markdown</summary>
          <div class="markdown-rendered landing-doc-scroll leaderboard-doc-preview">${renderMarkdown(ibdMarkdown)}</div>
        </details>
      ` : ""}
      ${tdMarkdown ? `
        <details>
          <summary>TD Markdown</summary>
          <div class="markdown-rendered landing-doc-scroll leaderboard-doc-preview">${renderMarkdown(tdMarkdown)}</div>
        </details>
      ` : ""}
      ${sourceCode ? `
        <details>
          <summary>Source code</summary>
          <pre class="md-code landing-doc-scroll leaderboard-doc-preview"><code>${escapeHtml(sourceCode)}</code></pre>
        </details>
      ` : ""}
      ${invariants.length ? `
        <details>
          <summary>Invariants (${invariants.length})</summary>
          <ul class="leaderboard-invariant-list">
            ${invariants.map((invariant) => `<li>${escapeHtml(invariant)}</li>`).join("")}
          </ul>
        </details>
      ` : ""}
      ${metrics.length ? `
        <details>
          <summary>Metrics &amp; PBT tests (${metrics.length})</summary>
          <div class="leaderboard-metric-list">
            ${metrics.map((metric, index) => `
              <details>
                <summary>Invariant ${index + 1}</summary>
                ${metric.invariant ? `<div class="markdown-rendered">${renderMarkdown(String(metric.invariant))}</div>` : ""}
                ${metric.test_code ? `<pre class="md-code"><code>${escapeHtml(metric.test_code)}</code></pre>` : ""}
              </details>
            `).join("")}
          </div>
        </details>
      ` : ""}
    </div>
  `;
}

function renderLeaderboardViz({ ibdPct, tdPct, ibdElo, tdElo, voteCount }) {
  if (!voteCount && !ibdElo && !tdElo && !ibdPct && !tdPct) {
    return '<p class="area-no-viz">No visualization to show for now.</p>';
  }
  const normalizedIbd = Math.max(8, Math.min(100, ibdPct));
  const normalizedTd = Math.max(8, Math.min(100, tdPct));
  const eloDelta = Number(ibdElo || 0) - Number(tdElo || 0);
  return `
    <div class="area-viz-grid" aria-label="Leaderboard visualizations">
      <div class="area-viz-card">
        <span class="area-viz-label">Preference split</span>
        <div class="area-mini-bars">
          <i style="--bar: ${normalizedIbd}%"><b>${ibdPct}%</b></i>
          <i style="--bar: ${normalizedTd}%"><b>${tdPct}%</b></i>
        </div>
      </div>
      <div class="area-viz-card">
        <span class="area-viz-label">Rating comparison</span>
        <div class="area-rating-pair">
          <span><strong>${ibdElo || "—"}</strong> Invariant-based</span>
          <span><strong>${tdElo || "—"}</strong> Baseline</span>
        </div>
      </div>
      <div class="area-viz-card">
        <span class="area-viz-label">Vote volume</span>
        <strong class="area-vote-volume">${voteCount}</strong>
        <small>${voteCount === 1 ? "comparison" : "comparisons"}</small>
      </div>
    </div>
  `;
}

async function fetchComparisonLeaderboard() {
  const response = await fetch(apiUrl("/comparison/leaderboard"));
  const data = await response.json().catch(() => []);
  if (!response.ok) throw new Error(data.detail || "Could not load leaderboard.");
  comparisonLeaderboardRows = Array.isArray(data) ? data : [];
  return comparisonLeaderboardRows;
}

function randomizeAreaSides() {
  if (Math.random() < 0.5) {
    activeAreaSides = { A: "TD", B: "IBD" };
  } else {
    activeAreaSides = { A: "IBD", B: "TD" };
  }
  selectedAreaWinner = null;
  areaVoteSubmitted = false;
}

async function renderLandingLeaderboard() {
  if (!landingLeaderboardList) return;
  landingLeaderboardSection?.classList.remove("is-hidden");
  landingLeaderboardList.innerHTML = '<li class="placeholder">Loading leaderboard...</li>';
  try {
    const ranked = (await fetchComparisonLeaderboard())
      .filter((entry) => String(entry.IBD_generated_md || entry.ibd_doc || "").trim() && String(entry.TD_md || entry.td_doc || "").trim());
    if (!ranked.length) {
      landingLeaderboardSection?.classList.add("is-hidden");
      landingLeaderboardList.innerHTML = '<li class="placeholder">No documentation pairs with both TD and IBD are ready for the leaderboard yet.</li>';
      return;
    }
    landingLeaderboardSection?.classList.remove("is-hidden");
    landingLeaderboardList.innerHTML = ranked.map((entry) => {
      const voteCount = Number(entry.comparison_count || 0);
      const ibdPct = Math.round(Number(entry.IBD_win_percentage || 0));
      const tdPct = Math.round(Number(entry.TD_win_percentage || 0));
      return `
        <li>
          <article class="area-ranking-card">
            <div class="area-ranking-main">
              <span class="area-rank">#${entry.rank}</span>
              <div>
                <strong>${escapeHtml(entry.documentation_title || "Documentation sample")}</strong>
                <small>${voteCount ? `${voteCount} blind comparisons` : "Ready for Arena votes"}</small>
              </div>
              <span class="area-rating">${Number(entry.ibd_doc_elo_rating || 0)}</span>
            </div>
            <details class="area-documentation-menu">
              <summary>Open docs / invariants</summary>
              ${renderLeaderboardDocumentationMenu(entry)}
            </details>
            <details class="area-ranking-details">
              <summary>Show study stats</summary>
              <div class="area-stat-grid">
                <span><strong>${Number(entry.ibd_doc_elo_rating || 0)}</strong> IBD Elo</span>
                <span><strong>${Number(entry.td_doc_elo_rating || 0)}</strong> TD Elo</span>
                <span><strong>${Math.round(Number(entry.bt_ibd_win_prob || 0) * 100)}%</strong> IBD win probability</span>
                <span><strong>${voteCount}</strong> comparisons</span>
              </div>
              <div class="area-distribution" aria-label="Preference distribution">
                <div class="area-distribution-bar">
                  <span style="--share: ${ibdPct}%" title="IBD ${ibdPct}%"></span>
                  <span style="--share: ${tdPct}%" title="TD ${tdPct}%"></span>
                </div>
                <div class="area-distribution-labels">
                  <small>IBD ${ibdPct}%</small>
                  <small>TD ${tdPct}%</small>
                </div>
              </div>
              ${renderLeaderboardViz({
                ibdPct,
                tdPct,
                ibdElo: Number(entry.ibd_doc_elo_rating || 0),
                tdElo: Number(entry.td_doc_elo_rating || 0),
                voteCount
              })}
              <details class="area-comment-details">
                <summary>Show comments</summary>
                ${formatLeaderboardComments(entry)}
              </details>
            </details>
          </article>
        </li>
      `;
    }).join("");
  } catch (error) {
    landingLeaderboardSection?.classList.add("is-hidden");
    landingLeaderboardList.innerHTML = `<li class="placeholder">${escapeHtml(error.message || "Could not load leaderboard.")}</li>`;
  }
}

function renderAreaLeaderboard() {
  if (!areaLeaderboardList) return;
  const ranked = [...areaFallbackPosts].sort((a, b) => b.ibdElo - a.ibdElo);
  areaLeaderboardList.innerHTML = ranked.map((post, index) => {
    const voteCount = areaPostVoteCount(post);
    const isCurrent = post === areaFallbackPosts[activeAreaIndex];
    const ibdPct = Math.round((post.ibdWins / Math.max(voteCount, 1)) * 100);
    const tdPct = 100 - ibdPct;
    return `
      <li class="${index === 0 ? "is-leading" : ""} ${isCurrent ? "is-current" : ""}">
        <article class="area-ranking-card">
          <div class="area-ranking-main">
            <span class="area-rank">#${index + 1}</span>
            <div>
              <strong>${escapeHtml(post.label)}</strong>
              <small>${isCurrent ? "Current comparison" : "Example documentation duel"}</small>
            </div>
            <span class="area-rating">${post.ibdElo}</span>
          </div>
          <details class="area-documentation-menu">
            <summary>Open docs / invariants</summary>
            ${renderLeaderboardDocumentationMenu({
              IBD_generated_md: post.ibdDoc,
              TD_md: post.tdDoc,
              invariants: post.invariants,
              hypothesis_tests: post.hypothesis_tests
            })}
          </details>
          <details class="area-ranking-details">
            <summary>Show more stats</summary>
            <div class="area-stat-grid">
              <span><strong>${post.ibdElo}</strong> IBD Elo</span>
              <span><strong>${post.tdElo}</strong> TD Elo</span>
              <span><strong>${Math.round(post.bt * 100)}%</strong> IBD win probability</span>
              <span><strong>${voteCount}</strong> comparisons</span>
            </div>
            <div class="area-distribution" aria-label="Preference distribution">
              <div class="area-distribution-bar">
                <span style="--share: ${ibdPct}%" title="IBD ${ibdPct}%"></span>
                <span style="--share: ${tdPct}%" title="TD ${tdPct}%"></span>
              </div>
              <div class="area-distribution-labels">
                <small>IBD ${ibdPct}%</small>
                <small>TD ${tdPct}%</small>
              </div>
            </div>
          </details>
        </article>
      </li>
    `;
  }).join("");
}

function leaderboardEntryForDoc(doc) {
  return comparisonLeaderboardRows.find((entry) => String(entry.documentation_id) === String(doc.id)) || null;
}

function renderAccountRankingSummary(doc) {
  const leaderboardEntry = leaderboardEntryForDoc(doc);
  const rank = leaderboardEntry?.rank || doc.rank || doc.comparison_rank || doc.leaderboard_rank;
  const comparisonCount = Number(leaderboardEntry?.comparison_count ?? doc.comparison_count ?? doc.comparisons ?? 0);
  const ibdElo = Number(leaderboardEntry?.ibd_doc_elo_rating ?? doc.ibd_doc_elo_rating ?? doc.ibdElo ?? 0);
  const tdElo = Number(leaderboardEntry?.td_doc_elo_rating ?? doc.td_doc_elo_rating ?? doc.tdElo ?? 0);
  const ibdWins = Number(leaderboardEntry?.IBD_wins ?? doc.ibd_wins ?? doc.IBD_wins ?? 0);
  const ibdPct = comparisonCount ? Math.round((ibdWins / comparisonCount) * 100) : 0;
  const tdPct = comparisonCount ? Math.max(0, 100 - ibdPct) : 0;
  const hasStats = rank || comparisonCount || ibdElo || tdElo || ibdPct;
  if (!hasStats) {
    return `
      <section class="account-detail-section account-ranking-panel">
        <p class="eyebrow">Arena ranking</p>
        <p class="placeholder">No arena ranking yet. Once this document receives blind-comparison votes, its rank and distributions will appear here.</p>
      </section>
    `;
  }
  return `
    <section class="account-detail-section account-ranking-panel">
      <p class="eyebrow">Arena ranking</p>
      <div class="account-ranking-summary">
        <span><strong>${rank ? `#${rank}` : "—"}</strong> Rank</span>
        <span><strong>${ibdElo || "—"}</strong> Invariant-based Elo</span>
        <span><strong>${tdElo || "—"}</strong> Baseline Elo</span>
        <span><strong>${comparisonCount}</strong> Blind votes</span>
      </div>
      <div class="area-distribution" aria-label="Your document preference distribution">
        <div class="area-distribution-bar">
          <span style="--share: ${ibdPct}%" title="Invariant-based ${ibdPct}%"></span>
          <span style="--share: ${tdPct}%" title="Baseline ${tdPct}%"></span>
        </div>
        <div class="area-distribution-labels">
          <small>Invariant-based ${ibdPct}%</small>
          <small>Baseline ${tdPct}%</small>
        </div>
      </div>
      ${renderLeaderboardViz({ ibdPct, tdPct, ibdElo, tdElo, voteCount: comparisonCount })}
      <details class="area-comment-details">
        <summary>Show comments</summary>
        ${leaderboardEntry ? formatLeaderboardComments(leaderboardEntry) : '<p class="placeholder">No reviewer comments recorded yet.</p>'}
      </details>
      <details class="area-documentation-menu">
        <summary>Open docs / invariants</summary>
        ${renderLeaderboardDocumentationMenu(leaderboardEntry || doc)}
      </details>
    </section>
  `;
}

function renderAreaPost() {
  const post = currentAreaPost || areaFallbackPosts[activeAreaIndex] || areaFallbackPosts[0];
  if (!post) return;

  const candidateADocument = getAreaCandidateDocument(post, "A");
  const candidateBDocument = getAreaCandidateDocument(post, "B");
  if (areaTitle) areaTitle.textContent = "Anonymous documentation comparison";
  if (areaTdTitle) areaTdTitle.textContent = "Candidate A";
  if (areaIbdTitle) areaIbdTitle.textContent = "Candidate B";
  if (areaTdDoc) areaTdDoc.innerHTML = renderMarkdown(candidateADocument);
  if (areaIbdDoc) areaIbdDoc.innerHTML = renderMarkdown(candidateBDocument);
  if (areaVoteButton) {
    areaVoteButton.textContent = selectedAreaWinner ? `Vote for ${areaCandidateLabelForWinner(selectedAreaWinner)}` : "Select a candidate";
  }
  if (areaVoteMessage) {
    areaVoteMessage.textContent = areaVoteSubmitted
      ? "Vote recorded. Source labels and rankings stay hidden in the ranking flow."
      : "Blind study mode. Pick a candidate without seeing source labels, rankings, or statistics.";
  }
  areaChoices.forEach((choice, index) => {
    const label = index === 0 ? "A" : "B";
    choice.dataset.areaLabel = label;
    choice.dataset.areaChoice = activeAreaSides[label];
    const active = choice.dataset.areaChoice === selectedAreaWinner;
    choice.classList.toggle("is-selected", active);
    choice.setAttribute("aria-pressed", String(active));
  });
  updateAreaSessionUI();
}

function selectAreaWinner(winner) {
  const nextWinner = winner === "TD" ? "TD" : "IBD";
  selectedAreaWinner = selectedAreaWinner === nextWinner ? null : nextWinner;
  renderAreaPost();
}

async function submitAreaVote() {
  const post = currentAreaPost;
  if (!selectedAreaWinner) {
    if (areaVoteMessage) areaVoteMessage.textContent = "Select Candidate A or Candidate B before submitting.";
    return;
  }
  const rankLimit = areaRankLimitValue();
  if (rankLimit && areaRankCountValue() >= rankLimit) {
    if (areaVoteMessage) areaVoteMessage.textContent = "Ranking limit reached. Increase the limit to continue.";
    updateAreaSessionUI();
    return;
  }
  const comment = (areaCommentInput?.value || "").trim();
  const commentWords = comment.split(/\s+/).filter(Boolean).length;
  if (comment.length < 40 || commentWords < 8) {
    if (areaVoteMessage) {
      areaVoteMessage.textContent = "Please add a meaningful comment before submitting: at least 40 characters and 8 words.";
    }
    areaCommentInput?.focus();
    return;
  }
  if (!post?.id) {
    areaVoteSubmitted = true;
    incrementAreaRankCount();
    renderAreaPost();
    return;
  }
  if (areaVoteButton) areaVoteButton.disabled = true;
  if (areaVoteMessage) areaVoteMessage.textContent = "Recording blind preference...";
  try {
    const response = await fetch(apiUrl("/comparison/vote"), {
      method: "POST",
      headers: authHeaders({ "Content-Type": "application/json" }),
      body: JSON.stringify({
        documentation_id: post.id,
        winner: selectedAreaWinner,
        comments: comment
      })
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(response.status === 401 ? "Log in to submit a recorded study vote." : data.detail || "Could not record vote.");
    }
    currentAreaPost = {
      ...post,
      ibdElo: Number(data.ibd_doc_elo_rating || post.ibdElo),
      tdElo: Number(data.td_doc_elo_rating || post.tdElo),
      ibdWins: Number(data.IBD_wins || post.ibdWins),
      tdWins: Number(data.TD_wins || post.tdWins),
      ibdWinPercentage: Number(data.IBD_win_percentage || post.ibdWinPercentage),
      tdWinPercentage: Number(data.TD_win_percentage || post.tdWinPercentage),
      bt: Number(data.bt_ibd_win_prob || post.bt)
    };
    areaVoteSubmitted = true;
    incrementAreaRankCount();
    renderAreaPost();
    renderLandingLeaderboard();
  } catch (error) {
    areaVoteSubmitted = true;
    renderAreaPost();
    if (areaVoteMessage) areaVoteMessage.textContent = `${error.message || "Vote was not recorded."} Statistics are shown for review only.`;
  } finally {
    if (areaVoteButton) areaVoteButton.disabled = false;
  }
}

function showNextAreaPost() {
  activeAreaIndex = (activeAreaIndex + 1) % areaFallbackPosts.length;
  if (areaCommentInput) areaCommentInput.value = "";
  loadAreaComparison();
}

function updateAccountMenuLabel() {
  if (!accountMenuLabel) return;
  accountMenuLabel.textContent = getSavedUserEmail() || "Guest";
  if (landingAccountButton) {
    const signedIn = Boolean(getAccessToken());
    landingAccountButton.textContent = signedIn ? "Account" : "Login";
    landingAccountButton.dataset.authMode = signedIn ? "account" : "login";
  }
}

async function refreshDatabaseStatus() {
  if (!databaseStatus || !databaseStatusText) return;
  databaseStatus.dataset.state = "checking";
  databaseStatusText.textContent = "Checking database...";
  try {
    const response = await fetch(apiUrl("/api/status"));
    const data = await response.json().catch(() => ({}));
    if (!response.ok || !data.database?.connected) {
      throw new Error(data.database?.error || "Database unavailable");
    }
    const database = data.database;
    databaseStatus.dataset.state = "connected";
    databaseStatusText.textContent = `${database.backend || "database"} connected: ${database.name || "default"}`;
  } catch (error) {
    databaseStatus.dataset.state = "error";
    databaseStatusText.textContent = error.message || "Database unavailable";
  }
}

function setAuthMode(nextMode) {
  authMode = nextMode === "signup" ? "signup" : "login";
  if (authSubmitButton) authSubmitButton.textContent = authMode === "signup" ? "Create account" : "Login";
  if (authModeToggle) authModeToggle.textContent = authMode === "signup" ? "Already have an account? Login" : "Need an account? Create one";
  if (authMessage) authMessage.textContent = "";
}

function showLoginPage(nextMode = "login") {
  if (isResearchModeActive()) {
    showAreaPage();
    return;
  }
  setAuthMode(nextMode);
  landingPage?.classList.add("is-hidden");
  areaPage?.classList.add("is-hidden");
  loginPage?.classList.remove("is-hidden");
  appShell?.classList.add("is-hidden");
  accountPage?.classList.add("is-hidden");
  document.body.classList.remove("landing-active", "app-active", "account-active", "area-active");
  document.body.classList.add("auth-active");
  window.scrollTo({ top: 0, behavior: "smooth" });
  window.setTimeout(() => authEmailInput?.focus(), 120);
}

async function submitAuth(event) {
  event.preventDefault();
  if (!authEmailInput?.value.trim() || !authPasswordInput?.value) return;
  if (authMessage) authMessage.textContent = authMode === "signup" ? "Creating account..." : "Logging in...";
  if (authSubmitButton) authSubmitButton.disabled = true;
  try {
    if (authMode === "signup") {
      const createResponse = await fetch(apiUrl("/users/"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: authEmailInput.value.trim(), password: authPasswordInput.value })
      });
      if (!createResponse.ok) {
        const data = await createResponse.json().catch(() => ({}));
        throw new Error(data.detail || data.error || "Could not create account.");
      }
    }

    const credentials = new URLSearchParams();
    credentials.set("username", authEmailInput.value.trim());
    credentials.set("password", authPasswordInput.value);
    const loginResponse = await fetch(apiUrl("/login/"), {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: credentials
    });
    const data = await loginResponse.json().catch(() => ({}));
    if (!loginResponse.ok) throw new Error(data.detail || data.error || "Invalid credentials.");
    localStorage.setItem(ACCESS_TOKEN_STORAGE_KEY, data.access_token || "");
    localStorage.setItem(USER_EMAIL_STORAGE_KEY, authEmailInput.value.trim());
    if (authMessage) authMessage.textContent = "Signed in.";
    updateAccountMenuLabel();
    showAppPage();
  } catch (error) {
    if (authMessage) authMessage.textContent = error.message || "Authentication failed.";
  } finally {
    if (authSubmitButton) authSubmitButton.disabled = false;
  }
}

const MODEL_PROVIDER_META = {
  openai: {
    keyLabel: "OpenAI key",
    keyPlaceholder: "sk-...",
    markdownModel: "gpt-5.5",
    metricsModel: "gpt-5.4-mini",
    showBaseUrl: false
  },
  claude: {
    keyLabel: "Anthropic key",
    keyPlaceholder: "sk-ant-...",
    markdownModel: "claude-sonnet-4-6",
    metricsModel: "claude-sonnet-4-6",
    showBaseUrl: false
  },
  cmu_gateway: {
    keyLabel: "Gateway key",
    keyPlaceholder: "Paste gateway key",
    markdownModel: "gpt-5.5",
    metricsModel: "gpt-5.4-mini",
    showBaseUrl: true
  }
};

const DEFAULT_CMU_GATEWAY_BASE_URL = "https://ai-gateway.andrew.cmu.edu/v1";

function currentModelProvider() {
  return modelProviderInput?.value || "openai";
}

function updateModelProviderControls() {
  const meta = MODEL_PROVIDER_META[currentModelProvider()] || MODEL_PROVIDER_META.openai;
  if (apiKeyLabel) apiKeyLabel.textContent = meta.keyLabel;
  if (openaiKeyInput) openaiKeyInput.placeholder = meta.keyPlaceholder;
  if (markdownModelInput) markdownModelInput.placeholder = `Default: ${meta.markdownModel}`;
  if (metricsModelInput) metricsModelInput.placeholder = `Default: ${meta.metricsModel}`;
  modelBaseUrlField?.classList.toggle("is-hidden", !meta.showBaseUrl);
}

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
  themeToggles.forEach((toggle) => {
    toggle.setAttribute("aria-pressed", dark ? "true" : "false");
    toggle.innerHTML = `
      <span class="theme-orbit" aria-hidden="true">
        <span class="theme-sun"></span>
        <span class="theme-moon"></span>
      </span>
      <span class="theme-label">${dark ? "Light mode" : "Dark mode"}</span>
    `;
    toggle.title = dark ? "Switch to light mode" : "Switch to dark mode";
  });
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
  syncStepAvailability();
  document.body.classList.remove("stage-input", "stage-review", "stage-compare", "stage-tests", "stage-td", "stage-coverage", "stage-docs-example", "stage-generated-docs");
  document.body.classList.add(`stage-${stage}`);
  stepTabs.forEach((tab) => {
    const active = tab.dataset.step === stage;
    tab.classList.toggle("is-active", active);
    tab.setAttribute("aria-current", active ? "step" : "false");
  });
}

function syncStepAvailability() {
  const tdTab = stepTabs.find((tab) => tab.dataset.step === "td");
  if (!tdTab) return;
  const hasSavedIbd = Boolean(currentMarkdown && currentMarkdown.trim() && activeSavedDocumentation?.id);
  tdTab.classList.toggle("is-hidden", !hasSavedIbd);
  tdTab.disabled = !hasSavedIbd;
  tdTab.setAttribute("aria-disabled", String(!hasSavedIbd));
}

function markTDStepReady() {
  const tdTab = stepTabs.find((tab) => tab.dataset.step === "td");
  if (!tdTab) return;
  syncStepAvailability();
  tdTab.classList.add("td-step-ready");
  setTimeout(() => tdTab.classList.remove("td-step-ready"), 4200);
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
  tdPanel?.classList.add("is-hidden");
  coveragePanel?.classList.add("is-hidden");
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

function parseStoredInvariants(value) {
  if (!value) return [];
  if (Array.isArray(value)) return value.map(String);
  if (typeof value !== "string") return [String(value)];
  try {
    const parsed = JSON.parse(value);
    if (Array.isArray(parsed)) return parsed.map((item) => typeof item === "string" ? item : JSON.stringify(item));
    return [String(parsed)];
  } catch {
    return value.split(/\r?\n/).map((item) => item.trim()).filter(Boolean);
  }
}

function addSavedDocToSession(doc) {
  const createdAt = doc.created_at ? new Date(doc.created_at) : new Date();
  const apiName = doc.documentation_title || "Saved documentation";
  const markdown = doc.IBD_generated_md || "";
  const savedDoc = {
    id: `saved-${doc.id}`,
    apiName,
    title: apiName,
    markdown,
    invariants: parseStoredInvariants(doc.invariants),
    createdAt,
    filename: `${slugify(apiName)}-${createdAt.toISOString().slice(0, 19).replace(/[:T]/g, "-")}.md`
  };
  generatedDocs = [savedDoc, ...generatedDocs.filter((item) => item.id !== savedDoc.id)].slice(0, 12);
  activeGeneratedDocId = savedDoc.id;
  renderGeneratedDocsLibrary();
  resetGeneratedDocsInactivityTimer();
  showGeneratedDoc(savedDoc.id);
}

function renderSavedDocs() {
  if (!savedDocList) return;
  if (!getAccessToken()) {
    savedDocumentation = [];
    savedDocList.innerHTML = '<p class="placeholder">Login to view saved Markdown from previous human review runs.</p>';
    return;
  }

  const query = (savedDocSearchInput?.value || "").trim().toLowerCase();
  const filtered = savedDocumentation.filter((doc) => {
    const haystack = [
      doc.documentation_title,
      doc.IBD_generated_md,
      doc.invariants
    ].join(" ").toLowerCase();
    return !query || haystack.includes(query);
  });

  if (!filtered.length) {
    savedDocList.innerHTML = '<p class="placeholder">No saved Markdown matches this search yet.</p>';
    return;
  }

  savedDocList.innerHTML = filtered.map((doc) => {
    const createdAt = doc.created_at ? new Date(doc.created_at) : null;
    const dateLabel = createdAt && !Number.isNaN(createdAt.valueOf())
      ? createdAt.toLocaleString([], { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" })
      : "Saved Markdown";
    return `
      <button type="button" class="saved-doc-card" data-saved-doc-id="${doc.id}">
        <strong>${escapeHtml(doc.documentation_title || "Saved documentation")}</strong>
        <small>${escapeHtml(dateLabel)}</small>
      </button>
    `;
  }).join("");
}

async function fetchSavedDocs() {
  if (!getAccessToken()) {
    renderSavedDocs();
    return;
  }
  if (savedDocList) savedDocList.innerHTML = '<p class="placeholder">Loading saved Markdown...</p>';
  try {
    const response = await fetch(apiUrl("/documentation/me"), {
      headers: authHeaders({ Accept: "application/json" })
    });
    const data = await response.json().catch(() => []);
    if (!response.ok) throw new Error(data.detail || data.error || "Could not load saved Markdown.");
    savedDocumentation = Array.isArray(data) ? data : [];
    renderSavedDocs();
  } catch (error) {
    if (savedDocList) savedDocList.innerHTML = `<p class="placeholder">${escapeHtml(error.message || "Could not load saved Markdown.")}</p>`;
  }
}

// ----- Account page -----
let accountDocuments = [];
let activeAccountDoc = null;
let accountSort = "created-desc";
let accountConfirmPhrase = "";

function formatAccountDate(value) {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.valueOf())) return "—";
  return date.toLocaleString([], {
    year: "numeric", month: "short", day: "numeric", hour: "numeric", minute: "2-digit"
  });
}

function formatPercentMaybe(value) {
  const numeric = Number(value);
  if (!Number.isFinite(numeric)) return "—";
  return `${Math.round(numeric * 100)}%`;
}

function parseStoredMetrics(value) {
  if (!value) return [];
  try {
    const parsed = typeof value === "string" ? JSON.parse(value) : value;
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function averageAccountMetric(field) {
  const values = accountDocuments
    .map((doc) => Number(doc?.[field]))
    .filter((value) => Number.isFinite(value));
  if (!values.length) return null;
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

function renderAccountStats() {
  if (!accountStats) return;
  const stats = [
    ["Avg soundness", averageAccountMetric("soundness")],
    ["Avg validity", averageAccountMetric("validity")],
    ["Avg mutation", averageAccountMetric("mutation_score")]
  ];
  accountStats.innerHTML = stats.map(([label, value]) => `
    <div class="account-stat">
      <strong>${value === null ? "—" : formatPercentMaybe(value)}</strong>
      <span>${escapeHtml(label)}</span>
    </div>
  `).join("");
}

function setDeleteConfirmPhrase(email) {
  accountConfirmPhrase = (email || "").trim();
  if (deleteConfirmPhrase) deleteConfirmPhrase.textContent = accountConfirmPhrase || "your email";
  if (deleteConfirmInput) deleteConfirmInput.placeholder = accountConfirmPhrase || "";
  updateDeleteConfirmState();
}

async function fetchAccountProfile() {
  if (!getAccessToken() || !accountEmail) return;
  accountEmail.textContent = getSavedUserEmail() || "—";
  accountCreated.textContent = "—";
  accountId.textContent = "—";
  setDeleteConfirmPhrase(getSavedUserEmail());
  try {
    const response = await fetch(apiUrl("/users/me"), { headers: authHeaders({ Accept: "application/json" }) });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || data.error || "Could not load profile.");
    accountEmail.textContent = data.email || getSavedUserEmail() || "—";
    accountCreated.textContent = formatAccountDate(data.created_at);
    accountId.textContent = data.id != null ? `#${data.id}` : "—";
    setDeleteConfirmPhrase(data.email || getSavedUserEmail());
  } catch {
    // Keep the cached email even when the profile lookup fails.
  }
}

function accountDocLibrary(doc) {
  const title = (doc?.documentation_title || "").trim();
  if (!title) return "";
  // Treat the leading namespace (before the first dot/space) as the library,
  // e.g. "numpy.linspace" -> "numpy", "torch.nn.relu" -> "torch".
  const match = title.match(/^[^.\s]+/);
  return (match ? match[0] : title).toLowerCase();
}

function sortedAccountDocuments() {
  const docs = [...accountDocuments];
  const query = (accountDocsSearch?.value || "").trim().toLowerCase();
  const filteredDocs = query ? docs.filter((doc) => {
    const metrics = parseStoredMetrics(doc.hypothesis_tests);
    const haystack = [
      doc.documentation_title,
      doc.source_code,
      doc.IBD_generated_md,
      doc.invariants,
      doc.mutation_summary,
      metrics.map((metric) => [
        metric.invariant,
        metric.explanation,
        metric.test_code,
        metric.mutation_analysis,
        metric.mutation_error
      ].join(" ")).join(" ")
    ].join(" ").toLowerCase();
    return haystack.includes(query);
  }) : docs;
  const byDate = (a, b) => new Date(a.created_at || 0) - new Date(b.created_at || 0);
  const byName = (a, b) =>
    (a.documentation_title || "").localeCompare(b.documentation_title || "", undefined, { sensitivity: "base" });
  switch (accountSort) {
    case "created-asc":
      filteredDocs.sort(byDate);
      break;
    case "name-asc":
      filteredDocs.sort(byName);
      break;
    case "name-desc":
      filteredDocs.sort((a, b) => byName(b, a));
      break;
    case "library-asc":
      filteredDocs.sort((a, b) => accountDocLibrary(a).localeCompare(accountDocLibrary(b)) || byName(a, b));
      break;
    case "created-desc":
    default:
      filteredDocs.sort((a, b) => byDate(b, a));
      break;
  }
  return filteredDocs;
}

function renderAccountDocs() {
  if (!accountDocsList) return;
  if (!getAccessToken()) {
    accountDocsList.innerHTML = '<p class="placeholder">Log in to view your documents.</p>';
    return;
  }
  if (!accountDocuments.length) {
    accountDocsList.innerHTML = '<p class="placeholder">No generated documents yet. Run the generator to create one.</p>';
    return;
  }
  const visibleDocs = sortedAccountDocuments();
  if (!visibleDocs.length) {
    accountDocsList.innerHTML = '<p class="placeholder">No documents match that search.</p>';
    return;
  }
  accountDocsList.innerHTML = visibleDocs.map((doc) => {
    const invariants = parseStoredInvariants(doc.invariants);
    const comparisonCount = Number(doc.comparison_count || 0);
    const ibdWins = Number(doc.ibd_wins || 0);
    const ibdPct = comparisonCount ? Math.round((ibdWins / comparisonCount) * 100) : 0;
    return `
      <article class="account-doc-card">
        <div class="account-doc-info">
          <strong>${escapeHtml(doc.documentation_title || "Untitled documentation")}</strong>
          <small>${escapeHtml(formatAccountDate(doc.created_at))}</small>
          <div class="account-doc-pills">
            <span>Soundness ${formatPercentMaybe(doc.soundness)}</span>
            <span>Validity ${formatPercentMaybe(doc.validity)}</span>
            <span>Mutation ${formatPercentMaybe(doc.mutation_score)}</span>
            <span>${invariants.length} invariants</span>
            <span>${comparisonCount} arena votes</span>
            ${comparisonCount ? `<span>${ibdPct}% invariant-based preference</span>` : ""}
          </div>
        </div>
        <div class="account-doc-actions">
          <button type="button" class="secondary-button account-doc-view" data-doc-id="${doc.id}">View more</button>
          <button type="button" class="danger-button account-doc-delete" data-doc-id="${doc.id}">Delete</button>
        </div>
      </article>
    `;
  }).join("");
}

async function fetchAccountDocs() {
  if (!getAccessToken()) {
    renderAccountDocs();
    return;
  }
  if (accountDocsList) accountDocsList.innerHTML = '<p class="placeholder">Loading your documents…</p>';
  try {
    const response = await fetch(apiUrl("/documentation/me"), { headers: authHeaders({ Accept: "application/json" }) });
    const data = await response.json().catch(() => []);
    if (!response.ok) throw new Error(data.detail || data.error || "Could not load documents.");
    accountDocuments = Array.isArray(data) ? data : [];
    await fetchComparisonLeaderboard().catch(() => []);
    if (accountDocCount) accountDocCount.textContent = String(accountDocuments.length);
    renderAccountStats();
    renderAccountDocs();
  } catch (error) {
    if (accountDocsList) accountDocsList.innerHTML = `<p class="placeholder">${escapeHtml(error.message || "Could not load documents.")}</p>`;
  }
}

function showAccountDocDetail(docId) {
  const doc = accountDocuments.find((item) => String(item.id) === String(docId));
  if (!doc || !accountDetailModal) return;
  activeAccountDoc = doc;
  const invariants = parseStoredInvariants(doc.invariants);
  const metrics = parseStoredMetrics(doc.hypothesis_tests);
  accountDetailTitle.textContent = doc.documentation_title || "Document";
  accountDetailEyebrow.textContent = `Generated ${formatAccountDate(doc.created_at)}`;
  accountDetailBody.innerHTML = `
    <section class="account-detail-section">
      <p class="eyebrow">Overview</p>
      <dl class="account-detail-meta">
        <div><dt>Name</dt><dd>${escapeHtml(doc.documentation_title || "—")}</dd></div>
        <div><dt>Generated</dt><dd>${escapeHtml(formatAccountDate(doc.created_at))}</dd></div>
        <div><dt>Soundness</dt><dd>${formatPercentMaybe(doc.soundness)}</dd></div>
        <div><dt>Validity</dt><dd>${formatPercentMaybe(doc.validity)}</dd></div>
        <div><dt>Mutation</dt><dd>${formatPercentMaybe(doc.mutation_score)}</dd></div>
      </dl>
    </section>
    ${invariants.length ? `
      <section class="account-detail-section">
        <p class="eyebrow">Invariants (${invariants.length})</p>
        <ul class="account-detail-invariants">${invariants.map((inv) => `<li>${escapeHtml(inv)}</li>`).join("")}</ul>
      </section>
    ` : ""}
    ${metrics.length ? `
      <section class="account-detail-section">
        <p class="eyebrow">Metrics &amp; tests (${metrics.length})</p>
        <div class="account-detail-metrics">
          ${metrics.map((metric, index) => `
            <details class="account-metric">
              <summary>
                <span>Invariant ${index + 1}</span>
                <span class="account-metric-pills">
                  <span>Valid ${formatPercentMaybe(metric.validity)}</span>
                  <span>Sound ${formatPercentMaybe(metric.soundness)}</span>
                  ${metric.mutation_score === null || metric.mutation_score === undefined ? "" : `<span>Mut ${formatPercentMaybe(metric.mutation_score)}</span>`}
                </span>
              </summary>
              ${metric.invariant ? `<div class="markdown-rendered">${renderMarkdown(String(metric.invariant))}</div>` : ""}
              ${metric.test_code ? `<pre class="md-code"><code>${escapeHtml(metric.test_code)}</code></pre>` : ""}
            </details>
          `).join("")}
        </div>
      </section>
    ` : ""}
    ${renderAccountRankingSummary(doc)}
    <section class="account-detail-section">
      <div class="account-detail-md-head">
        <p class="eyebrow">Generated Markdown</p>
        <div class="account-detail-md-actions">
          <button type="button" class="secondary-button" id="account-md-download">Download .md</button>
          <button type="button" class="secondary-button" id="account-md-edit">Edit</button>
          <button type="button" class="danger-button" id="account-md-delete">Delete</button>
        </div>
      </div>
      <p class="account-message" id="account-md-message"></p>
      <div class="markdown-rendered account-detail-markdown" id="account-detail-markdown">${doc.IBD_generated_md ? renderMarkdown(doc.IBD_generated_md) : '<p class="placeholder">No Markdown stored.</p>'}</div>
      <div class="account-detail-md-editor is-hidden" id="account-detail-md-editor">
        <textarea id="account-md-textarea" rows="16" spellcheck="false"></textarea>
        <div class="account-detail-md-editor-actions">
          <button type="button" class="landing-primary-button" id="account-md-save">Save changes</button>
          <button type="button" class="secondary-button" id="account-md-cancel">Cancel</button>
        </div>
      </div>
    </section>
  `;
  accountDetailModal.classList.remove("is-hidden");
  document.body.classList.add("account-detail-open");
  accountDetailClose?.focus();
}

async function deleteAccountDocument(docId) {
  const doc = accountDocuments.find((item) => String(item.id) === String(docId));
  if (!doc) return;
  const title = doc.documentation_title || "this document";
  if (!window.confirm(`Delete ${title}? This removes the saved Markdown, invariants, and metrics.`)) return;
  const response = await fetch(apiUrl(`/documentation/delete/${doc.id}`), {
    method: "DELETE",
    headers: authHeaders({ Accept: "application/json" })
  });
  if (!response.ok && response.status !== 204) {
    const data = await response.json().catch(() => ({}));
    throw new Error(data.detail || data.error || "Could not delete document.");
  }
  accountDocuments = accountDocuments.filter((item) => String(item.id) !== String(doc.id));
  savedDocumentation = savedDocumentation.filter((item) => String(item.id) !== String(doc.id));
  if (activeAccountDoc && String(activeAccountDoc.id) === String(doc.id)) {
    closeAccountDocDetail();
  }
  if (accountDocCount) accountDocCount.textContent = String(accountDocuments.length);
  renderAccountStats();
  renderAccountDocs();
  renderSavedDocs();
}

function closeAccountDocDetail() {
  accountDetailModal?.classList.add("is-hidden");
  document.body.classList.remove("account-detail-open");
  activeAccountDoc = null;
}

function setAccountMarkdownEditing(editing) {
  const rendered = accountDetailBody?.querySelector("#account-detail-markdown");
  const editor = accountDetailBody?.querySelector("#account-detail-md-editor");
  const textarea = accountDetailBody?.querySelector("#account-md-textarea");
  const editButton = accountDetailBody?.querySelector("#account-md-edit");
  const message = accountDetailBody?.querySelector("#account-md-message");
  if (!rendered || !editor) return;
  if (message) {
    message.textContent = "";
    message.classList.remove("is-success");
  }
  if (editing) {
    if (textarea && activeAccountDoc) textarea.value = activeAccountDoc.IBD_generated_md || "";
    rendered.classList.add("is-hidden");
    editor.classList.remove("is-hidden");
    editButton?.classList.add("is-hidden");
    textarea?.focus();
  } else {
    rendered.classList.remove("is-hidden");
    editor.classList.add("is-hidden");
    editButton?.classList.remove("is-hidden");
  }
}

function downloadActiveAccountMarkdown() {
  if (!activeAccountDoc) return;
  const filename = `${slugify(activeAccountDoc.documentation_title || "documentation")}.md`;
  downloadMarkdown(activeAccountDoc.IBD_generated_md || "", filename);
}

async function saveAccountMarkdown(button) {
  if (!activeAccountDoc) return;
  const textarea = accountDetailBody?.querySelector("#account-md-textarea");
  const message = accountDetailBody?.querySelector("#account-md-message");
  const rendered = accountDetailBody?.querySelector("#account-detail-markdown");
  const newMarkdown = textarea ? textarea.value : "";
  button.disabled = true;
  if (message) {
    message.classList.remove("is-success");
    message.textContent = "Saving changes...";
  }
  try {
    const payload = {
      documentation_title: activeAccountDoc.documentation_title || "api.function",
      source_code: activeAccountDoc.source_code || "",
      IBD_generated_md: newMarkdown,
      TD_md: activeAccountDoc.TD_md || "",
      invariants: activeAccountDoc.invariants ?? null,
      soundness: activeAccountDoc.soundness ?? null,
      validity: activeAccountDoc.validity ?? null,
      mutation_score: activeAccountDoc.mutation_score ?? null,
      mutation_summary: activeAccountDoc.mutation_summary ?? null,
      hypothesis_tests: activeAccountDoc.hypothesis_tests ?? null
    };
    const response = await fetch(apiUrl(`/documentation/update_ibd/${activeAccountDoc.id}`), {
      method: "PUT",
      headers: authHeaders({ "Content-Type": "application/json", Accept: "application/json" }),
      body: JSON.stringify(payload)
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || data.error || "Could not save changes.");
    activeAccountDoc.IBD_generated_md = newMarkdown;
    const index = accountDocuments.findIndex((item) => String(item.id) === String(activeAccountDoc.id));
    if (index >= 0) accountDocuments[index] = { ...accountDocuments[index], IBD_generated_md: newMarkdown };
    if (rendered) {
      rendered.innerHTML = newMarkdown ? renderMarkdown(newMarkdown) : '<p class="placeholder">No Markdown stored.</p>';
    }
    setAccountMarkdownEditing(false);
    if (message) {
      message.textContent = "Changes saved.";
      message.classList.add("is-success");
    }
  } catch (error) {
    if (message) message.textContent = error.message || "Could not save changes.";
  } finally {
    button.disabled = false;
  }
}

function showAccountPage() {
  if (isResearchModeActive()) {
    showAreaPage();
    return;
  }
  if (!getAccessToken()) {
    showLoginPage("login");
    return;
  }
  landingPage?.classList.add("is-hidden");
  loginPage?.classList.add("is-hidden");
  areaPage?.classList.add("is-hidden");
  appShell?.classList.add("is-hidden");
  accountPage?.classList.remove("is-hidden");
  document.body.classList.remove("landing-active", "auth-active", "app-active", "area-active");
  document.body.classList.add("account-active");
  accountMenu?.classList.add("is-hidden");
  accountMenuButton?.setAttribute("aria-expanded", "false");
  if (passwordMessage) {
    passwordMessage.textContent = "";
    passwordMessage.classList.remove("is-success");
  }
  hideDeleteConfirm();
  passwordForm?.reset();
  if (accountDocsSort) accountDocsSort.value = accountSort;
  window.scrollTo({ top: 0, behavior: "smooth" });
  fetchAccountProfile();
  fetchAccountDocs();
}

async function submitPasswordChange(event) {
  event.preventDefault();
  if (!passwordMessage) return;
  passwordMessage.classList.remove("is-success");
  const current = currentPasswordInput.value;
  const next = newPasswordInput.value;
  const confirmValue = confirmPasswordInput.value;
  if (!current || !next) {
    passwordMessage.textContent = "Fill in every password field.";
    return;
  }
  if (next !== confirmValue) {
    passwordMessage.textContent = "New passwords do not match.";
    return;
  }
  passwordSubmit.disabled = true;
  passwordMessage.textContent = "Updating password...";
  try {
    const response = await fetch(apiUrl("/users/me/password"), {
      method: "PUT",
      headers: authHeaders({ "Content-Type": "application/json", Accept: "application/json" }),
      body: JSON.stringify({ current_password: current, new_password: next })
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || data.error || "Could not update password.");
    passwordMessage.textContent = "Password updated.";
    passwordMessage.classList.add("is-success");
    passwordForm.reset();
  } catch (error) {
    passwordMessage.textContent = error.message || "Could not update password.";
  } finally {
    passwordSubmit.disabled = false;
  }
}

function deleteConfirmMatches() {
  const typed = (deleteConfirmInput?.value || "").trim().toLowerCase();
  const target = (accountConfirmPhrase || "").trim().toLowerCase();
  return Boolean(target) && typed === target;
}

function updateDeleteConfirmState() {
  if (deleteConfirmButton) deleteConfirmButton.disabled = !deleteConfirmMatches();
}

function revealDeleteConfirm() {
  if (!accountDeleteConfirm) return;
  accountDeleteConfirm.classList.remove("is-hidden");
  deleteAccountButton?.classList.add("is-hidden");
  if (deleteMessage) deleteMessage.textContent = "";
  if (deleteConfirmInput) deleteConfirmInput.value = "";
  updateDeleteConfirmState();
  deleteConfirmInput?.focus();
}

function hideDeleteConfirm() {
  accountDeleteConfirm?.classList.add("is-hidden");
  deleteAccountButton?.classList.remove("is-hidden");
  if (deleteConfirmInput) deleteConfirmInput.value = "";
  if (deleteMessage) deleteMessage.textContent = "";
  updateDeleteConfirmState();
}

async function deleteAccount() {
  if (!deleteMessage) return;
  if (!deleteConfirmMatches()) {
    deleteMessage.textContent = "Type your email exactly to confirm deletion.";
    return;
  }
  if (deleteConfirmButton) deleteConfirmButton.disabled = true;
  deleteMessage.textContent = "Deleting account...";
  try {
    const response = await fetch(apiUrl("/users/me"), {
      method: "DELETE",
      headers: authHeaders({ Accept: "application/json" })
    });
    if (!response.ok && response.status !== 204) {
      const data = await response.json().catch(() => ({}));
      throw new Error(data.detail || data.error || "Could not delete account.");
    }
    localStorage.removeItem(ACCESS_TOKEN_STORAGE_KEY);
    localStorage.removeItem(USER_EMAIL_STORAGE_KEY);
    savedDocumentation = [];
    accountDocuments = [];
    updateAccountMenuLabel();
    renderSavedDocs();
    closeAccountDocDetail();
    hideDeleteConfirm();
    showLandingPage();
  } catch (error) {
    deleteMessage.textContent = error.message || "Could not delete account.";
    updateDeleteConfirmState();
  }
}

function averageMetric(field) {
  const values = currentMetrics
    .map((metric) => Number(metric?.[field]))
    .filter((value) => Number.isFinite(value));
  if (!values.length) return null;
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

async function saveCompletedDocumentation(acceptedInvariants) {
  const token = getAccessToken();
  if (!token || !currentMarkdown.trim()) return null;
  const payload = {
    documentation_title: apiNameInput.value.trim() || "api.function",
    source_code: currentSource || documentationInput.value.trim(),
    IBD_generated_md: currentMarkdown,
    TD_md: "",
    invariants: JSON.stringify(acceptedInvariants),
    soundness: averageMetric("soundness"),
    validity: averageMetric("validity"),
    mutation_score: averageMetric("mutation_score"),
    mutation_summary: "",
    hypothesis_tests: currentMetrics.length ? JSON.stringify(currentMetrics) : null
  };

  // The streaming route cannot easily return a saved row id, so logged-in users
  // get a second authenticated save once the human-reviewed Markdown is complete.
  const response = await fetch(apiUrl("/documentation/create_ibd"), {
    method: "POST",
    headers: authHeaders({ "Content-Type": "application/json", Accept: "application/json" }),
    body: JSON.stringify(payload)
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.detail || data.error || "Could not save generated Markdown.");
  activeSavedDocumentation = data;
  savedDocumentation = [data, ...savedDocumentation.filter((doc) => doc.id !== data.id)];
  renderSavedDocs();
  return data;
}

async function formatTraditionalMarkdown() {
  const raw = (tdSourceInput?.value || "").trim();
  if (!raw) {
    if (tdMessage) tdMessage.textContent = "Paste original/reference documentation first.";
    tdSourceInput?.focus();
    return;
  }
  if (tdFormatButton) {
    tdFormatButton.disabled = true;
    tdFormatButton.textContent = "Formatting...";
  }
  if (tdMessage) tdMessage.textContent = "Calling GPT to format TD Markdown...";
  try {
    const data = await postJson("/api/td-markdown", {
      api_name: apiNameInput.value.trim() || activeSavedDocumentation?.documentation_title || "api.function",
      source_code: currentSource || documentationInput.value.trim(),
      td_text: raw,
      openai_key: openaiKeyInput?.value.trim() || "",
      model_provider: modelProviderInput?.value || "openai",
      markdown_model: markdownModelInput?.value.trim() || "",
      base_url: modelBaseUrlInput?.value.trim() || "",
      seed: Number(openaiSeedInput?.value || 42)
    }, { cache: false });
    const markdown = data.markdown || raw;
    if (tdSourceInput) tdSourceInput.value = markdown;
    if (tdPreview) tdPreview.innerHTML = renderMarkdown(markdown);
    if (tdMessage) tdMessage.textContent = "Formatted. Review the preview, then save.";
  } catch (error) {
    if (tdMessage) tdMessage.textContent = error.message || "Could not format TD Markdown.";
  } finally {
    if (tdFormatButton) {
      tdFormatButton.disabled = false;
      tdFormatButton.textContent = "Format TD with GPT";
    }
  }
}

async function saveTraditionalMarkdown() {
  const markdown = (tdSourceInput?.value || "").trim();
  if (!markdown) {
    if (tdMessage) tdMessage.textContent = "Paste or format TD Markdown before saving.";
    return;
  }
  if (!activeSavedDocumentation?.id) {
    if (tdMessage) tdMessage.textContent = "Generate and save IBD Markdown first, then save TD to that row.";
    return;
  }
  if (tdSaveButton) {
    tdSaveButton.disabled = true;
    tdSaveButton.textContent = "Saving...";
  }
  if (tdMessage) tdMessage.textContent = "Saving TD Markdown...";
  try {
    const response = await fetch(apiUrl(`/documentation/${activeSavedDocumentation.id}/td`), {
      method: "PUT",
      headers: authHeaders({ "Content-Type": "application/json", Accept: "application/json" }),
      body: JSON.stringify({ TD_md: markdown })
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || data.error || "Could not save TD Markdown.");
    activeSavedDocumentation = data;
    savedDocumentation = [data, ...savedDocumentation.filter((doc) => doc.id !== data.id)];
    renderSavedDocs();
    if (tdPreview) tdPreview.innerHTML = renderMarkdown(markdown);
    if (tdMessage) tdMessage.textContent = "TD Markdown saved. This document can now enter Arena comparisons.";
    await renderLandingLeaderboard();
  } catch (error) {
    if (tdMessage) tdMessage.textContent = error.message || "Could not save TD Markdown.";
  } finally {
    if (tdSaveButton) {
      tdSaveButton.disabled = false;
      tdSaveButton.textContent = "Save TD Markdown";
    }
  }
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
  const response = await fetch(apiUrl(path), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      ...payload,
      model_provider: currentModelProvider(),
      model_api_key: openaiKeyInput.value.trim(),
      base_url: modelBaseUrlInput?.value.trim() || (currentModelProvider() === "cmu_gateway" ? DEFAULT_CMU_GATEWAY_BASE_URL : ""),
      markdown_model: markdownModelInput?.value.trim() || "",
      metrics_model: metricsModelInput?.value.trim() || "",
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
  const response = await fetch(apiUrl(path), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      ...payload,
      model_provider: currentModelProvider(),
      model_api_key: openaiKeyInput.value.trim(),
      base_url: modelBaseUrlInput?.value.trim() || (currentModelProvider() === "cmu_gateway" ? DEFAULT_CMU_GATEWAY_BASE_URL : ""),
      markdown_model: markdownModelInput?.value.trim() || "",
      metrics_model: metricsModelInput?.value.trim() || "",
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
  tdPanel?.classList.add("is-hidden");
  coveragePanel?.classList.add("is-hidden");
  docsExamplePanel.classList.add("is-hidden");
  generatedDocsPanel.classList.add("is-hidden");
  backReviewButton.classList.add("is-hidden");
  outputEyebrow.textContent = "Review invariants";
  outputTitle.textContent = "Check the claims";
  setStage("input");
  syncMarkdownActions();
}

runCoverageButton?.addEventListener("click", () => {
  assessCoverage();
});

coverageDocStatements?.addEventListener("mouseover", (event) => {
  const card = event.target.closest(".coverage-doc-statement");
  if (!card) return;
  highlightCoverageEntry(Number(card.dataset.coverageIndex), { scrollSource: true });
});

coverageDocStatements?.addEventListener("mouseout", (event) => {
  const next = event.relatedTarget;
  if (next?.closest?.(".coverage-doc-statement")) return;
  clearCoverageHighlights();
});

coverageRenderedDocs?.addEventListener("mouseover", (event) => {
  const span = event.target.closest(".coverage-doc-highlight, .coverage-doc-highlight-block");
  if (!span) return;
  highlightCoverageEntry(Number(span.dataset.coverageIndex), { scrollSource: true });
});

coverageRenderedDocs?.addEventListener("mouseout", (event) => {
  const next = event.relatedTarget;
  if (next?.closest?.(".coverage-doc-highlight, .coverage-doc-highlight-block")) return;
  clearCoverageHighlights();
});

coverageSourceLines?.addEventListener("mouseover", (event) => {
  const line = event.target.closest(".coverage-source-line");
  if (!line) return;
  const index = coverageEntryIndexForLine(Number(line.dataset.line));
  if (index < 0) return;
  highlightCoverageEntry(index, { scrollDoc: true });
});

coverageSourceLines?.addEventListener("mouseout", (event) => {
  const next = event.relatedTarget;
  if (next?.closest?.(".coverage-source-line")) return;
  clearCoverageHighlights();
});

function bindCoverageHoverSurface(docStatementsRoot, renderedDocsRoot, sourceLinesRoot) {
  docStatementsRoot?.addEventListener("mouseover", (event) => {
    const card = event.target.closest(".coverage-doc-statement");
    if (!card) return;
    highlightCoverageEntry(Number(card.dataset.coverageIndex), { scrollSource: true });
  });
  docStatementsRoot?.addEventListener("mouseout", (event) => {
    const next = event.relatedTarget;
    if (next?.closest?.(".coverage-doc-statement")) return;
    clearCoverageHighlights();
  });
  renderedDocsRoot?.addEventListener("mouseover", (event) => {
    const span = event.target.closest(".coverage-doc-highlight, .coverage-doc-highlight-block");
    if (!span) return;
    highlightCoverageEntry(Number(span.dataset.coverageIndex), { scrollSource: true });
  });
  renderedDocsRoot?.addEventListener("mouseout", (event) => {
    const next = event.relatedTarget;
    if (next?.closest?.(".coverage-doc-highlight, .coverage-doc-highlight-block")) return;
    clearCoverageHighlights();
  });
  sourceLinesRoot?.addEventListener("mouseover", (event) => {
    const line = event.target.closest(".coverage-source-line");
    if (!line) return;
    const index = coverageEntryIndexForLine(Number(line.dataset.line));
    if (index < 0) return;
    highlightCoverageEntry(index, { scrollDoc: true });
  });
  sourceLinesRoot?.addEventListener("mouseout", (event) => {
    const next = event.relatedTarget;
    if (next?.closest?.(".coverage-source-line")) return;
    clearCoverageHighlights();
  });
}

bindCoverageHoverSurface(coverageFullscreenDocStatements, coverageFullscreenRenderedDocs, coverageFullscreenSourceLines);

function openCoverageFullscreen() {
  if (!currentCoverageData) return;
  renderCoverageModalContent(currentCoverageData);
  coverageFullscreenModal?.classList.remove("is-hidden");
  document.body.classList.add("coverage-fullscreen-open");
  coverageFullscreenClose?.focus();
}

function closeCoverageFullscreen() {
  coverageFullscreenModal?.classList.add("is-hidden");
  document.body.classList.remove("coverage-fullscreen-open");
  clearCoverageHighlights();
  coverageFullscreenButton?.focus();
}

coverageFullscreenButton?.addEventListener("click", openCoverageFullscreen);
coverageFullscreenClose?.addEventListener("click", closeCoverageFullscreen);
coverageFullscreenModal?.addEventListener("click", (event) => {
  if (event.target?.matches?.("[data-close-coverage-fullscreen]")) closeCoverageFullscreen();
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !coverageFullscreenModal?.classList.contains("is-hidden")) closeCoverageFullscreen();
});

function showReviewStage() {
  if (!currentInvariants.length) {
    showInputStage();
    return;
  }
  reviewPanel.classList.remove("is-hidden");
  comparePanel.classList.add("is-hidden");
  testsPanel.classList.add("is-hidden");
  tdPanel?.classList.add("is-hidden");
  coveragePanel?.classList.add("is-hidden");
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
  tdPanel?.classList.add("is-hidden");
  coveragePanel?.classList.add("is-hidden");
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
  coveragePanel?.classList.add("is-hidden");
  testsPanel.classList.remove("is-hidden");
  tdPanel?.classList.add("is-hidden");
  docsExamplePanel.classList.add("is-hidden");
  generatedDocsPanel.classList.add("is-hidden");
  backReviewButton.classList.remove("is-hidden");
  outputEyebrow.textContent = "Generated PBT";
  outputTitle.textContent = "Property tests";
  setStage("tests");
  setStatus("ready", "Tests ready");
  syncMarkdownActions();
}

function showTDStage() {
  if (!currentMarkdown || !activeSavedDocumentation?.id) {
    showCompareStage();
    if (tdMessage) tdMessage.textContent = "Generate and save IBD Markdown first, then add TD.";
    return;
  }
  syncStepAvailability();
  reviewPanel.classList.add("is-hidden");
  comparePanel.classList.add("is-hidden");
  testsPanel.classList.add("is-hidden");
  coveragePanel?.classList.add("is-hidden");
  docsExamplePanel.classList.add("is-hidden");
  generatedDocsPanel.classList.add("is-hidden");
  tdPanel?.classList.remove("is-hidden");
  backReviewButton.classList.remove("is-hidden");
  outputEyebrow.textContent = "Original TD";
  outputTitle.textContent = "Traditional documentation";
  setStage("td");
  setStatus("review", "TD needed");
  if (tdPreview && !tdPreview.innerHTML.trim()) {
    tdPreview.innerHTML = '<p class="placeholder">Formatted TD Markdown preview will appear here.</p>';
  }
}


function fillCoverageDocsFromCurrent(force = false) {
  if (!coverageDocsInput) return;
  if ((force || !coverageDocsInput.value.trim()) && currentMarkdown.trim()) {
    coverageDocsInput.value = currentMarkdown;
  }
}

function showCoverageStage() {
  fillCoverageDocsFromCurrent(false);
  reviewPanel.classList.add("is-hidden");
  comparePanel.classList.add("is-hidden");
  testsPanel.classList.add("is-hidden");
  tdPanel?.classList.add("is-hidden");
  coveragePanel?.classList.add("is-hidden");
  docsExamplePanel.classList.add("is-hidden");
  generatedDocsPanel.classList.add("is-hidden");
  coveragePanel.classList.remove("is-hidden");
  backReviewButton.classList.add("is-hidden");
  outputEyebrow.textContent = "Assess documentation coverage";
  outputTitle.textContent = "Map docs to source";
  setStage("coverage");
  setStatus("review", "Coverage ready");
  syncMarkdownActions();
}

function coverageEntryLineSet(entry) {
  return new Set((entry?.covered_lines || []).map((line) => Number(line)));
}

function coverageEntryIndexForLine(lineNumber) {
  const target = Number(lineNumber);
  if (!Number.isFinite(target)) return -1;
  return (currentCoverageData?.entries || []).findIndex((entry) => coverageEntryLineSet(entry).has(target));
}

function coverageDocStatementRoots() {
  return [coverageFullscreenDocStatements].filter(Boolean);
}

function coverageRenderedDocRoots() {
  return [coverageFullscreenRenderedDocs].filter(Boolean);
}

function coverageSourceRoots() {
  return [coverageFullscreenSourceLines].filter(Boolean);
}

function activeCoverageRootPair() {
  if (!coverageFullscreenModal?.classList.contains("is-hidden")) {
    return {
      docs: coverageFullscreenRenderedDocs,
      statements: coverageFullscreenDocStatements,
      source: coverageFullscreenSourceLines
    };
  }
  return { docs: coverageFullscreenRenderedDocs, statements: coverageFullscreenDocStatements, source: coverageFullscreenSourceLines };
}

function scrollCoverageDocToEntry(index) {
  const roots = activeCoverageRootPair();
  const target = roots.docs?.querySelector(`.coverage-doc-highlight-block[data-coverage-index="${index}"], .coverage-doc-highlight[data-coverage-index="${index}"]`)
    || roots.statements?.querySelector(`.coverage-doc-statement[data-coverage-index="${index}"]`);
  target?.scrollIntoView({ block: "center", behavior: "smooth" });
}

function scrollCoverageSourceToEntry(index) {
  const entry = currentCoverageData?.entries?.[index];
  const firstLine = entry?.covered_lines?.[0];
  if (!firstLine) return;
  activeCoverageRootPair().source
    ?.querySelector(`.coverage-source-line[data-line="${Number(firstLine)}"]`)
    ?.scrollIntoView({ block: "center", behavior: "smooth" });
}

function highlightCoverageEntry(index, options = {}) {
  const entry = currentCoverageData?.entries?.[index];
  if (!entry) return;
  const lines = coverageEntryLineSet(entry);
  coverageDocStatementRoots().forEach((root) => root.querySelectorAll(".coverage-doc-statement").forEach((node) => {
    node.classList.toggle("is-active", Number(node.dataset.coverageIndex) === index);
  }));
  coverageRenderedDocRoots().forEach((root) => root.querySelectorAll(".coverage-doc-highlight, .coverage-doc-highlight-block").forEach((node) => {
    node.classList.toggle("is-active", Number(node.dataset.coverageIndex) === index);
  }));
  coverageSourceRoots().forEach((root) => root.querySelectorAll(".coverage-source-line").forEach((node) => {
    const active = lines.has(Number(node.dataset.line));
    node.classList.toggle("is-active", active);
  }));
  if (options.scrollDoc) scrollCoverageDocToEntry(index);
  if (options.scrollSource) scrollCoverageSourceToEntry(index);
}

function clearCoverageHighlights() {
  coverageDocStatementRoots().forEach((root) => root.querySelectorAll(".coverage-doc-statement.is-active").forEach((node) => node.classList.remove("is-active")));
  coverageRenderedDocRoots().forEach((root) => root.querySelectorAll(".coverage-doc-highlight.is-active, .coverage-doc-highlight-block.is-active").forEach((node) => node.classList.remove("is-active")));
  coverageSourceRoots().forEach((root) => root.querySelectorAll(".coverage-source-line.is-active").forEach((node) => node.classList.remove("is-active")));
}

function renderCoverageSourceLines(data) {
  const covered = new Set(data.covered_lines || []);
  const coverable = new Set(data.coverable_lines || []);
  return (data.source_lines || []).map((line) => {
    const classes = ["coverage-source-line"];
    if (line.blank) classes.push("is-blank");
    if (covered.has(line.line)) classes.push("is-covered");
    if (coverable.has(line.line) && !covered.has(line.line)) classes.push("is-uncovered-coverable");
    return `<span class="${classes.join(" ")}" data-line="${line.line}"><span class="coverage-line-number">${line.line}</span><code>${escapeHtml(line.text || " ")}</code></span>`;
  }).join("");
}

function renderCoverageStatements(data) {
  const entries = data.entries || [];
  if (!entries.length) {
    return `<p class="placeholder">No documentation statements were mapped to source lines.</p>`;
  }
  return entries.map((entry, index) => {
    const lineText = entry.covered_lines?.length ? `Lines ${entry.covered_lines.join(", ")}` : "Unsupported by source";
    return `
      <button type="button" class="coverage-doc-statement confidence-${String(entry.confidence || "medium").toLowerCase()}" data-coverage-index="${index}">
        <span class="coverage-confidence">${escapeHtml(entry.confidence || "MEDIUM")}</span>
        <span class="coverage-lines-chip">${escapeHtml(lineText)}</span>
        <span class="coverage-statement-text">${escapeHtml(entry.statement || "Untitled documentation statement")}</span>
      </button>
    `;
  }).join("");
}

function coverageStatementPattern(statement) {
  const cleaned = `${statement || ""}`.replace(/\s+/g, " ").trim();
  if (!cleaned || cleaned.length < 16) return null;
  const fragment = cleaned
    .slice(0, Math.min(cleaned.length, 96))
    .replace(/[.*+?^${}()|[\]\\]/g, "\\$&")
    .replace(/\s+/g, "\\s+");
  try {
    return new RegExp(fragment, "i");
  } catch {
    return null;
  }
}

function markCoverageMarkdown(markdown, entries) {
  return `${markdown || ""}`;
}

function normalizedCoverageText(value) {
  return `${value || ""}`.replace(/\s+/g, " ").trim().toLowerCase();
}

function coverageStatementNeedle(statement) {
  const cleaned = normalizedCoverageText(statement);
  if (!cleaned || cleaned.length < 16) return "";
  return cleaned.slice(0, Math.min(cleaned.length, 82));
}

function decorateCoverageMarkdown(entries) {
  const blocks = [...coverageRenderedDocs.querySelectorAll("p, li, tr, blockquote")];
  const claimed = new Set();
  (entries || []).forEach((entry, index) => {
    if (!entry.covered_lines?.length) return;
    const needle = coverageStatementNeedle(entry.statement);
    if (!needle) return;
    const block = blocks.find((candidate) => {
      if (claimed.has(candidate)) return false;
      const text = normalizedCoverageText(candidate.textContent);
      return text.includes(needle) || needle.includes(text.slice(0, Math.min(text.length, 64)));
    });
    if (!block) return;
    claimed.add(block);
    block.classList.add("coverage-doc-highlight-block", `confidence-${String(entry.confidence || "medium").toLowerCase()}`);
    block.dataset.coverageIndex = String(index);
    block.dataset.coverageLines = `Lines ${entry.covered_lines.join(", ")}`;
    block.title = `Covered source: lines ${entry.covered_lines.join(", ")}`;
    block.tabIndex = 0;
  });
}

function renderCoverageMarkdown(markdown, entries) {
  return renderMarkdown(markdown);
}

function decorateCoverageMarkdownRoot(root, entries) {
  const originalRoot = coverageRenderedDocs;
  if (root === coverageRenderedDocs) {
    decorateCoverageMarkdown(entries);
    return;
  }
  const blocks = [...root.querySelectorAll("p, li, tr, blockquote")];
  const claimed = new Set();
  (entries || []).forEach((entry, index) => {
    if (!entry.covered_lines?.length) return;
    const needle = coverageStatementNeedle(entry.statement);
    if (!needle) return;
    const block = blocks.find((candidate) => {
      if (claimed.has(candidate)) return false;
      const text = normalizedCoverageText(candidate.textContent);
      return text.includes(needle) || needle.includes(text.slice(0, Math.min(text.length, 64)));
    });
    if (!block) return;
    claimed.add(block);
    block.classList.add("coverage-doc-highlight-block", `confidence-${String(entry.confidence || "medium").toLowerCase()}`);
    block.dataset.coverageIndex = String(index);
    block.dataset.coverageLines = `Lines ${entry.covered_lines.join(", ")}`;
    block.title = `Covered source: lines ${entry.covered_lines.join(", ")}`;
    block.tabIndex = 0;
  });
}

function renderCoverageModalContent(data) {
  if (!coverageFullscreenSourceLines || !coverageFullscreenRenderedDocs || !coverageFullscreenDocStatements) return;
  coverageFullscreenRenderedDocs.innerHTML = renderCoverageMarkdown(coverageDocsInput.value, data.entries || []);
  decorateCoverageMarkdownRoot(coverageFullscreenRenderedDocs, data.entries || []);
  coverageFullscreenSourceLines.innerHTML = renderCoverageSourceLines(data);
  coverageFullscreenDocStatements.innerHTML = renderCoverageStatements(data);
}

function renderCoverageReport(data) {
  currentCoverageData = data;
  const percent = Number(data.coverage_percent || 0);
  coverageEmpty.classList.add("is-hidden");
  coverageResults.classList.remove("is-hidden");
  coverageResults.classList.remove("coverage-just-rendered");
  coverageScoreRing.classList.remove("coverage-score-pop");
  void coverageResults.offsetWidth;
  coverageResults.classList.add("coverage-just-rendered");
  coverageScoreRing.classList.add("coverage-score-pop");
  coverageScoreRing.style.setProperty("--coverage-score", percent);
  coverageScoreValue.textContent = `${Math.round(percent)}%`;
  coverageScoreTitle.textContent = `${data.covered_line_count || 0} of ${data.total_line_count || 0} lines`;
  coverageScoreNote.textContent = "Hover highlighted documentation or source lines to jump between the evidence map.";
  coverageRenderedDocs.innerHTML = `<p class="coverage-inline-message">Coverage is ready. Open the fullscreen evidence map to inspect source lines and rendered Markdown side by side.</p>`;
  coverageDocStatements.innerHTML = "";
  coverageSourceLines.innerHTML = "";
  renderCoverageModalContent(data);
  coverageResults.classList.add("coverage-results-compact");
  coverageFullscreenButton?.classList.remove("is-hidden");
}

async function assessCoverage() {
  fillCoverageDocsFromCurrent(false);
  const docs = coverageDocsInput.value.trim();
  const sourceCode = currentSource.trim() || documentationInput.value.trim();
  if (!sourceCode || !docs) {
    renderError("Source code and documentation are required for coverage assessment.", "Coverage failed", "Missing coverage inputs");
    return;
  }
  runCoverageButton.disabled = true;
  runCoverageButton.textContent = "Assessing...";
  setStatus("review", "Assessing coverage");
  try {
    const data = await postJson("/api/coverage", {
      source_code: sourceCode,
      docs,
      openai_key: openaiKeyInput.value.trim(),
      openai_seed: openaiSeedInput.value
    }, { cache: false });
    renderCoverageReport(data);
    setStatus("ready", "Coverage assessed");
  } catch (error) {
    renderError(error.message || "Coverage assessment failed. Add an OpenAI key or set OPENAI_API_KEY, then try again.", "Coverage failed", "Could not assess documentation coverage");
  } finally {
    runCoverageButton.disabled = false;
    runCoverageButton.textContent = "Assess coverage";
  }
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
  tdPanel?.classList.add("is-hidden");
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
  tdPanel?.classList.add("is-hidden");
  coveragePanel?.classList.add("is-hidden");
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
    if (metric.mutation_error) {
      return `<span class="mutation-pill mutation-low"${mutationError}>Mutation failed</span>`;
    }
    if (metric.test_code) {
      return `
        <button type="button" class="mutation-pill mutation-medium mutation-analysis-button" data-mutation-index="${index}">
          Run mutation
        </button>
      `;
    }
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
    // Honor the mutation toggle here so mutation scores are available in
    // the review table when the user asks for them.
    show_mutation_tests: showMutationTestingInput.checked,
    run_mutation_in_overall: showMutationTestingInput.checked,
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
	      tone: toneInput.value,
	      skip_anonymous_save: Boolean(getAccessToken())
	    }, (_chunk, fullText) => {
	      writer.push(fullText);
	    });
    currentMarkdown = await writer.finish(streamedMarkdown);
    generatedDoc.classList.remove("is-streaming");
	    generatedDoc.innerHTML = renderMarkdown(currentMarkdown);
	    addGeneratedDoc(currentMarkdown, accepted);
	    try {
	      const savedDoc = await saveCompletedDocumentation(accepted);
	      if (savedDoc) {
	        setStatus("ready", "Saved to DB");
	        markTDStepReady();
	        showCompareStage(true);
	      } else {
	        setStatus("ready", "Generated");
	        showCompareStage(true);
	      }
	    } catch (saveError) {
	      setStatus("ready", "Generated, save failed");
	      console.warn("Could not save generated documentation", saveError);
	    }
    fillCoverageDocsFromCurrent(true);
    syncMarkdownActions();
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
  coveragePanel?.classList.add("is-hidden");
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

themeToggles.forEach((toggle) => {
  toggle.addEventListener("click", () => {
    const nextMode = document.body.classList.contains("dark-mode") ? "light" : "dark";
    localStorage.setItem(DARK_MODE_STORAGE_KEY, nextMode);
    applyTheme(nextMode);
  });
});

const landingExampleSwitch = document.querySelector(".landing-example-switch");
const landingOriginalDocs = document.querySelector("#landing-original-docs");
const landingInvariantDocs = document.querySelector("#landing-invariant-docs");
const landingOriginalTitle = document.querySelector("#landing-original-title");
const landingInvariantTitle = document.querySelector("#landing-invariant-title");
const landingExampleCache = new Map();
let landingExampleRequestId = 0;

async function loadLandingExample(exampleId = "numpy-pad") {
  if (!landingOriginalDocs || !landingInvariantDocs) return;
  const example = docsExamples[exampleId] || docsExamples["numpy-pad"];
  const requestId = (landingExampleRequestId += 1);

  landingExampleSwitch?.querySelectorAll(".landing-example-choice").forEach((button) => {
    const active = button.dataset.landingExample === exampleId;
    button.classList.toggle("is-active", active);
    button.setAttribute("aria-selected", active ? "true" : "false");
  });
  if (landingOriginalTitle) landingOriginalTitle.textContent = `Original ${example.label}`;
  if (landingInvariantTitle) landingInvariantTitle.textContent = `Invariant-based ${example.label}`;

  const render = ({ original, invariant }) => {
    if (requestId !== landingExampleRequestId) return;
    landingOriginalDocs.innerHTML = renderMarkdown(original);
    landingInvariantDocs.innerHTML = renderMarkdown(invariant);
  };

  if (landingExampleCache.has(exampleId)) {
    render(landingExampleCache.get(exampleId));
    return;
  }

  landingOriginalDocs.innerHTML = '<p class="placeholder">Loading public documentation…</p>';
  landingInvariantDocs.innerHTML = '<p class="placeholder">Loading invariant-based documentation…</p>';
  try {
    const [originalResponse, invariantResponse] = await Promise.all([
      fetch(example.originalPath),
      fetch(example.invariantPath)
    ]);
    if (!originalResponse.ok || !invariantResponse.ok) {
      throw new Error("unavailable");
    }
    const payload = {
      original: await originalResponse.text(),
      invariant: await invariantResponse.text()
    };
    landingExampleCache.set(exampleId, payload);
    render(payload);
  } catch {
    if (requestId !== landingExampleRequestId) return;
    landingOriginalDocs.innerHTML = `<p class="placeholder">Could not load the ${example.label} example. Launch the app to generate it live.</p>`;
    landingInvariantDocs.innerHTML = "";
  }
}

landingExampleSwitch?.addEventListener("click", (event) => {
  const button = event.target.closest(".landing-example-choice");
  if (!button) return;
  loadLandingExample(button.dataset.landingExample);
});

loadLandingExample("numpy-pad");
renderLandingLeaderboard();

if ("IntersectionObserver" in window) {
  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-revealed");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
  document.querySelectorAll("[data-reveal]").forEach((node) => revealObserver.observe(node));
} else {
  document.querySelectorAll("[data-reveal]").forEach((node) => node.classList.add("is-revealed"));
}

launchAppButtons.forEach((button) => {
  button.addEventListener("click", showAppPage);
});

loginOpenButtons.forEach((button) => {
  button.addEventListener("click", () => {
    if (button.dataset.authMode === "account" || (button.id === "landing-account-button" && getAccessToken())) {
      showAccountPage();
      return;
    }
    showLoginPage(button.dataset.authMode || "login");
  });
});

areaOpenButtons.forEach((button) => {
  button.addEventListener("click", showAreaPage);
});

document.querySelectorAll(".home-button").forEach((button) => {
  button.addEventListener("click", showLandingPage);
});

document.querySelectorAll(".research-mode-button").forEach((button) => {
  button.addEventListener("click", toggleResearchMode);
});

areaRankLimitInput?.addEventListener("input", () => {
  const value = Math.max(0, Number(areaRankLimitInput.value || 0));
  if (value) {
    localStorage.setItem(ARENA_RANK_LIMIT_STORAGE_KEY, String(value));
  } else {
    localStorage.removeItem(ARENA_RANK_LIMIT_STORAGE_KEY);
  }
  updateAreaSessionUI();
});

areaBackButton?.addEventListener("click", () => {
  if (isResearchModeActive()) {
    toggleResearchMode();
    return;
  }
  if (getAccessToken()) {
    showAccountPage();
    return;
  }
  showLandingPage();
});

areaNextButton?.addEventListener("click", showNextAreaPost);

areaChoices.forEach((choice) => {
  choice.addEventListener("click", () => selectAreaWinner(choice.dataset.areaChoice));
  choice.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      selectAreaWinner(choice.dataset.areaChoice);
    }
  });
});

areaVoteButton?.addEventListener("click", submitAreaVote);
tdFormatButton?.addEventListener("click", formatTraditionalMarkdown);
tdSaveButton?.addEventListener("click", saveTraditionalMarkdown);
researchConfirmButton?.addEventListener("click", confirmResearchMode);
researchCancelButton?.addEventListener("click", closeResearchModal);
researchChangePhraseButton?.addEventListener("click", changeResearchPhrase);
researchModal?.addEventListener("click", (event) => {
  if (event.target?.matches?.("[data-close-research-modal]")) closeResearchModal();
});
researchModal?.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    confirmResearchMode();
  }
  if (event.key === "Escape") closeResearchModal();
});

authBackButton?.addEventListener("click", showLandingPage);
authModeToggle?.addEventListener("click", () => setAuthMode(authMode === "signup" ? "login" : "signup"));
authForm?.addEventListener("submit", submitAuth);

accountMenuButton?.addEventListener("click", () => {
  const isHidden = accountMenu?.classList.toggle("is-hidden");
  accountMenuButton.setAttribute("aria-expanded", String(!isHidden));
  if (!isHidden) fetchSavedDocs();
});

savedDocRefreshButton?.addEventListener("click", fetchSavedDocs);
savedDocSearchInput?.addEventListener("input", renderSavedDocs);

savedDocList?.addEventListener("click", (event) => {
  const button = event.target.closest(".saved-doc-card");
  if (!button) return;
  const doc = savedDocumentation.find((item) => String(item.id) === String(button.dataset.savedDocId));
  if (!doc) return;
  addSavedDocToSession(doc);
  accountMenu?.classList.add("is-hidden");
  accountMenuButton?.setAttribute("aria-expanded", "false");
});

logoutButton?.addEventListener("click", () => {
  localStorage.removeItem(ACCESS_TOKEN_STORAGE_KEY);
  localStorage.removeItem(USER_EMAIL_STORAGE_KEY);
  savedDocumentation = [];
  updateAccountMenuLabel();
  renderSavedDocs();
  setStatus("draft", "Signed out");
});

accountPageButton?.addEventListener("click", showAccountPage);
accountBackButton?.addEventListener("click", showAppPage);
accountDocsRefresh?.addEventListener("click", () => {
  fetchAccountProfile();
  fetchAccountDocs();
});
passwordForm?.addEventListener("submit", submitPasswordChange);
deleteAccountButton?.addEventListener("click", revealDeleteConfirm);
deleteCancelButton?.addEventListener("click", hideDeleteConfirm);
deleteConfirmInput?.addEventListener("input", updateDeleteConfirmState);
deleteConfirmButton?.addEventListener("click", deleteAccount);
accountDocsSort?.addEventListener("change", () => {
  accountSort = accountDocsSort.value;
  renderAccountDocs();
});
accountDocsSearch?.addEventListener("input", renderAccountDocs);

accountDocsList?.addEventListener("click", (event) => {
  const deleteButton = event.target.closest(".account-doc-delete");
  if (deleteButton) {
    deleteAccountDocument(deleteButton.dataset.docId).catch((error) => {
      if (accountDocsList) accountDocsList.innerHTML = `<p class="placeholder">${escapeHtml(error.message || "Could not delete document.")}</p>`;
    });
    return;
  }
  const button = event.target.closest(".account-doc-view");
  if (!button) return;
  showAccountDocDetail(button.dataset.docId);
});

accountDetailClose?.addEventListener("click", closeAccountDocDetail);
accountDetailModal?.addEventListener("click", (event) => {
  if (event.target?.matches?.("[data-close-account-detail]")) closeAccountDocDetail();
});

accountDetailBody?.addEventListener("click", (event) => {
  if (event.target.closest("#account-md-download")) {
    downloadActiveAccountMarkdown();
    return;
  }
  if (event.target.closest("#account-md-edit")) {
    setAccountMarkdownEditing(true);
    return;
  }
  if (event.target.closest("#account-md-delete")) {
    deleteAccountDocument(activeAccountDoc?.id).catch((error) => {
      const message = accountDetailBody?.querySelector("#account-md-message");
      if (message) message.textContent = error.message || "Could not delete document.";
    });
    return;
  }
  if (event.target.closest("#account-md-cancel")) {
    setAccountMarkdownEditing(false);
    return;
  }
  const saveButton = event.target.closest("#account-md-save");
  if (saveButton) {
    saveAccountMarkdown(saveButton);
  }
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !accountDetailModal?.classList.contains("is-hidden")) closeAccountDocDetail();
});

modelProviderInput?.addEventListener("change", () => {
  updateModelProviderControls();
  requestCache.clear();
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
    if (tab.disabled || tab.getAttribute("aria-disabled") === "true") return;
    if (tab.dataset.step === "input") {
      showInputStage();
    } else if (tab.dataset.step === "review") {
      showReviewStage();
    } else if (tab.dataset.step === "compare") {
      showCompareStage();
    } else if (tab.dataset.step === "tests") {
      showTestsStage();
    } else if (tab.dataset.step === "td") {
      showTDStage();
    } else if (tab.dataset.step === "coverage") {
      showCoverageStage();
    }
  });
});

renderGeneratedDocsLibrary();
updateModelProviderControls();
// Always land on the marketing page so it stays viewable, even when signed in.
showLandingPage();
setStage("input");
updateAccountMenuLabel();
// Keep the session across refreshes: the stored token is preserved so the user
// stays logged in. Validate it in the background and only drop it if it has
// actually expired (401) — a refresh on its own never logs the user out.
if (getAccessToken()) {
  fetch(apiUrl("/users/me"), { headers: authHeaders({ Accept: "application/json" }) })
    .then((response) => {
      if (response.status === 401) {
        localStorage.removeItem(ACCESS_TOKEN_STORAGE_KEY);
        localStorage.removeItem(USER_EMAIL_STORAGE_KEY);
        updateAccountMenuLabel();
      }
    })
    .catch(() => {});
}
