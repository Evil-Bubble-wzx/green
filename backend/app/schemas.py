"""
Pydantic schemas for Green Compute System API responses.
"""

from typing import Optional, List
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Province
# ---------------------------------------------------------------------------

class ProvinceBasicOut(BaseModel):
    province: str
    region: Optional[str] = None
    is_hub: Optional[bool] = None
    adjacent_provinces: Optional[str] = None
    adjacent_count: Optional[int] = None

    model_config = {"from_attributes": True}


class ProvinceListOut(BaseModel):
    count: int
    provinces: List[ProvinceBasicOut]


# ---------------------------------------------------------------------------
# Scores
# ---------------------------------------------------------------------------

class ScoreItem(BaseModel):
    province: str
    year: int
    composite_score: Optional[float] = None
    rank: Optional[int] = None

    model_config = {"from_attributes": True}


class ScoreListOut(BaseModel):
    year: int
    count: int
    scores: List[ScoreItem]


# ---------------------------------------------------------------------------
# Province Profile (综合画像)
# ---------------------------------------------------------------------------

class ProvinceProfileOut(BaseModel):
    province: str
    year: int
    region: Optional[str] = None
    composite_score: Optional[float] = None
    rank: Optional[int] = None
    lpa_type: Optional[str] = None
    type_name: Optional[str] = None
    primary_obstacle_dimension: Optional[str] = None
    primary_obstacle_degree: Optional[float] = None
    secondary_obstacle_dimension: Optional[str] = None
    secondary_obstacle_degree: Optional[float] = None
    weakness_diagnosis_type: Optional[str] = None
    recommended_layout_type: Optional[str] = None
    layout_orientation: Optional[str] = None
    functional_positioning: Optional[str] = None
    optimization_strategy: Optional[str] = None
    risk_warning: Optional[str] = None


# ---------------------------------------------------------------------------
# Obstacles
# ---------------------------------------------------------------------------

class ObstacleProvinceOut(BaseModel):
    province: str
    region: Optional[str] = None
    lpa_type: Optional[str] = None
    primary_obstacle_dimension: Optional[str] = None
    primary_obstacle_degree: Optional[float] = None
    secondary_obstacle_dimension: Optional[str] = None
    secondary_obstacle_degree: Optional[float] = None
    weakness_diagnosis_type: Optional[str] = None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# LPA
# ---------------------------------------------------------------------------

class LpaProvinceItem(BaseModel):
    province: str
    lpa_type: Optional[str] = None
    type_name: Optional[str] = None
    score_2016: Optional[float] = None
    score_2024: Optional[float] = None
    stage_increment: Optional[float] = None
    mean_2016_2024: Optional[float] = None
    max_posterior_probability: Optional[float] = None

    model_config = {"from_attributes": True}


class LpaTypeItem(BaseModel):
    lpa_type: Optional[str] = None
    type_name: Optional[str] = None
    province_count: Optional[int] = None
    mean_2016: Optional[float] = None
    mean_2024: Optional[float] = None
    stage_increment: Optional[float] = None
    provinces: Optional[str] = None

    model_config = {"from_attributes": True}


class LpaListOut(BaseModel):
    province_assignments: List[LpaProvinceItem]
    type_summary: List[LpaTypeItem]


# ---------------------------------------------------------------------------
# SHAP
# ---------------------------------------------------------------------------

class ShapLocalItem(BaseModel):
    indicator_name: Optional[str] = None
    indicator_short_name: Optional[str] = None
    dimension: Optional[str] = None
    shap_value: Optional[float] = None
    abs_shap_value: Optional[float] = None

    model_config = {"from_attributes": True}


class ShapListOut(BaseModel):
    province: str
    year: int
    count: int
    explanations: List[ShapLocalItem]


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

class LayoutDecisionOut(BaseModel):
    province: str
    region: Optional[str] = None
    rank: Optional[int] = None
    composite_score: Optional[float] = None
    stage_increment: Optional[float] = None
    type_name: Optional[str] = None
    lisa_type: Optional[str] = None
    primary_obstacle_dimension: Optional[str] = None
    secondary_obstacle_dimension: Optional[str] = None
    weakness_diagnosis_type: Optional[str] = None
    demand_network_advantage_index: Optional[float] = None
    energy_low_carbon_advantage_index: Optional[float] = None
    constraint_pressure_index: Optional[float] = None
    suitability_index: Optional[float] = None
    recommended_layout_type: Optional[str] = None
    layout_orientation: Optional[str] = None
    functional_positioning: Optional[str] = None
    optimization_strategy: Optional[str] = None
    risk_warning: Optional[str] = None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Overview
