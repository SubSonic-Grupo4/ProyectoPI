const AUTH_TOKEN_KEY = "authToken";

function authGetStoredUser() {
  try {
    return JSON.parse(localStorage.getItem("user"));
  } catch (error) {
    return null;
  }
}

function authGetToken() {
  return localStorage.getItem(AUTH_TOKEN_KEY);
}

function authSaveSession(user, token = null) {
  if (user) {
    localStorage.setItem("user", JSON.stringify(user));
  }

  if (token) {
    localStorage.setItem(AUTH_TOKEN_KEY, token);
  }
}

function authClearSession() {
  localStorage.removeItem("user");
  localStorage.removeItem(AUTH_TOKEN_KEY);
}

function authRequireSession() {
  const user = authGetStoredUser();
  const token = authGetToken();

  if (!user || !token) {
    authClearSession();
    window.location.href = "./login.html";
    return null;
  }

  return user;
}

function authBuildHeaders(existingHeaders = {}) {
  const headers = new Headers(existingHeaders);
  const token = authGetToken();

  if (token && !headers.has("Authorization")) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  return headers;
}

async function authFetch(url, options = {}) {
  const response = await fetch(url, {
    ...options,
    headers: authBuildHeaders(options.headers || {})
  });

  if (response.status === 401) {
    authClearSession();
    window.location.href = "./login.html";
    throw new Error("Sesion expirada o token invalido");
  }

  return response;
}
