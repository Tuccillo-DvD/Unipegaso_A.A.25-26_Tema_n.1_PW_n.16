from sqlalchemy import select
from sqlalchemy.orm import Session

from modelli import Specializzazione


def elenco_specializzazioni(db: Session) -> list[Specializzazione]:
    """Restituisce le specializzazioni in ordine alfabetico"""
    query = select(Specializzazione).order_by(Specializzazione.nome)
    return list(db.scalars(query).all())