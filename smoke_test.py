from fastapi.testclient import TestClient

from backend.controller.controller import app


client = TestClient(app)


def login_json(email, password):
    response = client.post("/login", json={"email": email, "password": password})
    assert response.status_code == 200, response.text
    return response.json()


def bearer_headers(access_token):
    return {"Authorization": f"Bearer {access_token}"}


# Root publico
response = client.get("/")
assert response.status_code == 200, response.text

# Visitante publico
response = client.get("/events")
assert response.status_code == 200, response.text
assert len(response.json()) >= 1, response.text

# Login cliente con token
client_login = login_json("cliente@subsonic.es", "password123")
assert client_login["user"]["rol"] == "CLIENTE", client_login
client_headers = bearer_headers(client_login["access_token"])

# Login proveedor con token
provider_login = login_json("proveedor@subsonic.es", "password123")
assert provider_login["user"]["rol"] == "PROVEEDOR", provider_login
provider_id = provider_login["user"]["id_usuario"]
provider_headers = bearer_headers(provider_login["access_token"])

# Flujo Cliente
response = client.get("/profile/C-001", headers=client_headers)
assert response.status_code == 200, response.text

response = client.get("/tickets/C-001", headers=client_headers)
assert response.status_code == 200, response.text

response = client.get("/purchase/options", headers=client_headers)
assert response.status_code == 200, response.text

# Flujo Proveedor
response = client.get("/spaces", headers=provider_headers)
assert response.status_code == 200, response.text
spaces = response.json()
assert len(spaces) >= 1, spaces
space_id = spaces[0]["idEspacio"]

response = client.get(f"/spaces/{space_id}", headers=provider_headers)
assert response.status_code == 200, response.text

response = client.get(f"/provider/profile/{provider_id}", headers=provider_headers)
assert response.status_code == 200, response.text

response = client.get(f"/provider/applications/{provider_id}", headers=provider_headers)
assert response.status_code == 200, response.text

response = client.get(f"/provider/stats/{provider_id}", headers=provider_headers)
assert response.status_code == 200, response.text

# Sin token no se puede acceder
response = client.get("/tickets/C-001")
assert response.status_code == 401, response.text

# Un proveedor no puede usar rutas de cliente
response = client.get("/tickets/C-001", headers=provider_headers)
assert response.status_code == 403, response.text

# OAuth2 password flow
response = client.post(
    "/token",
    data={"username": "cliente@subsonic.es", "password": "password123"}
)
assert response.status_code == 200, response.text
assert response.json()["token_type"] == "bearer", response.text

print("SMOKE TEST OK")
