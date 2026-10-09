// Shared by every page. Change API_BASE if your API runs on another host, e.g. "http://127.0.0.1:8000"
const API_BASE = "";
const $ = (s, r = document) => r.querySelector(s);
const fmt = n => "Rs " + Number(n).toLocaleString("en-US");
const api = (path, opts) => fetch(API_BASE + path, opts).then(r => r.json());

// Chips (+ optional sort) filter the cards inside a grid, using each card's data-cat / data-price
function setupFilter(grid, sortSel) {
  const g = $(grid), items = [...g.children], sel = sortSel && $(sortSel);
  let cur = "All";
  items.forEach((el, i) => el.dataset.i = i);
  const apply = () => {
    const list = items.filter(el => cur === "All" || el.dataset.cat === cur);
    items.forEach(el => el.hidden = !list.includes(el));
    const v = sel ? sel.value : "def";
    list.sort((a, b) => v === "asc" ? a.dataset.price - b.dataset.price
      : v === "desc" ? b.dataset.price - a.dataset.price : a.dataset.i - b.dataset.i)
      .forEach(el => g.append(el));
    const c = $("#count");
    if (c) c.textContent = list.length + " model" + (list.length === 1 ? "" : "s");
  };
  $("#chips").addEventListener("click", e => {
    const b = e.target.closest(".chip"); if (!b) return;
    document.querySelectorAll("#chips .chip").forEach(x => x.classList.remove("active"));
    b.classList.add("active"); cur = b.dataset.value; apply();
  });
  if (sel) sel.onchange = apply;
  apply();
}

// Newsletter form (footer on every page) -> POST /api/subscribe
$("#subForm").addEventListener("submit", async e => {
  e.preventDefault();
  const msg = $("#subMsg");
  try {
    const res = await api("/api/subscribe", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: $("#email").value.trim() })
    });
    msg.textContent = res.message;
    msg.style.color = res.ok ? "#83c327" : "#ff8a8a";
    if (res.ok) e.target.reset();
  } catch {
    msg.textContent = "Could not reach the server. Try again.";
    msg.style.color = "#ff8a8a";
  }
});
