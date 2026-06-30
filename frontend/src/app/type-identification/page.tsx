"use client";
import { useEffect, useState } from "react";
import PageContainer from "@/components/PageContainer";
import LoadingSpinner from "@/components/LoadingSpinner";
import ErrorMessage from "@/components/ErrorMessage";
import RankingBar from "@/components/charts/RankingBar";
import { fetchLpa, LpaListOut } from "@/lib/api";

const TYPE_COLORS: Record<string, string> = { "高位领先型": "#10b981", "优势支撑型": "#0ea5e9", "中位追赶型": "#f59e0b", "基础培育型": "#8b5cf6" };

export default function TypeIdentificationPage() {
  const [data, setData] = useState<LpaListOut | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const load = () => { setLoading(true); setError(null); fetchLpa().then(setData).catch((e) => setError(e.message)).finally(() => setLoading(false)); };
  useEffect(() => { load(); }, []);
  if (loading) return <PageContainer title="类型识别"><LoadingSpinner /></PageContainer>;
  if (error) return <PageContainer title="类型识别"><ErrorMessage message={error} onRetry={load} /></PageContainer>;
  if (!data) return <PageContainer title="类型识别"><div className="text-slate-400 text-center py-20">暂无数据</div></PageContainer>;

  // Sort descending
  const scoreData = [...data.province_assignments].sort((a, b) => (b.mean_2016_2024 ?? 0) - (a.mean_2016_2024 ?? 0)).map((p) => ({ name: p.province, value: p.mean_2016_2024 ?? 0 }));
  const incrementData = [...data.province_assignments].sort((a, b) => (b.stage_increment ?? 0) - (a.stage_increment ?? 0)).map((p) => ({ name: p.province, value: p.stage_increment ?? 0 }));

  return (
    <PageContainer title="类型识别" subtitle="LPA 潜在剖面分析 — 31 省四种发展类型识别">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {data.type_summary.map((t) => (
          <div key={t.type_name} className="bg-dark-card rounded-xl border border-dark-lighter p-4" style={{ borderLeftWidth: 4, borderLeftColor: TYPE_COLORS[t.type_name || ""] || "#64748b" }}>
            <p className="text-xs text-slate-400 mb-1">{t.type_name}</p>
            <p className="text-2xl font-bold text-white">{t.province_count}<span className="text-sm text-slate-500 ml-1">省</span></p>
            <p className="text-xs text-slate-500 mt-1">均值 {t.mean_2024?.toFixed(4)}</p>
          </div>
        ))}
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <RankingBar data={scoreData} title="各省 2016-2024 平均得分（高→低）" height={800} />
        <RankingBar data={incrementData} title="各省阶段增量 2016→2024（高→低）" height={800} />
      </div>
      <div className="bg-dark-card rounded-xl border border-dark-lighter overflow-hidden">
        <table className="w-full text-sm"><thead className="bg-dark-lighter"><tr>
          <th className="text-left px-4 py-3 text-slate-300">省份</th><th className="text-left px-4 py-3 text-slate-300">LPA 类型</th><th className="text-right px-4 py-3 text-slate-300">2016</th><th className="text-right px-4 py-3 text-slate-300">2024</th><th className="text-right px-4 py-3 text-slate-300">增量</th><th className="text-right px-4 py-3 text-slate-300">后验概率</th>
        </tr></thead><tbody>
          {data.province_assignments.map((p) => (
            <tr key={p.province} className="border-t border-dark-lighter hover:bg-dark-lighter/30">
              <td className="px-4 py-2 text-white font-medium">{p.province}</td>
              <td className="px-4 py-2"><span className="px-2 py-0.5 rounded text-xs font-medium" style={{ background: (TYPE_COLORS[p.type_name || ""] || "#64748b") + "20", color: TYPE_COLORS[p.type_name || ""] || "#64748b" }}>{p.type_name}</span></td>
              <td className="px-4 py-2 text-right text-slate-300 font-mono">{p.score_2016?.toFixed(4)}</td>
              <td className="px-4 py-2 text-right text-slate-300 font-mono">{p.score_2024?.toFixed(4)}</td>
              <td className={`px-4 py-2 text-right font-mono ${(p.stage_increment ?? 0) > 0.15 ? "text-accent" : "text-slate-400"}`}>{p.stage_increment?.toFixed(4)}</td>
              <td className="px-4 py-2 text-right text-slate-500">{p.max_posterior_probability?.toFixed(2)}</td>
            </tr>
          ))}
        </tbody></table>
      </div>
    </PageContainer>
  );
}
