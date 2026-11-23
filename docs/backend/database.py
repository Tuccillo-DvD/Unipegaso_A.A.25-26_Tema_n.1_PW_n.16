from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings

# Costruzione dell'URL
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=settings.DB_USER,
    password=settings.DB_PASSWORD.get_secret_value(),
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME,
)

# Gestione delle connessioni al database
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Ogni richiesta userà una propria sessione
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """Classe da cui derivano tutti i modelli."""


def get_db():
    """Crea una sessione e la chiude al termine."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()