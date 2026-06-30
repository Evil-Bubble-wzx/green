# Data Import Validation Report

**Generated:** 2026-06-22 13:21:07
**Summary:** 41 succeeded, 0 failed
**Total rows imported:** 1412

---

## Import Results

| Table | File | Rows | Status |
|-------|------|------|--------|
| indicator_values | clean_data.xlsx | 0 | ✅ OK |
| indicator_system | 表2-1_指标体系.xlsx | 34 | ✅ OK |
| indicator_values_normalized | 表3-1_标准化数据.xlsx | 0 | ✅ OK |
| indicator_weights | 表3-2_组合权重结果.xlsx | 0 | ✅ OK |
| topsis_scores | 表3-3_绿色算力综合得分(1).xlsx | 0 | ✅ OK |
| lpa_model_fit | 第4章_LPA结果表(1).xlsx | 4 | ✅ OK |
| lpa_type_summary | 第4章_LPA结果表(1).xlsx | 4 | ✅ OK |
| lpa_province_assignment | 第4章_LPA结果表(1).xlsx | 0 | ✅ OK |
| lpa_type_trajectory | 第4章_LPA结果表(1).xlsx | 0 | ✅ OK |
| kde_statistics | 第5章_空间演化分析结果表(1).xlsx | 0 | ✅ OK |
| dagum_decomposition | 第5章_空间演化分析结果表(1).xlsx | 0 | ✅ OK |
| dagum_intra_region | 第5章_空间演化分析结果表(1).xlsx | 0 | ✅ OK |
| dagum_inter_region | 第5章_空间演化分析结果表(1).xlsx | 0 | ✅ OK |
| moran_results | 第5章_空间演化分析结果表(1).xlsx | 0 | ✅ OK |
| lisa_results | 第5章_空间演化分析结果表(1).xlsx | 0 | ✅ OK |
| markov_frequency | 第5章_空间演化分析结果表(1).xlsx | 0 | ✅ OK |
| markov_probability | 第5章_空间演化分析结果表(1).xlsx | 0 | ✅ OK |
| spatial_markov | 第5章_空间演化分析结果表(1).xlsx | 0 | ✅ OK |
| spatial_lag_state | 第5章_空间演化分析结果表(1).xlsx | 0 | ✅ OK |
| state_thresholds | 第5章_空间演化分析结果表(1).xlsx | 0 | ✅ OK |
| adjacency_matrix | 第5章_空间演化分析结果表(1).xlsx | 0 | ✅ OK |
| obstacle_national | 第6章_障碍度模型结果表(1).xlsx | 0 | ✅ OK |
| obstacle_regional | 第6章_障碍度模型结果表(1).xlsx | 0 | ✅ OK |
| obstacle_lpa | 第6章_障碍度模型结果表(1).xlsx | 0 | ✅ OK |
| obstacle_province | 第6章_障碍度模型结果表(1).xlsx | 0 | ✅ OK |
| obstacle_indicator | 第6章_障碍度模型结果表(1).xlsx | 34 | ✅ OK |
| obstacle_annual_evolution | 第6章_障碍度模型结果表(1).xlsx | 0 | ✅ OK |
| obstacle_province_indicator_detail | 第6章_障碍度模型结果表(1).xlsx | 1054 | ✅ OK |
| shap_model_metrics | 第7章_SHAP解释分析结果表(1).xlsx | 0 | ✅ OK |
| shap_predictions | 第7章_SHAP解释分析结果表(1).xlsx | 0 | ✅ OK |
| shap_importance | 第7章_SHAP解释分析结果表(1).xlsx | 34 | ✅ OK |
| shap_annual_dimension_contribution | 第7章_SHAP解释分析结果表(1).xlsx | 0 | ✅ OK |
| shap_lpa_dimension_contribution | 第7章_SHAP解释分析结果表(1).xlsx | 0 | ✅ OK |
| shap_province_summary | 第7章_SHAP解释分析结果表(1).xlsx | 0 | ✅ OK |
| shap_local_top8 | 第7章_SHAP解释分析结果表(1).xlsx | 248 | ✅ OK |
| layout_province_decision | 第8章_布局决策结果表.xlsx | 0 | ✅ OK |
| layout_type_summary | 第8章_布局决策结果表.xlsx | 0 | ✅ OK |
| layout_type_features | 第8章_布局决策结果表.xlsx | 0 | ✅ OK |
| layout_lpa_matrix | 第8章_布局决策结果表.xlsx | 0 | ✅ OK |
| layout_strategy_library | 第8章_布局决策结果表.xlsx | 0 | ✅ OK |
| layout_strategy_priority | 第8章_布局决策结果表.xlsx | 0 | ✅ OK |

---

## Warnings & Errors

---

## Data Standardization Changes

### indicator_values

- Created is_hub column from province and hub_provinces config

### indicator_values_normalized

- Created is_hub column from province and hub_provinces config

### topsis_scores

- Created is_hub column from province and hub_provinces config

### lpa_type_summary

- Created is_hub column from province and hub_provinces config

### lpa_province_assignment

- Created is_hub column from province and hub_provinces config

### lisa_results

- Created is_hub column from province and hub_provinces config

### spatial_lag_state

- Created is_hub column from province and hub_provinces config

### adjacency_matrix

- Created is_hub column from province and hub_provinces config

### obstacle_province

- Created is_hub column from province and hub_provinces config

### obstacle_province_indicator_detail

- Created is_hub column from province and hub_provinces config

### shap_predictions

- Created is_hub column from province and hub_provinces config

### shap_province_summary

- Created is_hub column from province and hub_provinces config

### shap_local_top8

- Created is_hub column from province and hub_provinces config

### layout_province_decision

- Created is_hub column from province and hub_provinces config

### layout_type_summary

- Created is_hub column from province and hub_provinces config

---

## Fields Needing Manual Confirmation

The following items should be reviewed by a human:

1. **Hub provinces** — Verify the hub_provinces list in the config
   matches the actual national compute hub node designations.
2. **Province names** — Check that all province name standardizations are correct.
3. **Indicator codes** — The indicator_system table is now auto-populated from
   data_dictionary.xlsx. Verify the 34 indicator codes are complete.
4. **Region mapping** — Verify all 31 provinces are assigned to the correct region.
5. **Markov state columns** — The 'Unnamed: 0' column in Markov sheets needs
   verification that it maps correctly to 'from_state'.
