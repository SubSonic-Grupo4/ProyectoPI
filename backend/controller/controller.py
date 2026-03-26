from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from backend.model.model import Model
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # luego se puede restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parents[2]

app.mount("/pages", StaticFiles(directory=BASE_DIR / "pages"), name="pages")
app.mount("/js", StaticFiles(directory=BASE_DIR / "js"), name="js")
app.mount("/css", StaticFiles(directory=BASE_DIR / "css"), name="css")

model = Model()


@app.middleware("http")
async def disable_static_cache(request: Request, call_next):
    response = await call_next(request)

    if request.url.path.startswith(("/pages/", "/js/", "/css/")):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"

    return response


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
