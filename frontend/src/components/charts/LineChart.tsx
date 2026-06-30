"use client";
import ReactECharts from "echarts-for-react";

interface Props {
  data: { name: string; value: number }[];
  title?: string;
  color?: string;
  height?: number;
  area?: boolean;
}

export default function LineChart({ data, title, color = "#0ea5e9", height = 350, area = true }: Props) {
  const option = {
    title: title ? { text: title, left: "center", top: 5, textStyle: { color: "#e2e8f0", fontSize: 14 } } : undefined,
    tooltip: {
      trigger: "axis" as const,
      backgroundColor: "rgba(15,23,42,0.95)",
      borderColor: "#334155",
      textStyle: { color: "#e2e8f0", fontSize: 12 },
    },
    grid: { left: 60, right: 30, top: title ? 40 : 15, bottom: 30 },
    xAxis: { type: "category", data: data.map((d) => d.name), axisLabel: { color: "#94a3b8", fontSize: 10, rotate: 30 } },
    yAxis: { type: "value", axisLabel: { color: "#94a3b8" }, splitLine: { lineStyle: { color: "#1e293b" } } },
    series: [{
      type: "line",
      data: data.map((d) => d.value),
      smooth: true,
      symbol: "circle",
      symbolSize: 6,
      lineStyle: { color, width: 2 },
      itemStyle: { color, borderColor: "#0f172a", borderWidth: 2 },
      areaStyle: area ? { color: { type: "linear" as const, x: 0, y: 0, x2: 0, y2: 1, colorStops: [{ offset: 0, color: color + "40" }, { offset: 1, color: color + "05" }] } } : undefined,
      emphasis: { focus: "series" as const },
    }],
    animationEasing: "cubicOut" as const,
  };

  return <div className="bg-dark-card rounded-xl border border-dark-lighter p-4"><ReactECharts option={option} style={{ height }} /></div>;
}
