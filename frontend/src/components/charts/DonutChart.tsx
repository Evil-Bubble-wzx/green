"use client";
import ReactECharts from "echarts-for-react";

interface Props {
  data: { name: string; value: number }[];
  title?: string;
  centerText?: string;
  height?: number;
  colors?: string[];
}

const DEFAULT_COLORS = ["#0ea5e9", "#10b981", "#f59e0b", "#8b5cf6"];

export default function DonutChart({ data, title, centerText = "区域均值", height = 380, colors }: Props) {
  const option = {
    title: title ? { text: title, left: "center", top: 5, textStyle: { color: "#e2e8f0", fontSize: 14 } } : undefined,
    tooltip: {
      trigger: "item" as const,
      backgroundColor: "rgba(15,23,42,0.95)",
      borderColor: "#334155",
      textStyle: { color: "#e2e8f0", fontSize: 12 },
      formatter: (p: { name: string; value: number; percent: number }) =>
        `<b>${p.name}</b><br/>平均得分：${p.value.toFixed(4)}<br/>占比：${p.percent.toFixed(1)}%`,
    },
    legend: { bottom: 0, textStyle: { color: "#94a3b8", fontSize: 11 }, itemGap: 16 },
    series: [{
      type: "pie",
      radius: ["50%", "72%"],
      center: ["50%", "48%"],
      avoidLabelOverlap: false,
      itemStyle: { borderRadius: 4, borderColor: "#0f172a", borderWidth: 3 },
      label: { show: false },
      emphasis: {
        label: { show: true, fontSize: 14, fontWeight: "bold", color: "#fff" },
        scaleSize: 12,
        focus: "self" as const,
      },
      data: data.map((d, i) => ({
        ...d,
        itemStyle: { color: (colors || DEFAULT_COLORS)[i % (colors || DEFAULT_COLORS).length] },
      })),
      animationType: "scale" as const,
      animationEasing: "elasticOut" as const,
    }],
    graphic: centerText ? [{
      type: "text" as const, left: "center", top: "42%",
      style: { text: centerText, textAlign: "center", fill: "#94a3b8", fontSize: 12 },
    }] : undefined,
  };

  return <div className="bg-dark-card rounded-xl border border-dark-lighter p-4"><ReactECharts option={option} style={{ height }} /></div>;
}
