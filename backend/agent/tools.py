"""
Database query tools for the RAG Agent.

Each tool function accepts no DB session — it creates its own engine,
executes the query, and returns a structured dict.
"""

import os
from pathlib import Path
from typing import Optional

from sqlalchemy import create_engine, text
from dotenv import load_dotenv


def _get_engine():
    project_root = Path(__file__).resolve().parent.parent.parent
    dotenv_path = project_root / ".env"
    load_dotenv(dotenv_path)
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL not set")
    return create_engine(db_url)


def _query(sql: str, params: dict = None) -> list:
    """Execute a SELECT query and return rows as dicts."""
    engine = _get_engine()
    try:
        with engine.connect() as conn:
            rows = conn.execute(text(sql), params or {}).fetchall()
            if rows:
                return [dict(r._mapping) for r in rows]
            return []
    finally:
        engine.dispose()


# ---------------------------------------------------------------------------
# Tool Functions
# ---------------------------------------------------------------------------

def get_latest_scores() -> dict:
    """Return TOPSIS scores for the latest available year."""
    rows = _query("""
        SELECT province, year, composite_score, rank
        FROM topsis_scores
        WHERE year = (SELECT MAX(year) FROM topsis_scores)
        ORDER BY rank
    """)
    return {
        "tool": "get_latest_scores",
        "year": rows[0]["year"] if rows else None,
        "count": len(rows),
        "data": rows,
    }


def get_province_score(province: str, year: int = None) -> dict:
    """Return score for one province in a given year."""
    if year is None:
        year = 2024
    rows = _query(
        "SELECT province, year, composite_score, rank FROM topsis_scores "
        "WHERE province = :prov AND year = :year",
        {"prov": province, "year": year},
    )
    if not rows:
        return {"tool": "get_province_score", "error": f"No data for {province} in {year}"}
    return {"tool": "get_province_score", "data": rows[0]}


def get_province_trend(province: str) -> dict:
    """Return score trend 2016-2024 for one province."""
    rows = _query(
        "SELECT province, year, composite_score, rank FROM topsis_scores "
        "WHERE province = :prov ORDER BY year",
        {"prov": province},
    )
    if not rows:
        return {"tool": "get_province_trend", "error": f"No data for {province}"}
    growth = None
    if len(rows) >= 2 and rows[0]["composite_score"] and rows[-1]["composite_score"]:
        first = rows[0]["composite_score"]
        last = rows[-1]["composite_score"]
        growth = round((last - first) / first, 4) if first > 0 else None
    return {
        "tool": "get_province_trend",
        "province": province,
        "growth_rate": growth,
        "data": rows,
    }


def get_top_rankings(year: int = 2024, limit: int = 10) -> dict:
    """Return top N provinces by rank."""
    rows = _query(
        "SELECT province, year, composite_score, rank FROM topsis_scores "
        "WHERE year = :year ORDER BY rank LIMIT :lim",
        {"year": year, "lim": limit},
    )
    return {"tool": "get_top_rankings", "year": year, "count": len(rows), "data": rows}


def get_lpa_result(province: str = None) -> dict:
    """Return LPA type for one province or all provinces."""
    if province:
        rows = _query(
            "SELECT province, lpa_type, type_name, score_2016, score_2024, "
            "stage_increment, mean_2016_2024 "
            "FROM lpa_province_assignment WHERE province = :prov",
            {"prov": province},
        )
    else:
        rows = _query(
            "SELECT province, lpa_type, type_name, score_2016, score_2024, "
            "stage_increment FROM lpa_province_assignment ORDER BY lpa_type, province"
        )
    return {"tool": "get_lpa_result", "province": province, "data": rows}


def get_obstacle_result(province: str) -> dict:
    """Return obstacle diagnosis for one province."""
    rows = _query(
        "SELECT province, region, lpa_type, primary_obstacle_dimension, "
        "primary_obstacle_degree, secondary_obstacle_dimension, "
        "secondary_obstacle_degree, weakness_diagnosis_type "
        "FROM obstacle_province WHERE province = :prov",
        {"prov": province},
    )
    if not rows:
        return {"tool": "get_obstacle_result", "error": f"No data for {province}"}
    return {"tool": "get_obstacle_result", "data": rows[0]}


