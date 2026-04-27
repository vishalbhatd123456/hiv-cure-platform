const API_BASE = "https://www.ebi.ac.uk/europepmc/webservices/rest/search";

const TOPIC_QUERIES = {
  all: [
    '"HIV cure"',
    '"HIV remission"',
    '"HIV reservoir"',
    '"HIV latency reversal"',
    '"HIV broadly neutralizing antibodies"',
    '"HIV gene therapy"',
    '"ART-free remission"',
    '"post-treatment control" HIV',
  ],
  reservoir: ['"HIV reservoir"', '"viral reservoir" HIV', '"reservoir decay" HIV'],
  latency: ['"HIV latency"', '"latency reversal" HIV', '"reactivation" HIV reservoir'],
  bnab: ['"broadly neutralizing antibodies" HIV', '"bNAb" HIV cure'],
  gene: ['"HIV gene therapy"', '"cell therapy" HIV cure', '"CCR5" HIV cure'],
  remission: ['"HIV remission"', '"ART-free remission"', '"post-treatment control" HIV'],
  vaccine: ['"therapeutic vaccine" HIV cure', '"HIV vaccine" remission'],
};

const state = {
  articles: [],
  topic: "all",
  filter: "",
};

const elements = {
  results: document.querySelector("#results"),
  loading: document.querySelector("#loadingState"),
  error: document.querySelector("#errorState"),
  count: document.querySelector("#resultCount"),
  lastUpdated: document.querySelector("#lastUpdated"),
  filter: document.querySelector("#filterInput"),
  topic: document.querySelector("#topicSelect"),
  refresh: document.querySelector("#refreshButton"),
};

function buildQuery(topic) {
  const topicQuery = `(${TOPIC_QUERIES[topic].join(" OR ")})`;
  return `${topicQuery} sort_date:y`;
}

async function fetchResearch() {
  setLoading(true);
  elements.error.classList.add("hidden");

  const params = new URLSearchParams({
    query: buildQuery(state.topic),
    format: "json",
    pageSize: "100",
    resultType: "core",
  });

  try {
    const response = await fetch(`${API_BASE}?${params.toString()}`, {
      headers: { Accept: "application/json" },
    });

    if (!response.ok) {
      throw new Error(`Europe PMC returned ${response.status}`);
    }

    const payload = await response.json();
    state.articles = normalizeResults(payload.resultList?.result ?? []);
    render();
  } catch (error) {
    elements.error.textContent =
      "Unable to load public research metadata right now. Check your network connection or try Refresh.";
    elements.error.classList.remove("hidden");
    state.articles = [];
    render();
  } finally {
    setLoading(false);
  }
}

function normalizeResults(results) {
  const seen = new Set();
  return results
    .map((item) => {
      const id = item.pmid || item.pmcid || item.doi || item.id;
      const source = normalizeId(item.source || "MED");
      const recordId = normalizeId(item.id);
      const pmid = normalizeId(item.pmid);
      const doi = normalizeDoi(item.doi);

      return {
        id,
        title: cleanText(item.title) || "Untitled publication",
        journal: cleanText(item.journalTitle) || item.source || "Unknown source",
        date: item.firstPublicationDate || item.firstIndexDate || item.pubYear || "Unknown date",
        authors: cleanText(item.authorString) || "Authors unavailable",
        abstractText: cleanText(item.abstractText) || "No abstract is available from the public metadata response.",
        citedByCount: Number(item.citedByCount || 0),
        doi,
        pmid,
        pmcid: item.pmcid,
        europePmcUrl: `https://europepmc.org/article/${encodeURIComponent(source)}/${encodeURIComponent(recordId)}`,
        tags: inferTags(`${item.title ?? ""} ${item.abstractText ?? ""}`),
      };
    })
    .filter((item) => {
      if (!item.id || seen.has(item.id)) return false;
      seen.add(item.id);
      return true;
    })
    .slice(0, 100);
}

