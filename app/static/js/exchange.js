// Estimator: old-model value (option value) x condition factor (option value); new price is the option value
const oldM = $("#oldModel"), cond = $("#cond"), newM = $("#newModel");
const sel = s => s.options[s.selectedIndex];
function estimate() {
  const value = Math.round(+oldM.value * +cond.value / 1000) * 1000;
  $("#valOld").textContent = fmt(value);
  $("#valPay").textContent = fmt(Math.max(0, +newM.value - value));
  return value;
}
[oldM, cond, newM].forEach(s => s.onchange = estimate);
estimate();

// Request form -> POST /api/exchange (sends the selections above)
$("#exForm").addEventListener("submit", async e => {
  e.preventDefault();
  const msg = $("#exMsg");
  try {
    const res = await api("/api/exchange", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: $("#exName").value.trim(), phone: $("#exPhone").value.trim(),
        old_model: sel(oldM).text, condition: sel(cond).text, new_model: sel(newM).text, estimate: estimate()
      })
    });
    msg.textContent = res.message;
    msg.style.color = res.ok ? "#4f7d12" : "#c0392b";
    if (res.ok) e.target.reset();
  } catch {
    msg.textContent = "Could not reach the server. Try again.";
    msg.style.color = "#c0392b";
  }
});
