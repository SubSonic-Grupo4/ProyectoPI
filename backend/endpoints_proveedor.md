# Endpoints del módulo Proveedor

## Autenticación
- `POST /login`

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

## Estadísticas
- `GET /provider/stats/{id_usuario}`
