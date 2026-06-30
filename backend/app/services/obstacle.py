"""Obstacle degree queries."""

from sqlalchemy.orm import Session
from ..models import ObstacleProvince


def get_obstacle_by_province(db: Session, province: str):
    """Return obstacle diagnosis for one province."""
    row = (
        db.query(ObstacleProvince)
        .filter(ObstacleProvince.province == province)
        .first()
    )
    if not row:
        # Suggest close matches
        all_provs = [
            r[0]
            for r in db.query(ObstacleProvince.province)
            .order_by(ObstacleProvince.province)
            .all()
        ]
        raise ValueError(
            f"Province '{province}' not found in obstacle results. "
            f"Available provinces: {all_provs}"
        )
    return row
