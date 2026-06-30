"use client";
import { useEffect, useState } from "react";
import PageContainer from "@/components/PageContainer";
import LoadingSpinner from "@/components/LoadingSpinner";
import ErrorMessage from "@/components/ErrorMessage";
import LineChart from "@/components/charts/LineChart";
import DonutChart from "@/components/charts/DonutChart";
import ChinaMap from "@/components/charts/ChinaMap";
import { fetchMoran, fetchScores, fetchLpa, MoranOut, ScoreListOut, LpaListOut } from "@/lib/api";

const LISA_COLORS: Record<string, string> = { "高-高": "#10b981", "低-低": "#ef4444", "高-低": "#f59e0b", "低-高": "#3b82f6", "不显著": "#64748b" };

export default function SpatialClusterPage() {
  const [moran, setMoran] = useState<MoranOut | null>(null);
  const [scores, setScores] = useState<ScoreListOut | null>(null);
  const [lpa, setLpa] = useState<LpaListOut | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = () => { setLoading(true); setError(null); Promise.all([fetchMoran(), fetchScores(2024), fetchLpa()]).then(([m, s, l]) => { setMoran(m); setScores(s); setLpa(l); }).catch((e) => setError(e.message)).finally(() => setLoading(false)); };
  useEffect(() => { load(); }, []);

  if (loading) return <PageContainer title="空间集聚"><LoadingSpinner /></PageContainer>;
  if (error) return <PageContainer title="空间集聚"><ErrorMessage message={error} onRetry={load} /></PageContainer>;
  if (!moran || !scores) return <PageContainer title="空间集聚"><div className="text-slate-400 text-center py-20">暂无数据</div></PageContainer>;

  const moranTrend = moran.moran_series.map((d) => ({ name: String(d.year), value: d.moran_i ?? 0 }));
  const lpaMap = new Map((lpa?.province_assignments || []).map((p) => [p.province, p.type_name || ""]));
  const mapData = scores.scores.map((s) => ({ name: s.province, value: s.composite_score ?? 0, rank: s.rank ?? undefined, typeName: lpaMap.get(s.province) || undefined, region: undefined }));

  // LISA type counts
  const lisaCounts: Record<string, number> = {};
  moran.lisa_2024.forEach((d) => { const t = d.lisa_type || "不显著"; lisaCounts[t] = (lisaCounts[t] || 0) + 1; });
  const lisaDonut = Object.entries(lisaCounts).map(([k, v]) => ({ name: k, value: v }));

  return (
    <PageContainer title="空间集聚" subtitle="Moran's I 空间自相关 + LISA 局部空间聚集 + 中国地图交互">
      {/* Row 1: trend + donut */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <LineChart data={moranTrend} title="全局 Moran's I 变化 (2016-2024)" color="#8b5cf6" height={350} area />
        <DonutChart data={lisaDonut} title="LISA 类型分布 (2024)" centerText={`${moran.lisa_2024.length}省`} height={350} colors={["#10b981", "#ef4444", "#f59e0b", "#3b82f6", "#64748b"]} />
      </div>

      {/* Row 2: LISA table + map */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="bg-dark-card rounded-xl border border-dark-lighter p-4">
          <h3 className="text-sm font-semibold text-slate-300 mb-3">LISA 明细表 (2024年)</h3>
          <div className="overflow-x-auto max-h-[400px]">
            <table className="w-full text-xs">
              <thead><tr className="text-slate-400 border-b border-dark-lighter"><th className="text-left py-1.5 sticky top-0 bg-dark-card">省份</th><th className="text-right py-1.5">得分</th><th className="text-right py-1.5">Z值</th><th className="text-right py-1.5">Local I</th><th className="text-left py-1.5 pl-2">类型</th></tr></thead>
              <tbody>
                {moran.lisa_2024.map((d) => (
                  <tr key={d.province} className="border-b border-dark/40 hover:bg-dark-lighter/30">
                    <td className="py-1.5 text-slate-300 font-medium">{d.province}</td>
                    <td className="py-1.5 text-right font-mono text-slate-400">{d.composite_score?.toFixed(4)}</td>
                    <td className="py-1.5 text-right font-mono text-slate-400">{d.standardized_score_z?.toFixed(4)}</td>
                    <td className="py-1.5 text-right font-mono text-slate-400">{d.local_moran_i?.toFixed(4)}</td>
                    <td className="py-1.5 pl-2"><span className="px-1.5 py-0.5 rounded text-[10px] font-medium" style={{ backgroundColor: (LISA_COLORS[d.lisa_type || ""] || "#64748b") + "20", color: LISA_COLORS[d.lisa_type || ""] || "#64748b" }}>{d.lisa_type || "-"}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
        <div className="bg-dark-card rounded-xl border border-dark-lighter p-4 space-y-2">
          <h3 className="text-sm font-semibold text-slate-300 mb-2">LISA 类型说明</h3>
          {[
            { type: "高-高", color: "#10b981", desc: "高水平省份被高水平包围 — 空间正相关的\"热点\"区" },
            { type: "低-低", color: "#ef4444", desc: "低水平省份被低水平包围 — 空间正相关的\"冷点\"区" },
            { type: "高-低", color: "#f59e0b", desc: "高水平省份被低水平包围 — 空间负相关" },
            { type: "低-高", color: "#3b82f6", desc: "低水平省份被高水平包围 — 空间负相关" },
            { type: "不显著", color: "#64748b", desc: "无显著空间聚集特征" },
          ].map((item) => (
            <div key={item.type} className="flex items-start gap-2 text-xs">
              <span className="w-2.5 h-2.5 rounded-sm mt-0.5 flex-shrink-0" style={{ backgroundColor: item.color }} />
              <div><span className="text-slate-200 font-medium">{item.type}</span><span className="text-slate-500 ml-2">{item.desc}</span></div>
            </div>
          ))}
        </div>
      </div>

      {/* Row 3: China map */}
      <ChinaMap data={mapData} title="2024 年各省综合得分地理分布" height={550} />
    </PageContainer>
  );
}
