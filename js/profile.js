const API_BASE_URL = "";

let currentUser = null;

function getStoredUser() {
  return JSON.parse(localStorage.getItem("user"));
}

function saveStoredUser(user) {
  localStorage.setItem("user", JSON.stringify(user));
}

function renderProfileFields(user) {
  const img = document.getElementById("profileImage");
  const nameInput = document.getElementById("profileName");
  const emailInput = document.getElementById("profileEmail");
  const addressInput = document.getElementById("profileAddress");

  if (nameInput) nameInput.value = user.name || "";
  if (emailInput) emailInput.value = user.email || "";
  if (addressInput) addressInput.value = user.address || "";
  if (img && user.avatarUrl) img.src = user.avatarUrl;
}

async function loadProfileFromBackend() {
  const storedUser = getStoredUser();

  if (!storedUser) {
    window.location.href = "login.html";
    return;
  }

  currentUser = storedUser;
  renderProfileFields(currentUser);

  try {
    const response = await fetch(`${API_BASE_URL}/profile/${currentUser.id_usuario}`);

    if (!response.ok) {
      throw new Error("No se pudo cargar el perfil");
    }

    currentUser = await response.json();
    saveStoredUser(currentUser);
    renderProfileFields(currentUser);
  } catch (error) {
    console.error("Error cargando perfil:", error);
  }
}

function attachImageUpload() {
  const img = document.getElementById("profileImage");
  const upload = document.getElementById("imageUpload");

  if (!upload || !img) return;

  upload.addEventListener("change", function () {
    const file = this.files && this.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function (event) {
      img.src = event.target.result;

      if (currentUser) {
        currentUser.avatarUrl = event.target.result;
      }
    };
    reader.readAsDataURL(file);
  });
}

function attachSaveHandler() {
  const saveBtn = document.getElementById("saveProfileBtn");
  const nameInput = document.getElementById("profileName");
  const emailInput = document.getElementById("profileEmail");
  const addressInput = document.getElementById("profileAddress");

  if (!saveBtn) return;

  saveBtn.addEventListener("click", async () => {
    if (!currentUser) {
      alert("Debes iniciar sesion");
      window.location.href = "login.html";
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/profile/${currentUser.id_usuario}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          name: nameInput ? nameInput.value : "",
          email: emailInput ? emailInput.value : "",
          address: addressInput ? addressInput.value : "",
          avatarUrl: currentUser.avatarUrl || null
        })
      });

      if (!response.ok) {
        throw new Error("No se pudo guardar el perfil");
      }

      const data = await response.json();
      currentUser = data.user;
      saveStoredUser(currentUser);
      renderProfileFields(currentUser);

      alert("Perfil actualizado correctamente");
    } catch (error) {
      console.error("Error guardando perfil:", error);
      alert("Error al guardar el perfil");
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  loadProfileFromBackend();
  attachImageUpload();
  attachSaveHandler();
});
