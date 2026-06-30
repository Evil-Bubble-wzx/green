# 未来趋势预测规则

## 数据粒度约束
**当前平台数据粒度为省级行政区，所有预测和分析仅支持省域级别。
系统不支持城市级数据查询和预测。当用户询问城市级问题时，
必须明确告知数据粒度限制，然后基于省域数据给出最接近的回答。**

## 未来潜力综合评分公式
future_potential_score =
  0.30 × current_score（当前综合得分）
  + 0.25 × historical_growth（2016-2024 历史增速）
  + 0.15 × markov_upgrade_probability（Markov 向上转移概率）
  + 0.15 × green_energy_low_carbon_advantage（能源低碳优势指数）
  + 0.10 × shap_positive_driver_strength（SHAP 正向驱动强度）
  + 0.05 × obstacle_reverse_score（障碍度反向得分）

## 各因子说明
- **current_score**：最新年份 TOPSIS 综合得分
- **historical_growth**：2016 到 2024 年得分增长量/2016 年得分
- **markov_upgrade_probability**：从当前状态向上转移至少一级的概率
- **green_energy_low_carbon_advantage**：能源低碳优势指数
- **shap_positive_driver_strength**：SHAP 正向贡献合计 / (正向+负向绝对值合计)
- **obstacle_reverse_score**：100 - 首要障碍度，障碍越低潜力越大

## 局限性说明
1. 未来潜力评分基于历史趋势外推，不代表确定性的未来结果
2. 未考虑政策变化、技术突破、重大投资等外生冲击
3. 评分反映的是基于当前模型和数据的最优估计
4. 建议结合专家判断和最新政策动态综合决策
