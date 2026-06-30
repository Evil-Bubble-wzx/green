"""Layout decision queries."""

from sqlalchemy.orm import Session
from ..models import LayoutProvinceDecision


def get_layout_by_province(db: Session, province: str):
    """Return layout decision for one province."""
    row = (
        db.query(LayoutProvinceDecision)
        .filter(LayoutProvinceDecision.province == province)
        .first()
    )
    if not row:
        all_provs = [
            r[0]
            for r in db.query(LayoutProvinceDecision.province)
            .order_by(LayoutProvinceDecision.province)
            .all()
        ]
        raise ValueError(
            f"Province '{province}' not found in layout decisions. "
            f"Available provinces: {all_provs}"
        )
    return row
