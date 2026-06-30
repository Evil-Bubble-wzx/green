"use client";
import ReactECharts from "echarts-for-react";

interface Props {
  data: { name: string; value: number }[];
  title?: string;
  height?: number;
}

const COLORS = ["#0ea5e9", "#10b981", "#f59e0b", "#8b5cf6", "#ec4899", "#06b6d4"];

export default function RoseChart({ data, title, height = 400 }: Props) {
  const option = {
    title: title ? { text: title, left: "center", top: 5, textStyle: { color: "#e2e8f0", fontSize: 14 } } : undefined,
    tooltip: {
      trigger: "item" as const,
      backgroundColor: "rgba(15,23,42,0.95)",
      borderColor: "#334155",
      textStyle: { color: "#e2e8f0", fontSize: 12 },
      formatter: (p: { name: string; value: number }) => `<b>${p.name}</b><br/>平均得分：${p.value.toFixed(4)}`,
    },
    legend: { bottom: 0, textStyle: { color: "#94a3b8", fontSize: 11 } },
    series: [{
      type: "pie",
      roseType: "area" as const,
      radius: ["15%", "72%"],
      center: ["50%", "48%"],
      itemStyle: { borderRadius: 4, borderColor: "#0f172a", borderWidth: 2 },
      label: { color: "#94a3b8", fontSize: 10 },
      emphasis: { scaleSize: 10, focus: "self" as const, label: { fontSize: 14, fontWeight: "bold", color: "#fff" } },
      data: data.map((d, i) => ({ ...d, itemStyle: { color: COLORS[i % COLORS.length] } })),
      animationType: "scale" as const,
      animationEasing: "elasticOut" as const,
    }],
  };

  return <div className="bg-dark-card rounded-xl border border-dark-lighter p-4"><ReactECharts option={option} style={{ height }} /></div>;
}
