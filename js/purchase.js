const API_BASE_URL = "";

let eventsData = [];
let passesData = [];

function fillSelect(selectEl, optionsHtml) {
  selectEl.innerHTML = optionsHtml;
}

function renderOptions() {
  const eventSelect = document.getElementById("eventSelect");
  const passSelect = document.getElementById("passSelect");
  const qtySelect = document.getElementById("qtySelect");
  const eventTitle = document.getElementById("eventTitle");
  const eventDate = document.getElementById("eventDate");

  if (!eventSelect || !passSelect || !qtySelect) return;

  fillSelect(
    eventSelect,
    eventsData.map(eventItem =>
      `<option value="${eventItem.eventId}">${eventItem.name} - ${eventItem.date}</option>`
    ).join("")
  );

  fillSelect(
    passSelect,
    passesData.map(passItem =>
      `<option value="${passItem.passId}">${passItem.label} - ${passItem.price} EUR</option>`
    ).join("")
  );

  fillSelect(
    qtySelect,
    [1, 2, 3, 4].map(number => `<option value="${number}">${number}</option>`).join("")
  );

  function updateEventPreview() {
    const selected = eventsData.find(eventItem => eventItem.eventId === eventSelect.value);
    if (!selected) return;

    if (eventTitle) eventTitle.textContent = selected.name;
    if (eventDate) eventDate.textContent = selected.date;
  }

  eventSelect.addEventListener("change", updateEventPreview);
  updateEventPreview();
}

async function loadPurchaseOptions() {
  const response = await fetch(`${API_BASE_URL}/purchase/options`);

  if (!response.ok) {
    throw new Error("No se pudieron cargar las opciones de compra");
  }

  const data = await response.json();
  eventsData = data.events || [];
  passesData = data.passes || [];
}

function attachPurchaseHandler() {
  const eventSelect = document.getElementById("eventSelect");
  const passSelect = document.getElementById("passSelect");
  const qtySelect = document.getElementById("qtySelect");
  const confirmBtn = document.getElementById("confirmPurchaseBtn");

  if (!eventSelect || !passSelect || !qtySelect || !confirmBtn) return;

  confirmBtn.addEventListener("click", async () => {
    const user = JSON.parse(localStorage.getItem("user"));

    if (!user) {
      alert("Debes iniciar sesion primero");
      window.location.href = "./login.html";
      return;
    }

    const selectedEvent = eventsData.find(eventItem => eventItem.eventId === eventSelect.value);
    const selectedPass = passesData.find(passItem => passItem.passId === passSelect.value);
    const qty = parseInt(qtySelect.value, 10) || 1;

    if (!selectedEvent || !selectedPass) {
      alert("Debes seleccionar un evento y un pase");
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/purchase`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          id_usuario: user.id_usuario,
          eventName: selectedEvent.name,
          dateLabel: selectedEvent.date,
          passType: selectedPass.label,
          quantity: qty
        })
      });

      if (!response.ok) {
        throw new Error("No se pudo completar la compra");
      }

      alert("Compra realizada correctamente");
      window.location.href = "./tickets.html";
    } catch (error) {
      console.error("Error en la compra:", error);
      alert("Error al realizar la compra");
    }
  });
}

async function initPurchase() {
  try {
    await loadPurchaseOptions();
    renderOptions();
    attachPurchaseHandler();
  } catch (error) {
    console.error("Error cargando opciones de compra:", error);
    alert("Error cargando las opciones de compra");
  }
}

document.addEventListener("DOMContentLoaded", initPurchase);
