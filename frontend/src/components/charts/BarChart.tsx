"use client";

import ReactECharts from "echarts-for-react";

interface Props {
  data: { name: string; value: number }[];
  title?: string;
  color?: string;
  height?: number;
  horizontal?: boolean;
}

export default function BarChart({ data, title, color = "#0ea5e9", height = 400, horizontal }: Props) {
  const option = {
    title: title
      ? { text: title, left: "center", textStyle: { color: "#e2e8f0", fontSize: 14 } }
      : undefined,
    tooltip: { trigger: "axis" as const },
    grid: { left: horizontal ? 100 : 50, right: 30, top: title ? 40 : 10, bottom: horizontal ? 30 : 60 },
    [horizontal ? "yAxis" : "xAxis"]: {
      type: "category",
      data: data.map((d) => d.name),
      axisLabel: { color: "#94a3b8", fontSize: 11, rotate: horizontal ? 0 : 45 },
    },
    [horizontal ? "xAxis" : "yAxis"]: {
      type: "value",
      axisLabel: { color: "#94a3b8" },
      splitLine: { lineStyle: { color: "#1e293b" } },
    },
    series: [
      {
        type: "bar",
        data: data.map((d) => d.value),
        itemStyle: {
          color,
          borderRadius: [4, 4, 0, 0],
        },
        emphasis: {
          itemStyle: { color: "#38bdf8" },
        },
      },
    ],
  };

  return (
    <div className="bg-dark-card rounded-xl border border-dark-lighter p-4">
      <ReactECharts option={option} style={{ height }} />
    </div>
  );
}
