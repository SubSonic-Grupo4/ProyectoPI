// js/profile.js

function renderProfile() {
  const user = window.SubsonicData.currentUser;

  const img = document.getElementById("profileImage");
  const upload = document.getElementById("imageUpload");

  const nameInput = document.getElementById("profileName");
  const emailInput = document.getElementById("profileEmail");
  const addressInput = document.getElementById("profileAddress");
  const saveBtn = document.getElementById("saveProfileBtn");

  // Pintar datos desde "JSON"
  if (nameInput) nameInput.value = user.name || "";
  if (emailInput) emailInput.value = user.email || "";
  if (addressInput) addressInput.value = user.address || "";
  if (img) img.src = user.avatarUrl || img.src;

  // Vista previa + guardar avatar en "JSON"
  if (upload && img) {
    upload.addEventListener("change", function() {
      const file = this.files && this.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = function(e) {
        img.src = e.target.result;

        // Guardamos el avatar en memoria (simulado)
        user.avatarUrl = e.target.result;
      };
      reader.readAsDataURL(file);
    });
  }

  // Guardar cambios (simulado)
  if (saveBtn) {
    saveBtn.addEventListener("click", () => {
      if (nameInput) user.name = nameInput.value;
      if (emailInput) user.email = emailInput.value;
      if (addressInput) user.address = addressInput.value;

      alert("Perfil actualizado (simulado).");
    });
  }
}

document.addEventListener("DOMContentLoaded", renderProfile);