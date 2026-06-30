"use client";
import { useEffect, useState } from "react";
import PageContainer from "@/components/PageContainer";
import ProvinceSelector from "@/components/ProvinceSelector";
import LoadingSpinner from "@/components/LoadingSpinner";
import ErrorMessage from "@/components/ErrorMessage";
import EmptyState from "@/components/EmptyState";
import StatCard from "@/components/StatCard";
import RankingBar from "@/components/charts/RankingBar";
import DonutChart from "@/components/charts/DonutChart";
import { fetchProvinces, fetchProvinceProfile, fetchObstacles, ProvinceProfile, ObstacleProvince } from "@/lib/api";

export default function ProvinceDiagnosisPage() {
  const [provinces, setProvinces] = useState<string[]>([]);
  const [selected, setSelected] = useState("上海");
  const [profile, setProfile] = useState<ProvinceProfile | null>(null);
  const [obstacle, setObstacle] = useState<ObstacleProvince | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => { fetchProvinces().then((d) => { const list = d.provinces.map((p) => p.province); setProvinces(list); if (!list.includes("上海")) setSelected(list[0] || ""); }).catch(() => {}); }, []);

  useEffect(() => {
    if (!selected) return;
    setLoading(true); setError(null);
    Promise.all([fetchProvinceProfile(selected, 2024), fetchObstacles(selected)])
      .then(([p, o]) => { setProfile(p); setObstacle(o); })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [selected]);

  const obstacleData = obstacle ? [
    { name: obstacle.primary_obstacle_dimension || "未知", value: obstacle.primary_obstacle_degree || 0 },
    { name: obstacle.secondary_obstacle_dimension || "未知", value: obstacle.secondary_obstacle_degree || 0 },
  ].filter((d) => d.value > 0) : [];

  return (
    <PageContainer title="省域诊断" subtitle="省份综合画像与障碍因素诊断">
      <div className="flex items-center gap-4 mb-6">
        <ProvinceSelector provinces={provinces} value={selected} onChange={setSelected} loading={loading} />
      </div>
      {!selected && <EmptyState text="请选择一个省份查看诊断结果" />}
      {loading && <LoadingSpinner />}
      {error && <ErrorMessage message={error} onRetry={() => setSelected(selected)} />}
      {profile && obstacle && !loading && !error && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <StatCard label="综合得分" value={profile.composite_score?.toFixed(4) ?? "-"} color="blue" />
            <StatCard label="全国排名" value={`#${profile.rank ?? "-"}`} color="green" />
            <StatCard label="区域" value={profile.region ?? "-"} color="amber" />
            <StatCard label="LPA 类型" value={profile.type_name ?? "-"} sub={profile.lpa_type ?? ""} color="red" />
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="bg-dark-card rounded-xl border border-dark-lighter p-5">
              <h3 className="text-sm font-semibold text-slate-300 mb-3">障碍因素诊断</h3>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between"><span className="text-slate-400">首要障碍维度</span><span className="text-white font-medium">{obstacle.primary_obstacle_dimension ?? "-"}</span></div>
                <div className="flex justify-between"><span className="text-slate-400">首要障碍度</span><span className="text-warning font-mono">{obstacle.primary_obstacle_degree?.toFixed(2) ?? "-"}%</span></div>
                <div className="flex justify-between"><span className="text-slate-400">次要障碍维度</span><span className="text-white font-medium">{obstacle.secondary_obstacle_dimension ?? "-"}</span></div>
                <div className="flex justify-between"><span className="text-slate-400">次要障碍度</span><span className="text-slate-300 font-mono">{obstacle.secondary_obstacle_degree?.toFixed(2) ?? "-"}%</span></div>
                <div className="flex justify-between border-t border-dark-lighter pt-3"><span className="text-slate-400">短板诊断类型</span><span className="text-accent font-semibold">{obstacle.weakness_diagnosis_type ?? "-"}</span></div>
              </div>
            </div>
            <div className="bg-dark-card rounded-xl border border-dark-lighter p-5 lg:col-span-1">
              <h3 className="text-sm font-semibold text-slate-300 mb-3">布局建议</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between"><span className="text-slate-400">推荐布局</span><span className="text-primary-light font-semibold">{profile.recommended_layout_type ?? "-"}</span></div>
                <div className="flex justify-between"><span className="text-slate-400">布局导向</span><span className="text-white">{profile.layout_orientation ?? "-"}</span></div>
                <div className="border-t border-dark-lighter pt-2"><p className="text-slate-400 text-xs mb-1">功能定位</p><p className="text-white text-sm">{profile.functional_positioning ?? "-"}</p></div>
                <div><p className="text-slate-400 text-xs mb-1">优化策略</p><p className="text-white text-sm">{profile.optimization_strategy ?? "-"}</p></div>
                {profile.risk_warning && <div className="border-t border-dark-lighter pt-2"><p className="text-danger text-xs mb-1">⚠ 风险提示</p><p className="text-danger text-sm">{profile.risk_warning}</p></div>}
              </div>
            </div>
            <RankingBar data={obstacleData} title="主要障碍因素" height={280} />
          </div>
        </div>
      )}
    </PageContainer>
  );
}
