const API_BASE_URL = "";

let currentProvider = null;
let spaces = [];
let applications = [];
let selectedSpace = null;

function getStoredUser() {
  return JSON.parse(localStorage.getItem("user"));
}

function ensureProviderAccess() {
  const user = getStoredUser();

  if (!user) {
    window.location.href = "./login.html";
    return null;
  }

  if (user.rol !== "PROVEEDOR") {
    window.location.href = "./tickets.html";
    return null;
  }

  return user;
}

function showMessage(message, isError = false) {
  const box = document.getElementById("spacesMessage");
  if (!box) return;

  box.hidden = false;
  box.textContent = message;
  box.classList.toggle("error", isError);
}

function clearMessage() {
  const box = document.getElementById("spacesMessage");
  if (!box) return;

  box.hidden = true;
  box.textContent = "";
  box.classList.remove("error");
}

function formatPrice(value) {
  return `${Number(value).toLocaleString("es-ES")} EUR`;
}

function formatDate(value) {
  if (!value) return "Sin fecha";

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString("es-ES");
}

function getSelectedTypes() {
  return Array.from(document.querySelectorAll(".filter-check:checked")).map((checkbox) => checkbox.value);
}

function getFilteredSpaces() {
  const selectedTypes = getSelectedTypes();
  const priceFilter = document.getElementById("priceFilter")?.value || "all";
  const availableOnly = document.getElementById("availableOnly")?.checked;

  return spaces.filter((space) => {
    if (!selectedTypes.includes(space.tipo)) {
      return false;
    }

    if (priceFilter === "budget" && Number(space.precio) > 1000) {
      return false;
    }

    if (priceFilter === "premium" && Number(space.precio) <= 1000) {
      return false;
    }

    if (availableOnly && !space.disponible) {
      return false;
    }

    return true;
  });
}

function hasOpenRequest(spaceId) {
  return applications.some((application) =>
    application.idEspacio === spaceId &&
    ["PENDIENTE", "APROBADA"].includes(application.estado)
  );
}

function renderSummary(filteredSpaces) {
  const summary = document.getElementById("spacesSummary");
  if (!summary) return;

  const availableCount = filteredSpaces.filter((space) => space.disponible).length;
  summary.innerHTML = `
    <span>${filteredSpaces.length} espacios visibles</span>
    <strong>${availableCount} disponibles para solicitar</strong>
  `;
}

function renderSpaces() {
  const filteredSpaces = getFilteredSpaces();
  renderSummary(filteredSpaces);

  const grid = document.getElementById("boothGrid");
  if (!grid) return;

  if (filteredSpaces.length === 0) {
    grid.innerHTML = '<div class="detail-card"><p class="placeholder-title">Sin resultados</p><p class="placeholder-copy">Prueba a cambiar los filtros para ver mas espacios.</p></div>';
    return;
  }

  grid.innerHTML = filteredSpaces.map((space) => {
    const isSelected = selectedSpace && selectedSpace.idEspacio === space.idEspacio;
    const requestOpen = hasOpenRequest(space.idEspacio);
    const availabilityLabel = space.disponible ? "Disponible" : "Ocupado";

    return `
      <article class="booth ${space.disponible ? "" : "occupied"} ${isSelected ? "selected" : ""}" data-space-id="${space.idEspacio}">
        <div class="booth-header">
          <div>
            <p class="booth-title">${space.idEspacio}</p>
            <small>${space.tipo}</small>
          </div>
          <span class="badge ${space.disponible ? "available" : "occupied"}">${availabilityLabel}</span>
        </div>
        <p class="booth-copy">${space.ubicacion}</p>
        <p class="booth-copy">${space.tamano} · ${formatPrice(space.precio)}</p>
        ${requestOpen ? '<p class="application-meta">Ya tienes una solicitud activa para este espacio.</p>' : ""}
      </article>
    `;
  }).join("");
}

function renderSelectedSpace() {
  const card = document.getElementById("selectedSpaceCard");
  const form = document.getElementById("applicationForm");
  const categorySelect = document.getElementById("applicationCategory");

  if (!card || !form) return;

  if (!selectedSpace) {
    card.innerHTML = `
      <p class="placeholder-title">Ningun espacio seleccionado</p>
      <p class="placeholder-copy">Pulsa en un espacio para ver sus detalles y solicitarlo.</p>
    `;
    form.hidden = true;
    return;
  }

  const requestOpen = hasOpenRequest(selectedSpace.idEspacio);

  card.innerHTML = `
    <div class="application-item-header">
      <div>
        <p class="header-kicker">Espacio seleccionado</p>
        <h4>${selectedSpace.idEspacio}</h4>
      </div>
      <span class="badge ${selectedSpace.disponible ? "available" : "occupied"}">${selectedSpace.disponible ? "Disponible" : "Ocupado"}</span>
    </div>

    <div class="space-meta">
      <p><strong>Tipo</strong>${selectedSpace.tipo}</p>
      <p><strong>Ubicacion</strong>${selectedSpace.ubicacion}</p>
      <p><strong>Tamano</strong>${selectedSpace.tamano}</p>
      <p><strong>Precio</strong>${formatPrice(selectedSpace.precio)}</p>
    </div>

    <p class="space-description">${selectedSpace.descripcion}</p>
    ${requestOpen ? '<p class="application-meta">Ya tienes una solicitud pendiente o aprobada para este espacio.</p>' : ""}
  `;

  if (categorySelect) {
    categorySelect.value = selectedSpace.tipo;
  }

  form.hidden = !selectedSpace.disponible || requestOpen;
}

