"""LPA (Latent Profile Analysis) queries."""

from sqlalchemy.orm import Session
from ..models import LpaProvinceAssignment, LpaTypeSummary


def get_lpa_results(db: Session) -> dict:
    """Return all province LPA assignments and type summaries."""
    provinces = (
        db.query(LpaProvinceAssignment)
        .order_by(LpaProvinceAssignment.lpa_type, LpaProvinceAssignment.province)
        .all()
    )
    types = (
        db.query(LpaTypeSummary)
        .order_by(LpaTypeSummary.lpa_type)
        .all()
    )

    if not provinces:
        raise ValueError("No LPA data found. Run data import first.")

    return {
        "province_assignments": provinces,
        "type_summary": types,
    }
