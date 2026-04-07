from fastapi.testclient import TestClient
from backend.controller.controller import app

client = TestClient(app)

# Root
resp = client.get('/')
assert resp.status_code == 200, resp.text

# Login proveedor
resp = client.post('/login', json={'email': 'proveedor@subsonic.es', 'password': 'password123'})
assert resp.status_code == 200, resp.text
user = resp.json()['user']
assert user['rol'] == 'PROVEEDOR', user
provider_id = user['id_usuario']

# Espacios
resp = client.get('/spaces?tipo=FOOD&only_available=true')
assert resp.status_code == 200, resp.text
spaces = resp.json()
assert len(spaces) >= 1, spaces
space_id = spaces[0]['idEspacio']

resp = client.get(f'/spaces/{space_id}')
assert resp.status_code == 200, resp.text

# Perfil proveedor
resp = client.get(f'/provider/profile/{provider_id}')
assert resp.status_code == 200, resp.text

resp = client.put(
    f'/provider/profile/{provider_id}',
    json={
        'name': 'Laura García',
        'email': 'proveedor@subsonic.es',
        'address': 'Avenida actualizada 99, Cáceres',
        'avatarUrl': 'https://example.com/avatar.png',
        'businessName': 'Food Trucks SL',
        'phone': '+34 600 111 222',
        'biography': 'Bio actualizada',
        'facebook': 'https://facebook.com/foodtruckssl',
        'instagram': 'https://instagram.com/foodtruckssl',
        'x': 'https://x.com/foodtruckssl',
        'website': 'https://foodtruckssl.example.com'
    }
)
assert resp.status_code == 200, resp.text

resp = client.post(f'/provider/gallery/{provider_id}', json={'imageUrl': 'https://example.com/gallery-1.jpg'})
assert resp.status_code == 200, resp.text

# Solicitudes
resp = client.get(f'/provider/applications/{provider_id}')
assert resp.status_code == 200, resp.text

resp = client.post(
    '/provider/applications',
    json={
        'id_proveedor': provider_id,
        'id_espacio': 'ESP-MERCH-01',
        'descripcion': 'Puesto temporal de productos exclusivos.',
        'categoriaServicio': 'MERCH',
        'portfolioUrl': 'https://example.com/portfolio'
    }
)
assert resp.status_code == 200, resp.text

# Estadísticas
resp = client.get(f'/provider/stats/{provider_id}')
assert resp.status_code == 200, resp.text
stats = resp.json()
assert 'totalSolicitudes' in stats, stats
assert 'activityLog' in stats, stats

# Usuario no proveedor
resp = client.get('/provider/profile/C-001')
assert resp.status_code == 403, resp.text

print('SMOKE TEST OK')