function inferTags(text) {
  const lower = text.toLowerCase();
  const tags = [];
  const checks = [
    ["Reservoir", ["reservoir"]],
    ["Latency", ["latency", "reactivation"]],
    ["bNAbs", ["neutralizing antibod", "bnab"]],
    ["Gene therapy", ["gene therapy", "crispr", "ccr5", "cell therapy"]],
    ["Remission", ["remission", "post-treatment", "art-free"]],
    ["Therapeutic vaccine", ["therapeutic vaccine", "vaccine"]],
  ];

  for (const [label, terms] of checks) {
    if (terms.some((term) => lower.includes(term))) {
      tags.push(label);
    }
  }

  return tags.length ? tags : ["HIV cure research"];
}

function render() {
  const filtered = state.articles.filter((article) => {
    const haystack = [
      article.title,
      article.journal,
      article.authors,
      article.abstractText,
      article.tags.join(" "),
    ]
      .join(" ")
      .toLowerCase();
    return haystack.includes(state.filter.toLowerCase());
  });

  elements.count.textContent = `${filtered.length} of ${state.articles.length} articles`;
  elements.lastUpdated.textContent = `Sorted by latest publication date. Updated ${new Date().toLocaleString()}.`;

  if (!filtered.length) {
    elements.results.innerHTML = '<div class="article-card empty">No matching research items found.</div>';
    return;
  }

  elements.results.innerHTML = filtered.map(renderArticle).join("");
}

function renderArticle(article, index) {
  const abstract = article.abstractText.length > 620
    ? `${article.abstractText.slice(0, 617)}...`
    : article.abstractText;

  const links = [
    `<a href="${escapeAttribute(article.europePmcUrl)}" target="_blank" rel="noreferrer">Europe PMC</a>`,
    article.pmid
      ? `<a href="https://pubmed.ncbi.nlm.nih.gov/${escapeAttribute(article.pmid)}/" target="_blank" rel="noreferrer">PubMed</a>`
      : "",
    article.doi
      ? `<a href="https://doi.org/${escapeAttribute(encodeURIComponent(article.doi))}" target="_blank" rel="noreferrer">DOI</a>`
      : "",
  ].filter(Boolean);

  return `
    <article class="article-card">
      <div class="article-meta">
        <span>#${index + 1}</span>
        <span>${escapeHtml(article.date)}</span>
        <span>${escapeHtml(article.journal)}</span>
        <span>${article.citedByCount} citations</span>
      </div>
      <h2><a href="${escapeAttribute(article.europePmcUrl)}" target="_blank" rel="noreferrer">${escapeHtml(article.title)}</a></h2>
      <p><strong>${escapeHtml(article.authors)}</strong></p>
      <p>${escapeHtml(abstract)}</p>
      <div class="tag-row">${article.tags.map((tag) => `<span class="tag">${escapeHtml(tag)}</span>`).join("")}</div>
      <div class="article-actions">${links.join("")}</div>
    </article>
  `;
}

function setLoading(isLoading) {
  elements.loading.classList.toggle("hidden", !isLoading);
  elements.results.classList.toggle("hidden", isLoading);
  elements.refresh.disabled = isLoading;
}

function cleanText(value) {
  const element = document.createElement("textarea");
  element.innerHTML = value ?? "";
  return element.value.replace(/\s+/g, " ").trim();
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function escapeAttribute(value) {
  return escapeHtml(value).replaceAll("`", "&#096;");
}

function normalizeId(value) {
  return String(value ?? "")
    .replace(/[^A-Za-z0-9._:-]/g, "")
    .slice(0, 128);
}

function normalizeDoi(value) {
  const doi = String(value ?? "").trim();
  if (!/^10\.\d{4,9}\/[-._;()/:A-Z0-9]+$/i.test(doi)) {
    return "";
  }
  return doi.slice(0, 256);
}

elements.filter.addEventListener("input", (event) => {
  state.filter = event.target.value;
  render();
});

elements.topic.addEventListener("change", (event) => {
  state.topic = event.target.value;
  fetchResearch();
});

elements.refresh.addEventListener("click", fetchResearch);

fetchResearch();
