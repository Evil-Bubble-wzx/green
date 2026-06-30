"""Markov chain queries."""
from sqlalchemy.orm import Session
from ..models import MarkovProbability, SpatialMarkov, StateThreshold, SpatialLagState

def get_markov_probability(db: Session) -> list:
    rows = db.query(MarkovProbability).order_by(MarkovProbability.from_state).all()
    if not rows: raise ValueError("No Markov data.")
    return rows

def get_spatial_markov(db: Session) -> list:
    rows = db.query(SpatialMarkov).order_by(SpatialMarkov.neighborhood_state, SpatialMarkov.from_state, SpatialMarkov.to_state).all()
    if not rows: raise ValueError("No spatial Markov data.")
    return rows

def get_state_thresholds(db: Session) -> list:
    rows = db.query(StateThreshold).all()
    if not rows: raise ValueError("No state threshold data.")
    return rows

def get_spatial_lag_states(db: Session, year: int = None) -> list:
    q = db.query(SpatialLagState)
    if year:
        q = q.filter(SpatialLagState.year == year)
    rows = q.order_by(SpatialLagState.province, SpatialLagState.year).all()
    if not rows: raise ValueError("No spatial lag data.")
    return rows
