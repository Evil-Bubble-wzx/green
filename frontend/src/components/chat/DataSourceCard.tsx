"use client";

interface Props {
  category: string;
  toolCalls: string[];
  ragSources: string[];
}

const CATEGORY_INFO: Record<string, { label: string; desc: string }> = {
  concept_explanation: { label: "概念解释", desc: "基于 RAG 知识库检索相关文档生成回答" },
  data_query: { label: "数据查询", desc: "查询 PostgreSQL 数据库中的最新数据" },
  province_diagnosis: { label: "省域诊断", desc: "综合得分、LPA、障碍度、SHAP 多模型分析" },
  layout_recommendation: { label: "布局建议", desc: "基于布局决策模型和对比分析" },
  future_prediction: { label: "未来预测", desc: "基于未来潜力评分模型和历史趋势外推" },
  unsupported: { label: "暂不支持", desc: "当前数据粒度不支持该查询" },
};

const TOOL_LABELS: Record<string, string> = {
  get_latest_scores: "最新得分排名",
  get_province_score: "省份得分",
  get_province_trend: "历史趋势",
  get_top_rankings: "Top 排名",
  get_lpa_result: "LPA 类型",
  get_obstacle_result: "障碍度诊断",
  get_shap_top_features: "SHAP 因子",
  get_layout_recommendation: "布局决策",
  compare_provinces: "省份对比",
  get_future_potential_ranking: "未来潜力评分",
};

export default function DataSourceCard({ category, toolCalls, ragSources }: Props) {
  if (!category && toolCalls.length === 0 && ragSources.length === 0) return null;

  const info = CATEGORY_INFO[category] || { label: category, desc: "" };

  return (
    <div className="mx-4 my-3 px-4 py-3 bg-dark-card/50 border border-dark-lighter rounded-xl">
      <div className="flex items-center gap-2 mb-2">
        <span className="text-xs">🔍</span>
        <span className="text-xs font-medium text-slate-300">{info.label}</span>
        <span className="text-[11px] text-slate-500">· {info.desc}</span>
      </div>

      <div className="flex flex-wrap gap-1.5">
        {toolCalls.map((tool) => (
          <span
            key={tool}
            className="inline-flex items-center px-2 py-0.5 rounded-md text-[11px]
                       bg-primary/10 text-primary-light border border-primary/20"
          >
            🔧 {TOOL_LABELS[tool] || tool}
          </span>
        ))}
        {ragSources.map((src) => (
          <span
            key={src}
            className="inline-flex items-center px-2 py-0.5 rounded-md text-[11px]
                       bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
          >
            📚 {src}
          </span>
        ))}
      </div>
    </div>
  );
}
