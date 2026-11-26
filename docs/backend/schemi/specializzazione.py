from typing import Optional

from pydantic import BaseModel, ConfigDict


class SpecializzazioneRead(BaseModel):
    id_specializzazione: int
    nome: str
    descrizione: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)