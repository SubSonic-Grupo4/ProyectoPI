// js/purchase.js

function fillSelect(selectEl, optionsHtml) {
  selectEl.innerHTML = optionsHtml;
}

function renderPurchase() {
  const eventSelect = document.getElementById("eventSelect");
  const passSelect = document.getElementById("passSelect");
  const qtySelect = document.getElementById("qtySelect");
  const confirmBtn = document.getElementById("confirmPurchaseBtn");

  const eventTitle = document.getElementById("eventTitle");
  const eventDate = document.getElementById("eventDate");

  if (!eventSelect || !passSelect || !qtySelect || !confirmBtn) return;

  // Si en tu data.js NO tienes events/passes, los creamos aquí por seguridad
  const data = window.SubsonicData;

  if (!data.events) {
    data.events = [
      { eventId: "E-101", name: "Subsonic Main Stage", date: "12/07/2026" },
      { eventId: "E-202", name: "Subsonic Underground", date: "20/07/2026" }
    ];
  }

  if (!data.passes) {
    data.passes = [
      { passId: "P-GEN", label: "Pase General", price: 49 },
      { passId: "P-VIP", label: "Pase VIP", price: 89 },
      { passId: "P-FULL", label: "Full Experience", price: 129 }
    ];
  }

  // Rellenar evento
  fillSelect(eventSelect, data.events.map(e =>
    `<option value="${e.eventId}">${e.name} - ${e.date}</option>`
  ).join(""));

  // Rellenar pase
  fillSelect(passSelect, data.passes.map(p =>
    `<option value="${p.passId}">${p.label} - ${p.price}€</option>`
  ).join(""));

  // Rellenar cantidad
  fillSelect(qtySelect, [1,2,3,4].map(n =>
    `<option value="${n}">${n}</option>`
  ).join(""));

  // Actualiza título/fecha visual según el evento seleccionado
  function updateEventPreview() {
    const selected = data.events.find(e => e.eventId === eventSelect.value);
    if (!selected) return;
    if (eventTitle) eventTitle.textContent = selected.name;
    if (eventDate) eventDate.textContent = selected.date;
  }

  eventSelect.addEventListener("change", updateEventPreview);
  updateEventPreview();

  // Confirmar compra (simulada)
  confirmBtn.addEventListener("click", () => {
    const selectedEvent = data.events.find(e => e.eventId === eventSelect.value);
    const selectedPass = data.passes.find(p => p.passId === passSelect.value);
    const qty = parseInt(qtySelect.value, 10) || 1;

    if (!selectedEvent || !selectedPass) return;

    // Crear X tickets
    for (let i = 0; i < qty; i++) {
      const newId = `T-${Math.floor(1000 + Math.random() * 9000)}`;

      // Mantengo el formato que usas en tickets (eventName, dateLabel, passType, status)
      data.tickets.push({
        ticketId: newId,
        eventName: selectedEvent.name,
        dateLabel: selectedEvent.date,
        monthDay: "NEW",            // opcional
        passType: selectedPass.label.replace("Pase ", ""), // para que quede "VIP" o "General"
        status: "Activa"
      });
    }

    // Ir a Mis Entradas
    window.location.href = "./tickets.html";
  });
}

document.addEventListener("DOMContentLoaded", renderPurchase);