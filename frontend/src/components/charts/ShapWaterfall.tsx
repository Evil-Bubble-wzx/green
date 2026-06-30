"use client";

import ReactECharts from "echarts-for-react";

interface ShapItem {
  indicator_short_name: string | null;
  indicator_name: string | null;
  shap_value: number | null;
  abs_shap_value: number | null;
  dimension: string | null;
}

interface Props {
  data: ShapItem[];
  height?: number;
}

export default function ShapWaterfall({ data, height = 400 }: Props) {
  const names = data.map((d) => d.indicator_short_name || d.indicator_name || "");
  const values = data.map((d) => d.shap_value || 0);
  const colors = values.map((v) => (v >= 0 ? "#10b981" : "#ef4444"));

  const option = {
    tooltip: {
      trigger: "axis" as const,
      axisPointer: { type: "shadow" as const },
      formatter: (params: { name: string; value: number }[]) => {
        const p = params[0];
        const item = data.find((d) => (d.indicator_short_name || d.indicator_name) === p.name);
        return `${p.name}<br/>SHAP值：${p.value.toFixed(6)}<br/>维度：${item?.dimension ?? ""}`;
      },
    },
    grid: { left: 100, right: 40, top: 10, bottom: 30 },
    xAxis: {
      type: "value",
      name: "SHAP Value",
      nameTextStyle: { color: "#94a3b8" },
      axisLabel: { color: "#94a3b8" },
      splitLine: { lineStyle: { color: "#1e293b" } },
    },
    yAxis: {
      type: "category",
      data: names,
      axisLabel: { color: "#e2e8f0", fontSize: 11 },
      inverse: true,
    },
    series: [
      {
        type: "bar",
        data: values.map((v, i) => ({ value: v, itemStyle: { color: colors[i], borderRadius: [0, 4, 4, 0] } })),
        label: {
          show: true,
          position: "right",
          color: "#e2e8f0",
          fontSize: 10,
          formatter: (p: { value: number }) => (p.value >= 0 ? "+" : "") + p.value.toFixed(4),
        },
      },
    ],
  };

  return (
    <div className="bg-dark-card rounded-xl border border-dark-lighter p-4">
      <div className="flex items-center gap-3 mb-2">
        <h3 className="text-sm font-semibold text-slate-300">SHAP 因子贡献</h3>
        <span className="flex items-center gap-1 text-xs">
          <span className="w-3 h-3 rounded-sm bg-accent" /> 正向
          <span className="w-3 h-3 rounded-sm bg-danger ml-2" /> 负向
        </span>
      </div>
      <ReactECharts option={option} style={{ height }} />
    </div>
  );
}