# ---------------------------------------------------------------------------

class OverviewOut(BaseModel):
    year: int
    national_avg_score: Optional[float] = None
    highest_province: Optional[str] = None
    highest_score: Optional[float] = None
    lowest_province: Optional[str] = None
    lowest_score: Optional[float] = None
    top10: List[ScoreItem]
    region_averages: List[dict]


# ---------------------------------------------------------------------------
# Indicators
# ---------------------------------------------------------------------------

class IndicatorItem(BaseModel):
    indicator_code: Optional[str] = None
    field_name: Optional[str] = None
    indicator_name: Optional[str] = None
    dimension: Optional[str] = None
    direction: Optional[str] = None
    unit: Optional[str] = None
    meaning: Optional[str] = None

    model_config = {"from_attributes": True}


class IndicatorListOut(BaseModel):
    count: int
    indicators: List[IndicatorItem]


# ---------------------------------------------------------------------------
# Dagum
# ---------------------------------------------------------------------------

class DagumDecompItem(BaseModel):
    year: int
    total_gini: Optional[float] = None
    intra_region_difference: Optional[float] = None
    inter_region_net_difference: Optional[float] = None
    hypervariable_density: Optional[float] = None
    intra_region_contribution_rate: Optional[float] = None
    inter_region_contribution_rate: Optional[float] = None
    hypervariable_density_contribution_rate: Optional[float] = None

    model_config = {"from_attributes": True}


class DagumIntraItem(BaseModel):
    year: int
    region: str
    sample_size: Optional[int] = None
    mean_value: Optional[float] = None
    intra_region_gini: Optional[float] = None

    model_config = {"from_attributes": True}


class DagumInterItem(BaseModel):
    year: int
    region_pair: str
    high_mean_region: Optional[str] = None
    low_mean_region: Optional[str] = None
    inter_region_gini: Optional[float] = None
    relative_influence_d: Optional[float] = None

    model_config = {"from_attributes": True}


class DagumOut(BaseModel):
    decomposition: List[DagumDecompItem]
    intra_region: List[DagumIntraItem]
    inter_region: List[DagumInterItem]


# ---------------------------------------------------------------------------
# Moran
# ---------------------------------------------------------------------------

class MoranItem(BaseModel):
    year: int
    moran_i: Optional[float] = None
    two_sided_p_value: Optional[float] = None
    positive_p_value: Optional[float] = None

    model_config = {"from_attributes": True}


class LisaItem(BaseModel):
    province: str
    year: int
    composite_score: Optional[float] = None
    standardized_score_z: Optional[float] = None
    spatial_lag_wz: Optional[float] = None
    local_moran_i: Optional[float] = None
    p_value: Optional[float] = None
    lisa_type: Optional[str] = None

    model_config = {"from_attributes": True}


class MoranOut(BaseModel):
    moran_series: List[MoranItem]
    lisa_2024: List[LisaItem]


# ---------------------------------------------------------------------------
# Markov
# ---------------------------------------------------------------------------

class MarkovProbItem(BaseModel):
    from_state: Optional[str] = None
    to_low_level_probability: Optional[float] = None
    to_mid_low_level_probability: Optional[float] = None
    to_mid_high_level_probability: Optional[float] = None
    to_high_level_probability: Optional[float] = None

    model_config = {"from_attributes": True}


class SpatialMarkovItem(BaseModel):
    neighborhood_state: Optional[str] = None
    from_state: Optional[str] = None
    to_state: Optional[str] = None
    frequency: Optional[int] = None
    probability: Optional[float] = None

    model_config = {"from_attributes": True}


class StateThresholdItem(BaseModel):
    state: Optional[str] = None
    classification_rule: Optional[str] = None
    threshold_note: Optional[str] = None

    model_config = {"from_attributes": True}


class MarkovOut(BaseModel):
    probability: List[MarkovProbItem]
    spatial: List[SpatialMarkovItem]
    thresholds: List[StateThresholdItem]
