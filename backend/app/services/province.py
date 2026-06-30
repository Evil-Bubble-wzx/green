"""Province-related queries."""

from sqlalchemy.orm import Session
from ..models import AdjacencyMatrix


def get_all_provinces(db: Session) -> list:
    """Return all provinces with region and adjacency info."""
    rows = (
        db.query(AdjacencyMatrix)
        .order_by(AdjacencyMatrix.province)
        .all()
    )
    if not rows:
        raise ValueError("No province data found. Run data import first.")
    return rows
