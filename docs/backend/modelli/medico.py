from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from modelli.associazioni import medico_esame, medico_specializzazione


class Medico(Base):
    __tablename__ = "medico"

    id_medico: Mapped[int] = mapped_column(
        ForeignKey("utente.id_utente"), primary_key=True
    )
    numero_albo: Mapped[str] = mapped_column(String(30))

    utente: Mapped["Utente"] = relationship(back_populates="medico")
    esami: Mapped[list["Esame"]] = relationship(
        secondary=medico_esame, back_populates="medici"
    )
    specializzazioni: Mapped[list["Specializzazione"]] = relationship(
        secondary=medico_specializzazione, back_populates="medici"
    )
    @property
    def nome(self) -> str:
        return self.utente.nome

    @property
    def cognome(self) -> str:
        return self.utente.cognome