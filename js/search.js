// ── Search + Browse logic ──

// ── Search ──
const searchInput = document.getElementById("search-input");
const searchResults = document.getElementById("search-results");

searchInput.addEventListener("input", () => {
  const q = searchInput.value.trim().toLowerCase();
  if (q.length < 2) {
    searchResults.classList.remove("active");
    searchResults.innerHTML = "";
    return;
  }

  const matches = aesthetics
    .filter(a => a.name.toLowerCase().includes(q))
    .sort((a, b) => {
      // Exact start match first, then by size (bigger = more relevant)
      const aStarts = a.name.toLowerCase().startsWith(q) ? 0 : 1;
      const bStarts = b.name.toLowerCase().startsWith(q) ? 0 : 1;
      if (aStarts !== bStarts) return aStarts - bStarts;
      return (b.size || 1) - (a.size || 1);
    })
    .slice(0, 12);

  if (matches.length === 0) {
    searchResults.innerHTML = `<div class="search-item" style="color:#aaa;cursor:default">no results</div>`;
  } else {
    searchResults.innerHTML = matches.map(a => `
      <div class="search-item" data-id="${a.id}">
        <span>${highlightMatch(a.name, q)}</span>
        <span class="family-hint">${a.family}</span>
      </div>
    `).join("");
  }
  searchResults.classList.add("active");
});

function highlightMatch(name, query) {
  const i = name.toLowerCase().indexOf(query);
  if (i === -1) return name;
  return name.slice(0, i) + `<strong>${name.slice(i, i + query.length)}</strong>` + name.slice(i + query.length);
}

searchResults.addEventListener("click", (e) => {
  const item = e.target.closest(".search-item");
  if (!item || !item.dataset.id) return;
  navigateToNode(item.dataset.id);
  searchInput.value = "";
  searchResults.classList.remove("active");
  searchResults.innerHTML = "";
});

// Close search on outside click
document.addEventListener("click", (e) => {
  if (!e.target.closest("#search-bar")) {
    searchResults.classList.remove("active");
  }
});

// Close search on Escape
searchInput.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    searchInput.blur();
    searchResults.classList.remove("active");
  }
});

// ── A-Z Browse ──
const browseToggle = document.getElementById("browse-toggle");
const browseMenu = document.getElementById("browse-menu");
const browseClose = document.getElementById("browse-close");
const browseLetters = document.getElementById("browse-letters");
const browseList = document.getElementById("browse-list");

let browseOpen = false;

browseToggle.addEventListener("click", () => {
  if (browseOpen) {
    closeBrowse();
  } else {
    openBrowse();
  }
});

browseClose.addEventListener("click", closeBrowse);

function openBrowse() {
  browseOpen = true;
  browseMenu.classList.remove("hidden");
  browseMenu.classList.add("open");
  buildBrowseList();
}

function closeBrowse() {
  browseOpen = false;
  browseMenu.classList.remove("open");
  setTimeout(() => {
    if (!browseMenu.classList.contains("open")) {
      browseMenu.classList.add("hidden");
    }
  }, 350);
}

function buildBrowseList() {
  // Group aesthetics by first letter
  const sorted = [...aesthetics].sort((a, b) => a.name.localeCompare(b.name));
  const groups = {};
  const usedLetters = new Set();

  sorted.forEach(a => {
    const letter = a.name[0].toUpperCase();
    if (!groups[letter]) groups[letter] = [];
    groups[letter].push(a);
    usedLetters.add(letter);
  });

  // Letter buttons
  const allLetters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
  browseLetters.innerHTML = allLetters.map(l => {
    const has = usedLetters.has(l);
    return `<button class="letter-btn${has ? "" : " disabled"}" data-letter="${l}"${has ? "" : " disabled"}>${l}</button>`;
  }).join("");

  // List with letter group headers
  let html = "";
  allLetters.forEach(l => {
    if (!groups[l]) return;
    html += `<div class="browse-letter-group" id="browse-${l}">${l}</div>`;
    groups[l].forEach(a => {
      html += `<div class="browse-item" data-id="${a.id}">
        <span>${a.name}</span>
        <span class="family-hint">${a.family}</span>
      </div>`;
    });
  });
  browseList.innerHTML = html;

  // Letter click → scroll to group
  browseLetters.addEventListener("click", (e) => {
    const btn = e.target.closest(".letter-btn");
    if (!btn || btn.disabled) return;
    const letter = btn.dataset.letter;
    const target = document.getElementById(`browse-${letter}`);
    if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });

    browseLetters.querySelectorAll(".letter-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
  });

  // Item click → navigate
  browseList.addEventListener("click", (e) => {
    const item = e.target.closest(".browse-item");
    if (!item || !item.dataset.id) return;
    navigateToNode(item.dataset.id);
    closeBrowse();
  });
}
