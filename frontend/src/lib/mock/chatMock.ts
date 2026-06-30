/**
 * Mock chat responses for demo / offline mode.
 * Activated when NEXT_PUBLIC_USE_MOCK=true.
 */

export interface MockChatResponse {
  answer: string;
  category: string;
  toolCalls: string[];
  ragSources: string[];
}

const MOCK_RESPONSES: Record<string, MockChatResponse> = {
  绿色算力: {
    answer: `## 结论
绿色算力承载能力指数是一个综合评价指标，用于衡量省级行政区在发展绿色算力方面的综合承载能力。

## 数据依据
- 指标体系：34 个二级指标，分为 8 个一级维度（算力需求基础、能源供给能力、数字基础设施、绿色低碳约束、创新与人才支撑、气候与自然条件、区域协同能力、其他）
- 权重方法：熵权法 + CRITIC 法组合权重
- 评价方法：TOPSIS 多属性决策
- 数据范围：2016-2024 年，31 个省级行政区

## 模型依据
TOPSIS（逼近理想解排序法）通过计算各省与"理想最优"和"理想最劣"方案的距离，生成 0-1 之间的综合得分。得分越高，绿色算力承载能力越强。

## 解释逻辑
该指数综合考虑了需求侧（经济、人口、数字产业）、供给侧（能源、基础设施）和约束侧（碳排放、环保）三个维度。某个省即使在某一方面不突出，只要综合条件较好，仍可获得较高得分。

## 建议
- 得分较高的省份（如江苏、广东、浙江）：优先布局全国级算力枢纽
- 得分中等的省份（如贵州、内蒙古）：发挥能源低碳优势，承接算力外溢
- 得分较低的省份：聚焦短板维度精准施策

## 局限性说明
本指数基于省级数据，不适用于城市级评估。指标权重通过数据驱动方法确定，可能无法完全反映政策优先级。`,
    category: "concept_explanation",
    toolCalls: [],
    ragSources: ["01_system_overview.md", "02_topsis_model.md"],
  },

  排名: {
    answer: `## 结论
2024 年绿色算力承载能力综合得分排名前十的省份为：江苏、广东、浙江、北京、上海、山东、福建、湖北、天津、河北。

## 数据依据（2024年 TOPSIS 综合得分）

| 排名 | 省份 | 综合得分 |
|------|------|----------|
| 1 | 江苏 | 0.5733 |
| 2 | 广东 | 0.5643 |
| 3 | 浙江 | 0.5620 |
| 4 | 北京 | 0.5426 |
| 5 | 上海 | 0.5106 |
| 6 | 山东 | 0.4712 |
| 7 | 福建 | 0.4538 |
| 8 | 湖北 | 0.4391 |
| 9 | 天津 | 0.4315 |
| 10 | 河北 | 0.4287 |

## 模型依据
基于熵权法+CRITIC 组合权重和 TOPSIS 方法计算。排名反映的是各省在 8 个维度 34 个指标上的综合表现。

## 解释逻辑
前十省份主要集中在东部沿海地区，这些省份在算力需求基础、数字基础设施和创新人才支撑维度具有显著优势。部分省份虽在能源或低碳维度不占优，但综合需求侧优势足以弥补。

## 建议
排名是相对评价，不应作为唯一决策依据。建议结合各维度的具体得分和障碍度诊断进行深入分析。`,
    category: "data_query",
    toolCalls: ["get_top_rankings", "get_latest_scores"],
    ragSources: ["02_topsis_model.md"],
  },

  贵州: {
    answer: `## 结论
贵州的首要发展短板是**创新与人才支撑**（障碍度 39.19%），次要短板是**算力需求基础**（障碍度 19.60%）。短板诊断类型为"创新需求协同型"。

## 数据依据
- LPA 类型：基础培育型（类型 4）
- 综合得分：0.3484（排名第 20 位）
- 首要障碍维度：创新与人才支撑（39.19%）
- 次要障碍维度：算力需求基础（19.60%）
- 能源低碳优势指数：0.3976（相对较高）
- 约束压力指数：0.5645

## 模型依据
基于障碍度诊断模型、LPA 潜在剖面分析和 SHAP 可解释性分析。

## 解释逻辑
贵州的"创新人才"短板主要体现在 R&D 投入强度、发明专利和科技支出等指标低于全国平均水平。而"需求基础"短板则体现在经济总量和数字产业规模较小。但贵州在能源供给和绿色低碳方面具有天然优势（可再生能源丰富、气候适宜），这正是其被推荐为"能源低碳优势承接区"的原因。

## 建议
1. **短期**：加强网络通道和运维能力建设，承接东部算力外溢
2. **中期**：培育本地数字产业需求，引入数据中心上下游企业
3. **长期**：加大科技教育投入，培育本地创新人才

## 局限性说明
障碍度反映的是相对短板，不代表绝对劣势。贵州在能源和气候维度的优势是显著的，应充分利用。`,
    category: "province_diagnosis",
    toolCalls: ["get_province_score", "get_lpa_result", "get_obstacle_result", "get_shap_top_features"],
    ragSources: ["05_obstacle_model.md", "07_layout_rules.md"],
  },

  布局: {
    answer: `## 结论
贵州和内蒙古各具优势。内蒙古在能源供给和综合适宜度方面略优于贵州，但两者都被推荐为**能源低碳优势承接区**。

## 数据对比

| 维度 | 贵州 | 内蒙古 |
|------|------|--------|
| 综合得分 | 0.3484 | 0.4255 |
| 全国排名 | 20 | 6 |
| LPA 类型 | 基础培育型 | 中位追赶型 |
| 推荐布局 | 能源低碳优势承接区 | 能源低碳优势承接区 |
| 能源低碳优势 | 0.3976 | 0.4263 |
| 首要障碍 | 创新与人才支撑 | 创新与人才支撑 |

## 解释逻辑
内蒙古得分更高，主要因为其在能源供给维度的优势更强（风电、光伏资源丰富），且综合适宜度指数更高。但两者的障碍结构相似——创新人才是共同的首要短板。

## 建议
- 内蒙古：优先发展，利用能源优势和现有排名，加速绿色数据中心集群建设
- 贵州：差异化发展，聚焦特色算力应用场景（如气候优势下的温冷数据存储）
- 两者可以协同：内蒙古承担大规模算力，贵州承担特色算力和灾备

## 局限性说明
比较仅基于当前数据（2024 年），未考虑未来政策变化和投资动向。`,
    category: "layout_recommendation",
    toolCalls: ["get_layout_recommendation", "compare_provinces"],
    ragSources: ["07_layout_rules.md"],
  },

  未来: {
    answer: `## 结论
基于未来潜力综合评分模型，**未来十年最具潜力的 5 个省份**为：江苏、广东、浙江、北京、上海。

## 未来潜力评分公式
\`\`\`
future_potential_score =
  0.30 × current_score（当前得分）
  + 0.25 × historical_growth（历史增速）
  + 0.15 × markov_upgrade_probability（Markov 向上转移概率）
  + 0.15 × energy_advantage（能源低碳优势指数）
  + 0.10 × shap_positive_strength（SHAP 正向驱动强度）
  + 0.05 × obstacle_reverse_score（障碍度反向得分）
\`\`\`

## 数据依据
- Top 5 省份当前得分均在 0.51 以上，具有明显先发优势
- 高位领先型省份历史增速稳定，具有较强的惯性效应
- Markov 转移概率显示高得分省份向下转移概率极低

## 解释逻辑
当前综合得分是最强的预测因子（权重 0.30），因为绿色算力承载能力的建设具有显著的路径依赖特征——基础设施、人才和产业生态的积累需要长期投入。历史增速（权重 0.25）反映了发展惯性。能源低碳优势（权重 0.15）对新兴算力布局尤为关键。

## 建议
- 高位省份应关注"防止高耗能扩张"的风险，避免重复建设
- 中位追赶型省份（如内蒙古、四川、安徽）具有较大的上升空间
- 基础培育型省份应聚焦 1-2 个优势维度实现突破

## 局限性说明
1. ⚠️ **数据粒度**：当前平台数据粒度为省级行政区，不支持城市级预测
2. 预测基于历史趋势外推，未考虑政策变化、技术突破等外生冲击
3. 评分权重基于专家经验设定，可根据实际决策需求调整`,
    category: "future_prediction",
    toolCalls: ["get_future_potential_ranking", "get_latest_scores"],
    ragSources: ["08_future_prediction_rules.md"],
  },
};

