from sqlalchemy import Column, ForeignKey, Table

from database import Base

medico_esame = Table(
    "medico_esame",
    Base.metadata,
    Column("id_medico", ForeignKey("medico.id_medico"), primary_key=True),
    Column("id_esame", ForeignKey("esame.id_esame"), primary_key=True),
)

medico_specializzazione = Table(
    "medico_specializzazione",
    Base.metadata,
    Column("id_medico", ForeignKey("medico.id_medico"), primary_key=True),
    Column(
        "id_specializzazione",
        ForeignKey("specializzazione.id_specializzazione"),
        primary_key=True,
    ),
)