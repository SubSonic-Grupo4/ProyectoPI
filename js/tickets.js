// js/tickets.js

function renderMiniTickets() {
  const miniWrap = document.getElementById("miniTickets");
  if (!miniWrap) return;

  miniWrap.innerHTML = window.SubsonicData.tickets.map(t => `
    <div class="mini-ticket" data-ticket-id="${t.ticketId}">
      <div class="mini-content">
        <div class="mini-img"></div>
        <div>
          <p>${t.eventName}</p>
          <span>${t.monthDay}</span>
        </div>
      </div>
      <button class="cancel-btn" type="button" data-action="cancel" data-ticket-id="${t.ticketId}">Cancel</button>
    </div>
  `).join("");
}

function renderBigTickets() {
  const list = document.getElementById("ticketsList");
  if (!list) return;

  list.innerHTML = window.SubsonicData.tickets.map(t => `
    <div class="ticket-card">
      <div class="ticket-img"></div>
      <div class="ticket-info">
        <h3>${t.eventName}</h3>
        <p>${t.dateLabel}</p>
        <span>${t.passType}</span>
        <p style="opacity:.75; margin-top:6px;">ID: #${t.ticketId} · Estado: ${t.status}</p>
      </div>
      <a class="cancel-btn"
         style="text-decoration:none; display:inline-flex; align-items:center; justify-content:center;"
         href="./ticket-detail.html?ticketId=${encodeURIComponent(t.ticketId)}">
        Ver detalle
      </a>
    </div>
  `).join("");
}

function renderProfilePanel() {
  const user = window.SubsonicData.currentUser;

  const nameInput = document.getElementById("nameInput");
  const emailInput = document.getElementById("emailInput");
  const avatarBox = document.getElementById("avatarBox");

  if (nameInput) nameInput.value = user.name;
  if (emailInput) emailInput.value = user.email;
  if (avatarBox) avatarBox.style.background = user.avatarColor;
}

function attachHandlers() {
  // Ir a perfil completo
  const goProfile = document.getElementById("goProfile");
  if (goProfile) {
    goProfile.addEventListener("click", () => {
      window.location.href = "./profile.html";
    });
  }

  // Guardado simulado del panel
  const saveBtn = document.getElementById("saveProfileBtn");
  if (saveBtn) {
    saveBtn.addEventListener("click", () => {
      const nameInput = document.getElementById("nameInput");
      const emailInput = document.getElementById("emailInput");

      if (nameInput) window.SubsonicData.currentUser.name = nameInput.value;
      if (emailInput) window.SubsonicData.currentUser.email = emailInput.value;

      alert("Cambios guardados (simulado).");
    });
  }

  // Cancelar desde mini-tickets (simulado)
  const miniWrap = document.getElementById("miniTickets");
  if (miniWrap) {
    miniWrap.addEventListener("click", (e) => {
      const btn = e.target.closest('button[data-action="cancel"]');
      if (!btn) return;

      const ticketId = btn.getAttribute("data-ticket-id");
      const ticket = window.SubsonicData.tickets.find(t => t.ticketId === ticketId);
      if (ticket) ticket.status = "Cancelada";

      renderMiniTickets();
      renderBigTickets();
    });
  }
}

document.addEventListener("DOMContentLoaded", () => {
  renderMiniTickets();
  renderBigTickets();
  renderProfilePanel();
  attachHandlers();
});