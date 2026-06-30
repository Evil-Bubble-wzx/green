"use client";
import { useEffect, useState } from "react";
import PageContainer from "@/components/PageContainer";
import LoadingSpinner from "@/components/LoadingSpinner";
import ErrorMessage from "@/components/ErrorMessage";
import RankingBar from "@/components/charts/RankingBar";
import RoseChart from "@/components/charts/RoseChart";
import { fetchScores, fetchOverview, ScoreListOut, OverviewOut } from "@/lib/api";

export default function EvaluationPage() {
  const [scores, setScores] = useState<ScoreListOut | null>(null);
  const [overview, setOverview] = useState<OverviewOut | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = () => { setLoading(true); setError(null); Promise.all([fetchScores(2024), fetchOverview(2024)]).then(([s, o]) => { setScores(s); setOverview(o); }).catch((e) => setError(e.message)).finally(() => setLoading(false)); };
  useEffect(() => { load(); }, []);

  if (loading) return <PageContainer title="综合评价"><LoadingSpinner /></PageContainer>;
  if (error) return <PageContainer title="综合评价"><ErrorMessage message={error} onRetry={load} /></PageContainer>;
  if (!scores) return <PageContainer title="综合评价"><div className="text-slate-400 text-center py-20">暂无数据</div></PageContainer>;

  const scoreData = scores.scores.map((s) => ({ name: s.province, value: s.composite_score ?? 0 }));
  const regionData = overview ? overview.region_averages.map((r) => ({ name: r.region, value: r.avg_score })) : [];

  return (
    <PageContainer title="综合评价" subtitle="TOPSIS 绿色算力综合得分与排名">
      <div className="bg-dark-card rounded-xl border border-dark-lighter overflow-hidden mb-6">
        <div className="overflow-x-auto max-h-[500px]">
          <table className="w-full text-sm"><thead className="sticky top-0 bg-dark-lighter"><tr>
            <th className="text-left px-4 py-3 text-slate-300">排名</th><th className="text-left px-4 py-3 text-slate-300">省份</th><th className="text-right px-4 py-3 text-slate-300">综合得分</th><th className="text-right px-4 py-3 text-slate-300">年份</th>
          </tr></thead><tbody>
            {scores.scores.map((s, i) => (
              <tr key={s.province} className={`border-t border-dark-lighter hover:bg-dark-lighter/50 ${i < 3 ? "bg-primary/5" : ""}`}>
                <td className="px-4 py-2.5"><span className={`inline-flex items-center justify-center w-7 h-7 rounded-full text-xs font-bold ${i === 0 ? "bg-amber-400/20 text-amber-400" : i === 1 ? "bg-slate-400/20 text-slate-300" : i === 2 ? "bg-orange-400/20 text-orange-400" : "text-slate-500"}`}>{s.rank ?? i + 1}</span></td>
                <td className="px-4 py-2.5 text-white font-medium">{s.province}</td>
                <td className="px-4 py-2.5 text-right text-slate-300 font-mono">{s.composite_score?.toFixed(6) ?? "-"}</td>
                <td className="px-4 py-2.5 text-right text-slate-500">{s.year}</td>
              </tr>
            ))}
          </tbody></table>
        </div>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <RoseChart data={regionData} title="区域平均得分（南丁格尔玫瑰图）" height={400} />
        <RankingBar data={scoreData} title="各省综合得分排名" height={500} />
      </div>
    </PageContainer>
  );
}
