const API_BASE_URL = "";

let currentProvider = null;

function getStoredUser() {
  return JSON.parse(localStorage.getItem("user"));
}

function saveStoredUser(user) {
  localStorage.setItem("user", JSON.stringify(user));
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
  const box = document.getElementById("providerMessage");
  if (!box) return;

  box.hidden = false;
  box.textContent = message;
  box.classList.toggle("error", isError);
}

function clearMessage() {
  const box = document.getElementById("providerMessage");
  if (!box) return;

  box.hidden = true;
  box.textContent = "";
  box.classList.remove("error");
}

function renderGallery(gallery) {
  const grid = document.getElementById("galleryGrid");
  const counter = document.getElementById("galleryCounter");

  if (counter) {
    const total = Array.isArray(gallery) ? gallery.length : 0;
    counter.textContent = `${total} imagen${total === 1 ? "" : "es"}`;
  }

  if (!grid) return;

  if (!gallery || gallery.length === 0) {
    grid.innerHTML = '<p class="empty-state">Todavia no hay imagenes en la galeria.</p>';
    return;
  }

  grid.innerHTML = gallery.map((imageUrl, index) => `
    <div class="gallery-item">
      <img src="${imageUrl}" alt="Imagen ${index + 1} de la galeria">
      <span>Imagen ${index + 1}</span>
    </div>
  `).join("");
}

function renderProviderProfile(profile) {
  currentProvider = profile;
  saveStoredUser(profile);

  const socialLinks = profile.socialLinks || {};

  const mappings = [
    ["providerAvatar", "src", profile.avatarUrl || "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d"],
    ["profileImage", "src", profile.avatarUrl || "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d"],
    ["providerBusinessLabel", "textContent", profile.businessName || profile.name || "Proveedor"],
    ["providerEmailLabel", "textContent", profile.email || ""],
    ["profileName", "value", profile.name || ""],
    ["businessName", "value", profile.businessName || ""],
    ["profileEmail", "value", profile.email || ""],
    ["profilePhone", "value", profile.phone || ""],
    ["profileAddress", "value", profile.address || ""],
    ["profileBiography", "value", profile.biography || ""],
    ["socialFacebook", "value", socialLinks.facebook || ""],
    ["socialInstagram", "value", socialLinks.instagram || ""],
    ["socialX", "value", socialLinks.x || ""],
    ["socialWebsite", "value", socialLinks.website || ""]
  ];

  mappings.forEach(([id, property, value]) => {
    const element = document.getElementById(id);
    if (element) {
      element[property] = value;
    }
  });

  renderGallery(profile.gallery || []);
}

async function loadProviderProfile() {
  const user = ensureProviderAccess();
  if (!user) return;

  try {
    const response = await fetch(`${API_BASE_URL}/provider/profile/${user.id_usuario}`);

    if (!response.ok) {
      throw new Error("No se pudo cargar el perfil del proveedor");
    }

    const profile = await response.json();
    renderProviderProfile(profile);
  } catch (error) {
    console.error(error);
    showMessage("No se pudo cargar el perfil del proveedor.", true);
  }
}

async function saveProviderProfile() {
  if (!currentProvider) return;

  clearMessage();

  const payload = {
    name: document.getElementById("profileName")?.value || "",
    email: document.getElementById("profileEmail")?.value || "",
    address: document.getElementById("profileAddress")?.value || "",
    avatarUrl: currentProvider.avatarUrl || null,
    businessName: document.getElementById("businessName")?.value || "",
    phone: document.getElementById("profilePhone")?.value || "",
    biography: document.getElementById("profileBiography")?.value || "",
    facebook: document.getElementById("socialFacebook")?.value || "",
    instagram: document.getElementById("socialInstagram")?.value || "",
    x: document.getElementById("socialX")?.value || "",
    website: document.getElementById("socialWebsite")?.value || ""
  };

  try {
    const response = await fetch(`${API_BASE_URL}/provider/profile/${currentProvider.id_usuario}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error("No se pudo guardar el perfil");
    }

    const data = await response.json();
    renderProviderProfile(data.profile);
    showMessage("Perfil actualizado correctamente.");
  } catch (error) {
    console.error(error);
    showMessage("Error al guardar el perfil del proveedor.", true);
  }
}

function readFileAsDataUrl(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (event) => resolve(event.target.result);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

async function uploadGalleryImage(file) {
  if (!currentProvider || !file) return;

  try {
    const imageUrl = await readFileAsDataUrl(file);
    const response = await fetch(`${API_BASE_URL}/provider/gallery/${currentProvider.id_usuario}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ imageUrl })
    });

    if (!response.ok) {
      throw new Error("No se pudo anadir la imagen");
    }

    const data = await response.json();
    currentProvider.gallery = data.gallery || [];
    renderGallery(currentProvider.gallery);
    saveStoredUser(currentProvider);
    showMessage("Imagen anadida a la galeria correctamente.");
  } catch (error) {
    console.error(error);
    showMessage("No se pudo anadir la imagen a la galeria.", true);
  }
}

function attachAvatarHandler() {
  const input = document.getElementById("imageUpload");
  if (!input) return;

  input.addEventListener("change", async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    try {
      const imageUrl = await readFileAsDataUrl(file);
      currentProvider.avatarUrl = imageUrl;
      document.getElementById("profileImage").src = imageUrl;
      document.getElementById("providerAvatar").src = imageUrl;
      showMessage("Avatar preparado. Pulsa Guardar cambios para persistirlo.");
    } catch (error) {
      console.error(error);
      showMessage("No se pudo cargar la imagen del avatar.", true);
    } finally {
      input.value = "";
    }
  });
}

function attachGalleryHandler() {
  const input = document.getElementById("galleryUpload");
  if (!input) return;

  input.addEventListener("change", async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    await uploadGalleryImage(file);
    input.value = "";
  });
}

function attachLogout() {
  const button = document.getElementById("logoutBtn");
  if (!button) return;

  button.addEventListener("click", () => {
    localStorage.removeItem("user");
    window.location.href = "./login.html";
  });
}

document.addEventListener("DOMContentLoaded", () => {
  if (!ensureProviderAccess()) {
    return;
  }

  loadProviderProfile();
  attachAvatarHandler();
  attachGalleryHandler();
  attachLogout();

  const saveButton = document.getElementById("saveProviderProfileBtn");
  if (saveButton) {
    saveButton.addEventListener("click", saveProviderProfile);
  }
});
