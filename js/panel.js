// ── Panel logic ──
const panel = document.getElementById("panel");
const panelContent = document.getElementById("panel-content");
const panelClose = document.getElementById("panel-close");
const graphContainer = document.getElementById("graph-container");

panelClose.addEventListener("click", closePanel);

function openPanel(aesthetic) {
  // Build related aesthetics from connections
  const related = connections
    .filter(c => c.source === aesthetic.id || c.target === aesthetic.id ||
                 (typeof c.source === "object" && c.source.id === aesthetic.id) ||
                 (typeof c.target === "object" && c.target.id === aesthetic.id))
    .map(c => {
      const sid = typeof c.source === "object" ? c.source.id : c.source;
      const tid = typeof c.target === "object" ? c.target.id : c.target;
      const otherId = sid === aesthetic.id ? tid : sid;
      const other = aesthetics.find(a => a.id === otherId);
      return { id: otherId, name: other?.name || otherId, label: c.label || "" };
    });

  const familyColor = FAMILIES[aesthetic.family]?.color || "#eee";
  const familyStroke = FAMILIES[aesthetic.family]?.stroke || "#ccc";

  const tags = aesthetic.tags || [];
  const elements = aesthetic.elements || [];
  const brands = aesthetic.brands || [];
  const references = aesthetic.references || [];
  const images = aesthetic.images || [];
  const description = aesthetic.description || "";
  const tagline = aesthetic.tagline || "";

  // Star size label
  const sizeLabels = { 1: "emerging", 2: "niche", 3: "established", 4: "popular", 5: "viral" };
  const sizeLabel = sizeLabels[aesthetic.size] || "";

  panelContent.innerHTML = `
    <div class="panel-header">
      <h2>${aesthetic.name}</h2>
      ${tagline ? `<p class="tagline">${tagline}</p>` : ""}
      <div class="panel-tags">
        <span class="panel-tag family-tag" style="background:${familyColor};border:1px solid ${familyStroke}">${aesthetic.family}</span>
        ${sizeLabel ? `<span class="panel-tag">${sizeLabel}</span>` : ""}
        ${tags.map(t => `<span class="panel-tag">${t}</span>`).join("")}
      </div>
    </div>

    ${description ? `
    <div class="panel-section">
      <p>${description}</p>
    </div>
    ` : ""}

    ${elements.length > 0 ? `
    <div class="key-elements">
      <h3>Key Elements</h3>
      <ul>
        ${elements.map(e => `<li>${e}</li>`).join("")}
      </ul>
    </div>
    ` : ""}

    ${images.length > 0 ? `
    <div class="panel-section">
      <h3>Mood Board</h3>
      <div class="mood-grid">
        ${images.map(img => `<img src="${img}" alt="${aesthetic.name}" loading="lazy">`).join("")}
      </div>
    </div>
    ` : `
    <div class="panel-section">
      <h3>Mood Board</h3>
      <div class="mood-grid">
        ${generatePlaceholders(aesthetic)}
      </div>
    </div>
    `}

    ${brands.length > 0 ? `
    <div class="panel-section">
      <h3>Brands</h3>
      <ul>
        ${brands.map(b => `<li>${b}</li>`).join("")}
      </ul>
    </div>
    ` : ""}

    ${references.length > 0 ? `
    <div class="panel-section">
      <h3>Cultural References</h3>
      <ul>
        ${references.map(r => `<li>${r}</li>`).join("")}
      </ul>
    </div>
    ` : ""}

    ${related.length > 0 ? `
    <div class="panel-section">
      <h3>Connected Aesthetics</h3>
      <div class="related-list">
        ${related.map(r => `
          <button class="related-chip" onclick="navigateToNode('${r.id}')">
            ${r.name}${r.label ? ` <span style="color:#aaa;font-size:11px">&middot; ${r.label}</span>` : ""}
          </button>
        `).join("")}
      </div>
    </div>
    ` : ""}
  `;

  panel.classList.remove("hidden");
  panel.classList.add("open");
  graphContainer.classList.add("shifted");
  panel.scrollTop = 0;

  // Update URL
  history.pushState({ id: aesthetic.id }, "", `#${aesthetic.id}`);
}

function closePanel() {
  panel.classList.remove("open");
  graphContainer.classList.remove("shifted");
  setTimeout(() => {
    if (!panel.classList.contains("open")) {
      panel.classList.add("hidden");
    }
  }, 400);
  history.pushState(null, "", window.location.pathname);
}

// Generate colored placeholder blocks for aesthetics without images
function generatePlaceholders(aesthetic) {
  const baseColor = FAMILIES[aesthetic.family]?.color || "#eee";
  const elements = aesthetic.elements || [];
  const count = 4;
  let html = "";
  for (let i = 0; i < count; i++) {
    html += `<div style="
      flex:0 0 auto;
      width:180px;
      aspect-ratio:3/4;
      border-radius:10px;
      background: ${baseColor};
      display:flex;
      align-items:center;
      justify-content:center;
      font-family:'Caveat',cursive;
      font-size:14px;
      color:#aaa;
    ">${elements[i] || ""}</div>`;
  }
  return html;
}

// Handle browser back/forward
window.addEventListener("popstate", (e) => {
  if (e.state?.id) {
    const node = aesthetics.find(a => a.id === e.state.id);
    if (node) openPanel(node);
  } else {
    closePanel();
  }
});

// Handle direct hash links
window.addEventListener("load", () => {
  const hash = window.location.hash.slice(1);
  if (hash) {
    const node = aesthetics.find(a => a.id === hash);
    if (node) setTimeout(() => openPanel(node), 500);
  }
});
