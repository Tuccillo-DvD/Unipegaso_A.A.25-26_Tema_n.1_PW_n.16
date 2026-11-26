from typing import Callable

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from config import settings
from database import get_db
from modelli import Utente

oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_utente_corrente(
    token: str = Depends(oauth2_schema),
    db: Session = Depends(get_db),
) -> Utente:
    """Restituisce l'utente identificato dal token, oppure risponde 401"""
    errore = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token non valido o scaduto",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        contenuto = jwt.decode(
            token,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=[settings.JWT_ALGORITHM],
        )
        id_utente = int(contenuto["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        raise errore

    utente = db.get(Utente, id_utente)
    if utente is None or not utente.attivo:
        raise errore
    return utente


def richiedi_ruoli(*ruoli_ammessi: str) -> Callable[[Utente], Utente]:
    """Crea una dipendenza che ammette solo gli utenti con uno dei ruoli indicati"""

    def verifica(utente: Utente = Depends(get_utente_corrente)) -> Utente:
        if utente.ruolo not in ruoli_ammessi:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permessi insufficienti",
            )
        return utente

    return verifica