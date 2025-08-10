/* global fetch */
(function () {
  const state = {
    items: [], // { path, name, dir, type: 'image'|'pdf' }
    filtered: [],
    categories: [],
    activeCategory: "ALL",
    typeFilters: new Set(["image", "pdf"]),
    searchQuery: "",
    lightboxIndex: -1,
  };

  const els = {
    categoryNav: document.getElementById("categoryNav"),
    searchInput: document.getElementById("searchInput"),
    grid: document.getElementById("galleryGrid"),
    breadcrumbs: document.getElementById("breadcrumbs"),
    resultStats: document.getElementById("resultStats"),
    gridItemTemplate: document.getElementById("gridItemTemplate"),
    lightbox: document.getElementById("lightbox"),
    lightboxImage: document.getElementById("lightboxImage"),
    lightboxCaption: document.getElementById("lightboxCaption"),
    lightboxClose: document.getElementById("lightboxClose"),
    lightboxPrev: document.getElementById("lightboxPrev"),
    lightboxNext: document.getElementById("lightboxNext"),
  };

  async function loadData() {
    try {
      const res = await fetch("gallery.json", { cache: "no-store" });
      if (!res.ok) throw new Error("failed to load gallery.json");
      const data = await res.json();
      state.items = data.items || [];
      buildCategories();
      applyFilters();
    } catch (e) {
      console.error(e);
      els.grid.innerHTML =
        '<div style="color:#fca5a5">データの読み込みに失敗しました。ローカルで閲覧する場合は簡易サーバを起動してください。</div>';
    }
  }

  function buildCategories() {
    const dirs = new Set(["ALL"]);
    for (const it of state.items) {
      const top = it.dir.split("/")[0] || "";
      if (top) dirs.add(top);
    }
    state.categories = Array.from(dirs);
    renderCategoryNav();
  }

  function renderCategoryNav() {
    els.categoryNav.innerHTML = "";
    for (const cat of state.categories) {
      const btn = document.createElement("button");
      btn.textContent = cat === "ALL" ? "すべて" : cat;
      btn.className = cat === state.activeCategory ? "active" : "";
      btn.addEventListener("click", () => {
        state.activeCategory = cat;
        renderCategoryNav();
        applyFilters();
      });
      els.categoryNav.appendChild(btn);
    }
  }

  function applyFilters() {
    const q = state.searchQuery.trim().toLowerCase();
    state.filtered = state.items.filter((it) => {
      if (!state.typeFilters.has(it.type)) return false;
      if (
        state.activeCategory !== "ALL" &&
        !it.dir.startsWith(state.activeCategory)
      )
        return false;
      if (!q) return true;
      const hay = `${it.name} ${it.path} ${it.dir} ${it.ext}`.toLowerCase();
      return hay.includes(q);
    });
    render();
  }

  function humanCount(n) {
    return new Intl.NumberFormat("ja-JP").format(n);
  }

  function render() {
    // breadcrumbs
    els.breadcrumbs.textContent =
      state.activeCategory === "ALL" ? "すべて" : state.activeCategory;
    els.resultStats.textContent = `${humanCount(state.filtered.length)} 件`;

    // grid
    els.grid.innerHTML = "";
    const frag = document.createDocumentFragment();
    state.filtered.forEach((it, idx) => {
      const node =
        els.gridItemTemplate.content.firstElementChild.cloneNode(true);
      const img = node.querySelector(".thumb");
      const badge = node.querySelector(".thumb-badge");
      const name = node.querySelector(".name");
      const path = node.querySelector(".path");
      name.textContent = it.name;
      name.title = it.name;
      path.textContent = it.dir;
      path.title = it.path;
      badge.dataset.type = it.type;
      badge.textContent = it.type.toUpperCase();

      if (it.type === "pdf") {
        img.src =
          "data:image/svg+xml;utf8," + encodeURIComponent(svgPdfPreview());
      } else {
        img.src = it.path;
      }

      node.addEventListener("click", () => onOpenLightbox(idx));
      frag.appendChild(node);
    });
    els.grid.appendChild(frag);
  }

  function svgPdfPreview() {
    return `<svg xmlns='http://www.w3.org/2000/svg' width='800' height='600'>
      <defs>
        <linearGradient id='g' x1='0' x2='1'>
          <stop offset='0' stop-color='#0ea5b7'/>
          <stop offset='1' stop-color='#a78bfa'/>
        </linearGradient>
      </defs>
      <rect width='100%' height='100%' fill='#0b1220'/>
      <rect x='120' y='80' width='560' height='440' rx='12' fill='url(#g)' opacity='0.2' stroke='#334155'/>
      <text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' font-family='sans-serif' font-size='48' fill='#e5e7eb'>PDF</text>
    </svg>`;
  }

  // Lightbox
  function onOpenLightbox(filteredIndex) {
    state.lightboxIndex = filteredIndex;
    updateLightbox();
    els.lightbox.classList.add("show");
    els.lightbox.setAttribute("aria-hidden", "false");
  }
  function onCloseLightbox() {
    els.lightbox.classList.remove("show");
    els.lightbox.setAttribute("aria-hidden", "true");
    state.lightboxIndex = -1;
  }
  function onPrev() {
    if (state.lightboxIndex <= 0) return;
    state.lightboxIndex -= 1;
    updateLightbox();
  }
  function onNext() {
    if (state.lightboxIndex >= state.filtered.length - 1) return;
    state.lightboxIndex += 1;
    updateLightbox();
  }
  function updateLightbox() {
    const it = state.filtered[state.lightboxIndex];
    if (!it) return;
    if (it.type === "pdf") {
      els.lightboxImage.src =
        "data:image/svg+xml;utf8," + encodeURIComponent(svgPdfPreview());
    } else {
      els.lightboxImage.src = it.path;
    }
    els.lightboxCaption.textContent = `${it.name} — ${it.dir}`;
  }

  // Events
  els.searchInput.addEventListener("input", (e) => {
    state.searchQuery = e.target.value;
    applyFilters();
  });
  document.querySelectorAll(".type-filter").forEach((cb) => {
    cb.addEventListener("change", () => {
      const v = cb.value;
      if (cb.checked) state.typeFilters.add(v);
      else state.typeFilters.delete(v);
      applyFilters();
    });
  });
  els.lightboxClose.addEventListener("click", onCloseLightbox);
  els.lightboxPrev.addEventListener("click", onPrev);
  els.lightboxNext.addEventListener("click", onNext);
  window.addEventListener("keydown", (e) => {
    if (state.lightboxIndex >= 0) {
      if (e.key === "Escape") onCloseLightbox();
      if (e.key === "ArrowLeft") onPrev();
      if (e.key === "ArrowRight") onNext();
    }
  });

  loadData();
})();
