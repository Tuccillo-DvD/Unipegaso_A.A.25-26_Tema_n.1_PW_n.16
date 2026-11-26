from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict

# Gli stessi valori ammessi dal vincolo CHECK del database
Ruolo = Literal["PAZIENTE", "MEDICO", "SEGRETERIA", "ADMIN"]


class UtenteRead(BaseModel):
    id_utente: int
    nome: str
    cognome: str
    email: str
    ruolo: Ruolo
    telefono: Optional[str] = None
    data_creazione: datetime
    attivo: bool

    model_config = ConfigDict(from_attributes=True)