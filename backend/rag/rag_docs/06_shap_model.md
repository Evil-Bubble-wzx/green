# SHAP 可解释性分析

## 模型原理
SHAP（SHapley Additive exPlanations）基于博弈论中的 Shapley 值，
为每个特征分配其对模型预测的边际贡献。

本系统使用 XGBoost 和 RandomForest 模型拟合综合得分，
再通过 SHAP 方法解释各指标的贡献方向和大小。

## SHAP 值含义
- SHAP 值 > 0：该指标对绿色算力承载能力有正向贡献
- SHAP 值 < 0：该指标对绿色算力承载能力有负向制约
- |SHAP 值| 越大：该指标的影响越重要

## 分析层次
1. **全局特征重要性** — 34 个指标的平均绝对 SHAP 值排名
2. **年度维度贡献** — 各维度在不同年份的 SHAP 贡献变化
3. **LPA 类型维度贡献** — 不同发展类型的 SHAP 贡献差异
4. **省份局部解释 Top 8** — 每个省份最重要的 8 个影响因素

## 模型性能
- XGBoost R²: 约 0.937
- RandomForest R²: 约 0.919
