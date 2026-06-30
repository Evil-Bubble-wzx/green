"use client";
import ReactECharts from "echarts-for-react";

interface Props {
  data: { name: string; value: number }[];
  title?: string;
  height?: number;
}

export default function AreaChart({ data, title, height = 350 }: Props) {
  const option = {
    title: title ? { text: title, left: "center", top: 5, textStyle: { color: "#e2e8f0", fontSize: 14 } } : undefined,
    tooltip: {
      trigger: "axis" as const,
      backgroundColor: "rgba(15,23,42,0.95)",
      borderColor: "#334155",
      textStyle: { color: "#e2e8f0", fontSize: 12 },
    },
    grid: { left: 60, right: 30, top: title ? 40 : 15, bottom: 30 },
    xAxis: { type: "category", data: data.map((d) => d.name), axisLabel: { color: "#94a3b8", fontSize: 10 } },
    yAxis: { type: "value", axisLabel: { color: "#94a3b8" }, splitLine: { lineStyle: { color: "#1e293b" } } },
    series: [{
      type: "line",
      data: data.map((d) => d.value),
      smooth: true,
      symbol: "circle",
      symbolSize: 4,
      lineStyle: { color: "#10b981", width: 2 },
      itemStyle: { color: "#10b981" },
      areaStyle: {
        color: {
          type: "linear" as const, x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: "rgba(16,185,129,0.4)" },
            { offset: 0.5, color: "rgba(14,165,233,0.15)" },
            { offset: 1, color: "rgba(139,92,246,0.05)" },
          ],
        },
      },
      emphasis: { focus: "series" as const },
    }],
    animationEasing: "cubicOut" as const,
  };

  return <div className="bg-dark-card rounded-xl border border-dark-lighter p-4"><ReactECharts option={option} style={{ height }} /></div>;
}
