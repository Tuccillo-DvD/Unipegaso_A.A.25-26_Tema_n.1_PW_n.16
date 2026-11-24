from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Utente(Base):
    __tablename__ = "utente"

    id_utente: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(50))
    cognome: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100))
    password_hash: Mapped[str] = mapped_column(String(255))
    ruolo: Mapped[str] = mapped_column(String(20))
    telefono: Mapped[Optional[str]] = mapped_column(String(20))
    data_creazione: Mapped[datetime] = mapped_column(DateTime)
    attivo: Mapped[bool] = mapped_column(Boolean)

    paziente: Mapped[Optional["Paziente"]] = relationship(back_populates="utente")
    medico: Mapped[Optional["Medico"]] = relationship(back_populates="utente")