from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from modelli import Esame


def elenco_esami(db: Session, solo_attivi: bool = True) -> list[Esame]:
    """Restituisce gli esami in ordine alfabetico."""
    query = select(Esame).order_by(Esame.nome)
    if solo_attivi:
        query = query.where(Esame.attivo.is_(True))
    return list(db.scalars(query).all())


def get_esame(db: Session, id_esame: int) -> Optional[Esame]:
    """Restituisce un esame dal suo id, oppure None se non esiste."""
    return db.get(Esame, id_esame)