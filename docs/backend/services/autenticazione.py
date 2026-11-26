from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from config import settings
from modelli import Utente

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash fittizio  serve a impiegare lo stesso tempo anche quando l'email non esiste
_HASH_FITTIZIO = pwd_context.hash("password-fittizia")


def verifica_password(password_in_chiaro: str, password_hash: str) -> bool:
    """Confronta una password con il suo hash bcrypt"""
    return pwd_context.verify(password_in_chiaro, password_hash)


def autentica_utente(db: Session, email: str, password: str) -> Optional[Utente]:
    """Restituisce l'utente se le credenziali sono valide e l'account è attivo"""
    utente = db.scalars(select(Utente).where(Utente.email == email)).first()
    if utente is None:
        verifica_password(password, _HASH_FITTIZIO)
        return None
    if not verifica_password(password, utente.password_hash):
        return None
    if not utente.attivo:
        return None
    return utente


def crea_token_accesso(utente: Utente) -> str:
    """Crea un token JWT firmato, con id, ruolo e scadenza"""
    scadenza = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    contenuto = {
        "sub": str(utente.id_utente),
        "ruolo": utente.ruolo,
        "exp": scadenza,
    }
    return jwt.encode(
        contenuto,
        settings.SECRET_KEY.get_secret_value(),
        algorithm=settings.JWT_ALGORITHM,
    )