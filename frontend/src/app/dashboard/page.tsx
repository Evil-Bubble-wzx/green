"use client";
import { useEffect, useState } from "react";
import PageContainer from "@/components/PageContainer";
import StatCard from "@/components/StatCard";
import LoadingSpinner from "@/components/LoadingSpinner";
import ErrorMessage from "@/components/ErrorMessage";
import DonutChart from "@/components/charts/DonutChart";
import RankingBar from "@/components/charts/RankingBar";
import { fetchOverview, fetchScores, OverviewOut, ScoreListOut } from "@/lib/api";

export default function DashboardPage() {
  const [overview, setOverview] = useState<OverviewOut | null>(null);
  const [scores, setScores] = useState<ScoreListOut | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = () => {
    setLoading(true); setError(null);
    Promise.all([fetchOverview(2024), fetchScores(2024)])
      .then(([o, s]) => { setOverview(o); setScores(s); })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  };
  useEffect(() => { load(); }, []);

  if (loading) return <PageContainer title="首页总览"><LoadingSpinner /></PageContainer>;
  if (error) return <PageContainer title="首页总览"><ErrorMessage message={error} onRetry={load} /></PageContainer>;
  if (!overview || !scores) return <PageContainer title="首页总览"><div className="text-slate-400 text-center py-20">暂无数据</div></PageContainer>;

  const regionData = overview.region_averages.map((r) => ({ name: r.region, value: r.avg_score }));
  const scoreData = scores.scores.map((s) => ({ name: s.province, value: s.composite_score ?? 0 }));

  return (
    <PageContainer title="首页总览" subtitle={`${overview.year} 年全国绿色算力承载能力概览`}>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <StatCard label="全国平均得分" value={overview.national_avg_score?.toFixed(4) ?? "-"} color="blue" />
        <StatCard label="最高省份" value={overview.highest_province ?? "-"} sub={`得分：${overview.highest_score?.toFixed(4) ?? "-"}`} color="green" />
        <StatCard label="最低省份" value={overview.lowest_province ?? "-"} sub={`得分：${overview.lowest_score?.toFixed(4) ?? "-"}`} color="amber" />
        <StatCard label="区域数量" value={overview.region_averages.length} sub="东部 / 中部 / 西部 / 东北" color="red" />
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <DonutChart data={regionData} title="区域平均得分分布" centerText="区域均值" height={380} />
        <div className="bg-dark-card rounded-xl border border-dark-lighter p-4 flex items-center justify-center">
          <div className="text-center space-y-2">
            <div className="text-4xl">🌿</div>
            <p className="text-slate-300 font-semibold">绿色算力承载能力</p>
            <p className="text-2xl font-bold text-white">{overview.national_avg_score?.toFixed(4)}</p>
            <p className="text-xs text-slate-500">全国平均综合得分 · {overview.year}年</p>
            <div className="flex gap-4 justify-center text-xs text-slate-400 mt-2">
              <div>🏆 {overview.highest_province}</div>
              <div>📊 {overview.top10.length}省入前十</div>
            </div>
          </div>
        </div>
      </div>
      <RankingBar data={scoreData} title="31 省综合得分排名" height={800} />
    </PageContainer>
  );
}
