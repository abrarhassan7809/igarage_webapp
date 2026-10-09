// Reads the model named in ?model=slug from the hidden #models block in the page
const el = document.querySelector(`#models [data-slug="${new URLSearchParams(location.search).get("model")}"]`)
        || document.querySelector("#models [data-slug]");
const d = el.dataset;
const pairs = s => s.split(",").map(x => x.split(":"));
const colors = pairs(d.colors), storage = pairs(d.storage);
let cc = 0, sc = 0;
document.title = d.name + " — i Garage";
$("#crumbName").textContent = $("#dName").textContent = d.name;
$("#sDisplay").textContent = d.display; $("#sChip").textContent = d.chip;
$("#sColors").textContent = colors.map(c => c[0]).join(", ");
$("#sStorage").textContent = storage.map(s => s[0]).join(", ");
function render() {
  $("#dImg").style.background = `radial-gradient(circle at 50% 60%,${colors[cc][1]}66,#f5f5f7 70%)`;
  $("#dColor").textContent = colors[cc][0];
  $("#dSwatches").innerHTML = colors.map(([n, h], j) =>
    `<button class="swatch${j === cc ? " on" : ""}" style="background:${h}" title="${n}" aria-label="${n}" data-c="${j}"></button>`).join("");
  $("#dStorage").innerHTML = storage.map(([k], j) => `<button class="st${j === sc ? " on" : ""}" data-s="${j}">${k}</button>`).join("");
  $("#dPrice").textContent = fmt(+d.base + +storage[sc][1]);
}
$("#dSwatches").onclick = e => { const b = e.target.closest("[data-c]"); if (b) { cc = +b.dataset.c; render(); } };
$("#dStorage").onclick = e => { const b = e.target.closest("[data-s]"); if (b) { sc = +b.dataset.s; render(); } };
render();
