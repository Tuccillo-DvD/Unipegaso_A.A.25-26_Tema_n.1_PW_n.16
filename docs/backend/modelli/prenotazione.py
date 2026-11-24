from datetime import date, datetime, time
from typing import Optional

from sqlalchemy import Date, DateTime, ForeignKey, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Prenotazione(Base):
    __tablename__ = "prenotazione"

    id_prenotazione: Mapped[int] = mapped_column(primary_key=True)
    id_paziente: Mapped[int] = mapped_column(ForeignKey("paziente.id_paziente"))
    id_medico: Mapped[int] = mapped_column(ForeignKey("medico.id_medico"))
    id_esame: Mapped[int] = mapped_column(ForeignKey("esame.id_esame"))
    id_creatore: Mapped[int] = mapped_column(ForeignKey("utente.id_utente"))
    data_appuntamento: Mapped[date] = mapped_column(Date)
    ora_inizio: Mapped[time] = mapped_column(Time)
    ora_fine: Mapped[time] = mapped_column(Time)
    stato: Mapped[str] = mapped_column(String(20))
    data_creazione: Mapped[datetime] = mapped_column(DateTime)
    data_annullamento: Mapped[Optional[datetime]] = mapped_column(DateTime)

    paziente: Mapped["Paziente"] = relationship()
    medico: Mapped["Medico"] = relationship()
    esame: Mapped["Esame"] = relationship()
    creatore: Mapped["Utente"] = relationship()
    referto: Mapped[Optional["Referto"]] = relationship(back_populates="prenotazione")