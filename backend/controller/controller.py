from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.model.model import Model


app = FastAPI(title="Subsonic Festival - Proveedor API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parents[2]
app.mount("/pages", StaticFiles(directory=BASE_DIR / "pages"), name="pages")
app.mount("/js", StaticFiles(directory=BASE_DIR / "js"), name="js")
app.mount("/css", StaticFiles(directory=BASE_DIR / "css"), name="css")

model = Model()


class LoginRequest(BaseModel):
    email: str
    password: str


class ProviderProfileUpdateRequest(BaseModel):
    name: str
    email: str
    address: str
    avatarUrl: str | None = None
    businessName: str | None = None
    phone: str | None = None
    biography: str | None = None
    facebook: str | None = None
    instagram: str | None = None
    x: str | None = None
    website: str | None = None


class GalleryImageRequest(BaseModel):
    imageUrl: str


class ApplicationCreateRequest(BaseModel):
    id_proveedor: str
    id_espacio: str
    descripcion: str
    categoriaServicio: str
    portfolioUrl: str | None = None


@app.get("/")
def root():
    return {"message": "Backend Subsonic Proveedor funcionando"}


@app.post("/login")
def login(data: LoginRequest):
    user = model.login(data.email, data.password)
    if user:
        return {
            "message": "Login correcto",
            "user": user.to_public_dict()
        }
    raise HTTPException(status_code=401, detail="Credenciales incorrectas")


@app.get("/spaces")
def get_spaces(tipo: str | None = None, only_available: bool = False):
    return model.get_spaces(tipo=tipo, only_available=only_available)


@app.get("/spaces/{id_espacio}")
def get_space(id_espacio: str):
    space = model.get_space_by_id(id_espacio)
    if space:
        return space
    raise HTTPException(status_code=404, detail="Espacio no encontrado")


@app.get("/provider/profile/{id_usuario}")
def get_provider_profile(id_usuario: str):
    profile, error = model.get_provider_profile(id_usuario)
    if profile:
        return profile
    status = 403 if error == "El usuario no pertenece al perfil Proveedor" else 404
    raise HTTPException(status_code=status, detail=error)


@app.put("/provider/profile/{id_usuario}")
def update_provider_profile(id_usuario: str, data: ProviderProfileUpdateRequest):
    profile, error = model.update_provider_profile(
        id_usuario=id_usuario,
        name=data.name,
        email=data.email,
        address=data.address,
        avatarUrl=data.avatarUrl,
        businessName=data.businessName,
        phone=data.phone,
        biography=data.biography,
        socialLinks={
            "facebook": data.facebook or "",
            "instagram": data.instagram or "",
            "x": data.x or "",
            "website": data.website or "",
        }
    )
    if profile:
        return {
            "message": "Perfil de proveedor actualizado correctamente",
            "profile": profile
        }
    status = 403 if error == "El usuario no pertenece al perfil Proveedor" else 404
    raise HTTPException(status_code=status, detail=error)


@app.post("/provider/gallery/{id_usuario}")
def add_gallery_image(id_usuario: str, data: GalleryImageRequest):
    profile, error = model.add_gallery_image(id_usuario, data.imageUrl)
    if profile:
        return {
            "message": "Imagen añadida a la galería",
            "gallery": profile["gallery"]
        }
    status = 403 if error == "El usuario no pertenece al perfil Proveedor" else 404
    if error == "La URL de imagen es obligatoria":
        status = 400
    raise HTTPException(status_code=status, detail=error)


@app.get("/provider/applications/{id_usuario}")
def get_provider_applications(id_usuario: str):
    applications, error = model.get_applications_by_provider(id_usuario)
    if applications is not None:
        return applications
    status = 403 if error == "El usuario no pertenece al perfil Proveedor" else 404
    raise HTTPException(status_code=status, detail=error)


@app.post("/provider/applications")
def create_provider_application(data: ApplicationCreateRequest):
    application, error = model.create_application(
        id_proveedor=data.id_proveedor,
        id_espacio=data.id_espacio,
        descripcion=data.descripcion,
        categoria_servicio=data.categoriaServicio,
        portfolio_url=data.portfolioUrl,
    )
    if application:
        return {
            "message": "Solicitud enviada correctamente",
            "application": application
        }
    if error in ("El usuario no pertenece al perfil Proveedor",):
        raise HTTPException(status_code=403, detail=error)
    if error in ("Espacio no encontrado", "Usuario no encontrado"):
        raise HTTPException(status_code=404, detail=error)
    raise HTTPException(status_code=400, detail=error)


@app.get("/provider/stats/{id_usuario}")
def get_provider_stats(id_usuario: str):
    stats, error = model.get_provider_stats(id_usuario)
    if stats:
        return stats
    status = 403 if error == "El usuario no pertenece al perfil Proveedor" else 404
    raise HTTPException(status_code=status, detail=error)
