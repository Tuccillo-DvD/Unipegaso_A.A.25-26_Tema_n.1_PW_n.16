from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, contains_eager, joinedload, selectinload

from modelli import Medico, Utente


def elenco_medici(db: Session) -> list[Medico]:
    """Medici con account attivo, in ordine alfabetico di cognome e nome"""
    query = (
        select(Medico)
        .join(Medico.utente)
        .where(Utente.attivo.is_(True))
        .options(
            contains_eager(Medico.utente),
            selectinload(Medico.specializzazioni),
            selectinload(Medico.esami),
        )
        .order_by(Utente.cognome, Utente.nome)
    )
    return list(db.scalars(query).all())


def get_medico(db: Session, id_medico: int) -> Optional[Medico]:
    """Un medico dal suo id, oppure None se non esiste o non è attivo"""
    query = (
        select(Medico)
        .where(Medico.id_medico == id_medico)
        .options(
            joinedload(Medico.utente),
            selectinload(Medico.specializzazioni),
            selectinload(Medico.esami),
        )
    )
    medico = db.scalars(query).first()
    if medico is None or not medico.utente.attivo:
        return None
    return medico