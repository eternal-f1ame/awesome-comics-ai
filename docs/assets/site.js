// Shared by every page. Each page names itself in <body data-page="...">; the list itself comes from papers.json.
// The first visit loads the data, the five pages and the blog posts once. After that, a link between the pages swaps
// only the content of <main>: no reload, the header and the footer stay, and the line under the current page slides to
// the new one. A blog post is a file named blog-<slug>.html; its tab is Blog.

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

(function () {
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const $ = id => document.getElementById(id);
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const PAGE_OF = { "index.html": "home", "papers.html": "papers", "topics.html": "topics", "blog.html": "blog", "news.html": "news", "tools.html": "tools" };
  const TAB_OF = { post: "blog" };                                             // the tab that a page lights up
  const MOVED = { "essay.html": "blog-comics-are-a-modality.html" };           // old files, now elsewhere
  const isPost = f => /^blog-[a-z0-9-]+\.html$/.test(f);
  const dir = location.pathname.replace(/[^/]*$/, "");
  function fileOf(href) {
    let u; try { u = new URL(href, location.href); } catch (e) { return null; }
    if (u.origin !== location.origin || !u.pathname.startsWith(dir)) return null;
    const f = u.pathname.slice(dir.length) || "index.html";
    return PAGE_OF[f] || isPost(f) || MOVED[f] ? f : null;
  }

  // links to the old one-page sections open their pages
  const moved = { "#list": "papers.html", "#papers": "papers.html", "#topics": "topics.html", "#why": MOVED["essay.html"], "#essay": MOVED["essay.html"], "#tools": "tools.html", "#resources": "tools.html" };
  if (document.body.dataset.page === "home" && moved[location.hash]) { location.replace(moved[location.hash]); return; }

  // ---- the pages, each fetched once and kept ----
  const cache = new Map();
  const snapshot = d => ({ title: d.title, page: d.body.dataset.page, main: d.querySelector("main").innerHTML });
  cache.set(fileOf(location.href), Promise.resolve(snapshot(document)));   // taken before this page renders anything
  function load(file) {
    if (!cache.has(file)) cache.set(file, fetch(file).then(r => { if (!r.ok) throw new Error(r.status); return r.text(); })
      .then(t => snapshot(new DOMParser().parseFromString(t, "text/html")))
      .catch(e => { cache.delete(file); throw e; }));
    return cache.get(file);
  }

  // ---- the line under the current page (above it, in the phone's bottom bar) ----
  const nav = document.querySelector(".nav");
  const pill = document.createElement("span");
  pill.className = "nav-line"; pill.setAttribute("aria-hidden", "true");
  nav.prepend(pill);
  let current = document.body.dataset.page;
  function setNav(page, instant) {
    let on = null;
    const want = TAB_OF[page] || page;
    nav.querySelectorAll("a.tab").forEach(t => {
      const yes = PAGE_OF[fileOf(t.href)] === want;
      t.classList.toggle("on", yes);
      if (yes) { t.setAttribute("aria-current", "page"); on = t; } else t.removeAttribute("aria-current");
    });
    if (!on) { pill.style.opacity = "0"; return; }
    const hidden = pill.style.opacity !== "1";
    if (instant || hidden || reduce) pill.style.transition = "none";
    const bottom = getComputedStyle(nav).position === "fixed", label = on.querySelector("span") || on;
    const w = bottom ? Math.max(label.offsetWidth, 24) : label.offsetWidth;
    const x = bottom ? on.offsetLeft + (on.offsetWidth - w) / 2 : on.offsetLeft + label.offsetLeft;
    pill.style.width = w + "px";
    pill.style.transform = `translate(${x}px, ${bottom ? 0 : on.offsetTop + on.offsetHeight - 1}px)`;
    if (instant || hidden || reduce) { void pill.offsetWidth; pill.style.transition = ""; }
    pill.style.opacity = "1";
  }
  setNav(current, true);
  addEventListener("resize", () => setNav(current, true));
  if (document.fonts) document.fonts.ready.then(() => setNav(current, true));

  // ---- soft reveal as parts come into view ----
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }), { rootMargin: "0px 0px -8% 0px" });
  const watch = el => reduce ? el.classList.add("in") : io.observe(el);

  // ---- the data, loaded once ----
  const dataP = fetch("papers.json", { cache: "no-cache" }).then(r => r.json());
  let sections, papers, resources, posts, news, meta, maxY, minY, recent;
  const short = t => t.startsWith("Adjacent: ") ? t.slice(10, 11).toUpperCase() + t.slice(11) + " (adjacent)" : t;
  const byCat = id => papers.filter(p => p.category === id);
  const topicName = id => short((sections.find(s => s.id === id) || { title: id }).title);
  // when a paper appeared, for sorting newest first: a preprint's first-version day; else its year, with the month of its arXiv id
  // when that id is from the same year (2507.10053 is July 2025); else the year alone, after the dated papers of that year
  const when = p => {
    if (p.date) return String(p.date);
    const m = /^(\d{2})(\d{2})\./.exec(String(p.arxiv || ""));
    return m && 2000 + +m[1] === p.year ? `${p.year}-${m[2]}` : `${p.year}-00`;
  };
  const chrono = list => [...list].sort((a, b) => when(b).localeCompare(when(a)) || a.title.localeCompare(b.title));
  const matches = (p, terms) => terms.every(t => (p.title + " " + p.venue + " " + p.year + " " + (p.authors || "") + " " + topicName(p.category)).toLowerCase().includes(t));
  const link = (href, label) => href ? `<a href="${esc(href)}" target="_blank" rel="noopener">${label}&nbsp;↗</a>` : "";
  function row(p, active) {
    const main = p.paper || (p.arxiv ? "https://arxiv.org/abs/" + p.arxiv : "");
    const ax = p.arxiv && !(p.paper || "").includes(p.arxiv) ? link("https://arxiv.org/abs/" + p.arxiv, "arXiv") : "";
    const venue = p.venue === "arXiv" ? `<span class="venue pre">preprint${p.date ? " " + esc(String(p.date).slice(0, 7)) : ""}</span>` : `<span class="venue">${esc(p.venue)}</span>`;
    return `<div class="paper"><div class="yr">${p.year}</div><div class="pb"><a class="t" href="${esc(main)}" target="_blank" rel="noopener">${esc(p.title)}</a>
      <div class="meta"><a class="tag${active === p.category ? " on" : ""}" href="papers.html?topic=${encodeURIComponent(p.category)}" data-topic="${esc(p.category)}">${esc(topicName(p.category))}</a><span>${esc(p.authors || "")}</span>${ax}${link(p.code, "Code")}${link(p.project, "Project")}</div></div><div class="pv">${venue}</div></div>`;
  }

  // ---- render the page that is in <main> now ----
  let gen = 0;   // each render gets a number; work left over from a page that was left stops itself
  async function mount(page) {
    const my = ++gen;
    document.querySelectorAll("main .reveal").forEach(watch);
    if (!papers) {
      try { ({ sections, papers, resources, posts = [], news = [] } = await dataP); }
      catch (e) {
        const p = document.createElement("p"); p.className = "empty"; p.textContent = "The list could not be loaded. Read it in the README on GitHub.";
        document.querySelector("main").appendChild(p); return;
      }
      meta = resources.meta || {};
      const years = papers.map(p => p.year); maxY = Math.max(...years); minY = Math.min(...years);
      recent = papers.filter(p => p.year >= maxY - 2).length;
      setTimeout(() => [...Object.keys(PAGE_OF), ...posts.map(p => p.file)].forEach(f => load(f).catch(() => {})), 300);   // preload the other pages and the posts
    }
    if (my !== gen) return;
    if (meta.repo) document.querySelectorAll("[data-repo]").forEach(a => { a.href = meta.repo + a.dataset.repo; });
    if ($("updated-foot") && meta.updated) $("updated-foot").textContent = "Updated " + meta.updated;
    const counts = { papers: `${papers.length} papers`, "papers-n": String(papers.length), topics: `${sections.length} topics`, tools: `${resources.tools.length} tools` };
    document.querySelectorAll("main [data-count]").forEach(el => { if (counts[el.dataset.count]) el.textContent = counts[el.dataset.count]; });
    ({ home, papers: papersPage, topics, blog, post, tools, news: newsPage }[page] || (() => {}))(my);
  }

  // ---- move between pages without a reload ----
  let navTo = 0;
  async function go(url, push) {
    let file = fileOf(url.href);
    if (MOVED[file]) { file = MOVED[file]; url = new URL(file, location.href); }
    const my = ++navTo;
    let next;
    try { next = await load(file); } catch (e) { location.href = url.href; return; }
    if (my !== navTo) return;
    if (push) { history.replaceState({ ...(history.state || {}), y: scrollY }, ""); history.pushState({ y: 0 }, "", url.href); }
    const y = push ? 0 : ((history.state && history.state.y) || 0);
    current = next.page;
    setNav(current, false);   // the pill starts to slide while the old content fades
    const main = document.querySelector("main");
    let out = null;
    if (!reduce) { out = main.animate([{ opacity: 1, transform: "none" }, { opacity: 0, transform: "translateY(6px)" }], { duration: 130, easing: "ease-in", fill: "forwards" }); await out.finished; }
    if (my !== navTo) { if (out) out.cancel(); return; }
    main.innerHTML = next.main;
    document.title = next.title;
    document.body.dataset.page = next.page;
    mount(next.page);   // draws the page first, so that the old scroll position exists again
    scrollTo({ top: y, behavior: "instant" });
    if (!reduce) main.animate([{ opacity: 0, transform: "translateY(10px)" }, { opacity: 1, transform: "none" }], { duration: 300, easing: "cubic-bezier(.2,.8,.2,1)" });
    if (out) out.cancel();
  }
  document.addEventListener("click", e => {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    const a = e.target.closest("a[href]");
    if (!a || a.target === "_blank" || a.hasAttribute("download") || !fileOf(a.href)) return;
    e.preventDefault();
    const url = new URL(a.href, location.href);
    if (url.href === location.href) { scrollTo({ top: 0, behavior: reduce ? "instant" : "smooth" }); return; }
    go(url, true);
  });
  addEventListener("popstate", () => { if (fileOf(location.href)) go(new URL(location.href), false); });
  history.scrollRestoration = "manual";
  let saveT;   // remember where the reader was on this page, for Back and Forward
  addEventListener("scroll", () => { clearTimeout(saveT); saveT = setTimeout(() => history.replaceState({ ...(history.state || {}), y: scrollY }, ""), 250); }, { passive: true });
  addEventListener("keydown", e => { const q = $("q"); if (e.key === "/" && q && document.activeElement !== q) { e.preventDefault(); q.focus(); } });

  mount(current).then(() => { if (history.state && history.state.y) scrollTo({ top: history.state.y, behavior: "instant" }); });

  // ---- the pages ----
  function home(my) {
    // numbers, counted up when they come into view
    const venues = new Set(papers.map(p => p.venue)).size;
    const stats = [[papers.length, "papers, each verified"], [sections.length, "topics"], [venues, "venues"], [maxY - minY + 1, `years, ${minY}–${maxY}`]];
    $("stats").innerHTML = stats.map(([n, l]) => `<div><b data-n="${n}">${reduce ? n : 0}</b><span>${esc(l)}</span></div>`).join("");
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
    // the newest papers, by the same order as the list
    $("newest").innerHTML = chrono(papers).slice(0, 6).map(p => row(p)).join("");
    newsTiles();
  }

  // a news item as a tile; a sponsored one is marked and carries rel="sponsored"
  const newsKind = { industry: "Industry", research: "Research", sponsored: "Sponsored" };
  function newsTile(n) {
    const ad = n.kind === "sponsored";
    const when = new Date(String(n.date) + "T12:00:00Z").toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });
    return `<div class="cell reveal"><a class="tile ${ad ? "ad" : "plain"}" href="${esc(n.url)}" target="_blank" rel="${ad ? "sponsored noopener" : "noopener"}">
      <span class="k"><span>${newsKind[n.kind] || "News"}</span><em>${esc(ad ? n.sponsor : when)}</em></span>
      <h3>${esc(n.title)}</h3><p>${esc(n.note)}</p><span class="go">${esc(n.source)} ↗</span></a></div>`;
  }
  const askUrl = () => ((meta && meta.repo) || "https://github.com/eternal-f1ame/awesome-comics-ai") + "/issues/new?template=advertise.yml";
  // The form behind the "Advertise here!" box sends its fields to Web3Forms, which mails them to the maintainers. The key is
  // public by design: it only names the inbox. Without a key the box opens the GitHub issue form, as before.
  const FORM_KEY = "";
  const reveal = box => box.querySelectorAll(".cell").forEach((el, i) => { el.style.transitionDelay = (i % 3) * 60 + "ms"; watch(el); });

  // the box that invites more, always the sixth tile: after the newest five, as on the home page
  const askBody = go => `<span class="k"><span>Your work here</span></span><h3>Relevant content? Advertise here!</h3>
      <p>Put a paper, dataset, tool, platform or event in front of the people who read this map. Sponsored items are always marked.</p><span class="go">${go}</span>`;
  const askTile = () => FORM_KEY
    ? `<div class="cell reveal"><button class="tile sun" type="button" data-ask aria-haspopup="dialog">${askBody("Get in touch →")}</button></div>`
    : `<div class="cell reveal"><a class="tile sun" href="${esc(askUrl())}" target="_blank" rel="noopener">${askBody("Get in touch ↗")}</a></div>`;

  // the form itself: one dialog, made on first use and kept outside <main>, so a page swap leaves it alone
  const FEATURES = ["A sponsored placement (advertisement)", "Research, a dataset or a benchmark release", "A tool or a product", "An event, a workshop or a call for papers", "Industry news from a comic, manga or webtoon platform"];
  function askDialog() {
    let d = $("ask");
    if (d) return d;
    const field = (id, label, input, note = "") => `<div class="field"><label for="ask-${id}">${label}</label>${input}${note ? `<p class="note">${note}</p>` : ""}</div>`;
    document.body.insertAdjacentHTML("beforeend", `<dialog class="ask" id="ask" aria-labelledby="ask-title">
      <form class="ask-form" novalidate>
        <button class="ask-x" type="button" value="close" aria-label="Close">×</button>
        <p class="eyebrow">Advertise</p>
        <h2 id="ask-title">Relevant content? Tell us about it.</h2>
        <p class="ask-lead">Papers, datasets, tools, platforms and events about comics, manga or webtoons. A sponsored placement is always marked <b>Sponsored</b>. We reply by email.</p>
        <div class="ask-grid">
          ${field("feature", "What would you like to feature?", `<span class="pick"><select id="ask-feature" name="feature" required><option value="">Choose one</option>${FEATURES.map(f => `<option>${esc(f)}</option>`).join("")}</select><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></span>`)}
          ${field("work", "Name", `<input id="ask-work" name="work" required maxlength="200" autocomplete="off">`, "The work, product, event or organisation.")}
          ${field("link", "Link", `<input id="ask-link" name="link" type="url" required maxlength="500" placeholder="https://">`)}
          ${field("about", "In one or two sentences", `<textarea id="ask-about" name="about" required rows="3" maxlength="1200"></textarea>`, "What it is and why it matters to people who work on comics and AI.")}
          ${field("dates", "Dates", `<input id="ask-dates" name="dates" maxlength="120">`, "Optional. When it should run, or the date of the event or release.")}
          <div class="two">
            ${field("name", "Your name", `<input id="ask-name" name="name" required maxlength="120" autocomplete="name">`)}
            ${field("email", "Your email", `<input id="ask-email" name="email" type="email" required maxlength="200" autocomplete="email">`, "Used only to reply.")}
          </div>
          <label class="check"><input type="checkbox" name="scope" value="yes" required><span>It is about comics, manga, manhwa, webtoons or other sequential art.</span></label>
          <input class="trap" type="checkbox" name="botcheck" tabindex="-1" autocomplete="off" aria-hidden="true">
        </div>
        <div class="ask-end"><button class="btn primary" type="submit">Send</button><p class="ask-status" role="status" aria-live="polite"></p></div>
      </form>
      <div class="ask-done" hidden><p class="eyebrow">Sent</p><h2>Thank you.</h2><p class="ask-lead">Your note is with the maintainers, and we will reply by email.</p><button class="btn" type="button" value="close">Close</button></div>
    </dialog>`);
    d = $("ask");
    const form = d.querySelector("form"), status = d.querySelector(".ask-status"), send = form.querySelector('[type="submit"]');
    const close = () => { if (reduce || !d.animate) { d.close(); return; } d.animate([{ opacity: 1, transform: "none" }, { opacity: 0, transform: "translateY(0.5rem)" }], { duration: 140, easing: "ease-in" }).finished.then(() => d.close()); };
    d.addEventListener("click", e => { if (e.target === d || (e.target.closest("button") && e.target.closest("button").value === "close")) close(); });   // a click on the backdrop, the cross or Close
    d.addEventListener("cancel", e => { e.preventDefault(); close(); });                                                                             // Escape
    form.addEventListener("submit", async e => {
      e.preventDefault();
      form.classList.add("tried");
      if (!form.checkValidity()) { status.textContent = "Please fill in the marked fields."; const bad = form.querySelector(":invalid"); if (bad) bad.focus(); return; }
      const data = Object.fromEntries(new FormData(form));
      send.disabled = true; status.textContent = "Sending…";
      try {
        const r = await fetch("https://api.web3forms.com/submit", { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify({ access_key: FORM_KEY, subject: `Advertise: ${data.work} (${data.feature})`, from_name: "Comics & Manga AI", ...data }) });
        const j = await r.json().catch(() => ({}));
        if (!r.ok || !j.success) throw new Error(j.message || String(r.status));
        form.hidden = true; d.querySelector(".ask-done").hidden = false; d.querySelector(".ask-done .btn").focus();
      } catch (err) {
        status.innerHTML = `Sending failed. Please try again, or <a href="${esc(askUrl())}" target="_blank" rel="noopener">open a GitHub issue</a>.`;
      } finally { send.disabled = false; }
    });
    return d;
  }
  document.addEventListener("click", e => {
    const b = e.target.closest("[data-ask]");
    if (!b || !FORM_KEY) return;
    const d = askDialog();
    if (d.open) return;
    const form = d.querySelector("form");
    if (form.hidden) { form.reset(); form.classList.remove("tried"); form.hidden = false; d.querySelector(".ask-done").hidden = true; d.querySelector(".ask-status").textContent = ""; }
    d.showModal();
    if (!reduce && d.animate) d.animate([{ opacity: 0, transform: "translateY(0.75rem)" }, { opacity: 1, transform: "none" }], { duration: 260, easing: "cubic-bezier(.2,.8,.2,1)" });
    d.querySelector("select").focus();
  });
  const newsOrder = () => [...news.filter(n => n.kind === "sponsored"), ...news.filter(n => n.kind !== "sponsored")];
  const withAsk = items => items.slice(0, 5).map(newsTile).join("") + askTile() + items.slice(5).map(newsTile).join("");

  // the home page's "Around the field": at most two sponsored items, then the newest news, five in all, then the box
  function newsTiles() {
    if (!$("news")) return;
    const items = [...news.filter(n => n.kind === "sponsored").slice(0, 2), ...news.filter(n => n.kind !== "sponsored")].slice(0, 5);
    $("news").innerHTML = withAsk(items);
    reveal($("news"));
  }

  // the News page: the same grid, with every item
  function newsPage() {
    $("news-list").innerHTML = withAsk(newsOrder());
    reveal($("news-list"));
  }

  function papersPage() {
    // one list, newest first, whatever the topic; a topic is a tag, and the menu (or a click on a tag) filters by it. Published
    // papers only, until the reader includes the preprints. The address keeps all three, so a filtered list can be shared:
    // papers.html?topic=datasets&q=manga&preprints=1
    const params = new URLSearchParams(location.search);
    const q = $("q"), pick = $("topic"), pre = $("preprints"), all = chrono(papers);
    const isPre = p => p.venue === "arXiv";
    let withPre = params.get("preprints") === "1";
    pick.innerHTML = `<option value="all"></option>` + sections.map(s => `<option value="${esc(s.id)}"></option>`).join("");
    pick.value = sections.some(s => s.id === params.get("topic")) ? params.get("topic") : "all";
    q.value = params.get("q") || "";
    function sync() {
      const u = new URL(location.href);
      ["topic", "q", "preprints"].forEach(k => u.searchParams.delete(k));
      if (pick.value !== "all") u.searchParams.set("topic", pick.value);
      if (q.value.trim()) u.searchParams.set("q", q.value.trim());
      if (withPre) u.searchParams.set("preprints", "1");
      if (u.href !== location.href) history.replaceState(history.state, "", u);
    }
    ["speaker", "colorization", "Manga109", "translation", "benchmark"].forEach(t => {
      const b = document.createElement("button"); b.className = "pill"; b.type = "button"; b.textContent = t;
      b.onclick = () => { q.value = t; render(); sync(); }; $("try").appendChild(b);
    });
    q.addEventListener("input", () => { render(); sync(); });
    pick.addEventListener("change", () => { render(); sync(); });
    pre.addEventListener("click", () => { withPre = !withPre; render(); sync(); });
    $("results").addEventListener("click", e => {          // a tag filters this list in place
      const t = e.target.closest("[data-topic]");
      if (!t) return;
      e.preventDefault(); pick.value = t.dataset.topic; render(); sync();
      scrollTo({ top: $("results").getBoundingClientRect().top + scrollY - 160, behavior: reduce ? "instant" : "smooth" });
    });
    function render() {
      const terms = q.value.toLowerCase().split(/\s+/).filter(Boolean);
      const shown = all.filter(p => withPre || !isPre(p));
      // the menu counts what the reader would see: published papers, or every paper once preprints are in
      pick.options[0].textContent = `All topics (${shown.length})`;
      sections.forEach((s, i) => { pick.options[i + 1].textContent = `${short(s.title)} (${shown.filter(p => p.category === s.id).length})`; });
      const hits = all.filter(p => (pick.value === "all" || p.category === pick.value) && matches(p, terms));
      const ps = hits.filter(p => withPre || !isPre(p)), nPre = hits.filter(isPre).length;
      pick.closest(".pick").classList.toggle("on", pick.value !== "all");
      pre.setAttribute("aria-pressed", String(withPre));
      pre.querySelector("small").textContent = nPre;
      const kind = withPre ? "papers" : "published papers";
      $("results").innerHTML = ps.map(p => row(p, pick.value)).join("") ||
        `<p class="empty">No ${kind} match. ${!withPre && nPre ? `Include the preprints to see ${nPre} more.` : "Try fewer words or another topic, or open an issue if a paper is missing."}</p>`;
      const filtered = terms.length || pick.value !== "all";
      $("count").textContent = `${filtered ? `${ps.length} of ${shown.length}` : ps.length} ${kind}, newest first` + (withPre && nPre ? `, ${ps.filter(isPre).length} of them preprints` : "");
    }
    render(); sync();
  }

  function topics() {
    $("topic-grid").innerHTML = sections.map((s, i) => { const n = byCat(s.id).length; return `<div class="cell reveal"><a class="tile plain" href="papers.html?topic=${encodeURIComponent(s.id)}">
      <span class="k"><span>${String(i + 1).padStart(2, "0")}</span><em>${n} paper${n > 1 ? "s" : ""}</em></span>
      <h3>${esc(short(s.title))}</h3><p>${esc(s.blurb)}</p><span class="go">Open the papers →</span></a></div>`; }).join("");
    $("topic-grid").querySelectorAll(".cell").forEach((el, i) => { el.style.transitionDelay = (i % 3) * 60 + "ms"; watch(el); });
  }

  function blog() {
    if (!posts.length) return;
    const fmt = d => new Date(d + "T12:00:00Z").toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });
    $("posts").innerHTML = [...posts].sort((a, b) => String(b.date).localeCompare(String(a.date))).map((p, i) => `<div class="cell reveal"><a class="tile ${i === 0 ? "ink" : "plain"}" href="${esc(p.file)}">
      <span class="k"><time datetime="${esc(p.date)}">${esc(fmt(String(p.date)))}</time><em>${p.minutes} min read</em></span>
      <h3>${esc(p.title)}</h3><p>${esc(p.dek)}</p><span class="go">Read the post →</span></a></div>`).join("");
    $("posts").querySelectorAll(".cell").forEach(watch);
  }

  function post() {
    if (!$("recent-line")) return;
    $("recent-line").textContent = `Of the ${papers.length} papers on this map, ${recent} appeared in ${maxY - 2}–${maxY}.`;
    if ($("updated")) $("updated").textContent = meta.updated ? " · updated " + meta.updated : "";
    const span = []; for (let y = minY; y <= maxY; y++) span.push(y);
    const per = span.map(y => papers.filter(p => p.year === y).length), top = Math.max(...per);
    $("bars").innerHTML = per.map((n, i) => `<div class="${span[i] >= maxY - 2 ? "hot" : ""}" data-h="${n ? Math.max(3, 100 * n / top) : 0}" title="${span[i]}: ${n}">${n ? `<span class="mono">${n}</span>` : ""}</div>`).join("");
    $("axis").innerHTML = span.map((y, i) => `<span>${i % 4 === 0 || y === maxY ? "’" + String(y).slice(2) : ""}</span>`).join("");
    $("bars-sub").textContent = `Every paper on the map by year; the last three years in colour (${recent} of ${papers.length}).`;
    const grow = () => $("bars").querySelectorAll("div").forEach(d => { d.style.height = d.dataset.h + "%"; });
    if (reduce) grow(); else new IntersectionObserver((es, o) => es.forEach(e => { if (e.isIntersecting) { grow(); o.disconnect(); } }), { threshold: .3 }).observe($("panel"));
  }

  function tools() {
    const tile = (k, h, p, href) => `<div class="cell reveal"><a class="tile plain" href="${esc(href)}" target="_blank" rel="noopener"><span class="k"><span>${esc(k)}</span><em>↗</em></span><h3>${esc(h)}</h3><p>${esc(p)}</p></a></div>`;
    const two = n => String(n).padStart(2, "0");
    $("tool-cards").innerHTML = resources.tools.map(t => tile("tool", t.name, t.what, t.url)).join("");
    $("workshop-cards").innerHTML = resources.workshops.map(w => tile("workshop", w.name, w.what, w.url)).join("");
    $("list-cards").innerHTML = resources.related.map(r => tile("list", r.name, r.what, r.url)).join("");
    $("n-tools").textContent = two(resources.tools.length); $("n-workshops").textContent = two(resources.workshops.length); $("n-lists").textContent = two(resources.related.length);
    document.querySelectorAll("main .tiles .cell").forEach(watch);
  }
})();
