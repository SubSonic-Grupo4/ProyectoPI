# Endpoints del modulo Proveedor

## Autenticacion
- `POST /login`
- `POST /token`

Las rutas privadas del proveedor requieren la cabecera:

```http
Authorization: Bearer <access_token>
```

## Espacios
- `GET /spaces`
- `GET /spaces/{id_espacio}`

## Perfil proveedor
- `GET /provider/profile/{id_usuario}`
- `PUT /provider/profile/{id_usuario}`
- `POST /provider/gallery/{id_usuario}`

## Solicitudes de alquiler
- `GET /provider/applications/{id_usuario}`
- `POST /provider/applications`

## Estadisticas
- `GET /provider/stats/{id_usuario}`
