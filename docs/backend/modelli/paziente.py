from datetime import date
from typing import Optional

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Paziente(Base):
    __tablename__ = "paziente"

    id_paziente: Mapped[int] = mapped_column(
        ForeignKey("utente.id_utente"), primary_key=True
    )
    codice_fiscale: Mapped[str] = mapped_column(String(16))
    data_nascita: Mapped[date] = mapped_column(Date)
    indirizzo: Mapped[Optional[str]] = mapped_column(String(50))

    utente: Mapped["Utente"] = relationship(back_populates="paziente")