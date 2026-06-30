"""Indicator system queries."""
from sqlalchemy.orm import Session
from ..models import IndicatorSystem

def get_indicators(db: Session) -> list:
    rows = db.query(IndicatorSystem).order_by(IndicatorSystem.indicator_code).all()
    if not rows:
        raise ValueError("No indicator data found.")
    return rows
