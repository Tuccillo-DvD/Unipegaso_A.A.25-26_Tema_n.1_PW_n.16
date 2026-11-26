from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from schemi.autenticazione import Token
from services import autenticazione as auth_service

router = APIRouter(prefix="/auth", tags=["Autenticazione"])


@router.post("/login", response_model=Token)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Accesso con email (campo username) e password"""
    utente = auth_service.autentica_utente(db, form.username, form.password)
    if utente is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenziali non valide",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=auth_service.crea_token_accesso(utente))