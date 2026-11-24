from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from modelli.associazioni import medico_esame


class Esame(Base):
    __tablename__ = "esame"

    id_esame: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    descrizione: Mapped[Optional[str]] = mapped_column(Text)
    durata_minuti: Mapped[int] = mapped_column(Integer)
    prezzo: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    attivo: Mapped[bool] = mapped_column(Boolean)

    medici: Mapped[list["Medico"]] = relationship(
        secondary=medico_esame, back_populates="esami"
    )