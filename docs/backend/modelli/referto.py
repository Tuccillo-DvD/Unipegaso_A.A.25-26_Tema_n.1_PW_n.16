from datetime import datetime

from sqlalchemy import DateTime, ForeignKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Referto(Base):
    __tablename__ = "referto"
    __table_args__ = (
        ForeignKeyConstraint(
            ["id_prenotazione", "id_medico_caricante"],
            ["prenotazione.id_prenotazione", "prenotazione.id_medico"],
        ),
    )

    id_referto: Mapped[int] = mapped_column(primary_key=True)
    id_prenotazione: Mapped[int]
    id_medico_caricante: Mapped[int]
    nome_file: Mapped[str] = mapped_column(String(250))
    percorso_file: Mapped[str] = mapped_column(String(500))
    data_caricamento: Mapped[datetime] = mapped_column(DateTime)

    prenotazione: Mapped["Prenotazione"] = relationship(back_populates="referto")