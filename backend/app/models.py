"""
SQLAlchemy ORM models for Green Compute System.
"""

from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Text, DateTime,
)
from sqlalchemy.sql import func
from .database import Base


# ---------------------------------------------------------------------------
# Lookup / reference tables
# ---------------------------------------------------------------------------

class ProvinceBasic(Base):
    __tablename__ = "province_basic"
    id = Column(Integer, primary_key=True, index=True)
    province = Column(String(50), unique=True, nullable=False)
    region = Column(String(20))
    is_hub = Column(Boolean, default=False)
    adjacent_provinces = Column(Text)
    adjacent_count = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())


class AdjacencyMatrix(Base):
    __tablename__ = "adjacency_matrix"
    id = Column(Integer, primary_key=True, index=True)
    province = Column(String(50), unique=True, nullable=False)
    adjacent_provinces = Column(Text)
    adjacent_count = Column(Integer)
    region = Column(String(20))
    created_at = Column(DateTime, server_default=func.now())


class IndicatorSystem(Base):
    __tablename__ = "indicator_system"
    id = Column(Integer, primary_key=True, index=True)
    indicator_code = Column(String(20))
    indicator_name = Column(String(100), nullable=False)
    field_name = Column(String(100))
    dimension = Column(String(50), nullable=False)
    direction = Column(String(10))
    unit = Column(String(50))
    meaning = Column(Text)
    is_core_indicator = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())


# ---------------------------------------------------------------------------
# Core data tables
# ---------------------------------------------------------------------------

class TopsisScore(Base):
    __tablename__ = "topsis_scores"
    id = Column(Integer, primary_key=True, index=True)
    province = Column(String(50), nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    composite_score = Column(Float)
    rank = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())


# ---------------------------------------------------------------------------
# LPA results
# ---------------------------------------------------------------------------

class LpaProvinceAssignment(Base):
    __tablename__ = "lpa_province_assignment"
    id = Column(Integer, primary_key=True, index=True)
    province = Column(String(50), unique=True, nullable=False)
    lpa_type = Column(String(20))
    type_name = Column(String(50))
    score_2016 = Column(Float)
    score_2024 = Column(Float)
    stage_increment = Column(Float)
    mean_2016_2024 = Column(Float)
    max_posterior_probability = Column(Float)
    created_at = Column(DateTime, server_default=func.now())


class LpaTypeSummary(Base):
    __tablename__ = "lpa_type_summary"
    id = Column(Integer, primary_key=True, index=True)
    lpa_type = Column(String(20))
    type_name = Column(String(50))
    province_count = Column(Integer)
    mean_2016 = Column(Float)
    mean_2024 = Column(Float)
    stage_increment = Column(Float)
    mean_2016_2024 = Column(Float)
    province = Column(Text)
    created_at = Column(DateTime, server_default=func.now())


# ---------------------------------------------------------------------------
# Obstacle degree model
# ---------------------------------------------------------------------------

class ObstacleProvince(Base):
    __tablename__ = "obstacle_province"
    id = Column(Integer, primary_key=True, index=True)
    province = Column(String(50), unique=True, nullable=False, index=True)
    region = Column(String(20))
    lpa_type = Column(String(20))
    primary_obstacle_dimension = Column(String(50))
    primary_obstacle_degree = Column(Float)
    secondary_obstacle_dimension = Column(String(50))
    secondary_obstacle_degree = Column(Float)
    weakness_diagnosis_type = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())


class ObstacleNational(Base):
    __tablename__ = "obstacle_national"
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False)
    dimension = Column(String(50), nullable=False)
    dimension_obstacle_degree = Column(Float)
    created_at = Column(DateTime, server_default=func.now())


# ---------------------------------------------------------------------------
# SHAP interpretation
# ---------------------------------------------------------------------------

class ShapLocalTop8(Base):
    __tablename__ = "shap_local_top8"
    id = Column(Integer, primary_key=True, index=True)
    province = Column(String(50), nullable=False, index=True)
    indicator_name = Column(String(100))
    indicator_short_name = Column(String(50))
    dimension = Column(String(50))
    shap_value = Column(Float)
    abs_shap_value = Column(Float)
    created_at = Column(DateTime, server_default=func.now())


class ShapImportance(Base):
    __tablename__ = "shap_importance"
    id = Column(Integer, primary_key=True, index=True)
    indicator_name = Column(String(100))
    indicator_short_name = Column(String(50))
    dimension = Column(String(50))
    dimension_short_name = Column(String(50))
    combined_weight = Column(Float)
    mean_abs_shap_value = Column(Float)
    mean_shap_value = Column(Float)
    importance_rank = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())


# ---------------------------------------------------------------------------
# Layout decision
# ---------------------------------------------------------------------------

class LayoutProvinceDecision(Base):
    __tablename__ = "layout_province_decision"
    id = Column(Integer, primary_key=True, index=True)
    province = Column(String(50), unique=True, nullable=False, index=True)
    region = Column(String(20))
    rank = Column(Integer)
    composite_score = Column(Float)
    stage_increment = Column(Float)
    type_name = Column(String(50))
    lisa_type = Column(String(50))
    primary_obstacle_dimension = Column(String(50))
    secondary_obstacle_dimension = Column(String(50))
    weakness_diagnosis_type = Column(String(100))
    demand_network_advantage_index = Column(Float)
    energy_low_carbon_advantage_index = Column(Float)
    constraint_pressure_index = Column(Float)
    suitability_index = Column(Float)
    recommended_layout_type = Column(String(50))
    layout_orientation = Column(String(50))
    functional_positioning = Column(Text)
    optimization_strategy = Column(Text)
    risk_warning = Column(Text)
    created_at = Column(DateTime, server_default=func.now())


