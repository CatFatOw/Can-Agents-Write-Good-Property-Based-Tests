const form = document.querySelector("#documentation-form");
const landingPage = document.querySelector("#landing-page");
const loginPage = document.querySelector("#login-page");
const areaPage = document.querySelector("#area-page");
const appShell = document.querySelector("#app-shell");
const launchAppButtons = Array.from(document.querySelectorAll(".launch-app-button"));
const loginOpenButtons = Array.from(document.querySelectorAll(".login-open-button"));
const loginAccountButtons = Array.from(document.querySelectorAll(".login-open-button[data-auth-mode='login'], #landing-account-button"));
const areaOpenButtons = Array.from(document.querySelectorAll(".area-open-button"));
const homeButton = document.querySelector("#home-button");
const areaBackButton = document.querySelector(".area-back-button");
const areaNextButton = document.querySelector("#area-next-button");
const areaNextBottomButton = document.querySelector("#area-next-bottom-button");
const areaVoteButton = document.querySelector("#area-vote-button");
const areaVoteMessage = document.querySelector("#area-vote-message");
const areaCommentInput = document.querySelector("#area-comment-input");
const areaRankCount = document.querySelector("#area-rank-count");
const areaRankLimitInput = document.querySelector("#area-rank-limit");
const areaLimitMessage = document.querySelector("#area-limit-message");
const areaSessionProgressBar = document.querySelector("#area-session-progress-bar");
const areaResetButton = document.querySelector("#area-reset-button");
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
const areaModeTabs = Array.from(document.querySelectorAll(".area-mode-tab"));
const areaPanels = Array.from(document.querySelectorAll("[data-area-panel]"));
const areaComprehensionView = document.querySelector("#area-comprehension-view");
const assessmentNextButton = document.querySelector("#assessment-next-button");
const assessmentDocSelect = document.querySelector("#assessment-doc-select");
const assessmentDocTypeSelect = document.querySelector("#assessment-doc-type-select");
const assessmentDocRemaining = document.querySelector("#assessment-doc-remaining");
const assessmentDocTitle = document.querySelector("#assessment-doc-title");
const assessmentResourceTabs = Array.from(document.querySelectorAll(".assessment-resource-tab"));
const assessmentResourceSummary = document.querySelector("#assessment-resource-summary");
const assessmentResourceBody = document.querySelector("#assessment-resource-body");
const assessmentProgressText = document.querySelector("#assessment-progress-text");
const assessmentProgressBar = document.querySelector("#assessment-progress-bar");
const assessmentQuestionText = document.querySelector("#assessment-question-text");
const assessmentChoiceList = document.querySelector("#assessment-choice-list");
const assessmentSubmitButton = document.querySelector("#assessment-submit-button");
const assessmentMessage = document.querySelector("#assessment-message");
const assessmentCorrectCount = document.querySelector("#assessment-correct-count");
const assessmentAnsweredCount = document.querySelector("#assessment-answered-count");
const assessmentPercentCorrect = document.querySelector("#assessment-percent-correct");
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
const databaseStatus = document.querySelector("#database-status");
const databaseStatusText = document.querySelector("#database-status-text");
let databaseStatusRetryTimer = 0;
let databaseStatusRetryDelay = 5000;
const DATABASE_STATUS_STORAGE_KEY = "pbt_database_status";
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
const accountLogoutButton = document.querySelector("#account-logout-button");
const accountAdminActions = document.querySelector("#account-admin-actions");
const accountAdminMessage = document.querySelector("#account-admin-message");
const accountResetTarget = document.querySelector("#account-reset-target");
const accountResetLookupField = document.querySelector("#account-reset-lookup-field");
const accountResetLookup = document.querySelector("#account-reset-lookup");
const accountResetAttemptsAll = document.querySelector("#account-reset-attempts-all");
const accountEmail = document.querySelector("#account-email");
const accountCreated = document.querySelector("#account-created");
const accountId = document.querySelector("#account-id");
const accountRole = document.querySelector("#account-role");
const accountDocCount = document.querySelector("#account-doc-count");
const accountStats = document.querySelector("#account-stats");
const accountDocsList = document.querySelector("#account-docs-list");
const accountDocsRefresh = document.querySelector("#account-docs-refresh");
const accountDocsSearch = document.querySelector("#account-docs-search");
const accountDocsTitle = document.querySelector("#account-docs-title");
const accountDocsScope = document.querySelector("#account-docs-scope");
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
const ARENA_COMPLETED_COMPARISONS_STORAGE_KEY = "ibd-arena-completed-comparisons";
const RESEARCH_MODE_STORAGE_KEY = "ibd-research-mode";
const RESEARCH_PHRASE_STORAGE_KEY = "ibd-research-phrase";
const RUNTIME_API_BASE_URL = window.__IBD_CONFIG__?.apiBaseUrl || window.__APP_CONFIG__?.apiBaseUrl || "";
const API_BASE_URL = RUNTIME_API_BASE_URL.replace(/\/$/, "") || (window.location.protocol === "file:" ? "http://127.0.0.1:8011" : "");
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
let activeAreaMode = "compare";
let currentAssessment = null;
let currentAssessmentDoc = null;
let currentAssessmentQuestionIndex = 0;
let selectedAssessmentChoice = "";
let answeredAssessmentQuestions = new Set();
let assessmentSelectedChoices = new Map();
let assessmentAnswerResults = new Map();
let assessmentAnsweredCountValue = 0;
let assessmentCorrectCountValue = 0;
let activeAssessmentResource = "documentation";
let assessmentSummaryVisible = false;
let assessmentDocumentationOptions = [];
let activeAssessmentDocumentationId = "";
let activeAssessmentDocType = "random";
const assessmentSessionCache = new Map();
let activeAccountAssessmentTab = "questions";
let activeAccountResponseUserFilter = "all";
let accountRefreshTimer = 0;
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
  refreshAccountDataSoon();
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
  updateAccountMenuLabel();
  if (getAccessToken()) {
    await refreshAccountAdminState();
  } else {
    accountIsAdmin = false;
    updateAccountDocsScopeUi();
    updateAssessmentDocTypeControl();
  }
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

function areaCompletedComparisonIds() {
  try {
    const parsed = JSON.parse(localStorage.getItem(ARENA_COMPLETED_COMPARISONS_STORAGE_KEY) || "[]");
    return new Set(Array.isArray(parsed) ? parsed.map(String) : []);
  } catch {
    return new Set();
  }
}

function saveAreaCompletedComparisonIds(ids) {
  localStorage.setItem(ARENA_COMPLETED_COMPARISONS_STORAGE_KEY, JSON.stringify([...ids]));
}

function markAreaComparisonCompleted(documentationId) {
  if (!documentationId) return;
  const completed = areaCompletedComparisonIds();
  completed.add(String(documentationId));
  saveAreaCompletedComparisonIds(completed);
}

function resetLocalAreaSession() {
  localStorage.setItem(ARENA_RANK_COUNT_STORAGE_KEY, "0");
  localStorage.removeItem(ARENA_COMPLETED_COMPARISONS_STORAGE_KEY);
  selectedAreaWinner = null;
  areaVoteSubmitted = false;
  if (areaCommentInput) areaCommentInput.value = "";
  updateAreaSessionUI();
}

function areaRankLimitValue() {
  if (!isResearchModeActive()) return 0;
  return Number(localStorage.getItem(ARENA_RANK_LIMIT_STORAGE_KEY) || 0);
}

