"use client";
import { useEffect, useState } from "react";
import PageContainer from "@/components/PageContainer";
import ProvinceSelector from "@/components/ProvinceSelector";
import LoadingSpinner from "@/components/LoadingSpinner";
import ErrorMessage from "@/components/ErrorMessage";
import EmptyState from "@/components/EmptyState";
import StatCard from "@/components/StatCard";
import { fetchProvinces, fetchLayout, LayoutDecision } from "@/lib/api";

export default function LayoutDecisionPage() {
  const [provinces, setProvinces] = useState<string[]>([]);
  const [selected, setSelected] = useState("上海");
  const [data, setData] = useState<LayoutDecision | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => { fetchProvinces().then((d) => { const list = d.provinces.map((p) => p.province); setProvinces(list); if (!list.includes("上海")) setSelected(list[0] || ""); }).catch(() => {}); }, []);

  useEffect(() => {
    if (!selected) { setData(null); return; }
    setLoading(true); setError(null);
    fetchLayout(selected).then(setData).catch((e) => setError(e.message)).finally(() => setLoading(false));
  }, [selected]);

  return (
    <PageContainer title="布局决策" subtitle="资源布局决策结果 — 推荐布局类型与优化策略">
      <div className="flex items-center gap-4 mb-6"><ProvinceSelector provinces={provinces} value={selected} onChange={setSelected} loading={loading} /></div>
      {!selected && <EmptyState text="请选择一个省份查看布局决策结果" />}
      {loading && <LoadingSpinner />}
      {error && <ErrorMessage message={error} onRetry={() => setSelected(selected)} />}
      {data && !loading && !error && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <StatCard label="推荐布局类型" value={data.recommended_layout_type ?? "-"} color="blue" />
            <StatCard label="布局导向" value={data.layout_orientation ?? "-"} color="green" />
            <StatCard label="综合适宜度指数" value={data.suitability_index?.toFixed(2) ?? "-"} color="amber" />
            <StatCard label="LISA 类型" value={data.lisa_type ?? "-"} color="red" />
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {[{ label: "需求网络优势指数", value: data.demand_network_advantage_index, color: "bg-primary" },
              { label: "能源低碳优势指数", value: data.energy_low_carbon_advantage_index, color: "bg-accent" },
              { label: "约束压力指数", value: data.constraint_pressure_index, color: "bg-warning" }].map((item) => (
              <div key={item.label} className="bg-dark-card rounded-xl border border-dark-lighter p-4">
                <p className="text-xs text-slate-400 mb-1">{item.label}</p>
                <div className="w-full bg-dark-lighter rounded-full h-2 mt-2"><div className={`${item.color} h-2 rounded-full transition-all`} style={{ width: `${((item.value ?? 0) * 100).toFixed(1)}%` }} /></div>
                <p className="text-lg font-bold text-white mt-1">{item.value?.toFixed(4) ?? "-"}</p>
              </div>
            ))}
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-dark-card rounded-xl border border-dark-lighter p-5 space-y-3">
              <div><h3 className="text-sm font-semibold text-slate-300 mb-1">🏗️ 功能定位</h3><p className="text-white text-sm leading-relaxed">{data.functional_positioning ?? "-"}</p></div>
              <div><h3 className="text-sm font-semibold text-slate-300 mb-1">📋 优化策略</h3><p className="text-white text-sm leading-relaxed">{data.optimization_strategy ?? "-"}</p></div>
            </div>
            <div className="bg-dark-card rounded-xl border border-dark-lighter p-5 space-y-3">
              <h3 className="text-sm font-semibold text-slate-300 mb-2">📊 基础信息</h3>
              <div className="space-y-1.5 text-sm">
                <div className="flex justify-between"><span className="text-slate-400">省份</span><span className="text-white">{data.province}</span></div>
                <div className="flex justify-between"><span className="text-slate-400">区域</span><span className="text-white">{data.region ?? "-"}</span></div>
                <div className="flex justify-between"><span className="text-slate-400">LPA 类型</span><span className="text-white">{data.type_name ?? "-"}</span></div>
                <div className="flex justify-between"><span className="text-slate-400">综合得分</span><span className="text-white font-mono">{data.composite_score?.toFixed(6) ?? "-"}</span></div>
                <div className="flex justify-between"><span className="text-slate-400">全国排名</span><span className="text-white">#{data.rank ?? "-"}</span></div>
                <div className="flex justify-between"><span className="text-slate-400">阶段增量</span><span className="text-accent font-mono">{data.stage_increment?.toFixed(6) ?? "-"}</span></div>
              </div>
              {data.risk_warning && <div className="border-t border-dark-lighter pt-3"><h3 className="text-sm font-semibold text-danger mb-1">⚠️ 风险预警</h3><p className="text-danger text-sm leading-relaxed">{data.risk_warning}</p></div>}
            </div>
          </div>
        </div>
      )}
    </PageContainer>
  );
}
