setupFilter("#grid");

// Compare tool: reads product data from the cards in the page
const cards = [...document.querySelectorAll("#grid [data-name]")].map(c => c.dataset);
const cmpA = $("#cmpA"), cmpB = $("#cmpB");
cmpA.innerHTML = cmpB.innerHTML = cards.map(p => `<option>${p.name}</option>`).join("");
cmpB.selectedIndex = 1;
function renderCompare() {
  const a = cards.find(p => p.name === cmpA.value), b = cards.find(p => p.name === cmpB.value);
  const rows = [["Price", p => fmt(p.price)], ["Display", p => p.display], ["Chip", p => p.chip], ["Storage", p => p.storage]];
  $("#cmpTable").innerHTML = rows.map(([l, f]) => `<tr><th>${l}</th><td>${f(a)}</td><td>${f(b)}</td></tr>`).join("");
}
cmpA.onchange = cmpB.onchange = renderCompare;
renderCompare();
$("#grid").addEventListener("click", e => {
  const b = e.target.closest("[data-compare]"); if (!b) return;
  cmpA.value = b.dataset.compare; renderCompare();
  $("#compare").scrollIntoView({ behavior: "smooth" });
});

// Reseller finder -> GET /api/stores?city=
$("#findBtn").onclick = async () => {
  const q = $("#city").value.trim(), out = $("#cityResult");
  if (!q) { out.textContent = "Enter a city name."; return; }
  try {
    const { city, count } = await api("/api/stores?city=" + encodeURIComponent(q));
    out.textContent = count ? `${count} authorized store${count > 1 ? "s" : ""} found in ${city}.` : "No stores listed for that city yet.";
  } catch { out.textContent = "Could not reach the server. Try again."; }
};
