from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class EsameBase(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    descrizione: Optional[str] = None
    durata_minuti: int = Field(gt=0)
    prezzo: Decimal = Field(ge=0, max_digits=5, decimal_places=2)
    attivo: bool = True


class EsameCreate(EsameBase):
    """Dati richiesti per creare un esame."""


class EsameUpdate(BaseModel):
    """Modifica parziale, tutti i campi sono facoltativi."""

    nome: Optional[str] = Field(default=None, min_length=1, max_length=100)
    descrizione: Optional[str] = None
    durata_minuti: Optional[int] = Field(default=None, gt=0)
    prezzo: Optional[Decimal] = Field(
        default=None, ge=0, max_digits=5, decimal_places=2
    )
    attivo: Optional[bool] = None


class EsameRead(EsameBase):
    id_esame: int

    model_config = ConfigDict(from_attributes=True)