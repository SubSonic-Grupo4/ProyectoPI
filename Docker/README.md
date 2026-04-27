# Practica 04 - Docker y Azure

Esta carpeta contiene los archivos necesarios para construir la imagen Docker del proyecto SubSonic Festival y desplegarla en Azure.

## Imagen base usada

- Imagen: `python:3.11-slim`
- Origen: Docker Hub
- Finalidad: ejecutar la aplicacion Python/FastAPI dentro del contenedor.

## Construir la imagen en local

Ejecutar desde la raiz del repositorio:

```powershell
docker build -f Docker/Dockerfile -t subsonic-festival:practica04 .
```

## Probar el contenedor en local

```powershell
docker run --rm -p 8000:8000 subsonic-festival:practica04
```

Abrir en el navegador:

```text
http://127.0.0.1:8000/pages/visitante.html
http://127.0.0.1:8000/pages/login.html
http://127.0.0.1:8000/docs
```

## Credenciales de prueba

Cliente:

```text
cliente@subsonic.es
password123
```

Proveedor:

```text
proveedor@subsonic.es
password123
```

## Despliegue en Azure

La guia de comandos esta en:

```text
Docker/azure-deploy-template.ps1
```

Antes de ejecutarla, revisar los nombres de variables para que coincidan con el grupo y la cuenta de Azure usada en la entrega.
