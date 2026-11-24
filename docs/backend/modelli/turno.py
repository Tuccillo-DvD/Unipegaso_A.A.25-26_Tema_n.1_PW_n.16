from datetime import date, time

from sqlalchemy import Date, ForeignKey, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Turno(Base):
    __tablename__ = "turno"

    id_turno: Mapped[int] = mapped_column(primary_key=True)
    id_medico: Mapped[int] = mapped_column(ForeignKey("medico.id_medico"))
    data_turno: Mapped[date] = mapped_column(Date)
    ora_inizio: Mapped[time] = mapped_column(Time)
    ora_fine: Mapped[time] = mapped_column(Time)

    medico: Mapped["Medico"] = relationship()