function updateAreaSessionUI() {
  const count = areaRankCountValue();
  const limit = areaRankLimitValue();
  const completed = areaCompletedComparisonIds().size;
  const denominator = limit || Math.max(completed, count, comparisonLeaderboardRows.length || areaFallbackPosts.length, 1);
  const progress = Math.max(0, Math.min(100, (Math.max(count, completed) / denominator) * 100));
  if (areaRankCount) {
    areaRankCount.textContent = limit ? `${count} / ${limit} ranked` : `${completed || count} completed`;
  }
  if (areaSessionProgressBar) areaSessionProgressBar.style.width = `${progress}%`;
  if (areaRankLimitInput) {
    areaRankLimitInput.value = limit ? String(limit) : "";
  }
  if (areaLimitMessage) {
    areaLimitMessage.textContent = isResearchModeActive()
      ? (limit && count >= limit
        ? (accountIsAdmin ? "Research limit reached. Reset attempts from the Account admin page." : "Research limit reached. Ask an admin to reset the Arena session.")
        : "Research mode limit is enforced.")
      : "Normal mode tracks completed comparisons in this browser.";
  }
  if (areaResetButton) {
    areaResetButton.classList.add("is-hidden");
    areaResetButton.disabled = true;
  }
  if (areaVoteButton) {
    areaVoteButton.disabled = Boolean(areaVoteSubmitted || (limit && count >= limit) || !selectedAreaWinner);
  }
  areaNextButton?.classList.toggle("assessment-next-ready", areaVoteSubmitted);
  areaNextBottomButton?.classList.toggle("assessment-next-ready", areaVoteSubmitted);
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

function hasRenderableAreaDocs(post) {
  return Boolean(String(post?.tdDoc || "").trim() && String(post?.ibdDoc || "").trim());
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
  const completed = areaCompletedComparisonIds();
  const hasRemainingFallback = areaFallbackPosts.some((post, index) => !completed.has(String(post.id || post.title || index)));
  if (!getAccessToken() && !hasRemainingFallback) {
    areaVoteSubmitted = true;
    selectedAreaWinner = null;
    if (areaVoteMessage) areaVoteMessage.textContent = accountIsAdmin
      ? "You have completed every bundled comparison in this browser. Reset comparison attempts from the Account admin page."
      : "You have completed every bundled comparison in this browser. Ask an admin to reset comparison progress.";
    updateAreaSessionUI();
    return;
  }
  areaLoading = true;
  areaVoteSubmitted = false;
  selectedAreaWinner = null;
  randomizeAreaSides();
  if (areaVoteMessage) areaVoteMessage.textContent = "Loading anonymous documentation samples...";
  if (areaVoteButton) areaVoteButton.disabled = true;
  try {
    const response = await fetch(apiUrl(getAccessToken() ? "/comparison/random-user" : "/comparison/random"), {
      headers: authHeaders({ Accept: "application/json" })
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || "No comparison documents are available yet.");
    currentAreaPost = normalizeAreaPost(data);
    if (!hasRenderableAreaDocs(currentAreaPost)) {
      throw new Error("The selected comparison is missing either TD or IBD Markdown.");
    }
  } catch (error) {
    const fallbackIndex = areaFallbackPosts.findIndex((post, index) => !completed.has(String(post.id || post.title || index)));
    activeAreaIndex = fallbackIndex >= 0 ? fallbackIndex : 0;
    currentAreaPost = fallbackIndex >= 0 ? areaFallbackPosts[fallbackIndex] : null;
    if (!currentAreaPost) {
      if (areaVoteMessage) areaVoteMessage.textContent = error.message || "No remaining comparisons are available.";
      return;
    }
    await hydrateAreaPostDocs(currentAreaPost).catch((fallbackError) => {
      if (areaVoteMessage) areaVoteMessage.textContent = fallbackError.message;
    });
    if (!hasRenderableAreaDocs(currentAreaPost)) {
      currentAreaPost = null;
      if (areaVoteMessage) areaVoteMessage.textContent = "No comparison with both TD and IBD Markdown is ready yet.";
      return;
    }
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

function formatPercentValue(value) {
  const numeric = Number(value);
  if (!Number.isFinite(numeric)) return "—";
  return `${Math.round(numeric * 100)}%`;
}

function formatSignedStatistic(value) {
  const numeric = Number(value);
  if (!Number.isFinite(numeric)) return "—";
  return numeric.toFixed(2);
}

function renderBradleyTerryStats(entry) {
  const comparisonCount = Number(entry.comparison_count || 0);
  const winProb = Number(entry.bt_ibd_win_prob);
  const ciLower = Number(entry.bt_ibd_win_prob_ci_lower);
  const ciUpper = Number(entry.bt_ibd_win_prob_ci_upper);
  const hasCi = Number.isFinite(ciLower) && Number.isFinite(ciUpper);
  const hasBt = comparisonCount >= 2 && Number.isFinite(winProb);
  if (!hasBt) {
    return `
      <section class="bt-stat-panel is-empty" aria-label="Bradley-Terry statistics">
        <div class="bt-stat-head">
          <span class="area-viz-label">Bradley-Terry model</span>
          <strong>Not enough comparisons yet</strong>
        </div>
        <p>Model-estimated win probability appears after at least 2 blind comparisons for this documentation pair.</p>
      </section>
    `;
  }
  return `
    <section class="bt-stat-panel" aria-label="Bradley-Terry statistics">
      <div class="bt-stat-head">
        <span class="area-viz-label">Bradley-Terry model</span>
        <strong>${formatPercentValue(winProb)}</strong>
      </div>
      <p class="bt-stat-note">Model-estimated probability from the vote pattern, not the raw observed win rate.</p>
      <div class="area-stat-grid">
        <span><strong>${formatSignedStatistic(entry.bt_ibd_rating)}</strong> Invariant-based BT rating</span>
        <span><strong>${formatSignedStatistic(entry.bt_td_rating)}</strong> Baseline BT rating</span>
        <span><strong>${formatPercentValue(winProb)}</strong> Model-estimated invariant-based win probability</span>
        <span><strong>${hasCi ? `${formatPercentValue(ciLower)}-${formatPercentValue(ciUpper)}` : "—"}</strong> 95% CI</span>
      </div>
    </section>
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
          <summary>Invariant-based Markdown</summary>
          <div class="markdown-rendered landing-doc-scroll leaderboard-doc-preview">${renderMarkdown(ibdMarkdown)}</div>
        </details>
      ` : ""}
      ${tdMarkdown ? `
        <details>
          <summary>Baseline Markdown</summary>
          <div class="markdown-rendered landing-doc-scroll leaderboard-doc-preview">${renderMarkdown(tdMarkdown)}</div>
        </details>
      ` : ""}
      ${sourceCode ? `
        <details>
          <summary>Source code</summary>
          <div class="landing-doc-scroll leaderboard-doc-preview">${renderPythonMarkdown(sourceCode)}</div>
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
                ${metric.test_code ? renderPythonMarkdown(metric.test_code) : ""}
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
        <span class="area-viz-label">Observed vote split</span>
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
      .filter((entry) => String(entry.IBD_generated_md || entry.ibd_doc || "").trim());
    if (!ranked.length) {
      landingLeaderboardSection?.classList.remove("is-hidden");
      landingLeaderboardList.innerHTML = '<li class="placeholder">No generated invariant-based documentation has been saved to this database yet.</li>';
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
                <small>${voteCount ? `${voteCount} blind comparisons` : (String(entry.TD_md || entry.td_doc || "").trim() ? "Ready for Arena votes" : "Saved; add baseline Markdown for Arena")}</small>
              </div>
              <span class="area-rating">ELO: ${Number(entry.ibd_doc_elo_rating || 0)}</span>
            </div>
            <details class="area-documentation-menu">
              <summary>Open docs / invariants</summary>
              ${renderLeaderboardDocumentationMenu(entry)}
            </details>
            <details class="area-ranking-details">
              <summary>Show study stats</summary>
              <div class="area-stat-grid">
                <span><strong>${Number(entry.ibd_doc_elo_rating || 0)}</strong> Invariant-based Elo</span>
                <span><strong>${Number(entry.td_doc_elo_rating || 0)}</strong> Baseline Elo</span>
                <span><strong>${voteCount >= 2 ? formatPercentValue(entry.bt_ibd_win_prob) : "Pending"}</strong> Bradley-Terry model probability</span>
                <span><strong>${voteCount}</strong> comparisons</span>
              </div>
              ${renderBradleyTerryStats(entry)}
              <div class="area-distribution" aria-label="Preference distribution">
                <div class="area-distribution-bar">
                  <span style="--share: ${ibdPct}%" title="Invariant-based ${ibdPct}%"></span>
                  <span style="--share: ${tdPct}%" title="Baseline ${tdPct}%"></span>
                </div>
                <div class="area-distribution-labels">
                  <small>Observed invariant-based wins ${ibdPct}%</small>
                  <small>Observed baseline wins ${tdPct}%</small>
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
    landingLeaderboardSection?.classList.remove("is-hidden");
    landingLeaderboardList.innerHTML = `<li class="placeholder">${escapeHtml(error.message || "Could not load leaderboard.")} Retrying when the cloud database wakes up.</li>`;
    window.setTimeout(renderLandingLeaderboard, 7000);
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
            <span class="area-rating">ELO: ${post.ibdElo}</span>
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
              <span><strong>${post.ibdElo}</strong> Invariant-based Elo</span>
              <span><strong>${post.tdElo}</strong> Baseline Elo</span>
              <span><strong>${voteCount >= 2 ? formatPercentValue(post.bt) : "Pending"}</strong> Bradley-Terry model probability</span>
              <span><strong>${voteCount}</strong> comparisons</span>
            </div>
            ${renderBradleyTerryStats({
              comparison_count: voteCount,
              bt_ibd_rating: post.btIbdRating,
              bt_td_rating: post.btTdRating,
              bt_ibd_win_prob: post.bt,
              bt_ibd_win_prob_ci_lower: post.btCiLower,
              bt_ibd_win_prob_ci_upper: post.btCiUpper
            })}
            <div class="area-distribution" aria-label="Preference distribution">
              <div class="area-distribution-bar">
                <span style="--share: ${ibdPct}%" title="Invariant-based ${ibdPct}%"></span>
                <span style="--share: ${tdPct}%" title="Baseline ${tdPct}%"></span>
              </div>
              <div class="area-distribution-labels">
                <small>Observed invariant-based wins ${ibdPct}%</small>
                <small>Observed baseline wins ${tdPct}%</small>
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
          <small>Observed invariant-based wins ${ibdPct}%</small>
          <small>Observed baseline wins ${tdPct}%</small>
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
  if (!hasRenderableAreaDocs(post)) {
    if (areaTdDoc) areaTdDoc.innerHTML = '<p class="placeholder">TD Markdown is not ready for this comparison.</p>';
    if (areaIbdDoc) areaIbdDoc.innerHTML = '<p class="placeholder">IBD Markdown is not ready for this comparison.</p>';
    if (areaVoteButton) areaVoteButton.disabled = true;
    if (areaVoteMessage) areaVoteMessage.textContent = "This comparison is missing one documentation version.";
    return;
  }

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
      ? "Vote recorded. Use Next comparison to continue."
      : "Blind study mode. Pick a candidate without seeing source labels, rankings, or statistics.";
  }
  areaChoices.forEach((choice, index) => {
    const label = index === 0 ? "A" : "B";
    choice.dataset.areaLabel = label;
    choice.dataset.areaChoice = activeAreaSides[label];
    const active = choice.dataset.areaChoice === selectedAreaWinner;
    choice.classList.toggle("is-selected", active);
    choice.classList.toggle("is-locked", areaVoteSubmitted);
    choice.setAttribute("aria-pressed", String(active));
    choice.setAttribute("aria-disabled", String(areaVoteSubmitted));
  });
  updateAreaSessionUI();
}

function setAreaMode(nextMode) {
  activeAreaMode = nextMode === "comprehension" ? "comprehension" : "compare";
  areaModeTabs.forEach((button) => {
    const active = button.dataset.areaMode === activeAreaMode;
    button.classList.toggle("is-active", active);
    button.setAttribute("aria-selected", active ? "true" : "false");
  });
  areaPanels.forEach((panel) => {
    panel.classList.toggle("is-hidden", panel.dataset.areaPanel !== activeAreaMode);
  });
  if (activeAreaMode === "comprehension") {
    loadAssessmentDocumentationOptions();
    if (!currentAssessment) loadAssessment(activeAssessmentDocumentationId);
  }
}

function anonymizeStudyReference(text, label = "Reference") {
  return String(text || "")
    .split(/\r?\n/)
    .map((line) => {
      if (/^\s*(?:>\s*)?(?:source|url|original source|reference source)\s*:/i.test(line)) {
        return "";
      }
      return line
        .replace(/\[[^\]]+\]\((?:https?:\/\/|www\.)[^)]+\)/gi, "reference")
        .replace(/https?:\/\/\S+|www\.\S+/gi, "")
        .replace(/\b(?:TD|IBD)\b/gi, label)
        .replace(/\b(?:original|traditional|baseline)\s+documentation\b/gi, `${label} documentation`)
        .replace(/\binvariant[-\s]?based documentation\b/gi, `${label} documentation`)
        .replace(/\b(?:public|official|original)?\s*(?:NumPy\s+)?reference documentation\b/gi, "reference documentation");
    })
    .filter((line) => line.trim())
    .join("\n");
}

async function fetchAssessmentDocumentation(documentationId) {
  if (!documentationId) return null;
  try {
    const response = await fetch(apiUrl(`/documentation/${documentationId}`), {
      headers: authHeaders({ Accept: "application/json" })
    });
    const data = await response.json().catch(() => ({}));
    return response.ok ? data : null;
  } catch {
    return null;
  }
}

function currentAssessmentQuestion() {
  return currentAssessment?.questions?.[currentAssessmentQuestionIndex] || null;
}

function normalizeAssessmentDocType(value) {
  const type = String(value || "").toLowerCase();
  if (type === "ibd" || type === "td") return type;
  return "random";
}

function selectedAssessmentDocType() {
  return accountIsAdmin ? normalizeAssessmentDocType(assessmentDocTypeSelect?.value || "random") : "random";
}

function assessmentSessionKey(documentationId, docType) {
  const docId = documentationId || currentAssessment?.documentation_id || activeAssessmentDocumentationId || "random";
  return `${docId}:${normalizeAssessmentDocType(docType)}`;
}

function saveCurrentAssessmentSession() {
  if (!currentAssessment) return;
  const docType = normalizeAssessmentDocType(currentAssessment.documentation_type || activeAssessmentDocType || selectedAssessmentDocType());
  assessmentSessionCache.set(assessmentSessionKey(currentAssessment.documentation_id, docType), {
    currentAssessment,
    currentAssessmentDoc,
    currentAssessmentQuestionIndex,
    selectedAssessmentChoice,
    answeredAssessmentQuestions: Array.from(answeredAssessmentQuestions),
    assessmentSelectedChoices: Array.from(assessmentSelectedChoices.entries()),
    assessmentAnswerResults: Array.from(assessmentAnswerResults.entries()),
    assessmentAnsweredCountValue,
    assessmentCorrectCountValue,
    activeAssessmentResource,
    assessmentSummaryVisible,
    activeAssessmentDocType: docType,
    activeAssessmentDocumentationId: String(currentAssessment.documentation_id || activeAssessmentDocumentationId || "")
  });
}

function restoreAssessmentSession(session) {
  currentAssessment = session.currentAssessment;
  currentAssessmentDoc = session.currentAssessmentDoc;
  currentAssessmentQuestionIndex = session.currentAssessmentQuestionIndex || 0;
  selectedAssessmentChoice = session.selectedAssessmentChoice || "";
  answeredAssessmentQuestions = new Set(session.answeredAssessmentQuestions || []);
  assessmentSelectedChoices = new Map(session.assessmentSelectedChoices || []);
  assessmentAnswerResults = new Map(session.assessmentAnswerResults || []);
  assessmentAnsweredCountValue = Number(session.assessmentAnsweredCountValue || 0);
  assessmentCorrectCountValue = Number(session.assessmentCorrectCountValue || 0);
  activeAssessmentResource = session.activeAssessmentResource || "documentation";
  assessmentSummaryVisible = Boolean(session.assessmentSummaryVisible);
  activeAssessmentDocType = normalizeAssessmentDocType(session.activeAssessmentDocType || currentAssessment?.documentation_type || "random");
  activeAssessmentDocumentationId = session.activeAssessmentDocumentationId || "";
  if (assessmentDocSelect) assessmentDocSelect.value = activeAssessmentDocumentationId;
  renderAssessmentResource();
  if (assessmentSummaryVisible) {
    renderAssessmentSummary();
  } else {
    renderAssessmentQuestion();
  }
  updateAssessmentStatsUI();
  fetchAssessmentStats();
}

function renderAssessmentResource() {
  if (!assessmentResourceBody || !currentAssessment) return;
  assessmentResourceTabs.forEach((button) => {
    const active = button.dataset.assessmentResource === activeAssessmentResource;
    button.classList.toggle("is-active", active);
    button.setAttribute("aria-selected", active ? "true" : "false");
  });
  const title = currentAssessment.documentation_title || "Documentation sample";
  const typeLabel = currentAssessment.documentation_type ? ` (${currentAssessment.documentation_type})` : "";
  if (assessmentDocTitle) assessmentDocTitle.textContent = `${title}${typeLabel}`;
  if (activeAssessmentResource === "source") {
    const source = anonymizeStudyReference(currentAssessmentDoc?.source_code || "", "Reference");
    if (assessmentResourceSummary) assessmentResourceSummary.textContent = "Open source code";
    assessmentResourceBody.innerHTML = source
      ? renderPythonMarkdown(source)
      : '<p class="placeholder">Source code is not available for this assessment.</p>';
    return;
  }
  const doc = anonymizeStudyReference(currentAssessment.documentation || "", "Reference");
  if (assessmentResourceSummary) assessmentResourceSummary.textContent = "Open documentation";
  assessmentResourceBody.innerHTML = doc ? renderMarkdown(doc) : '<p class="placeholder">Documentation is not available for this assessment.</p>';
}

function updateAssessmentStatsUI(stats = null) {
  const totalAnswered = stats?.total_answered ?? assessmentAnsweredCountValue;
  const totalCorrect = stats?.total_correct ?? assessmentCorrectCountValue;
  const pct = stats?.percentage_correct ?? (totalAnswered ? (totalCorrect / totalAnswered) * 100 : 0);
  if (assessmentCorrectCount) assessmentCorrectCount.textContent = String(totalCorrect);
  if (assessmentAnsweredCount) assessmentAnsweredCount.textContent = String(totalAnswered);
  if (assessmentPercentCorrect) assessmentPercentCorrect.textContent = `${Math.round(pct)}%`;
}

async function fetchAssessmentStats() {
  try {
    const response = await fetch(apiUrl("/assessments/stats"), {
      headers: authHeaders({ Accept: "application/json" })
    });
    const data = await response.json().catch(() => ({}));
    if (response.ok) updateAssessmentStatsUI(data);
  } catch {
    updateAssessmentStatsUI();
  }
}

function renderAssessmentQuestion() {
  const question = currentAssessmentQuestion();
  assessmentSummaryVisible = false;
  selectedAssessmentChoice = question ? (assessmentSelectedChoices.get(String(question.id)) || "") : "";
  if (assessmentNextButton) {
    assessmentNextButton.textContent = "Next question";
    assessmentNextButton.disabled = !question || !answeredAssessmentQuestions.has(question.id);
    assessmentNextButton.classList.remove("assessment-next-ready");
  }
  if (!question) {
    if (assessmentQuestionText) assessmentQuestionText.textContent = "No questions are available for this assessment.";
    if (assessmentChoiceList) assessmentChoiceList.innerHTML = "";
    if (assessmentProgressText) assessmentProgressText.textContent = "Question 0 of 0";
    if (assessmentProgressBar) assessmentProgressBar.style.width = "0%";
    return;
  }
  const total = currentAssessment.questions.length;
  if (assessmentProgressText) assessmentProgressText.textContent = `${currentAssessment.documentation_title || "Documentation"} - Question ${currentAssessmentQuestionIndex + 1} of ${total}`;
  if (assessmentProgressBar) assessmentProgressBar.style.width = `${((currentAssessmentQuestionIndex + 1) / Math.max(total, 1)) * 100}%`;
  if (assessmentQuestionText) assessmentQuestionText.textContent = question.question;
  if (assessmentChoiceList) {
    assessmentChoiceList.innerHTML = Object.entries(question.choices || {}).map(([key, value]) => `
      <button type="button" class="assessment-choice ${selectedAssessmentChoice === key ? "is-selected" : ""}" data-assessment-choice="${escapeHtml(key)}">
        <span>${escapeHtml(key)}</span>
        <strong>${escapeHtml(value)}</strong>
      </button>
    `).join("");
  }
  const storedResult = assessmentAnswerResults.get(String(question.id));
  if (storedResult) {
    assessmentChoiceList?.querySelectorAll(".assessment-choice").forEach((button) => {
      const selected = button.dataset.assessmentChoice === storedResult.selected_choice;
      const correct = button.dataset.assessmentChoice === storedResult.correct_response;
      button.classList.toggle("is-correct", correct);
      button.classList.toggle("is-incorrect", selected && !correct);
      button.classList.toggle("is-feedback-selected", selected);
      button.disabled = true;
    });
    renderAssessmentFeedback(question, storedResult, { scroll: false });
  }
  if (assessmentMessage) assessmentMessage.textContent = answeredAssessmentQuestions.has(question.id)
    ? "You already answered this one. Move to the next question when ready."
    : "Choose the best answer using only the documentation and source reference.";
  if (assessmentSubmitButton) assessmentSubmitButton.disabled = answeredAssessmentQuestions.has(question.id);
  if (assessmentNextButton && answeredAssessmentQuestions.has(question.id)) {
    assessmentNextButton.textContent = answeredAssessmentQuestions.size >= total ? "View summary" : "Next question";
    assessmentNextButton.disabled = false;
    assessmentNextButton.classList.add("assessment-next-ready");
  }
}

function renderAssessmentFeedback(question, result, options = {}) {
  const selectedKey = result.selected_choice || selectedAssessmentChoice;
  const correctKey = result.correct_response || question.correct_response || "";
  const selectedText = question.choices?.[selectedKey] || "";
  const correctText = question.choices?.[correctKey] || "";
  const explanation = result.explanation || question.explanation || "";
  const feedback = document.createElement("article");
  feedback.className = `assessment-feedback-card ${result.is_correct ? "is-correct" : "is-incorrect"}`;
  feedback.innerHTML = `
    <div class="assessment-feedback-head">
      <span>${result.is_correct ? "Correct" : "Review this one"}</span>
      <strong>${result.is_correct ? "Nice work." : `Correct answer: ${escapeHtml(correctKey)}`}</strong>
    </div>
    <div class="assessment-feedback-grid">
      <p>
        <span>Your choice</span>
        <code>${escapeHtml(selectedKey)}</code>
        ${selectedText ? escapeHtml(selectedText) : ""}
      </p>
      <p>
        <span>Correct choice</span>
        <code>${escapeHtml(correctKey)}</code>
        ${correctText ? escapeHtml(correctText) : ""}
      </p>
    </div>
    ${explanation ? `<p class="assessment-feedback-explanation">${escapeHtml(explanation)}</p>` : ""}
  `;
  assessmentChoiceList?.appendChild(feedback);
  if (options.scroll !== false) feedback.scrollIntoView({ block: "nearest", behavior: "smooth" });
}

function renderAssessmentSummary() {
  assessmentSummaryVisible = true;
  const total = currentAssessment?.questions?.length || 0;
  const correct = assessmentCorrectCountValue;
  const percent = total ? Math.round((correct / total) * 100) : 0;
  if (assessmentProgressText) assessmentProgressText.textContent = "Assessment complete";
  if (assessmentProgressBar) assessmentProgressBar.style.width = "100%";
  if (assessmentQuestionText) assessmentQuestionText.textContent = "Summary";
  if (assessmentChoiceList) {
    assessmentChoiceList.innerHTML = `
      <div class="assessment-summary-card">
        <strong>${correct} / ${total} correct</strong>
        <span>${percent}% score</span>
        <p>You answered every question for ${escapeHtml(currentAssessment?.documentation_title || "this documentation sample")}.</p>
      </div>
    `;
  }
  if (assessmentMessage) assessmentMessage.textContent = "Start a new assessment when you are ready.";
  if (assessmentSubmitButton) assessmentSubmitButton.disabled = true;
  if (assessmentNextButton) {
    assessmentNextButton.textContent = "Start new assessment";
    assessmentNextButton.disabled = false;
  }
  saveCurrentAssessmentSession();
}

function renderAssessmentDocumentationOptions() {
  if (!assessmentDocSelect) return;
  const selected = activeAssessmentDocumentationId || "";
  const remaining = assessmentDocumentationOptions.filter((option) => !option.attempted).length;
  const total = assessmentDocumentationOptions.length;
  assessmentDocSelect.innerHTML = `
    <option value="">Random remaining documentation</option>
    ${assessmentDocumentationOptions.map((option) => `
      <option value="${escapeHtml(String(option.documentation_id))}" ${String(option.documentation_id) === String(selected) ? "selected" : ""}>
        ${escapeHtml(option.documentation_title || "Untitled documentation")} (${option.question_count} questions${option.attempted ? ", completed" : ""})
      </option>
    `).join("")}
  `;
  if (assessmentDocRemaining) {
    assessmentDocRemaining.textContent = total
      ? `${remaining} of ${total} documentation sets remaining in random mode.`
      : "No documentation sets with questions are available yet.";
  }
}

async function loadAssessmentDocumentationOptions() {
  if (!assessmentDocSelect || !getAccessToken()) return;
  try {
    const response = await fetch(apiUrl("/assessments/documentation-options"), {
      headers: authHeaders({ Accept: "application/json" })
    });
    const data = await response.json().catch(() => []);
    if (!response.ok) throw new Error(data.detail || data.error || "Could not load documentation options.");
    assessmentDocumentationOptions = Array.isArray(data) ? data : [];
    renderAssessmentDocumentationOptions();
  } catch {
    assessmentDocumentationOptions = [];
    renderAssessmentDocumentationOptions();
  }
}

async function loadAssessment(documentationId = activeAssessmentDocumentationId, options = {}) {
  saveCurrentAssessmentSession();
  const docType = selectedAssessmentDocType();
  const requestedDocumentationId = documentationId || "";
  const cachedSession = assessmentSessionCache.get(assessmentSessionKey(requestedDocumentationId, docType));
  if (options.forceNew) {
    assessmentSessionCache.delete(assessmentSessionKey(requestedDocumentationId, docType));
  }
  if (!options.forceNew && cachedSession) {
    restoreAssessmentSession(cachedSession);
    if (assessmentMessage) assessmentMessage.textContent = "Restored your saved quiz progress for this documentation version.";
    return;
  }
  if (assessmentMessage) assessmentMessage.textContent = "Loading comprehension practice...";
  if (assessmentSubmitButton) assessmentSubmitButton.disabled = true;
  if (assessmentNextButton) assessmentNextButton.disabled = true;
  try {
    const endpointPath = documentationId
      ? `/assessments/documentation/${encodeURIComponent(documentationId)}/start`
      : "/assessments/random";
    const params = new URLSearchParams({ doc_type: docType });
    const endpoint = `${endpointPath}?${params.toString()}`;
    const response = await fetch(apiUrl(endpoint), {
      headers: authHeaders({ Accept: "application/json" })
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(response.status === 401 ? "Log in to load comprehension practice." : data.detail || "Could not load an assessment.");
    }
    currentAssessment = data;
    activeAssessmentDocType = docType;
    currentAssessmentQuestionIndex = 0;
    answeredAssessmentQuestions = new Set();
    assessmentSelectedChoices = new Map();
    assessmentAnswerResults = new Map();
    assessmentAnsweredCountValue = 0;
    assessmentCorrectCountValue = 0;
    assessmentSummaryVisible = false;
    activeAssessmentDocumentationId = documentationId ? String(documentationId) : "";
    if (assessmentDocSelect) assessmentDocSelect.value = activeAssessmentDocumentationId;
    currentAssessmentDoc = await fetchAssessmentDocumentation(data.documentation_id);
    activeAssessmentResource = "documentation";
    renderAssessmentResource();
    renderAssessmentQuestion();
    updateAssessmentStatsUI();
    fetchAssessmentStats();
    loadAssessmentDocumentationOptions();
  } catch (error) {
    currentAssessment = null;
    if (assessmentQuestionText) assessmentQuestionText.textContent = "Could not load comprehension practice";
    if (assessmentChoiceList) assessmentChoiceList.innerHTML = "";
    if (assessmentMessage) assessmentMessage.textContent = error.message || "Could not load assessment.";
  } finally {
    if (assessmentSubmitButton) assessmentSubmitButton.disabled = !currentAssessmentQuestion();
  }
}

function selectAssessmentChoice(choice) {
  const question = currentAssessmentQuestion();
  if (question && answeredAssessmentQuestions.has(question.id)) {
    if (assessmentMessage) assessmentMessage.textContent = "This answer is locked. Continue to the next question.";
    return;
  }
  selectedAssessmentChoice = choice;
  if (question) assessmentSelectedChoices.set(String(question.id), choice);
  assessmentChoiceList?.querySelectorAll(".assessment-choice").forEach((button) => {
    button.classList.toggle("is-selected", button.dataset.assessmentChoice === choice);
  });
  if (assessmentMessage) assessmentMessage.textContent = "Answer selected. Check it when you are ready.";
  saveCurrentAssessmentSession();
}

async function submitAssessmentAnswer() {
  const question = currentAssessmentQuestion();
  if (!currentAssessment || !question) return;
  if (!selectedAssessmentChoice) {
    if (assessmentMessage) assessmentMessage.textContent = "Choose an answer first.";
    return;
  }
  if (answeredAssessmentQuestions.has(question.id)) {
    moveAssessmentQuestion(1);
    return;
  }
  if (assessmentSubmitButton) assessmentSubmitButton.disabled = true;
  try {
    const response = await fetch(apiUrl("/assessments/submit"), {
      method: "POST",
      headers: authHeaders({ "Content-Type": "application/json", Accept: "application/json" }),
      body: JSON.stringify({
        attempt_id: currentAssessment.attempt_id,
        question_id: question.id,
        user_response: selectedAssessmentChoice,
        user_id: 0
      })
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(response.status === 409 ? "You already answered this question." : data.detail || "Could not submit answer.");
    }
    answeredAssessmentQuestions.add(question.id);
    assessmentSelectedChoices.set(String(question.id), selectedAssessmentChoice);
    const storedResult = {
      ...data,
      selected_choice: selectedAssessmentChoice,
      correct_response: data.correct_response || question.correct_response || "",
      explanation: data.explanation || question.explanation || ""
    };
    assessmentAnswerResults.set(String(question.id), storedResult);
    assessmentAnsweredCountValue += 1;
    if (data.is_correct) assessmentCorrectCountValue += 1;
    updateAssessmentStatsUI();
    const total = currentAssessment.questions.length;
    if (assessmentProgressText) {
      assessmentProgressText.textContent = `Answered ${answeredAssessmentQuestions.size} of ${total} - Question ${currentAssessmentQuestionIndex + 1}`;
    }
    if (assessmentProgressBar) {
      assessmentProgressBar.style.width = `${(answeredAssessmentQuestions.size / Math.max(total, 1)) * 100}%`;
    }
    assessmentChoiceList?.querySelectorAll(".assessment-choice").forEach((button) => {
      const selected = button.dataset.assessmentChoice === selectedAssessmentChoice;
      const correct = button.dataset.assessmentChoice === data.correct_response;
      button.classList.toggle("is-correct", correct);
      button.classList.toggle("is-incorrect", selected && !correct);
      button.classList.toggle("is-feedback-selected", selected);
      button.disabled = true;
    });
    const assessmentCard = document.querySelector(".assessment-card");
    assessmentCard?.classList.add(data.is_correct ? "assessment-feedback-correct" : "assessment-feedback-incorrect");
    window.setTimeout(() => {
      assessmentCard?.classList.remove("assessment-feedback-correct", "assessment-feedback-incorrect");
    }, 900);
    if (assessmentMessage) assessmentMessage.textContent = data.is_correct
      ? "Correct. Press Next question when you are ready."
      : `Not quite. Correct answer: ${data.correct_response}. ${data.explanation || ""} Press Next question when you are ready.`;
    renderAssessmentFeedback(question, storedResult);
    if (assessmentNextButton) {
      assessmentNextButton.textContent = answeredAssessmentQuestions.size >= total ? "View summary" : "Next question";
      assessmentNextButton.disabled = false;
      assessmentNextButton.classList.add("assessment-next-ready");
      assessmentNextButton.focus({ preventScroll: true });
    }
    fetchAssessmentStats();
    refreshAccountDataSoon(0);
    saveCurrentAssessmentSession();
  } catch (error) {
    if (assessmentMessage) assessmentMessage.textContent = error.message || "Could not submit answer.";
  } finally {
    if (assessmentSubmitButton) assessmentSubmitButton.disabled = answeredAssessmentQuestions.has(question.id);
  }
}

function moveAssessmentQuestion(direction) {
  if (!currentAssessment?.questions?.length) return;
  if (assessmentSummaryVisible) {
    loadAssessment(activeAssessmentDocumentationId, { forceNew: true });
    return;
  }
  const question = currentAssessmentQuestion();
  if (question && !answeredAssessmentQuestions.has(question.id)) {
    if (assessmentMessage) assessmentMessage.textContent = "Answer this question before moving on.";
    return;
  }
  const total = currentAssessment.questions.length;
  if (answeredAssessmentQuestions.size >= total && direction > 0) {
    renderAssessmentSummary();
    return;
  }
  currentAssessmentQuestionIndex = (currentAssessmentQuestionIndex + direction + total) % total;
  renderAssessmentQuestion();
  saveCurrentAssessmentSession();
}

function selectAreaWinner(winner) {
  if (areaVoteSubmitted) {
    if (areaVoteMessage) areaVoteMessage.textContent = "This comparison is locked after voting. Continue to the next comparison.";
    return;
  }
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
    markAreaComparisonCompleted(post?.id || post?.title || activeAreaIndex);
    incrementAreaRankCount();
    renderAreaPost();
    return;
  }
  if (areaVoteButton) areaVoteButton.disabled = true;
  areaVoteButton?.classList.add("is-submitting");
  if (areaVoteMessage) {
    areaVoteMessage.className = "area-vote-message is-submitting";
    areaVoteMessage.textContent = "Recording blind preference in the study database...";
  }
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
    markAreaComparisonCompleted(post.id);
    incrementAreaRankCount();
    renderAreaPost();
    areaVoteButton?.classList.remove("is-submitting");
    areaVoteButton?.classList.add("is-success");
    if (areaVoteMessage) {
      areaVoteMessage.className = "area-vote-message is-success";
      areaVoteMessage.textContent = `Vote saved. ${areaRankCountValue()} comparison${areaRankCountValue() === 1 ? "" : "s"} completed in this session.`;
    }
    window.setTimeout(() => areaVoteButton?.classList.remove("is-success"), 900);
    await fetchComparisonLeaderboard().catch(() => []);
    renderLandingLeaderboard();
  } catch (error) {
    areaVoteSubmitted = false;
    areaVoteButton?.classList.remove("is-submitting");
    areaVoteButton?.classList.add("is-error");
    if (areaVoteMessage) {
      areaVoteMessage.className = "area-vote-message is-error";
      areaVoteMessage.textContent = error.message || "Vote was not recorded.";
    }
    window.setTimeout(() => areaVoteButton?.classList.remove("is-error"), 900);
  } finally {
    if (areaVoteButton) areaVoteButton.disabled = false;
  }
}

function showNextAreaPost() {
  const completed = areaCompletedComparisonIds();
  const nextIndex = areaFallbackPosts.findIndex((post, index) => {
    if (index <= activeAreaIndex) return false;
    return !completed.has(String(post.id || post.title || index));
  });
  activeAreaIndex = nextIndex >= 0 ? nextIndex : 0;
  if (areaCommentInput) areaCommentInput.value = "";
  loadAreaComparison();
}

function updateAccountMenuLabel() {
  if (!accountMenuLabel) return;
  accountMenuLabel.textContent = getSavedUserEmail() || "Guest";
  const signedIn = Boolean(getAccessToken());
  loginAccountButtons.forEach((button) => {
    button.textContent = signedIn ? "Account" : "Login";
    button.dataset.authMode = signedIn ? "account" : "login";
  });
}

function cachedDatabaseStatusText() {
  try {
    return localStorage.getItem(DATABASE_STATUS_STORAGE_KEY) || "";
  } catch {
    return "";
  }
}

function cacheDatabaseStatusText(text) {
  try {
    localStorage.setItem(DATABASE_STATUS_STORAGE_KEY, text);
  } catch {
    // Ignore storage failures; the live status still renders.
  }
}

function showQueueStatus(label, state = "checking") {
  if (!databaseStatus || !databaseStatusText) return;
  databaseStatus.dataset.state = state;
  databaseStatusText.textContent = label;
}

async function refreshDatabaseStatus() {
  if (!databaseStatus || !databaseStatusText) return;
  window.clearTimeout(databaseStatusRetryTimer);
  databaseStatus.dataset.state = "checking";
  const cached = cachedDatabaseStatusText();
  databaseStatusText.textContent = cached
    ? `${cached} · checking...`
    : (API_BASE_URL ? "Checking cloud backend..." : "Checking local backend...");
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), API_BASE_URL ? 12000 : 5000);
  try {
    const response = await fetch(apiUrl("/api/status"), {
      cache: "no-store",
      signal: controller.signal
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok || !data.database?.connected) {
      throw new Error(data.database?.error || "Database unavailable");
    }
    const database = data.database;
    const queue = data.queue || {};
    databaseStatus.dataset.state = queue.connected === false ? "partial" : "connected";
    const environment = database.environment ? `${database.environment} ` : "";
    const fallback = database.using_local_fallback ? " fallback" : "";
    const databaseLabel = `${environment}${database.backend || "database"}${fallback}: ${database.name || "default"}`;
    const label = queue.connected === false ? `${databaseLabel} · Redis queue unavailable` : databaseLabel;
    databaseStatusText.textContent = label;
    cacheDatabaseStatusText(label);
    if (queue.connected === false) {
      databaseStatusRetryTimer = window.setTimeout(refreshDatabaseStatus, databaseStatusRetryDelay);
      databaseStatusRetryDelay = Math.min(databaseStatusRetryDelay + 3000, 15000);
    } else {
      databaseStatusRetryDelay = 5000;
    }
  } catch (error) {
    if (error?.name === "AbortError") {
      databaseStatus.dataset.state = "checking";
      databaseStatusText.textContent = API_BASE_URL
        ? "Cloud backend still waking up..."
        : "Local backend still checking...";
      databaseStatusRetryTimer = window.setTimeout(refreshDatabaseStatus, databaseStatusRetryDelay);
      databaseStatusRetryDelay = Math.min(databaseStatusRetryDelay + 3000, 15000);
      return;
    }
    databaseStatus.dataset.state = "checking";
    databaseStatusText.textContent = `${error.message || "Backend unavailable"} · retrying`;
    databaseStatusRetryTimer = window.setTimeout(refreshDatabaseStatus, databaseStatusRetryDelay);
    databaseStatusRetryDelay = Math.min(databaseStatusRetryDelay + 3000, 15000);
  } finally {
    window.clearTimeout(timeoutId);
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

const PYTHON_KEYWORDS = new Set([
  "and", "as", "assert", "async", "await", "break", "class", "continue", "def", "del",
  "elif", "else", "except", "False", "finally", "for", "from", "global", "if", "import",
  "in", "is", "lambda", "None", "nonlocal", "not", "or", "pass", "raise", "return",
  "True", "try", "while", "with", "yield"
]);

const PYTHON_BUILTINS = new Set([
  "abs", "all", "any", "bool", "bytes", "callable", "dict", "dir", "enumerate", "filter",
  "float", "format", "getattr", "hasattr", "int", "isinstance", "issubclass", "len", "list",
  "map", "max", "min", "next", "object", "open", "print", "range", "repr", "reversed",
  "round", "set", "slice", "sorted", "str", "sum", "super", "tuple", "type", "zip"
]);

function wrapSyntax(className, value) {
  return `<span class="syntax-${className}">${escapeHtml(value)}</span>`;
}

function readPythonString(source, start) {
  const quote = source[start];
  const triple = source.slice(start, start + 3) === quote.repeat(3);
  let index = start + (triple ? 3 : 1);
  while (index < source.length) {
    if (source[index] === "\\") {
      index += 2;
      continue;
    }
    if (triple && source.slice(index, index + 3) === quote.repeat(3)) {
      return source.slice(start, index + 3);
    }
    if (!triple && source[index] === quote) {
      return source.slice(start, index + 1);
    }
    index += 1;
  }
  return source.slice(start);
}

function highlightPythonCode(source) {
  let html = "";
  let index = 0;
  let expectDefinitionName = false;
  const text = String(source || "");
  while (index < text.length) {
    const char = text[index];
    const previous = text[index - 1] || "";
    const next = text[index + 1] || "";

    if (char === "#") {
      const end = text.indexOf("\n", index);
      const comment = end === -1 ? text.slice(index) : text.slice(index, end);
      html += wrapSyntax("comment", comment);
      index += comment.length;
      continue;
    }

    const stringStart = char === "\"" || char === "'" || ((char === "r" || char === "u" || char === "b" || char === "f" || char === "R" || char === "U" || char === "B" || char === "F") && (next === "\"" || next === "'"));
    if (stringStart) {
      const prefixLength = char === "\"" || char === "'" ? 0 : 1;
      const stringValue = text.slice(index, index + prefixLength) + readPythonString(text, index + prefixLength);
      html += wrapSyntax("string", stringValue);
      index += stringValue.length;
      continue;
    }

    const numberMatch = /^\d+(?:\.\d+)?(?:e[+-]?\d+)?/i.exec(text.slice(index));
    if (numberMatch && !/[A-Za-z0-9_]/.test(previous)) {
      html += wrapSyntax("number", numberMatch[0]);
      index += numberMatch[0].length;
      continue;
    }

    const nameMatch = /^[A-Za-z_][A-Za-z0-9_]*/.exec(text.slice(index));
    if (nameMatch) {
      const name = nameMatch[0];
      const after = text.slice(index + name.length);
      if (expectDefinitionName) {
        html += wrapSyntax("definition", name);
        expectDefinitionName = false;
      } else if (PYTHON_KEYWORDS.has(name)) {
        html += wrapSyntax("keyword", name);
        expectDefinitionName = name === "def" || name === "class";
      } else if (/^\s*\(/.test(after)) {
        html += wrapSyntax("function", name);
      } else if (PYTHON_BUILTINS.has(name)) {
        html += wrapSyntax("builtin", name);
      } else {
        html += escapeHtml(name);
      }
      index += name.length;
      continue;
    }

    if ("+-*/%=<>!&|^~:.,()[]{}".includes(char)) {
      html += wrapSyntax("operator", char);
    } else if (char === "@" && /^[A-Za-z_]/.test(next)) {
      html += wrapSyntax("decorator", char);
    } else {
      html += escapeHtml(char);
    }
    index += 1;
  }
  return html;
}

function renderCodeBlock(code, language) {
  const normalizedLanguage = String(language || "").trim().toLowerCase();
  const languageClass = normalizedLanguage ? ` language-${escapeHtml(normalizedLanguage)}` : "";
  const highlighted = normalizedLanguage === "python" || normalizedLanguage === "py"
    ? highlightPythonCode(code)
    : escapeHtml(code);
  return `<pre class="md-code${languageClass}" data-language="${escapeHtml(normalizedLanguage || "code")}"><code class="${languageClass.trim()}">${highlighted}</code></pre>`;
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
      html.push(renderCodeBlock(codeLines.join("\n"), language));
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

function renderPythonMarkdown(source) {
  return renderMarkdown(["```python", String(source || ""), "```"].join("\n"));
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
  tdTab.classList.remove("is-hidden");
  tdTab.disabled = false;
  tdTab.setAttribute("aria-disabled", "false");
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
    ${doc.kind === "td" ? "" : `<section class="saved-invariants">
      <p class="eyebrow">Invariants used</p>
      <ul>${doc.invariants.map((invariant) => `<li>${escapeHtml(invariant)}</li>`).join("")}</ul>
    </section>`}
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
  const timestamp = createdAt.toISOString().slice(0, 19).replace(/[:T]/g, "-");
  const savedDocs = [{
    id: `saved-${doc.id}-ibd`,
    apiName,
    title: `${apiName} IBD`,
    markdown: doc.IBD_generated_md || "",
    invariants: parseStoredInvariants(doc.invariants),
    createdAt,
    filename: `${slugify(apiName)}-ibd-${timestamp}.md`,
    kind: "ibd"
  }];
  if (hasTraditionalDocumentation(doc)) {
    savedDocs.push({
      id: `saved-${doc.id}-td`,
      apiName,
      title: `${apiName} TD`,
      markdown: accountDocMarkdown(doc, "td"),
      invariants: [],
      createdAt,
      filename: `${slugify(apiName)}-td-${timestamp}.md`,
      kind: "td"
    });
  }
  const savedIds = new Set(savedDocs.map((item) => item.id));
  generatedDocs = [...savedDocs, ...generatedDocs.filter((item) => !savedIds.has(item.id))].slice(0, 12);
  activeGeneratedDocId = savedDocs[0].id;
  renderGeneratedDocsLibrary();
  resetGeneratedDocsInactivityTimer();
  showGeneratedDoc(savedDocs[0].id);
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
      doc.TD_md,
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
        ${hasTraditionalDocumentation(doc) ? '<span class="saved-doc-badge">TD available</span>' : ""}
      </button>
    `;
  }).join("");
}

async function fetchSavedDocs({ retry = true } = {}) {
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
    if (savedDocList) savedDocList.innerHTML = `<p class="placeholder">${escapeHtml(error.message || "Could not load saved Markdown.")}${retry ? " Retrying..." : ""}</p>`;
    if (retry) window.setTimeout(() => fetchSavedDocs({ retry: false }), 5000);
  }
}

// ----- Account page -----
let accountDocuments = [];
let activeAccountDoc = null;
let accountSort = "created-desc";
let accountConfirmPhrase = "";
let accountCurrentUserId = null;
let accountIsAdmin = false;
let activeAccountQuestions = [];
let activeAccountAnswers = [];

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

function updateAccountDocsScopeUi() {
  if (accountRole) {
    accountRole.textContent = accountIsAdmin ? "Admin account" : "Normal user";
    accountRole.dataset.role = accountIsAdmin ? "admin" : "user";
  }
  if (accountDocsTitle) accountDocsTitle.textContent = accountIsAdmin ? "All generated documents" : "Your documents";
  if (accountDocsScope) {
    accountDocsScope.textContent = accountIsAdmin
      ? "Admin view: every saved documentation row is available for assessment generation."
      : "Saved documentation generated by your account.";
  }
  accountAdminActions?.classList.toggle("is-hidden", !accountIsAdmin);
  updateAdminResetTargetUi();
}

function updateAdminResetTargetUi() {
  const target = accountResetTarget?.value || "all";
  accountResetLookupField?.classList.toggle("is-hidden", target === "all");
  if (accountResetLookup) {
    accountResetLookup.placeholder = target === "email" ? "participant@example.com" : "42";
    accountResetLookup.inputMode = target === "id" ? "numeric" : "text";
  }
}

function refreshAccountDataSoon(delay = 120) {
  if (!getAccessToken()) return;
  window.clearTimeout(accountRefreshTimer);
  accountRefreshTimer = window.setTimeout(() => {
    fetchSavedDocs();
    fetchAccountProfile().finally(() => fetchAccountDocs());
    if (activeAreaMode === "comprehension") {
      loadAssessmentDocumentationOptions();
    }
  }, delay);
}

function logoutCurrentUser() {
  localStorage.removeItem(ACCESS_TOKEN_STORAGE_KEY);
  localStorage.removeItem(USER_EMAIL_STORAGE_KEY);
  savedDocumentation = [];
  accountDocuments = [];
  accountCurrentUserId = null;
  accountIsAdmin = false;
  updateAccountDocsScopeUi();
  updateAssessmentDocTypeControl();
  updateAccountMenuLabel();
  renderSavedDocs();
  setStatus("draft", "Signed out");
  showLandingPage();
}

async function refreshAccountAdminState() {
  accountIsAdmin = false;
  if (!getAccessToken()) {
    updateAccountDocsScopeUi();
    updateAssessmentDocTypeControl();
    return false;
  }
  try {
    const response = await fetch(apiUrl("/users/me/admin"), {
      headers: authHeaders({ Accept: "application/json" })
    });
    accountIsAdmin = response.ok;
  } catch {
    accountIsAdmin = false;
  }
  updateAccountDocsScopeUi();
  updateAssessmentDocTypeControl();
  return accountIsAdmin;
}

function updateAssessmentDocTypeControl() {
  const wrapper = assessmentDocTypeSelect?.closest(".assessment-doc-type-picker");
  if (!assessmentDocTypeSelect || !wrapper) return;
  wrapper.classList.toggle("is-hidden", !accountIsAdmin);
  assessmentDocTypeSelect.disabled = !accountIsAdmin;
  if (!accountIsAdmin) assessmentDocTypeSelect.value = "random";
}

function canManageAccountDoc(doc) {
  if (accountIsAdmin) return true;
  return accountCurrentUserId != null && String(doc?.owner_id) === String(accountCurrentUserId);
}

function setDeleteConfirmPhrase(email) {
  accountConfirmPhrase = (email || "").trim();
  if (deleteConfirmPhrase) deleteConfirmPhrase.textContent = accountConfirmPhrase || "your email";
  if (deleteConfirmInput) deleteConfirmInput.placeholder = accountConfirmPhrase || "";
  updateDeleteConfirmState();
}

async function fetchAccountProfile() {
  if (!getAccessToken() || !accountEmail) return;
  accountCurrentUserId = null;
  accountEmail.textContent = getSavedUserEmail() || "—";
  accountCreated.textContent = "—";
  accountId.textContent = "—";
  setDeleteConfirmPhrase(getSavedUserEmail());
  try {
    const response = await fetch(apiUrl("/users/me"), { headers: authHeaders({ Accept: "application/json" }) });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || data.error || "Could not load profile.");
    accountCurrentUserId = data.id ?? null;
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

function hasTraditionalDocumentation(doc) {
  return Boolean(String(doc?.TD_md || doc?.td_doc || doc?.td_markdown || "").trim());
}

function accountDocMarkdown(doc, type = "ibd") {
  if (type === "td") return String(doc?.TD_md || doc?.td_doc || doc?.td_markdown || "");
  return String(doc?.IBD_generated_md || doc?.ibd_doc || doc?.ibd_markdown || "");
}

function renderAccountMarkdownViewer(doc, canManage, activeKind = "ibd") {
  const ibdMarkdown = accountDocMarkdown(doc, "ibd");
  const tdMarkdown = accountDocMarkdown(doc, "td");
  const hasTD = Boolean(tdMarkdown.trim());
  const selectedKind = activeKind === "td" && hasTD ? "td" : "ibd";
  const selectedMarkdown = selectedKind === "td" ? tdMarkdown : ibdMarkdown;
  return `
    <section class="account-detail-section">
      <div class="account-detail-md-head">
        <div>
          <p class="eyebrow">Documentation Markdown</p>
          <h3>Invariant-based and traditional documentation</h3>
        </div>
        <div class="account-detail-md-actions">
          <button type="button" class="secondary-button account-md-download" data-doc-kind="ibd">Download IBD .md</button>
          ${hasTD ? '<button type="button" class="secondary-button account-md-download" data-doc-kind="td">Download TD .md</button>' : ""}
          ${canManage ? '<button type="button" class="secondary-button" id="account-md-edit">Edit IBD</button>' : ""}
          ${canManage ? '<button type="button" class="secondary-button" id="account-td-edit">Add/Edit TD</button>' : ""}
          ${canManage ? '<button type="button" class="danger-button" id="account-md-delete">Delete</button>' : ""}
        </div>
      </div>
      <p class="account-message" id="account-md-message"></p>
      <div class="account-doc-kind-tabs" role="tablist" aria-label="Documentation versions">
        <button type="button" class="account-doc-kind-tab ${selectedKind === "ibd" ? "is-active" : ""}" data-doc-kind="ibd" role="tab" aria-selected="${selectedKind === "ibd" ? "true" : "false"}">IBD Markdown</button>
        <button type="button" class="account-doc-kind-tab ${selectedKind === "td" ? "is-active" : ""}" data-doc-kind="td" role="tab" aria-selected="${selectedKind === "td" ? "true" : "false"}" ${hasTD ? "" : "disabled"}>Traditional Markdown</button>
      </div>
      <div class="markdown-rendered account-detail-markdown" id="account-detail-markdown">${selectedMarkdown ? renderMarkdown(selectedMarkdown) : `<p class="placeholder">No ${selectedKind.toUpperCase()} Markdown stored.</p>`}</div>
      <div class="account-detail-md-editor is-hidden" id="account-detail-md-editor" data-doc-kind="ibd">
        <textarea id="account-md-textarea" rows="16" spellcheck="false"></textarea>
        <div class="account-detail-md-editor-actions">
          <button type="button" class="landing-primary-button" id="account-md-save">Save changes</button>
          <button type="button" class="secondary-button" id="account-md-cancel">Cancel</button>
        </div>
      </div>
      <div class="account-detail-md-editor is-hidden" id="account-detail-td-editor">
        <textarea id="account-td-textarea" rows="16" spellcheck="false" placeholder="Paste traditional/reference documentation Markdown here."></textarea>
        <div class="account-detail-md-editor-actions">
          <button type="button" class="landing-primary-button" id="account-td-save">Save TD Markdown</button>
          <button type="button" class="secondary-button" id="account-td-cancel">Cancel</button>
        </div>
      </div>
    </section>
  `;
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
    accountDocsList.innerHTML = accountIsAdmin
      ? '<p class="placeholder">No generated documentation rows exist yet.</p>'
      : '<p class="placeholder">No generated documents yet. Run the generator to create one.</p>';
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
    const canManage = canManageAccountDoc(doc);
    const hasTD = hasTraditionalDocumentation(doc);
    const questionCount = Number(doc.question_count || 0);
    const responseCount = Number(doc.response_count || 0);
    const questionsLabel = questionCount ? `Questions (${questionCount})` : "No questions generated";
    const responsesLabel = responseCount
      ? (accountIsAdmin ? `View responses (${responseCount})` : `My responses (${responseCount})`)
      : "No responses yet";
    return `
      <article class="account-doc-card">
        <div class="account-doc-info">
          <strong>${escapeHtml(doc.documentation_title || "Untitled documentation")}</strong>
          <small>${escapeHtml(formatAccountDate(doc.created_at))}</small>
          <div class="account-doc-pills">
            ${accountIsAdmin ? `<span>Owner #${escapeHtml(String(doc.owner_id ?? "—"))}</span>` : ""}
            <span>Soundness ${formatPercentMaybe(doc.soundness)}</span>
            <span>Validity ${formatPercentMaybe(doc.validity)}</span>
            <span>Mutation ${formatPercentMaybe(doc.mutation_score)}</span>
            <span>${invariants.length} invariants</span>
            <span class="${questionCount ? "account-doc-pill-ready" : "account-doc-pill-muted"}">${questionCount ? `${questionCount} questions` : "No questions"}</span>
            <span class="${responseCount ? "account-doc-pill-ready" : "account-doc-pill-muted"}">${responseCount ? `${responseCount} responses` : "No responses"}</span>
            <span>${comparisonCount} arena votes</span>
            <span class="${hasTD ? "account-doc-pill-ready" : "account-doc-pill-muted"}">${hasTD ? "Traditional doc" : "No TD yet"}</span>
            ${comparisonCount ? `<span>${ibdPct}% invariant-based preference</span>` : ""}
          </div>
        </div>
        <div class="account-doc-actions">
          ${accountIsAdmin ? `<button type="button" class="${questionCount ? "landing-primary-button" : "secondary-button"} account-doc-questions" data-doc-id="${doc.id}">${questionsLabel}</button>` : ""}
          <button type="button" class="secondary-button account-doc-responses" data-doc-id="${doc.id}" ${responseCount ? "" : "disabled"}>${responsesLabel}</button>
          ${accountIsAdmin ? `<button type="button" class="secondary-button account-doc-retake" data-doc-id="${doc.id}">Retake access</button>` : ""}
          ${accountIsAdmin ? `<button type="button" class="danger-button account-doc-reset-questions" data-doc-id="${doc.id}">Reset questions</button>` : ""}
          <button type="button" class="secondary-button account-doc-view" data-doc-kind="ibd" data-doc-id="${doc.id}">View IBD</button>
          <button
            type="button"
            class="secondary-button account-doc-view"
            data-doc-kind="td"
            data-doc-action="${hasTD ? "view" : "add-td"}"
            data-doc-id="${doc.id}"
            ${hasTD || canManage ? "" : "disabled"}
          >${hasTD ? "View TD" : "Missing TD"}</button>
          ${canManage ? `<button type="button" class="danger-button account-doc-delete" data-doc-id="${doc.id}">Delete</button>` : ""}
        </div>
      </article>
    `;
  }).join("");
}

async function fetchAccountDocs({ retry = true } = {}) {
  if (!getAccessToken()) {
    renderAccountDocs();
    return;
  }
  if (accountDocsList) accountDocsList.innerHTML = '<p class="placeholder">Loading your documents…</p>';
  try {
    const isAdmin = await refreshAccountAdminState();
    if (accountDocsList) accountDocsList.innerHTML = `<p class="placeholder">Loading ${isAdmin ? "all generated documents" : "your documents"}…</p>`;
    const response = await fetch(apiUrl(isAdmin ? "/documentation/" : "/documentation/me"), { headers: authHeaders({ Accept: "application/json" }) });
    const data = await response.json().catch(() => []);
    if (!response.ok) throw new Error(data.detail || data.error || "Could not load documents.");
    accountDocuments = Array.isArray(data) ? data : [];
    await mergeAssessmentCountsIntoAccountDocs();
    await fetchComparisonLeaderboard().catch(() => []);
    if (accountDocCount) accountDocCount.textContent = String(accountDocuments.length);
    renderAccountStats();
    renderAccountDocs();
  } catch (error) {
    if (accountDocsList) accountDocsList.innerHTML = `<p class="placeholder">${escapeHtml(error.message || "Could not load documents.")}${retry ? " Retrying..." : ""}</p>`;
    if (retry) window.setTimeout(() => fetchAccountDocs({ retry: false }), 5000);
  }
}

async function mergeAssessmentCountsIntoAccountDocs() {
  if (!getAccessToken() || !accountDocuments.length) return;
  try {
    const response = await fetch(apiUrl("/assessments/documentation-options"), {
      headers: authHeaders({ Accept: "application/json" })
    });
    const data = await response.json().catch(() => []);
    if (!response.ok || !Array.isArray(data)) return;
    const countsById = new Map(data.map((item) => [String(item.documentation_id), item]));
    accountDocuments = accountDocuments.map((doc) => {
      const counts = countsById.get(String(doc.id));
      if (!counts) return { ...doc, question_count: Number(doc.question_count || 0), response_count: Number(doc.response_count || 0) };
      return {
        ...doc,
        question_count: Number(counts.question_count || doc.question_count || 0),
        response_count: Number(counts.response_count || doc.response_count || 0)
      };
    });
  } catch {
    // Keep the base document response; counts are display-only.
  }
}

function showAccountDocDetail(docId, initialKind = "ibd") {
  const doc = accountDocuments.find((item) => String(item.id) === String(docId));
  if (!doc || !accountDetailModal) return;
  activeAccountDoc = doc;
  const invariants = parseStoredInvariants(doc.invariants);
  const metrics = parseStoredMetrics(doc.hypothesis_tests);
  const canManage = canManageAccountDoc(doc);
  accountDetailTitle.textContent = doc.documentation_title || "Document";
  accountDetailEyebrow.textContent = `Generated ${formatAccountDate(doc.created_at)}`;
  accountDetailBody.innerHTML = `
    <section class="account-detail-section">
      <p class="eyebrow">Overview</p>
      <dl class="account-detail-meta">
        <div><dt>Name</dt><dd>${escapeHtml(doc.documentation_title || "—")}</dd></div>
        <div><dt>Generated</dt><dd>${escapeHtml(formatAccountDate(doc.created_at))}</dd></div>
        ${accountIsAdmin ? `<div><dt>Owner</dt><dd>#${escapeHtml(String(doc.owner_id ?? "—"))}</dd></div>` : ""}
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
              ${metric.test_code ? renderPythonMarkdown(metric.test_code) : ""}
            </details>
          `).join("")}
        </div>
      </section>
    ` : ""}
    ${renderAccountRankingSummary(doc)}
    ${renderAccountMarkdownViewer(doc, canManage, initialKind)}
  `;
  accountDetailModal.classList.remove("is-hidden");
  document.body.classList.add("account-detail-open");
  accountDetailClose?.focus();
}

function showAccountQuestionBuilder(docId) {
  const doc = accountDocuments.find((item) => String(item.id) === String(docId));
  if (!doc || !accountDetailModal) return;
  activeAccountDoc = doc;
  activeAccountAssessmentTab = "questions";
  activeAccountResponseUserFilter = "all";
  accountDetailTitle.textContent = "Question builder";
  accountDetailEyebrow.textContent = doc.documentation_title || "Selected documentation";
  accountDetailBody.innerHTML = `
    <section class="account-question-builder">
      <div class="account-question-head">
        <div>
          <p class="eyebrow">Admin assessment</p>
          <h3>Questions for this documentation</h3>
          <p>Write a human-authored comprehension question for <strong>${escapeHtml(doc.documentation_title || "this documentation")}</strong>, or use the smaller AI generator tab for drafts.</p>
        </div>
      </div>

      <section class="account-human-question-panel" aria-labelledby="human-question-title">
        <div class="account-question-section-head">
          <div>
            <p class="eyebrow">Human input</p>
            <h4 id="human-question-title">Add a question</h4>
          </div>
        </div>
        <label class="field" for="manual-question-text">
          <span>Question</span>
          <textarea id="manual-question-text" rows="4" placeholder="Ask a comprehension question about the selected documentation."></textarea>
        </label>
        <div class="manual-choice-grid">
          ${["A", "B", "C", "D"].map((choice) => `
            <label class="field" for="manual-choice-${choice}">
              <span>Choice ${choice}</span>
              <input id="manual-choice-${choice}" data-manual-choice="${choice}" type="text" placeholder="Answer ${choice}">
            </label>
          `).join("")}
        </div>
        <div class="manual-answer-row">
          <label class="field compact-field" for="manual-correct-response">
            <span>Correct</span>
            <select id="manual-correct-response">
              ${["A", "B", "C", "D"].map((choice) => `<option value="${choice}">${choice}</option>`).join("")}
            </select>
          </label>
          <label class="field" for="manual-explanation">
            <span>Explanation</span>
            <input id="manual-explanation" type="text" placeholder="Why this answer is correct">
          </label>
        </div>
        <div class="account-question-actions">
          <button type="button" class="landing-primary-button" id="account-manual-question-save">Save human question</button>
          <button type="button" class="secondary-button" id="account-question-refresh">Refresh questions</button>
          <p class="account-message" id="account-manual-question-message"></p>
        </div>
      </section>

      <section class="account-ai-generate-panel" id="account-ai-generate-panel">
        <div>
          <p class="eyebrow">AI generator</p>
          <h4>Generate a full question set</h4>
        </div>
        <div class="account-ai-question-grid">
          <label class="field compact-field" for="account-assessment-count">
            <span>Questions</span>
            <input id="account-assessment-count" type="number" min="1" max="30" value="10">
          </label>
          <label class="field compact-field" for="account-assessment-choices">
            <span>Choices</span>
            <input id="account-assessment-choices" type="number" min="2" max="6" value="4">
          </label>
          <label class="field compact-field" for="account-assessment-doc-type">
            <span>Docs</span>
            <select id="account-assessment-doc-type">
              <option value="random">Random</option>
              <option value="ibd">IBD</option>
              <option value="td" ${hasTraditionalDocumentation(doc) ? "" : "disabled"}>TD</option>
            </select>
          </label>
          <button type="button" class="landing-primary-button" id="account-assessment-generate">AI generate full set</button>
        </div>
        <p class="account-message" id="account-assessment-message">AI generation creates draft questions from the selected documentation version and adds them to this row.</p>
      </section>

      <section class="account-question-list-section">
        <div class="account-question-list-head">
          <div>
            <p class="eyebrow">Question bank</p>
            <h4 id="account-question-count">Questions</h4>
          </div>
          <button type="button" class="danger-button" id="account-question-reset-all">Reset all questions</button>
        </div>
        <div class="account-question-list" id="account-question-list">
          <p class="placeholder">Loading questions...</p>
        </div>
      </section>
    </section>
  `;
  accountDetailModal.classList.remove("is-hidden");
  document.body.classList.add("account-detail-open");
  accountDetailClose?.focus();
  loadAccountQuestions();
}

function showAccountResponses(docId) {
  const doc = accountDocuments.find((item) => String(item.id) === String(docId));
  if (!doc || !accountDetailModal) return;
  activeAccountDoc = doc;
  activeAccountResponseUserFilter = "all";
  accountDetailTitle.textContent = accountIsAdmin ? "User responses" : "My responses";
  accountDetailEyebrow.textContent = doc.documentation_title || "Selected documentation";
  accountDetailBody.innerHTML = `
    <section class="account-question-builder">
      <div class="account-question-head">
        <div>
          <p class="eyebrow">${accountIsAdmin ? "Admin responses" : "Assessment history"}</p>
          <h3>${accountIsAdmin ? "Assessment response summary" : "Your submitted answers"}</h3>
          <p>${accountIsAdmin ? "Review submitted answers, filter by all users or a specific user, and inspect each attempt without editing questions." : "Review your submitted answers, correct answers, and explanations for this documentation."}</p>
        </div>
      </div>
      <section class="account-response-dashboard">
        <div class="account-question-list-head">
          <div>
            <p class="eyebrow">${accountIsAdmin ? "User responses" : "Your responses"}</p>
            <h4 id="account-response-count">Response summary</h4>
          </div>
          <label class="field compact-field ${accountIsAdmin ? "" : "is-hidden"}" for="account-response-user-filter">
            <span>User</span>
            <select id="account-response-user-filter">
              <option value="all">All users</option>
            </select>
          </label>
        </div>
        <div id="account-response-summary">
          <p class="placeholder">Loading responses...</p>
        </div>
      </section>
    </section>
  `;
  accountDetailModal.classList.remove("is-hidden");
  document.body.classList.add("account-detail-open");
  accountDetailClose?.focus();
  if (accountIsAdmin) {
    loadAccountQuestions();
  } else {
    loadAccountUserResponses();
  }
}

function showAccountRetakeAccess(docId) {
  const doc = accountDocuments.find((item) => String(item.id) === String(docId));
  if (!doc || !accountDetailModal) return;
  activeAccountDoc = doc;
  activeAccountAnswers = [];
  accountDetailTitle.textContent = "Retake access";
  accountDetailEyebrow.textContent = doc.documentation_title || "Selected documentation";
  accountDetailBody.innerHTML = `
    <section class="account-question-builder">
      <div class="account-question-head">
        <div>
          <p class="eyebrow">Admin retake control</p>
          <h3>Allow another assessment attempt</h3>
          <p>This does not remove previous attempts or answers. It makes this documentation available again for the selected audience.</p>
        </div>
      </div>
      <section class="account-retake-panel">
        <label class="field" for="account-retake-scope">
          <span>Who can retake?</span>
          <select id="account-retake-scope">
            <option value="all">All users</option>
            <option value="user">Specific user</option>
          </select>
        </label>
        <div class="account-retake-user-fields is-hidden" id="account-retake-user-fields">
          <label class="field" for="account-retake-known-user">
            <span>Known respondents</span>
            <select id="account-retake-known-user">
              <option value="">Select a user who has answered</option>
            </select>
          </label>
          <label class="field" for="account-retake-user-lookup">
            <span>User ID or email</span>
            <input id="account-retake-user-lookup" type="text" placeholder="42 or participant@example.com">
          </label>
        </div>
        <div class="account-question-actions">
          <button type="button" class="landing-primary-button" id="account-retake-all">Allow all users to retake</button>
          <button type="button" class="landing-primary-button" id="account-retake-grant">Allow retake</button>
          <button type="button" class="secondary-button" id="account-retake-refresh-users">Refresh users</button>
          <p class="account-message" id="account-retake-message"></p>
        </div>
      </section>
    </section>
  `;
  accountDetailModal.classList.remove("is-hidden");
  document.body.classList.add("account-detail-open");
  accountDetailClose?.focus();
  loadRetakeKnownUsers();
}

function accountResponseUserKey(answer) {
  return String(answer?.user_id ?? "unknown");
}

function accountResponseUserLabel(answer) {
  const email = (answer?.user_email || "").trim();
  const id = answer?.user_id ?? "unknown";
  return email ? `${email} (User #${id})` : `User #${id}`;
}

function setAccountAssessmentTab(nextTab) {
  activeAccountAssessmentTab = nextTab === "responses" ? "responses" : "questions";
  accountDetailBody?.querySelectorAll(".account-assessment-tab").forEach((button) => {
    const active = button.dataset.accountAssessmentTab === activeAccountAssessmentTab;
    button.classList.toggle("is-active", active);
    button.setAttribute("aria-selected", active ? "true" : "false");
  });
  accountDetailBody?.querySelectorAll("[data-account-assessment-panel]").forEach((panel) => {
    panel.classList.toggle("is-hidden", panel.dataset.accountAssessmentPanel !== activeAccountAssessmentTab);
  });
}

function renderAccountResponseDashboard() {
  const summary = accountDetailBody?.querySelector("#account-response-summary");
  const count = accountDetailBody?.querySelector("#account-response-count");
  const filter = accountDetailBody?.querySelector("#account-response-user-filter");
  if (!summary) return;

  const userMap = new Map();
  activeAccountAnswers.forEach((answer) => {
    const key = accountResponseUserKey(answer);
    if (!userMap.has(key)) userMap.set(key, accountResponseUserLabel(answer));
  });
  const sortedUsers = Array.from(userMap.entries()).sort((a, b) => a[1].localeCompare(b[1], undefined, { sensitivity: "base" }));
  if (filter) {
    const previous = activeAccountResponseUserFilter;
    filter.innerHTML = `
      <option value="all">All users</option>
      ${sortedUsers.map(([key, label]) => `<option value="${escapeHtml(key)}">${escapeHtml(label)}</option>`).join("")}
    `;
    activeAccountResponseUserFilter = previous !== "all" && userMap.has(previous) ? previous : "all";
    filter.value = activeAccountResponseUserFilter;
  }

  const answers = activeAccountResponseUserFilter === "all"
    ? activeAccountAnswers
    : activeAccountAnswers.filter((answer) => accountResponseUserKey(answer) === activeAccountResponseUserFilter);
  const total = answers.length;
  const correct = answers.filter((answer) => answer.is_correct).length;
  const attempts = new Map();
  answers.forEach((answer) => {
    const attemptKey = String(answer.attempt_id);
    if (!attempts.has(attemptKey)) attempts.set(attemptKey, []);
    attempts.get(attemptKey).push(answer);
  });
  const users = new Set(answers.map(accountResponseUserKey));
  const pct = total ? Math.round((correct / total) * 100) : 0;
  if (count) count.textContent = total ? `${total} submitted answer${total === 1 ? "" : "s"}` : "No submitted answers";
  if (!total) {
    summary.innerHTML = '<p class="placeholder">No submitted answers match this user filter.</p>';
    return;
  }

  const questionById = new Map(activeAccountQuestions.map((question, index) => [String(question.id), { ...question, number: index + 1 }]));
  const questionCards = activeAccountQuestions.map((question, index) => {
    const questionAnswers = answers.filter((answer) => String(answer.question_id) === String(question.id));
    const questionCorrect = questionAnswers.filter((answer) => answer.is_correct).length;
    const questionPct = questionAnswers.length ? Math.round((questionCorrect / questionAnswers.length) * 100) : 0;
    const choiceCounts = Object.keys(question.choices || {}).map((choice) => {
      const countForChoice = questionAnswers.filter((answer) => answer.user_response === choice).length;
      return `<span class="${choice === question.correct_response ? "is-correct" : ""}">${escapeHtml(choice)}: ${countForChoice}</span>`;
    }).join("");
    const correctChoice = question.choices?.[question.correct_response] || "";
    return `
      <article class="account-response-question-card">
        <div>
          <strong>Question ${index + 1}</strong>
          <small>${questionAnswers.length} answer${questionAnswers.length === 1 ? "" : "s"} · ${questionPct}% correct · correct ${escapeHtml(question.correct_response || "—")}</small>
        </div>
        <p>${escapeHtml(question.question || "Untitled question")}</p>
        <p class="account-response-answer-key"><strong>Correct answer:</strong> <code>${escapeHtml(question.correct_response || "")}</code>${correctChoice ? ` ${escapeHtml(correctChoice)}` : ""}</p>
        ${question.explanation ? `<p class="account-response-explanation"><strong>Explanation:</strong> ${escapeHtml(question.explanation)}</p>` : ""}
        <div class="account-response-choice-counts">${choiceCounts}</div>
      </article>
    `;
  }).join("");
  const attemptCards = Array.from(attempts.entries())
    .sort((a, b) => Number(b[0]) - Number(a[0]))
    .map(([attemptId, attemptAnswers]) => {
      const attemptCorrect = attemptAnswers.filter((answer) => answer.is_correct).length;
      const first = attemptAnswers[0] || {};
      const attemptPct = attemptAnswers.length ? Math.round((attemptCorrect / attemptAnswers.length) * 100) : 0;
      return `
        <details class="account-response-attempt">
          <summary>
            <span>
              <strong>${escapeHtml(accountResponseUserLabel(first))}</strong>
              <small>Attempt #${escapeHtml(attemptId)}</small>
            </span>
            <b>${attemptCorrect}/${attemptAnswers.length} correct (${attemptPct}%)</b>
          </summary>
          <div class="account-response-list">
            ${attemptAnswers.map((answer) => {
              const question = questionById.get(String(answer.question_id));
              const choiceText = question?.choices?.[answer.user_response] || "";
              const correctResponse = question?.correct_response || "";
              const correctText = correctResponse ? question?.choices?.[correctResponse] || "" : "";
              return `
                <article class="account-response-comment ${answer.is_correct ? "is-correct" : "is-incorrect"}">
                  <div>
                    <strong>Question ${escapeHtml(String(question?.number || answer.question_id))}</strong>
                    <small>${answer.is_correct ? "Correct" : "Incorrect"}</small>
                  </div>
                  <p>${escapeHtml(question?.question || "Question text unavailable.")}</p>
                  <div class="account-response-answer-pair">
                    <p><span>Chosen</span><code>${escapeHtml(answer.user_response || "")}</code>${choiceText ? ` ${escapeHtml(choiceText)}` : ""}</p>
                    <p><span>Correct</span><code>${escapeHtml(correctResponse)}</code>${correctText ? ` ${escapeHtml(correctText)}` : ""}</p>
                  </div>
                  ${question?.explanation ? `<p class="account-response-explanation"><strong>Explanation:</strong> ${escapeHtml(question.explanation)}</p>` : ""}
                </article>
              `;
            }).join("")}
          </div>
        </details>
      `;
    }).join("");

  summary.innerHTML = `
    <div class="account-response-summary-grid">
      <span><strong>${correct}</strong> correct</span>
      <span><strong>${total - correct}</strong> incorrect</span>
      <span><strong>${pct}%</strong> accuracy</span>
      <span><strong>${attempts.size}</strong> attempt${attempts.size === 1 ? "" : "s"}</span>
      <span><strong>${users.size}</strong> user${users.size === 1 ? "" : "s"}</span>
    </div>
    <div class="account-response-section-label">Question breakdown</div>
    <div class="account-response-question-grid">${questionCards}</div>
    <div class="account-response-section-label">Attempts</div>
    <div class="account-response-attempts">${attemptCards}</div>
  `;
}

function renderRetakeKnownUsers() {
  const select = accountDetailBody?.querySelector("#account-retake-known-user");
  if (!select) return;
  const userMap = new Map();
  activeAccountAnswers.forEach((answer) => {
    const key = accountResponseUserKey(answer);
    if (!userMap.has(key)) userMap.set(key, accountResponseUserLabel(answer));
  });
  const sortedUsers = Array.from(userMap.entries()).sort((a, b) => a[1].localeCompare(b[1], undefined, { sensitivity: "base" }));
  select.innerHTML = `
    <option value="">Select a user who has answered</option>
    ${sortedUsers.map(([key, label]) => `<option value="${escapeHtml(key)}">${escapeHtml(label)}</option>`).join("")}
  `;
}

function updateRetakeScopeUi() {
  const scope = accountDetailBody?.querySelector("#account-retake-scope")?.value || "all";
  accountDetailBody?.querySelector("#account-retake-user-fields")?.classList.toggle("is-hidden", scope !== "user");
}

async function loadRetakeKnownUsers() {
  if (!activeAccountDoc) return;
  const message = accountDetailBody?.querySelector("#account-retake-message");
  try {
    const response = await fetch(apiUrl(`/assessments/documentation/${activeAccountDoc.id}/answers`), {
      headers: authHeaders({ Accept: "application/json" })
    });
    const data = await response.json().catch(() => []);
    if (!response.ok) throw new Error(data.detail || data.error || "Could not load respondents.");
    activeAccountAnswers = Array.isArray(data) ? data : [];
    renderRetakeKnownUsers();
    if (message) message.textContent = activeAccountAnswers.length
      ? "Choose all users, a known respondent, or type a user id/email."
      : "No submitted respondents yet. You can still type a user id or email.";
  } catch (error) {
    activeAccountAnswers = [];
    renderRetakeKnownUsers();
    if (message) message.textContent = error.message || "Could not load respondents.";
  }
}

async function grantRetakeAccess(button, forcedScope = null) {
  if (!activeAccountDoc) return;
  const message = accountDetailBody?.querySelector("#account-retake-message");
  const scope = forcedScope || accountDetailBody?.querySelector("#account-retake-scope")?.value || "all";
  const knownUser = accountDetailBody?.querySelector("#account-retake-known-user")?.value || "";
  const lookup = accountDetailBody?.querySelector("#account-retake-user-lookup")?.value.trim() || "";
  const payload = { scope };
  if (scope === "user") {
    const selected = lookup || knownUser;
    if (!selected) {
      if (message) message.textContent = "Choose a known user or type a user id/email.";
      return;
    }
    if (/^\d+$/.test(selected)) {
      payload.user_id = Number(selected);
    } else {
      payload.user_email = selected;
    }
  }
  if (message) message.textContent = "Granting retake access...";
  if (button) button.disabled = true;
  try {
    const response = await fetch(apiUrl(`/assessments/documentation/${activeAccountDoc.id}/retake-access`), {
      method: "POST",
      headers: authHeaders({ "Content-Type": "application/json", Accept: "application/json" }),
      body: JSON.stringify(payload)
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || data.error || "Could not grant retake access.");
    if (message) {
      const who = data.allow_all_users
        ? "all users"
        : data.user_email || (data.user_id ? `User #${data.user_id}` : "the selected user");
      message.textContent = `Retake access granted for ${who}. Previous answers were kept.`;
    }
  } catch (error) {
    if (message) message.textContent = error.message || "Could not grant retake access.";
  } finally {
    if (button) button.disabled = false;
  }
}

function renderAccountQuestions() {
  const list = accountDetailBody?.querySelector("#account-question-list");
  const count = accountDetailBody?.querySelector("#account-question-count");
  if (count) count.textContent = `${activeAccountQuestions.length} question${activeAccountQuestions.length === 1 ? "" : "s"}`;
  if (!list) {
    renderAccountResponseDashboard();
    return;
  }
  if (!activeAccountQuestions.length) {
    list.innerHTML = '<p class="placeholder">No questions yet. Use AI generate questions to create a first draft.</p>';
    renderAccountResponseDashboard();
    setAccountAssessmentTab(activeAccountAssessmentTab);
    return;
  }
  list.innerHTML = activeAccountQuestions.map((question, index) => {
    const choices = question.choices || {};
    const choiceKeys = Object.keys(choices).length ? Object.keys(choices) : ["A", "B", "C", "D"];
    const answers = activeAccountAnswers.filter((answer) => String(answer.question_id) === String(question.id));
    return `
      <details class="account-question-item" data-question-id="${question.id}">
        <summary class="account-question-summary">
          <span>
            <strong>Question ${index + 1}</strong>
            <small>${answers.length} response${answers.length === 1 ? "" : "s"}</small>
          </span>
          <b>${escapeHtml(question.question || "Untitled question")}</b>
        </summary>
        <div class="account-question-readonly">
          <p>${escapeHtml(question.question || "")}</p>
          <ol type="A" class="account-question-choice-preview">
            ${choiceKeys.map((choice) => `
              <li class="${question.correct_response === choice ? "is-correct" : ""}">
                <span>${escapeHtml(choices[choice] || "")}</span>
              </li>
            `).join("")}
          </ol>
          <p class="account-question-explanation"><strong>Explanation:</strong> ${escapeHtml(question.explanation || "No explanation stored.")}</p>
          <div class="account-question-actions">
            <button type="button" class="secondary-button account-question-edit" data-question-id="${question.id}">Edit</button>
            <button type="button" class="danger-button account-question-delete" data-question-id="${question.id}">Delete</button>
            <p class="account-message" data-question-message="${question.id}"></p>
          </div>
        </div>
        <div class="account-question-edit-panel is-hidden">
          <label class="field">
            <span>Question</span>
            <textarea data-question-field="question" rows="3">${escapeHtml(question.question || "")}</textarea>
          </label>
          <div class="manual-choice-grid">
            ${choiceKeys.map((choice) => `
              <label class="field">
                <span>Choice ${escapeHtml(choice)}</span>
                <input data-choice-key="${escapeHtml(choice)}" type="text" value="${escapeHtml(choices[choice] || "")}">
              </label>
            `).join("")}
          </div>
          <div class="manual-answer-row">
            <label class="field compact-field">
              <span>Correct</span>
              <select data-question-field="correct_response">
                ${choiceKeys.map((choice) => `<option value="${escapeHtml(choice)}" ${question.correct_response === choice ? "selected" : ""}>${escapeHtml(choice)}</option>`).join("")}
              </select>
            </label>
            <label class="field">
              <span>Explanation</span>
              <input data-question-field="explanation" type="text" value="${escapeHtml(question.explanation || "")}">
            </label>
          </div>
          <div class="account-question-actions">
            <button type="button" class="landing-primary-button account-question-save" data-question-id="${question.id}">Save changes</button>
            <button type="button" class="secondary-button account-question-cancel" data-question-id="${question.id}">Cancel</button>
          </div>
        </div>
      </details>
    `;
  }).join("");
  renderAccountResponseDashboard();
  setAccountAssessmentTab(activeAccountAssessmentTab);
}

async function loadAccountQuestions() {
  if (!activeAccountDoc) return;
  const list = accountDetailBody?.querySelector("#account-question-list");
  if (list) list.innerHTML = '<p class="placeholder">Loading questions...</p>';
  try {
    const [questionResponse, answerResponse] = await Promise.all([
      fetch(apiUrl(`/assessments/documentation/${activeAccountDoc.id}`), {
        headers: authHeaders({ Accept: "application/json" })
      }),
      fetch(apiUrl(`/assessments/documentation/${activeAccountDoc.id}/answers`), {
        headers: authHeaders({ Accept: "application/json" })
      })
    ]);
    const questionData = await questionResponse.json().catch(() => []);
    const answerData = await answerResponse.json().catch(() => []);
    if (!questionResponse.ok) throw new Error(questionData.detail || questionData.error || "Could not load questions.");
    if (!answerResponse.ok) throw new Error(answerData.detail || answerData.error || "Could not load answers.");
    activeAccountQuestions = Array.isArray(questionData) ? questionData : [];
    activeAccountAnswers = Array.isArray(answerData) ? answerData : [];
    const index = accountDocuments.findIndex((doc) => String(doc.id) === String(activeAccountDoc.id));
    if (index >= 0) {
      accountDocuments[index] = {
        ...accountDocuments[index],
        question_count: activeAccountQuestions.length,
        response_count: activeAccountAnswers.length
      };
      renderAccountDocs();
    }
    renderAccountQuestions();
    renderAccountResponseDashboard();
  } catch (error) {
    activeAccountQuestions = [];
    activeAccountAnswers = [];
    if (list) list.innerHTML = `<p class="placeholder">${escapeHtml(error.message || "Could not load questions.")}</p>`;
  }
}

async function loadAccountUserResponses() {
  if (!activeAccountDoc) return;
  const summary = accountDetailBody?.querySelector("#account-response-summary");
  if (summary) summary.innerHTML = '<p class="placeholder">Loading your responses...</p>';
  try {
    const response = await fetch(apiUrl(`/assessments/documentation/${activeAccountDoc.id}/my-answers`), {
      headers: authHeaders({ Accept: "application/json" })
    });
    const data = await response.json().catch(() => []);
    if (!response.ok) throw new Error(data.detail || data.error || "Could not load your responses.");
    activeAccountAnswers = Array.isArray(data) ? data : [];
    const questionMap = new Map();
    activeAccountAnswers.forEach((answer) => {
      if (!questionMap.has(String(answer.question_id))) {
        questionMap.set(String(answer.question_id), {
          id: answer.question_id,
          documentation_id: answer.documentation_id,
          question: answer.question,
          choices: answer.choices || {},
          correct_response: answer.correct_response,
          explanation: answer.explanation
        });
      }
    });
    activeAccountQuestions = Array.from(questionMap.values());
    const index = accountDocuments.findIndex((doc) => String(doc.id) === String(activeAccountDoc.id));
    if (index >= 0) {
      accountDocuments[index] = {
        ...accountDocuments[index],
        question_count: activeAccountQuestions.length || accountDocuments[index].question_count || 0,
        response_count: activeAccountAnswers.length
      };
      renderAccountDocs();
    }
    renderAccountResponseDashboard();
  } catch (error) {
    activeAccountQuestions = [];
    activeAccountAnswers = [];
    if (summary) summary.innerHTML = `<p class="placeholder">${escapeHtml(error.message || "Could not load your responses.")}</p>`;
  }
}

function collectManualQuestionPayload() {
  const choices = {};
  accountDetailBody?.querySelectorAll("[data-manual-choice]").forEach((input) => {
    choices[input.dataset.manualChoice] = input.value.trim();
  });
  return {
    id: 0,
    documentation_id: activeAccountDoc?.id,
    question: accountDetailBody?.querySelector("#manual-question-text")?.value.trim() || "",
    choices,
    correct_response: accountDetailBody?.querySelector("#manual-correct-response")?.value || "A",
    explanation: accountDetailBody?.querySelector("#manual-explanation")?.value.trim() || ""
  };
}

function resetManualQuestionForm() {
  const questionInput = accountDetailBody?.querySelector("#manual-question-text");
  if (questionInput) questionInput.value = "";
  accountDetailBody?.querySelectorAll("[data-manual-choice]").forEach((input) => {
    input.value = "";
  });
  const explanation = accountDetailBody?.querySelector("#manual-explanation");
  if (explanation) explanation.value = "";
  const correct = accountDetailBody?.querySelector("#manual-correct-response");
  if (correct) correct.value = "A";
}

async function saveManualAssessmentQuestion(button) {
  const message = accountDetailBody?.querySelector("#account-manual-question-message");
  const payload = collectManualQuestionPayload();
  if (!activeAccountDoc?.id) return;
  if (!payload.question || !payload.explanation || Object.values(payload.choices).some((choice) => !choice)) {
    if (message) message.textContent = "Fill in the question, all choices, and the explanation.";
    return;
  }
  if (message) message.textContent = "Saving human question...";
  if (button) button.disabled = true;
  try {
    const response = await fetch(apiUrl("/assessments/admin_submit"), {
      method: "POST",
      headers: authHeaders({ "Content-Type": "application/json", Accept: "application/json" }),
      body: JSON.stringify(payload)
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || data.error || "Could not save question.");
    resetManualQuestionForm();
    if (message) message.textContent = `Saved human question${data.id ? ` #${data.id}` : ""}.`;
    await loadAccountQuestions();
    await fetchAccountDocs({ retry: false });
  } catch (error) {
    if (message) message.textContent = error.message || "Could not save question.";
  } finally {
    if (button) button.disabled = false;
  }
}

async function generateAssessmentForActiveDoc(button) {
  if (!activeAccountDoc) return;
  const message = accountDetailBody?.querySelector("#account-assessment-message");
  const countInput = accountDetailBody?.querySelector("#account-assessment-count");
  const choicesInput = accountDetailBody?.querySelector("#account-assessment-choices");
  const docTypeInput = accountDetailBody?.querySelector("#account-assessment-doc-type");
  const nQuestions = Math.max(1, Math.min(30, Number(countInput?.value || 10)));
  const choices = Math.max(2, Math.min(6, Number(choicesInput?.value || 4)));
  const docType = docTypeInput?.value || "random";
  const params = new URLSearchParams({
    n_questions: String(nQuestions),
    choice: String(choices),
    doc_type: docType
  });
  if (metricsModelInput?.value.trim()) params.set("model", metricsModelInput.value.trim());
  if (currentModelProvider()) params.set("model_provider", currentModelProvider());
  if (modelBaseUrlInput?.value.trim()) params.set("base_url", modelBaseUrlInput.value.trim());
  const providerPayload = {
    model_provider: currentModelProvider(),
    model_api_key: openaiKeyInput?.value.trim() || "",
    api_key: openaiKeyInput?.value.trim() || "",
    base_url: modelBaseUrlInput?.value.trim() || (currentModelProvider() === "cmu_gateway" ? DEFAULT_CMU_GATEWAY_BASE_URL : ""),
    metrics_model: metricsModelInput?.value.trim() || ""
  };
  if (message) message.textContent = `Generating assessment questions from ${docType.toUpperCase()} docs...`;
  if (button) {
    button.disabled = true;
    button.textContent = "Generating...";
  }
  try {
    const response = await fetch(apiUrl(`/assessments/generate/${activeAccountDoc.id}?${params.toString()}`), {
      method: "POST",
      headers: authHeaders({ "Content-Type": "application/json", Accept: "application/json" }),
      body: JSON.stringify(providerPayload)
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(response.status === 403 ? "Only admin users can generate assessment questions." : data.detail || data.error || "Could not generate questions.");
    }
    if (message) {
      const questionId = data.id ? ` Last question id: ${data.id}.` : "";
      message.textContent = `Generated ${nQuestions} comprehension questions from ${docType.toUpperCase()} docs.${questionId}`;
    }
    await loadAccountQuestions();
    await fetchAccountDocs({ retry: false });
  } catch (error) {
    if (message) message.textContent = error.message || "Could not generate questions.";
  } finally {
    if (button) {
      button.disabled = false;
      button.textContent = "AI generate full set";
    }
  }
}

function collectQuestionPayload(questionId) {
  const item = accountDetailBody?.querySelector(`.account-question-item[data-question-id="${CSS.escape(String(questionId))}"]`);
  if (!item) return null;
  const choices = {};
  item.querySelectorAll("[data-choice-key]").forEach((input) => {
    choices[input.dataset.choiceKey] = input.value.trim();
  });
  return {
    id: Number(questionId),
    documentation_id: activeAccountDoc?.id,
    question: item.querySelector('[data-question-field="question"]')?.value.trim() || "",
    choices,
    correct_response: item.querySelector('[data-question-field="correct_response"]')?.value || "A",
    explanation: item.querySelector('[data-question-field="explanation"]')?.value.trim() || ""
  };
}

async function saveAccountQuestion(questionId, button) {
  const message = accountDetailBody?.querySelector(`[data-question-message="${CSS.escape(String(questionId))}"]`);
  const payload = collectQuestionPayload(questionId);
  if (!payload) return;
  if (message) message.textContent = "Saving...";
  if (button) button.disabled = true;
  try {
    const response = await fetch(apiUrl("/assessments/submit/update"), {
      method: "PUT",
      headers: authHeaders({ "Content-Type": "application/json", Accept: "application/json" }),
      body: JSON.stringify(payload)
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || data.error || "Could not save question.");
    if (message) message.textContent = "Saved.";
    await loadAccountQuestions();
    refreshAccountDataSoon();
  } catch (error) {
    if (message) message.textContent = error.message || "Could not save question.";
  } finally {
    if (button) button.disabled = false;
  }
}

async function deleteAccountQuestion(questionId, button) {
  if (button) button.disabled = true;
  try {
    const response = await fetch(apiUrl(`/assessments/submit/delete/${questionId}`), {
      method: "DELETE",
      headers: authHeaders({ Accept: "application/json" })
    });
    if (!response.ok && response.status !== 204) {
      const data = await response.json().catch(() => ({}));
      throw new Error(data.detail || data.error || "Could not delete question.");
    }
    await loadAccountQuestions();
    refreshAccountDataSoon();
  } catch (error) {
    const message = accountDetailBody?.querySelector(`[data-question-message="${CSS.escape(String(questionId))}"]`);
    if (message) message.textContent = error.message || "Could not delete question.";
  } finally {
    if (button) button.disabled = false;
  }
}

async function resetAllAccountQuestions(button) {
  if (!activeAccountDoc || !activeAccountQuestions.length) return;
  const message = accountDetailBody?.querySelector("#account-manual-question-message");
  const phrase = "RESET QUESTIONS";
  const typed = window.prompt(`Type ${phrase} to delete all ${activeAccountQuestions.length} questions for ${activeAccountDoc.documentation_title || "this documentation"}. Answers tied to deleted questions may also be removed.`);
  if (typed !== phrase) {
    if (message) message.textContent = "Reset cancelled. Phrase did not match.";
    return;
  }
  if (message) message.textContent = "Resetting all questions...";
  if (button) button.disabled = true;
  try {
    for (const question of activeAccountQuestions) {
      const response = await fetch(apiUrl(`/assessments/submit/delete/${question.id}`), {
        method: "DELETE",
        headers: authHeaders({ Accept: "application/json" })
      });
      if (!response.ok && response.status !== 204) {
        const data = await response.json().catch(() => ({}));
        throw new Error(data.detail || data.error || `Could not delete question #${question.id}.`);
      }
    }
    if (message) message.textContent = "All questions reset.";
    await loadAccountQuestions();
    refreshAccountDataSoon();
  } catch (error) {
    if (message) message.textContent = error.message || "Could not reset questions.";
  } finally {
    if (button) button.disabled = false;
  }
}

async function resetAllAssessmentAttempts(button, requestedScope = "ALL") {
  if (!accountIsAdmin) return;
  const scope = String(requestedScope || "").trim().toUpperCase();
  if (!["ALL", "QUIZ", "COMPARISON"].includes(scope)) {
    if (accountAdminMessage) accountAdminMessage.textContent = "Reset cancelled. Choose ALL, QUIZ, or COMPARISON.";
    return;
  }
  const target = accountResetTarget?.value || "all";
  const lookup = (accountResetLookup?.value || "").trim();
  if (target !== "all" && !lookup) {
    if (accountAdminMessage) accountAdminMessage.textContent = target === "email" ? "Enter a user email first." : "Enter a user id first.";
    accountResetLookup?.focus();
    return;
  }
  if (target === "id" && !/^\d+$/.test(lookup)) {
    if (accountAdminMessage) accountAdminMessage.textContent = "User id must be a number.";
    accountResetLookup?.focus();
    return;
  }
  const targetLabel = target === "all" ? "all users" : (target === "email" ? `user email ${lookup}` : `user id ${lookup}`);
  const phrase = `RESET ${scope}`;
  const typed = window.prompt(`Type ${phrase} to confirm resetting ${scope.toLowerCase()} data for ${targetLabel}.`);
  if (typed !== phrase) {
    if (accountAdminMessage) accountAdminMessage.textContent = "Reset cancelled. Phrase did not match.";
    return;
  }
  const params = new URLSearchParams({ scope: target === "all" ? "all" : "user" });
  if (target === "email") params.set("user_email", lookup);
  if (target === "id") params.set("user_id", lookup);
  if (accountAdminMessage) accountAdminMessage.textContent = `Resetting ${scope.toLowerCase()} data for ${targetLabel}...`;
  if (button) button.disabled = true;
  try {
    const messages = [];
    if (scope === "ALL" || scope === "QUIZ") {
      const response = await fetch(apiUrl(`/assessments/attempts?${params.toString()}`), {
        method: "DELETE",
        headers: authHeaders({ Accept: "application/json" })
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        const detail = data.detail || data.error || "No backend detail returned.";
        throw new Error(`Could not reset quiz attempts (HTTP ${response.status}). ${detail}`);
      }
      const grantNote = data.retake_grants_table_found === false
        ? " Retake grant table was skipped."
        : ` ${Number(data.deleted_retake_grants || 0)} retake grants deleted.`;
      messages.push(`Quiz: ${Number(data.deleted_answers || 0)} answers and ${Number(data.deleted_attempts || 0)} attempts deleted.${grantNote}`);
    }

    if (scope === "ALL" || scope === "COMPARISON") {
      const response = await fetch(apiUrl(`/comparison/attempts?${params.toString()}`), {
        method: "DELETE",
        headers: authHeaders({ Accept: "application/json" })
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        const detail = data.detail || data.error || "No backend detail returned.";
        throw new Error(`Could not reset comparisons (HTTP ${response.status}). ${detail}`);
      }
      resetLocalAreaSession();
      messages.push(`Comparison: ${Number(data.deleted_comparisons || 0)} votes deleted and ${Number(data.updated_documents || 0)} documents reset.`);
    }

    if (accountAdminMessage) accountAdminMessage.textContent = `Reset complete for ${targetLabel}. ${messages.join(" ")}`;
    await fetchAccountDocs();
    refreshAccountDataSoon();
  } catch (error) {
    if (accountAdminMessage) accountAdminMessage.textContent = error.message || "Could not reset.";
  } finally {
    if (button) button.disabled = false;
  }
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
  refreshAccountDataSoon();
}

function openTDUploaderForAccountDoc(docId) {
  const doc = accountDocuments.find((item) => String(item.id) === String(docId));
  if (!doc) return;
  activeSavedDocumentation = doc;
  activeAccountDoc = doc;
  currentMarkdown = accountDocMarkdown(doc, "ibd");
  currentSource = doc.source_code || "";
  if (apiNameInput) apiNameInput.value = doc.documentation_title || "api.function";
  if (documentationInput) documentationInput.value = doc.source_code || "";
  if (tdSourceInput) tdSourceInput.value = accountDocMarkdown(doc, "td");
  if (tdPreview) {
    const tdMarkdown = accountDocMarkdown(doc, "td");
    tdPreview.innerHTML = tdMarkdown
      ? renderMarkdown(tdMarkdown)
      : '<p class="placeholder">Paste traditional/reference documentation for this API.</p>';
  }
  closeAccountDocDetail();
  showAppPage();
  showTDStage();
  if (tdMessage) tdMessage.textContent = `Adding TD Markdown for ${doc.documentation_title || "this API"}.`;
}

function setAccountMarkdownEditing(editing) {
  const rendered = accountDetailBody?.querySelector("#account-detail-markdown");
  const editor = accountDetailBody?.querySelector("#account-detail-md-editor");
  const tdEditor = accountDetailBody?.querySelector("#account-detail-td-editor");
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
    tdEditor?.classList.add("is-hidden");
    editButton?.classList.add("is-hidden");
    textarea?.focus();
  } else {
    rendered.classList.remove("is-hidden");
    editor.classList.add("is-hidden");
    editButton?.classList.remove("is-hidden");
  }
}

function setAccountTraditionalEditing(editing) {
  const rendered = accountDetailBody?.querySelector("#account-detail-markdown");
  const ibdEditor = accountDetailBody?.querySelector("#account-detail-md-editor");
  const editor = accountDetailBody?.querySelector("#account-detail-td-editor");
  const textarea = accountDetailBody?.querySelector("#account-td-textarea");
  const editButton = accountDetailBody?.querySelector("#account-td-edit");
  const message = accountDetailBody?.querySelector("#account-md-message");
  if (!rendered || !editor) return;
  if (message) {
    message.textContent = "";
    message.classList.remove("is-success");
  }
  if (editing) {
    if (textarea && activeAccountDoc) textarea.value = accountDocMarkdown(activeAccountDoc, "td");
    rendered.classList.add("is-hidden");
    ibdEditor?.classList.add("is-hidden");
    editor.classList.remove("is-hidden");
    editButton?.classList.add("is-hidden");
    textarea?.focus();
  } else {
    rendered.classList.remove("is-hidden");
    editor.classList.add("is-hidden");
    editButton?.classList.remove("is-hidden");
  }
}

function setAccountMarkdownKind(kind) {
  if (!activeAccountDoc) return;
  const selectedKind = kind === "td" && hasTraditionalDocumentation(activeAccountDoc) ? "td" : "ibd";
  const rendered = accountDetailBody?.querySelector("#account-detail-markdown");
  if (rendered) {
    const markdown = accountDocMarkdown(activeAccountDoc, selectedKind);
    rendered.innerHTML = markdown ? renderMarkdown(markdown) : `<p class="placeholder">No ${selectedKind.toUpperCase()} Markdown stored.</p>`;
  }
  accountDetailBody?.querySelectorAll(".account-doc-kind-tab").forEach((button) => {
    const active = button.dataset.docKind === selectedKind;
    button.classList.toggle("is-active", active);
    button.setAttribute("aria-selected", active ? "true" : "false");
  });
  setAccountMarkdownEditing(false);
  setAccountTraditionalEditing(false);
}

function downloadActiveAccountMarkdown(kind = "ibd") {
  if (!activeAccountDoc) return;
  const selectedKind = kind === "td" ? "td" : "ibd";
  const filename = `${slugify(activeAccountDoc.documentation_title || "documentation")}-${selectedKind}.md`;
  downloadMarkdown(accountDocMarkdown(activeAccountDoc, selectedKind), filename);
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

async function saveAccountTraditionalMarkdown(button) {
  if (!activeAccountDoc) return;
  const textarea = accountDetailBody?.querySelector("#account-td-textarea");
  const message = accountDetailBody?.querySelector("#account-md-message");
  const newMarkdown = textarea ? textarea.value : "";
  button.disabled = true;
  if (message) {
    message.classList.remove("is-success");
    message.textContent = "Saving TD Markdown...";
  }
  try {
    const response = await fetch(apiUrl(`/documentation/${activeAccountDoc.id}/td`), {
      method: "PUT",
      headers: authHeaders({ "Content-Type": "application/json", Accept: "application/json" }),
      body: JSON.stringify({ TD_md: newMarkdown })
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || data.error || "Could not save TD Markdown.");
    activeAccountDoc.TD_md = newMarkdown;
    const index = accountDocuments.findIndex((item) => String(item.id) === String(activeAccountDoc.id));
    if (index >= 0) accountDocuments[index] = { ...accountDocuments[index], TD_md: newMarkdown };
    savedDocumentation = [data, ...savedDocumentation.filter((doc) => doc.id !== data.id)];
    renderAccountDocs();
    renderSavedDocs();
    showAccountDocDetail(activeAccountDoc.id, newMarkdown.trim() ? "td" : "ibd");
    const nextMessage = accountDetailBody?.querySelector("#account-md-message");
    if (nextMessage) {
      nextMessage.textContent = "TD Markdown saved.";
      nextMessage.classList.add("is-success");
    }
  } catch (error) {
    if (message) message.textContent = error.message || "Could not save TD Markdown.";
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
  fetchAccountProfile().finally(() => fetchAccountDocs());
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
    accountCurrentUserId = null;
    accountIsAdmin = false;
    updateAccountDocsScopeUi();
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
  const data = await fetchJsonWithRetry(apiUrl("/documentation/create_ibd"), {
    method: "POST",
    headers: authHeaders({ "Content-Type": "application/json", Accept: "application/json" }),
    body: JSON.stringify(payload)
  }, {
    retries: 2,
    timeout: API_BASE_URL ? 20000 : 10000,
    retryDelay: 1800
  });
  activeSavedDocumentation = data;
  savedDocumentation = [data, ...savedDocumentation.filter((doc) => doc.id !== data.id)];
  renderSavedDocs();
  refreshDatabaseStatus();
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
    const accountIndex = accountDocuments.findIndex((doc) => String(doc.id) === String(data.id));
    if (accountIndex >= 0) accountDocuments[accountIndex] = { ...accountDocuments[accountIndex], TD_md: markdown };
    renderSavedDocs();
    renderAccountDocs();
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

async function pollCeleryTask(taskId, {
  statusPath,
  queuedLabel = "Redis queued task",
  runningLabel = "Celery worker running",
  doneLabel = "Celery task complete",
  maxAttempts = 240,
  delayMs = 2000
} = {}) {
  if (!taskId || !statusPath) throw new Error("Missing Celery task status details.");
  showQueueStatus(`${queuedLabel}: ${taskId}`, "checking");
  for (let attempt = 0; attempt < maxAttempts; attempt += 1) {
    const response = await fetch(apiUrl(statusPath(taskId)), {
      cache: "no-store",
      headers: authHeaders({ Accept: "application/json" })
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(data.detail || data.error || `Task poll failed with HTTP ${response.status}.`);
    }
    if (data.ready) {
      if (data.result?.error) {
        showQueueStatus("Celery task failed", "error");
        throw new Error(data.result.error);
      }
      showQueueStatus(doneLabel, "connected");
      window.setTimeout(refreshDatabaseStatus, 1800);
      return data.result;
    }
    const state = data.status ? String(data.status).toLowerCase() : "pending";
    showQueueStatus(`${runningLabel}: ${state}`, "checking");
    await wait(delayMs);
  }
  showQueueStatus("Celery task still running", "partial");
  throw new Error("Celery task is still running. Check the task result again shortly.");
}

async function downloadAdminCsv(path, button) {
  if (!accountIsAdmin) return;
  const originalText = button?.textContent || "Export CSV";
  if (button) {
    button.disabled = true;
    button.textContent = "Exporting...";
  }
  try {
    const response = await fetch(apiUrl(path), {
      headers: authHeaders({ Accept: "text/csv" })
    });
    if (!response.ok) {
      const detail = await response.text().catch(() => "");
      throw new Error(detail || `Export failed with HTTP ${response.status}.`);
    }
    const contentType = response.headers.get("content-type") || "";
    let blob;
    let filename;
    if (contentType.includes("application/json")) {
      const data = await response.json();
      if (!data.task_id) throw new Error("Export did not return a CSV or task id.");
      if (button) button.textContent = "Queued...";
      const result = await pollCeleryTask(data.task_id, {
        statusPath: (taskId) => `/assessments/export/${encodeURIComponent(taskId)}`,
        queuedLabel: "Redis queued export",
        runningLabel: "Celery export running",
        doneLabel: "Export ready"
      });
      filename = result?.filename || "export.csv";
      blob = new Blob([result?.content || ""], { type: result?.media_type || "text/csv;charset=utf-8" });
    } else {
      blob = await response.blob();
      const disposition = response.headers.get("content-disposition") || "";
      filename = disposition.match(/filename="?([^"]+)"?/i)?.[1] || "export.csv";
    }
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
    if (accountAdminMessage) accountAdminMessage.textContent = `${filename} downloaded.`;
  } catch (error) {
    if (accountAdminMessage) accountAdminMessage.textContent = error.message || "Could not export CSV.";
  } finally {
    if (button) {
      button.disabled = false;
      button.textContent = originalText;
    }
  }
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
  if (data.task_id) {
    const result = await pollCeleryTask(data.task_id, {
      statusPath: (taskId) => `/metrics/${encodeURIComponent(taskId)}`,
      queuedLabel: "Redis queued metric job",
      runningLabel: "Celery metric job running",
      doneLabel: "Metric job complete"
    });
    if (useCache) {
      requestCache.set(cacheKey, result);
    }
    return result;
  }
  if (useCache) {
    requestCache.set(cacheKey, data);
  }
  return data;
}

async function fetchJsonWithRetry(url, options = {}, { retries = 1, timeout = 15000, retryDelay = 1200 } = {}) {
  let lastError = null;
  for (let attempt = 0; attempt <= retries; attempt += 1) {
    const controller = new AbortController();
    const timeoutId = window.setTimeout(() => controller.abort(), timeout);
    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(data.detail || data.error || `Request failed with ${response.status}.`);
      }
      return data;
    } catch (error) {
      lastError = error;
      if (attempt >= retries) break;
      await wait(retryDelay);
    } finally {
      window.clearTimeout(timeoutId);
    }
  }
  throw lastError || new Error("Request failed.");
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

function selectedInvariantIndexes() {
  const inputs = Array.from(reviewPanel.querySelectorAll(".invariant-item input[type='checkbox']"));
  if (!inputs.length) {
    return currentInvariants.map((_invariant, index) => index);
  }
  return inputs
    .filter((input) => input.checked)
    .map((input) => Number(input.dataset.index))
    .filter((index) => Number.isInteger(index) && index >= 0 && index < currentInvariants.length);
}

function selectedInvariantTexts() {
  return selectedInvariantIndexes()
    .map((index) => invariantText(currentInvariants[index]))
    .filter(Boolean);
}

function checkedInvariantIndexSet(invariants) {
  const checked = new Set(selectedInvariantIndexes());
  if (checked.size || reviewPanel.querySelector(".invariant-item input[type='checkbox']")) {
    return checked;
  }
  return new Set(invariants.map((_invariant, index) => index));
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
  const checkedIndexes = checkedInvariantIndexSet(invariants);
  renderInvariantReview([]);
  const list = document.querySelector("#invariant-list");
  list.innerHTML = invariants.map((invariant, index) => {
    const metric = metricForInvariant(invariant, index);
    const range = invariantRange(invariant);
    return `
      <label class="invariant-item" data-index="${index}">
        <input type="checkbox" ${checkedIndexes.has(index) ? "checked" : ""} data-index="${index}">
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
  const selectedInvariants = selectedInvariantTexts();
  if (!assessMetricsInput.checked || !selectedInvariants.length) {
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
    invariants: selectedInvariants,
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
  const accepted = selectedInvariantTexts();

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
areaNextBottomButton?.addEventListener("click", showNextAreaPost);
areaResetButton?.addEventListener("click", async () => {
  if (getAccessToken()) {
    await refreshAccountAdminState();
  }
  if (!accountIsAdmin) {
    if (areaVoteMessage) areaVoteMessage.textContent = "Only admin accounts can reset the Arena session.";
    updateAreaSessionUI();
    return;
  }
  resetLocalAreaSession();
  loadAreaComparison();
});

areaModeTabs.forEach((button) => {
  button.addEventListener("click", () => setAreaMode(button.dataset.areaMode));
});

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
assessmentNextButton?.addEventListener("click", () => moveAssessmentQuestion(1));
assessmentDocSelect?.addEventListener("change", () => {
  saveCurrentAssessmentSession();
  activeAssessmentDocumentationId = assessmentDocSelect.value || "";
  loadAssessment(activeAssessmentDocumentationId);
});
assessmentDocTypeSelect?.addEventListener("change", () => {
  saveCurrentAssessmentSession();
  const documentationId = activeAssessmentDocumentationId || currentAssessment?.documentation_id || "";
  if (documentationId) activeAssessmentDocumentationId = String(documentationId);
  loadAssessment(activeAssessmentDocumentationId);
});
assessmentResourceTabs.forEach((button) => {
  button.addEventListener("click", () => {
    activeAssessmentResource = button.dataset.assessmentResource || "documentation";
    renderAssessmentResource();
    saveCurrentAssessmentSession();
  });
});
assessmentChoiceList?.addEventListener("click", (event) => {
  const button = event.target.closest(".assessment-choice");
  if (!button) return;
  selectAssessmentChoice(button.dataset.assessmentChoice);
});
assessmentSubmitButton?.addEventListener("click", submitAssessmentAnswer);
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

logoutButton?.addEventListener("click", logoutCurrentUser);
accountLogoutButton?.addEventListener("click", logoutCurrentUser);
accountResetTarget?.addEventListener("change", updateAdminResetTargetUi);
accountAdminActions?.addEventListener("click", (event) => {
  const resetButton = event.target.closest(".admin-reset-button");
  if (resetButton) {
    if (!accountIsAdmin) {
      if (accountAdminMessage) accountAdminMessage.textContent = "Only admin users can reset attempts.";
      accountAdminActions?.classList.add("is-hidden");
      return;
    }
    resetAllAssessmentAttempts(resetButton, resetButton.dataset.resetScope);
    return;
  }
  const button = event.target.closest(".admin-export-button");
  if (!button) return;
  downloadAdminCsv(button.dataset.exportPath, button);
});

accountPageButton?.addEventListener("click", showAccountPage);
accountBackButton?.addEventListener("click", showAppPage);
accountDocsRefresh?.addEventListener("click", () => {
  fetchAccountProfile().finally(() => fetchAccountDocs());
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
  const questionsButton = event.target.closest(".account-doc-questions");
  if (questionsButton) {
    if (!accountIsAdmin) return;
    showAccountQuestionBuilder(questionsButton.dataset.docId);
    return;
  }
  const responsesButton = event.target.closest(".account-doc-responses");
  if (responsesButton) {
    showAccountResponses(responsesButton.dataset.docId);
    return;
  }
  const retakeButton = event.target.closest(".account-doc-retake");
  if (retakeButton) {
    if (!accountIsAdmin) return;
    showAccountRetakeAccess(retakeButton.dataset.docId);
    return;
  }
  const deleteButton = event.target.closest(".account-doc-delete");
  if (deleteButton) {
    deleteAccountDocument(deleteButton.dataset.docId).catch((error) => {
      if (accountDocsList) accountDocsList.innerHTML = `<p class="placeholder">${escapeHtml(error.message || "Could not delete document.")}</p>`;
    });
    return;
  }
  const button = event.target.closest(".account-doc-view");
  if (!button) return;
  if (button.dataset.docAction === "add-td") {
    openTDUploaderForAccountDoc(button.dataset.docId);
    return;
  }
  showAccountDocDetail(button.dataset.docId, button.dataset.docKind || "ibd");
});

accountDetailClose?.addEventListener("click", closeAccountDocDetail);
accountDetailModal?.addEventListener("click", (event) => {
  if (event.target?.matches?.("[data-close-account-detail]")) closeAccountDocDetail();
});

accountDetailBody?.addEventListener("click", (event) => {
  const manualSaveButton = event.target.closest("#account-manual-question-save");
  if (manualSaveButton) {
    saveManualAssessmentQuestion(manualSaveButton);
    return;
  }
  if (event.target.closest("#account-question-refresh")) {
    loadAccountQuestions();
    return;
  }
  const resetAllQuestionsButton = event.target.closest("#account-question-reset-all");
  if (resetAllQuestionsButton) {
    if (!accountIsAdmin) return;
    resetAllAccountQuestions(resetAllQuestionsButton);
    return;
  }
  if (event.target.closest("#account-retake-refresh-users")) {
    if (!accountIsAdmin) return;
    loadRetakeKnownUsers();
    return;
  }
  const retakeAllButton = event.target.closest("#account-retake-all");
  if (retakeAllButton) {
    if (!accountIsAdmin) return;
    grantRetakeAccess(retakeAllButton, "all");
    return;
  }
  const retakeGrantButton = event.target.closest("#account-retake-grant");
  if (retakeGrantButton) {
    if (!accountIsAdmin) return;
    grantRetakeAccess(retakeGrantButton);
    return;
  }
  const questionSaveButton = event.target.closest(".account-question-save");
  if (questionSaveButton) {
    if (!accountIsAdmin) return;
    saveAccountQuestion(questionSaveButton.dataset.questionId, questionSaveButton);
    return;
  }
  const questionEditButton = event.target.closest(".account-question-edit");
  if (questionEditButton) {
    const item = questionEditButton.closest(".account-question-item");
    item?.querySelector(".account-question-edit-panel")?.classList.remove("is-hidden");
    item?.querySelector(".account-question-readonly")?.classList.add("is-hidden");
    return;
  }
  const questionCancelButton = event.target.closest(".account-question-cancel");
  if (questionCancelButton) {
    const item = questionCancelButton.closest(".account-question-item");
    item?.querySelector(".account-question-edit-panel")?.classList.add("is-hidden");
    item?.querySelector(".account-question-readonly")?.classList.remove("is-hidden");
    return;
  }
  const questionDeleteButton = event.target.closest(".account-question-delete");
  if (questionDeleteButton) {
    deleteAccountQuestion(questionDeleteButton.dataset.questionId, questionDeleteButton);
    return;
  }
  const markdownDownloadButton = event.target.closest(".account-md-download");
  if (markdownDownloadButton) {
    downloadActiveAccountMarkdown(markdownDownloadButton.dataset.docKind || "ibd");
    return;
  }
  const assessmentGenerateButton = event.target.closest("#account-assessment-generate");
  if (assessmentGenerateButton) {
    generateAssessmentForActiveDoc(assessmentGenerateButton);
    return;
  }
  const assessmentTabButton = event.target.closest(".account-assessment-tab");
  if (assessmentTabButton) {
    setAccountAssessmentTab(assessmentTabButton.dataset.accountAssessmentTab);
    return;
  }
  if (event.target.closest("#account-md-edit")) {
    setAccountMarkdownEditing(true);
    return;
  }
  if (event.target.closest("#account-td-edit")) {
    setAccountTraditionalEditing(true);
    return;
  }
  const docKindTab = event.target.closest(".account-doc-kind-tab");
  if (docKindTab) {
    setAccountMarkdownKind(docKindTab.dataset.docKind);
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
  if (event.target.closest("#account-td-cancel")) {
    setAccountTraditionalEditing(false);
    return;
  }
  const saveButton = event.target.closest("#account-md-save");
  if (saveButton) {
    saveAccountMarkdown(saveButton);
    return;
  }
  const tdSaveButton = event.target.closest("#account-td-save");
  if (tdSaveButton) {
    saveAccountTraditionalMarkdown(tdSaveButton);
  }
});

accountDetailBody?.addEventListener("change", (event) => {
  const responseFilter = event.target.closest("#account-response-user-filter");
  if (responseFilter) {
    activeAccountResponseUserFilter = responseFilter.value || "all";
    renderAccountResponseDashboard();
    return;
  }
  if (event.target.closest("#account-retake-scope")) {
    updateRetakeScopeUi();
    return;
  }
  const knownRetakeUser = event.target.closest("#account-retake-known-user");
  if (knownRetakeUser && knownRetakeUser.value) {
    const lookup = accountDetailBody?.querySelector("#account-retake-user-lookup");
    if (lookup) lookup.value = knownRetakeUser.value;
  }
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !accountDetailModal?.classList.contains("is-hidden")) closeAccountDocDetail();
});

window.addEventListener("pageshow", (event) => {
  if (event.persisted || document.body.classList.contains("account-active")) {
    refreshAccountDataSoon(0);
  }
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
updateAccountDocsScopeUi();
refreshDatabaseStatus();
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
