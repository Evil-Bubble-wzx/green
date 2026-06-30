"""Score-related queries."""

from sqlalchemy.orm import Session
from ..models import TopsisScore


def get_scores_by_year(db: Session, year: int) -> list:
    """Return TOPSIS composite scores for a given year, ordered by rank."""
    rows = (
        db.query(TopsisScore)
        .filter(TopsisScore.year == year)
        .order_by(TopsisScore.rank)
        .all()
    )
    if not rows:
        available = (
            db.query(TopsisScore.year)
            .distinct()
            .order_by(TopsisScore.year)
            .all()
        )
        years = [r[0] for r in available]
        raise ValueError(
            f"No data for year {year}. Available years: {years}"
        )
    return rows
