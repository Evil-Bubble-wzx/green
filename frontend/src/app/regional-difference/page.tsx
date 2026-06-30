"use client";
import { useEffect, useState } from "react";
import PageContainer from "@/components/PageContainer";
import LoadingSpinner from "@/components/LoadingSpinner";
import ErrorMessage from "@/components/ErrorMessage";
import LineChart from "@/components/charts/LineChart";
import BarChart from "@/components/charts/BarChart";
import RankingBar from "@/components/charts/RankingBar";
import StackedBar from "@/components/charts/StackedBar";
import { fetchDagum, DagumOut } from "@/lib/api";

export default function RegionalDifferencePage() {
  const [data, setData] = useState<DagumOut | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const load = () => { setLoading(true); setError(null); fetchDagum().then(setData).catch((e) => setError(e.message)).finally(() => setLoading(false)); };
  useEffect(() => { load(); }, []);
  if (loading) return <PageContainer title="区域差异"><LoadingSpinner /></PageContainer>;
  if (error) return <PageContainer title="区域差异"><ErrorMessage message={error} onRetry={load} /></PageContainer>;
  if (!data) return <PageContainer title="区域差异"><div className="text-slate-400 text-center py-20">暂无数据</div></PageContainer>;

  // 图1: 折线面积图 - 总体基尼系数趋势
  const giniTrend = data.decomposition.map((d) => ({ name: String(d.year), value: d.total_gini ?? 0 }));
  // 图2: 堆叠柱状图 - 差异贡献率逐年分解
  const contribYears = data.decomposition.map((d) => String(d.year));
  const intraData = data.decomposition.map((d) => (d.intra_region_contribution_rate ?? 0) * 100);
  const interData = data.decomposition.map((d) => (d.inter_region_contribution_rate ?? 0) * 100);
  const hyperData = data.decomposition.map((d) => (d.hypervariable_density_contribution_rate ?? 0) * 100);
  // 图3: 横向排名条 - 区域间基尼系数
  const inter2024 = data.inter_region.filter((d) => d.year === 2024).map((d) => ({ name: d.region_pair, value: d.inter_region_gini ?? 0 })).sort((a, b) => b.value - a.value);
  // 图4: 区域内基尼
  const intra2024 = data.intra_region.filter((d) => d.year === 2024).map((d) => ({ name: d.region, value: d.intra_region_gini ?? 0 }));

  return (
    <PageContainer title="区域差异" subtitle="Dagum 基尼系数分解 — 四大区域差异来源分析">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <LineChart data={giniTrend} title="总体基尼系数变化趋势 (2016-2024)" color="#0ea5e9" height={350} area />
        <StackedBar
          categories={contribYears}
          title="差异贡献率逐年分解"
          height={350}
          series={[
            { name: "区域内差异", data: intraData, color: "#0ea5e9" },
            { name: "区域间净差异", data: interData, color: "#10b981" },
            { name: "超变密度", data: hyperData, color: "#8b5cf6" },
          ]}
        />
        <RankingBar data={inter2024} title="区域间基尼系数对比 (2024)" height={380} />
        <BarChart data={intra2024} title="区域内基尼系数 (2024)" color="#10b981" height={350} />
      </div>
    </PageContainer>
  );
}