class LayoutTypeSummary(Base):
    __tablename__ = "layout_type_summary"
    id = Column(Integer, primary_key=True, index=True)
    recommended_layout_type = Column(String(50), unique=True)
    province_count = Column(Integer)
    avg_composite_score = Column(Float)
    avg_rank = Column(Float)
    avg_suitability_index = Column(Float)
    demand_network_advantage_index = Column(Float)
    energy_low_carbon_advantage_index = Column(Float)
    avg_primary_obstacle_degree = Column(Float)
    province = Column(Text)
    created_at = Column(DateTime, server_default=func.now())


# ---------------------------------------------------------------------------
# Dagum Decomposition (added for public API)
# ---------------------------------------------------------------------------

class DagumDecomposition(Base):
    __tablename__ = "dagum_decomposition"
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, unique=True)
    total_gini = Column(Float)
    intra_region_difference = Column(Float)
    inter_region_net_difference = Column(Float)
    hypervariable_density = Column(Float)
    decomposition_sum = Column(Float)
    intra_region_contribution_rate = Column(Float)
    inter_region_contribution_rate = Column(Float)
    hypervariable_density_contribution_rate = Column(Float)
    created_at = Column(DateTime, server_default=func.now())


class DagumIntraRegion(Base):
    __tablename__ = "dagum_intra_region"
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False)
    region = Column(String(20), nullable=False)
    sample_size = Column(Integer)
    mean_value = Column(Float)
    intra_region_gini = Column(Float)
    p_j = Column(Float)
    s_j = Column(Float)
    created_at = Column(DateTime, server_default=func.now())


class DagumInterRegion(Base):
    __tablename__ = "dagum_inter_region"
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False)
    region_pair = Column(String(50), nullable=False)
    high_mean_region = Column(String(20))
    low_mean_region = Column(String(20))
    inter_region_gini = Column(Float)
    relative_influence_d = Column(Float)
    net_difference_contribution = Column(Float)
    hypervariable_density_contribution = Column(Float)
    created_at = Column(DateTime, server_default=func.now())


class MoranResult(Base):
    __tablename__ = "moran_results"
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, unique=True)
    moran_i = Column(Float)
    two_sided_p_value = Column(Float)
    positive_p_value = Column(Float)
    permutation_mean = Column(Float)
    permutation_std = Column(Float)
    created_at = Column(DateTime, server_default=func.now())


class LisaResult(Base):
    __tablename__ = "lisa_results"
    id = Column(Integer, primary_key=True, index=True)
    province = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    composite_score = Column(Float)
    standardized_score_z = Column(Float)
    spatial_lag_wz = Column(Float)
    local_moran_i = Column(Float)
    p_value = Column(Float)
    lisa_type = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())


class MarkovProbability(Base):
    __tablename__ = "markov_probability"
    id = Column(Integer, primary_key=True, index=True)
    from_state = Column(String(20), nullable=False, unique=True)
    to_low_level_probability = Column(Float)
    to_mid_low_level_probability = Column(Float)
    to_mid_high_level_probability = Column(Float)
    to_high_level_probability = Column(Float)
    created_at = Column(DateTime, server_default=func.now())


class SpatialMarkov(Base):
    __tablename__ = "spatial_markov"
    id = Column(Integer, primary_key=True, index=True)
    neighborhood_state = Column(String(20), nullable=False)
    from_state = Column(String(20), nullable=False)
    to_state = Column(String(20), nullable=False)
    frequency = Column(Integer)
    probability = Column(Float)
    created_at = Column(DateTime, server_default=func.now())


class StateThreshold(Base):
    __tablename__ = "state_thresholds"
    id = Column(Integer, primary_key=True, index=True)
    state = Column(String(20), nullable=False, unique=True)
    classification_rule = Column(Text)
    threshold_note = Column(Text)
    created_at = Column(DateTime, server_default=func.now())


class SpatialLagState(Base):
    __tablename__ = "spatial_lag_state"
    id = Column(Integer, primary_key=True, index=True)
    province = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    spatial_lag_score = Column(Float)
    neighborhood_state_code = Column(Integer)
    neighborhood_state_name = Column(String(20))
    current_state = Column(String(20))
    next_state = Column(String(20))
    created_at = Column(DateTime, server_default=func.now())


class KdeStatistic(Base):
    __tablename__ = "kde_statistics"
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, unique=True)
    mean_value = Column(Float)
    standard_deviation = Column(Float)
    skewness = Column(Float)
    kurtosis = Column(Float)
    min_value = Column(Float)
    max_value = Column(Float)
    peak_position = Column(Float)
    peak_height = Column(Float)
    created_at = Column(DateTime, server_default=func.now())


class LpaTypeTrajectory(Base):
    __tablename__ = "lpa_type_trajectory"
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, unique=True)
    type1_high_leading = Column(Float)
    type2_advantage_supporting = Column(Float)
    type3_mid_catching_up = Column(Float)
    type4_basic_cultivating = Column(Float)
    created_at = Column(DateTime, server_default=func.now())