function renderApplications() {
  const list = document.getElementById("applicationsList");
  if (!list) return;

  if (!applications.length) {
    list.innerHTML = '<p class="empty-list">Todavia no has enviado solicitudes.</p>';
    return;
  }

  const ordered = [...applications].sort((a, b) => String(b.fechaSolicitud).localeCompare(String(a.fechaSolicitud)));

  list.innerHTML = ordered.map((application) => `
    <article class="application-item">
      <div class="application-item-header">
        <div>
          <strong>${application.idSolicitud} · ${application.idEspacio}</strong>
          <span class="application-meta">${application.categoriaServicio}</span>
        </div>
        <span class="badge state-${application.estado.toLowerCase()}">${application.estado}</span>
      </div>
      <p class="application-description">${application.descripcion}</p>
      <p class="application-meta">${formatDate(application.fechaSolicitud)}</p>
    </article>
  `).join("");
}

async function loadProviderSummary() {
  const user = ensureProviderAccess();
  if (!user) return;

  currentProvider = user;

  try {
    const response = await fetch(`${API_BASE_URL}/provider/profile/${user.id_usuario}`);
    if (!response.ok) {
      throw new Error("No se pudo cargar el proveedor");
    }

    currentProvider = await response.json();
    localStorage.setItem("user", JSON.stringify(currentProvider));

    const nameLabel = document.getElementById("providerNameLabel");
    const businessLabel = document.getElementById("providerBusinessLabel");

    if (nameLabel) nameLabel.textContent = currentProvider.name || "Proveedor";
    if (businessLabel) businessLabel.textContent = currentProvider.businessName || currentProvider.email || "";
  } catch (error) {
    console.error(error);
    showMessage("No se pudo cargar el perfil del proveedor.", true);
  }
}

async function loadSpaces() {
  const response = await fetch(`${API_BASE_URL}/spaces`);

  if (!response.ok) {
    throw new Error("No se pudieron cargar los espacios");
  }

  spaces = await response.json();
  renderSpaces();
}

async function loadApplications() {
  if (!currentProvider) return;

  const response = await fetch(`${API_BASE_URL}/provider/applications/${currentProvider.id_usuario}`);

  if (!response.ok) {
    throw new Error("No se pudieron cargar las solicitudes");
  }

  applications = await response.json();
  renderApplications();
  renderSelectedSpace();
  renderSpaces();
}

async function submitApplication(event) {
  event.preventDefault();
  clearMessage();

  if (!selectedSpace || !currentProvider) {
    showMessage("Selecciona primero un espacio disponible.", true);
    return;
  }

  const description = document.getElementById("applicationDescription")?.value?.trim() || "";
  const category = document.getElementById("applicationCategory")?.value || selectedSpace.tipo;
  const portfolioUrl = document.getElementById("portfolioUrlInput")?.value?.trim() || null;

  if (!description) {
    showMessage("Debes escribir una descripcion para la solicitud.", true);
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/provider/applications`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        id_proveedor: currentProvider.id_usuario,
        id_espacio: selectedSpace.idEspacio,
        descripcion: description,
        categoriaServicio: category,
        portfolioUrl
      })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "No se pudo enviar la solicitud");
    }

    document.getElementById("applicationDescription").value = "";
    document.getElementById("portfolioUrlInput").value = "";
    showMessage("Solicitud enviada correctamente.");
    await loadApplications();
  } catch (error) {
    console.error(error);
    showMessage(error.message || "No se pudo enviar la solicitud.", true);
  }
}

function attachSpaceEvents() {
  const grid = document.getElementById("boothGrid");
  if (!grid) return;

  grid.addEventListener("click", (event) => {
    const booth = event.target.closest("[data-space-id]");
    if (!booth) return;

    const spaceId = booth.getAttribute("data-space-id");
    selectedSpace = spaces.find((space) => space.idEspacio === spaceId) || null;
    renderSpaces();
    renderSelectedSpace();
  });
}

function attachFilterEvents() {
  document.querySelectorAll(".filter-check").forEach((checkbox) => {
    checkbox.addEventListener("change", () => {
      renderSpaces();
      renderSelectedSpace();
    });
  });

  const priceFilter = document.getElementById("priceFilter");
  const availableOnly = document.getElementById("availableOnly");
  const resetButton = document.getElementById("resetFiltersBtn");

  if (priceFilter) {
    priceFilter.addEventListener("change", () => {
      renderSpaces();
      renderSelectedSpace();
    });
  }

  if (availableOnly) {
    availableOnly.addEventListener("change", () => {
      renderSpaces();
      renderSelectedSpace();
    });
  }

  if (resetButton) {
    resetButton.addEventListener("click", () => {
      document.querySelectorAll(".filter-check").forEach((checkbox) => {
        checkbox.checked = true;
      });

      if (priceFilter) {
        priceFilter.value = "all";
      }

      if (availableOnly) {
        availableOnly.checked = true;
      }

      renderSpaces();
      renderSelectedSpace();
    });
  }
}

function attachLogout() {
  const button = document.getElementById("logoutBtn");
  if (!button) return;

  button.addEventListener("click", () => {
    localStorage.removeItem("user");
    window.location.href = "./login.html";
  });
}

async function initSpacesPage() {
  if (!ensureProviderAccess()) {
    return;
  }

  attachSpaceEvents();
  attachFilterEvents();
  attachLogout();

  const form = document.getElementById("applicationForm");
  if (form) {
    form.addEventListener("submit", submitApplication);
  }

  try {
    await loadProviderSummary();
    await loadSpaces();
    await loadApplications();
  } catch (error) {
    console.error(error);
    showMessage("No se pudo cargar la vista de espacios del proveedor.", true);
  }
}

document.addEventListener("DOMContentLoaded", initSpacesPage);
