from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.controller.security import ACCESS_TOKEN_EXPIRE_SECONDS, create_access_token, decode_access_token
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
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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


def build_auth_response(user):
    access_token = create_access_token(user)
    return {
        "message": "Login correcto",
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_SECONDS,
        "user": user.to_public_dict()
    }


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
    except ValueError as error:
        raise HTTPException(
            status_code=401,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"}
        ) from error

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Token sin usuario asociado",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = model.get_user_profile(user_id)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Usuario del token no encontrado",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user


def require_client_user(current_user=Depends(get_current_user)):
    if str(current_user.rol).upper() != "CLIENTE":
        raise HTTPException(status_code=403, detail="Acceso exclusivo para Cliente")
    return current_user


def require_provider_user(current_user=Depends(get_current_user)):
    if str(current_user.rol).upper() != "PROVEEDOR":
        raise HTTPException(status_code=403, detail="Acceso exclusivo para Proveedor")
    return current_user


def ensure_same_user(current_user, requested_user_id):
    if current_user.id_usuario != requested_user_id:
        raise HTTPException(status_code=403, detail="No puedes acceder a los datos de otro usuario")


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


@app.get("/events")
def get_public_events():
    return model.get_public_events()


@app.post("/login")
def login(data: LoginRequest):
    user = model.login(data.email, data.password)
    if user:
        return build_auth_response(user)
    raise HTTPException(status_code=401, detail="Credenciales incorrectas")


@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = model.login(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return {
        "access_token": create_access_token(user),
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_SECONDS
    }


@app.get("/profile/{id_usuario}")
def get_profile(id_usuario: str, current_user=Depends(require_client_user)):
    ensure_same_user(current_user, id_usuario)
    user = model.get_user_profile(id_usuario)
    if user:
        return user.to_public_dict()
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@app.put("/profile/{id_usuario}")
def update_profile(id_usuario: str, data: ProfileUpdateRequest, current_user=Depends(require_client_user)):
    ensure_same_user(current_user, id_usuario)
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
def get_tickets(id_usuario: str, current_user=Depends(require_client_user)):
    ensure_same_user(current_user, id_usuario)
    tickets = model.get_tickets_by_user(id_usuario)
    return [ticket.to_dict() for ticket in tickets]


@app.get("/ticket/{ticket_id}")
def get_ticket(ticket_id: str, current_user=Depends(require_client_user)):
    ticket = model.get_ticket_by_id(ticket_id)
    if ticket:
        if ticket.id_usuario != current_user.id_usuario:
            raise HTTPException(status_code=403, detail="No puedes acceder a tickets de otro usuario")
        return ticket.to_dict()
    raise HTTPException(status_code=404, detail="Ticket no encontrado")


@app.get("/purchase/options")
def get_purchase_options(current_user=Depends(require_client_user)):
    options = model.get_purchase_options()
    return options.to_dict()


@app.put("/ticket/cancel/{ticket_id}")
def cancel_ticket(ticket_id: str, current_user=Depends(require_client_user)):
    ticket = model.get_ticket_by_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    if ticket.id_usuario != current_user.id_usuario:
        raise HTTPException(status_code=403, detail="No puedes cancelar tickets de otro usuario")
    updated = model.cancel_ticket(ticket_id)
    if updated:
        return {"message": "Entrada cancelada correctamente"}
    raise HTTPException(status_code=404, detail="Ticket no encontrado")


@app.post("/purchase")
def purchase(data: PurchaseRequest, current_user=Depends(require_client_user)):
    ensure_same_user(current_user, data.id_usuario)
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
def get_spaces(tipo: str | None = None, only_available: bool = False, current_user=Depends(require_provider_user)):
    return model.get_spaces(tipo=tipo, only_available=only_available)


@app.get("/spaces/{id_espacio}")
def get_space(id_espacio: str, current_user=Depends(require_provider_user)):
    space = model.get_space_by_id(id_espacio)
    if space:
        return space
    raise HTTPException(status_code=404, detail="Espacio no encontrado")


@app.get("/provider/profile/{id_usuario}")
def get_provider_profile(id_usuario: str, current_user=Depends(require_provider_user)):
    ensure_same_user(current_user, id_usuario)
    profile, error = model.get_provider_profile(id_usuario)
    if profile:
        return profile
    status = 403 if error == "El usuario no pertenece al perfil Proveedor" else 404
    raise HTTPException(status_code=status, detail=error)


@app.put("/provider/profile/{id_usuario}")
def update_provider_profile(id_usuario: str, data: ProviderProfileUpdateRequest, current_user=Depends(require_provider_user)):
    ensure_same_user(current_user, id_usuario)
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
def add_gallery_image(id_usuario: str, data: GalleryImageRequest, current_user=Depends(require_provider_user)):
    ensure_same_user(current_user, id_usuario)
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
def get_provider_applications(id_usuario: str, current_user=Depends(require_provider_user)):
    ensure_same_user(current_user, id_usuario)
    applications, error = model.get_applications_by_provider(id_usuario)
    if applications is not None:
        return applications
    status = 403 if error == "El usuario no pertenece al perfil Proveedor" else 404
    raise HTTPException(status_code=status, detail=error)


@app.post("/provider/applications")
def create_provider_application(data: ApplicationCreateRequest, current_user=Depends(require_provider_user)):
    ensure_same_user(current_user, data.id_proveedor)
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
def get_provider_stats(id_usuario: str, current_user=Depends(require_provider_user)):
    ensure_same_user(current_user, id_usuario)
    stats, error = model.get_provider_stats(id_usuario)
    if stats:
        return stats
    status = 403 if error == "El usuario no pertenece al perfil Proveedor" else 404
    raise HTTPException(status_code=status, detail=error)
