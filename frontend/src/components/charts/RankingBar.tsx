"use client";
import ReactECharts from "echarts-for-react";

interface Props {
  data: { name: string; value: number }[];
  title?: string;
  height?: number;
}

export default function RankingBar({ data, title, height = 750 }: Props) {
  const sorted = [...data].sort((a, b) => b.value - a.value);
  const names = sorted.map((d) => d.name);
  const values = sorted.map((d) => d.value);

  const option = {
    title: title ? { text: title, left: "center", top: 5, textStyle: { color: "#e2e8f0", fontSize: 14 } } : undefined,
    tooltip: {
      trigger: "axis" as const,
      backgroundColor: "rgba(15,23,42,0.95)",
      borderColor: "#334155",
      textStyle: { color: "#e2e8f0", fontSize: 12 },
      formatter: (p: { name: string; value: number; dataIndex: number }[]) => {
        const d = p[0]; const rank = d.dataIndex + 1;
        let medal = rank === 1 ? "🥇" : rank === 2 ? "🥈" : rank === 3 ? "🥉" : `#${rank}`;
        return `${medal} <b>${d.name}</b><br/>综合得分：${d.value.toFixed(6)}`;
      },
    },
    grid: { left: 110, right: 60, top: title ? 40 : 10, bottom: 10 },
    xAxis: {
      type: "value",
      axisLabel: { color: "#94a3b8", fontSize: 10 },
      splitLine: { lineStyle: { color: "#1e293b", type: "dashed" } },
      max: Math.ceil(Math.max(...values) * 10) / 10,
    },
    yAxis: {
      type: "category",
      data: names,
      axisLabel: { color: "#e2e8f0", fontSize: 11 },
      axisLine: { lineStyle: { color: "#334155" } },
      inverse: true,
      position: "left",
    },
    series: [{
      type: "bar",
      data: values.map((v, i) => {
        let color = i === 0 ? "#f59e0b" : i === 1 ? "#94a3b8" : i === 2 ? "#d97706" : "#0ea5e9";
        return { value: v, itemStyle: { color, borderRadius: [0, 4, 4, 0], opacity: i < 3 ? 1 : 0.7 } };
      }),
      barWidth: "60%",
      label: {
        show: true, position: "right", color: "#94a3b8", fontSize: 10,
        formatter: (p: { value: number; dataIndex: number }) => {
          const rank = p.dataIndex + 1;
          return rank <= 3 ? `🥇${p.value.toFixed(4)}` : p.value.toFixed(4);
        },
      },
      emphasis: {
        itemStyle: { shadowBlur: 10, shadowColor: "rgba(14,165,233,0.5)" },
        label: { fontSize: 12, fontWeight: "bold" },
      },
      animationDelay: (idx: number) => idx * 30,
    }],
  };

  return <div className="bg-dark-card rounded-xl border border-dark-lighter p-4"><ReactECharts option={option} style={{ height }} /></div>;
}
