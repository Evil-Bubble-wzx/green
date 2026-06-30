"use client";
import { useEffect, useState } from "react";
import PageContainer from "@/components/PageContainer";
import LoadingSpinner from "@/components/LoadingSpinner";
import ErrorMessage from "@/components/ErrorMessage";
import AreaChart from "@/components/charts/AreaChart";
import LineChart from "@/components/charts/LineChart";
import { fetchMarkov, fetchScores, MarkovOut, ScoreListOut, MarkovProbItem } from "@/lib/api";

const STATES = ["低水平", "中低水平", "中高水平", "高水平"] as const;
function getProb(d: MarkovProbItem, state: string): number {
  const map: Record<string, number | null | undefined> = { "低水平": d.to_low_level_probability, "中低水平": d.to_mid_low_level_probability, "中高水平": d.to_mid_high_level_probability, "高水平": d.to_high_level_probability };
  return map[state] ?? 0;
}

export default function DynamicEvolutionPage() {
  const [markov, setMarkov] = useState<MarkovOut | null>(null);
  const [scores, setScores] = useState<ScoreListOut | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = () => { setLoading(true); setError(null); Promise.all([fetchMarkov(), fetchScores(2024)]).then(([m, s]) => { setMarkov(m); setScores(s); }).catch((e) => setError(e.message)).finally(() => setLoading(false)); };
  useEffect(() => { load(); }, []);

  if (loading) return <PageContainer title="动态演化"><LoadingSpinner /></PageContainer>;
  if (error) return <PageContainer title="动态演化"><ErrorMessage message={error} onRetry={load} /></PageContainer>;
  if (!markov || !scores) return <PageContainer title="动态演化"><div className="text-slate-400 text-center py-20">暂无数据</div></PageContainer>;

  // 2016→2024 得分变化趋势
  const scoreTrend = scores.scores.map((s) => ({ name: s.province, value: s.composite_score ?? 0 }));

  // Markov 转移热力 - 用面积图展示从各状态的流向概率
  const fromLow = STATES.map((to) => ({ name: `低水平→${to}`, value: getProb(markov.probability[0], to) }));
  const spatialUpgrade = markov.spatial.filter((d) => {
    const order = ["低水平", "中低水平", "中高水平", "高水平"];
    return order.indexOf(d.to_state || "") > order.indexOf(d.from_state || "");
  }).map((d) => ({ name: `${d.neighborhood_state}|${d.from_state}→${d.to_state}`, value: d.probability ?? 0 })).slice(0, 12);

  return (
    <PageContainer title="动态演化" subtitle="Markov 转移矩阵 + 省域得分趋势">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="bg-dark-card rounded-xl border border-dark-lighter overflow-hidden">
          <table className="w-full text-sm"><thead className="bg-dark-lighter"><tr>
            <th className="text-left px-4 py-3 text-slate-300">转移前</th>
            {STATES.map((s) => <th key={s} className="text-right px-3 py-3 text-slate-300 text-xs">{s}</th>)}
          </tr></thead><tbody>
            {markov.probability.map((d) => (
              <tr key={d.from_state} className="border-t border-dark-lighter hover:bg-dark-lighter/30">
                <td className="px-4 py-2.5 text-white font-medium">{d.from_state}</td>
                {STATES.map((s) => { const v = getProb(d, s); return <td key={s} className={`px-3 py-2.5 text-right font-mono text-xs ${v > 0.3 ? "text-accent font-bold" : "text-slate-400"}`}>{(v * 100).toFixed(1)}%</td>; })}
              </tr>
            ))}
          </tbody></table>
        </div>
        <AreaChart data={fromLow} title="低水平状态向各级转移概率" height={350} />
        <AreaChart data={scoreTrend} title="2024 年各省得分趋势" height={350} />
        <div className="bg-dark-card rounded-xl border border-dark-lighter p-4">
          <h3 className="text-sm font-semibold text-slate-300 mb-3">状态划分阈值</h3>
          {markov.thresholds.map((t) => (
            <div key={t.state} className="flex items-center justify-between text-sm py-1 border-b border-dark/40">
              <span className="text-white font-medium">{t.state}</span>
              <span className="text-slate-400 text-xs">{t.classification_rule}</span>
              <span className="text-slate-500 text-xs">{t.threshold_note}</span>
            </div>
          ))}
        </div>
      </div>
      <LineChart data={spatialUpgrade} title="空间 Markov 向上转移概率" color="#8b5cf6" height={350} area />
    </PageContainer>
  );
}
