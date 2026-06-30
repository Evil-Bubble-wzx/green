"use client";

import ReactECharts from "echarts-for-react";

interface Props {
  data: { region: string; avg_score: number; province_count: number }[];
  height?: number;
}

const REGION_COLORS: Record<string, string> = {
  "东部": "#0ea5e9",
  "中部": "#10b981",
  "西部": "#f59e0b",
  "东北": "#ef4444",
};

export default function RegionChart({ data, height = 350 }: Props) {
  const option = {
    tooltip: {
      trigger: "axis" as const,
      formatter: (params: { name: string; value: number }[]) => {
        const p = params[0];
        const item = data.find((d) => d.region === p.name);
        return `${p.name}<br/>平均得分：${p.value.toFixed(4)}<br/>省份数：${item?.province_count ?? ""}`;
      },
    },
    grid: { left: 60, right: 30, top: 10, bottom: 40 },
    xAxis: {
      type: "category",
      data: data.map((d) => d.region),
      axisLabel: { color: "#94a3b8", fontSize: 12 },
    },
    yAxis: {
      type: "value",
      name: "平均综合得分",
      nameTextStyle: { color: "#94a3b8" },
      axisLabel: { color: "#94a3b8" },
      splitLine: { lineStyle: { color: "#1e293b" } },
    },
    series: [
      {
        type: "bar",
        data: data.map((d) => ({
          value: d.avg_score,
          itemStyle: {
            color: REGION_COLORS[d.region] || "#0ea5e9",
            borderRadius: [6, 6, 0, 0],
          },
        })),
        label: {
          show: true,
          position: "top",
          color: "#e2e8f0",
          fontSize: 11,
          formatter: (p: { value: number }) => p.value.toFixed(4),
        },
      },
    ],
  };

  return (
    <div className="bg-dark-card rounded-xl border border-dark-lighter p-4">
      <h3 className="text-sm font-semibold text-slate-300 mb-2">区域平均得分对比</h3>
      <ReactECharts option={option} style={{ height }} />
    </div>
  );
}
