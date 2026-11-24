from typing import Optional

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from modelli.associazioni import medico_specializzazione


class Specializzazione(Base):
    __tablename__ = "specializzazione"

    id_specializzazione: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    descrizione: Mapped[Optional[str]] = mapped_column(Text)

    medici: Mapped[list["Medico"]] = relationship(
        secondary=medico_specializzazione, back_populates="specializzazioni"
    )