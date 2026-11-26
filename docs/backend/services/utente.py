from sqlalchemy import select
from sqlalchemy.orm import Session

from modelli import Utente


def elenco_utenti(db: Session) -> list[Utente]:
    """Restituisce tutti gli utenti in ordine di cognome e nome"""
    query = select(Utente).order_by(Utente.cognome, Utente.nome)
    return list(db.scalars(query).all())