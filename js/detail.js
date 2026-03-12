// js/detail.js

function qs(name) {
  return new URLSearchParams(window.location.search).get(name);
}

function getTicket(ticketId) {
  return window.SubsonicData.tickets.find(t => t.ticketId === ticketId);
}

function setBadge(badgeEl, status) {
  badgeEl.textContent = status;

  // Limpia clases y aplica según estado
  badgeEl.classList.remove("badge--active", "badge--cancelled");

  if (status === "Cancelada") {
    badgeEl.classList.add("badge--cancelled");
  } else {
    badgeEl.classList.add("badge--active");
  }
}

function renderDetail() {
  const ticketId = qs("ticketId") || window.SubsonicData.tickets[0]?.ticketId;
  const ticket = getTicket(ticketId);

  const eventNameEl = document.getElementById("eventName");
  const eventMetaEl = document.getElementById("eventMeta");
  const statusBadgeEl = document.getElementById("statusBadge");

  const ticketIdValueEl = document.getElementById("ticketIdValue");
  const passValueEl = document.getElementById("passValue");
  const priceValueEl = document.getElementById("priceValue");
  const holderValueEl = document.getElementById("holderValue");

  if (!ticket) {
    if (eventNameEl) eventNameEl.textContent = "Ticket no encontrado";
    if (eventMetaEl) eventMetaEl.textContent = "";
    if (statusBadgeEl) setBadge(statusBadgeEl, "Cancelada");
    if (ticketIdValueEl) ticketIdValueEl.textContent = "-";
    if (passValueEl) passValueEl.textContent = "-";
    if (priceValueEl) priceValueEl.textContent = "-";
    if (holderValueEl) holderValueEl.textContent = "-";
    return;
  }

  // En tu data.js actual tenemos: eventName, dateLabel, passType, status
  if (eventNameEl) eventNameEl.textContent = ticket.eventName;
  if (eventMetaEl) eventMetaEl.textContent = `Evento · ${ticket.dateLabel}`;
  if (statusBadgeEl) setBadge(statusBadgeEl, ticket.status);

  if (ticketIdValueEl) ticketIdValueEl.textContent = `#${ticket.ticketId}`;
  if (passValueEl) passValueEl.textContent = ticket.passType;

  // Precio: si no lo tienes en data.js, lo simulamos según tipo de pase
  const price =
    ticket.passType.toLowerCase().includes("vip") ? 89 :
    ticket.passType.toLowerCase().includes("full") ? 129 :
    49;

  if (priceValueEl) priceValueEl.textContent = `${price}€`;
  if (holderValueEl) holderValueEl.textContent = window.SubsonicData.currentUser.name;

  // Botón cancelar
  const cancelBtn = document.getElementById("cancelBtn");
  if (cancelBtn) {
    cancelBtn.disabled = (ticket.status === "Cancelada");
    cancelBtn.textContent = ticket.status === "Cancelada" ? "Entrada cancelada" : "Cancelar Entrada";

    cancelBtn.addEventListener("click", () => {
      ticket.status = "Cancelada";
      window.location.href = "./tickets.html";
    });
  }
}

document.addEventListener("DOMContentLoaded", renderDetail);