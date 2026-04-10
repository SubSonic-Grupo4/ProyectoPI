import base64
import hashlib
import hmac
import json
import os
import time


SECRET_KEY = os.getenv("SUBSONIC_SECRET_KEY", "subsonic-festival-practica-03-secret")
ACCESS_TOKEN_EXPIRE_SECONDS = 60 * 60 * 8


def _b64url_encode(raw_bytes):
    return base64.urlsafe_b64encode(raw_bytes).rstrip(b"=").decode("ascii")


def _b64url_decode(encoded_value):
    padding = "=" * (-len(encoded_value) % 4)
    return base64.urlsafe_b64decode(encoded_value + padding)


def _sign(message):
    signature = hmac.new(
        SECRET_KEY.encode("utf-8"),
        message.encode("ascii"),
        hashlib.sha256
    ).digest()
    return _b64url_encode(signature)


def create_access_token(user):
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": user.id_usuario,
        "rol": user.rol,
        "email": user.email,
        "exp": int(time.time()) + ACCESS_TOKEN_EXPIRE_SECONDS
    }

    header_segment = _b64url_encode(
        json.dumps(header, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    )
    payload_segment = _b64url_encode(
        json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    )
    signing_input = f"{header_segment}.{payload_segment}"

    return f"{signing_input}.{_sign(signing_input)}"


def decode_access_token(token):
    try:
        header_segment, payload_segment, signature_segment = token.split(".")
    except ValueError as exc:
        raise ValueError("Token mal formado") from exc

    signing_input = f"{header_segment}.{payload_segment}"
    expected_signature = _sign(signing_input)

    if not hmac.compare_digest(signature_segment, expected_signature):
        raise ValueError("Firma del token invalida")

    try:
        payload = json.loads(_b64url_decode(payload_segment).decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError, ValueError) as exc:
        raise ValueError("Payload del token invalido") from exc

    if int(payload.get("exp", 0)) < int(time.time()):
        raise ValueError("Token expirado")

    return payload
