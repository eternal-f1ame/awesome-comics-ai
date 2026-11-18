// Shared by every page. Each page names itself in <body data-page="...">; the list itself comes from papers.json.

// theme: the system setting by default, the reader's choice once made (kept only on this device)
(function () {
  const root = document.documentElement;
  const store = { get() { try { return localStorage.getItem("theme"); } catch (e) { return null; } }, set(v) { try { localStorage.setItem("theme", v); } catch (e) {} } };
  const btns = document.querySelectorAll(".theme button");
  function apply(t) {
    if (t) root.setAttribute("data-theme", t); else root.removeAttribute("data-theme");
    const eff = t || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    btns.forEach(b => b.setAttribute("aria-pressed", String(b.dataset.t === eff)));
  }
  apply(store.get());
  btns.forEach(b => b.addEventListener("click", () => { store.set(b.dataset.t); apply(b.dataset.t); }));
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => apply(store.get()));
})();

(async function () {
  const page = document.body.dataset.page;
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const $ = id => document.getElementById(id);
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  // links to the old one-page sections now open their pages
  const moved = { "#list": "papers.html", "#papers": "papers.html", "#topics": "topics.html", "#why": "essay.html", "#essay": "essay.html", "#tools": "tools.html", "#resources": "tools.html" };
  if (page === "home" && moved[location.hash]) { location.replace(moved[location.hash]); return; }

  // soft reveal as parts come into view
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }), { rootMargin: "0px 0px -8% 0px" });
  const watch = el => reduce ? el.classList.add("in") : io.observe(el);
  document.querySelectorAll(".reveal").forEach(watch);

  let data;
  try { data = await (await fetch("papers.json", { cache: "no-cache" })).json(); }
  catch (e) {
    const p = document.createElement("p"); p.className = "empty"; p.textContent = "The list could not be loaded. Read it in the README on GitHub.";
    document.querySelector("main").insertBefore(p, document.querySelector("footer")); return;
  }
  const { sections, papers, resources } = data;
  const meta = resources.meta || {};
  if (meta.repo) document.querySelectorAll("[data-repo]").forEach(a => { a.href = meta.repo + a.dataset.repo; });

  const years = papers.map(p => p.year), maxY = Math.max(...years), minY = Math.min(...years);
  const recent = papers.filter(p => p.year >= maxY - 2).length;
  const short = t => t.startsWith("Adjacent: ") ? t.slice(10, 11).toUpperCase() + t.slice(11) + " (adjacent)" : t;
  const byCat = id => papers.filter(p => p.category === id);
  const matches = (p, terms) => terms.every(t => (p.title + " " + p.venue + " " + p.year + " " + (p.authors || "")).toLowerCase().includes(t));
  const link = (href, label) => href ? `<a href="${esc(href)}" target="_blank" rel="noopener">${label}&nbsp;↗</a>` : "";
  function row(p) {
    const main = p.paper || (p.arxiv ? "https://arxiv.org/abs/" + p.arxiv : "");
    const ax = p.arxiv && !(p.paper || "").includes(p.arxiv) ? link("https://arxiv.org/abs/" + p.arxiv, "arXiv") : "";
    const venue = p.venue === "arXiv" ? `<span class="venue pre">preprint${p.date ? " " + esc(String(p.date).slice(0, 7)) : ""}</span>` : `<span class="venue">${esc(p.venue)}</span>`;
    return `<div class="paper"><div class="yr mono">${p.year}</div><div><a class="t" href="${esc(main)}" target="_blank" rel="noopener">${esc(p.title)}</a>
      <div class="meta">${venue}<span>${esc(p.authors || "")}</span>${ax}${link(p.code, "Code")}${link(p.project, "Project")}</div></div></div>`;
  }
  const counts = { papers: `${papers.length} papers`, "papers-n": String(papers.length), topics: `${sections.length} topics`, tools: `${resources.tools.length} tools` };
  document.querySelectorAll("[data-count]").forEach(el => { if (counts[el.dataset.count]) el.textContent = counts[el.dataset.count]; });

  ({ home, papers: papersPage, topics, essay, tools }[page] || (() => {}))();

  function home() {
    // numbers, counted up when they come into view
    const venues = new Set(papers.map(p => p.venue)).size;
    const stats = [[papers.length, "papers, each verified"], [sections.length, "topics"], [venues, "venues"], [maxY - minY + 1, `years, ${minY}–${maxY}`]];
    $("stats").innerHTML = stats.map(([n, l]) => `<div><b class="mono" data-n="${n}">${reduce ? n : 0}</b><span>${esc(l)}</span></div>`).join("");
    if (!reduce) {
      const counter = new IntersectionObserver(es => es.forEach(e => {
        if (!e.isIntersecting) return; counter.disconnect();
        e.target.querySelectorAll("b[data-n]").forEach(b => {
          const n = +b.dataset.n, t0 = performance.now();
          const step = t => { const k = Math.min(1, (t - t0) / 1100); b.textContent = Math.round(n * (1 - Math.pow(1 - k, 3))); if (k < 1) requestAnimationFrame(step); };
          requestAnimationFrame(step);
        });
      }), { threshold: .4 });
      counter.observe($("stats"));
    }
    // the newest papers: by year, preprints by their first-version date
    const key = p => p.date ? String(p.date) : `${p.year}-00`;
    $("newest").innerHTML = [...papers].sort((a, b) => key(b).localeCompare(key(a)) || a.title.localeCompare(b.title)).slice(0, 6).map(row).join("");
    // the hero demo: real queries over the real list
    const demoQ = ["speaker", "colorization", "Manga109", "translation", "question answering"];
    const typed = $("typed"), out = $("demo-results");
    const show = query => {
      const hits = papers.filter(p => matches(p, query.toLowerCase().split(/\s+/))).slice(0, 2);
      out.innerHTML = hits.map(p => `<li><span class="venue">${esc(p.venue === "arXiv" ? "preprint" : p.venue)}</span><b>${esc(p.title)}</b></li>`).join("");
      requestAnimationFrame(() => out.querySelectorAll("li").forEach((li, i) => setTimeout(() => li.classList.add("in"), 120 * i)));
    };
    if (reduce) { typed.textContent = demoQ[0]; show(demoQ[0]); return; }
    (async function loop() {
      const wait = ms => new Promise(r => setTimeout(r, ms));
      for (let k = 0; ; k = (k + 1) % demoQ.length) {
        const w = demoQ[k];
        for (let i = 1; i <= w.length; i++) { typed.textContent = w.slice(0, i); await wait(70); }
        show(w); await wait(2600);
        out.querySelectorAll("li").forEach(li => li.classList.remove("in")); await wait(250);
        for (let i = w.length; i >= 0; i--) { typed.textContent = w.slice(0, i); await wait(28); }
        out.innerHTML = ""; await wait(300);
      }
    })();
  }

  function papersPage() {
    // the address keeps the topic and the search, so a filtered list can be shared: papers.html?topic=datasets&q=manga
    const params = new URLSearchParams(location.search);
    let active = sections.some(s => s.id === params.get("topic")) ? params.get("topic") : "all";
    const q = $("q"), chips = $("chips");
    q.value = params.get("q") || "";
    const mk = (id, label, n) => {
      const b = document.createElement("button"); b.className = "chip"; b.type = "button"; b.dataset.id = id;
      b.innerHTML = esc(label) + `<small>${n}</small>`; b.onclick = () => setActive(id, true); chips.appendChild(b);
    };
    mk("all", "All", papers.length);
    sections.forEach(s => mk(s.id, short(s.title), byCat(s.id).length));
    function sync() {
      const u = new URL(location.href);
      u.searchParams.delete("topic"); u.searchParams.delete("q");
      if (active !== "all") u.searchParams.set("topic", active);
      if (q.value.trim()) u.searchParams.set("q", q.value.trim());
      history.replaceState(null, "", u);
    }
    function setActive(id, smooth) {
      active = id;
      [...chips.children].forEach(c => {
        const on = c.dataset.id === active; c.setAttribute("aria-pressed", String(on));
        if (on) chips.scrollTo({ left: c.offsetLeft - (chips.clientWidth - c.offsetWidth) / 2, behavior: smooth && !reduce ? "smooth" : "auto" });   // scrolls the chip row only
      });
      render(); sync();
    }
    ["speaker", "colorization", "Manga109", "translation", "benchmark"].forEach(t => {
      const b = document.createElement("button"); b.className = "pill"; b.type = "button"; b.textContent = t;
      b.onclick = () => { q.value = t; render(); sync(); }; $("try").appendChild(b);
    });
    q.addEventListener("input", () => { render(); sync(); });
    addEventListener("keydown", e => { if (e.key === "/" && document.activeElement !== q) { e.preventDefault(); q.focus(); } });
    function render() {
      const terms = q.value.toLowerCase().split(/\s+/).filter(Boolean);
      let html = "", n = 0;
      sections.forEach((s, i) => {
        if (active !== "all" && active !== s.id) return;
        const ps = byCat(s.id).filter(p => matches(p, terms));
        if (!ps.length) return;
        n += ps.length;
        html += `<div class="group"><div class="ghead"><span class="gn mono">${String(i + 1).padStart(2, "0")}</span><h3>${esc(short(s.title))}</h3><span class="gc mono">${ps.length}</span></div>${ps.map(row).join("")}</div>`;
      });
      $("results").innerHTML = html || '<p class="empty">No paper matches. Try fewer words, or open an issue if a paper is missing.</p>';
      $("count").textContent = terms.length || active !== "all" ? `${n} of ${papers.length} papers` : "";
    }
    setActive(active, false);
  }

  function topics() {
    $("topic-grid").innerHTML = sections.map((s, i) => `<a class="topic glass reveal" href="papers.html?topic=${encodeURIComponent(s.id)}">
      <span class="n mono"><span>${String(i + 1).padStart(2, "0")}</span><em>${byCat(s.id).length} paper${byCat(s.id).length > 1 ? "s" : ""}</em></span>
      <h3>${esc(short(s.title))}</h3><p>${esc(s.blurb)}</p><span class="go mono">Open the papers →</span></a>`).join("");
    $("topic-grid").querySelectorAll(".topic").forEach((el, i) => { el.style.transitionDelay = (i % 4) * 60 + "ms"; watch(el); });
  }

  function essay() {
    $("recent-line").textContent = `Of the ${papers.length} papers on this map, ${recent} appeared in ${maxY - 2}–${maxY}.`;
    $("updated").textContent = meta.updated ? " · updated " + meta.updated : "";
    const span = []; for (let y = minY; y <= maxY; y++) span.push(y);
    const per = span.map(y => papers.filter(p => p.year === y).length), top = Math.max(...per);
    $("bars").innerHTML = per.map((n, i) => `<div class="${span[i] >= maxY - 2 ? "hot" : ""}" data-h="${n ? Math.max(3, 100 * n / top) : 0}" title="${span[i]}: ${n}">${n ? `<span class="mono">${n}</span>` : ""}</div>`).join("");
    $("axis").innerHTML = span.map((y, i) => `<span>${i % 4 === 0 || y === maxY ? "’" + String(y).slice(2) : ""}</span>`).join("");
    $("bars-sub").textContent = `Every paper on the map by year; the last three years in colour (${recent} of ${papers.length}).`;
    const grow = () => $("bars").querySelectorAll("div").forEach(d => { d.style.height = d.dataset.h + "%"; });
    if (reduce) grow(); else new IntersectionObserver((es, o) => es.forEach(e => { if (e.isIntersecting) { grow(); o.disconnect(); } }), { threshold: .3 }).observe($("panel"));
  }

  function tools() {
    const card = (k, h, p, href) => `<a class="card glass reveal" href="${esc(href)}" target="_blank" rel="noopener"><span class="k mono"><span>${esc(k)}</span><span>↗</span></span><h4>${esc(h)}</h4><p>${esc(p)}</p></a>`;
    $("tool-cards").innerHTML = resources.tools.map(t => card("tool", t.name, t.what, t.url)).join("");
    $("workshop-cards").innerHTML = resources.workshops.map(w => card("workshop", w.name, w.what, w.url)).join("");
    $("list-cards").innerHTML = resources.related.map(r => card("list", r.name, r.what, r.url)).join("");
    document.querySelectorAll(".cards .card").forEach(watch);
  }
})();
