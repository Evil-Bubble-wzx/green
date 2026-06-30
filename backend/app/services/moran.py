"""Moran's I and LISA queries."""
from sqlalchemy.orm import Session
from ..models import MoranResult, LisaResult

def get_moran(db: Session) -> list:
    rows = db.query(MoranResult).order_by(MoranResult.year).all()
    if not rows: raise ValueError("No Moran data.")
    return rows

def get_lisa(db: Session) -> list:
    rows = db.query(LisaResult).order_by(LisaResult.province).all()
    if not rows: raise ValueError("No LISA data.")
    return rows
