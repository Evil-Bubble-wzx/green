"""Overview / dashboard queries."""

from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models import TopsisScore, AdjacencyMatrix


def get_overview(db: Session, year: int) -> dict:
    """Return dashboard overview for a given year."""

    scores = (
        db.query(TopsisScore)
        .filter(TopsisScore.year == year)
        .order_by(TopsisScore.rank)
        .all()
    )

    if not scores:
        available = [
            r[0]
            for r in db.query(TopsisScore.year)
            .distinct()
            .order_by(TopsisScore.year)
            .all()
        ]
        raise ValueError(
            f"No data for year {year}. Available years: {available}"
        )

    # National average
    avg_score = sum(s.composite_score for s in scores if s.composite_score) / len(scores)

    # Top & bottom
    top = scores[0]
    bottom = scores[-1]

    # Top 10
    top10 = scores[:10]

    # Region averages
    region_scores = {}
    region_counts = {}
    for s in scores:
        # Look up region from adjacency_matrix
        region_row = (
            db.query(AdjacencyMatrix.region)
            .filter(AdjacencyMatrix.province == s.province)
            .first()
        )
        region = region_row[0] if region_row else "Unknown"
        if region not in region_scores:
            region_scores[region] = 0.0
            region_counts[region] = 0
        if s.composite_score:
            region_scores[region] += s.composite_score
            region_counts[region] += 1

    region_avgs = [
        {"region": r, "avg_score": round(region_scores[r] / region_counts[r], 6),
         "province_count": region_counts[r]}
        for r in sorted(region_scores.keys())
    ]

    return {
        "year": year,
        "national_avg_score": round(avg_score, 6),
        "highest_province": top.province,
        "highest_score": top.composite_score,
        "lowest_province": bottom.province,
        "lowest_score": bottom.composite_score,
        "top10": top10,
        "region_averages": region_avgs,
    }
