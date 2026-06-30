"use client";
import { useEffect, useState } from "react";
import PageContainer from "@/components/PageContainer";
import ProvinceSelector from "@/components/ProvinceSelector";
import LoadingSpinner from "@/components/LoadingSpinner";
import ErrorMessage from "@/components/ErrorMessage";
import EmptyState from "@/components/EmptyState";
import ShapWaterfall from "@/components/charts/ShapWaterfall";
import { fetchProvinces, fetchShap, ShapListOut } from "@/lib/api";

export default function ShapPage() {
  const [provinces, setProvinces] = useState<string[]>([]);
  const [selected, setSelected] = useState("上海");
  const [data, setData] = useState<ShapListOut | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => { fetchProvinces().then((d) => { const list = d.provinces.map((p) => p.province); setProvinces(list); if (!list.includes("上海")) setSelected(list[0] || ""); }).catch(() => {}); }, []);

  useEffect(() => {
    if (!selected) { setData(null); return; }
    setLoading(true); setError(null);
    fetchShap(selected, 2024).then(setData).catch((e) => setError(e.message)).finally(() => setLoading(false));
  }, [selected]);

  const deduped = data ? data.explanations.filter((item, idx, arr) => arr.findIndex((x) => x.indicator_name === item.indicator_name) === idx) : [];
  const positiveCount = deduped.filter((d) => (d.shap_value ?? 0) > 0).length;
  const negativeCount = deduped.filter((d) => (d.shap_value ?? 0) < 0).length;

  return (
    <PageContainer title="SHAP 解释" subtitle="模型可解释性分析 — 局部因子贡献 Top 8">
      <div className="flex items-center gap-4 mb-6"><ProvinceSelector provinces={provinces} value={selected} onChange={setSelected} loading={loading} /></div>
      {!selected && <EmptyState text="请选择一个省份查看 SHAP 解释结果" />}
      {loading && <LoadingSpinner />}
      {error && <ErrorMessage message={error} onRetry={() => setSelected(selected)} />}
      {data && !loading && !error && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="bg-dark-card border border-dark-lighter rounded-xl p-4 text-center"><p className="text-xs text-slate-400 mb-1">因子总数</p><p className="text-2xl font-bold text-white">{deduped.length}</p></div>
            <div className="bg-dark-card border border-dark-lighter rounded-xl p-4 text-center"><p className="text-xs text-slate-400 mb-1">正向贡献</p><p className="text-2xl font-bold text-accent">{positiveCount}</p></div>
            <div className="bg-dark-card border border-dark-lighter rounded-xl p-4 text-center"><p className="text-xs text-slate-400 mb-1">负向贡献</p><p className="text-2xl font-bold text-danger">{negativeCount}</p></div>
          </div>
          <ShapWaterfall data={deduped} height={500} />
          <div className="bg-dark-card rounded-xl border border-dark-lighter overflow-hidden"><table className="w-full text-sm"><thead className="bg-dark-lighter"><tr><th className="text-left px-4 py-3 text-slate-300">指标</th><th className="text-left px-4 py-3 text-slate-300">维度</th><th className="text-right px-4 py-3 text-slate-300">SHAP 值</th><th className="text-right px-4 py-3 text-slate-300">|SHAP|</th></tr></thead><tbody>
            {deduped.map((item, i) => (
              <tr key={i} className="border-t border-dark-lighter hover:bg-dark-lighter/30"><td className="px-4 py-2.5 text-white">{item.indicator_short_name || item.indicator_name || "-"}</td><td className="px-4 py-2.5 text-slate-400">{item.dimension ?? "-"}</td><td className="px-4 py-2.5 text-right font-mono"><span className={((item.shap_value ?? 0) >= 0) ? "text-accent" : "text-danger"}>{((item.shap_value ?? 0) >= 0 ? "+" : "")}{(item.shap_value ?? 0).toFixed(6)}</span></td><td className="px-4 py-2.5 text-right text-slate-400 font-mono">{item.abs_shap_value?.toFixed(6) ?? "-"}</td></tr>
            ))}
          </tbody></table></div>
        </div>
      )}
    </PageContainer>
  );
}