def get_shap_top_features(province: str, year: int = 2024) -> dict:
    """Return top SHAP features for one province."""
    rows = _query(
        "SELECT indicator_name, indicator_short_name, dimension, shap_value, abs_shap_value "
        "FROM shap_local_top8 WHERE province = :prov "
        "ORDER BY abs_shap_value DESC LIMIT 8",
        {"prov": province},
    )
    if not rows:
        return {"tool": "get_shap_top_features", "error": f"No SHAP data for {province}"}
    positive = [r for r in rows if (r["shap_value"] or 0) > 0]
    negative = [r for r in rows if (r["shap_value"] or 0) < 0]
    pos_sum = sum(r["shap_value"] for r in positive) if positive else 0
    neg_sum = sum(abs(r["shap_value"]) for r in negative) if negative else 0
    return {
        "tool": "get_shap_top_features",
        "province": province,
        "positive_count": len(positive),
        "negative_count": len(negative),
        "positive_sum": round(pos_sum, 6),
        "negative_sum": round(neg_sum, 6),
        "data": rows,
    }


def get_layout_recommendation(province: str) -> dict:
    """Return layout recommendation for one province."""
    rows = _query(
        "SELECT province, region, recommended_layout_type, layout_orientation, "
        "functional_positioning, optimization_strategy, risk_warning, "
        "suitability_index, demand_network_advantage_index, "
        "energy_low_carbon_advantage_index, constraint_pressure_index, "
        "composite_score, rank "
        "FROM layout_province_decision WHERE province = :prov",
        {"prov": province},
    )
    if not rows:
        return {"tool": "get_layout_recommendation", "error": f"No data for {province}"}
    return {"tool": "get_layout_recommendation", "data": rows[0]}


def compare_provinces(provinces: list[str]) -> dict:
    """Compare multiple provinces on key metrics."""
    result = []
    for prov in provinces:
        score = _query(
            "SELECT composite_score, rank FROM topsis_scores "
            "WHERE province = :prov AND year = 2024",
            {"prov": prov},
        )
        lpa = _query(
            "SELECT type_name FROM lpa_province_assignment WHERE province = :prov",
            {"prov": prov},
        )
        layout = _query(
            "SELECT recommended_layout_type, suitability_index "
            "FROM layout_province_decision WHERE province = :prov",
            {"prov": prov},
        )
        obstacle = _query(
            "SELECT primary_obstacle_dimension, primary_obstacle_degree "
            "FROM obstacle_province WHERE province = :prov",
            {"prov": prov},
        )
        result.append({
            "province": prov,
            "score": score[0] if score else None,
            "lpa_type": lpa[0]["type_name"] if lpa else None,
            "layout_type": layout[0]["recommended_layout_type"] if layout else None,
            "suitability_index": layout[0]["suitability_index"] if layout else None,
            "primary_obstacle": obstacle[0]["primary_obstacle_dimension"] if obstacle else None,
            "primary_obstacle_degree": obstacle[0]["primary_obstacle_degree"] if obstacle else None,
        })
    return {"tool": "compare_provinces", "count": len(result), "data": result}


