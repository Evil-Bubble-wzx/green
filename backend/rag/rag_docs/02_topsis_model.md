# TOPSIS 综合评价模型

## 模型原理
TOPSIS（Technique for Order Preference by Similarity to Ideal Solution）
是一种多属性决策方法。本系统先使用熵权法和 CRITIC 法计算组合权重，
再通过 TOPSIS 计算各省绿色算力承载能力的综合得分。

## 权重计算方法
- **熵权法**：基于数据离散程度赋权，离散度越大权重越高
- **CRITIC 法**：基于指标间的对比强度和冲突性赋权
- **组合权重**：熵权法权重与 CRITIC 权重的均值

## 得分含义
综合得分（composite_score）取值范围为 [0, 1]，得分越高表示该省绿色
算力承载能力越强。得分为相对评价，反映省份间的相对位置。

## 排名规则
按 composite_score 降序排列，rank=1 为承载能力最强的省份。
