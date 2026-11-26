from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from dipendenze import get_utente_corrente, richiedi_ruoli
from modelli import Utente
from schemi.utente import UtenteRead
from services import utente as utente_service

router = APIRouter(prefix="/utenti", tags=["Utenti"])


@router.get("/me", response_model=UtenteRead)
def profilo_corrente(utente: Utente = Depends(get_utente_corrente)):
    """Dati dell'utente che ha effettuato l'accesso (qualsiasi ruolo)"""
    return utente


@router.get(
    "",
    response_model=list[UtenteRead],
    dependencies=[Depends(richiedi_ruoli("ADMIN"))],
)
def elenco_utenti(db: Session = Depends(get_db)):
    """Elenco di tutti gli utenti (solo ADMIN)"""
    return utente_service.elenco_utenti(db)