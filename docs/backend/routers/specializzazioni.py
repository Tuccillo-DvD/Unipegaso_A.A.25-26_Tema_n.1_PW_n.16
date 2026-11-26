from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemi.specializzazione import SpecializzazioneRead
from services import specializzazione as specializzazione_service

router = APIRouter(prefix="/specializzazioni", tags=["Specializzazioni"])


@router.get("", response_model=list[SpecializzazioneRead])
def elenco_specializzazioni(db: Session = Depends(get_db)):
    """Elenco delle specializzazioni mediche"""
    return specializzazione_service.elenco_specializzazioni(db)