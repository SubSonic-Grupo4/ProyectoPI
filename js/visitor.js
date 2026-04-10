const VISITOR_API_BASE_URL = "";

let visitorEvents = [];

function getCurrentSessionRoute() {
  const user = authGetStoredUser();
  const token = authGetToken();

  if (!user || !token) {
    return "./login.html";
  }

  if (String(user.rol).toUpperCase() === "PROVEEDOR") {
    return "./gestion.html?v=1";
  }

  return "./purchase.html?v=7";
}

function parseEventDate(dateLabel) {
  const [day, month, year] = String(dateLabel).split("/");
  if (!day || !month || !year) {
    return null;
  }

  return new Date(`${year}-${month}-${day}T00:00:00`);
}

function formatEventDate(dateLabel, timeLabel) {
  const parsed = parseEventDate(dateLabel);
  if (!parsed || Number.isNaN(parsed.getTime())) {
    return `${dateLabel} · ${timeLabel}`;
  }

  return `${parsed.toLocaleDateString("es-ES", { weekday: "long", day: "numeric", month: "long" })} · ${timeLabel}`;
}

function showVisitorMessage(message) {
  const box = document.getElementById("visitorMessage");
  if (!box) return;

  box.hidden = false;
  box.textContent = message;
}

function clearVisitorMessage() {
  const box = document.getElementById("visitorMessage");
  if (!box) return;

  box.hidden = true;
  box.textContent = "";
}

function updateCtaTargets() {
  const route = getCurrentSessionRoute();

  document.querySelectorAll(".auth-buttons a").forEach((link) => {
    link.setAttribute("href", "./login.html");
  });

  const heroCta = document.getElementById("heroCta");
  if (heroCta) {
    heroCta.setAttribute("href", route);
    heroCta.innerHTML = route.includes("purchase")
      ? '<i class="fa-solid fa-ticket"></i> Ir a compra'
      : route.includes("gestion")
        ? '<i class="fa-solid fa-briefcase"></i> Ir al portal proveedor'
        : '<i class="fa-solid fa-ticket"></i> Ver acceso a compra';
  }
}

function getFilteredEvents() {
  const fromValue = document.getElementById("desde")?.value;
  const untilValue = document.getElementById("hasta")?.value;
  const genreValue = document.getElementById("genero")?.value || "todos";

  return visitorEvents.filter((eventItem) => {
    const parsedDate = parseEventDate(eventItem.date);

    if (genreValue !== "todos" && eventItem.genre !== genreValue) {
      return false;
    }

    if (fromValue && parsedDate && parsedDate < new Date(`${fromValue}T00:00:00`)) {
      return false;
    }

    if (untilValue && parsedDate && parsedDate > new Date(`${untilValue}T23:59:59`)) {
      return false;
    }

    return true;
  });
}

function renderEvents() {
  const grid = document.getElementById("eventsGrid");
  const summary = document.getElementById("eventsSummary");
  if (!grid) return;

  const filteredEvents = getFilteredEvents();

  if (summary) {
    summary.textContent = `${filteredEvents.length} evento${filteredEvents.length === 1 ? "" : "s"} visibles en el calendario publico.`;
  }

  if (!filteredEvents.length) {
    grid.innerHTML = '<div class="empty-state">No hay eventos que cumplan con los filtros seleccionados.</div>';
    return;
  }

  const ctaRoute = getCurrentSessionRoute();
  const ctaText = ctaRoute.includes("purchase")
    ? "Ir a compra"
    : ctaRoute.includes("gestion")
      ? "Ir a mi portal"
      : "Login para comprar";

  grid.innerHTML = filteredEvents.map((eventItem) => `
    <article class="event-card">
      <div class="card-image">
        <span class="genre-tag">${eventItem.genre}</span>
      </div>
      <div class="card-content">
        <h3>${eventItem.name}</h3>
        <p class="event-summary">${eventItem.summary}</p>
        <div class="event-info">
          <i class="fa-regular fa-calendar"></i>
          ${formatEventDate(eventItem.date, eventItem.time)}
        </div>
        <div class="event-info">
          <i class="fa-solid fa-location-dot"></i>
          ${eventItem.location}
        </div>
      </div>
      <div class="card-action">
        <a href="${ctaRoute}" class="btn btn-outline btn-block">${ctaText} &rarr;</a>
      </div>
    </article>
  `).join("");
}

async function loadPublicEvents() {
  try {
    const response = await fetch(`${VISITOR_API_BASE_URL}/events`);

    if (!response.ok) {
      throw new Error("No se pudieron cargar los eventos publicos");
    }

    visitorEvents = await response.json();
    clearVisitorMessage();
    renderEvents();
  } catch (error) {
    console.error(error);
    showVisitorMessage("No se pudieron cargar los eventos publicos del festival.");
  }
}

function attachVisitorFilters() {
  const controls = ["desde", "hasta", "genero"];
  controls.forEach((id) => {
    const element = document.getElementById(id);
    if (element) {
      element.addEventListener("change", renderEvents);
    }
  });

  const searchButton = document.getElementById("searchBtn");
  if (searchButton) {
    searchButton.addEventListener("click", renderEvents);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  updateCtaTargets();
  attachVisitorFilters();
  loadPublicEvents();
});
