from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import get_db
from routers import esami, medici, specializzazioni, autenticazione

app = FastAPI(title="Piattaforma Centro Polidiagnostico Pio X")
app.include_router(esami.router)
app.include_router(medici.router)
app.include_router(specializzazioni.router)
app.include_router(autenticazione.router)

@app.get("/salute")
def salute():
    """Controlla che il server sia in esecuzione"""
    return {"stato": "ok"}


@app.get("/salute/db")
def salute_db(db: Session = Depends(get_db)):
    """Controlla che il database sia raggiungibile"""
    db.execute(text("SELECT 1"))
    return {"database": "raggiungibile"}
