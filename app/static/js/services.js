// "Request this" buttons pre-select the service and scroll to the form
document.querySelectorAll("[data-service]").forEach(b => b.onclick = () => {
  $("#enqService").value = b.dataset.service;
  $("#callback").scrollIntoView({ behavior: "smooth" });
  $("#enqName").focus({ preventScroll: true });
});

// Callback form -> POST /api/enquiry
$("#enqForm").addEventListener("submit", async e => {
  e.preventDefault();
  const msg = $("#enqMsg");
  try {
    const res = await api("/api/enquiry", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: $("#enqName").value.trim(), phone: $("#enqPhone").value.trim(), service: $("#enqService").value })
    });
    msg.textContent = res.message;
    msg.style.color = res.ok ? "#4f7d12" : "#c0392b";
    if (res.ok) e.target.reset();
  } catch {
    msg.textContent = "Could not reach the server. Try again.";
    msg.style.color = "#c0392b";
  }
});
