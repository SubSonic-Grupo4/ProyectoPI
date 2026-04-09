from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.model.model import Model


app = FastAPI(title="Subsonic Festival API", version="1.0.0")
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


class ProfileUpdateRequest(BaseModel):
    name: str
    email: str
    address: str
    avatarUrl: str | None = None


class PurchaseRequest(BaseModel):
    id_usuario: str
    eventName: str
    dateLabel: str
    passType: str
    quantity: int


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


@app.middleware("http")
async def disable_static_cache(request: Request, call_next):
    response = await call_next(request)

    if request.url.path.startswith(("/pages/", "/js/", "/css/")):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"

    return response


@app.get("/")
def root():
    return {"message": "Backend Subsonic funcionando"}


@app.post("/login")
def login(data: LoginRequest):
    user = model.login(data.email, data.password)
    if user:
        return {
            "message": "Login correcto",
            "user": user.to_public_dict()
        }
    raise HTTPException(status_code=401, detail="Credenciales incorrectas")


@app.get("/profile/{id_usuario}")
def get_profile(id_usuario: str):
    user = model.get_user_profile(id_usuario)
    if user:
        return user.to_public_dict()
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@app.put("/profile/{id_usuario}")
def update_profile(id_usuario: str, data: ProfileUpdateRequest):
    updated_user = model.update_user_profile(
        id_usuario=id_usuario,
        name=data.name,
        email=data.email,
        address=data.address,
        avatarUrl=data.avatarUrl
    )

    if updated_user:
        return {
            "message": "Perfil actualizado correctamente",
            "user": updated_user.to_public_dict()
        }

    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@app.get("/tickets/{id_usuario}")
def get_tickets(id_usuario: str):
    tickets = model.get_tickets_by_user(id_usuario)
    return [ticket.to_dict() for ticket in tickets]


@app.get("/ticket/{ticket_id}")
def get_ticket(ticket_id: str):
    ticket = model.get_ticket_by_id(ticket_id)
    if ticket:
        return ticket.to_dict()
    raise HTTPException(status_code=404, detail="Ticket no encontrado")


@app.get("/purchase/options")
def get_purchase_options():
    options = model.get_purchase_options()
    return options.to_dict()


@app.put("/ticket/cancel/{ticket_id}")
def cancel_ticket(ticket_id: str):
    updated = model.cancel_ticket(ticket_id)
    if updated:
        return {"message": "Entrada cancelada correctamente"}
    raise HTTPException(status_code=404, detail="Ticket no encontrado")


@app.post("/purchase")
def purchase(data: PurchaseRequest):
    created_tickets = model.purchase_tickets(
        id_usuario=data.id_usuario,
        eventName=data.eventName,
        dateLabel=data.dateLabel,
        passType=data.passType,
        quantity=data.quantity
    )

    if created_tickets is None:
        raise HTTPException(status_code=400, detail="No se pudo completar la compra")

    return {
        "message": "Compra realizada correctamente",
        "tickets": [ticket.to_dict() for ticket in created_tickets]
    }


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
