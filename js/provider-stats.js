const API_BASE_URL = "";

let currentProvider = null;

function getStoredUser() {
  return authGetStoredUser();
}

function ensureProviderAccess() {
  const user = authRequireSession();

  if (!user) {
    return null;
  }

  if (String(user.rol).toUpperCase() !== "PROVEEDOR") {
    window.location.href = "./tickets.html";
    return null;
  }

  return user;
}

function showMessage(message, isError = false) {
  const box = document.getElementById("statsMessage");
  if (!box) return;

  box.hidden = false;
  box.textContent = message;
  box.classList.toggle("error", isError);
}

function formatCurrency(value) {
  return `${Number(value || 0).toLocaleString("es-ES")} EUR`;
}

function formatDate(value) {
  if (!value) return "";

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleDateString("es-ES");
}

function updateClock() {
  const clock = document.getElementById("liveClock");
  if (!clock) return;

  clock.textContent = new Date().toLocaleString("es-ES");
}

function renderMonthlyReservations(monthlyReservations) {
  const container = document.getElementById("monthlyReservations");
  const peak = document.getElementById("monthlyPeak");

  if (!container || !peak) return;

  if (!monthlyReservations || monthlyReservations.length === 0) {
    container.innerHTML = '<p class="empty-state">No hay datos de reservas mensuales.</p>';
    peak.textContent = "Sin datos";
    return;
  }

  const maxValue = Math.max(...monthlyReservations.map((item) => Number(item.reservas || 0)), 1);
  const highest = monthlyReservations.reduce((best, current) => (
    Number(current.reservas || 0) > Number(best.reservas || 0) ? current : best
  ));

  peak.textContent = `Pico: ${highest.reservas} en ${highest.mes}`;

  container.innerHTML = monthlyReservations.map((item) => {
    const reservations = Number(item.reservas || 0);
    const percentage = Math.max(8, Math.round((reservations / maxValue) * 100));

    return `
      <article class="bar-item">
        <div class="bar-track">
          <div class="bar-fill" style="height:${percentage}%"></div>
        </div>
        <div class="bar-meta">
          <strong>${reservations} reservas</strong>
          <span>${item.mes}</span>
        </div>
      </article>
    `;
  }).join("");
}

function renderActivityLog(activityLog) {
  const container = document.getElementById("activityLog");
  if (!container) return;

  if (!activityLog || activityLog.length === 0) {
    container.innerHTML = '<p class="empty-state">No hay actividad registrada.</p>';
    return;
  }

  container.innerHTML = activityLog.map((entry) => `
    <article class="activity-item">
      <div>
        <strong>${entry.tipo}</strong>
        <p class="activity-copy">${entry.detalle}</p>
      </div>
      <span>${formatDate(entry.fecha)}</span>
    </article>
  `).join("");
}

function renderStats(stats) {
  const totalRequests = Number(stats.totalSolicitudes || 0);
  const approved = Number(stats.solicitudesAprobadas || 0);
  const pending = Number(stats.solicitudesPendientes || 0);
  const rejected = Number(stats.solicitudesRechazadas || 0);
  const approvalRate = totalRequests > 0 ? Math.round((approved / totalRequests) * 100) : 0;

  const mappings = [
    ["totalVentasValue", formatCurrency(stats.totalVentas)],
    ["profileViewsValue", String(stats.profileViews || 0)],
    ["totalRequestsValue", String(totalRequests)],
    ["approvalRateValue", `${approvalRate}%`],
    ["pendingValue", String(pending)],
    ["approvedValue", String(approved)],
    ["rejectedValue", String(rejected)]
  ];

  mappings.forEach(([id, value]) => {
    const element = document.getElementById(id);
    if (element) {
      element.textContent = value;
    }
  });

  const summary = document.getElementById("summaryText");
  if (summary) {
    summary.textContent = `Tienes ${pending} solicitud${pending === 1 ? "" : "es"} pendiente${pending === 1 ? "" : "s"}, ${approved} aprobada${approved === 1 ? "" : "s"} y ${rejected} rechazada${rejected === 1 ? "" : "s"}.`;
  }

  renderMonthlyReservations(stats.monthlyReservations || []);
  renderActivityLog(stats.activityLog || []);
}

async function loadProviderStats() {
  const user = ensureProviderAccess();
  if (!user) return;

  currentProvider = user;

  try {
    const [profileResponse, statsResponse] = await Promise.all([
      authFetch(`${API_BASE_URL}/provider/profile/${user.id_usuario}`),
      authFetch(`${API_BASE_URL}/provider/stats/${user.id_usuario}`)
    ]);

    if (!profileResponse.ok || !statsResponse.ok) {
      throw new Error("No se pudieron cargar las estadisticas");
    }

    currentProvider = await profileResponse.json();
    authSaveSession(currentProvider);

    const stats = await statsResponse.json();

    const subtitle = document.getElementById("providerSubtitle");
    if (subtitle) {
      subtitle.textContent = `${currentProvider.businessName || currentProvider.name || "Proveedor"} · ${currentProvider.email}`;
    }

    renderStats(stats);
  } catch (error) {
    console.error(error);
    showMessage("No se pudieron cargar las estadisticas del proveedor.", true);
  }
}

function attachLogout() {
  const button = document.getElementById("logoutBtn");
  if (!button) return;

  button.addEventListener("click", () => {
    authClearSession();
    window.location.href = "./login.html";
  });
}

document.addEventListener("DOMContentLoaded", () => {
  if (!ensureProviderAccess()) {
    return;
  }

  updateClock();
  setInterval(updateClock, 1000);
  attachLogout();
  loadProviderStats();

  const refreshButton = document.getElementById("refreshStatsBtn");
  if (refreshButton) {
    refreshButton.addEventListener("click", loadProviderStats);
  }
});