def get_future_potential_ranking(years: int = 10) -> dict:
    """
    Compute future potential scores for all 31 provinces.

    Formula:
      future_potential_score =
        0.30 * current_score
        + 0.25 * historical_growth
        + 0.15 * markov_upgrade_probability
        + 0.15 * green_energy_low_carbon_advantage
        + 0.10 * shap_positive_driver_strength
        + 0.05 * obstacle_reverse_score
    """
    # 1. Current scores (2024)
    current = {
        r["province"]: r["composite_score"]
        for r in _query("SELECT province, composite_score FROM topsis_scores WHERE year = 2024")
    }

    # 2. Historical growth (2016 -> 2024)
    scores_2016 = {
        r["province"]: r["composite_score"]
        for r in _query("SELECT province, composite_score FROM topsis_scores WHERE year = 2016")
    }
    growth = {}
    for prov, s2024 in current.items():
        s2016 = scores_2016.get(prov, s2024)
        if s2016 and s2016 > 0:
            growth[prov] = (s2024 - s2016) / s2016
        else:
            growth[prov] = 0.0

    # 3. Markov upgrade probability
    markov = {}
    spatial_rows = _query(
        "SELECT province, current_state, next_state, neighborhood_state_name "
        "FROM spatial_lag_state WHERE year = 2023"
    )
    state_order = {"低水平": 0, "中低水平": 1, "中高水平": 2, "高水平": 3}
    for r in spatial_rows:
        cur = state_order.get(r["current_state"], -1)
        nxt = state_order.get(r["next_state"], -1)
        if cur >= 0 and nxt >= 0:
            markov[r["province"]] = 1.0 if nxt > cur else (0.5 if nxt == cur else 0.0)
        else:
            markov[r["province"]] = 0.5

    # 4. Green energy low-carbon advantage
    energy = {}
    layout_rows = _query(
        "SELECT province, energy_low_carbon_advantage_index FROM layout_province_decision"
    )
    for r in layout_rows:
        energy[r["province"]] = r["energy_low_carbon_advantage_index"] or 0.0

    # 5. SHAP positive driver strength
    shap_strength = {}
    for prov in current:
        shap_rows = _query(
            "SELECT shap_value FROM shap_local_top8 WHERE province = :prov",
            {"prov": prov},
        )
        if shap_rows:
            pos = sum(r["shap_value"] for r in shap_rows if (r["shap_value"] or 0) > 0)
            neg = sum(abs(r["shap_value"]) for r in shap_rows if (r["shap_value"] or 0) < 0)
            total = pos + neg
            shap_strength[prov] = pos / total if total > 0 else 0.5
        else:
            shap_strength[prov] = 0.5

    # 6. Obstacle reverse score
    obstacle_rev = {}
    obs_rows = _query("SELECT province, primary_obstacle_degree FROM obstacle_province")
    for r in obs_rows:
        deg = r["primary_obstacle_degree"] or 50.0
        obstacle_rev[r["province"]] = (100.0 - deg) / 100.0

    # ---- Compute final score ----
    results = []
    for prov in current:
        cs = current.get(prov, 0) or 0
        hg = growth.get(prov, 0) or 0
        mu = markov.get(prov, 0.5) or 0.5
        ga = energy.get(prov, 0) or 0
        ss = shap_strength.get(prov, 0.5) or 0.5
        ob = obstacle_rev.get(prov, 0.5) or 0.5

        # Normalize growth to [0,1] range
        all_growths = [v for v in growth.values() if v is not None]
        if all_growths:
            g_min, g_max = min(all_growths), max(all_growths)
            hg_norm = (hg - g_min) / (g_max - g_min) if g_max > g_min else 0.5
        else:
            hg_norm = 0.5

        score = (
            0.30 * (cs or 0)
            + 0.25 * hg_norm
            + 0.15 * mu
            + 0.15 * (ga or 0)
            + 0.10 * ss
            + 0.05 * ob
        )
        results.append({
            "province": prov,
            "future_potential_score": round(score, 6),
            "current_score": round(cs, 6) if cs else None,
            "historical_growth": round(hg, 4) if hg else None,
            "markov_upgrade_prob": round(mu, 4) if mu else None,
            "energy_advantage": round(ga, 4) if ga else None,
            "shap_positive_strength": round(ss, 4) if ss else None,
            "obstacle_reverse": round(ob, 4) if ob else None,
        })

    results.sort(key=lambda x: x["future_potential_score"], reverse=True)

    return {
        "tool": "get_future_potential_ranking",
        "years_forward": years,
        "formula": (
            "0.30*current_score + 0.25*historical_growth "
            "+ 0.15*markov_upgrade_prob + 0.15*energy_advantage "
            "+ 0.10*shap_positive_strength + 0.05*obstacle_reverse"
        ),
        "data_granularity": "省域（省级行政区），不支持城市级预测",
        "count": len(results),
        "top5": results[:5],
        "full_data": results,
    }
