from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schemi.esame import EsameRead
from services import esame as esame_service

router = APIRouter(prefix="/esami", tags=["Esami"])


@router.get("", response_model=list[EsameRead])
def elenco_esami(solo_attivi: bool = True, db: Session = Depends(get_db)):
    """Elenco degli esami attivi)"""
    return esame_service.elenco_esami(db, solo_attivi)


@router.get("/{id_esame}", response_model=EsameRead)
def dettaglio_esame(id_esame: int, db: Session = Depends(get_db)):
    """Dettaglio di un singolo esame"""
    esame = esame_service.get_esame(db, id_esame)
    if esame is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Esame non trovato",
        )
    return esame