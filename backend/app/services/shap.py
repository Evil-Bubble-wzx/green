"""SHAP interpretation queries."""

from sqlalchemy.orm import Session
from ..models import ShapLocalTop8, ShapImportance


def get_shap_local(
    db: Session, province: str, year: int = 2024
) -> list:
    """Return local SHAP Top-8 explanations for a province, sorted by abs SHAP desc."""
    rows = (
        db.query(ShapLocalTop8)
        .filter(ShapLocalTop8.province == province)
        .order_by(ShapLocalTop8.abs_shap_value.desc())
        .all()
    )
    if not rows:
        all_provs = [
            r[0]
            for r in db.query(ShapLocalTop8.province)
            .distinct()
            .order_by(ShapLocalTop8.province)
            .all()
        ]
        raise ValueError(
            f"No SHAP data for province '{province}'. "
            f"Available provinces: {all_provs}"
        )
    return rows


def get_shap_global(db: Session) -> list:
    """Return global SHAP feature importance, ordered by rank."""
    rows = (
        db.query(ShapImportance)
        .order_by(ShapImportance.importance_rank)
        .all()
    )
    if not rows:
        raise ValueError("No SHAP importance data found.")
    return rows
