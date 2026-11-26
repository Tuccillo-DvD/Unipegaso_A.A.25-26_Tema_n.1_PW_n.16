from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schemi.medico import MedicoRead
from services import medico as medico_service

router = APIRouter(prefix="/medici", tags=["Medici"])


@router.get("", response_model=list[MedicoRead])
def elenco_medici(db: Session = Depends(get_db)):
    """Elenco dei medici attivi con specializzazioni ed esami"""
    return medico_service.elenco_medici(db)


@router.get("/{id_medico}", response_model=MedicoRead)
def dettaglio_medico(id_medico: int, db: Session = Depends(get_db)):
    """Dettaglio di un singolo medico"""
    medico = medico_service.get_medico(db, id_medico)
    if medico is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medico non trovato",
        )
    return medico