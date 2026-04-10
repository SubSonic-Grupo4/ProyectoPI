# Endpoints Cliente - Subsonic Festival

## Autenticacion
- `POST /login`
- `POST /token`

Las rutas privadas del cliente requieren la cabecera:

```http
Authorization: Bearer <access_token>
```

## 1. Login
- Metodo: `POST`
- URL: `/login`
- Uso: autenticar al cliente y devolver `access_token`
- Body JSON:

```json
{
  "email": "cliente@subsonic.es",
  "password": "password123"
}
```

## 2. Obtener perfil
- Metodo: `GET`
- URL: `/profile/{id_usuario}`
- Uso: cargar el perfil del cliente autenticado
- Requiere token `Bearer`

## 3. Actualizar perfil
- Metodo: `PUT`
- URL: `/profile/{id_usuario}`
- Uso: guardar nombre, email, direccion y avatar del cliente
- Requiere token `Bearer`
- Body JSON:

```json
{
  "name": "Nombre Apellidos",
  "email": "cliente@subsonic.es",
  "address": "Calle Ejemplo 123, Madrid",
  "avatarUrl": "https://i.pravatar.cc/150?img=12"
}
```

## 4. Obtener tickets del usuario
- Metodo: `GET`
- URL: `/tickets/{id_usuario}`
- Uso: listar las entradas del cliente
- Requiere token `Bearer`

## 5. Obtener detalle de ticket
- Metodo: `GET`
- URL: `/ticket/{ticket_id}`
- Uso: ver la informacion completa de una entrada
- Requiere token `Bearer`

## 6. Obtener opciones de compra
- Metodo: `GET`
- URL: `/purchase/options`
- Uso: cargar desde backend los eventos y pases disponibles en la pantalla de compra
- Requiere token `Bearer`

## 7. Cancelar ticket
- Metodo: `PUT`
- URL: `/ticket/cancel/{ticket_id}`
- Uso: cambiar el estado de una entrada a `Cancelada`
- Requiere token `Bearer`

## 8. Comprar entradas
- Metodo: `POST`
- URL: `/purchase`
- Uso: crear una o varias entradas nuevas en `tickets.json`
- Requiere token `Bearer`
- Body JSON:

```json
{
  "id_usuario": "C-001",
  "eventName": "Subsonic Main Stage",
  "dateLabel": "12/07/2026",
  "passType": "Pase VIP",
  "quantity": 2
}
```
