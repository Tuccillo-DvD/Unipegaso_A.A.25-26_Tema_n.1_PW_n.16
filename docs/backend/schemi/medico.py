from pydantic import BaseModel, ConfigDict

from schemi.esame import EsameRead
from schemi.specializzazione import SpecializzazioneRead


class MedicoRead(BaseModel):
    id_medico: int
    nome: str
    cognome: str
    numero_albo: str
    specializzazioni: list[SpecializzazioneRead]
    esami: list[EsameRead]

    model_config = ConfigDict(from_attributes=True)