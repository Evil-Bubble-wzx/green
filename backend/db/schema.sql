-- ============================================================================
-- Green Compute System - PostgreSQL Schema
-- Database: green_compute
-- Generated from data/metadata/data_dictionary.xlsx
-- ============================================================================

-- ============================================================================
-- 1. Reference / Lookup Tables
-- ============================================================================

-- Province basic information (31 provinces, 4 regions)
CREATE TABLE IF NOT EXISTS province_basic (
    id SERIAL PRIMARY KEY,
    province VARCHAR(50) NOT NULL UNIQUE,
    region VARCHAR(20) NOT NULL,           -- 东部 / 中部 / 西部 / 东北
    is_hub BOOLEAN DEFAULT FALSE,          -- 是否为国家算力枢纽节点
    adjacent_provinces TEXT,               -- 邻接省份列表
    adjacent_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indicator system definition (34 indicators, 8 dimensions)
CREATE TABLE IF NOT EXISTS indicator_system (
    id SERIAL PRIMARY KEY,
    indicator_code VARCHAR(20) UNIQUE,     -- X01 ~ X34
    indicator_name VARCHAR(100) NOT NULL,  -- 指标名称 (Chinese)
    field_name VARCHAR(100) NOT NULL UNIQUE, -- English field name (e.g., x01_gdp)
    dimension VARCHAR(50) NOT NULL,        -- 一级维度
    direction VARCHAR(10) NOT NULL,        -- 正向 / 逆向
    unit VARCHAR(50),                      -- 单位
    meaning TEXT,                          -- 指标含义
    is_core_indicator BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 2. Core Data Tables
-- ============================================================================

-- Raw indicator values (clean_data.xlsx -> clean_data sheet)
CREATE TABLE IF NOT EXISTS indicator_values (
    id SERIAL PRIMARY KEY,
    province VARCHAR(50) NOT NULL,
    year INTEGER NOT NULL,
    x01_gdp DOUBLE PRECISION,
    x02_population DOUBLE PRECISION,
    x03_energy_consumption DOUBLE PRECISION,
    x04_co2_emission DOUBLE PRECISION,
    x05_fiber_cable_per_10k DOUBLE PRECISION,
    x06_5g_base_stations_per_10k DOUBLE PRECISION,
    x07_access_ports_per_10k DOUBLE PRECISION,
    x08_energy_consumption_per_gdp DOUBLE PRECISION,
    x09_renewable_power_share DOUBLE PRECISION,
    x10_carbon_intensity DOUBLE PRECISION,
    x11_it_service_value_added_share DOUBLE PRECISION,
    x12_telecom_business_intensity DOUBLE PRECISION,
    x13_labor_productivity DOUBLE PRECISION,
    x14_rd_expenditure_intensity DOUBLE PRECISION,
    x15_invention_patents_per_10k DOUBLE PRECISION,
    x16_high_tech_investment_intensity DOUBLE PRECISION,
    x17_power_capacity_per_10k DOUBLE PRECISION,
    x18_mobile_phone_penetration DOUBLE PRECISION,
    x19_mobile_internet_penetration DOUBLE PRECISION,
    x20_broadband_users_per_10k DOUBLE PRECISION,
    x21_avg_temperature DOUBLE PRECISION,
    x22_it_employee_share DOUBLE PRECISION,
    x23_water_resources_per_capita DOUBLE PRECISION,
    x24_science_tech_expenditure_share DOUBLE PRECISION,
    x25_electricity_consumption DOUBLE PRECISION,
    x26_electricity_per_capita DOUBLE PRECISION,
    x27_industrial_solid_waste_utilization DOUBLE PRECISION,
    x28_energy_saving_env_spending_intensity DOUBLE PRECISION,
    x29_tertiary_industry_value_added DOUBLE PRECISION,
    x30_rd_personnel_fte DOUBLE PRECISION,
    x31_green_patent_applications DOUBLE PRECISION,
    x32_gov_science_tech_spending DOUBLE PRECISION,
    x33_digital_financial_inclusion_index DOUBLE PRECISION,
    x34_national_compute_hub_code INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (province, year)
);

-- Normalized/standardized indicator values (表3-1_标准化数据.xlsx)
CREATE TABLE IF NOT EXISTS indicator_values_normalized (
    id SERIAL PRIMARY KEY,
    province VARCHAR(50) NOT NULL,
    year INTEGER NOT NULL,
    x01_gdp DOUBLE PRECISION,
    x02_population DOUBLE PRECISION,
    x03_energy_consumption DOUBLE PRECISION,
    x04_co2_emission DOUBLE PRECISION,
    x05_fiber_cable_per_10k DOUBLE PRECISION,
    x06_5g_base_stations_per_10k DOUBLE PRECISION,
    x07_access_ports_per_10k DOUBLE PRECISION,
    x08_energy_consumption_per_gdp DOUBLE PRECISION,
    x09_renewable_power_share DOUBLE PRECISION,
    x10_carbon_intensity DOUBLE PRECISION,
    x11_it_service_value_added_share DOUBLE PRECISION,
    x12_telecom_business_intensity DOUBLE PRECISION,
    x13_labor_productivity DOUBLE PRECISION,
    x14_rd_expenditure_intensity DOUBLE PRECISION,
    x15_invention_patents_per_10k DOUBLE PRECISION,
    x16_high_tech_investment_intensity DOUBLE PRECISION,
    x17_power_capacity_per_10k DOUBLE PRECISION,
    x18_mobile_phone_penetration DOUBLE PRECISION,
    x19_mobile_internet_penetration DOUBLE PRECISION,
    x20_broadband_users_per_10k DOUBLE PRECISION,
    x21_avg_temperature DOUBLE PRECISION,
    x22_it_employee_share DOUBLE PRECISION,
    x23_water_resources_per_capita DOUBLE PRECISION,
    x24_science_tech_expenditure_share DOUBLE PRECISION,
    x25_electricity_consumption DOUBLE PRECISION,
    x26_electricity_per_capita DOUBLE PRECISION,
    x27_industrial_solid_waste_utilization DOUBLE PRECISION,
    x28_energy_saving_env_spending_intensity DOUBLE PRECISION,
    x29_tertiary_industry_value_added DOUBLE PRECISION,
    x30_rd_personnel_fte DOUBLE PRECISION,
    x31_green_patent_applications DOUBLE PRECISION,
    x32_gov_science_tech_spending DOUBLE PRECISION,
    x33_digital_financial_inclusion_index DOUBLE PRECISION,
    x34_national_compute_hub_code INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (province, year)
);

-- Indicator weights (表3-2_组合权重结果.xlsx)
CREATE TABLE IF NOT EXISTS indicator_weights (
    id SERIAL PRIMARY KEY,
    rank INTEGER NOT NULL,
    indicator_name VARCHAR(100) NOT NULL,
    dimension VARCHAR(50) NOT NULL,
    indicator_direction VARCHAR(10) NOT NULL,
    entropy_weight DOUBLE PRECISION,
    critic_weight DOUBLE PRECISION,
    combined_weight DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TOPSIS composite scores (表3-3_绿色算力综合得分(1).xlsx)
CREATE TABLE IF NOT EXISTS topsis_scores (
    id SERIAL PRIMARY KEY,
    province VARCHAR(50) NOT NULL,
    year INTEGER NOT NULL,
    composite_score DOUBLE PRECISION,
    rank INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (province, year)
);

-- ============================================================================
-- 3. LPA (Latent Profile Analysis) Results
-- ============================================================================

-- LPA model fit statistics (第4章 - 表4-1模型拟合)
CREATE TABLE IF NOT EXISTS lpa_model_fit (
    id SERIAL PRIMARY KEY,
    class_count INTEGER NOT NULL,
    aic DOUBLE PRECISION,
    bic DOUBLE PRECISION,
    entropy DOUBLE PRECISION,
    min_class_sample_size INTEGER,
    class_size VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- LPA type summary (第4章 - 表4-2类型汇总)
CREATE TABLE IF NOT EXISTS lpa_type_summary (
    id SERIAL PRIMARY KEY,
    lpa_type VARCHAR(20) NOT NULL,         -- 类型1 ~ 类型4
    type_name VARCHAR(50) NOT NULL,        -- 高位领先型 / 优势支撑型 / 中位追赶型 / 基础培育型
    province_count INTEGER,
    mean_2016 DOUBLE PRECISION,
    mean_2024 DOUBLE PRECISION,
    stage_increment DOUBLE PRECISION,
    mean_2016_2024 DOUBLE PRECISION,
    province TEXT,                         -- Comma-separated province list
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- LPA province assignment (第4章 - 表4-3省份归属)
CREATE TABLE IF NOT EXISTS lpa_province_assignment (
    id SERIAL PRIMARY KEY,
    province VARCHAR(50) NOT NULL UNIQUE,
    lpa_type VARCHAR(20) NOT NULL,
    type_name VARCHAR(50) NOT NULL,
    score_2016 DOUBLE PRECISION,
    score_2024 DOUBLE PRECISION,
    stage_increment DOUBLE PRECISION,
    mean_2016_2024 DOUBLE PRECISION,
    max_posterior_probability DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- LPA type mean trajectory (第4章 - 类型均值轨迹)
CREATE TABLE IF NOT EXISTS lpa_type_trajectory (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    type1_high_leading DOUBLE PRECISION,
    type2_advantage_supporting DOUBLE PRECISION,
    type3_mid_catching_up DOUBLE PRECISION,
    type4_basic_cultivating DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (year)
);

-- ============================================================================
-- 4. Spatial Evolution Analysis Results (第5章)
-- ============================================================================

-- KDE statistics
CREATE TABLE IF NOT EXISTS kde_statistics (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL UNIQUE,
    mean_value DOUBLE PRECISION,
    standard_deviation DOUBLE PRECISION,
    skewness DOUBLE PRECISION,
    kurtosis DOUBLE PRECISION,
    min_value DOUBLE PRECISION,
    max_value DOUBLE PRECISION,
    peak_position DOUBLE PRECISION,
    peak_height DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dagum decomposition (overall)
CREATE TABLE IF NOT EXISTS dagum_decomposition (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL UNIQUE,
    total_gini DOUBLE PRECISION,
    intra_region_difference DOUBLE PRECISION,
    inter_region_net_difference DOUBLE PRECISION,
    hypervariable_density DOUBLE PRECISION,
    decomposition_sum DOUBLE PRECISION,
    intra_region_contribution_rate DOUBLE PRECISION,
    inter_region_contribution_rate DOUBLE PRECISION,
    hypervariable_density_contribution_rate DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dagum intra-region details
CREATE TABLE IF NOT EXISTS dagum_intra_region (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    region VARCHAR(20) NOT NULL,
    sample_size INTEGER,
    mean_value DOUBLE PRECISION,
    intra_region_gini DOUBLE PRECISION,
    p_j DOUBLE PRECISION,
    s_j DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (year, region)
);

-- Dagum inter-region details
CREATE TABLE IF NOT EXISTS dagum_inter_region (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    region_pair VARCHAR(50) NOT NULL,
    high_mean_region VARCHAR(20),
    low_mean_region VARCHAR(20),
    inter_region_gini DOUBLE PRECISION,
    relative_influence_d DOUBLE PRECISION,
    net_difference_contribution DOUBLE PRECISION,
    hypervariable_density_contribution DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (year, region_pair)
);

-- Global Moran's I
CREATE TABLE IF NOT EXISTS moran_results (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL UNIQUE,
    moran_i DOUBLE PRECISION,
    two_sided_p_value DOUBLE PRECISION,
    positive_p_value DOUBLE PRECISION,
    permutation_mean DOUBLE PRECISION,
    permutation_std DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- LISA results (2024)
CREATE TABLE IF NOT EXISTS lisa_results (
    id SERIAL PRIMARY KEY,
    province VARCHAR(50) NOT NULL,
    year INTEGER NOT NULL DEFAULT 2024,
    composite_score DOUBLE PRECISION,
    standardized_score_z DOUBLE PRECISION,
    spatial_lag_wz DOUBLE PRECISION,
    local_moran_i DOUBLE PRECISION,
    p_value DOUBLE PRECISION,
    lisa_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (province, year)
);

-- Traditional Markov transition frequency
CREATE TABLE IF NOT EXISTS markov_frequency (
    id SERIAL PRIMARY KEY,
    from_state VARCHAR(20) NOT NULL,
    to_low_level_count INTEGER DEFAULT 0,
    to_mid_low_level_count INTEGER DEFAULT 0,
    to_mid_high_level_count INTEGER DEFAULT 0,
    to_high_level_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (from_state)
);

-- Traditional Markov transition probability
CREATE TABLE IF NOT EXISTS markov_probability (
    id SERIAL PRIMARY KEY,
    from_state VARCHAR(20) NOT NULL,
    to_low_level_probability DOUBLE PRECISION,
    to_mid_low_level_probability DOUBLE PRECISION,
    to_mid_high_level_probability DOUBLE PRECISION,
    to_high_level_probability DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (from_state)
);

-- Spatial Markov chain (long format)
CREATE TABLE IF NOT EXISTS spatial_markov (
    id SERIAL PRIMARY KEY,
    neighborhood_state VARCHAR(20) NOT NULL,
    from_state VARCHAR(20) NOT NULL,
    to_state VARCHAR(20) NOT NULL,
    frequency INTEGER,
    probability DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (neighborhood_state, from_state, to_state)
);

-- Spatial lag state (panel)
CREATE TABLE IF NOT EXISTS spatial_lag_state (
    id SERIAL PRIMARY KEY,
    province VARCHAR(50) NOT NULL,
    year INTEGER NOT NULL,
    spatial_lag_score DOUBLE PRECISION,
    neighborhood_state_code INTEGER,
    neighborhood_state_name VARCHAR(20),
    current_state VARCHAR(20),
    next_state VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (province, year)
);

-- State classification thresholds
CREATE TABLE IF NOT EXISTS state_thresholds (
    id SERIAL PRIMARY KEY,
    state VARCHAR(20) NOT NULL UNIQUE,
    classification_rule TEXT,
    threshold_note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Spatial adjacency matrix
CREATE TABLE IF NOT EXISTS adjacency_matrix (
    id SERIAL PRIMARY KEY,
    province VARCHAR(50) NOT NULL UNIQUE,
    adjacent_provinces TEXT,
    adjacent_count INTEGER,
    region VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 5. Obstacle Degree Model Results (第6章)
-- ============================================================================

-- National-level dimension obstacle degree
CREATE TABLE IF NOT EXISTS obstacle_national (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    dimension VARCHAR(50) NOT NULL,
    dimension_obstacle_degree DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (year, dimension)
);

-- Regional dimension obstacle degree
CREATE TABLE IF NOT EXISTS obstacle_regional (
    id SERIAL PRIMARY KEY,
    region VARCHAR(20) NOT NULL UNIQUE,
    digital_infrastructure DOUBLE PRECISION,
    computing_demand_base DOUBLE PRECISION,
    energy_supply_capacity DOUBLE PRECISION,
    green_low_carbon_constraint DOUBLE PRECISION,
    innovation_talent_support DOUBLE PRECISION,
    climate_natural_condition DOUBLE PRECISION,
    regional_coordination_capacity DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- LPA-type dimension obstacle degree
CREATE TABLE IF NOT EXISTS obstacle_lpa (
    id SERIAL PRIMARY KEY,
    lpa_type VARCHAR(20) NOT NULL UNIQUE,
    digital_infrastructure DOUBLE PRECISION,
    computing_demand_base DOUBLE PRECISION,
    energy_supply_capacity DOUBLE PRECISION,
    green_low_carbon_constraint DOUBLE PRECISION,
    innovation_talent_support DOUBLE PRECISION,
    climate_natural_condition DOUBLE PRECISION,
    regional_coordination_capacity DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Province weakness diagnosis (short board analysis)
CREATE TABLE IF NOT EXISTS obstacle_province (
    id SERIAL PRIMARY KEY,
    province VARCHAR(50) NOT NULL UNIQUE,
    region VARCHAR(20),
    lpa_type VARCHAR(20),
    primary_obstacle_dimension VARCHAR(50),
    primary_obstacle_degree DOUBLE PRECISION,
    secondary_obstacle_dimension VARCHAR(50),
    secondary_obstacle_degree DOUBLE PRECISION,
    weakness_diagnosis_type VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Secondary indicator obstacle degree
CREATE TABLE IF NOT EXISTS obstacle_indicator (
    id SERIAL PRIMARY KEY,
    indicator_name VARCHAR(100) NOT NULL,
    dimension VARCHAR(50),
    secondary_indicator_obstacle_degree DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Annual obstacle degree evolution (wide format -> stored as year-dimension pairs)
CREATE TABLE IF NOT EXISTS obstacle_annual_evolution (
    id SERIAL PRIMARY KEY,
    dimension VARCHAR(50) NOT NULL,
    year_2016 DOUBLE PRECISION,
    year_2017 DOUBLE PRECISION,
    year_2018 DOUBLE PRECISION,
    year_2019 DOUBLE PRECISION,
    year_2020 DOUBLE PRECISION,
    year_2021 DOUBLE PRECISION,
    year_2022 DOUBLE PRECISION,
    year_2023 DOUBLE PRECISION,
    year_2024 DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (dimension)
);

-- Province-indicator detail 2024
CREATE TABLE IF NOT EXISTS obstacle_province_indicator_detail (
    id SERIAL PRIMARY KEY,
    province VARCHAR(50) NOT NULL,
    year INTEGER NOT NULL DEFAULT 2024,
    indicator_name VARCHAR(100) NOT NULL,
    dimension VARCHAR(50),
    standardized_value DOUBLE PRECISION,
    target_gap DOUBLE PRECISION,
    combined_weight DOUBLE PRECISION,
    weighted_target_gap DOUBLE PRECISION,
    secondary_indicator_obstacle_degree DOUBLE PRECISION,
    region VARCHAR(20),
    lpa_type VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 6. SHAP Interpretation Results (第7章)
-- ============================================================================

-- Model performance metrics
CREATE TABLE IF NOT EXISTS shap_model_metrics (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(50) NOT NULL,
    test_year INTEGER NOT NULL,
    r2 DOUBLE PRECISION,
    rmse DOUBLE PRECISION,
    mae DOUBLE PRECISION,
    mse DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (model_name, test_year)
);

-- Prediction results
CREATE TABLE IF NOT EXISTS shap_predictions (
    id SERIAL PRIMARY KEY,
    province VARCHAR(50) NOT NULL,
    year INTEGER NOT NULL DEFAULT 2024,
    composite_score DOUBLE PRECISION,
    rank INTEGER,
    lpa_type VARCHAR(20),
    type_name VARCHAR(50),
    predicted_composite_score DOUBLE PRECISION,
    prediction_error DOUBLE PRECISION,
    absolute_error DOUBLE PRECISION,
    error_direction VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (province, year)
);

-- Global SHAP importance
CREATE TABLE IF NOT EXISTS shap_importance (
    id SERIAL PRIMARY KEY,
    indicator_name VARCHAR(100) NOT NULL,
    indicator_short_name VARCHAR(50),
    dimension VARCHAR(50),
    dimension_short_name VARCHAR(50),
    combined_weight DOUBLE PRECISION,
    mean_abs_shap_value DOUBLE PRECISION,
    mean_shap_value DOUBLE PRECISION,
    importance_rank INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Annual dimension SHAP contribution
CREATE TABLE IF NOT EXISTS shap_annual_dimension_contribution (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL UNIQUE,
    innovation_talent_support DOUBLE PRECISION,
    digital_infrastructure DOUBLE PRECISION,
    energy_supply_capacity DOUBLE PRECISION,
    regional_coordination_capacity DOUBLE PRECISION,
    climate_natural_condition DOUBLE PRECISION,
    computing_demand_base DOUBLE PRECISION,
    green_low_carbon_constraint DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- LPA dimension SHAP contribution
CREATE TABLE IF NOT EXISTS shap_lpa_dimension_contribution (
    id SERIAL PRIMARY KEY,
    type_name VARCHAR(50) NOT NULL UNIQUE,
    innovation_talent_support DOUBLE PRECISION,
    digital_infrastructure DOUBLE PRECISION,
    energy_supply_capacity DOUBLE PRECISION,
    regional_coordination_capacity DOUBLE PRECISION,
    climate_natural_condition DOUBLE PRECISION,
    computing_demand_base DOUBLE PRECISION,
    green_low_carbon_constraint DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Province SHAP summary
CREATE TABLE IF NOT EXISTS shap_province_summary (
    id SERIAL PRIMARY KEY,
    province VARCHAR(50) NOT NULL,
    year INTEGER NOT NULL DEFAULT 2024,
    composite_score DOUBLE PRECISION,
    rank INTEGER,
    lpa_type VARCHAR(20),
    type_name VARCHAR(50),
    predicted_composite_score DOUBLE PRECISION,
    prediction_error DOUBLE PRECISION,
    absolute_error DOUBLE PRECISION,
    error_direction VARCHAR(20),
    positive_contribution_sum DOUBLE PRECISION,
    negative_contribution_sum DOUBLE PRECISION,
    base_value DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (province, year)
);

-- Local SHAP Top 8 explanation
CREATE TABLE IF NOT EXISTS shap_local_top8 (
    id SERIAL PRIMARY KEY,
    province VARCHAR(50) NOT NULL,
    indicator_name VARCHAR(100),
    indicator_short_name VARCHAR(50),
    dimension VARCHAR(50),
    shap_value DOUBLE PRECISION,
    abs_shap_value DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 7. Layout Decision Results (第8章)
-- ============================================================================

-- Province layout decision
CREATE TABLE IF NOT EXISTS layout_province_decision (
    id SERIAL PRIMARY KEY,
    province VARCHAR(50) NOT NULL UNIQUE,
    region VARCHAR(20),
    rank INTEGER,
    composite_score DOUBLE PRECISION,
    stage_increment DOUBLE PRECISION,
    type_name VARCHAR(50),
    lisa_type VARCHAR(50),
    primary_obstacle_dimension VARCHAR(50),
    secondary_obstacle_dimension VARCHAR(50),
    weakness_diagnosis_type VARCHAR(100),
    demand_network_advantage_index DOUBLE PRECISION,
    energy_low_carbon_advantage_index DOUBLE PRECISION,
    constraint_pressure_index DOUBLE PRECISION,
    suitability_index DOUBLE PRECISION,
    recommended_layout_type VARCHAR(50),
    layout_orientation VARCHAR(50),
    functional_positioning TEXT,
    optimization_strategy TEXT,
    risk_warning TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Layout type summary
CREATE TABLE IF NOT EXISTS layout_type_summary (
    id SERIAL PRIMARY KEY,
    recommended_layout_type VARCHAR(50) NOT NULL UNIQUE,
    province_count INTEGER,
    avg_composite_score DOUBLE PRECISION,
    avg_rank DOUBLE PRECISION,
    avg_suitability_index DOUBLE PRECISION,
    demand_network_advantage_index DOUBLE PRECISION,
    energy_low_carbon_advantage_index DOUBLE PRECISION,
    avg_primary_obstacle_degree DOUBLE PRECISION,
    province TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Layout type feature means
CREATE TABLE IF NOT EXISTS layout_type_features (
    id SERIAL PRIMARY KEY,
    recommended_layout_type VARCHAR(50) NOT NULL UNIQUE,
    avg_composite_score DOUBLE PRECISION,
    avg_suitability_index DOUBLE PRECISION,
    demand_network_advantage_index DOUBLE PRECISION,
    energy_low_carbon_advantage_index DOUBLE PRECISION,
    avg_primary_obstacle_degree DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- LPA to layout mapping matrix
CREATE TABLE IF NOT EXISTS layout_lpa_matrix (
    id SERIAL PRIMARY KEY,
    type_name VARCHAR(50) NOT NULL UNIQUE,
    high_suitability_comprehensive_zone INTEGER DEFAULT 0,
    demand_network_driven_zone INTEGER DEFAULT 0,
    energy_low_carbon_advantage_zone INTEGER DEFAULT 0,
    comprehensive_potential_improvement_zone INTEGER DEFAULT 0,
    constraint_control_zone INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Strategy library
CREATE TABLE IF NOT EXISTS layout_strategy_library (
    id SERIAL PRIMARY KEY,
    recommended_layout_type VARCHAR(50) NOT NULL UNIQUE,
    layout_orientation VARCHAR(50),
    functional_positioning TEXT,
    optimization_strategy TEXT,
    risk_warning TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Strategy priority scores
CREATE TABLE IF NOT EXISTS layout_strategy_priority (
    id SERIAL PRIMARY KEY,
    recommended_layout_type VARCHAR(50) NOT NULL UNIQUE,
    new_computing_layout_priority INTEGER,
    green_energy_coordination_priority INTEGER,
    network_channel_strengthening_priority INTEGER,
    industrial_demand_cultivation_priority INTEGER,
    existing_energy_saving_retrofit_priority INTEGER,
    innovation_talent_support_priority INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 8. Indexes for common query patterns
-- ============================================================================

-- Province + year lookups
CREATE INDEX IF NOT EXISTS idx_indicator_values_province_year ON indicator_values (province, year);
CREATE INDEX IF NOT EXISTS idx_indicator_values_norm_province_year ON indicator_values_normalized (province, year);
CREATE INDEX IF NOT EXISTS idx_topsis_scores_province_year ON topsis_scores (province, year);
CREATE INDEX IF NOT EXISTS idx_topsis_scores_rank ON topsis_scores (rank);
CREATE INDEX IF NOT EXISTS idx_topsis_scores_year ON topsis_scores (year);

-- Spatial analysis indexes
CREATE INDEX IF NOT EXISTS idx_dagum_intra_region_year ON dagum_intra_region (year);
CREATE INDEX IF NOT EXISTS idx_dagum_inter_region_year ON dagum_inter_region (year);
CREATE INDEX IF NOT EXISTS idx_spatial_lag_state_province_year ON spatial_lag_state (province, year);
CREATE INDEX IF NOT EXISTS idx_lisa_results_province ON lisa_results (province);

-- Obstacle indexes
CREATE INDEX IF NOT EXISTS idx_obstacle_national_year ON obstacle_national (year);
CREATE INDEX IF NOT EXISTS idx_obstacle_province_indicator_detail_province ON obstacle_province_indicator_detail (province);

-- SHAP indexes
CREATE INDEX IF NOT EXISTS idx_shap_local_top8_province ON shap_local_top8 (province);
CREATE INDEX IF NOT EXISTS idx_shap_importance_rank ON shap_importance (importance_rank);

-- Layout indexes
CREATE INDEX IF NOT EXISTS idx_layout_province_decision_type ON layout_province_decision (recommended_layout_type);