const FALLBACK_RESPONSE: MockChatResponse = {
  answer: `## 回答

感谢您的提问。当前我主要擅长以下领域的问题：

1. **概念解释**：绿色算力承载能力指数是什么？TOPSIS 模型如何工作？
2. **数据查询**：某年排名前十的省份有哪些？某省得分是多少？
3. **省域诊断**：某省的发展短板和障碍因素是什么？
4. **布局建议**：哪些省份适合布局绿色算力？
5. **未来预测**：未来十年哪些省份潜力更大？

请尝试提出以上类型的问题，我会基于 RAG 知识库和数据库查询为您提供详细的分析回答。

> 💡 提示：本系统数据粒度为省级行政区，不支持城市级数据查询。`,
  category: "concept_explanation",
  toolCalls: [],
  ragSources: [],
};

/**
 * Match user question to a mock response category.
 * Returns the best matching mock response.
 */
export function getMockResponse(question: string): MockChatResponse {
  const q = question.toLowerCase();

  const matchers: [string[], MockChatResponse][] = [
    [["绿色算力", "承载能力", "指数是什么", "topsis", "什么是"], MOCK_RESPONSES["绿色算力"]],
    [["排名", "前十", "top", "top10", "前10"], MOCK_RESPONSES["排名"]],
    [["贵州", "短板", "障碍", "诊断", "为什么"], MOCK_RESPONSES["贵州"]],
    [["布局", "哪个更适合", "比较", "对比", "承接"], MOCK_RESPONSES["布局"]],
    [["未来", "十年", "潜力", "预测", "趋势", "前景"], MOCK_RESPONSES["未来"]],
  ];

  for (const [keywords, response] of matchers) {
    if (keywords.some((kw) => q.includes(kw))) {
      return response;
    }
  }

  // Province-specific matching
  const provinces = [
    "北京", "天津", "上海", "重庆", "河北", "山西", "内蒙古",
    "辽宁", "吉林", "黑龙江", "江苏", "浙江", "安徽", "福建",
    "江西", "山东", "河南", "湖北", "湖南", "广东", "广西",
    "海南", "四川", "贵州", "云南", "西藏", "陕西", "甘肃",
    "青海", "宁夏", "新疆",
  ];
  const mentioned = provinces.filter((p) => question.includes(p));
  if (mentioned.length >= 2) {
    return MOCK_RESPONSES["布局"];
  }
  if (mentioned.length === 1) {
    if (question.includes("贵州")) return MOCK_RESPONSES["贵州"];
    return {
      ...MOCK_RESPONSES["贵州"],
      answer: MOCK_RESPONSES["贵州"].answer.replace(/贵州/g, mentioned[0]),
    };
  }

  return FALLBACK_RESPONSE;
}

/**
 * Simulate network delay for realistic demo experience.
 */
export function mockDelay(ms: number = 1200): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms + Math.random() * 800));
}
