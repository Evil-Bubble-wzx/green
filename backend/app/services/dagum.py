"""Dagum decomposition queries."""
from sqlalchemy.orm import Session
from ..models import DagumDecomposition, DagumIntraRegion, DagumInterRegion

def get_dagum_decomposition(db: Session) -> list:
    rows = db.query(DagumDecomposition).order_by(DagumDecomposition.year).all()
    if not rows: raise ValueError("No Dagum data.")
    return rows

def get_dagum_intra_region(db: Session) -> list:
    rows = db.query(DagumIntraRegion).order_by(DagumIntraRegion.year, DagumIntraRegion.region).all()
    if not rows: raise ValueError("No Dagum intra-region data.")
    return rows

def get_dagum_inter_region(db: Session) -> list:
    rows = db.query(DagumInterRegion).order_by(DagumInterRegion.year, DagumInterRegion.region_pair).all()
    if not rows: raise ValueError("No Dagum inter-region data.")
    return rows
