const API_BASE_URL = "";

function qs(name) {
  return new URLSearchParams(window.location.search).get(name);
}

function setBadge(badgeEl, status) {
  badgeEl.textContent = status;

  badgeEl.classList.remove("badge--active", "badge--cancelled");

  if (status === "Cancelada") {
    badgeEl.classList.add("badge--cancelled");
  } else {
    badgeEl.classList.add("badge--active");
  }
}

async function cancelTicket(ticketId) {
  try {
    const response = await authFetch(`${API_BASE_URL}/ticket/cancel/${ticketId}`, {
      method: "PUT"
    });

    if (!response.ok) {
      throw new Error("No se pudo cancelar el ticket");
    }

    alert("Ticket cancelado");
    window.location.href = "tickets.html";
  } catch (error) {
    console.error("Error cancelando ticket:", error);
    alert("Error al cancelar la entrada");
  }
}

async function loadTicketDetail() {
  const user = authRequireSession();
  const ticketId = qs("ticketId");

  if (!user) {
    return;
  }

  if (!ticketId) {
    renderNotFound();
    return;
  }

  try {
    const response = await authFetch(`${API_BASE_URL}/ticket/${ticketId}`);

    if (!response.ok) {
      throw new Error("Ticket no encontrado");
    }

    const ticket = await response.json();
    renderDetail(ticket, user);
  } catch (error) {
    console.error("Error cargando detalle:", error);
    renderNotFound();
  }
}

function renderNotFound() {
  const eventNameEl = document.getElementById("eventName");
  const eventMetaEl = document.getElementById("eventMeta");
  const statusBadgeEl = document.getElementById("statusBadge");
  const ticketIdValueEl = document.getElementById("ticketIdValue");
  const passValueEl = document.getElementById("passValue");
  const priceValueEl = document.getElementById("priceValue");
  const holderValueEl = document.getElementById("holderValue");

  if (eventNameEl) eventNameEl.textContent = "Ticket no encontrado";
  if (eventMetaEl) eventMetaEl.textContent = "";
  if (statusBadgeEl) setBadge(statusBadgeEl, "Cancelada");
  if (ticketIdValueEl) ticketIdValueEl.textContent = "-";
  if (passValueEl) passValueEl.textContent = "-";
  if (priceValueEl) priceValueEl.textContent = "-";
  if (holderValueEl) holderValueEl.textContent = "-";
}

function renderDetail(ticket, user) {
  const eventNameEl = document.getElementById("eventName");
  const eventMetaEl = document.getElementById("eventMeta");
  const statusBadgeEl = document.getElementById("statusBadge");
  const ticketIdValueEl = document.getElementById("ticketIdValue");
  const passValueEl = document.getElementById("passValue");
  const priceValueEl = document.getElementById("priceValue");
  const holderValueEl = document.getElementById("holderValue");

  if (eventNameEl) eventNameEl.textContent = ticket.eventName;
  if (eventMetaEl) eventMetaEl.textContent = `Evento - ${ticket.dateLabel}`;
  if (statusBadgeEl) setBadge(statusBadgeEl, ticket.status);
  if (ticketIdValueEl) ticketIdValueEl.textContent = `#${ticket.ticketId}`;
  if (passValueEl) passValueEl.textContent = ticket.passType;

  const price =
    ticket.passType.toLowerCase().includes("vip") ? 89 :
    ticket.passType.toLowerCase().includes("full") ? 129 :
    49;

  if (priceValueEl) priceValueEl.textContent = `${price} EUR`;
  if (holderValueEl) holderValueEl.textContent = user.name || "Usuario";

  const cancelBtn = document.getElementById("cancelBtn");
  if (cancelBtn) {
    cancelBtn.disabled = ticket.status === "Cancelada";
    cancelBtn.textContent = ticket.status === "Cancelada"
      ? "Entrada cancelada"
      : "Cancelar Entrada";

    cancelBtn.addEventListener("click", async () => {
      if (ticket.status === "Cancelada") return;
      await cancelTicket(ticket.ticketId);
    });
  }
}

document.addEventListener("DOMContentLoaded", loadTicketDetail);
