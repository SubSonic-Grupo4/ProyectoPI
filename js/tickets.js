const API_BASE_URL = "";

let currentTickets = [];

function getStoredUser() {
  return authGetStoredUser();
}

function saveStoredUser(user) {
  authSaveSession(user);
}

async function loadTickets() {
  const user = authRequireSession();
  if (!user) {
    return;
  }

  try {
    const response = await authFetch(`${API_BASE_URL}/tickets/${user.id_usuario}`);

    if (!response.ok) {
      throw new Error("No se pudieron cargar los tickets");
    }

    const tickets = await response.json();
    currentTickets = tickets.filter(ticket => ticket.status !== "Cancelada");

    renderMiniTickets();
    renderBigTickets();
  } catch (error) {
    console.error("Error cargando tickets:", error);
  }
}

function renderMiniTickets() {
  const miniWrap = document.getElementById("miniTickets");
  if (!miniWrap) return;

  if (currentTickets.length === 0) {
    miniWrap.innerHTML = `
      <div class="mini-ticket">
        <div>
          <p>No tienes entradas activas</p>
          <span>Compra una nueva entrada para verla aqui.</span>
        </div>
      </div>
    `;
    return;
  }

  miniWrap.innerHTML = currentTickets.map(t => `
    <div class="mini-ticket" data-ticket-id="${t.ticketId}">
      <div class="mini-content">
        <div class="mini-img"></div>
        <div>
          <p>${t.eventName}</p>
          <span>${t.monthDay}</span>
        </div>
      </div>
      <button class="cancel-btn" type="button" data-action="cancel" data-ticket-id="${t.ticketId}">
        Cancel
      </button>
    </div>
  `).join("");
}

function renderBigTickets() {
  const list = document.getElementById("ticketsList");
  if (!list) return;

  if (currentTickets.length === 0) {
    list.innerHTML = `
      <div class="ticket-card">
        <div class="ticket-info">
          <h3>No tienes entradas activas</h3>
          <p>Las entradas canceladas ya no se muestran en My Tickets.</p>
        </div>
        <a class="cancel-btn"
           style="text-decoration:none; display:inline-flex; align-items:center; justify-content:center;"
           href="./purchase.html">
          Comprar ahora
        </a>
      </div>
    `;
    return;
  }

  list.innerHTML = currentTickets.map(t => `
    <div class="ticket-card">
      <div class="ticket-img"></div>
      <div class="ticket-info">
        <h3>${t.eventName}</h3>
        <p>${t.dateLabel}</p>
        <span>${t.passType}</span>
        <p style="opacity:.75; margin-top:6px;">
          ID: #${t.ticketId} - Estado: ${t.status}
        </p>
      </div>
      <a class="cancel-btn"
         style="text-decoration:none; display:inline-flex; align-items:center; justify-content:center;"
         href="./ticket-detail.html?ticketId=${encodeURIComponent(t.ticketId)}">
        Ver detalle
      </a>
    </div>
  `).join("");
}

function renderProfilePanel(user) {
  const nameInput = document.getElementById("nameInput");
  const emailInput = document.getElementById("emailInput");
  const avatarBox = document.getElementById("avatarBox");

  if (nameInput) nameInput.value = user.name || "";
  if (emailInput) emailInput.value = user.email || "";

  if (avatarBox) {
    avatarBox.style.background = user.avatarColor || "";
    avatarBox.style.backgroundImage = "";

    if (user.avatarUrl) {
      avatarBox.style.backgroundImage = `url(${user.avatarUrl})`;
      avatarBox.style.backgroundSize = "cover";
      avatarBox.style.backgroundPosition = "center";
    }
  }
}

async function loadUserProfilePanel() {
  const user = getStoredUser();
  if (!user) return;

  renderProfilePanel(user);

  try {
    const response = await authFetch(`${API_BASE_URL}/profile/${user.id_usuario}`);

    if (!response.ok) {
      throw new Error("No se pudo cargar el perfil");
    }

    const profile = await response.json();
    saveStoredUser(profile);
    renderProfilePanel(profile);
  } catch (error) {
    console.error("Error cargando perfil:", error);
  }
}

async function cancelTicket(ticketId) {
  try {
    const response = await authFetch(`${API_BASE_URL}/ticket/cancel/${ticketId}`, {
      method: "PUT"
    });

    if (!response.ok) {
      throw new Error("No se pudo cancelar la entrada");
    }

    await loadTickets();
  } catch (error) {
    console.error("Error cancelando ticket:", error);
    alert("Error al cancelar la entrada");
  }
}

function attachHandlers() {
  const goPurchase = document.getElementById("goPurchase");
  if (goPurchase) {
    goPurchase.addEventListener("click", () => {
      window.location.href = "./purchase.html?v=7";
    });
  }

  const goProfile = document.getElementById("goProfile");
  if (goProfile) {
    goProfile.addEventListener("click", () => {
      window.location.href = "./profile.html?v=9";
    });
  }

  const saveBtn = document.getElementById("saveProfileBtn");
  if (saveBtn) {
    saveBtn.addEventListener("click", async () => {
      const user = getStoredUser();

      if (!user) {
        window.location.href = "./login.html";
        return;
      }

      const nameInput = document.getElementById("nameInput");
      const emailInput = document.getElementById("emailInput");

      try {
        const response = await authFetch(`${API_BASE_URL}/profile/${user.id_usuario}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            name: nameInput ? nameInput.value : "",
            email: emailInput ? emailInput.value : "",
            address: user.address || "",
            avatarUrl: user.avatarUrl || null
          })
        });

        if (!response.ok) {
          throw new Error("No se pudo guardar el perfil");
        }

        const data = await response.json();
        saveStoredUser(data.user);
        renderProfilePanel(data.user);

        alert("Cambios guardados correctamente");
      } catch (error) {
        console.error("Error guardando perfil:", error);
        alert("Error al guardar el perfil");
      }
    });
  }

  const miniWrap = document.getElementById("miniTickets");
  if (miniWrap) {
    miniWrap.addEventListener("click", (event) => {
      const btn = event.target.closest('button[data-action="cancel"]');
      if (!btn) return;

      const ticketId = btn.getAttribute("data-ticket-id");
      cancelTicket(ticketId);
    });
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadTickets();
  loadUserProfilePanel();
  attachHandlers();
});
